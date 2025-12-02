package com.aliyun.agentbay.test;

import com.aliyun.agentbay.AgentBay;
import com.aliyun.agentbay.exception.AgentBayException;
import com.aliyun.agentbay.model.DeleteResult;
import com.aliyun.agentbay.model.GetSessionData;
import com.aliyun.agentbay.model.GetSessionResult;
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
 * DESIGN PHILOSOPHY:
 * 
 * Python SDK:
 *   - create() → caches session in _sessions
 *   - get(session_id) → calls remote GetSession API (does NOT cache)
 *   - Purpose: Recover existing sessions after restart or across processes
 * 
 * Java SDK:
 *   - create() → caches session in sessions map
 *   - get(session_id) → calls remote GetSession API (does NOT cache)
 *   - getSession(session_id) → queries local cache only
 *   - Purpose: Recover existing sessions after restart or across processes
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
     * Test GetSessionInfo API to retrieve session metadata.
     * This is equivalent to Python's get_session() method.
     * 
     * This test:
     * 1. Creates a new session
     * 2. Retrieves session info using getSessionInfo()
     * 3. Validates the response structure and data fields
     * 4. Cleans up by deleting the session
     */
    @Test
    public void testGetSessionInfo() throws AgentBayException {
        System.out.println("Creating a new session for GetSessionInfo testing...");

        // Create session
        SessionResult createResult = agentBayClient.create(new CreateSessionParams());
        assertTrue("Failed to create session: " + createResult.getErrorMessage(), 
                   createResult.isSuccess());
        
        Session createdSession = createResult.getSession();
        assertNotNull("Created session is null", createdSession);
        
        String sessionId = createdSession.getSessionId();
        assertNotNull("Session ID is null", sessionId);
        System.out.println("Session created with ID: " + sessionId);

        try {
            // Test GetSessionInfo API
            System.out.println("Testing GetSessionInfo API...");
            GetSessionResult getResult = agentBayClient.getSessionInfo(sessionId);
            
            // Validate response
            assertNotNull("GetSessionInfo returned null result", getResult);
            assertNotNull("RequestId should not be null", getResult.getRequestId());
            System.out.println("GetSessionInfo RequestId: " + getResult.getRequestId());
            
            assertTrue("Expected success to be true", getResult.isSuccess());
            
            // Validate Data field
            GetSessionData data = getResult.getData();
            assertNotNull("Data field should not be null", data);
            assertEquals("Expected SessionID " + sessionId + ", got " + data.getSessionId(),
                         sessionId, data.getSessionId());
            
            assertNotNull("AppInstanceId should not be null", data.getAppInstanceId());
            assertFalse("AppInstanceId should not be empty", data.getAppInstanceId().isEmpty());
            System.out.println("AppInstanceId: " + data.getAppInstanceId());
            
            assertNotNull("ResourceId should not be null", data.getResourceId());
            assertFalse("ResourceId should not be empty", data.getResourceId().isEmpty());
            System.out.println("ResourceId: " + data.getResourceId());
            
            // Print additional fields from GetSession response
            System.out.println("VpcResource: " + data.isVpcResource());
            System.out.println("HttpPort: " + data.getHttpPort());
            System.out.println("NetworkInterfaceIp: " + data.getNetworkInterfaceIp());
            System.out.println("Token: " + (data.getToken() != null ? "***" : ""));
            System.out.println("ResourceUrl: " + data.getResourceUrl());
            
            System.out.println("GetSessionInfo API test passed successfully");
            
        } finally {
            // Cleanup: Delete the session
            System.out.println("Cleaning up: Deleting the session...");
            DeleteResult deleteResult = createdSession.delete();
            assertTrue("Failed to delete session: " + deleteResult.getErrorMessage(), 
                       deleteResult.isSuccess());
            System.out.println("Session " + sessionId + " deleted successfully");
        }
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
     * 2. Retrieves session info using getSessionInfo() first
     * 3. Retrieves it using the get() API (simulating recovery)
     * 4. Validates the retrieved session properties match GetSessionInfo data
     * 5. Cleans up by deleting the session
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

        try {
            // First get session info to compare with get() result
            System.out.println("Getting session info for comparison...");
            GetSessionResult getInfoResult = agentBayClient.getSessionInfo(sessionId);
            assertTrue("Failed to get session info", getInfoResult.isSuccess());
            GetSessionData expectedData = getInfoResult.getData();
            assertNotNull("GetSessionInfo data is null", expectedData);

            // Test Get API
            System.out.println("Testing Get API...");
            SessionResult result = agentBayClient.get(sessionId);
            
            assertNotNull("Get returned null result", result);
            assertTrue("Failed to get session: " + result.getErrorMessage(), result.isSuccess());
            assertNotNull("Get should return request_id", result.getRequestId());
            System.out.println("Get() RequestId: " + result.getRequestId());
            
            Session session = result.getSession();
            assertNotNull("Get returned null session", session);
            assertTrue("Expected Session instance, got " + session.getClass().getName(), 
                       session instanceof Session);
            assertEquals("Expected SessionID " + sessionId + ", got " + session.getSessionId(),
                         sessionId, session.getSessionId());
            assertNotNull("Session agentBay reference is null", session.getAgentBay());
            
            // Verify session fields are populated from GetSession response
            // Note: resourceUrl may have different authcode on each call, so we only check that it's present
            assertNotNull("Session resourceUrl should not be null", session.getResourceUrl());
            assertTrue("Session resourceUrl should contain 'resourceId='", 
                       session.getResourceUrl().contains("resourceId="));
            System.out.println("Session resourceUrl validated");
            
            // VPC fields verification (if VPC is enabled)
            // Note: VPC functionality is temporarily disabled in Java SDK
            // When enabled, uncomment these verifications:
            /*
            if (expectedData.isVpcResource()) {
                assertEquals("Session httpPort should match", 
                             expectedData.getHttpPort(), session.getHttpPort());
                assertEquals("Session networkInterfaceIp should match",
                             expectedData.getNetworkInterfaceIp(), session.getNetworkInterfaceIp());
                assertEquals("Session token should match",
                             expectedData.getToken(), session.getToken());
            }
            */
            
            System.out.println("Successfully retrieved session with ID: " + session.getSessionId());
            System.out.println("Get API test passed successfully");
            
        } finally {
            // Cleanup: Delete the session
            System.out.println("Cleaning up: Deleting the session...");
            DeleteResult deleteResult = createdSession.delete();
            assertTrue("Failed to delete session: " + deleteResult.getErrorMessage(), 
                       deleteResult.isSuccess());
            System.out.println("Session " + sessionId + " deleted successfully");
        }
    }

    /**
     * Test Get API with a non-existent session ID.
     * 
     * This test verifies that attempting to get a non-existent session
     * returns an appropriate error response.
     */
    @Test
    public void testGetNonExistentSession() throws AgentBayException {
        System.out.println("Testing Get API with non-existent session ID...");
        String nonExistentSessionId = "session-nonexistent-12345";

        SessionResult result = agentBayClient.get(nonExistentSessionId);
        
        assertFalse("Expected get() to fail for non-existent session", result.isSuccess());
        assertTrue("Error message should contain 'Failed to get session'",
                   result.getErrorMessage() != null && 
                   result.getErrorMessage().contains("Failed to get session"));
        
        System.out.println("Correctly received error for non-existent session: " + 
                           result.getErrorMessage());
        System.out.println("Get API non-existent session test passed successfully");
    }

    /**
     * Test Get API with empty session ID.
     * 
     * This test verifies that attempting to get a session with an empty
     * session ID returns an appropriate validation error.
     */
    @Test
    public void testGetEmptySessionId() throws AgentBayException {
        System.out.println("Testing Get API with empty session ID...");

        SessionResult result = agentBayClient.get("");
        
        assertFalse("Expected get() to fail for empty session ID", result.isSuccess());
        assertTrue("Error message should contain 'session_id is required'",
                   result.getErrorMessage() != null && 
                   result.getErrorMessage().contains("session_id is required"));
        
        System.out.println("Correctly received error for empty session ID: " + 
                           result.getErrorMessage());
        System.out.println("Get API empty session ID test passed successfully");
    }

    /**
     * Test Get API with whitespace-only session ID.
     * 
     * This test verifies that attempting to get a session with a whitespace-only
     * session ID returns an appropriate validation error.
     */
    @Test
    public void testGetWhitespaceSessionId() throws AgentBayException {
        System.out.println("Testing Get API with whitespace session ID...");

        SessionResult result = agentBayClient.get("   ");
        
        assertFalse("Expected get() to fail for whitespace session ID", result.isSuccess());
        assertTrue("Error message should contain 'session_id is required'",
                   result.getErrorMessage() != null && 
                   result.getErrorMessage().contains("session_id is required"));
        
        System.out.println("Correctly received error for whitespace session ID: " + 
                           result.getErrorMessage());
        System.out.println("Get API whitespace session ID test passed successfully");
    }

    /**
     * Test GetSessionInfo API with a non-existent session ID.
     * 
     * This test verifies that attempting to get session info for a non-existent session
     * returns an appropriate error response.
     */
    @Test
    public void testGetSessionInfoNonExistent() throws AgentBayException {
        System.out.println("Testing GetSessionInfo API with non-existent session ID...");
        String nonExistentSessionId = "session-nonexistent-12345";

        GetSessionResult result = agentBayClient.getSessionInfo(nonExistentSessionId);
        
        assertFalse("Expected getSessionInfo() to fail for non-existent session", result.isSuccess());
        assertNotNull("Error message should not be null", result.getErrorMessage());
        assertTrue("Error message should indicate session not found",
                   result.getErrorMessage().contains("not found") || 
                   result.getErrorMessage().contains("Failed to get session"));
        
        System.out.println("Correctly received error for non-existent session: " + 
                           result.getErrorMessage());
        System.out.println("GetSessionInfo non-existent session test passed successfully");
    }

    /**
     * Main method to run tests manually (for debugging purposes).
     * In production, use Maven or IDE test runners.
     */
    public static void main(String[] args) {
        System.out.println("=== Running AgentBay Get API Integration Tests ===");
        System.out.println("=== Testing Session Recovery Capability ===\n");
        
        TestAgentBayGetIntegration test = new TestAgentBayGetIntegration();
        
        try {
            test.setUp();
            
            System.out.println("\n--- Test 1: GetSessionInfo API ---");
            test.testGetSessionInfo();
            
            System.out.println("\n--- Test 2: Get API with real session ---");
            test.testGetApi();
            
            System.out.println("\n--- Test 3: Get API with non-existent session ---");
            test.testGetNonExistentSession();
            
            System.out.println("\n--- Test 4: Get API with empty session ID ---");
            test.testGetEmptySessionId();
            
            System.out.println("\n--- Test 5: Get API with whitespace session ID ---");
            test.testGetWhitespaceSessionId();
            
            System.out.println("\n--- Test 6: GetSessionInfo with non-existent session ---");
            test.testGetSessionInfoNonExistent();
            
            System.out.println("\n=== All Tests Completed Successfully ===");
        } catch (Exception e) {
            System.err.println("❌ Test failed: " + e.getMessage());
            e.printStackTrace();
        }
    }
}

