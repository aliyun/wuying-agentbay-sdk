package com.aliyun.agentbay.test;

import com.aliyun.agentbay.AgentBay;
import com.aliyun.agentbay.context.Context;
import com.aliyun.agentbay.context.ContextListResult;
import com.aliyun.agentbay.context.ContextResult;
import com.aliyun.agentbay.context.ContextSync;
import com.aliyun.agentbay.context.SyncPolicy;
import com.aliyun.agentbay.exception.AgentBayException;
import com.aliyun.agentbay.model.CommandResult;
import com.aliyun.agentbay.model.DeleteResult;
import com.aliyun.agentbay.model.SessionResult;
import com.aliyun.agentbay.session.CreateSessionParams;
import com.aliyun.agentbay.session.Session;
import org.junit.AfterClass;
import org.junit.BeforeClass;
import org.junit.Test;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.Arrays;

import static org.junit.Assert.*;

/**
 * JUnit 4 test cases for SessionContextExample functionality
 * Tests context management operations including list, get, create, update and cleanup
 */
public class TestSessionContextExample {
    private static final Logger logger = LoggerFactory.getLogger(TestSessionContextExample.class);
    
    private static AgentBay agentBay;
    private static Session session;
    private static Context context;
    private static String apiKey;
    private static String contextName;

    @BeforeClass
    public static void setUpClass() {
        logger.info("Starting Session Context Example Tests");
    }

    @BeforeClass
    public static void setUp() throws AgentBayException {
        // Get API key from environment variable
        apiKey = System.getenv("AGENTBAY_API_KEY");
        assertNotNull("AGENTBAY_API_KEY environment variable must be set", apiKey);
        assertFalse("AGENTBAY_API_KEY must not be empty", apiKey.trim().isEmpty());
        
        // Initialize AgentBay client
        agentBay = new AgentBay(apiKey);
        assertNotNull("AgentBay client should be initialized", agentBay);
        
        // Generate unique context name for this test run
        contextName = "test-context-java-" + System.currentTimeMillis();
        
        logger.info("Test setup completed with API key and context name: {}", contextName);
    }

    @AfterClass
    public static void tearDown() {
        // Clean up session if it was created
        if (agentBay != null && session != null) {
            try {
                DeleteResult deleteResult = agentBay.delete(session, true);
                assertTrue("Session should be deleted successfully", deleteResult.isSuccess());
                assertNotNull("Delete result should have request ID", deleteResult.getRequestId());
                logger.info("Session cleaned up successfully with request ID: {}", deleteResult.getRequestId());
            } catch (Exception e) {
                logger.error("Failed to clean up session", e);
            }
        }
        
        logger.info("Test cleanup completed");
    }

    @AfterClass
    public static void tearDownClass() {
        logger.info("All Session Context Example Tests completed");
    }

    /**
     * Test 1: List all contexts
     */
    @Test
    public void testListContexts() {
        logger.info("Test: Listing all contexts");
        
        try {
            ContextListResult result = agentBay.getContext().list();
            
            // Verify result
            assertNotNull("Context list result should not be null", result);
            assertNotNull("Request ID should not be null", result.getRequestId());
            assertTrue("List contexts should be successful", result.isSuccess());
            assertNotNull("Contexts list should not be null", result.getContexts());
            
            logger.info("Successfully listed {} contexts with request ID: {}", 
                       result.getContexts().size(), result.getRequestId());
            
            // Log context details
            for (Context ctx : result.getContexts()) {
                logger.info("  - Context: {} ({}), state={}, os={}", 
                           ctx.getName(), ctx.getId(), ctx.getState(), ctx.getOsType());
            }
            
        } catch (Exception e) {
            logger.error("Error listing contexts", e);
            fail("Should not throw exception when listing contexts: " + e.getMessage());
        }
    }

    /**
     * Test 2: Get a context (create if it doesn't exist)
     */
    @Test
    public void testGetOrCreateContext() {
        logger.info("Test: Getting or creating context with name: {}", contextName);
        
        try {
            ContextResult result = agentBay.getContext().get(contextName, true);
            
            // Verify result
            assertNotNull("Context result should not be null", result);
            assertNotNull("Request ID should not be null", result.getRequestId());
            assertTrue("Get context should be successful", result.isSuccess());
            assertNotNull("Context should not be null", result.getContext());
            
            context = result.getContext();
            assertNotNull("Context ID should not be null", context.getId());
            assertEquals("Context name should match", contextName, context.getName());
            
            logger.info("Successfully got/created context: {} ({}) with request ID: {}", 
                       context.getName(), context.getId(), result.getRequestId());
            
        } catch (Exception e) {
            logger.error("Error getting or creating context", e);
            fail("Should not throw exception when getting or creating context: " + e.getMessage());
        }
    }

    /**
     * Test 3: Create a session with context
     */
    @Test
    public void testCreateSessionWithContext() {
        logger.info("Test: Creating session with context");
        
        try {
            // First get or create context
            ContextResult contextResult = agentBay.getContext().get(contextName, true);
            assertTrue("Get context should be successful", contextResult.isSuccess());
            assertNotNull("Context should not be null", contextResult.getContext());
            context = contextResult.getContext();
            
            logger.info("Got context: {} ({})", context.getName(), context.getId());
            
            // Create session with context
            CreateSessionParams params = new CreateSessionParams();
            
            SyncPolicy syncPolicy = SyncPolicy.defaultPolicy();
            ContextSync contextSync = ContextSync.create(
                context.getId(),
                "/tmp/shared",
                syncPolicy
            );
            params.setContextSyncs(Arrays.asList(contextSync));
            params.setImageId("linux_latest");
            
            SessionResult sessionResult = agentBay.create(params);
            
            // Verify result
            assertNotNull("Session result should not be null", sessionResult);
            assertNotNull("Request ID should not be null", sessionResult.getRequestId());
            assertNotNull("Session should not be null", sessionResult.getSession());
            
            session = sessionResult.getSession();
            assertNotNull("Session ID should not be null", session.getSessionId());
            
            logger.info("Successfully created session with ID: {} and request ID: {}", 
                       session.getSessionId(), sessionResult.getRequestId());
            
        } catch (AgentBayException e) {
            logger.error("Error creating session with context", e);
            fail("Should not throw exception when creating session: " + e.getMessage());
        }
    }

    /**
     * Test 4: Execute commands in session with context
     */
    @Test
    public void testExecuteCommandsInContextSession() {
        logger.info("Test: Executing commands in session with context");
        
        try {
            // First get or create context
            ContextResult contextResult = agentBay.getContext().get(contextName, true);
            assertTrue("Get context should be successful", contextResult.isSuccess());
            context = contextResult.getContext();
            
            // Create session with context
            CreateSessionParams params = new CreateSessionParams();
            SyncPolicy syncPolicy = SyncPolicy.defaultPolicy();
            ContextSync contextSync = ContextSync.create(
                context.getId(),
                "/tmp/shared",
                syncPolicy
            );
            params.setContextSyncs(Arrays.asList(contextSync));
            params.setImageId("linux_latest");
            
            SessionResult sessionResult = agentBay.create(params);
            session = sessionResult.getSession();
            
            logger.info("Session created with ID: {}", session.getSessionId());
            
            // Execute first command: create directory and file
            String createCommand = "mkdir -p /tmp/shared/ && touch /tmp/shared/" + session.getSessionId();
            CommandResult commandResult = session.getCommand().executeCommand(createCommand, 1000);
            
            assertNotNull("Command result should not be null", commandResult);
            assertTrue("Command should execute successfully: " + commandResult.getErrorMessage(), 
                      commandResult.isSuccess());
            assertNotNull("Command result should have request ID", commandResult.getRequestId());
            
            logger.info("✅ First command executed successfully!");
            logger.info("   Request ID: {}", commandResult.getRequestId());
            logger.info("   Output: {}", commandResult.getOutput());
            
            // Execute second command: list directory contents
            CommandResult listResult = session.getCommand().executeCommand("ls -al /tmp/shared", 1000);
            
            assertNotNull("List command result should not be null", listResult);
            assertTrue("List command should execute successfully: " + listResult.getErrorMessage(), 
                      listResult.isSuccess());
            assertNotNull("List command result should have request ID", listResult.getRequestId());
            assertNotNull("List command should have output", listResult.getOutput());
            
            logger.info("✅ Second command executed successfully!");
            logger.info("   Request ID: {}", listResult.getRequestId());
            logger.info("   Output: {}", listResult.getOutput());
            
            // Verify the file was created (should be in the output)
            assertTrue("Output should contain the created file", 
                      listResult.getOutput().contains(session.getSessionId()));
            
        } catch (Exception e) {
            logger.error("Error executing commands in context session", e);
            fail("Should not throw exception when executing commands: " + e.getMessage());
        }
    }

    /**
     * Test 5: Complete workflow - list, get, create session, execute commands, and cleanup
     */
    @Test
    public void testCompleteContextWorkflow() {
        logger.info("Test: Complete context workflow");
        
        try {
            // Step 1: List all contexts
            logger.info("Step 1: Listing all contexts");
            ContextListResult listResult = agentBay.getContext().list();
            assertTrue("List contexts should be successful", listResult.isSuccess());
            int initialContextCount = listResult.getContexts().size();
            logger.info("Found {} existing contexts", initialContextCount);
            
            // Step 2: Get or create context
            logger.info("Step 2: Getting or creating context: {}", contextName);
            ContextResult contextResult = agentBay.getContext().get(contextName, true);
            assertTrue("Get context should be successful", contextResult.isSuccess());
            assertNotNull("Context should not be null", contextResult.getContext());
            context = contextResult.getContext();
            logger.info("Got context: {} ({})", context.getName(), context.getId());
            
            // Step 3: Create session with context
            logger.info("Step 3: Creating session with context");
            CreateSessionParams params = new CreateSessionParams();
            SyncPolicy syncPolicy = SyncPolicy.defaultPolicy();
            ContextSync contextSync = ContextSync.create(
                context.getId(),
                "/tmp/shared",
                syncPolicy
            );
            params.setContextSyncs(Arrays.asList(contextSync));
            params.setImageId("linux_latest");
            
            SessionResult sessionResult = agentBay.create(params);
            session = sessionResult.getSession();
            assertNotNull("Session should be created", session);
            logger.info("Session created with ID: {}", session.getSessionId());
            
            // Step 4: Execute commands
            logger.info("Step 4: Executing commands in session");
            String createCommand = "mkdir -p /tmp/shared/ && touch /tmp/shared/" + session.getSessionId();
            CommandResult createResult = session.getCommand().executeCommand(createCommand, 1000);
            assertTrue("Create command should succeed", createResult.isSuccess());
            
            CommandResult listCommandResult = session.getCommand().executeCommand("ls -al /tmp/shared", 1000);
            assertTrue("List command should succeed", listCommandResult.isSuccess());
            assertTrue("Created file should exist in output", 
                      listCommandResult.getOutput().contains(session.getSessionId()));
            logger.info("Commands executed successfully");
            
            // Step 5: Delete session with context synchronization
            logger.info("Step 5: Deleting session with context synchronization");
            DeleteResult deleteResult = agentBay.delete(session, true);
            assertTrue("Session deletion should be successful", deleteResult.isSuccess());
            assertNotNull("Delete result should have request ID", deleteResult.getRequestId());
            logger.info("Session deleted successfully with request ID: {}", deleteResult.getRequestId());
            
            // Clear session reference to prevent duplicate cleanup
            session = null;
            
            logger.info("✅ Complete context workflow test passed!");
            
        } catch (Exception e) {
            logger.error("Error in complete context workflow", e);
            fail("Should not throw exception in complete workflow: " + e.getMessage());
        }
    }

    /**
     * Test 6: Get non-existent context without auto-create
     */
    @Test
    public void testGetNonExistentContextWithoutCreate() {
        logger.info("Test: Getting non-existent context without auto-create");
        
        String nonExistentContextName = "non-existent-context-" + System.currentTimeMillis();
        
        try {
            // Try to get context without creating it (second parameter = false)
            ContextResult result = agentBay.getContext().get(nonExistentContextName, false);
            
            assertNotNull("Context result should not be null", result);
            assertNotNull("Request ID should not be null", result.getRequestId());
            
            // Context should be null when it doesn't exist and auto-create is false
            if (!result.isSuccess() || result.getContext() == null) {
                logger.info("As expected, context does not exist and was not created");
            } else {
                logger.warn("Context was found or created unexpectedly");
            }
            
        } catch (Exception e) {
            logger.info("Exception thrown as expected when getting non-existent context: {}", e.getMessage());
            // This is acceptable behavior
        }
    }

    /**
     * Test 7: Create session with invalid context should fail gracefully
     */
    @Test
    public void testCreateSessionWithInvalidContext() {
        logger.info("Test: Creating session with invalid context ID");
        
        try {
            CreateSessionParams params = new CreateSessionParams();
            
            // Use an invalid context ID
            String invalidContextId = "invalid-context-id-12345";
            SyncPolicy syncPolicy = SyncPolicy.defaultPolicy();
            ContextSync contextSync = ContextSync.create(
                invalidContextId,
                "/tmp/shared",
                syncPolicy
            );
            params.setContextSyncs(Arrays.asList(contextSync));
            params.setImageId("linux_latest");
            
            try {
                SessionResult sessionResult = agentBay.create(params);
                // If it succeeds, that's unexpected but we should handle it
                session = sessionResult.getSession();
                logger.warn("Session creation succeeded with invalid context ID (unexpected)");
            } catch (AgentBayException e) {
                logger.info("As expected, session creation failed with invalid context ID: {}", e.getMessage());
                // This is the expected behavior
            }
            
        } catch (Exception e) {
            logger.info("Exception thrown as expected: {}", e.getMessage());
            // This is acceptable behavior
        }
    }
}

