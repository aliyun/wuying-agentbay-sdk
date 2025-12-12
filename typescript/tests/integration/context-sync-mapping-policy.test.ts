import { AgentBay } from "../../src/agent-bay";
import {
  newUploadPolicy,
  newDownloadPolicy,
  newDeletePolicy,
  newExtractPolicy,
  MappingPolicy,
  SyncPolicy,
} from "../../src/context-sync";
import { CreateSessionParams } from "../../src/session-params";

describe("Context Sync with MappingPolicy Integration Tests", () => {
  let agentBay: AgentBay;
  const apiKey = process.env.AGENTBAY_API_KEY;

  beforeAll(() => {
    if (!apiKey || process.env.CI) {
      console.log("Skipping integration test: No API key available or running in CI");
      return;
    }
    agentBay = new AgentBay({ apiKey });
  });

  it("should create session with MappingPolicy for cross-platform persistence", async () => {
    if (!apiKey || process.env.CI) {
      console.log("Skipping test: No API key available or running in CI");
      return;
    }

    // 1. Create a unique context name
    const contextName = `test-mapping-policy-${Date.now()}`;
    const contextResult = await agentBay.context.get(contextName, true);
    expect(contextResult.context).toBeDefined();

    const context = contextResult.context!;
    console.log(`Created context: ${context.name} (ID: ${context.id})`);

    try {
      // Define paths
      const windowsPath = "c:\\Users\\Administrator\\Downloads";
      const linuxPath = "/home/wuying/下载";
      const testFileName = "cross-platform-test.txt";
      const testContent = "This file was created in Windows session and should be accessible in Linux session";

      // ========== Phase 1: Create Windows session and persist data ==========
      console.log("========== Phase 1: Windows Session - Create and Persist Data ==========");

      // Create sync policy for Windows session (no mapping policy needed for first session)
      const windowsSyncPolicy: SyncPolicy = {
        uploadPolicy: newUploadPolicy(),
        downloadPolicy: newDownloadPolicy(),
        deletePolicy: newDeletePolicy(),
        extractPolicy: newExtractPolicy(),
      };

      // Create Windows session with context sync
      const windowsSessionParams = new CreateSessionParams();
      windowsSessionParams.addContextSync(context.id, windowsPath, windowsSyncPolicy);
      windowsSessionParams.withImageId("windows_latest");
      windowsSessionParams.withLabels({ test: "mapping-policy-windows" });

      // Create Windows session
      const windowsSessionResult = await agentBay.create(windowsSessionParams);
      expect(windowsSessionResult.session).toBeDefined();

      const windowsSession = windowsSessionResult.session!;
      console.log(`Created Windows session: ${windowsSession.sessionId}`);

      // Wait for Windows session to be ready
      console.log("Waiting for Windows session to be ready...");
      await new Promise((resolve) => setTimeout(resolve, 15000));

      // Create directory in Windows session
      console.log(`Creating directory in Windows: ${windowsPath}`);
      const windowsDirResult = await windowsSession.fileSystem.createDirectory(windowsPath);
      expect(windowsDirResult.requestId).toBeDefined();

      // Create test file in Windows session
      const testFilePath = `${windowsPath}\\${testFileName}`;
      console.log(`Creating test file in Windows: ${testFilePath}`);
      const createFileCmd = `echo ${testContent} > "${testFilePath}"`;
      const windowsCmdResult = await windowsSession.command.executeCommand(createFileCmd);
      expect(windowsCmdResult.output).toBeDefined();
      console.log(`Windows file creation result: ${windowsCmdResult}`);

      // Verify file exists in Windows session
      const verifyFileCmd = `type "${testFilePath}"`;
      const verifyResult = await windowsSession.command.executeCommand(verifyFileCmd);
      expect(verifyResult.output).toBeDefined();
      console.log(`Windows file content: ${verifyResult.output}`);
      expect(verifyResult.output).toContain(testContent);

      // Sync Windows session to upload data
      console.log("Syncing Windows session to upload data...");
      const windowsSyncResult = await windowsSession.context.sync();
      expect(windowsSyncResult.success).toBe(true);
      console.log(`Windows context sync successful (RequestID: ${windowsSyncResult.requestId})`);

      // Wait for upload to complete
      console.log("Waiting for upload to complete...");
      await new Promise((resolve) => setTimeout(resolve, 10000));

      // Delete Windows session
      console.log("Deleting Windows session...");
      const windowsDeleteResult = await agentBay.delete(windowsSession, true);
      console.log(
        `Windows session deleted: ${windowsSession.sessionId} (RequestID: ${windowsDeleteResult.requestId})`
      );

      // ========== Phase 2: Create Linux session with MappingPolicy and verify data ==========
      console.log("========== Phase 2: Linux Session - Access Data via MappingPolicy ==========");

      // Create mapping policy with Windows path
      const mappingPolicy: MappingPolicy = {
        path: windowsPath,
      };

      // Create sync policy with mapping policy for Linux session
      const linuxSyncPolicy: SyncPolicy = {
        uploadPolicy: newUploadPolicy(),
        downloadPolicy: newDownloadPolicy(),
        deletePolicy: newDeletePolicy(),
        extractPolicy: newExtractPolicy(),
        mappingPolicy: mappingPolicy,
      };

      // Create Linux session with context sync and mapping policy
      const linuxSessionParams = new CreateSessionParams();
      linuxSessionParams.addContextSync(context.id, linuxPath, linuxSyncPolicy);
      linuxSessionParams.withImageId("linux_latest");
      linuxSessionParams.withLabels({ test: "mapping-policy-linux" });

      // Create Linux session
      const linuxSessionResult = await agentBay.create(linuxSessionParams);
      expect(linuxSessionResult.session).toBeDefined();

      const linuxSession = linuxSessionResult.session!;
      console.log(
        `Created Linux session: ${linuxSession.sessionId} with mapping from ${windowsPath} to ${linuxPath}`
      );

      try {
        // Wait for Linux session to be ready and data to be downloaded
        console.log("Waiting for Linux session to be ready and data to be downloaded...");
        await new Promise((resolve) => setTimeout(resolve, 15000));

        // Verify file exists in Linux session at the mapped path
        const linuxTestFilePath = `${linuxPath}/${testFileName}`;
        console.log(`Verifying file exists in Linux at: ${linuxTestFilePath}`);

        // Check if file exists
        const checkFileCmd = `test -f "${linuxTestFilePath}" && echo "FILE_EXISTS" || echo "FILE_NOT_FOUND"`;
        const checkResult = await linuxSession.command.executeCommand(checkFileCmd);
        expect(checkResult).toBeDefined();
        console.log(`Linux file check result: ${checkResult.output}`);

        // Verify file exists
        expect(checkResult.output).toContain("FILE_EXISTS");

        // Read file content in Linux session
        const readFileCmd = `cat "${linuxTestFilePath}"`;
        const readResult = await linuxSession.command.executeCommand(readFileCmd);
        expect(readResult).toBeDefined();
        console.log(`Linux file content: ${readResult.output}`);

        // Verify file content matches
        expect(
          readResult.output.includes(testContent) || readResult.output.includes(testContent.trim())
        ).toBe(true);

        // Verify context info
        const contextInfo = await linuxSession.context.info();
        expect(contextInfo.requestId).toBeDefined();

        if (contextInfo.contextStatusData && contextInfo.contextStatusData.length > 0) {
          console.log("Context status data in Linux session:");
          contextInfo.contextStatusData.forEach((data: any, i: number) => {
            console.log(`Context Status Data [${i}]:`);
            console.log(`  ContextId: ${data.contextId}`);
            console.log(`  Path: ${data.path}`);
            console.log(`  Status: ${data.status}`);
            console.log(`  TaskType: ${data.taskType}`);
          });

          // Verify the context data
          const contextData = contextInfo.contextStatusData.find(
            (data: any) => data.contextId === context.id
          );
          if (contextData) {
            expect(contextData.path).toBe(linuxPath);
          }
        }

        console.log("========== Cross-platform mapping policy test completed successfully ==========");
        console.log("✓ Data created in Windows session was successfully accessed in Linux session via MappingPolicy");
      } finally {
        // Ensure Linux session is deleted
        const deleteResult = await agentBay.delete(linuxSession, true);
        console.log(
          `Linux session deleted: ${linuxSession.sessionId} (RequestID: ${deleteResult.requestId})`
        );
      }
    } finally {
      // Ensure context is deleted
      const deleteContextResult = await agentBay.context.delete(context);
      console.log(
        `Context deleted: ${context.id} (RequestID: ${deleteContextResult.requestId})`
      );
    }
  }, 180000);
});
