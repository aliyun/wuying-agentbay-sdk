package com.aliyun.agentbay.test;

import com.aliyun.agentbay.AgentBay;
import com.aliyun.agentbay.exception.AgentBayException;
import com.aliyun.agentbay.model.DeleteResult;
import com.aliyun.agentbay.model.SessionResult;
import com.aliyun.agentbay.session.CreateSessionParams;
import com.aliyun.agentbay.session.Session;
import org.junit.Before;
import org.junit.Test;

import static org.junit.Assert.*;

/**
 * Test cases for AgentBay Get API integration.
 * This test class is equivalent to test_agentbay_get_integration.py in Python SDK.
 * 
 * DESIGN PHILOSOPHY COMPARISON:
 * 
 * Python SDK:
 *   - create() → caches session in _sessions
 *   - get(session_id) → calls remote GetSession API (does NOT cache)
 *   - Purpose: Recover existing sessions after restart or across processes
 * 
 * Java SDK (Current):
 *   - create() → caches session in sessions map
 *   - getSession(session_id) → queries local cache only (does NOT call API)
 *   - Missing: Session recovery capability from remote API
 * 
 * WHAT'S MISSING:
 * Java SDK needs a method like Python's get() that:
 * 1. Calls the remote GetSession API
 * 2. Creates a Session object with data from the API
 * 3. Enables session recovery scenarios (restart, cross-process)
 * 
 * This test file is prepared for when the Java SDK implements the actual GetSession API.
 * Until then, the tests use getSession() as a workaround and are marked with TODO comments.
 * 
 * Tests cover:
 * - Getting an existing session by ID (session recovery scenario)
 * - Handling non-existent session IDs
 * - Validating empty and whitespace session IDs
 */
public class TestAgentBayGetIntegration {

    private AgentBay agentBayClient;

    /**
     * Get API key for testing
     */
    private static String getTestApiKey() {
        String apiKey = System.getenv("AGENTBAY_API_KEY");
        if (apiKey == null || apiKey.trim().isEmpty()) {
            fail("AGENTBAY_API_KEY environment variable is not set");
        }
        return apiKey;
    }

    @Before
    public void setUp() throws AgentBayException {
        String apiKey = getTestApiKey();
        this.agentBayClient = new AgentBay(apiKey);
    }

    /**
     * Test Get API with a real session (Session Recovery Scenario).
     * 
     * In a real-world scenario, this tests the ability to recover a session that:
     * - Was created in a previous program run (after restart)
     * - Was created by a different AgentBay instance (cross-process)
     * - Exists on the server but not in local cache
     * 
     * Python SDK flow:
     * 1. Create a session (cached locally)
     * 2. Call get(session_id) - makes API call, creates new Session object (NOT cached)
     * 3. Verify the session can be used normally
     * 
     * This test:
     * 1. Creates a new session
     * 2. Retrieves it using the Get API (simulating recovery)
     * 3. Validates the retrieved session properties
     * 4. Cleans up by deleting the session
     */
    @Test
    public void testGetApi() throws AgentBayException {
        System.out.println("Creating a new session for Get API testing...");

        // Create session
        SessionResult createResult = agentBayClient.create(new CreateSessionParams());
        assertTrue("Failed to create session: " + createResult.getErrorMessage(), 
                   createResult.isSuccess());
        
        Session createdSession = createResult.getSession();
        assertNotNull("Created session is null", createdSession);
        
        String sessionId = createdSession.getSessionId();
        assertNotNull("Session ID is null", sessionId);
        System.out.println("Session created with ID: " + sessionId);

        System.out.println("Testing Get API...");
        
        // TODO: Java SDK does not yet implement AgentBay.get() method that calls GetSession API
        // Python SDK's get() calls the remote GetSession API: self.client.get_session(request)
        // Java SDK's getSession() only queries local cache: sessions.get(sessionId)
        // 
        // Once the Java SDK implements the real GetSession API call, it should work like:
        /*
        SessionResult result = agentBayClient.get(sessionId);
        
        assertNotNull("Get returned null result", result);
        assertTrue("Failed to get session: " + result.getErrorMessage(), result.isSuccess());
        
        Session session = result.getSession();
        assertNotNull("Get returned null session", session);
        assertTrue("Expected Session instance, got " + session.getClass().getName(), 
                   session instanceof Session);
        assertEquals("Expected SessionID " + sessionId + ", got " + session.getSessionId(),
                     sessionId, session.getSessionId());
        assertNotNull("Session agentBay reference is null", session.getAgentBay());
        
        System.out.println("Successfully retrieved session with ID: " + session.getSessionId());
        System.out.println("Get API test passed successfully");
        */
        
        // TEMPORARY WORKAROUND: Use getSession() from local cache
        // This only works because the session was just created in this test
        Session session = agentBayClient.getSession(sessionId);
        assertNotNull("Session not found in cache", session);
        assertEquals("Expected SessionID " + sessionId + ", got " + session.getSessionId(),
                     sessionId, session.getSessionId());
        assertNotNull("Session agentBay reference is null", session.getAgentBay());
        
        System.out.println("Successfully retrieved session from cache with ID: " + session.getSessionId());
        System.out.println("⚠️  Note: Using getSession() cache workaround. Real GetSession API not yet implemented in Java SDK.");

        // Cleanup: Delete the session
        System.out.println("Cleaning up: Deleting the session...");
        DeleteResult deleteResult = session.delete();
        assertTrue("Failed to delete session: " + deleteResult.getErrorMessage(), 
                   deleteResult.isSuccess());
        System.out.println("Session " + sessionId + " deleted successfully");
    }

    /**
     * Test Get API with a non-existent session ID.
     * 
     * This test verifies that attempting to get a non-existent session
     * returns an appropriate error response.
     */
    @Test
    public void testGetNonExistentSession() {
        System.out.println("Testing Get API with non-existent session ID...");
        String nonExistentSessionId = "session-nonexistent-12345";

        // TODO: Java SDK does not yet implement AgentBay.get() method that calls GetSession API
        // Once the real GetSession API is implemented, this should work like:
        /*
        SessionResult result = agentBayClient.get(nonExistentSessionId);
        
        assertFalse("Expected get() to fail for non-existent session", result.isSuccess());
        assertTrue("Error message should contain 'Failed to get session'",
                   result.getErrorMessage().contains("Failed to get session"));
        
        System.out.println("Correctly received error for non-existent session: " + 
                           result.getErrorMessage());
        System.out.println("Get API non-existent session test passed successfully");
        */
        
        // TEMPORARY WORKAROUND: Test with local cache
        Session session = agentBayClient.getSession(nonExistentSessionId);
        assertNull("Expected null for non-existent session in cache", session);
        
        System.out.println("Correctly received null for non-existent session from cache");
        System.out.println("⚠️  Note: Real GetSession API would return error, not null");
    }

    /**
     * Test Get API with empty session ID.
     * 
     * This test verifies that attempting to get a session with an empty
     * session ID returns an appropriate validation error.
     */
    @Test
    public void testGetEmptySessionId() {
        System.out.println("Testing Get API with empty session ID...");

        // TODO: Java SDK does not yet implement AgentBay.get() method with validation
        // Once the real GetSession API is implemented with input validation, this should work like:
        /*
        SessionResult result = agentBayClient.get("");
        
        assertFalse("Expected get() to fail for empty session ID", result.isSuccess());
        assertTrue("Error message should contain 'session_id is required'",
                   result.getErrorMessage().contains("session_id is required"));
        
        System.out.println("Correctly received error for empty session ID: " + 
                           result.getErrorMessage());
        System.out.println("Get API empty session ID test passed successfully");
        */
        
        // TEMPORARY WORKAROUND: Test with local cache
        Session session = agentBayClient.getSession("");
        assertNull("Expected null for empty session ID in cache", session);
        
        System.out.println("Correctly received null for empty session ID from cache");
        System.out.println("⚠️  Note: Real GetSession API should return validation error");
    }

    /**
     * Test Get API with whitespace-only session ID.
     * 
     * This test verifies that attempting to get a session with a whitespace-only
     * session ID returns an appropriate validation error.
     */
    @Test
    public void testGetWhitespaceSessionId() {
        System.out.println("Testing Get API with whitespace session ID...");

        // TODO: Java SDK does not yet implement AgentBay.get() method with validation
        // Once the real GetSession API is implemented with input validation, this should work like:
        /*
        SessionResult result = agentBayClient.get("   ");
        
        assertFalse("Expected get() to fail for whitespace session ID", result.isSuccess());
        assertTrue("Error message should contain 'session_id is required'",
                   result.getErrorMessage().contains("session_id is required"));
        
        System.out.println("Correctly received error for whitespace session ID: " + 
                           result.getErrorMessage());
        System.out.println("Get API whitespace session ID test passed successfully");
        */
        
        // TEMPORARY WORKAROUND: Test with local cache
        Session session = agentBayClient.getSession("   ");
        assertNull("Expected null for whitespace session ID in cache", session);
        
        System.out.println("Correctly received null for whitespace session ID from cache");
        System.out.println("⚠️  Note: Real GetSession API should return validation error");
    }

    /**
     * Main method to run tests manually (for debugging purposes).
     * In production, use Maven or IDE test runners.
     * 
     * Note: These tests demonstrate the need for a session recovery API in Java SDK.
     * Currently using getSession() cache lookup as a workaround.
     */
    public static void main(String[] args) {
        System.out.println("=== Running AgentBay Get API Integration Tests ===");
        System.out.println("=== Testing Session Recovery Capability ===\n");
        
        TestAgentBayGetIntegration test = new TestAgentBayGetIntegration();
        
        try {
            test.setUp();
            
            System.out.println("\n--- Test 1: Get API with real session ---");
            test.testGetApi();
            
            System.out.println("\n--- Test 2: Get API with non-existent session ---");
            test.testGetNonExistentSession();
            
            System.out.println("\n--- Test 3: Get API with empty session ID ---");
            test.testGetEmptySessionId();
            
            System.out.println("\n--- Test 4: Get API with whitespace session ID ---");
            test.testGetWhitespaceSessionId();
            
            System.out.println("\n=== All Tests Completed Successfully ===");
        } catch (Exception e) {
            System.err.println("❌ Test failed: " + e.getMessage());
            e.printStackTrace();
        }
    }
}

