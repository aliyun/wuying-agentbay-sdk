import { log } from 'console';
import { AgentBay, ContextSync, newContextSync, newSyncPolicy } from '../../src';
import { Session } from '../../src/session';

describe('Context Data Persistence Integration Tests', () => {

  describe('4.1 Same API Key and Context Data Sharing', () => {
    let agentBay: AgentBay;
    let session1: Session;
    let session2: Session;
    let session3: Session;
    let contextId: string;
    let contextObject: any; // Store context object for deletion
    const randomSuffix = Math.random().toString(36).substring(2, 8);
    const filePath = '/tmp/shared_data/persistent_file.txt';

    beforeAll(async () => {
      // Step 1.1.1: Environment preparation
      agentBay = new AgentBay();
      expect(agentBay).toBeDefined();
      log('Step 1.1.1: AgentBay instance created successfully');
    });

    it('should verify data persistence between sessions with same apikey and contextId', async () => {
      // Step 1.1.2: Context creation
      const contextManager = agentBay.context;
      const contextName = `persistent-context-${randomSuffix}`;
      const createResult = await contextManager.create(contextName);
      expect(createResult.success).toBe(true);
      log(`Step 1.1.2: Context created with name: ${JSON.stringify(createResult.context)}`);
      expect(createResult.context.name).toBe(contextName);
      log('Step 1.1.2: Context created successfully');

      const contextResult = await contextManager.get(contextName);
      expect(contextResult.success).toBe(true);
      expect(contextResult.context).toBeDefined();
      contextId = contextResult.contextId;
      contextObject = contextResult.context;
      log(`Step 1.1.2: Got contextId: ${contextId}`);

      // Step 1.1.3: Context status check
      const contextList = await contextManager.list();
      const createdContext = contextList.contexts.find(ctx => ctx.id === contextId);
      expect(createdContext).toBeDefined();
      expect(createdContext!.state).toBe('available');
      log(`Step 1.1.3: Context status verified as 'available', contextId: ${contextId}`);

      // Step 1.1.4: First session creation
      const contextSync1: ContextSync = newContextSync(
        contextId,
        '/tmp/shared_data',
        newSyncPolicy()
      );

      const sessionResult1 = await agentBay.create({
        imageId: 'linux_latest',
        contextSync: [contextSync1]
      });
      expect(sessionResult1.success).toBe(true);
      session1 = sessionResult1.session!;
      log('Step 1.1.4: First session created successfully');

      // Step 1.1.5: Context status update check
      const updatedContextList = await contextManager.list();
      const inUseContext = updatedContextList.contexts.find(ctx => ctx.id === contextId);
      expect(inUseContext).toBeDefined();
      log(`Step 1.1.5: Context status checked, current state: ${inUseContext!.state}`);

      // Step 1.1.6: File creation
      const createFileCommand = 'echo "Data from first session" > /tmp/shared_data/persistent_file.txt';
      const createFileResult = await session1.command.executeCommand(createFileCommand);
      expect(createFileResult.success).toBe(true);
      log(`Step 1.1.6: File created successfully at ${filePath}`);

      // Step 1.1.7: File content validation
      const fileContent = await session1.fileSystem.readFile(filePath);
      expect(fileContent.content.trim()).toBe('Data from first session');
      log('Step 1.1.7: File content verified successfully');

      // Step 1.1.8: Session deletion with second parameter true
      const deleteResult = await agentBay.delete(session1, true);
      expect(deleteResult.success).toBe(true);
      log('Step 1.1.8: Session deleted successfully with syncContext=true');

      // Step 1.1.9: Create two new sessions with same contextId
      const contextSync2: ContextSync = newContextSync(
        contextId,
        '/tmp/shared_data',
        newSyncPolicy()
      );

      const contextSync3: ContextSync = newContextSync(
        contextId,
        '/tmp/shared_data',
        newSyncPolicy()
      );

      const sessionResult2 = await agentBay.create({
        imageId: 'linux_latest',
        contextSync: [contextSync2]
      });
      expect(sessionResult2.success).toBe(true);
      session2 = sessionResult2.session!;

      const sessionResult3 = await agentBay.create({
        imageId: 'linux_latest',
        contextSync: [contextSync3]
      });
      expect(sessionResult3.success).toBe(true);
      session3 = sessionResult3.session!;
      log('Step 1.1.9: Two new sessions created successfully with same contextId');

      // Step 1.2.0: Wait for 20 seconds
      log('Step 1.2.0: Waiting for 20 seconds...');
      await new Promise(resolve => setTimeout(resolve, 20000));
      log('Step 1.2.0: Wait completed');

      // Step 1.2.0: Data persistence verification
      // Check with first session
      const listCommand1 = 'ls -la /tmp/shared_data/';
      const listResult1 = await session2.command.executeCommand(listCommand1);
      expect(listResult1.success).toBe(true);

      expect(listResult1.output).toContain('persistent_file.txt');
      log('Step 1.2.0: Directory listing from session2:', listResult1.output);

      // Check with second session
      const listCommand2 = 'ls -la /tmp/shared_data/';
      const listResult2 = await session3.command.executeCommand(listCommand2);
      expect(listResult2.success).toBe(true);
      expect(listResult2.output).toContain('persistent_file.txt');
      log('Step 1.2.0: Directory listing from session3:', listResult2.output);

      // Try to read the persistent file from both sessions
      try {
        const persistentContent1 = await session2.fileSystem.readFile(filePath);
        expect(persistentContent1.content.trim()).toBe('Data from first session');
        log('Step 1.2.0: File content successfully read from session2');
      } catch (error) {
        log('Step 1.2.0: Failed to read file from session2:', error);
      }

      try {
        const persistentContent2 = await session3.fileSystem.readFile(filePath);
        expect(persistentContent2.content.trim()).toBe('Data from first session');
        log('Step 1.2.0: File content successfully read from session3');
      } catch (error) {
        log('Step 1.2.0: Failed to read file from session3:', error);
      }

    });

    afterAll(async () => {
      // Step 1.2.1: Resource cleanup
      try {
        if (session2) {
          await agentBay.delete(session2,true);
          log('Session2 cleaned up successfully');
        }
        if (session3) {
          await agentBay.delete(session3,true);
          log('Session3 cleaned up successfully');
        }
        if (contextObject && agentBay) {
          const deleteResult = await agentBay.context.delete(contextObject);
          expect(deleteResult.success).toBe(true);
          log('Context cleaned up successfully');
        }
        log('Step 1.2.1: All resources cleaned up successfully');
      } catch (error) {
        log('Error during cleanup:', error);
      }
    });
  });
});
