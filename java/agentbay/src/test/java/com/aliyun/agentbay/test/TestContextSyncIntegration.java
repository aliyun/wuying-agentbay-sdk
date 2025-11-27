package com.aliyun.agentbay.test;

import com.aliyun.agentbay.AgentBay;
import com.aliyun.agentbay.context.*;
import com.aliyun.agentbay.exception.AgentBayException;
import com.aliyun.agentbay.model.BoolResult;
import com.aliyun.agentbay.model.CommandResult;
import com.aliyun.agentbay.model.DeleteResult;
import com.aliyun.agentbay.model.SessionResult;
import com.aliyun.agentbay.session.CreateSessionParams;
import com.aliyun.agentbay.session.Session;
import org.junit.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.Arrays;

import static org.junit.Assert.*;

/**
 * Integration tests for context synchronization functionality
 * Tests complete context sync workflow across multiple sessions
 * 
 * This test is equivalent to Python's test_context_sync_integration.py
 */
public class TestContextSyncIntegration {
    private static final Logger logger = LoggerFactory.getLogger(TestContextSyncIntegration.class);
    
    private static AgentBay agentBay;
    
    @BeforeClass
    public static void setUpClass() throws AgentBayException {
        // Skip if no API key is available or in CI environment
        String apiKey = System.getenv("AGENTBAY_API_KEY");
        String ci = System.getenv("CI");
        if (apiKey == null || apiKey.trim().isEmpty() || "true".equals(ci)) {
            throw new IllegalStateException(
                "Skipping integration test: No API key available or running in CI"
            );
        }
        
        // Initialize AgentBay client
        agentBay = new AgentBay(apiKey);
        logger.info("AgentBay client initialized");
    }
    
    /**
     * Test context synchronization persistence with retry
     * 
     * This test verifies the complete context sync workflow:
     * 1. Create a context
     * 2. Create first session with context sync
     * 3. Create a test file in the sync path
     * 4. Trigger context sync
     * 5. Delete first session with sync_context=true
     * 6. Create second session with same context
     * 7. Verify file exists in second session
     */
    @Test
    public void testContextSyncPersistenceWithRetry() throws Exception {
        logger.info("Test: Context sync persistence with retry");
        
        // 1. Create a unique context name and get its ID
        String contextName = "test-persistence-retry-java-" + System.currentTimeMillis();
        ContextResult contextResult = agentBay.getContext().get(contextName, true);
        assertTrue("Error getting/creating context", contextResult.isSuccess());
        assertNotNull("Context should not be None", contextResult.getContext());
        
        Context context = contextResult.getContext();
        logger.info("Created context: {} (ID: {})", context.getName(), context.getId());
        
        Session session1 = null;
        Session session2 = null;
        
        try {
            // 2. Create a session with context sync, using a timestamped path under /home/wuying/
            long timestamp = System.currentTimeMillis();
            String syncPath = "/home/wuying/test-path-java-" + timestamp;
            
            // Use default policy
            SyncPolicy defaultPolicy = SyncPolicy.defaultPolicy();
            
            // Create session parameters with context sync
            CreateSessionParams sessionParams = new CreateSessionParams();
            ContextSync contextSync = ContextSync.create(context.getId(), syncPath, defaultPolicy);
            sessionParams.setContextSyncs(Arrays.asList(contextSync));
            sessionParams.setImageId("linux_latest");
            
            // Create first session
            SessionResult sessionResult = agentBay.create(sessionParams);
            assertTrue("Error creating first session", sessionResult.isSuccess());
            assertNotNull("Session should not be null", sessionResult.getSession());
            
            session1 = sessionResult.getSession();
            logger.info("Created first session: {}", session1.getSessionId());
            
            // 3. Wait for session to be ready and retry context info until data is available
            logger.info("Waiting for session to be ready and context status data to be available...");
            
            boolean foundData = false;
            ContextInfoResult contextInfo = null;
            
            for (int i = 0; i < 20; i++) {
                contextInfo = session1.getContext().info();
                
                if (!contextInfo.getContextStatusData().isEmpty()) {
                    logger.info("Found context status data on attempt {}", i + 1);
                    foundData = true;
                    break;
                }
                
                logger.info("No context status data available yet (attempt {}), retrying in 1 second...", i + 1);
                Thread.sleep(1000);
            }
            
            assertTrue("Context status data should be available after retries", foundData);
            printContextStatusData(contextInfo.getContextStatusData());
            
            // 4. Create a test file in the context sync path
            String testFilePath = syncPath + "/test-file.txt";
            // Build test content using StringBuilder for Java 8 compatibility
            StringBuilder contentBuilder = new StringBuilder();
            for (int i = 0; i < 100; i++) {
                contentBuilder.append("Test content for context sync persistence\n");
            }
            String testContent = contentBuilder.toString();
            
            // Create directory first
            logger.info("Creating directory: {}", syncPath);
            BoolResult dirResult = session1.getFileSystem().createDirectory(syncPath);
            assertTrue("Error creating directory", dirResult.isSuccess());
            
            // Create test file
            logger.info("Creating test file at {}", testFilePath);
            BoolResult fileResult = session1.getFileSystem().writeFile(
                testFilePath, 
                testContent
            );
            assertTrue("Error creating test file", fileResult.isSuccess());
            logger.info("Created test file successfully");
            
            // 5. Sync to trigger file upload
            logger.info("Triggering context sync...");
            ContextSyncResult syncResult = session1.getContext().syncAndWait();
            assertTrue("Context sync should be successful", syncResult.isSuccess());
            logger.info("Context sync successful (RequestID: {})", syncResult.getRequestId());
            
            // 6. Get context info with retry for upload status
            logger.info("Checking file upload status with retry...");
            
            boolean foundUpload = false;
            for (int i = 0; i < 20; i++) {
                contextInfo = session1.getContext().info();
                
                // Check if we have upload status for our context
                for (ContextStatusData data : contextInfo.getContextStatusData()) {
                    if (data.getContextId().equals(context.getId()) && "upload".equals(data.getTaskType())) {
                        foundUpload = true;
                        logger.info("Found upload task for context at attempt {}", i + 1);
                        break;
                    }
                }
                
                if (foundUpload) {
                    break;
                }
                
                logger.info("No upload status found yet (attempt {}), retrying in 1 second...", i + 1);
                Thread.sleep(1000);
            }
            
            if (foundUpload) {
                logger.info("Found upload status for context");
                printContextStatusData(contextInfo.getContextStatusData());
            } else {
                logger.warn("Warning: Could not find upload status after all retries");
            }
            
            // 7. Release first session
            logger.info("Releasing first session...");
            DeleteResult deleteResult = agentBay.delete(session1, true);
            assertTrue("Error deleting first session", deleteResult.isSuccess());
            session1 = null;  // Mark as deleted
            
            // 8. Create a second session with the same context
            logger.info("Creating second session with the same context...");
            sessionParams = new CreateSessionParams();
            contextSync = ContextSync.create(context.getId(), syncPath, defaultPolicy);
            sessionParams.setContextSyncs(Arrays.asList(contextSync));
            sessionParams.setImageId("linux_latest");
            
            sessionResult = agentBay.create(sessionParams);
            assertTrue("Error creating second session", sessionResult.isSuccess());
            assertNotNull("Second session should not be null", sessionResult.getSession());
            
            session2 = sessionResult.getSession();
            logger.info("Created second session: {}", session2.getSessionId());
            
            // 9. Get context info with retry for download status
            logger.info("Checking file download status with retry...");
            
            boolean foundDownload = false;
            for (int i = 0; i < 20; i++) {
                contextInfo = session2.getContext().info();
                
                // Check if we have download status for our context
                for (ContextStatusData data : contextInfo.getContextStatusData()) {
                    if (data.getContextId().equals(context.getId()) && "download".equals(data.getTaskType())) {
                        foundDownload = true;
                        logger.info("Found download task for context at attempt {}", i + 1);
                        break;
                    }
                }
                
                if (foundDownload) {
                    break;
                }
                
                logger.info("No download status found yet (attempt {}), retrying in 1 second...", i + 1);
                Thread.sleep(1000);
            }
            
            if (foundDownload) {
                logger.info("Found download status for context");
                printContextStatusData(contextInfo.getContextStatusData());
            } else {
                logger.warn("Warning: Could not find download status after all retries");
            }
            
            // 10. Verify the test file exists in the second session
            logger.info("Verifying test file exists in second session...");
            
            // Check file exists using command
            String checkFileCmd = "test -f " + testFilePath + " && echo 'File exists'";
            CommandResult existsResult = session2.getCommand().executeCommand(checkFileCmd, 5000);
            assertTrue("Error checking if file exists", existsResult.isSuccess());
            assertTrue("Test file should exist in second session", 
                      existsResult.getOutput().contains("File exists"));
            logger.info("Test file persistence verified successfully");
            
            // Read file content to verify it matches
            try {
                String readContent = session2.getFileSystem().read(testFilePath);
                assertEquals("File content should match", testContent, readContent);
                logger.info("File content verified successfully");
            } catch (AgentBayException e) {
                logger.error("Error reading file: {}", e.getMessage());
                fail("Should be able to read the file");
            }
            
            logger.info("✅ Test passed: Context sync persistence works correctly");
            
        } finally {
            // Clean up sessions
            if (session1 != null) {
                try {
                    agentBay.delete(session1, false);
                    logger.info("First session deleted: {}", session1.getSessionId());
                } catch (Exception e) {
                    logger.warn("Warning: Failed to delete first session: {}", e.getMessage());
                }
            }
            
            if (session2 != null) {
                try {
                    agentBay.delete(session2, false);
                    logger.info("Second session deleted: {}", session2.getSessionId());
                } catch (Exception e) {
                    logger.warn("Warning: Failed to delete second session: {}", e.getMessage());
                }
            }
            
            // Clean up context
            try {
                agentBay.getContext().delete(context);
                logger.info("Context deleted: {}", context.getId());
            } catch (Exception e) {
                logger.warn("Warning: Failed to delete context: {}", e.getMessage());
            }
        }
    }
    
    /**
     * Test RecyclePolicy with custom lifecycle
     */
    @Test
    public void testRecyclePolicyWithLifecycle1Day() {
        logger.info("Test: RecyclePolicy with Lifecycle_1Day");
        
        // Create a custom recycle policy with Lifecycle_1Day
        RecyclePolicy customRecyclePolicy = new RecyclePolicy(
            Lifecycle.LIFECYCLE_1DAY,
            Arrays.asList("/custom/path")
        );
        
        // Create a sync policy with the custom recycle policy
        SyncPolicy syncPolicy = new SyncPolicy(
            UploadPolicy.defaultPolicy(),
            DownloadPolicy.defaultPolicy(),
            DeletePolicy.defaultPolicy(),
            ExtractPolicy.defaultPolicy(),
            customRecyclePolicy,
            new BWList(Arrays.asList(new WhiteList("", Arrays.asList())))
        );
        
        // Verify the recycle policy
        assertNotNull("Recycle policy should not be null", syncPolicy.getRecyclePolicy());
        assertEquals("Lifecycle should be LIFECYCLE_1DAY", 
                    Lifecycle.LIFECYCLE_1DAY, 
                    syncPolicy.getRecyclePolicy().getLifecycle());
        assertNotNull("Paths should not be null", syncPolicy.getRecyclePolicy().getPaths());
        assertEquals("Should have one path", 1, syncPolicy.getRecyclePolicy().getPaths().size());
        assertEquals("Path should match", "/custom/path", syncPolicy.getRecyclePolicy().getPaths().get(0));
        
        // Create ContextSync with the custom policy
        ContextSync contextSync = ContextSync.create(
            "test-recycle-context",
            "/test/recycle/path",
            syncPolicy
        );
        
        // Verify ContextSync properties
        assertEquals("Context ID should match", "test-recycle-context", contextSync.getContextId());
        assertEquals("Path should match", "/test/recycle/path", contextSync.getPath());
        assertEquals("Policy should match", syncPolicy, contextSync.getPolicy());
        
        logger.info("✅ Test passed: RecyclePolicy with Lifecycle_1Day works correctly");
    }
    
    /**
     * Helper method to print context status data
     */
    private void printContextStatusData(java.util.List<ContextStatusData> data) {
        if (data == null || data.isEmpty()) {
            logger.info("No context status data available");
            return;
        }
        
        for (int i = 0; i < data.size(); i++) {
            ContextStatusData item = data.get(i);
            logger.info("Context Status Data [{}]:", i);
            logger.info("  ContextId: {}", item.getContextId());
            logger.info("  Path: {}", item.getPath());
            logger.info("  Status: {}", item.getStatus());
            logger.info("  TaskType: {}", item.getTaskType());
            logger.info("  StartTime: {}", item.getStartTime());
            logger.info("  FinishTime: {}", item.getFinishTime());
            if (item.getErrorMessage() != null && !item.getErrorMessage().isEmpty()) {
                logger.info("  ErrorMessage: {}", item.getErrorMessage());
            }
        }
    }
}

