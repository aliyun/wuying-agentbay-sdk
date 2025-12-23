package com.aliyun.agentbay.test;

import com.aliyun.agentbay.AgentBay;
import com.aliyun.agentbay.agent.Agent;
import com.aliyun.agentbay.exception.AgentBayException;
import com.aliyun.agentbay.model.ExecutionResult;
import com.aliyun.agentbay.model.QueryResult;
import com.aliyun.agentbay.model.SessionResult;
import com.aliyun.agentbay.session.CreateSessionParams;
import com.aliyun.agentbay.session.Session;
import org.junit.AfterClass;
import org.junit.BeforeClass;
import org.junit.Test;

import static org.junit.Assert.*;

/**
 * Integration tests for Agent functionality in AgentBay Java SDK.
 * This test class is equivalent to test_agent_integration.py in Python SDK.
 */
public class TestAgentIntegration {
    private static AgentBay agentBay;
    private static Session session;
    private static Agent agent;

    /**
     * Get API key for testing
     */
    private static String getTestApiKey() {
        String apiKey = System.getenv("AGENTBAY_API_KEY");
        if (apiKey == null || apiKey.trim().isEmpty()) {
            apiKey = "akm-xxx"; // Replace with your actual API key for testing
            System.out.println("Warning: Using default API key. Set AGENTBAY_API_KEY environment variable for production use.");
        }
        return apiKey;
    }

    /**
     * Set up the test environment by creating a session and initializing agent.
     */
    @BeforeClass
    public static void setUp() throws AgentBayException, InterruptedException {
        // Ensure a delay to avoid session creation conflicts
        Thread.sleep(3000);
        
        String apiKey = getTestApiKey();
        agentBay = new AgentBay(apiKey);
        
        // Create a session with windows_latest image
        CreateSessionParams params = new CreateSessionParams();
        params.setImageId("windows_latest");
        
        System.out.println("Creating a new session for agent testing...");
        SessionResult sessionResult = agentBay.create(params);
        
        if (!sessionResult.isSuccess() || sessionResult.getSession() == null) {
            throw new AgentBayException("Failed to create session: " + sessionResult.getErrorMessage());
        }
        
        session = sessionResult.getSession();
        agent = session.getAgent();

        System.out.println("Session created with ID: " + session.getSessionId());
    }

    /**
     * Clean up resources after all tests.
     */
    @AfterClass
    public static void tearDown() {
        System.out.println("Cleaning up: Deleting the session...");
        try {
            if (session != null) {
                agentBay.delete(session, false);
            }
        } catch (Exception e) {
            System.err.println("Warning: Error deleting session: " + e.getMessage());
        }
    }

    @Test
    public void testExecuteTaskSuccess() {
        System.out.println("🚀 Test: Execute task synchronously");

        String task = "create a folder named 'agentbay' in C:\\Windows\\Temp";
        String maxTryTimesEnv = System.getenv("AGENT_TASK_TIMEOUT");
        int maxTryTimes = (maxTryTimesEnv != null && !maxTryTimesEnv.isEmpty())
            ? Integer.parseInt(maxTryTimesEnv)
            : 100;

        ExecutionResult result = agent.getComputer().executeTaskAndWait(task, maxTryTimes);

        assertTrue("Task execution should succeed", result.isSuccess());
        assertNotNull("Request ID should not be null", result.getRequestId());
        assertFalse("Request ID should not be empty", result.getRequestId().isEmpty());
        assertEquals("Error message should be empty", "", result.getErrorMessage());
        assertNotNull("Task result should not be null", result.getTaskResult());

        System.out.println("✅ Task result: " + result.getTaskResult());
    }

    @Test
    public void testAsyncExecuteTaskSuccess() throws InterruptedException {
        System.out.println("🚀 Test: Execute task asynchronously");

        String task = "create a folder named 'agentbay' in C:\\Windows\\Temp";
        String maxTryTimesEnv = System.getenv("AGENT_TASK_TIMEOUT");
        int maxTryTimes = (maxTryTimesEnv != null && !maxTryTimesEnv.isEmpty())
            ? Integer.parseInt(maxTryTimesEnv)
            : 100;

        // Start async task execution
        ExecutionResult result = agent.getComputer().executeTask(task);

        assertTrue("Async task execution should succeed", result.isSuccess());
        assertNotNull("Request ID should not be null", result.getRequestId());
        assertFalse("Request ID should not be empty", result.getRequestId().isEmpty());
        assertEquals("Error message should be empty", "", result.getErrorMessage());
        assertNotNull("Task ID should not be null", result.getTaskId());
        assertFalse("Task ID should not be empty", result.getTaskId().isEmpty());

        // Poll task status until finished
        int retryTimes = 0;
        QueryResult queryResult = null;

        while (retryTimes < maxTryTimes) {
            queryResult = agent.getComputer().getTaskStatus(result.getTaskId());

            assertTrue("Query should succeed", queryResult.isSuccess());
            System.out.println("⏳ Task " + queryResult.getTaskId() + " running 🚀: " +
                              queryResult.getTaskAction());

            if ("finished".equals(queryResult.getTaskStatus())) {
                break;
            }

            retryTimes++;
            Thread.sleep(3000);
        }

        // Verify the final task status
        assertNotNull("Query result should not be null", queryResult);
        assertTrue("Task should finish within timeout", retryTimes < maxTryTimes);
        assertEquals("Task status should be finished", "finished", queryResult.getTaskStatus());

        System.out.println("✅ Task result: " + queryResult.getTaskProduct());
    }

    /**
     * Main method to run tests manually (for debugging purposes).
     * In production, use Maven or IDE test runners.
     */
    public static void main(String[] args) {
        System.out.println("=== Running Agent Integration Tests ===\n");
        
        TestAgentIntegration test = new TestAgentIntegration();
        
        try {
            
            // Run testExecuteTaskSuccess (currently skipped)
            System.out.println("\n--- Test 2: Execute Task Success ---");
            test.setUp();
            test.testExecuteTaskSuccess();
            test.tearDown();
            
            // Run testAsyncExecuteTaskSuccess (currently skipped)
            System.out.println("\n--- Test 3: Async Execute Task Success ---");
            test.setUp();
            test.testAsyncExecuteTaskSuccess();
            test.tearDown();
            
            System.out.println("\n=== All Tests Completed ===");
            System.out.println("\nNote: Some tests are currently skipped because Agent task execution");
            System.out.println("      methods are not yet implemented in the Java SDK.");
            System.out.println("      Once implemented, uncomment the test code to enable full testing.");
            
        } catch (Exception e) {
            System.err.println("❌ Test failed: " + e.getMessage());
            e.printStackTrace();
        }
    }
}

