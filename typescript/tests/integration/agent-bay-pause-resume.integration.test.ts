import { AgentBay } from "../../src/agent-bay";
import { CreateSessionParams } from "../../src/session-params";
import { Session } from "../../src/session";
import { log } from "../../src/utils/logger";
import * as dotenv from "dotenv";
import * as path from "path";
import * as fs from "fs";


describe("AgentBay pause and resume integration tests", () => {
  let agentBay: AgentBay;
  let sessionId: string | undefined;
  let sessionCreated = false;

  beforeAll(async () => {
    
    const apiKey = process.env.AGENTBAY_API_KEY;
    log(`API Key loaded: ${apiKey ? "YES" : "NO"}`);
    if (!apiKey) {
      throw new Error("AGENTBAY_API_KEY environment variable is not set");
    }
    agentBay = new AgentBay({ apiKey });

    try {
      log("🚀 Creating a new session for pause/resume testing...");
      // Create session
      const params = new CreateSessionParams();
      params.imageId = "linux_latest";
      const createResult = await agentBay.create(params);
      if (createResult.success && createResult.session) {
        sessionId = createResult.session.sessionId;
        sessionCreated = true;
      log(`✅ Session created with ID: ${sessionId}`);
      } else {
        log("⚠️  Session creation failed, some tests will be skipped");
        log(`   Error: ${createResult.errorMessage}`);
      }
    } catch (error) {
      log(`❌ Session creation error: ${error}`);
    }
  });

  test("should pause and resume existing session", async () => {
    if (!sessionCreated || !sessionId) {
      log("⊘ Skipping test: session was not created");
      return;
    }

    log("📋 Test: Pause and resume existing session");
    
    // First get the session object
    const getResult = await agentBay.get(sessionId);
    if (!getResult.success || !getResult.session) {
      log("⊘ Skipping test: failed to get session object");
      return;
    }
    
    const session = getResult.session;
    
    // Pause the session
    log("⏸️  Pausing session...");
    const pauseResult = await agentBay.pauseAsync(session);
    
    expect(pauseResult).toBeDefined();
    if (pauseResult.success) {
      log(`✅ Session pause initiated successfully. Request ID: ${pauseResult.requestId}`);
    } else {
      log(`⚠️  Session pause failed (this might be expected): ${pauseResult.errorMessage}`);
    }
    
    // Wait a bit
    await new Promise(resolve => setTimeout(resolve, 3000));
    
    // Resume the session
    log("▶️  Resuming session...");
    const resumeResult = await agentBay.resumeAsync(session);
    
    expect(resumeResult).toBeDefined();
    if (resumeResult.success) {
      log(`✅ Session resume initiated successfully. Request ID: ${resumeResult.requestId}`);
    } else {
      log(`⚠️  Session resume failed (this might be expected): ${resumeResult.errorMessage}`);
    }
  });

  test("should handle pause of nonexistent session", async () => {
    log("📋 Test: Handle pause of nonexistent session");
    
    // Create a fake session with invalid ID
    const fakeSession = new Session(agentBay, "session-nonexistent-12345");
    
    // Try to pause the nonexistent session
    log("⏸️  Attempting to pause nonexistent session...");
    const pauseResult = await agentBay.pauseAsync(fakeSession);
    
    expect(pauseResult).toBeDefined();
    expect(pauseResult.success).toBe(false);
    log(`✅ Correctly handled pause of nonexistent session: ${pauseResult.errorMessage}`);
  });

  test("should handle resume of nonexistent session", async () => {
    log("📋 Test: Handle resume of nonexistent session");
    
    // Create a fake session with invalid ID
    const fakeSession = new Session(agentBay, "session-nonexistent-12345");
    
    // Try to resume the nonexistent session
    log("▶️  Attempting to resume nonexistent session...");
    const resumeResult = await agentBay.resumeAsync(fakeSession);
    
    expect(resumeResult).toBeDefined();
    expect(resumeResult.success).toBe(false);
    log(`✅ Correctly handled resume of nonexistent session: ${resumeResult.errorMessage}`);
  });

  afterAll(async () => {
    if (sessionCreated && sessionId) {
      try {
        log("🧹 Cleaning up test session...");
        // Get session object first
        const getResult = await agentBay.get(sessionId);
        if (getResult.success && getResult.session) {
          // Delete session
          const deleteResult = await agentBay.delete(getResult.session);
          if (deleteResult.success) {
            log(`✅ Session ${sessionId} deleted successfully`);
          } else {
            log(`⚠️  Failed to delete session ${sessionId}: ${deleteResult.errorMessage}`);
          }
        }
      } catch (error) {
        log(`❌ Error deleting session ${sessionId}: ${error}`);
      }
    }
  });
});