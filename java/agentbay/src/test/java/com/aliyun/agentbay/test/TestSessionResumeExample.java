package com.aliyun.agentbay.test;

import com.aliyun.agentbay.AgentBay;
import com.aliyun.agentbay.exception.AgentBayException;
import com.aliyun.agentbay.model.CommandResult;
import com.aliyun.agentbay.model.DeleteResult;
import com.aliyun.agentbay.model.SessionResult;
import com.aliyun.agentbay.session.CreateSessionParams;
import com.aliyun.agentbay.session.Session;
import org.junit.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import static org.junit.Assert.*;

/**
 * JUnit 4 test cases for SessionResumeExample functionality
 * Tests session state dump and restore operations
 */
public class TestSessionResumeExample {
    private static final Logger logger = LoggerFactory.getLogger(TestSessionResumeExample.class);
    
    private AgentBay agentBay;
    private Session session;
    private String apiKey;

    @BeforeClass
    public static void setUpClass() {
        logger.info("Starting Session Resume Example Tests");
    }

    @Before
    public void setUp() throws AgentBayException {
        // Get API key from environment variable
        apiKey = System.getenv("AGENTBAY_API_KEY");
        assertNotNull("AGENTBAY_API_KEY environment variable must be set", apiKey);
        assertFalse("AGENTBAY_API_KEY must not be empty", apiKey.trim().isEmpty());
        
        // Initialize AgentBay client
        logger.info("Creating AgentBay client...");
        agentBay = new AgentBay(apiKey);
        assertNotNull("AgentBay client should be initialized", agentBay);
        
        // Create session
        logger.info("Creating session...");
        CreateSessionParams params = new CreateSessionParams();
        params.setImageId("imgc-0abxi0lc574y4cltl");
        params.setIsVpc(true);
        
        SessionResult sessionResult = agentBay.create(params);
        assertTrue("Session creation should succeed", sessionResult.isSuccess());
        assertNotNull("Session result should have a session", sessionResult.getSession());
        assertNotNull("Session result should have request ID", sessionResult.getRequestId());
        
        session = sessionResult.getSession();
        assertNotNull("Session should be initialized", session);
        assertNotNull("Session ID should not be null", session.getSessionId());
        
        logger.info("✅ Session created successfully!");
        logger.info("   Session ID: {}", session.getSessionId());
        logger.info("   Request ID: {}", sessionResult.getRequestId());
    }

    @After
    public void tearDown() {
        if (session != null && agentBay != null) {
            try {
                logger.info("Cleaning up session: {}", session.getSessionId());
                DeleteResult deleteResult = agentBay.delete(session, false);
                if (deleteResult.isSuccess()) {
                    logger.info("✅ Session deleted successfully");
                } else {
                    logger.error("❌ Failed to delete session: {}", deleteResult.getErrorMessage());
                }
            } catch (Exception e) {
                logger.error("❌ Error deleting session: {}", e.getMessage());
            }
        }
    }

    @AfterClass
    public static void tearDownClass() {
        logger.info("Session Resume Example Tests completed");
    }

    /**
     * Test basic command execution on session
     */
    @Test
    public void testCommandExecution() {
        logger.info("\n=== Testing Command Execution ===");
        
        // Execute write command
        CommandResult commandResult = session.getCommand().executeCommand("echo 'Hello, World!' > /tmp/test", 1000);
        assertTrue("Command execution should succeed", commandResult.isSuccess());
        assertNotNull("Command result should have output", commandResult.getOutput());
        
        logger.info("✅ Command executed successfully!");
        logger.info("   Command output: {}", commandResult.getOutput());
        
        // Verify the file was created
        CommandResult verifyResult = session.getCommand().executeCommand("cat /tmp/test", 1000);
        assertTrue("Verify command should succeed", verifyResult.isSuccess());
        assertTrue("Output should contain expected text", verifyResult.getOutput().contains("Hello, World!"));
        
        logger.info("✅ Command verification successful!");
        logger.info("   Verification output: {}", verifyResult.getOutput());
    }

    /**
     * Test session state dump functionality
     */
    @Test
    public void testSessionStateDump() throws AgentBayException {
        logger.info("\n=== Testing Session State Dump ===");
        
        // Dump session state
        String stateJson = session.dumpState();
        assertNotNull("State JSON should not be null", stateJson);
        assertFalse("State JSON should not be empty", stateJson.trim().isEmpty());
        assertTrue("State JSON should be valid JSON (contains braces)", stateJson.contains("{") && stateJson.contains("}"));
        
        logger.info("✅ Session state dumped!");
        logger.info("   State JSON length: {} characters", stateJson.length());
        logger.info("   State preview: {}", stateJson.length() > 100 ? stateJson.substring(0, 100) + "..." : stateJson);
    }

    /**
     * Test session state restore functionality
     */
    @Test
    public void testSessionStateRestore() throws AgentBayException {
        logger.info("\n=== Testing Session State Dump/Restore ===");
        
        // First, create a test file
        CommandResult setupResult = session.getCommand().executeCommand("echo 'Hello, World!' > /tmp/test", 1000);
        assertTrue("Setup command should succeed", setupResult.isSuccess());
        logger.info("✅ Test file created!");
        
        // Dump session state
        String stateJson = session.dumpState();
        assertNotNull("State JSON should not be null", stateJson);
        assertFalse("State JSON should not be empty", stateJson.trim().isEmpty());
        
        logger.info("✅ Session state dumped!");
        logger.info("   State JSON length: {} characters", stateJson.length());
        logger.info("   State preview: {}", stateJson.length() > 100 ? stateJson.substring(0, 100) + "..." : stateJson);
        
        // Restore session state
        Session restoredSession = Session.restoreState(agentBay, stateJson);
        assertNotNull("Restored session should not be null", restoredSession);
        assertNotNull("Restored session ID should not be null", restoredSession.getSessionId());
        assertEquals("Restored session ID should match original", session.getSessionId(), restoredSession.getSessionId());
        
        logger.info("✅ Session state restored!");
        logger.info("   Restored session ID: {}", restoredSession.getSessionId());
        logger.info("   VPC enabled: {}", restoredSession.isVpcEnabled());
        
        // Verify VPC settings if enabled
        if (restoredSession.isVpcEnabled()) {
            assertNotNull("HTTP port should not be null when VPC is enabled", restoredSession.getHttpPort());
            logger.info("   HTTP Port: {}", restoredSession.getHttpPort());
            logger.info("   VPC Link URL: {}", restoredSession.getVpcLinkUrl() != null ? "cached" : "not cached");
        }
        
        // Execute command on restored session to verify it works
        CommandResult restoreCommandResult = restoredSession.getCommand().executeCommand("cat /tmp/test", 1000);
        assertTrue("Command on restored session should succeed", restoreCommandResult.isSuccess());
        assertNotNull("Restored command result should have output", restoreCommandResult.getOutput());
        assertTrue("Output should contain expected text", restoreCommandResult.getOutput().contains("Hello, World!"));
        
        logger.info("✅ Command executed on restored session!");
        logger.info("   Output: {}", restoreCommandResult.getOutput());
    }

    /**
     * Test multiple session state dump/restore cycles
     */
    @Test
    public void testMultipleSessionRestoreCycles() throws AgentBayException, InterruptedException {
        logger.info("\n=== Testing Multiple Session Restore Cycles ===");
        
        // Create initial test file
        CommandResult setupResult = session.getCommand().executeCommand("echo 'Hello, World!' > /tmp/test", 1000);
        assertTrue("Setup command should succeed", setupResult.isSuccess());
        
        String stateJson = session.dumpState();
        assertNotNull("Initial state JSON should not be null", stateJson);
        
        // Test 3 cycles instead of 1000 for practical testing
        int cycles = 3;
        for (int i = 0; i < cycles; i++) {
            logger.info("--- Restore cycle {} ---", i + 1);
            
            // Restore session
            Session restoredSession = Session.restoreState(agentBay, stateJson);
            assertNotNull("Restored session should not be null", restoredSession);
            assertEquals("Session ID should remain consistent", session.getSessionId(), restoredSession.getSessionId());
            
            logger.info("✅ Session state restored!");
            logger.info("   Restored session ID: {}", restoredSession.getSessionId());
            logger.info("   VPC enabled: {}", restoredSession.isVpcEnabled());
            
            if (restoredSession.isVpcEnabled()) {
                assertNotNull("HTTP port should not be null", restoredSession.getHttpPort());
                logger.info("   HTTP Port: {}", restoredSession.getHttpPort());
                logger.info("   VPC Link URL: {}", restoredSession.getVpcLinkUrl() != null ? "cached" : "not cached");
            }
            
            // Execute command on restored session
            CommandResult restoreCommandResult = restoredSession.getCommand().executeCommand("cat /tmp/test", 1000);
            assertTrue("Command should succeed on cycle " + (i + 1), restoreCommandResult.isSuccess());
            assertTrue("Output should contain expected text", restoreCommandResult.getOutput().contains("Hello, World!"));
            
            logger.info("✅ Command executed on restored session!");
            logger.info("   Output: {}", restoreCommandResult.getOutput());
            
            // Dump state again for next cycle
            stateJson = session.dumpState();
            assertNotNull("State JSON should not be null in cycle " + (i + 1), stateJson);
            
            // Small delay between cycles
            Thread.sleep(1000);
        }
        
        logger.info("✅ All {} restore cycles completed successfully!", cycles);
    }

    /**
     * Test VPC settings on restored session
     */
    @Test
    public void testVpcSettingsOnRestoredSession() throws AgentBayException {
        logger.info("\n=== Testing VPC Settings on Restored Session ===");
        
        // Dump and restore
        String stateJson = session.dumpState();
        Session restoredSession = Session.restoreState(agentBay, stateJson);
        
        // Verify VPC settings
        assertTrue("Session should have VPC enabled", restoredSession.isVpcEnabled());
        assertNotNull("HTTP port should be available", restoredSession.getHttpPort());
        
        logger.info("✅ VPC settings verified on restored session");
        logger.info("   VPC enabled: {}", restoredSession.isVpcEnabled());
        logger.info("   HTTP Port: {}", restoredSession.getHttpPort());
        logger.info("   VPC Link URL: {}", restoredSession.getVpcLinkUrl() != null ? "cached" : "not cached");
    }

    /**
     * Test command execution failure handling
     */
    @Test
    public void testCommandExecutionFailureHandling() {
        logger.info("\n=== Testing Command Execution Failure Handling ===");
        
        // Execute a command that should fail
        CommandResult failResult = session.getCommand().executeCommand("nonexistentcommand12345", 1000);
        // Note: Depending on the implementation, this might succeed with error output or fail
        // We just verify we get a result
        assertNotNull("Command result should not be null", failResult);
        
        logger.info("Command result received: success={}, output={}", 
            failResult.isSuccess(), failResult.getOutput());
    }

    /**
     * Test session state consistency after restore
     */
    @Test
    public void testSessionStateConsistency() throws AgentBayException {
        logger.info("\n=== Testing Session State Consistency ===");
        
        String originalSessionId = session.getSessionId();
        boolean originalVpcEnabled = session.isVpcEnabled();
        String originalHttpPort = session.getHttpPort();
        
        // Dump and restore
        String stateJson = session.dumpState();
        Session restoredSession = Session.restoreState(agentBay, stateJson);
        
        // Verify all properties match
        assertEquals("Session ID should match", originalSessionId, restoredSession.getSessionId());
        assertEquals("VPC enabled status should match", originalVpcEnabled, restoredSession.isVpcEnabled());
        assertEquals("HTTP port should match", originalHttpPort, restoredSession.getHttpPort());
        
        logger.info("✅ Session state consistency verified!");
        logger.info("   Original Session ID: {}", originalSessionId);
        logger.info("   Restored Session ID: {}", restoredSession.getSessionId());
        logger.info("   States match: {}", originalSessionId.equals(restoredSession.getSessionId()));
    }
}

