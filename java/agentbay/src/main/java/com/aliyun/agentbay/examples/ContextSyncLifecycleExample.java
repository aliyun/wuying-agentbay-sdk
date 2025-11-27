package com.aliyun.agentbay.examples;

import com.aliyun.agentbay.AgentBay;
import com.aliyun.agentbay.context.*;
import com.aliyun.agentbay.exception.AgentBayException;
import com.aliyun.agentbay.model.BoolResult;
import com.aliyun.agentbay.model.CommandResult;
import com.aliyun.agentbay.model.DeleteResult;
import com.aliyun.agentbay.model.SessionResult;
import com.aliyun.agentbay.session.CreateSessionParams;
import com.aliyun.agentbay.session.Session;

import java.util.Arrays;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.TimeUnit;

/**
 * Context Sync Lifecycle Example - Java equivalent of Python context_sync_demo.py
 * 
 * This example demonstrates the complete context synchronization lifecycle:
 * 1. Creating a persistent context
 * 2. Creating a session with context sync
 * 3. Creating test data in the session
 * 4. Using session.context.sync() with different modes:
 *    - Basic sync (trigger only)
 *    - Sync with callback (async mode)
 *    - syncAndWait (blocking mode)
 * 5. Monitoring sync status with session.context.info()
 * 6. Deleting session with context sync
 * 7. Verifying data persistence in a new session
 */
public class ContextSyncLifecycleExample {
    
    /**
     * Helper method to repeat a string n times (Java 8 compatible)
     */
    private static String repeat(String str, int count) {
        if (count <= 0) return "";
        StringBuilder sb = new StringBuilder(str.length() * count);
        for (int i = 0; i < count; i++) {
            sb.append(str);
        }
        return sb.toString();
    }
    
    public static void main(String[] args) {
        try {
            // Initialize AgentBay client
            String apiKey = System.getenv("AGENTBAY_API_KEY");
            if (apiKey == null || apiKey.isEmpty()) {
                System.err.println("❌ Please set AGENTBAY_API_KEY environment variable");
                return;
            }
            
            AgentBay agentBay = new AgentBay(apiKey);
            System.out.println("✅ AgentBay client initialized");
            
            // Example 1: Basic context sync (trigger only)
            System.out.println("\n" + repeat("=", 60));
            basicContextSyncExample(agentBay);
            
            // Example 2: Context sync with callback (async mode)
            System.out.println("\n" + repeat("=", 60));
            contextSyncWithCallbackExample(agentBay);
            
            // Example 3: Context sync and wait (blocking mode)
            System.out.println("\n" + repeat("=", 60));
            contextSyncAndWaitExample(agentBay);
            
            // Example 4: Complete context persistence workflow
            System.out.println("\n" + repeat("=", 60));
            completeContextPersistenceWorkflow(agentBay);
            
            System.out.println("\n" + repeat("=", 60));
            System.out.println("🎉 All Context Sync Lifecycle examples completed!");
            
        } catch (Exception e) {
            System.err.println("❌ Error: " + e.getMessage());
            e.printStackTrace();
        }
    }
    
    /**
     * Example 1: Basic context sync (trigger only)
     * 
     * This example demonstrates:
     * - Creating a session with context sync
     * - Creating test data
     * - Triggering sync without waiting for completion
     */
    private static void basicContextSyncExample(AgentBay agentBay) throws AgentBayException {
        System.out.println("Example 1: Basic Context Sync (Trigger Only)");
        System.out.println(repeat("-", 60));
        
        // Step 1: Create a persistent context
        String contextName = "sync-basic-demo-" + System.currentTimeMillis();
        System.out.println("📦 Step 1: Creating persistent context: " + contextName);
        
        ContextResult contextResult = agentBay.getContext().get(contextName, true);
        if (!contextResult.isSuccess() || contextResult.getContext() == null) {
            System.err.println("❌ Failed to create context: " + contextResult.getErrorMessage());
            return;
        }
        
        Context context = contextResult.getContext();
        System.out.println("✅ Context created with ID: " + context.getId());
        
        Session session = null;
        
        try {
            // Step 2: Create session with context sync
            System.out.println("\n🌐 Step 2: Creating session with context sync");
            CreateSessionParams params = new CreateSessionParams();
            SyncPolicy syncPolicy = SyncPolicy.defaultPolicy();
            ContextSync contextSync = ContextSync.create(
                context.getId(),
                "/tmp/sync_data",
                syncPolicy
            );
            params.setContextSyncs(Arrays.asList(contextSync));
            params.setImageId("linux_latest");
            
            SessionResult result = agentBay.create(params);
            if (!result.isSuccess() || result.getSession() == null) {
                System.err.println("❌ Failed to create session: " + result.getErrorMessage());
                return;
            }
            
            session = result.getSession();
            System.out.println("✅ Session created: " + session.getSessionId());
            
            // Step 3: Create test data
            System.out.println("\n💾 Step 3: Creating test data...");
            CommandResult cmdResult = session.getCommand().executeCommand(
                "mkdir -p /tmp/sync_data/test_files",
                5000
            );
            if (!cmdResult.isSuccess()) {
                System.err.println("❌ Failed to create directory: " + cmdResult.getErrorMessage());
                return;
            }
            
            // Create test files
            String[] testFiles = {
                "/tmp/sync_data/test_files/small.txt",
                "/tmp/sync_data/test_files/medium.txt",
                "/tmp/sync_data/config.json"
            };
            
            int createdFiles = 0;
            for (String filePath : testFiles) {
                String content = "Test content for " + filePath + "\n";
                BoolResult fileResult = session.getFileSystem().writeFile(
                    filePath,
                    content
                );
                if (fileResult.isSuccess()) {
                    System.out.println("✅ Created file: " + filePath);
                    createdFiles++;
                } else {
                    System.err.println("❌ Failed to create file " + filePath + ": " + fileResult.getErrorMessage());
                }
            }
            
            System.out.println("📊 Created " + createdFiles + "/" + testFiles.length + " test files");
            
            // Step 4: Trigger sync (without waiting)
            System.out.println("\n📤 Step 4: Triggering context sync...");
            ContextSyncResult syncResult = session.getContext().sync();
            
            if (!syncResult.isSuccess()) {
                System.err.println("❌ Failed to trigger context sync: " + syncResult.getErrorMessage());
                return;
            }
            
            System.out.println("⚡ Context sync triggered successfully");
            System.out.println("   Request ID: " + syncResult.getRequestId());
            System.out.println("   Initial success: " + syncResult.isSuccess());
            System.out.println("💡 Note: Sync is now running in the background");
            
        } finally {
            // Clean up
            if (session != null) {
                System.out.println("\n🧹 Cleaning up session...");
                agentBay.delete(session, false);
                System.out.println("✅ Session deleted");
            }
            
            try {
                agentBay.getContext().delete(context);
                System.out.println("🧹 Context cleaned up");
            } catch (Exception e) {
                System.err.println("⚠️  Warning: Failed to delete context: " + e.getMessage());
            }
        }
    }
    
    /**
     * Example 2: Context sync with callback (async mode)
     * 
     * This example demonstrates:
     * - Using callback mode for non-blocking sync
     * - Monitoring sync completion asynchronously
     */
    private static void contextSyncWithCallbackExample(AgentBay agentBay) throws Exception {
        System.out.println("Example 2: Context Sync with Callback (Async Mode)");
        System.out.println(repeat("-", 60));
        System.out.println("📤 This method uses callback for completion notification");
        System.out.println("⚡ Function returns immediately, callback handles completion");
        
        // Create context and session
        String contextName = "sync-callback-demo-" + System.currentTimeMillis();
        System.out.println("\n📦 Creating context and session...");
        
        ContextResult contextResult = agentBay.getContext().get(contextName, true);
        if (!contextResult.isSuccess()) {
            System.err.println("❌ Context creation failed: " + contextResult.getErrorMessage());
            return;
        }
        
        Context context = contextResult.getContext();
        System.out.println("✅ Context created: " + context.getId());
        
        Session session = null;
        
        try {
            // Create session with context sync
            CreateSessionParams params = new CreateSessionParams();
            SyncPolicy syncPolicy = SyncPolicy.defaultPolicy();
            ContextSync contextSync = ContextSync.create(
                context.getId(),
                "/tmp/sync_data",
                syncPolicy
            );
            params.setContextSyncs(Arrays.asList(contextSync));
            params.setImageId("linux_latest");
            
            SessionResult result = agentBay.create(params);
            session = result.getSession();
            System.out.println("✅ Session created: " + session.getSessionId());
            
            // Create test data
            System.out.println("\n💾 Creating test data...");
            session.getCommand().executeCommand("mkdir -p /tmp/sync_data/test_files", 5000);
            
            BoolResult fileResult = session.getFileSystem().writeFile(
                "/tmp/sync_data/test_files/test.txt",
                "Test content\n"
            );
            
            if (fileResult.isSuccess()) {
                System.out.println("✅ Created test file");
            }
            
            // Create a CompletableFuture to wait for callback
            CompletableFuture<Boolean> callbackFuture = new CompletableFuture<>();
            final Session finalSession = session;
            
            long syncStartTime = System.currentTimeMillis();
            
            // Call context.sync() with callback - immediate return
            System.out.println("\n📤 Calling session.context.sync() with callback...");
            ContextSyncResult syncResult = finalSession.getContext().sync(success -> {
                long duration = System.currentTimeMillis() - syncStartTime;
                System.out.println("✅ Callback received: " + (success ? "SUCCESS" : "FAILED") + 
                                 " in " + (duration / 1000.0) + " seconds");
                System.out.println("   📊 " + (success ? "All files synchronized successfully" : 
                                            "Some files may have failed to synchronize"));
                callbackFuture.complete(success);
            });
            
            if (!syncResult.isSuccess()) {
                System.err.println("❌ Failed to initiate context sync: " + syncResult.getErrorMessage());
                return;
            }
            
            System.out.println("⚡ Context sync initiated successfully (immediate return)");
            System.out.println("   Request ID: " + syncResult.getRequestId());
            System.out.println("   Initial success: " + syncResult.isSuccess());
            System.out.println("⏳ Waiting for callback completion...");
            
            // Wait for callback (max 5 minutes)
            Boolean callbackSuccess = callbackFuture.get(5, TimeUnit.MINUTES);
            
            if (callbackSuccess) {
                System.out.println("🎉 Callback-based sync completed successfully!");
            } else {
                System.err.println("❌ Sync failed according to callback");
            }
            
        } finally {
            // Clean up
            if (session != null) {
                System.out.println("\n🧹 Cleaning up session...");
                agentBay.delete(session, false);
                System.out.println("✅ Session deleted");
            }
            
            try {
                agentBay.getContext().delete(context);
                System.out.println("🧹 Context cleaned up");
            } catch (Exception e) {
                System.err.println("⚠️  Warning: Failed to delete context: " + e.getMessage());
            }
        }
    }
    
    /**
     * Example 3: Context sync and wait (blocking mode)
     * 
     * This example demonstrates:
     * - Using syncAndWait for blocking sync operation
     * - Waiting for sync completion before proceeding
     */
    private static void contextSyncAndWaitExample(AgentBay agentBay) throws AgentBayException {
        System.out.println("Example 3: Context Sync and Wait (Blocking Mode)");
        System.out.println(repeat("-", 60));
        System.out.println("📤 This method waits for sync completion");
        System.out.println("⏳ Function blocks until sync is complete");
        
        // Create context and session
        String contextName = "sync-wait-demo-" + System.currentTimeMillis();
        System.out.println("\n📦 Creating context and session...");
        
        ContextResult contextResult = agentBay.getContext().get(contextName, true);
        if (!contextResult.isSuccess()) {
            System.err.println("❌ Context creation failed: " + contextResult.getErrorMessage());
            return;
        }
        
        Context context = contextResult.getContext();
        System.out.println("✅ Context created: " + context.getId());
        
        Session session = null;
        
        try {
            // Create session with context sync
            CreateSessionParams params = new CreateSessionParams();
            SyncPolicy syncPolicy = SyncPolicy.defaultPolicy();
            ContextSync contextSync = ContextSync.create(
                context.getId(),
                "/tmp/sync_data",
                syncPolicy
            );
            params.setContextSyncs(Arrays.asList(contextSync));
            params.setImageId("linux_latest");
            
            SessionResult result = agentBay.create(params);
            session = result.getSession();
            System.out.println("✅ Session created: " + session.getSessionId());
            
            // Create test data
            System.out.println("\n💾 Creating test data...");
            session.getCommand().executeCommand("mkdir -p /tmp/sync_data/test_files", 5000);
            
            BoolResult fileResult = session.getFileSystem().writeFile(
                "/tmp/sync_data/test_files/test.txt",
                "Test content\n"
            );
            
            if (fileResult.isSuccess()) {
                System.out.println("✅ Created test file");
            }
            
            // Call syncAndWait - this will block until sync completes
            System.out.println("\n📤 Calling session.context.syncAndWait()...");
            long syncStartTime = System.currentTimeMillis();
            
            ContextSyncResult syncResult = session.getContext().syncAndWait();
            
            long syncDuration = System.currentTimeMillis() - syncStartTime;
            
            if (syncResult.isSuccess()) {
                System.out.println("✅ Sync completed successfully");
                System.out.println("   Request ID: " + syncResult.getRequestId());
                System.out.println("   Final success: " + syncResult.isSuccess());
                System.out.println("   Duration: " + (syncDuration / 1000.0) + " seconds");
            } else {
                System.err.println("❌ Sync failed");
                System.out.println("   Request ID: " + syncResult.getRequestId());
                System.out.println("   Final success: " + syncResult.isSuccess());
                System.out.println("   Duration: " + (syncDuration / 1000.0) + " seconds");
            }
            
        } finally {
            // Clean up
            if (session != null) {
                System.out.println("\n🧹 Cleaning up session...");
                agentBay.delete(session, false);
                System.out.println("✅ Session deleted");
            }
            
            try {
                agentBay.getContext().delete(context);
                System.out.println("🧹 Context cleaned up");
            } catch (Exception e) {
                System.err.println("⚠️  Warning: Failed to delete context: " + e.getMessage());
            }
        }
    }
    
    /**
     * Example 4: Complete context persistence workflow
     * 
     * This example demonstrates:
     * - Creating data in first session
     * - Syncing and deleting session with sync_context=true
     * - Creating second session with same context
     * - Verifying data persisted
     */
    private static void completeContextPersistenceWorkflow(AgentBay agentBay) throws Exception {
        System.out.println("Example 4: Complete Context Persistence Workflow");
        System.out.println(repeat("-", 60));
        
        // Create a unique context name
        String contextName = "workflow-demo-" + System.currentTimeMillis();
        
        System.out.println("📦 Step 1: Creating persistent context...");
        ContextResult contextResult = agentBay.getContext().get(contextName, true);
        if (!contextResult.isSuccess() || contextResult.getContext() == null) {
            System.err.println("❌ Failed to create context");
            return;
        }
        
        Context context = contextResult.getContext();
        System.out.println("✅ Context created: " + context.getName() + " (ID: " + context.getId() + ")");
        
        Session session1 = null;
        Session session2 = null;
        
        try {
            // Create first session
            System.out.println("\n🌐 Step 2: Creating first session...");
            CreateSessionParams params = new CreateSessionParams();
            SyncPolicy syncPolicy = SyncPolicy.defaultPolicy();
            ContextSync contextSync = ContextSync.create(
                context.getId(),
                "/tmp/persist_data",
                syncPolicy
            );
            params.setContextSyncs(Arrays.asList(contextSync));
            params.setImageId("linux_latest");
            
            SessionResult result1 = agentBay.create(params);
            if (!result1.isSuccess() || result1.getSession() == null) {
                System.err.println("❌ Failed to create first session");
                return;
            }
            
            session1 = result1.getSession();
            System.out.println("✅ First session created: " + session1.getSessionId());
            
            // Create test data
            System.out.println("\n💾 Step 3: Creating test data in first session...");
            session1.getCommand().executeCommand("mkdir -p /tmp/persist_data", 5000);
            
            String testContent = "Data from first session - timestamp: " + System.currentTimeMillis();
            BoolResult fileResult = session1.getFileSystem().writeFile(
                "/tmp/persist_data/persistent_file.txt",
                testContent
            );
            
            if (fileResult.isSuccess()) {
                System.out.println("✅ Created test file with content: " + testContent);
            } else {
                System.err.println("❌ Failed to create test file");
                return;
            }
            
            // Sync data
            System.out.println("\n📤 Step 4: Syncing context data...");
            ContextSyncResult syncResult = session1.getContext().syncAndWait();
            if (syncResult.isSuccess()) {
                System.out.println("✅ Context sync completed successfully");
            } else {
                System.err.println("❌ Context sync failed");
                return;
            }
            
            // Delete first session WITH context sync
            System.out.println("\n🗑️  Step 5: Deleting first session WITH context sync...");
            DeleteResult deleteResult = agentBay.delete(session1, true);
            
            if (deleteResult.isSuccess()) {
                System.out.println("✅ First session deleted (RequestID: " + deleteResult.getRequestId() + ")");
                System.out.println("✅ Context data uploaded to cloud storage");
                session1 = null;  // Mark as deleted
            } else {
                System.err.println("❌ Failed to delete session: " + deleteResult.getErrorMessage());
                return;
            }
            
            // Wait for context sync to complete
            System.out.println("\n⏳ Waiting for context synchronization to complete...");
            Thread.sleep(3000);
            System.out.println("✅ Context sync completed");
            
            // Create second session with same context
            System.out.println("\n🌐 Step 6: Creating second session with same context...");
            SessionResult result2 = agentBay.create(params);
            
            if (result2.isSuccess() && result2.getSession() != null) {
                session2 = result2.getSession();
                System.out.println("✅ Second session created: " + session2.getSessionId());
                System.out.println("✅ Context data automatically restored from cloud storage!");
                
                // Verify data persisted
                System.out.println("\n🔍 Step 7: Verifying data persistence...");
                try {
                    String restoredContent = session2.getFileSystem().read("/tmp/persist_data/persistent_file.txt");
                    System.out.println("✅ File content restored: " + restoredContent);
                    
                    if (testContent.equals(restoredContent)) {
                        System.out.println("✅ Content matches! Data persisted correctly!");
                    } else {
                        System.err.println("❌ Content mismatch!");
                        System.out.println("   Expected: " + testContent);
                        System.out.println("   Got: " + restoredContent);
                    }
                } catch (AgentBayException e) {
                    System.err.println("❌ Failed to read file: " + e.getMessage());
                }
                
            } else {
                System.err.println("❌ Failed to create second session");
            }
            
        } finally {
            // Clean up sessions
            if (session1 != null) {
                System.out.println("\n🧹 Cleaning up first session...");
                agentBay.delete(session1, false);
            }
            
            if (session2 != null) {
                System.out.println("🧹 Cleaning up second session...");
                agentBay.delete(session2, false);
            }
            
            // Clean up context
            try {
                agentBay.getContext().delete(context);
                System.out.println("🧹 Context cleaned up");
            } catch (Exception e) {
                System.err.println("⚠️  Warning: Failed to delete context: " + e.getMessage());
            }
        }
        
        System.out.println("\n🎯 Key Takeaways:");
        System.out.println("   1. Context sync enables persistent data across sessions");
        System.out.println("   2. Use syncAndWait() to ensure sync completes before proceeding");
        System.out.println("   3. Delete session with sync_context=true to upload data");
        System.out.println("   4. Next session with same context_id will restore all data");
        System.out.println("   5. Supports callback mode for async operations");
    }
}

