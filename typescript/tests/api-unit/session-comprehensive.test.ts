import { describe, beforeEach, afterEach, test, expect } from '@jest/globals';
import { AgentBay } from '../../src/agent-bay';
import { Session } from '../../src/session';
import { ContextSync, newContextSync, newUploadPolicy, newDownloadPolicy, newDeletePolicy } from '../../src/context-sync';
import { log } from 'console';

// Helper function to generate random context name
function generateRandomContextName(): string {
  const timestamp = Date.now();
  const randomStr = Math.random().toString(36).substring(2, 8);
  return `test-context-${timestamp}-${randomStr}`;
}

// Session creation helper function
async function createSession(imageId?: string): Promise<{ agentBay: AgentBay; session: Session }> {
  const agentBay = new AgentBay({ apiKey: process.env.AGENTBAY_API_KEY || 'test-api-key' });
  log(process.env.AGENTBAY_API_KEY)
  const sessionResult = await agentBay.create(imageId ? { imageId } : {});
  expect(sessionResult.success).toBe(true);

  return {
    agentBay,
    session: sessionResult.session!
  };
}

describe('Session Comprehensive Tests', () => {
  let agentBay: AgentBay;
  let session: Session;

  beforeEach(async () => {
    const sessionInfo = await createSession();
    agentBay = sessionInfo.agentBay;
    session = sessionInfo.session;
  });

  afterEach(async () => {
    if (session) {
      await agentBay.delete(session);
    }
  });

  // 1. Session Basic Information Management Tests
  describe('1. Session Basic Information Management Tests', () => {
    test('TC-SESSION-001: Get session ID test', async () => {
      // Prerequisites: AgentBay instance has been created, Session instance has been successfully created
      // Test objective: Verify that Session.getSessionId() method can correctly return the session ID

      const sessionId = session.getSessionId();

      // Verification points
      expect(sessionId).toBeDefined();
      expect(typeof sessionId).toBe('string');
      expect(sessionId).not.toBe('');
      expect(sessionId).toBe(session.sessionId);

      log(`TC-SESSION-001 SessionId: ${sessionId}`);
    });

    test('TC-SESSION-002: Get API key test', async () => {
      // Prerequisites: AgentBay instance has been created, Session instance has been successfully created
      // Test objective: Verify that Session.getAPIKey() method can correctly return the API key

      const apiKey = session.getAPIKey();
      const agentBayApiKey = agentBay.getAPIKey();

      // Verification points
      expect(apiKey).toBeDefined();
      expect(typeof apiKey).toBe('string');
      expect(apiKey).toBe(agentBayApiKey);
      expect(apiKey).not.toBe('');

      log(`TC-SESSION-002 API Key length: ${apiKey.length}`);
    });

    test('TC-SESSION-003: Get session information test', async () => {
      // Prerequisites: Session instance has been successfully created and connection established
      // Test objective: Verify that Session.info() method can correctly retrieve detailed session information

      const infoResult = await session.info();

      // Verification points
      expect(infoResult.success).toBe(true);
      expect(infoResult.requestId).toBeDefined();
      expect(infoResult.requestId).not.toBe('');
      expect(infoResult.data).toBeDefined();

      const sessionInfo = infoResult.data;
      expect(sessionInfo.sessionId).toBe(session.sessionId);
      expect(sessionInfo.sessionId).not.toBe('');

      if (sessionInfo.resourceUrl) {
        expect(typeof sessionInfo.resourceUrl).toBe('string');
      }

      log(`TC-SESSION-003 SessionInfo: SessionId=${sessionInfo.sessionId}, ResourceUrl=${sessionInfo.resourceUrl}`);
    });

    test('TC-SESSION-004-1: Get session link test (no parameters scenario)', async () => {
      // Use browser_latest image to create session for link testing
      const browserSessionInfo = await createSession('browser_latest');
      const browserAgentBay = browserSessionInfo.agentBay;
      const browserSession = browserSessionInfo.session;

      try {
        const linkResult = await browserSession.getLink();

        // Verification points
        expect(linkResult.success).toBe(true);
        expect(linkResult.requestId).toBeDefined();
        expect(linkResult.data).toBeDefined();
        expect(typeof linkResult.data).toBe('string');
        expect(linkResult.data).not.toBe('');

        log(`TC-SESSION-004-1 Link (no params): ${linkResult.data}`);
      } finally {
        await browserAgentBay.delete(browserSession);
      }
    });

    test('TC-SESSION-004-2: Get session link test (port parameter)', async () => {
      // Use browser_latest image to create session for link testing
      const browserSessionInfo = await createSession('browser_latest');
      const browserAgentBay = browserSessionInfo.agentBay;
      const browserSession = browserSessionInfo.session;

      try {
        const linkResult = await browserSession.getLink(undefined, 8080);

        // Verification points
        expect(linkResult.success).toBe(true);
        expect(linkResult.requestId).toBeDefined();
        expect(linkResult.data).toBeDefined();
        expect(typeof linkResult.data).toBe('string');
        expect(linkResult.data).not.toBe('');

        log(`TC-SESSION-004-2 Link (port 8080): ${linkResult.data}`);
      } finally {
        await browserAgentBay.delete(browserSession);
      }
    });

    test('TC-SESSION-004-3: Get session link test (protocol type parameter)', async () => {
      // Use linux_latest image to create session for link testing
      const linuxSessionInfo = await createSession('linux_latest');
      const linuxAgentBay = linuxSessionInfo.agentBay;
      const linuxSession = linuxSessionInfo.session;

      try {
        const linkResult = await linuxSession.getLink('https');

        // Verification points
        expect(linkResult.success).toBe(true);
        expect(linkResult.requestId).toBeDefined();
        expect(linkResult.data).toBeDefined();
        expect(typeof linkResult.data).toBe('string');
        expect(linkResult.data).not.toBe('');

        log(`TC-SESSION-004-3 Link (https protocol): ${linkResult.data}`);
      } catch(err) {
        const errorMessage = err instanceof Error ? err.message : String(err);
        expect(errorMessage).toContain('PARAM_ERROR:');
        log(`TC-SESSION-004-3 Expected PARAM_ERROR caught: ${errorMessage}`);
      } finally {
        await linuxAgentBay.delete(linuxSession);
      }
    });

    test('TC-SESSION-004-4: Get session link test (port and protocol combination)', async () => {
      // Use browser_latest image to create session for link testing
      const browserSessionInfo = await createSession('browser_latest');
      const browserAgentBay = browserSessionInfo.agentBay;
      const browserSession = browserSessionInfo.session;

      try {
        const linkResult = await browserSession.getLink('https', 8080);

        // Verification points
        expect(linkResult.success).toBe(true);
        expect(linkResult.requestId).toBeDefined();
        expect(linkResult.data).toBeDefined();
        expect(typeof linkResult.data).toBe('string');
        expect(linkResult.data).not.toBe('');

        log(`TC-SESSION-004-4 Link (https + port 8080): ${linkResult.data}`);
      } finally {
        await browserAgentBay.delete(browserSession);
      }
    });
  });

  // 2. Label Management Tests
  describe('2. Label Management Tests', () => {
    // For label testing, use the same session instance
    let labelSession: Session;
    let labelAgentBay: AgentBay;

    beforeAll(async () => {
      const sessionInfo = await createSession();
      labelAgentBay = sessionInfo.agentBay;
      labelSession = sessionInfo.session;
    });

    afterAll(async () => {
      if (labelSession) {
        await labelAgentBay.delete(labelSession);
      }
    });

    test('TC-LABEL-001: Set session labels test', async () => {
      // Prerequisites: Session instance has been successfully created
      // Test objective: Verify that Session.setLabels() method can correctly set session labels

      const labels = { env: "test", version: "1.0", team: "dev" };
      const setResult = await labelSession.setLabels(labels);

      // Verification points
      expect(setResult.success).toBe(true);
      expect(setResult.requestId).toBeDefined();
      expect(setResult.requestId).not.toBe('');

      log(`TC-LABEL-001 Set labels result: Success=${setResult.success}, RequestId=${setResult.requestId}`);
    });

    test('TC-LABEL-002: Get session labels test', async () => {
      // Prerequisites: Session instance has been created and labels have been set
      // Test objective: Verify that Session.getLabels() method can correctly retrieve session labels

      const labels = { env: "test", version: "1.0", team: "dev" };
      await labelSession.setLabels(labels);

      const getResult = await labelSession.getLabels();

      // Verification points
      expect(getResult.success).toBe(true);
      expect(getResult.requestId).toBeDefined();
      expect(getResult.data).toBeDefined();
      expect(typeof getResult.data).toBe('object');

      const retrievedLabels = getResult.data as Record<string, string>;
      expect(retrievedLabels.env).toBe("test");
      expect(retrievedLabels.version).toBe("1.0");
      expect(retrievedLabels.team).toBe("dev");

      log(`TC-LABEL-002 Retrieved labels: ${JSON.stringify(retrievedLabels)}`);
    });

    test('TC-LABEL-003: Label update test', async () => {
      // Prerequisites: Session instance has been created and initial labels have been set
      // Test objective: Verify that labels can be correctly updated and overridden

      // Set initial labels
      const initialLabels = { env: "test", version: "1.0" };
      await labelSession.setLabels(initialLabels);

      // Update labels
      const updatedLabels = { env: "prod", newKey: "newValue", team: "ops" };
      await labelSession.setLabels(updatedLabels);

      // Get labels to verify update result
      const getResult = await labelSession.getLabels();
      const retrievedLabels = getResult.data as Record<string, string>;

      // Verification points
      expect(retrievedLabels.env).toBe("prod");
      expect(retrievedLabels.newKey).toBe("newValue");
      expect(retrievedLabels.team).toBe("ops");
      expect(retrievedLabels.version).toBeUndefined(); // Old labels should be replaced

      log(`TC-LABEL-003 Updated labels: ${JSON.stringify(retrievedLabels)}`);
    });

    test('TC-LABEL-004: Empty labels handling test', async () => {
      // Prerequisites: Session instance has been created
      // Test objective: Verify handling of setting empty labels object

      const emptyLabels = {};
      const setResult = await labelSession.setLabels(emptyLabels);

      // Verification points
      expect(setResult.success).toBe(true);

      const getResult = await labelSession.getLabels();
      expect(getResult.success).toBe(true);
      expect(getResult.data).toBeDefined();
      expect(typeof getResult.data).toBe('object');

      const retrievedLabels = getResult.data as Record<string, string>;
      expect(Object.keys(retrievedLabels).length).toBe(0);

      log(`TC-LABEL-004 Empty labels handled successfully`);
    });
  });

  // 3. Session Deletion Tests
  describe('3. Session Deletion Tests', () => {
    test('TC-DELETE-001: Regular deletion test', async () => {
      // Prerequisites: Session instance has been successfully created
      // Test objective: Verify that Session.delete() method can correctly delete the session

      const testSessionInfo = await createSession();
      const testAgentBay = testSessionInfo.agentBay;
      const testSession = testSessionInfo.session;

      const deleteResult = await testSession.delete(false);

      // Verification points
      expect(deleteResult.success).toBe(true);
      expect(deleteResult.requestId).toBeDefined();
      expect(deleteResult.requestId).not.toBe('');

      log(`TC-DELETE-001 Delete result: Success=${deleteResult.success}, RequestId=${deleteResult.requestId}`);
    });

    test('TC-DELETE-002: Context sync deletion test', async () => {
      // Prerequisites: Session instance has been created with context sync configured
      // Test objective: Verify that delete method can correctly sync context before deletion when syncContext=true

      let contextId: string;

      // Get or create context
      const contextListResult = await agentBay.context.list();
      if (contextListResult.contexts.length > 0) {
        const availableContext = contextListResult.contexts.find(ctx => ctx.state === 'available');
        if (availableContext) {
          contextId = availableContext.id;
          log(`Using existing context: ${contextId}`);
        } else {
          const createResult = await agentBay.context.create(generateRandomContextName());
          contextId = createResult.contextId;
          log(`Created new context: ${contextId}`);
        }
      } else {
        const createResult = await agentBay.context.create(generateRandomContextName());
        contextId = createResult.contextId;
        log(`Created new context: ${contextId}`);
      }

      // Create Session with context sync
      const contextSync = newContextSync(contextId, '/tmp/home', {
        uploadPolicy: newUploadPolicy(),
        downloadPolicy: newDownloadPolicy(),
        deletePolicy: newDeletePolicy(),
        bwList: {
          whiteLists: [
            {
              path: "/tmp/home",
              excludePaths: ['/tmp/home/test'],
            },
          ],
        }
      });

      const syncSessionResult = await agentBay.create({
        contextSync: [contextSync]
      });
      expect(syncSessionResult.success).toBe(true);
      const syncSession = syncSessionResult.session!;

      try {
        // Trigger upload
        const syncResult = await syncSession.context.sync();
        log(`Sync triggered: Success=${syncResult.success}`);

        // Check upload status
        const infoResult = await syncSession.context.info();
        for (const item of infoResult.contextStatusData) {
          log(`Context ${item.contextId} status: ${item.status}, taskType: ${item.taskType}, path: ${item.path}`);
        }

        // Call sync context deletion
        const deleteResult = await syncSession.delete(true);

        // Verification points
        expect(deleteResult.success).toBe(true);
        expect(deleteResult.requestId).toBeDefined();

        log(`TC-DELETE-002 Sync delete result: Success=${deleteResult.success}`);
      } finally {
        // Ensure session is cleaned up
        if (syncSession) {
          try {
            await agentBay.delete(syncSession);
          } catch (error) {
            log(`Session already deleted or error occurred: ${error}`);
          }
        }
      }
    });

    test('TC-DELETE-003: Deletion timeout handling test', async () => {
      // Prerequisites: Session instance has been created, context sync may take longer time
      // Test objective: Verify timeout handling mechanism of deletion operations

      let contextId: string;
      let context: any;

      // Get or create context
      const contextListResult = await agentBay.context.list();
      if (contextListResult.contexts.length > 0) {
        context = contextListResult.contexts[0];
        contextId = context.id;
        log(`Using existing context: ${contextId}`);
      } else {
        const createResult = await agentBay.context.create(generateRandomContextName());
        context = createResult.context!;
        expect(createResult.success).toBe(true);
        expect(createResult.context).toBeDefined();
        expect(createResult.context.id).not.toBe('');
        expect(createResult.context.state).toBe('available');
        expect(createResult.context.name).toBe(generateRandomContextName());
        contextId = context.id;
        log(`Created new context: ${contextId}`);
      }

      // Create upload policy with longer timeout duration
      const longTimeoutUploadPolicy = {
        ...newUploadPolicy(),
        period: 300 // 5 minutes
      };

      const contextSync = newContextSync(contextId, '/tmp/home', {
        uploadPolicy: longTimeoutUploadPolicy,
        downloadPolicy: newDownloadPolicy(),
        deletePolicy: newDeletePolicy(),
        bwList: {
          whiteLists: [
            {
              path: "/tmp/home",
              excludePaths: [],
            },
          ],
        }
      });

      const timeoutSessionResult = await agentBay.create({
        contextSync: [contextSync]
      });
      expect(timeoutSessionResult.success).toBe(true);
      const timeoutSession = timeoutSessionResult.session!;

      try {
        // Trigger upload
        await timeoutSession.context.sync();

        // Check upload status
        const infoResult = await timeoutSession.context.info();
        for (const item of infoResult.contextStatusData) {
          log(`Context ${item.contextId} status: ${item.status}, taskType: ${item.taskType}`);
        }

        // Delete context
        await agentBay.context.delete(context);

        // Verify context is deleted
        const listAfterDelete = await agentBay.context.list();
        const deletedContext = listAfterDelete.contexts.find(ctx => ctx.id === contextId);
        expect(deletedContext).toBeUndefined();

        // Call sync deletion (should handle timeout situation)
        const deleteResult = await timeoutSession.delete(true);

        // Verification points
        expect(deleteResult.success).toBe(true);

        log(`TC-DELETE-003 Timeout delete handled: Success=${deleteResult.success}`);
      } finally {
        // Ensure resource cleanup
        try {
          await agentBay.delete(timeoutSession);
        } catch (error) {
          log(`Session cleanup: ${error}`);
        }
      }
    });
  });

  // 4. Sub-modules Initialization Tests
  describe('4. Sub-modules Initialization Tests', () => {
    test('TC-MODULES-001: Sub-modules initialization test', async () => {
      // Prerequisites: Session instance has been successfully created
      // Test objective: Verify that all sub-modules of session are correctly initialized and not null

      // Verification points
      expect(session.fileSystem).toBeDefined();
      expect(session.fileSystem).not.toBeNull();
      expect(session.fileSystem.constructor.name).toBe('FileSystem');

      expect(session.command).toBeDefined();
      expect(session.command).not.toBeNull();
      expect(session.command.constructor.name).toBe('Command');

      expect(session.code).toBeDefined();
      expect(session.code).not.toBeNull();
      expect(session.code.constructor.name).toBe('Code');

      expect(session.context).toBeDefined();
      expect(session.context).not.toBeNull();

      expect(session.application).toBeDefined();
      expect(session.application).not.toBeNull();
      expect(session.application.constructor.name).toBe('Application');

      expect(session.window).toBeDefined();
      expect(session.window).not.toBeNull();
      expect(session.window.constructor.name).toBe('WindowManager');

      expect(session.ui).toBeDefined();
      expect(session.ui).not.toBeNull();
      expect(session.ui.constructor.name).toBe('UI');

      expect(session.oss).toBeDefined();
      expect(session.oss).not.toBeNull();
      expect(session.oss.constructor.name).toBe('Oss');

      log(`TC-MODULES-001 All sub-modules initialized successfully`);
    });
  });

  // 5. Error Handling Tests
  describe('5. Error Handling Tests', () => {
    test('TC-ERROR-001: setLabels invalid parameter handling test', async () => {
      // Prerequisites: Session instance has been created
      // Test objective: Verify handling when invalid parameters are passed

      // Test null parameter
      const nullResult = await session.setLabels(null as any);
      expect(nullResult.success).toBe(false);
      expect(nullResult.errorMessage).toBe("Labels cannot be null, undefined, or invalid type. Please provide a valid labels object.");
      expect(nullResult.requestId).toBe("");

      // Test undefined parameter
      const undefinedResult = await session.setLabels(undefined as any);
      expect(undefinedResult.success).toBe(false);
      expect(undefinedResult.errorMessage).toBe("Labels cannot be null, undefined, or invalid type. Please provide a valid labels object.");
      expect(undefinedResult.requestId).toBe("");

      // Test non-object type parameters
      const stringResult = await session.setLabels("invalid" as any);
      expect(stringResult.success).toBe(false);
      expect(stringResult.errorMessage).toBe("Labels cannot be null, undefined, or invalid type. Please provide a valid labels object.");

      const numberResult = await session.setLabels(123 as any);
      expect(numberResult.success).toBe(false);
      expect(numberResult.errorMessage).toBe("Labels cannot be null, undefined, or invalid type. Please provide a valid labels object.");

      const booleanResult = await session.setLabels(true as any);
      expect(booleanResult.success).toBe(false);
      expect(booleanResult.errorMessage).toBe("Labels cannot be null, undefined, or invalid type. Please provide a valid labels object.");

      // Test array type parameters
      const arrayResult = await session.setLabels([] as any);
      expect(arrayResult.success).toBe(false);
      expect(arrayResult.errorMessage).toBe("Labels cannot be an array. Please provide a valid labels object.");

      const arrayWithDataResult = await session.setLabels([{key: "value"}] as any);
      expect(arrayWithDataResult.success).toBe(false);
      expect(arrayWithDataResult.errorMessage).toBe("Labels cannot be an array. Please provide a valid labels object.");

      // Test built-in object type parameters
      const dateResult = await session.setLabels(new Date() as any);
      expect(dateResult.success).toBe(false);
      expect(dateResult.errorMessage).toBe("Labels must be a plain object. Built-in object types are not allowed.");

      const regexResult = await session.setLabels(/test/ as any);
      expect(regexResult.success).toBe(false);
      expect(regexResult.errorMessage).toBe("Labels must be a plain object. Built-in object types are not allowed.");

      const errorResult = await session.setLabels(new Error("test") as any);
      expect(errorResult.success).toBe(false);
      expect(errorResult.errorMessage).toBe("Labels must be a plain object. Built-in object types are not allowed.");

      const mapResult = await session.setLabels(new Map() as any);
      expect(mapResult.success).toBe(false);
      expect(mapResult.errorMessage).toBe("Labels must be a plain object. Built-in object types are not allowed.");

      const setResult = await session.setLabels(new Set() as any);
      expect(setResult.success).toBe(false);
      expect(setResult.errorMessage).toBe("Labels must be a plain object. Built-in object types are not allowed.");

      const promiseResult = await session.setLabels(Promise.resolve() as any);
      expect(promiseResult.success).toBe(false);
      expect(promiseResult.errorMessage).toBe("Labels must be a plain object. Built-in object types are not allowed.");

      log(`TC-ERROR-001 setLabels invalid parameters: All invalid parameter types correctly rejected`);
    });

    test('TC-ERROR-002: setLabels empty object handling test', async () => {
      // Prerequisites: Session instance has been created
      // Test objective: Verify handling when empty object is passed

      const emptyResult = await session.setLabels({});
      expect(emptyResult.success).toBe(false);
      expect(emptyResult.errorMessage).toBe("Labels cannot be empty. Please provide at least one label.");
      expect(emptyResult.requestId).toBe("");

      log(`TC-ERROR-002 setLabels empty object: Empty object correctly rejected`);
    });

    test('TC-ERROR-003: setLabels empty keys/values handling test', async () => {
      // Prerequisites: Session instance has been created
      // Test objective: Verify handling when empty keys or values are passed

      // Test empty key
      const emptyKeyResult = await session.setLabels({"": "value"});
      expect(emptyKeyResult.success).toBe(false);
      expect(emptyKeyResult.errorMessage).toBe("Label keys cannot be empty Please provide valid keys.");
      expect(emptyKeyResult.requestId).toBe("");

      // Test empty value
      const emptyValueResult = await session.setLabels({"key": ""});
      expect(emptyValueResult.success).toBe(false);
      expect(emptyValueResult.errorMessage).toBe("Label values cannot be empty Please provide valid values.");
      expect(emptyValueResult.requestId).toBe("");

      // Test null value
      const nullValueResult = await session.setLabels({"key": null as any});
      expect(nullValueResult.success).toBe(false);
      expect(nullValueResult.errorMessage).toBe("Label values cannot be empty Please provide valid values.");

      // Test undefined value
      const undefinedValueResult = await session.setLabels({"key": undefined as any});
      expect(undefinedValueResult.success).toBe(false);
      expect(undefinedValueResult.errorMessage).toBe("Label values cannot be empty Please provide valid values.");

      log(`TC-ERROR-003 setLabels empty keys/values: All empty keys and values correctly rejected`);
    });

    test('TC-ERROR-004: setLabels mixed invalid parameters test', async () => {
      // Prerequisites: Session instance has been created
      // Test objective: Verify priority handling of mixed invalid parameters

      // Test mixed situation with empty key and valid key-value pair
      const mixedEmptyKeyResult = await session.setLabels({
        "validKey": "validValue",
        "": "emptyKeyValue"
      });
      expect(mixedEmptyKeyResult.success).toBe(false);
      expect(mixedEmptyKeyResult.errorMessage).toBe("Label keys cannot be empty Please provide valid keys.");

      // Test mixed situation with empty value and valid key-value pair
      const mixedEmptyValueResult = await session.setLabels({
        "validKey": "validValue",
        "emptyValueKey": ""
      });
      expect(mixedEmptyValueResult.success).toBe(false);
      expect(mixedEmptyValueResult.errorMessage).toBe("Label values cannot be empty Please provide valid values.");

      // Test multiple invalid key-value pairs
      const multipleInvalidResult = await session.setLabels({
        "": "emptyKey",
        "emptyValue": "",
        "nullValue": null as any
      });
      expect(multipleInvalidResult.success).toBe(false);
      // Should return the first encountered error (empty key)
      expect(multipleInvalidResult.errorMessage).toBe("Label keys cannot be empty Please provide valid keys.");

      log(`TC-ERROR-004 setLabels mixed invalid parameters: Mixed invalid parameters correctly handled with proper priority`);
    });

    test('TC-ERROR-005: setLabels boundary cases test', async () => {
      // Prerequisites: Session instance has been created
      // Test objective: Verify handling of boundary cases

      // Test key with only whitespace
      const whitespaceKeyResult = await session.setLabels({" ": "value"});
      expect(whitespaceKeyResult.success).toBe(false);

      // Test value with only whitespace
      const whitespaceValueResult = await session.setLabels({"key": " "});
      expect(whitespaceValueResult.success).toBe(false);

      // Test zero-length but non-empty special cases (if any exist)
      const specialCharsResult = await session.setLabels({
        "key1": "value1",
        "key2": "value2"
      });
      expect(specialCharsResult.success).toBe(true);

      log(`TC-ERROR-005 setLabels boundary cases: Boundary cases correctly handled`);
    });

    test('TC-ERROR-006: API response exception handling test', async () => {
      // Prerequisites: Session instance has been created
      // Test objective: Verify handling when API returns exceptional responses

      // This test mainly verifies existing error handling mechanisms
      try {
        // Call info method, should succeed under normal circumstances
        const result = await session.info();
        expect(result.requestId).toBeDefined();

        if (!result.success) {
          // If failure, verify error information exists
          expect(result.errorMessage).toBeDefined();
        }

        log(`TC-ERROR-006 API response handling verified`);
      } catch (error) {
        // Verify exception is correctly caught
        expect(error).toBeDefined();
        log(`TC-ERROR-006 API exception handled: ${error}`);
      }
    });
  });

  // 6. Performance Tests
  describe('6. Performance Tests', () => {
    test('TC-PERF-001: Label operations performance test', async () => {
      // Prerequisites: Session instance has been created
      // Test objective: Verify performance of label operations

      const iterations = 5;
      const setTimes: number[] = [];
      const getTimes: number[] = [];

      for (let i = 0; i < iterations; i++) {
        const labels = { iteration: i.toString(), timestamp: Date.now().toString() };

        // Test setLabels performance
        const setStartTime = Date.now();
        await session.setLabels(labels);
        const setTime = Date.now() - setStartTime;
        setTimes.push(setTime);

        // Test getLabels performance
        const getStartTime = Date.now();
        await session.getLabels();
        const getTime = Date.now() - getStartTime;
        getTimes.push(getTime);
      }

      const avgSetTime = setTimes.reduce((a, b) => a + b, 0) / setTimes.length;
      const avgGetTime = getTimes.reduce((a, b) => a + b, 0) / getTimes.length;

      // Verification points
      expect(avgSetTime).toBeLessThan(2000); // Within 2 seconds
      expect(avgGetTime).toBeLessThan(2000); // Within 2 seconds

      log(`TC-PERF-001 Label operations: Avg set=${avgSetTime}ms, Avg get=${avgGetTime}ms`);
    });

    test('TC-PERF-002: Concurrent operations performance test', async () => {
      // Prerequisites: Multiple Session instances have been created
      // Test objective: Verify performance of concurrent operations

      const sessions: Session[] = [];
      const agentBays: AgentBay[] = [];

      try {
        // Create multiple sessions
        for (let i = 0; i < 3; i++) {
          const sessionInfo = await createSession();
          agentBays.push(sessionInfo.agentBay);
          sessions.push(sessionInfo.session);
        }

        // Execute concurrent operations
        const startTime = Date.now();
        const promises = sessions.map((sess, index) =>
          sess.setLabels({ test: `concurrent-${index}`, timestamp: Date.now().toString() })
        );

        const results = await Promise.all(promises);
        const concurrentTime = Date.now() - startTime;

        // Verification points
        results.forEach(result => {
          expect(result.success).toBe(true);
        });

        log(`TC-PERF-003 Concurrent operations: Total time=${concurrentTime}ms, Success rate=100%`);

      } finally {
        // Clean up sessions
        for (let i = 0; i < sessions.length; i++) {
          await agentBays[i].delete(sessions[i]);
        }
      }
    });
  });

  // 7. Integration Tests
  describe('7. Integration Tests', () => {
    test('TC-INTEGRATION-001: Complete session lifecycle test', async () => {
      // Prerequisites: AgentBay instance is available
      // Test objective: Verify complete session lifecycle from creation to deletion

      const lifecycleSessionInfo = await createSession();
      const lifecycleAgentBay = lifecycleSessionInfo.agentBay;
      const lifecycleSession = lifecycleSessionInfo.session;

      try {
        // 1. Verify session creation
        expect(lifecycleSession.sessionId).toBeDefined();

        // 2. Set labels
        const labels = { env: "integration", test: "lifecycle" };
        const setResult = await lifecycleSession.setLabels(labels);
        expect(setResult.success).toBe(true);

        // 3. Get session information
        const infoResult = await lifecycleSession.info();
        expect(infoResult.success).toBe(true);

        // 4. Verify labels
        const getResult = await lifecycleSession.getLabels();
        expect(getResult.success).toBe(true);
        const retrievedLabels = getResult.data as Record<string, string>;
        expect(retrievedLabels.env).toBe("integration");

        // 5. Use sub-modules (basic verification)
        expect(lifecycleSession.command).toBeDefined();
        expect(lifecycleSession.fileSystem).toBeDefined();

        log(`TC-INTEGRATION-001 Full lifecycle completed successfully`);

      } finally {
        // 6. Delete session
        const deleteResult = await lifecycleAgentBay.delete(lifecycleSession);
        expect(deleteResult.success).toBe(true);
      }
    });

    test('TC-INTEGRATION-002: Multi-session interaction test', async () => {
      // Prerequisites: AgentBay instance is available
      // Test objective: Verify independence and interaction between multiple sessions

      const multiSessions: Session[] = [];
      const multiAgentBays: AgentBay[] = [];

      try {
        // Create multiple Session instances
        for (let i = 0; i < 3; i++) {
          const sessionInfo = await createSession();
          multiAgentBays.push(sessionInfo.agentBay);
          multiSessions.push(sessionInfo.session);
        }

        // Set different labels for each session
        const labelTasks = multiSessions.map((sess, index) =>
          sess.setLabels({
            sessionIndex: index.toString(),
            type: 'multi-session-test',
            timestamp: Date.now().toString()
          })
        );

        await Promise.all(labelTasks);

        // Verify independence between sessions
        const getLabelTasks = multiSessions.map((sess, index) =>
          sess.getLabels()
        );

        const labelResults = await Promise.all(getLabelTasks);

        // Verification points
        labelResults.forEach((result, index) => {
          expect(result.success).toBe(true);
          const labels = result.data as Record<string, string>;
          expect(labels.sessionIndex).toBe(index.toString());
          expect(labels.type).toBe('multi-session-test');
        });

        // Test concurrent operations
        const concurrentInfoTasks = multiSessions.map(sess => sess.info());
        const infoResults = await Promise.all(concurrentInfoTasks);

        infoResults.forEach(result => {
          expect(result.success).toBe(true);
        });

        log(`TC-INTEGRATION-002 Multi-session test: ${multiSessions.length} sessions operated independently`);

      } finally {
        // Release sessions
        for (let i = 0; i < multiSessions.length; i++) {
          await multiAgentBays[i].delete(multiSessions[i]);
        }
      }
    });
  });

  // 8. Boundary Condition Tests
  describe('8. Boundary Condition Tests', () => {
    test('TC-BOUNDARY-001: Large amount of label data test', async () => {
      // Prerequisites: Session instance has been created
      // Test objective: Verify ability to handle large amount of label data

      // Create labels object with many key-value pairs
      const largeLabels: Record<string, string> = {};
      for (let i = 0; i < 50; i++) {
        largeLabels[`key_${i}`] = `value_${i}_${'x'.repeat(100)}`; // Each value approximately 100 characters
      }

      // Set large amount of label data
      const setResult = await session.setLabels(largeLabels);
      expect(setResult.success).toBe(true);

      // Get and verify data integrity
      const getResult = await session.getLabels();
      expect(getResult.success).toBe(true);

      const retrievedLabels = getResult.data as Record<string, string>;
      expect(Object.keys(retrievedLabels).length).toBe(50);

      // Verify data integrity
      for (let i = 0; i < 50; i++) {
        expect(retrievedLabels[`key_${i}`]).toBe(`value_${i}_${'x'.repeat(100)}`);
      }

      log(`TC-BOUNDARY-001 Large labels: Successfully handled ${Object.keys(largeLabels).length} label pairs`);
    });

    test('TC-BOUNDARY-002: Special characters in labels test', async () => {
      // Prerequisites: Session instance has been created
      // Test objective: Verify handling of special characters in labels

      // Set labels containing special characters
      const specialLabels = {
        htmlTags: "<script>alert('test')</script>",
        jsonChars: '{"key": "value", "array": [1,2,3]}',
        specialSymbols: "!@#$%^&*()_+-=[]{}|;':\",./<>?",
        newlines: "line1\nline2\ttabbed",
        quotes: `single'quote and "double"quote`,
        backslashes: "path\\to\\file\\with\\backslashes"
      };

      // Set special character labels
      const setResult = await session.setLabels(specialLabels);
      expect(setResult.success).toBe(true);

      // Verify correctness of storage and retrieval
      const getResult = await session.getLabels();
      expect(getResult.success).toBe(true);

      const retrievedLabels = getResult.data as Record<string, string>;
      log(`TC-BOUNDARY-002 Retrieved special labels: ${JSON.stringify(retrievedLabels)}`);
      // Verification points
      expect(retrievedLabels.htmlTags).toBe("<script>alert('test')</script>");
      expect(retrievedLabels.jsonChars).toBe('{"key": "value", "array": [1,2,3]}');
      expect(retrievedLabels.specialSymbols).toBe("!@#$%^&*()_+-=[]{}|;':\",./<>?");
      expect(retrievedLabels.newlines).toBe("line1\nline2\ttabbed");
      expect(retrievedLabels.quotes).toBe(`single'quote and "double"quote`);
      expect(retrievedLabels.backslashes).toBe("path\\to\\file\\with\\backslashes");

      log(`TC-BOUNDARY-002 Special characters: All special characters correctly encoded and decoded`);
    });

    test('TC-BOUNDARY-003: Long-running session test', async () => {
      // Prerequisites: Session instance has been created
      // Test objective: Verify stability of long-running sessions

      const longRunningSessionInfo = await createSession();
      const longRunningAgentBay = longRunningSessionInfo.agentBay;
      const longRunningSession = longRunningSessionInfo.session;

      try {
        // Periodically execute various operations
        const iterations = 10;
        const operationResults: boolean[] = [];

        for (let i = 0; i < iterations; i++) {
          // Set labels
          const labels = { iteration: i.toString(), timestamp: Date.now().toString() };
          const setResult = await longRunningSession.setLabels(labels);
          operationResults.push(setResult.success);

          // Get session information
          const infoResult = await longRunningSession.info();
          operationResults.push(infoResult.success);

          // Get labels
          const getResult = await longRunningSession.getLabels();
          operationResults.push(getResult.success);

          // Brief wait to simulate long-running
          await new Promise(resolve => setTimeout(resolve, 100));
        }

        // Verification points
        const successRate = operationResults.filter(result => result).length / operationResults.length;
        expect(successRate).toBeGreaterThanOrEqual(0.9); // 90% success rate

        // Final verification that session is still active
        const finalInfoResult = await longRunningSession.info();
        expect(finalInfoResult.success).toBe(true);
        expect(finalInfoResult.data.sessionId).toBe(longRunningSession.sessionId);

        log(`TC-BOUNDARY-003 Long running session: ${iterations} iterations completed with ${successRate * 100}% success rate`);

      } finally {
        await longRunningAgentBay.delete(longRunningSession);
      }
    });
  });

  // Data Integrity and Consistency Tests
  describe('9. Data Integrity Tests', () => {
    test('should maintain session consistency across operations', async () => {
      // Verify session consistency across various operations
      const originalSessionId = session.sessionId;

      // Execute multiple operations
      await session.setLabels({ test: "consistency" });
      const infoResult = await session.info();
      await session.getLabels();

      // Verify session ID remains consistent
      expect(session.sessionId).toBe(originalSessionId);
      expect(infoResult.data.sessionId).toBe(originalSessionId);

      log(`Data consistency test: SessionId remained consistent across operations`);
    });

    test('should handle concurrent operations safely', async () => {
      // Verify safety of concurrent operations
      const concurrentOperations = [
        session.info(),
        session.setLabels({ concurrent: "test1" }),
        session.getLabels(),
        session.setLabels({ concurrent: "test2" }),
        session.info()
      ];

      const results = await Promise.all(concurrentOperations);

      // Verify all operations have valid requestId
      results.forEach(result => {
        expect(result.requestId).toBeDefined();
        expect(result.requestId).not.toBe('');
      });

      log(`Concurrent operations test: All ${results.length} concurrent operations completed with valid requestIds`);
    });
  });
});
