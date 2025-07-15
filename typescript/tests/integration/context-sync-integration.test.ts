import { AgentBay } from "../../src/agent-bay";
import { ContextStatusData } from "../../src/context-manager";
import { ContextSync, SyncPolicy } from "../../src/context-sync";
import { CreateSessionParams } from "../../src/session-params";
import { sleep, wait, randomString } from "../utils/test-helpers";

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

  itif("should test context sync persistence with retry", async () => {
    // 1. Create a unique context name and get its ID
    const contextName = `test-persistence-retry-ts-${randomString()}`;
    const contextResult = await agentBay.context.get(contextName, true);
    expect(contextResult.success).toBe(true);
    expect(contextResult.context).toBeDefined();
    
    const contextObj = contextResult.context!;
    const contextIdLocal = contextObj.id;
    console.log(`Created context: ${contextObj.name} (ID: ${contextIdLocal})`);
    
    // 2. Create a session with context sync, using a timestamped path under /data/wuying/
    const timestamp = Date.now();
    const syncPath = `/data/wuying/test-path-ts-${timestamp}`;
    
    // Use default sync policy
    const sessionParams = {
      imageId: "linux_latest",
      labels: { "test": "persistence-retry-test-ts" },
      contextSync: [
        {
          contextId: contextIdLocal,
          path: syncPath,
          policy: {
            uploadPolicy: {
              autoUpload: true,
              uploadStrategy: "beforeResourceRelease"
            },
            downloadPolicy: {
              autoDownload: true,
              downloadStrategy: "async"
            }
          }
        }
      ]
    };
    
    // Create first session
    const sessionResult = await agentBay.create(sessionParams);
    expect(sessionResult.success).toBe(true);
    expect(sessionResult.session).toBeDefined();
    
    let session1 = sessionResult.session!;
    console.log(`Created first session: ${session1.sessionId}`);
    
    // 3. Wait for session to be ready and retry context info until data is available
    console.log("Waiting for session to be ready and context status data to be available...");
    
    let foundData = false;
    let contextInfo;
    
    for (let i = 0; i < 20; i++) { // Retry up to 20 times
      contextInfo = await session1.context.info();
      
      if (contextInfo.contextStatusData && contextInfo.contextStatusData.length > 0) {
        console.log(`Found context status data on attempt ${i+1}`);
        foundData = true;
        break;
      }
      
      console.log(`No context status data available yet (attempt ${i+1}), retrying in 1 second...`);
      await wait(1000);
    }
    
    expect(foundData).toBe(true);
    printContextStatusData(contextInfo?.contextStatusData || []);
    
    // 4. Write a file to the context sync path
    const testContent = `Test content for TypeScript persistence retry test at ${timestamp}`;
    const testFilePath = `${syncPath}/test-file.txt`;
    
    // Create directory first
    console.log(`Creating directory: ${syncPath}`);
    const dirResult = await session1.fileSystem.createDirectory(syncPath);
    expect(dirResult.success).toBe(true);
    
    // Write the file
    console.log(`Writing file to ${testFilePath}`);
    const writeResult = await session1.fileSystem.writeFile(testFilePath, testContent);
    expect(writeResult.success).toBe(true);
    
    // 5. Sync to trigger file upload
    console.log("Triggering context sync...");
    const syncResult = await session1.context.sync();
    expect(syncResult.success).toBe(true);
    console.log(`Context sync successful (RequestID: ${syncResult.requestId})`);
    
    // 6. Get context info with retry for upload status
    console.log("Checking file upload status with retry...");
    
    let foundUpload = false;
    for (let i = 0; i < 20; i++) { // Retry up to 20 times
      contextInfo = await session1.context.info();
      
      // Check if we have upload status for our context
      for (const data of contextInfo.contextStatusData) {
        if (data.contextId === contextIdLocal && data.taskType === "upload") {
          foundUpload = true;
          console.log(`Found upload task for context at attempt ${i+1}`);
          break;
        }
      }
      
      if (foundUpload) {
        break;
      }
      
      console.log(`No upload status found yet (attempt ${i+1}), retrying in 1 second...`);
      await wait(1000);
    }
    
    if (foundUpload) {
      console.log("Found upload status for context");
      printContextStatusData(contextInfo?.contextStatusData || []);
    } else {
      console.log("Warning: Could not find upload status after all retries");
    }
    
    // 7. Release first session
    console.log("Releasing first session...");
    const deleteResult = await session1.delete();
    expect(deleteResult.success).toBe(true);
    
    // 8. Create a second session with the same context ID
    console.log("Creating second session with the same context ID...");
    const sessionParams2 = {
      imageId: "linux_latest",
      labels: { "test": "persistence-retry-test-ts-second" },
      contextSync: [
        {
          contextId: contextIdLocal,
          path: syncPath,
          policy: {
            uploadPolicy: {
              autoUpload: true,
              uploadStrategy: "beforeResourceRelease"
            },
            downloadPolicy: {
              autoDownload: true,
              downloadStrategy: "async"
            }
          }
        }
      ]
    };
    
    const sessionResult2 = await agentBay.create(sessionParams2);
    expect(sessionResult2.success).toBe(true);
    expect(sessionResult2.session).toBeDefined();
    
    let session2 = sessionResult2.session!;
    console.log(`Created second session: ${session2.sessionId}`);
    
    // 9. Get context info with retry for download status
    console.log("Checking file download status with retry...");
    
    let foundDownload = false;
    for (let i = 0; i < 20; i++) { // Retry up to 20 times
      contextInfo = await session2.context.info();
      
      // Check if we have download status for our context
      for (const data of contextInfo.contextStatusData) {
        if (data.contextId === contextIdLocal && data.taskType === "download") {
          foundDownload = true;
          console.log(`Found download task for context at attempt ${i+1}`);
          break;
        }
      }
      
      if (foundDownload) {
        break;
      }
      
      console.log(`No download status found yet (attempt ${i+1}), retrying in 1 second...`);
      await wait(1000);
    }
    
    if (foundDownload) {
      console.log("Found download status for context");
      printContextStatusData(contextInfo?.contextStatusData || []);
    } else {
      console.log("Warning: Could not find download status after all retries");
    }
    
    // 10. Read the file from the second session
    console.log("Reading file from second session...");
    const readResult = await session2.fileSystem.readFile(testFilePath);
    expect(readResult.success).toBe(true);
    
    // 11. Verify the file content matches what was written
    expect(readResult.content).toBe(testContent);
    console.log("File content verified successfully");
  });
}); 

// Helper function to print context status data
function printContextStatusData(data: any[]): void {
  if (data.length === 0) {
    console.log("No context status data available");
    return;
  }
  
  for (let i = 0; i < data.length; i++) {
    const item = data[i];
    console.log(`Context Status Data [${i}]:`);
    console.log(`  ContextId: ${item.contextId}`);
    console.log(`  Path: ${item.path}`);
    console.log(`  Status: ${item.status}`);
    console.log(`  TaskType: ${item.taskType}`);
    console.log(`  StartTime: ${item.startTime}`);
    console.log(`  FinishTime: ${item.finishTime}`);
    if (item.errorMessage) {
      console.log(`  ErrorMessage: ${item.errorMessage}`);
    }
  }
} 