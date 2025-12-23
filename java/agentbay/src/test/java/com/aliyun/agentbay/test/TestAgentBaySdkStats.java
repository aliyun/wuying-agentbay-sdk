package com.aliyun.agentbay.test;

import com.aliyun.agentbay.AgentBay;
import com.aliyun.agentbay.exception.AgentBayException;
import com.aliyun.agentbay.model.DeleteResult;
import com.aliyun.agentbay.model.SessionResult;
import com.aliyun.agentbay.session.CreateSessionParams;
import com.aliyun.agentbay.session.Session;
import org.junit.*;

import static org.junit.Assert.*;

/**
 * Test cases for SDK stats tracking in AgentBay
 * This test class verifies that sessions can be created with and without framework parameter,
 * which ensures the sdkStats field is correctly set during session creation.
 * Similar to test_create_session_with_policy_id in Python SDK, but using integration tests
 * instead of mocks to match the style of other Java test cases.
 */
public class TestAgentBaySdkStats {

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
     * Test that session can be created without framework parameter
     * This verifies that sdkStats is correctly set with empty framework field
     */
    @Test
    public void testCreateSessionWithoutFramework() throws AgentBayException {
        String apiKey = getTestApiKey();
        AgentBay agentBay = new AgentBay(apiKey);

        // Create session parameters without framework
        CreateSessionParams params = new CreateSessionParams();

        // Create session
        SessionResult result = agentBay.create(params);

        // Verify session creation was successful
        assertTrue("Session creation failed: " + result.getErrorMessage(), result.isSuccess());
        assertNotNull("Session object is null", result.getSession());

        Session session = result.getSession();
        assertNotNull("Session ID is null", session.getSessionId());
        assertFalse("Session ID is empty", session.getSessionId().isEmpty());

        System.out.println("✅ testCreateSessionWithoutFramework passed");
        System.out.println("Session created with ID: " + session.getSessionId());

        // Clean up
        try {
            DeleteResult deleteResult = agentBay.delete(session, false);
            assertTrue("Session deletion failed", deleteResult.isSuccess());
        } catch (Exception e) {
            System.out.println("Warning: Error deleting session: " + e.getMessage());
        }
    }

    /**
     * Test that session can be created with framework parameter
     * This verifies that sdkStats is correctly set with framework field
     */
    @Test
    public void testCreateSessionWithFramework() throws AgentBayException {
        String apiKey = getTestApiKey();
        AgentBay agentBay = new AgentBay(apiKey);

        // Create session parameters with framework
        CreateSessionParams params = new CreateSessionParams();
        params.setFramework("spring-ai");

        // Create session
        SessionResult result = agentBay.create(params);

        // Verify session creation was successful
        assertTrue("Session creation failed: " + result.getErrorMessage(), result.isSuccess());
        assertNotNull("Session object is null", result.getSession());

        Session session = result.getSession();
        assertNotNull("Session ID is null", session.getSessionId());
        assertFalse("Session ID is empty", session.getSessionId().isEmpty());

        System.out.println("✅ testCreateSessionWithFramework passed");
        System.out.println("Session created with ID: " + session.getSessionId());
        System.out.println("Framework: " + params.getFramework());

        // Clean up
        try {
            DeleteResult deleteResult = agentBay.delete(session, false);
            assertTrue("Session deletion failed", deleteResult.isSuccess());
        } catch (Exception e) {
            System.out.println("Warning: Error deleting session: " + e.getMessage());
        }
    }

    /**
     * Test that session can be created with different framework values
     */
    @Test
    public void testCreateSessionWithDifferentFrameworks() throws AgentBayException {
        String apiKey = getTestApiKey();
        AgentBay agentBay = new AgentBay(apiKey);

        String[] frameworks = {"spring-ai", "langchain4j", ""};

        for (String framework : frameworks) {
            // Create session parameters with framework
            CreateSessionParams params = new CreateSessionParams();
            if (!framework.isEmpty()) {
                params.setFramework(framework);
            }

            // Create session
            SessionResult result = agentBay.create(params);

            // Verify session creation was successful
            assertTrue("Session creation failed for framework '" + framework + "': " + result.getErrorMessage(), 
                      result.isSuccess());
            assertNotNull("Session object is null for framework '" + framework + "'", result.getSession());

            Session session = result.getSession();
            assertNotNull("Session ID is null for framework '" + framework + "'", session.getSessionId());

            System.out.println("✅ Session created successfully with framework: '" + framework + "'");
            System.out.println("   Session ID: " + session.getSessionId());

            // Clean up
            try {
                DeleteResult deleteResult = agentBay.delete(session, false);
                assertTrue("Session deletion failed", deleteResult.isSuccess());
            } catch (Exception e) {
                System.out.println("Warning: Error deleting session: " + e.getMessage());
            }
        }

        System.out.println("✅ testCreateSessionWithDifferentFrameworks passed");
    }
}

