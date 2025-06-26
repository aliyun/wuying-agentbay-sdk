import { AgentBay, Session,Context } from '../../src';
import { getTestApiKey, randomString } from '../utils/test-helpers';
import { log } from '../../src/utils/logger';

// Define Node.js process if it's not available
declare var process: {
  env: {
    [key: string]: string | undefined;
  }
};

// Helper function to check if a string contains "tool not found"
function containsToolNotFound(s: string): boolean {
  return s.toLowerCase().includes("tool not found");
}

// Helper function to check if a string contains "context not found"
function containsContextNotFoundError(s: string): boolean {
  return s.toLowerCase().includes("context not found");
}

describe('Context Persistence Integration', () => {
  let agentBay: AgentBay;
  let testContextName: string;
  let testContextId: string | null = null;
  let testContext: Context | null;
  const testFilePath = `~/test-file-${Date.now()}.txt`;
  const testFileContent = "This is a test file for context persistence";
  const testFileMode = "664"; // Read and write for owner only

  beforeEach(async () => {
    const apiKey = getTestApiKey();
    agentBay = new AgentBay({ apiKey });
    testContextName = `test-context-${randomString()}`;
    
    // List existing contexts before creation
    try {
      const existingContexts = await agentBay.context.list();
      log(`Found ${existingContexts.length} existing contexts before creation`);
    } catch (error) {
      log(`Warning: Failed to list existing contexts: ${error}`);
      testContext = null;
    }

    // Create test context
    try {
      testContext = await agentBay.context.create(testContextName);
      testContextId = testContext.id;
      log(`Context created successfully - ID: ${testContextId}, Name: ${testContext.name}, State: ${testContext.state}, OSType: ${testContext.osType}`);
    } catch (error) {
      throw new Error(`Error creating context: ${error}`);
    }
  });

  afterEach(async () => {
    if (testContext) {
      // Delete the test context
      log(`Cleaning up: Deleting test context: ${testContextName}`);
      try {
        await agentBay.context.delete(testContext);
        log(`Context ${testContextId} deleted successfully`);
      } catch (error) {
        log(`Warning: Error deleting context: ${error}`);
      }
    }
  });

  it('should persist files between sessions in the same context', async () => {
    // Add describe info
    log('Test Case: Verifying file persistence between sessions in the same context');
    if (!testContextId) {
      log('Skipping test as test context creation failed');
      throw new Error('Test context creation failed');
    }

    // Create first session with the test context
    let session1: Session | null = null;
    try {
      session1 = await agentBay.create({imageId:'linux_latest', contextId: testContextId });
      log(`First session created with ID: ${session1.sessionId}`);

      // Check if file exists before creating it
      const checkCmd = `ls -la ${testFilePath} 2>&1 || echo 'File does not exist'`;
      const checkOutput = await session1.command?.executeCommand(checkCmd);
      log(`Pre-check output: ${checkOutput}`);

      // Create test file
      const createFileCmd = `echo '${testFileContent}' > ${testFilePath}`;
      const createOutput = await session1.command?.executeCommand(createFileCmd);
      log(`File creation output: ${createOutput}`);

      // Verify the file was created
      const verifyCmd = `cat ${testFilePath}`;
      const verifyOutput = await session1.command?.executeCommand(verifyCmd);
      log(`File content: ${verifyOutput}`);
      // Check file permissions
      const modeCmd = `stat -c "%a" ${testFilePath}`;
      const modeOutput = await session1.command?.executeCommand(modeCmd);
      log(`File mode: ${modeOutput}`);

      // Also check file attributes
      const lsCmd = `ls -la ${testFilePath}`;
      const lsOutput = await session1.command?.executeCommand(lsCmd);
      if (lsOutput) {
        log(`File attributes: ${lsOutput}`);
      }

      if (!verifyOutput || !verifyOutput.includes(testFileContent)) {
        throw new Error(`File content verification failed. Expected to contain '${testFileContent}', got: '${verifyOutput}'`);
      }

      // Release the first session
      await session1.delete();
    } catch (error) {
      if (session1) {
        await session1.delete();
      }
      throw error;
    }

    // Wait for 30 seconds to ensure the session is fully released and persisted
    log('Waiting for 30 seconds before creating the second session...');
    await new Promise(resolve => setTimeout(resolve, 30000));

    // List active sessions before creating second session
    try {
      const activeSessions = await agentBay.list();
      log(`Found ${activeSessions.length} active sessions before second session creation`);
    } catch (error) {
      log(`Warning: Failed to list active sessions: ${error}`);
    }

    // Create second session with the same context ID
    let session2: Session | null = null;
    try {
      session2 = await agentBay.create({imageId:'linux_latest', contextId: testContextId });
      log(`Second session created with ID: ${session2.sessionId}`);

      // Verify the file still exists
      const verifyCmd = `cat ${testFilePath}`;
      const verifyOutput = await session2.command?.executeCommand(verifyCmd);
      if (!verifyOutput || !verifyOutput.includes(testFileContent)) {
        throw new Error(`File persistence test failed. Expected file to exist with content '${testFileContent}', got: '${verifyOutput}'`);
      }
      
      log(`File persistence verified: file exists in the second session`);
    } finally {
      if (session2) {
        await session2.delete();
      }
    }
  });

  it('should isolate files between different contexts', async () => {
    // Add describe info
    log('Test Case: Verifying file isolation between different contexts');
    if (!testContextId) {
      throw new Error('Test context creation failed');
    }

    // Create a second test context
    const secondContextName = `test-context-2-${Date.now()}`;
    let secondContext: Context | null = null;
    try {
      secondContext = await agentBay.context.create(secondContextName);
      log(`Second context created - ID: ${secondContext.id}, Name: ${secondContext.name}, State: ${secondContext.state}, OSType: ${secondContext.osType}`);

      // Create first session with the first test context
      let session1: Session | null = null;
      try {
        session1 = await agentBay.create({imageId:'linux_latest', contextId: testContextId });
        log(`First session created with ID: ${session1.sessionId}`);

        // Create test file
        const createFileCmd = `echo '${testFileContent}' > ${testFilePath}`;
        const createOutput = await session1.command?.executeCommand(createFileCmd);
        log(`File creation output: ${createOutput}`);

        // Verify the file was created
        const verifyCmd = `cat ${testFilePath}`;
        const verifyOutput = await session1.command?.executeCommand(verifyCmd);
        log(`File content: ${verifyOutput}`);

        if (!verifyOutput || !verifyOutput.includes(testFileContent)) {
          throw new Error(`File content verification failed. Expected to contain '${testFileContent}', got: '${verifyOutput}'`);
        }
      } finally {
        if (session1) {
          await session1.delete();
        }
      }

      // Create third session with the second context ID
      let session3: Session | null = null;
      try {
        session3 = await agentBay.create({imageId:'linux_latest', contextId: secondContext.id });
        log(`Third session created with ID: ${session3.sessionId}`);

        // Try to read the file
        const verifyCmd = `cat ${testFilePath}`;
        const checkCmd = `ls -la ${testFilePath} 2>&1 || echo 'File does not exist'`;
        
        // First check with ls command
        const checkOutput = await session3.command?.executeCommand(checkCmd);
        log(`ls command output in third session: ${checkOutput}`);

        // Then try to read the file content
        const verifyOutput = await session3.command?.executeCommand(verifyCmd);

        if (verifyOutput && verifyOutput.includes(testFileContent)) {
          throw new Error(`File isolation test failed. File unexpectedly exists in the third session with content: '${verifyOutput}'`);
        } else {
          log(`File isolation verified: file does not exist in the third session`);
        }
      } finally {
        if (session3) {
          await session3.delete();
        }
      }
    } finally {
      // Delete the second context if it was created
      if (secondContext) {
        try {
          await agentBay.context.delete(secondContext);
          log(`Second context ${secondContext.id} deleted successfully`);
        } catch (error) {
          log(`Warning: Error deleting second context: ${error}`);
        }
      }
    }
  });
});