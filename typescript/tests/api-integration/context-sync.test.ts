import { AgentBay, ContextSync, newContextSync, newUploadPolicy, newDownloadPolicy, newDeletePolicy } from '../../src';
import { CreateSessionParams } from '../../src/agent-bay';
import { Session } from '../../src/session';

describe('Context Sync Integration Tests', () => {
  let agentBay: AgentBay;
  const testTimeout = 60000; // 60 seconds

  beforeAll(() => {
    // Initialize AgentBay with API key from environment
    agentBay = new AgentBay();
  });

  describe('1.1 Single Session Context Sync Upload/Download', () => {
    let session: Session;
    let contextId: string;
    let contextObject: any; // Store context object for deletion
    const randomSuffix = Math.random().toString(36).substring(2, 10);

    it('should complete single session context sync workflow', async () => {
      // Step 1: Environment preparation
      expect(agentBay).toBeDefined();

      // Step 2: Get context manager
      const contextManager = agentBay.context;
      expect(contextManager).toBeDefined();

      // Step 3: Context query and creation
      const existingContexts = await contextManager.list();
      const availableContext = existingContexts.contexts.find(ctx => ctx.state === 'available');

      if (availableContext) {
        contextId = availableContext.id;
        contextObject = availableContext;
      } else {
        const contextName = `test-context-${randomSuffix}`;
        const createResult = await contextManager.create(contextName);
        expect(createResult.success).toBe(true);

        const createdContextResult = await contextManager.get(contextName);
        expect(createdContextResult.success).toBe(true);
        expect(createdContextResult.context).toBeDefined();
        contextId = createdContextResult.contextId;
        contextObject = createdContextResult.context;
      }

      expect(contextId).toBeDefined();
      expect(contextId).not.toBe('');

      // Step 4: Session creation with context sync
      const contextSync: ContextSync = newContextSync(
        contextId,
        '/tmp/user',
        {
          uploadPolicy: newUploadPolicy(),
          downloadPolicy: newDownloadPolicy(),
          deletePolicy: newDeletePolicy(),
          bwList: {
            whiteLists: [
              { path: '/tmp/user', excludePaths: ['/tmp/user/excluded'] }
            ]
          }
        }
      );

      const createParams: CreateSessionParams = {
        imageId: 'linux_latest',
        labels: {
          test: 'sync_context',
          timestamp: Date.now().toString()
        },
        contextSync: [contextSync]
      };

      const sessionResult = await agentBay.create(createParams);
      expect(sessionResult.success).toBe(true);
      expect(sessionResult.session).toBeDefined();

      session = sessionResult.session!;
      expect(session.getSessionId()).toBeDefined();
      expect(session.getSessionId()).not.toBe('');

      // Step 5: Labels verification
      const labelsResult = await session.getLabels();
      expect(labelsResult.success).toBe(true);
      expect(labelsResult.data.test).toBe('sync_context');
      expect(labelsResult.data.timestamp).toBeDefined();

      // Step 6: Context manager retrieval
      const sessionContextManager = session.context;
      expect(sessionContextManager).toBeDefined();
      const sessionContextInfo = await sessionContextManager.info();

      const contextStatusDataInfo = sessionContextInfo.contextStatusData;
      expect(contextStatusDataInfo).toBeDefined();
      expect(contextStatusDataInfo.length).toBeGreaterThan(0);
      const sessionStatusDataItem = contextStatusDataInfo[0];
      expect(sessionStatusDataItem.contextId).toBe(contextId);

      // Step 7: Sync operation
      const syncResult = await sessionContextManager.sync();
      expect(syncResult.success).toBe(true);

      // Step 8: Sync info query
      const contextStatusData = await sessionContextManager.info();
      expect(contextStatusData).toBeDefined();
      console.log('Context Status Data:', contextStatusData);

      // Step 9: Session info retrieval
      const apikey = session.getAPIKey();
      const sessionId = session.getSessionId();
      expect(apikey).toBeDefined();
      expect(sessionId).toBeDefined();

      // Step 10: Labels re-verification
      const verifyLabelsResult = await session.getLabels();
      expect(verifyLabelsResult.success).toBe(true);
      expect(verifyLabelsResult.data.test).toBe('sync_context');

      // Step 11: Session info query
      const sessionInfo = await session.info();
      expect(sessionInfo.success).toBe(true);

      // Step 12: Labels update
      const newLabels = {
        test: 'updated_sync_context',
        version: 'v2'
      };
      const setLabelsResult = await session.setLabels(newLabels);
      expect(setLabelsResult.success).toBe(true);

      // Step 13: Updated labels verification
      const updatedLabelsResult = await session.getLabels();
      expect(updatedLabelsResult.success).toBe(true);
      expect(updatedLabelsResult.data.test).toBe('updated_sync_context');
      expect(updatedLabelsResult.data.version).toBe('v2');

    });

    afterAll(async () => {
      // Step 14 & 15: Context deletion and verification
      if (contextObject) {
        const deleteResult = await agentBay.context.delete(contextObject);
        expect(deleteResult.success).toBe(true);

        const remainingContexts = await agentBay.context.list();
        const deletedContext = remainingContexts.contexts.find(ctx => ctx.id === contextId);
        expect(deletedContext).toBeUndefined();
      }

      // Step 16: Resource cleanup
      if (session) {
        const deleteResult = await agentBay.delete(session, true);
        expect(deleteResult.success).toBe(true);
      }
    });
  });

  describe('1.2 Two SyncContext Sessions Creation', () => {
    let session1: Session;
    let session2: Session;
    let contextId1: string;
    let contextId2: string;
    let contextObject1: any;
    let contextObject2: any;
    const randomSuffix1 = Math.random().toString(36).substring(2, 8);
    const randomSuffix2 = Math.random().toString(36).substring(2, 8);

    it('should create two sessions with different context sync configurations', async () => {
      // Step 1: Environment preparation
      expect(agentBay).toBeDefined();

      // Step 2: Get context manager
      const contextManager = agentBay.context;
      expect(contextManager).toBeDefined();

      // Step 3: Create two contexts
      const contextName1 = `test-context-1-${randomSuffix1}`;
      const contextName2 = `test-context-2-${randomSuffix2}`;

      const createResult1 = await contextManager.create(contextName1);
      const createResult2 = await contextManager.create(contextName2);

      expect(createResult1.success).toBe(true);
      expect(createResult2.success).toBe(true);

      // Step 4: Get context instances
      const contextResult1 = await contextManager.get(contextName1);
      const contextResult2 = await contextManager.get(contextName2);

      expect(contextResult1.success).toBe(true);
      expect(contextResult2.success).toBe(true);
      expect(contextResult1.context).toBeDefined();
      expect(contextResult2.context).toBeDefined();

      contextId1 = contextResult1.contextId;
      contextId2 = contextResult2.contextId;
      contextObject1 = contextResult1.context;
      contextObject2 = contextResult2.context;
      expect(contextId1).not.toBe(contextId2);

      // Step 5: Create two sessions
      const contextSync1: ContextSync = newContextSync(
        contextId1,
        '/tmp/user1',
        {
          uploadPolicy: newUploadPolicy(),
          downloadPolicy: newDownloadPolicy(),
          deletePolicy: newDeletePolicy(),
          bwList: {
            whiteLists: [
              { path: '/tmp/user1', excludePaths: ['/tmp/user1/cache', '/tmp/user1/temp'] }
            ]
          }
        }
      );

      const contextSync2: ContextSync = newContextSync(
        contextId2,
        '/tmp/user2',
        {
          uploadPolicy: newUploadPolicy(),
          downloadPolicy: newDownloadPolicy(),
          deletePolicy: newDeletePolicy(),
          bwList: {
            whiteLists: [
              { path: '/tmp/user2', excludePaths: ['/tmp/user2/logs'] }
            ]
          }
        }
      );

      const sessionResult1 = await agentBay.create({
        imageId: 'linux_latest',
        contextSync: [contextSync1]
      });

      const sessionResult2 = await agentBay.create({
        imageId: 'linux_latest',
        contextSync: [contextSync2]
      });

      expect(sessionResult1.success).toBe(true);
      expect(sessionResult2.success).toBe(true);

      session1 = sessionResult1.session!;
      session2 = sessionResult2.session!;

      expect(session1.getSessionId()).not.toBe(session2.getSessionId());

      // Step 6: Sync status query
      const contextStatus1 = await session1.context.info();
      const contextStatus2 = await session2.context.info();

      expect(contextStatus1).toBeDefined();
      expect(contextStatus2).toBeDefined();
      console.log('Session1 Context Status:', contextStatus1);
      console.log('Session2 Context Status:', contextStatus2);

      // Step 7: Concurrent sync test
      const [syncResult1, syncResult2] = await Promise.all([
        session1.context.sync(),
        session2.context.sync()
      ]);

      expect(syncResult1.success).toBe(true);
      expect(syncResult2.success).toBe(true);

      // Step 8: Concurrent sync verification
      const verifyStatus1 = await session1.context.info();
      const verifyStatus2 = await session2.context.info();

      expect(verifyStatus1).toBeDefined();
      expect(verifyStatus2).toBeDefined();

    });

    afterAll(async () => {
      // Step 8: Context cleanup
      if (contextObject1) {
        const deleteResult1 = await agentBay.context.delete(contextObject1);
        expect(deleteResult1.success).toBe(true);
      }
      if (contextObject2) {
        const deleteResult2 = await agentBay.context.delete(contextObject2);
        expect(deleteResult2.success).toBe(true);
      }

      // Step 9: Session cleanup
      if (session1) await agentBay.delete(session1, true);
      if (session2) await agentBay.delete(session2, true);
    });
  });

  describe('1.3 Same ContextId Two Sessions Creation', () => {
    let session1: Session;
    let session2: Session;
    let contextId: string;
    let contextObject: any;
    const randomSuffix = Math.random().toString(36).substring(2, 8);

    it('should create two sessions using the same contextId', async () => {
      // Step 1: Environment preparation
      expect(agentBay).toBeDefined();

      // Step 2: Get context manager
      const contextManager = agentBay.context;
      expect(contextManager).toBeDefined();

      // Step 3: Create single context
      const contextName = `shared-context-${randomSuffix}`;
      const createResult = await contextManager.create(contextName);
      expect(createResult.success).toBe(true);

      const contextResult = await contextManager.get(contextName);
      expect(contextResult.success).toBe(true);
      expect(contextResult.context).toBeDefined();
      contextId = contextResult.contextId;
      contextObject = contextResult.context;

      // Step 4: Create two sessions with same contextId but different paths
      const contextSync1: ContextSync = newContextSync(
        contextId,
        '/tmp/path1',
        {
          uploadPolicy: newUploadPolicy(),
          downloadPolicy: newDownloadPolicy(),
          deletePolicy: newDeletePolicy(),
          bwList: {
            whiteLists: [
              { path: '/tmp/path1', excludePaths: ['/tmp/path1/backup'] }
            ]
          }
        }
      );

      const contextSync2: ContextSync = newContextSync(
        contextId,
        '/tmp/path2',
        {
          uploadPolicy: newUploadPolicy(),
          downloadPolicy: newDownloadPolicy(),
          deletePolicy: newDeletePolicy(),
          bwList: {
            whiteLists: [
              { path: '/tmp/path2', excludePaths: ['/tmp/path2/tmp', '/tmp/path2/cache'] }
            ]
          }
        }
      );

      const sessionResult1 = await agentBay.create({
        imageId: 'linux_latest',
        contextSync: [contextSync1]
      });

      const sessionResult2 = await agentBay.create({
        imageId: 'linux_latest',
        contextSync: [contextSync2]
      });

      expect(sessionResult1.success).toBe(true);
      expect(sessionResult2.success).toBe(true);

      session1 = sessionResult1.session!;
      session2 = sessionResult2.session!;

      // Step 5: Context sharing verification
      const sessionContextManager1 = session1.context;
      expect(sessionContextManager1).toBeDefined();
      const sessionContextInfo1 = await sessionContextManager1.info();

      const contextStatusDataInfo1 = sessionContextInfo1.contextStatusData;
      expect(contextStatusDataInfo1).toBeDefined();
      expect(contextStatusDataInfo1.length).toBeGreaterThan(0);
      const session1ContextId = contextStatusDataInfo1[0].contextId;

      const sessionContextManager2 = session2.context;
      expect(sessionContextManager2).toBeDefined();
      const sessionContextInfo2 = await sessionContextManager2.info();

      const contextStatusDataInfo2 = sessionContextInfo2.contextStatusData;
      expect(contextStatusDataInfo2).toBeDefined();
      expect(contextStatusDataInfo2.length).toBeGreaterThan(0);
      const session2ContextId = contextStatusDataInfo2[0].contextId;

      expect(session1ContextId).toBe(contextId);
      expect(session2ContextId).toBe(contextId);
      expect(session1ContextId).toBe(session2ContextId);

      // Step 6: Independent path verification
      // Paths are configured independently in each session's context sync
      // This is verified by the different path configurations above

    });

    afterAll(async () => {
      // Step 7: Context cleanup
      if (contextObject) {
        const deleteResult = await agentBay.context.delete(contextObject);
        expect(deleteResult.success).toBe(true);
      }

      // Step 8: Session cleanup
      if (session1) await agentBay.delete(session1,true);
      if (session2) await agentBay.delete(session2,true);
    });
  });
});
