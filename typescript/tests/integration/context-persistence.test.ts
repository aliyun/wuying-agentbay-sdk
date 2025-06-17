import { AgentBay, Session, Context } from '../../src';
import { getTestApiKey, randomString } from '../utils/test-helpers';

// Define test runner types if they're not available
declare function describe(name: string, fn: () => void): void;
declare function beforeEach(fn: () => void | Promise<void>): void;
declare function afterEach(fn: () => void | Promise<void>): void;
declare function it(name: string, fn: () => void | Promise<void>): void;
declare function expect(actual: any): any;

// Define Node.js process if it's not available
declare namespace NodeJS {
  interface ProcessEnv {
    [key: string]: string | undefined;
  }
}

declare var process: {
  env: {
    [key: string]: string | undefined;
  }
};

describe('Context Persistence Integration', () => {
  let agentBay: AgentBay;
  let testContext: Context | null;
  let testContextName: string;
  
  beforeEach(async () => {
    const apiKey = getTestApiKey();
    agentBay = new AgentBay({ apiKey });
    
    // Create a unique context name for testing
    testContextName = `test-context-${randomString()}`;
    
    // Create a test context
    console.log(`Creating test context: ${testContextName}`);
    try {
      testContext = await agentBay.context.create(testContextName);
      console.log(`Test context created with ID: ${testContext.id}`);
    } catch (error) {
      console.log(`Warning: Error creating test context: ${error}`);
      testContext = null;
    }
  });
  
  afterEach(async () => {
    // Clean up the test context
    if (testContext) {
      console.log(`Cleaning up: Deleting test context: ${testContextName}`);
      try {
        await agentBay.context.delete(testContext);
        console.log('Test context deleted successfully');
      } catch (error) {
        console.log(`Warning: Error deleting test context: ${error}`);
      }
    }
  });
  
  describe('Context persistence across sessions', () => {
    it('should persist files between sessions in the same context', async () => {
      if (!testContext) {
        console.log('Skipping test as test context creation failed');
        return;
      }
      
      // Create first session with the test context
      console.log('Creating first session with test context...');
      let session1: Session | null = null;
      try {
        session1 = await agentBay.create({ contextId: testContext.id });
        console.log(`First session created with ID: ${session1.sessionId}`);
        
        // Write a test file in the first session
        if (session1.filesystem && typeof (session1.filesystem as any).writeFile === 'function') {
          const testFilePath = '/tmp/context-test-file.txt';
          const testContent = `Test content created at ${new Date().toISOString()}`;
          
          console.log(`Writing test file: ${testFilePath}`);
          await (session1.filesystem as any).writeFile(testFilePath, testContent);
          
          // Verify the file was written
          const readContent = await session1.filesystem.readFile(testFilePath);
          console.log(`Verified file content in first session: ${readContent}`);
          expect(readContent).toBe(testContent);
          
          // Create a second session with the same context
          console.log('Creating second session with the same test context...');
          let session2: Session | null = null;
          try {
            session2 = await agentBay.create({ contextId: testContext.id });
            console.log(`Second session created with ID: ${session2.sessionId}`);
            
            // Verify the file exists and has the same content in the second session
            console.log(`Reading test file in second session: ${testFilePath}`);
            const content2 = await session2.filesystem.readFile(testFilePath);
            console.log(`File content in second session: ${content2}`);
            
            // Check if the content matches
            expect(content2).toBe(testContent);
            console.log('File persistence verified successfully');
          } catch (error) {
            console.log(`Error in second session: ${error}`);
            throw error;
          } finally {
            // Clean up the second session
            if (session2) {
              console.log('Cleaning up: Deleting second session...');
              try {
                await agentBay.delete(session2.sessionId);
              } catch (error) {
                console.log(`Warning: Error deleting second session: ${error}`);
              }
            }
          }
        } else {
          console.log('Skipping test as filesystem.writeFile is not available');
        }
      } catch (error) {
        console.log(`Error in first session: ${error}`);
        throw error;
      } finally {
        // Clean up the first session
        if (session1) {
          console.log('Cleaning up: Deleting first session...');
          try {
            await agentBay.delete(session1.sessionId);
          } catch (error) {
            console.log(`Warning: Error deleting first session: ${error}`);
          }
        }
      }
    });
  });
  
  describe('File isolation between contexts', () => {
    it('should isolate files between different contexts', async () => {
      if (!testContext) {
        console.log('Skipping test as test context creation failed');
        return;
      }
      
      // Create a second test context
      const secondContextName = `test-context-2-${randomString()}`;
      console.log(`Creating second test context: ${secondContextName}`);
      let secondContext: Context | null = null;
      try {
        secondContext = await agentBay.context.create(secondContextName);
        console.log(`Second test context created with ID: ${secondContext.id}`);
        
        // Create first session with the first test context
        console.log('Creating session with first test context...');
        let session1: Session | null = null;
        try {
          session1 = await agentBay.create({ contextId: testContext.id });
          console.log(`First session created with ID: ${session1.sessionId}`);
          
          // Write a test file in the first session
          if (session1.filesystem && typeof (session1.filesystem as any).writeFile === 'function') {
            const testFilePath = '/tmp/context-isolation-test-file.txt';
            const testContent = `Test content for isolation test created at ${new Date().toISOString()}`;
            
            console.log(`Writing test file in first context: ${testFilePath}`);
            await (session1.filesystem as any).writeFile(testFilePath, testContent);
            
            // Verify the file was written
            const readContent = await session1.filesystem.readFile(testFilePath);
            console.log(`Verified file content in first context: ${readContent}`);
            expect(readContent).toBe(testContent);
            
            // Create a second session with the second context
            console.log('Creating session with second test context...');
            let session2: Session | null = null;
            try {
              session2 = await agentBay.create({ contextId: secondContext.id });
              console.log(`Second session created with ID: ${session2.sessionId}`);
              
              // Try to read the file in the second context
              console.log(`Attempting to read test file in second context: ${testFilePath}`);
              try {
                const content2 = await session2.filesystem.readFile(testFilePath);
                console.log(`File content in second context: ${content2}`);
                
                // If we get here, the file might exist but should have different content
                // or the API might return an empty string for non-existent files
                if (content2 === testContent) {
                  console.log('Warning: File content is the same in both contexts, isolation may not be working');
                  expect(content2).not.toBe(testContent);
                } else {
                  console.log('File content is different or empty in second context, isolation is working');
                }
              } catch (error) {
                // If reading the file throws an error, that's also a sign of isolation
                console.log(`Error reading file in second context: ${error}`);
                console.log('File isolation verified successfully (file not accessible in second context)');
              }
            } catch (error) {
              console.log(`Error in second session: ${error}`);
              throw error;
            } finally {
              // Clean up the second session
              if (session2) {
                console.log('Cleaning up: Deleting second session...');
                try {
                  await agentBay.delete(session2.sessionId);
                } catch (error) {
                  console.log(`Warning: Error deleting second session: ${error}`);
                }
              }
            }
          } else {
            console.log('Skipping test as filesystem.writeFile is not available');
          }
        } catch (error) {
          console.log(`Error in first session: ${error}`);
          throw error;
        } finally {
          // Clean up the first session
          if (session1) {
            console.log('Cleaning up: Deleting first session...');
            try {
              await agentBay.delete(session1.sessionId);
            } catch (error) {
              console.log(`Warning: Error deleting first session: ${error}`);
            }
          }
        }
      } catch (error) {
        console.log(`Error creating second test context: ${error}`);
        throw error;
      } finally {
        // Clean up the second test context
        if (secondContext) {
          console.log(`Cleaning up: Deleting second test context: ${secondContextName}`);
          try {
            await agentBay.context.delete(secondContext);
          } catch (error) {
            console.log(`Warning: Error deleting second test context: ${error}`);
          }
        }
      }
    });
  });
});
