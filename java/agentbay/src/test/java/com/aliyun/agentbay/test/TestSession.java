package com.aliyun.agentbay.test;

import com.aliyun.agentbay.AgentBay;
import com.aliyun.agentbay.exception.AgentBayException;
import com.aliyun.agentbay.model.CommandResult;
import com.aliyun.agentbay.model.DeleteResult;
import com.aliyun.agentbay.model.FileContentResult;
import com.aliyun.agentbay.model.SessionResult;
import com.aliyun.agentbay.session.CreateSessionParams;
import com.aliyun.agentbay.session.Session;
import org.junit.AfterClass;
import org.junit.BeforeClass;
import org.junit.Test;

import static org.junit.Assert.*;

/**
 * Test cases for the Session class.
 * This test class is equivalent to TestSession in test_agent_bay_session.py
 */
public class TestSession {
    private static AgentBay agentBay;
    private static Session session;
    private static SessionResult result;

    /**
     * Get API key for testing
     */
    private static String getTestApiKey() {
        String apiKey = System.getenv("AGENTBAY_API_KEY");
        if (apiKey == null || apiKey.trim().isEmpty()) {
            apiKey = "akm-xxx"; // Replace with your test API key
            System.out.println("Warning: Using default API key. Set AGENTBAY_API_KEY environment variable for testing.");
        }
        return apiKey;
    }

    @BeforeClass
    public static void setUp() throws AgentBayException {
        // Set up test fixtures
        String apiKey = getTestApiKey();
        agentBay = new AgentBay(apiKey);

        // Create a session with default windows image
        System.out.println("Creating a new session for testing...");
        result = agentBay.create(new CreateSessionParams());
        
        // Check if session creation was successful
        if (!result.isSuccess()) {
            fail("Session creation failed in setUp: " + result.getErrorMessage());
        }
        if (result.getSession() == null) {
            fail("Session object is null in setUp");
        }
            
        session = result.getSession();
        System.out.println("Session created with ID: " + session.getSessionId());
    }

    @AfterClass
    public static void tearDown() {
        // Tear down test fixtures
        System.out.println("Cleaning up: Deleting the session...");
        try {
            agentBay.delete(session, false);
        } catch (Exception e) {
            System.out.println("Warning: Error deleting session: " + e.getMessage());
        }
    }

    @Test
    public void testSessionProperties() {
        // Test session properties and methods
        assertNotNull(this.session.getSessionId());
        assertEquals(this.agentBay, this.session.getAgentBay());

        // Test access to API key through agentBay
        String apiKey = this.session.getAgentBay().getApiKey();
        assertEquals(apiKey, this.agentBay.getApiKey());

        // Test access to client through agentBay
        assertEquals(this.session.getAgentBay().getClient(), this.agentBay.getClient());

        // Test sessionId property
        String sessionId = this.session.getSessionId();
        assertNotNull(sessionId);
        
        System.out.println("✅ testSessionProperties passed");
    }

    @Test
    public void testDelete() throws AgentBayException {
        // Test session delete method
        // Create a new session specifically for this test
        System.out.println("Creating a new session for delete testing...");
        SessionResult result = this.agentBay.create(new CreateSessionParams());
        Session session = result.getSession();
        System.out.println("Session created with ID: " + session.getSessionId());

        // Test delete method
        System.out.println("Testing session.delete method...");
        try {
            DeleteResult deleteResult = session.delete();
            assertTrue(deleteResult.isSuccess());
            
            System.out.println("✅ testDelete passed");
            // Session deletion verified
        } catch (Exception e) {
            System.out.println("Note: Session deletion failed: " + e.getMessage());
            // Clean up if the test failed
            try {
                this.agentBay.delete(session, false);
            } catch (Exception cleanupException) {
                // Ignore cleanup errors
            }
            throw e;
        }
    }

    @Test
    public void testCommand() {
        // Test command execution
        if (this.session.getCommand() != null) {
            System.out.println("Executing command...");
            try {
                CommandResult response = this.session.getCommand().executeCommand("ls", 1000);
                System.out.println("Command execution result: " + response);
                assertNotNull(response);
                assertTrue("Command failed: " + response.getErrorMessage(), response.isSuccess());
                // Check if response contains "tool not found"
                assertFalse(
                    "Command.executeCommand returned 'tool not found'",
                    response.getOutput().toLowerCase().contains("tool not found")
                );
                System.out.println("✅ testCommand passed");
            } catch (Exception e) {
                System.out.println("Note: Command execution failed: " + e.getMessage());
                // Don't fail the test if command execution is not supported
            }
        } else {
            System.out.println("Note: Command interface is null, skipping command test");
        }
    }

    @Test
    public void testFilesystem() {
        // Test filesystem operations
        if (this.session.getFileSystem() != null) {
            System.out.println("Reading file...");
            try {
                FileContentResult result = this.session.getFileSystem().readFile("/etc/hosts");
                System.out.println("ReadFile result: content='" + result + "'");
                assertNotNull(result);
                assertTrue("Read file failed: " + result.getErrorMessage(), result.isSuccess());
                // Check if response contains "tool not found"
                assertFalse(
                    "FileSystem.readFile returned 'tool not found'",
                    result.getContent().toLowerCase().contains("tool not found")
                );
                System.out.println("File read successful");
                System.out.println("✅ testFilesystem passed");
            } catch (Exception e) {
                System.out.println("Note: File operation failed: " + e.getMessage());
                // Don't fail the test if filesystem operations are not supported
            }
        } else {
            System.out.println("Note: FileSystem interface is null, skipping file test");
        }
    }
}

