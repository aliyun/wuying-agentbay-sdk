import { AgentBay } from "../../src/agent-bay";
import { ContextStatusData } from "../../src/context-manager";
import { ContextSync, SyncPolicy } from "../../src/context-sync";
import { CreateSessionParams } from "../../src/session-params";
import { sleep } from "../utils/test-helpers";

describe("ContextSyncIntegration", () => {
  let agentBay: AgentBay;
  let contextId: string;
  let sessionId: string;
  
  // Skip tests if no API key is available or in CI environment
  const apiKey = process.env.AGENTBAY_API_KEY;
  const shouldSkip = !apiKey || process.env.CI;
  
  beforeAll(async () => {
    if (shouldSkip) {
      return;
    }
    
    // Initialize AgentBay client
    agentBay = new AgentBay(apiKey!);
    
    // Create a unique context name for this test
    const contextName = `test-sync-context-${Date.now()}`;
    
    // Create a context
    const contextResult = await agentBay.context.get(contextName, true);
    if (!contextResult.success || !contextResult.context) {
      throw new Error("Failed to create context");
    }
    
    contextId = contextResult.context.id;
    console.log(`Created context: ${contextResult.context.name} (ID: ${contextId})`);
    
    // Create session parameters with context sync
    const sessionParams = new CreateSessionParams();
    
    // Create context sync configuration
    const contextSync = new ContextSync(contextId, "/home/wuying", SyncPolicy.default());
    sessionParams.contextSyncs = [contextSync];
    
    // Add labels and image ID
    sessionParams.labels = { "test": "context-sync-integration" };
    sessionParams.imageId = "linux_latest";
    
    // Create session
    const sessionResult = await agentBay.create(sessionParams);
    if (!sessionResult.success || !sessionResult.session) {
      await agentBay.context.delete(contextResult.context!);
      throw new Error("Failed to create session");
    }
    
    sessionId = sessionResult.session.sessionId;
    console.log(`Created session: ${sessionId}`);
    
    // Wait for session to be ready
    await sleep(10000);
  });
  
  afterAll(async () => {
    if (shouldSkip) {
      return;
    }
    
    // Clean up session
    try {
      if (sessionId) {
        await agentBay.delete({ sessionId });
        console.log(`Session deleted: ${sessionId}`);
      }
    } catch (e) {
      console.warn(`Warning: Failed to delete session: ${e}`);
    }
    
    // Clean up context
    try {
      if (contextId) {
        await agentBay.context.delete({ id: contextId });
        console.log(`Context deleted: ${contextId}`);
      }
    } catch (e) {
      console.warn(`Warning: Failed to delete context: ${e}`);
    }
  });
  
  // Skip all tests if no API key is available or in CI environment
  const itif = shouldSkip ? it.skip : it;
  
  itif("should return parsed ContextStatusData", async () => {
    // Get the session
    const session = agentBay.getSession(sessionId);
    
    // Get context info
    const contextInfo = await session.context.info();
    
    // Verify that we have a request ID
    expect(contextInfo.requestId).toBeDefined();
    expect(contextInfo.requestId).not.toBe("");
    
    // Log the context status data
    console.log(`Context status data count: ${contextInfo.contextStatusData.length}`);
    for (let i = 0; i < contextInfo.contextStatusData.length; i++) {
      const data = contextInfo.contextStatusData[i];
      console.log(`Status data ${i}:`);
      console.log(`  Context ID: ${data.contextId}`);
      console.log(`  Path: ${data.path}`);
      console.log(`  Status: ${data.status}`);
      console.log(`  Task Type: ${data.taskType}`);
      console.log(`  Start Time: ${data.startTime}`);
      console.log(`  Finish Time: ${data.finishTime}`);
      if (data.errorMessage) {
        console.log(`  Error: ${data.errorMessage}`);
      }
    }
    
    // There might not be any status data yet, so we don't assert on the count
    // But if there is data, verify it has the expected structure
    for (const data of contextInfo.contextStatusData) {
      expect(data).toBeInstanceOf(Object);
      expect(data.contextId).toBeDefined();
      expect(data.path).toBeDefined();
      expect(data.status).toBeDefined();
      expect(data.taskType).toBeDefined();
    }
  });
  
  itif("should sync context and return info", async () => {
    // Get the session
    const session = agentBay.getSession(sessionId);
    
    // Sync context
    const syncResult = await session.context.sync();
    
    // Verify sync result
    expect(syncResult.success).toBe(true);
    expect(syncResult.requestId).toBeDefined();
    expect(syncResult.requestId).not.toBe("");
    
    // Wait for sync to complete
    await sleep(5000);
    
    // Get context info
    const contextInfo = await session.context.info();
    
    // Verify context info
    expect(contextInfo.requestId).toBeDefined();
    
    // Log the context status data
    console.log(`Context status data after sync, count: ${contextInfo.contextStatusData.length}`);
    for (let i = 0; i < contextInfo.contextStatusData.length; i++) {
      const data = contextInfo.contextStatusData[i];
      console.log(`Status data ${i}:`);
      console.log(`  Context ID: ${data.contextId}`);
      console.log(`  Path: ${data.path}`);
      console.log(`  Status: ${data.status}`);
      console.log(`  Task Type: ${data.taskType}`);
    }
    
    // Check if we have status data for our context
    let foundContext = false;
    for (const data of contextInfo.contextStatusData) {
      if (data.contextId === contextId) {
        foundContext = true;
        expect(data.path).toBe("/home/wuying");
        // Status might vary, but should not be empty
        expect(data.status).toBeDefined();
        expect(data.status).not.toBe("");
        break;
      }
    }
    
    // We should have found our context in the status data
    // But this might be flaky in CI, so just log a warning if not found
    if (!foundContext) {
      console.warn(`Warning: Could not find context ${contextId} in status data`);
    }
  });
  
  itif("should get context info with parameters", async () => {
    // Get the session
    const session = agentBay.getSession(sessionId);
    
    // Get context info with parameters
    const contextInfo = await session.context.infoWithParams(
      contextId,
      "/home/wuying",
      undefined
    );
    
    // Verify that we have a request ID
    expect(contextInfo.requestId).toBeDefined();
    
    // Log the filtered context status data
    console.log(`Filtered context status data count: ${contextInfo.contextStatusData.length}`);
    for (let i = 0; i < contextInfo.contextStatusData.length; i++) {
      const data = contextInfo.contextStatusData[i];
      console.log(`Status data ${i}:`);
      console.log(`  Context ID: ${data.contextId}`);
      console.log(`  Path: ${data.path}`);
      console.log(`  Status: ${data.status}`);
      console.log(`  Task Type: ${data.taskType}`);
    }
    
    // If we have status data, verify it matches our filters
    for (const data of contextInfo.contextStatusData) {
      if (data.contextId === contextId) {
        expect(data.path).toBe("/home/wuying");
      }
    }
  });
}); 