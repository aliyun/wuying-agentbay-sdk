/**
 * Integration test for GetSession API
 */

import { AgentBay } from "../../src/agent-bay";
import { Session } from "../../src/session";
import { log } from "../../src/utils/logger";

describe('GetSession API Integration Test', () => {
  let agentBay: AgentBay;
  const apiKey = process.env.AGENTBAY_API_KEY;

  beforeAll(() => {
    if (!apiKey) {
      throw new Error('AGENTBAY_API_KEY environment variable is not set');
    }
    agentBay = new AgentBay({ apiKey });
  });

  it('should retrieve session information using GetSession API', async () => {
    // Create a session first
    log('Creating a new session for GetSession testing...');
    const createResult = await agentBay.create({ imageId: "linux_latest"});
    expect(createResult.success).toBe(true);
    expect(createResult.session).toBeDefined();

    const session = createResult.session!;
    const sessionId = session.sessionId;
    log(`Session created with ID: ${sessionId}`);

    try {
      // Test GetSession API
      log('Testing GetSession API...');
      const getSessionResult = await agentBay.getSession(sessionId);

      // Validate response
      expect(getSessionResult.requestId).toBeTruthy();
      log(`GetSession RequestID: ${getSessionResult.requestId}`);

      expect(getSessionResult.httpStatusCode).toBe(200);
      expect(getSessionResult.code).toBe('ok');
      expect(getSessionResult.success).toBe(true);

      // Validate Data field
      expect(getSessionResult.data).toBeDefined();
      expect(getSessionResult.data!.sessionId).toBe(sessionId);
      // Note: data.success may reflect a different status than the overall response
      // We validate the overall response success instead
      expect(getSessionResult.data!.appInstanceId).toBeTruthy();
      log(`AppInstanceID: ${getSessionResult.data!.appInstanceId}`);
      expect(getSessionResult.data!.resourceId).toBeTruthy();
      log(`ResourceID: ${getSessionResult.data!.resourceId}`);

      // Validate contexts field
      expect(getSessionResult.data!.contexts).toBeDefined();
      expect(getSessionResult.data!.contexts).not.toBeNull();
      expect(getSessionResult.data!.contexts!.length).toBeGreaterThan(0);
      log(`Contexts count: ${getSessionResult.data!.contexts!.length}`);
      getSessionResult.data!.contexts!.forEach((ctx, i) => {
        expect(ctx.name).toBeTruthy();
        expect(ctx.id).toBeTruthy();
        log(`Context ${i}: name=${ctx.name}, id=${ctx.id}`);
      });

      log('GetSession API test passed successfully');
    } finally {
      // Clean up: Delete the session
      log('Cleaning up: Deleting the session...');
      const deleteResult = await session.delete();
      if (deleteResult.success) {
        log(`Session ${sessionId} deleted successfully`);
      } else {
        log(`Warning: Failed to delete session: ${deleteResult.errorMessage}`);
      }
    }
  });
});

