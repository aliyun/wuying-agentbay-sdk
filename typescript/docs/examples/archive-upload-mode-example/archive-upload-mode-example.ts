import { AgentBay, CreateSessionParams, Session, newContextSync, newSyncPolicy, FileSystem, UploadMode } from "wuying-agentbay-sdk";

/**
 * Archive Upload Mode Context Sync Example
 * 
 * This example demonstrates how to use Archive upload mode for context synchronization.
 * Archive mode compresses files before uploading, which is more efficient for large files
 * or when dealing with many files.
 * 
 * Features demonstrated:
 * - Creating context with Archive upload mode
 * - Session creation with context sync
 * - File operations in the context path
 * - Context sync and info operations
 * - Proper cleanup and error handling
 */

function getAPIKey(): string {
  const apiKey = process.env.AGENTBAY_API_KEY;
  if (!apiKey) {
    console.warn("Warning: AGENTBAY_API_KEY environment variable not set. Using default key.");
    return "your-api-key-here"; // Replace with your actual API key
  }
  return apiKey;
}

function generateUniqueId(): string {
  const timestamp = Date.now() * 1000 + Math.floor(Math.random() * 1000);
  const randomPart = Math.floor(Math.random() * 10000);
  return `${timestamp}-${randomPart}`;
}

async function archiveUploadModeExample(): Promise<void> {
  console.log("🚀 Archive Upload Mode Context Sync Example");
  console.log("=" .repeat(60));

  // Initialize AgentBay client
  const agentBay = new AgentBay({ apiKey: getAPIKey() });
  const uniqueId = generateUniqueId();
  
  let session: Session | null = null;

  try {
    // Step 1: Create context for Archive mode
    console.log("\n📦 Step 1: Creating context for Archive upload mode...");
    const contextName = `archive-mode-context-${uniqueId}`;
    const contextResult = await agentBay.context.get(contextName, true);
    
    if (!contextResult.success) {
      throw new Error(`Context creation failed: ${contextResult.errorMessage}`);
    }
    
    console.log(`✅ Context created successfully!`);
    console.log(`   Context ID: ${contextResult.contextId}`);
    console.log(`   Request ID: ${contextResult.requestId}`);

    // Step 2: Configure sync policy with Archive upload mode
    console.log("\n⚙️  Step 2: Configuring sync policy with Archive upload mode...");
    const syncPolicy = newSyncPolicy();
    syncPolicy.uploadPolicy!.uploadMode = UploadMode.Archive; // Set to Archive mode
    
    console.log(`✅ Sync policy configured with uploadMode: ${syncPolicy.uploadPolicy!.uploadMode}`);

    // Step 3: Create context sync configuration
    console.log("\n🔧 Step 3: Creating context sync configuration...");
    const contextSync = newContextSync(
      contextResult.contextId,
      "/tmp/archive-mode-test",
      syncPolicy
    );

    console.log(`✅ Context sync created:`);
    console.log(`   Context ID: ${contextSync.contextId}`);
    console.log(`   Path: ${contextSync.path}`);
    console.log(`   Upload Mode: ${contextSync.policy?.uploadPolicy?.uploadMode}`);

    // Step 4: Create session with Archive mode context sync
    console.log("\n🏗️  Step 4: Creating session with Archive mode context sync...");
    const sessionParams: CreateSessionParams = {
      labels: {
        example: `archive-mode-${uniqueId}`,
        type: "archive-upload-demo",
        uploadMode: UploadMode.Archive
      },
      contextSync: [contextSync]
    };

    const sessionResult = await agentBay.create(sessionParams);
    if (!sessionResult.success) {
      throw new Error(`Session creation failed: ${sessionResult.errorMessage}`);
    }

    session = sessionResult.session!;
    console.log(`✅ Session created successfully!`);
    console.log(`   Session ID: ${session!.sessionId}`);
    console.log(`   Request ID: ${sessionResult.requestId}`);

    // Get session info to verify setup
    const sessionInfo = await agentBay.getSession(session!.sessionId);
    if (sessionInfo.success && sessionInfo.data) {
      console.log(`   App Instance ID: ${sessionInfo.data.appInstanceId}`);
    }

    // Step 5: Create and write test files
    console.log("\n📝 Step 5: Creating test files in Archive mode context...");
    const fileSystem = new FileSystem(session!);
    
    // Generate 5KB test content
    const contentSize = 5 * 1024; // 5KB
    const baseContent = "Archive mode test successful! This is a test file created in the session path. ";
    const repeatedContent = baseContent.repeat(Math.ceil(contentSize / baseContent.length));
    const fileContent = repeatedContent.substring(0, contentSize);
    
    const filePath = "/tmp/archive-mode-test/test-file-5kb.txt";
    
    console.log(`📄 Creating file: ${filePath}`);
    console.log(`📊 File content size: ${fileContent.length} bytes`);

    const writeResult = await fileSystem.writeFile(filePath, fileContent, "overwrite");
    
    if (!writeResult.success) {
      throw new Error(`File write failed: ${writeResult.errorMessage}`);
    }

    console.log(`✅ File write successful!`);
    console.log(`   Request ID: ${writeResult.requestId}`);

    // Step 6: Test context info functionality
    console.log("\n📊 Step 6: Testing context info functionality...");
    const infoResult = await session!.context.info();
    
    if (!infoResult.success) {
      throw new Error(`Context info failed: ${infoResult.errorMessage}`);
    }

    console.log(`✅ Context info retrieved successfully!`);
    console.log(`   Request ID: ${infoResult.requestId}`);
    console.log(`   Context status data count: ${infoResult.contextStatusData.length}`);
    
    // Display context status details
    if (infoResult.contextStatusData.length > 0) {
      console.log("\n📋 Context status details:");
      infoResult.contextStatusData.forEach((status:any, index:any) => {
        console.log(`   [${index}] Context ID: ${status.contextId}`);
        console.log(`       Path: ${status.path}`);
        console.log(`       Status: ${status.status}`);
        console.log(`       Task Type: ${status.taskType}`);
        if (status.errorMessage) {
          console.log(`       Error: ${status.errorMessage}`);
        }
      });
    }

    // Step 7: Verify file information
    console.log("\n🔍 Step 7: Verifying file information...");
    const fileInfoResult = await fileSystem.getFileInfo(filePath);
    
    if (!fileInfoResult.success) {
      throw new Error(`Get file info failed: ${fileInfoResult.errorMessage}`);
    }

    console.log(`✅ File info retrieved successfully!`);
    console.log(`   Request ID: ${fileInfoResult.requestId}`);
    
    if (fileInfoResult.fileInfo) {
      console.log(`📄 File details:`);
      console.log(`   Size: ${fileInfoResult.fileInfo.size} bytes`);
      console.log(`   Is Directory: ${fileInfoResult.fileInfo.isDirectory}`);
      console.log(`   Modified Time: ${fileInfoResult.fileInfo.modTime}`);
      console.log(`   Mode: ${fileInfoResult.fileInfo.mode}`);
    }

    console.log("\n🎉 Archive upload mode example completed successfully!");
    console.log("✅ All operations completed without errors.");

  } catch (error) {
    console.error("\n❌ Error occurred during example execution:");
    console.error(error);
  } finally {
    // Step 8: Cleanup
    if (session) {
      console.log("\n🧹 Step 8: Cleaning up session...");
      try {
        const deleteResult = await agentBay.delete(session, true);
        console.log(`✅ Session deleted successfully!`);
        console.log(`   Success: ${deleteResult.success}`);
        console.log(`   Request ID: ${deleteResult.requestId}`);
      } catch (deleteError) {
        console.error(`❌ Failed to delete session: ${deleteError}`);
      }
    }
  }
}

// Main execution
async function main(): Promise<void> {
  try {
    await archiveUploadModeExample();
  } catch (error) {
    console.error("❌ Example execution failed:", error);
    process.exit(1);
  }
}

// Run the example if this file is executed directly
if (require.main === module) {
  main().catch((error) => {
    console.error("❌ Unhandled error:", error);
    process.exit(1);
  });
}

export { archiveUploadModeExample };