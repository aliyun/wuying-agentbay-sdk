import { AgentBay } from "../../src/agent-bay";
import { getTestApiKey } from '../../tests/utils/test-helpers';
import {
  newBasicContextSync,
  newContextSync,
  UploadStrategy,
  DownloadStrategy,
  UploadPolicy,
  DownloadPolicy,
  DeletePolicy,
  WhiteList,
  BWList,
  SyncPolicy,
  ContextSync
} from "../../src/context-sync";
import { newCreateSessionParams } from "../../src/session-params";

async function main() {
  // Get API key from environment variable
  const apiKey = getTestApiKey(); // Replace with your actual API key

  try {
    // Initialize the AgentBay client
    console.log("Initializing AgentBay client...");
    const ab = new AgentBay({ apiKey });

    // Example 1: Create a new context
    console.log("Example 1: Creating a new context...");
    // Use timestamp in context name to ensure uniqueness for each test run
    const contextName = `my-sync-context-${Date.now()}`;
    const contextResult = await ab.context.get(contextName, true);

    if (!contextResult.context) {
      throw new Error("Context not found and could not be created");
    }

    const context = contextResult.context;
    console.log(`Context created/retrieved: ${context.name} (ID: ${context.id})`);

    // Example 2: Create a basic context sync configuration
    console.log("\nExample 2: Creating a basic context sync configuration...");
    const basicSync = newBasicContextSync(context.id, "/home/wuying");
    console.log(`Basic sync - ContextID: ${basicSync.contextId}, Path: ${basicSync.path}`);

    // Example 3: Create an advanced context sync configuration with policies
    console.log("\nExample 3: Creating an advanced context sync configuration...");

    // Create upload policy
    const uploadPolicy: UploadPolicy = {
      autoUpload: true,
      uploadStrategy: UploadStrategy.PeriodicUpload,
      period: 15, // 15 minutes
    };

    // Create download policy
    const downloadPolicy: DownloadPolicy = {
      autoDownload: true,
      downloadStrategy: DownloadStrategy.DownloadAsync,
    };

    // Create delete policy
    const deletePolicy: DeletePolicy = {
      syncLocalFile: true,
    };

    // Create white list
    const whiteList: WhiteList = {
      path: "/data/important",
      excludePaths: ["/data/important/temp", "/data/important/logs"],
    };

    // Create BW list
    const bwList: BWList = {
      whiteLists: [whiteList],
    };

    // Create sync policy
    const syncPolicy: SyncPolicy = {
      uploadPolicy,
      downloadPolicy,
      deletePolicy,
      bwList,
    };

    // Create advanced sync configuration
    const advancedSync = new ContextSync(context.id, "/data", syncPolicy);

    console.log(`Advanced sync - ContextID: ${advancedSync.contextId}, Path: ${advancedSync.path}`);
    console.log(`  - Upload: Auto=${advancedSync.policy?.uploadPolicy?.autoUpload}, Strategy=${advancedSync.policy?.uploadPolicy?.uploadStrategy}, Period=${advancedSync.policy?.uploadPolicy?.period}`);
    console.log(`  - Download: Auto=${advancedSync.policy?.downloadPolicy?.autoDownload}, Strategy=${advancedSync.policy?.downloadPolicy?.downloadStrategy}`);
    console.log(`  - Delete: SyncLocalFile=${advancedSync.policy?.deletePolicy?.syncLocalFile}`);
    console.log(`  - WhiteList: Path=${advancedSync.policy?.bwList?.whiteLists?.[0]?.path}, ExcludePaths=${JSON.stringify(advancedSync.policy?.bwList?.whiteLists?.[0]?.excludePaths)}`);

    // Example 4: Create session parameters with context sync
    console.log("\nExample 4: Creating session parameters with context sync...");
    const sessionParams = newCreateSessionParams();

    // Method 1: Add context sync using addContextSync
    sessionParams.addContextSync(context.id, "/data", syncPolicy);

    // Method 2: Add context sync using addContextSyncConfig
    sessionParams.addContextSyncConfig(basicSync);

    // Set labels for the session
    sessionParams.withLabels({
      username: "alice",
      project: "context-sync-example",
    });

    sessionParams.withImageId("imgc-07eksy57eawchjkro");

    console.log(`Session params created with ${sessionParams.contextSync.length} context sync configurations`);

    // Example 5: Create session with context sync
    console.log("\nExample 5: Creating session with context sync...");
    const sessionResult = await ab.create(sessionParams);

    const session = sessionResult.session;
    console.log(`Session created with ID: ${session.sessionId}`);
    console.log(`Session creation RequestID: ${sessionResult.requestId}`);

    // Example 6: Use context manager from session
    console.log("\nExample 6: Using context manager from session...");

    try {
      // Get context info
      const contextInfo = await session.context.info();
      console.log(`Context status: ${contextInfo.contextStatus} (RequestID: ${contextInfo.requestId})`);
    } catch (error) {
      console.error(`Error getting context info: ${error}`);
    }

    try {
      // Sync context
      const syncResult = await session.context.sync();
      console.log(`Context sync success: ${syncResult.success} (RequestID: ${syncResult.requestId})`);
    } catch (error) {
      console.error(`Error syncing context: ${error}`);
    }

    // Example 7: Alternative way using builder pattern
    console.log("\nExample 7: Using builder pattern for context sync...");
    const builderSync = newContextSync(context.id, "/workspace")
      .withUploadPolicy({
        autoUpload: true,
        uploadStrategy: UploadStrategy.UploadBeforeResourceRelease,
      })
      .withDownloadPolicy({
        autoDownload: true,
        downloadStrategy: DownloadStrategy.DownloadAsync,
      })
      .withWhiteList("/workspace/src", ["/workspace/src/node_modules"]);

    console.log(`Builder sync - ContextID: ${builderSync.contextId}, Path: ${builderSync.path}`);

    // Clean up
    console.log("\nCleaning up...");

    try {
      // Delete the session
      const deleteResult = await ab.delete(session);
      console.log(`Session deleted successfully (RequestID: ${deleteResult.requestId})`);
    } catch (error) {
      console.error(`Error deleting session: ${error}`);
    }

    try {
      // Delete the context
      const deleteContextResult = await ab.context.delete(context);
      console.log(`Context deleted successfully (RequestID: ${deleteContextResult.requestId})`);
    } catch (error) {
      console.error(`Error deleting context: ${error}`);
    }

    console.log("\nContext sync example completed!");

  } catch (error) {
    console.error(`Fatal error: ${error}`);
    process.exit(1);
  }
}

// Execute the main function
if (require.main === module) {
  main().catch((error) => {
    console.error(`Unhandled error: ${error}`);
    process.exit(1);
  });
}

export { main };
