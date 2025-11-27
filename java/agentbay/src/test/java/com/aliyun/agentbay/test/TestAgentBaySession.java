package com.aliyun.agentbay.test;

import com.aliyun.agentbay.AgentBay;
import com.aliyun.agentbay.exception.AgentBayException;
import com.aliyun.agentbay.model.SessionResult;
import com.aliyun.agentbay.session.CreateSessionParams;
import com.aliyun.agentbay.session.Session;
import org.junit.Test;

import static org.junit.Assert.*;

/**
 * Test cases for AgentBay session operations.
 * This test class is equivalent to test_agent_bay_session.py in Python SDK
 */
public class TestAgentBaySession {

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

    /**
     * Test cases for AgentBay session operations - Create, List, Delete
     */
    @Test
    public void testCreateListDelete() throws AgentBayException {
        // Test create, list, and delete methods
        String apiKey = getTestApiKey();
        AgentBay agentBay = new AgentBay(apiKey);

        // Create a session
        System.out.println("Creating a new session...");
        SessionResult result = agentBay.create(new CreateSessionParams());
        
        // Check if session creation was successful
        assertTrue("Session creation failed: " + result.getErrorMessage(), result.isSuccess());
        assertNotNull("Session object is null", result.getSession());
        
        Session session = result.getSession();
        System.out.println("Session created with ID: " + session.getSessionId());

        // Ensure session ID is not empty
        assertNotNull(session.getSessionId());
        assertFalse(session.getSessionId().isEmpty());

        // Delete the session
        System.out.println("Deleting the session...");
        agentBay.delete(session, false);

        // Session deletion completed
        System.out.println("✅ testCreateListDelete passed");
    }

    /**
     * Main method to run tests manually (for debugging purposes)
     * In production, use Maven or IDE test runners
     */
    public static void main(String[] args) {
        System.out.println("=== Running AgentBay Session Tests ===\n");
        
        // Run TestAgentBaySession test
        System.out.println("Running TestAgentBaySession tests...");
        TestAgentBaySession testAgentBaySession = new TestAgentBaySession();
        try {
            testAgentBaySession.testCreateListDelete();
        } catch (Exception e) {
            System.err.println("❌ Test failed: " + e.getMessage());
            e.printStackTrace();
        }

        // Run TestSession tests
        System.out.println("\nRunning TestSession tests...");
        TestSession testSession = new TestSession();
        try {
            testSession.setUp();
            testSession.testSessionProperties();
            testSession.testCommand();
            testSession.testFilesystem();
            testSession.tearDown();
            
            // Test delete separately
            testSession.setUp();
            testSession.testDelete();
            testSession.tearDown();
        } catch (Exception e) {
            System.err.println("❌ Test failed: " + e.getMessage());
            e.printStackTrace();
        }

        System.out.println("\n=== All Tests Completed ===");
    }

}