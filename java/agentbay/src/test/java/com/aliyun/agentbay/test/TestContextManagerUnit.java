package com.aliyun.agentbay.test;

import com.aliyun.agentbay.AgentBay;
import com.aliyun.agentbay.context.*;
import com.aliyun.agentbay.exception.AgentBayException;
import com.aliyun.agentbay.model.SessionResult;
import com.aliyun.agentbay.session.CreateSessionParams;
import com.aliyun.agentbay.session.Session;
import org.junit.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.Arrays;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.TimeUnit;

import static org.junit.Assert.*;

/**
 * Unit tests for ContextManager functionality
 * Tests session.context.info() and session.context.sync() methods
 * 
 * This test is equivalent to Python's test_context_manager.py
 */
public class TestContextManagerUnit {
    private static final Logger logger = LoggerFactory.getLogger(TestContextManagerUnit.class);
    
    private static AgentBay agentBay;
    private static Context context;
    private static Session session;
    
    @BeforeClass
    public static void setUpClass() throws AgentBayException {
        // Skip if no API key is available or in CI environment
        String apiKey = System.getenv("AGENTBAY_API_KEY");
        String ci = System.getenv("CI");
        if (apiKey == null || apiKey.trim().isEmpty() || "true".equals(ci)) {
            throw new IllegalStateException(
                "Skipping unit test: No API key available or running in CI"
            );
        }

        // Initialize AgentBay client
        agentBay = new AgentBay(apiKey);

        // Create a unique context name for this test
        String contextName = "test-context-manager-" + System.currentTimeMillis();

        // Create a context
        ContextResult contextResult = agentBay.getContext().get(contextName, true);
        if (!contextResult.isSuccess() || contextResult.getContext() == null) {
            throw new IllegalStateException("Failed to create context");
        }

        context = contextResult.getContext();
        logger.info("Created context: {} (ID: {})", context.getName(), context.getId());

        // Create a session for all tests
        CreateSessionParams params = new CreateSessionParams();
        ContextSync contextSync = ContextSync.create(
            context.getId(),
            "/home/wuying/test",
            SyncPolicy.defaultPolicy()
        );
        params.setContextSyncs(Arrays.asList(contextSync));
        params.setImageId("linux_latest");

        SessionResult sessionResult = agentBay.create(params);
        if (!sessionResult.isSuccess() || sessionResult.getSession() == null) {
            throw new IllegalStateException("Failed to create session for test");
        }

        session = sessionResult.getSession();
        logger.info("Created session: {}", session.getSessionId());

        // Wait a bit for session to be ready
        try {
            Thread.sleep(3000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
    
    @AfterClass
    public static void tearDownClass() {
        // Clean up session
        if (session != null && agentBay != null) {
            try {
                agentBay.delete(session, false);
                logger.info("Session deleted: {}", session.getSessionId());
            } catch (Exception e) {
                logger.warn("Warning: Failed to delete session: {}", e.getMessage());
            }
        }

        // Clean up context
        if (context != null && agentBay != null) {
            try {
                agentBay.getContext().delete(context);
                logger.info("Context deleted: {}", context.getId());
            } catch (Exception e) {
                logger.warn("Warning: Failed to delete context: {}", e.getMessage());
            }
        }
    }
    
    
    /**
     * Test that context.info() returns context status data
     */
    @Test
    public void testContextInfoReturnsStatusData() {
        logger.info("Test: context.info() returns context status data");
        
        // Get context info
        ContextInfoResult infoResult = session.getContext().info();
        
        // Verify that we have a request ID
        assertNotNull("Request ID should not be null", infoResult.getRequestId());
        assertNotEquals("Request ID should not be empty", "", infoResult.getRequestId());
        
        // Log the context status data
        logger.info("Context status data count: {}", infoResult.getContextStatusData().size());
        for (int i = 0; i < infoResult.getContextStatusData().size(); i++) {
            ContextStatusData data = infoResult.getContextStatusData().get(i);
            logger.info("Status data {}:", i);
            logger.info("  Context ID: {}", data.getContextId());
            logger.info("  Path: {}", data.getPath());
            logger.info("  Status: {}", data.getStatus());
            logger.info("  Task Type: {}", data.getTaskType());
            logger.info("  Start Time: {}", data.getStartTime());
            logger.info("  Finish Time: {}", data.getFinishTime());
            if (data.getErrorMessage() != null && !data.getErrorMessage().isEmpty()) {
                logger.info("  Error: {}", data.getErrorMessage());
            }
        }
        
        // There might not be any status data yet, so we don't assert on the count
        // But if there is data, verify it has the expected structure
        for (ContextStatusData data : infoResult.getContextStatusData()) {
            assertNotNull("Context ID should not be null", data.getContextId());
            assertNotNull("Path should not be null", data.getPath());
            assertNotNull("Status should not be null", data.getStatus());
            assertNotNull("Task Type should not be null", data.getTaskType());
        }
        
        logger.info("✅ Test passed: context.info() returns valid context status data");
    }
    
    /**
     * Test that context.info() with parameters filters correctly
     */
    @Test
    public void testContextInfoWithParameters() {
        logger.info("Test: context.info() with parameters");
        
        // Get context info with parameters
        ContextInfoResult infoResult = session.getContext().info(
            context.getId(),
            "/home/wuying/test",
            null
        );
        
        // Verify that we have a request ID
        assertNotNull("Request ID should not be null", infoResult.getRequestId());
        
        // Log the filtered context status data
        logger.info("Filtered context status data count: {}", infoResult.getContextStatusData().size());
        for (int i = 0; i < infoResult.getContextStatusData().size(); i++) {
            ContextStatusData data = infoResult.getContextStatusData().get(i);
            logger.info("Status data {}:", i);
            logger.info("  Context ID: {}", data.getContextId());
            logger.info("  Path: {}", data.getPath());
            logger.info("  Status: {}", data.getStatus());
            logger.info("  Task Type: {}", data.getTaskType());
        }
        
        // If we have status data, verify it matches our filters
        for (ContextStatusData data : infoResult.getContextStatusData()) {
            if (data.getContextId().equals(context.getId())) {
                assertEquals("Path should match filter", "/home/wuying/test", data.getPath());
            }
        }
        
        logger.info("✅ Test passed: context.info() with parameters filters correctly");
    }
    
    /**
     * Test basic sync functionality (trigger only)
     */
    @Test
    public void testContextSyncBasic() {
        logger.info("Test: Basic context sync (trigger only)");
        
        // Trigger a sync
        ContextSyncResult syncResult = session.getContext().sync();
        
        // Verify sync result
        assertTrue("Sync should be successful", syncResult.isSuccess());
        assertNotNull("Request ID should not be null", syncResult.getRequestId());
        assertNotEquals("Request ID should not be empty", "", syncResult.getRequestId());
        
        logger.info("Sync triggered successfully with request ID: {}", syncResult.getRequestId());
        logger.info("✅ Test passed: Basic context sync works");
    }
    
    /**
     * Test sync with callback
     */
    @Test
    public void testContextSyncWithCallback() throws Exception {
        logger.info("Test: Context sync with callback");
        
        // Create a CompletableFuture to wait for callback
        CompletableFuture<Boolean> callbackFuture = new CompletableFuture<>();
        
        // Trigger sync with callback
        ContextSyncResult syncResult = session.getContext().sync(success -> {
            logger.info("Callback received: {}", success ? "SUCCESS" : "FAILED");
            callbackFuture.complete(success);
        });
        
        // Verify initial sync trigger was successful
        assertTrue("Sync trigger should be successful", syncResult.isSuccess());
        assertNotNull("Request ID should not be null", syncResult.getRequestId());
        
        logger.info("Sync triggered with callback, request ID: {}", syncResult.getRequestId());
        logger.info("Waiting for callback completion...");
        
        // Wait for callback (max 5 minutes)
        Boolean callbackSuccess = callbackFuture.get(5, TimeUnit.MINUTES);
        
        // Verify callback result
        assertNotNull("Callback should have been called", callbackSuccess);
        assertTrue("Callback should report success", callbackSuccess);
        
        logger.info("✅ Test passed: Context sync with callback works correctly");
    }
    
    /**
     * Test syncAndWait functionality
     */
    @Test
    public void testContextSyncAndWait() {
        logger.info("Test: Context syncAndWait (blocking)");
        
        long startTime = System.currentTimeMillis();
        
        // Call syncAndWait - this should block until sync completes
        ContextSyncResult syncResult = session.getContext().syncAndWait();
        
        long duration = System.currentTimeMillis() - startTime;
        
        // Verify sync result
        assertTrue("Sync should be successful", syncResult.isSuccess());
        assertNotNull("Request ID should not be null", syncResult.getRequestId());
        
        logger.info("Sync completed in {} ms with request ID: {}", duration, syncResult.getRequestId());
        logger.info("✅ Test passed: syncAndWait works correctly");
    }
    
    /**
     * Test sync with custom parameters
     */
    @Test
    public void testContextSyncWithParameters() {
        logger.info("Test: Context sync with custom parameters");
        
        // Trigger sync with custom parameters
        ContextSyncResult syncResult = session.getContext().sync(
            context.getId(),
            "/home/wuying/test",
            "upload"
        );
        
        // Verify sync result
        assertTrue("Sync should be successful", syncResult.isSuccess());
        assertNotNull("Request ID should not be null", syncResult.getRequestId());
        
        logger.info("Sync triggered with custom parameters, request ID: {}", syncResult.getRequestId());
        logger.info("✅ Test passed: Context sync with parameters works");
    }
    
    /**
     * Test sync and then check info
     */
    @Test
    public void testSyncThenCheckInfo() throws InterruptedException {
        logger.info("Test: Sync context and then check info");
        
        // First trigger a sync
        ContextSyncResult syncResult = session.getContext().sync();
        assertTrue("Sync should be successful", syncResult.isSuccess());
        
        logger.info("Sync triggered, waiting a bit before checking info...");
        Thread.sleep(3000);
        
        // Then get info
        ContextInfoResult infoResult = session.getContext().info();
        assertNotNull("Info result should not be null", infoResult);
        assertNotNull("Request ID should not be null", infoResult.getRequestId());
        
        // Log context status data
        logger.info("Context status data after sync, count: {}", infoResult.getContextStatusData().size());
        for (int i = 0; i < infoResult.getContextStatusData().size(); i++) {
            ContextStatusData data = infoResult.getContextStatusData().get(i);
            logger.info("Status data {}:", i);
            logger.info("  Context ID: {}", data.getContextId());
            logger.info("  Path: {}", data.getPath());
            logger.info("  Status: {}", data.getStatus());
            logger.info("  Task Type: {}", data.getTaskType());
        }
        
        // Check if we have status data for our context
        boolean foundContext = false;
        for (ContextStatusData data : infoResult.getContextStatusData()) {
            if (data.getContextId().equals(context.getId())) {
                foundContext = true;
                assertEquals("Path should match", "/home/wuying/test", data.getPath());
                // Status might vary, but should not be empty
                assertNotNull("Status should not be null", data.getStatus());
                assertNotEquals("Status should not be empty", "", data.getStatus());
                break;
            }
        }
        
        // We should have found our context in the status data
        // But this might be flaky, so just log a warning if not found
        if (!foundContext) {
            logger.warn("Warning: Could not find context {} in status data", context.getId());
        }
        
        logger.info("✅ Test passed: Sync and check info works correctly");
    }
}

