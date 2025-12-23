package com.aliyun.agentbay.examples;

import com.aliyun.agentbay.AgentBay;
import com.aliyun.agentbay.model.AgentOptions;
import com.aliyun.agentbay.model.ExecutionResult;
import com.aliyun.agentbay.model.InitializationResult;
import com.aliyun.agentbay.model.QueryResult;
import com.aliyun.agentbay.model.SessionResult;
import com.aliyun.agentbay.session.CreateSessionParams;
import com.aliyun.agentbay.session.Session;

/**
 * Example demonstrating Agent module usage in AgentBay Java SDK.
 *
 * This example shows how to:
 * 1. Execute computer tasks with natural language (Computer Agent)
 * 2. Execute browser tasks with natural language (Browser Agent)
 * 3. Use both synchronous and asynchronous task execution
 * 4. Monitor task status and get results
 */
public class AgentExample {

    public static void main(String[] args) throws Exception {
        String apiKey = System.getenv("AGENTBAY_API_KEY");
        if (apiKey == null || apiKey.trim().isEmpty()) {
            System.err.println("Error: AGENTBAY_API_KEY environment variable is not set");
            System.err.println("Please set it with: export AGENTBAY_API_KEY=your_api_key_here");
            return;
        }

        AgentBay agentBay = new AgentBay(apiKey);

        System.out.println("=== AgentBay Agent Module Example ===\n");

        // Example 1: Computer Agent - Synchronous execution
        System.out.println("--- Example 1: Computer Agent (Sync) ---");
        computerAgentSyncExample(agentBay);

        // Example 2: Computer Agent - Asynchronous execution
        System.out.println("\n--- Example 2: Computer Agent (Async) ---");
        computerAgentAsyncExample(agentBay);

        // Example 3: Browser Agent - Synchronous execution
        System.out.println("\n--- Example 3: Browser Agent (Sync) ---");
        browserAgentSyncExample(agentBay);

        // Example 4: Browser Agent - Asynchronous execution
        System.out.println("\n--- Example 4: Browser Agent (Async) ---");
        browserAgentAsyncExample(agentBay);

        System.out.println("\n=== All examples completed ===");
    }

    /**
     * Example 1: Computer Agent with synchronous task execution
     * Demonstrates executing a desktop task and waiting for completion
     */
    private static void computerAgentSyncExample(AgentBay agentBay) {
        Session session = null;
        try {
            // Create a Windows session
            System.out.println("Creating Windows session...");
            CreateSessionParams params = new CreateSessionParams();
            params.setImageId("windows_latest");

            SessionResult sessionResult = agentBay.create(params);
            if (!sessionResult.isSuccess() || sessionResult.getSession() == null) {
                System.err.println("Failed to create session: " + sessionResult.getErrorMessage());
                return;
            }

            session = sessionResult.getSession();
            System.out.println("Session created: " + session.getSessionId());

            // Execute a task synchronously
            String task = "Open Notepad and type 'Hello from AgentBay Java SDK'";
            System.out.println("\nExecuting task: " + task);

            ExecutionResult result = session.getAgent().getComputer()
                .executeTaskAndWait(task, 30);

            if (result.isSuccess()) {
                System.out.println("✅ Task completed successfully!");
                System.out.println("Task ID: " + result.getTaskId());
                System.out.println("Task Status: " + result.getTaskStatus());
                System.out.println("Task Result: " + result.getTaskResult());
            } else {
                System.err.println("❌ Task failed: " + result.getErrorMessage());
            }

        } catch (Exception e) {
            System.err.println("Error: " + e.getMessage());
            e.printStackTrace();
        } finally {
            if (session != null) {
                System.out.println("\nCleaning up session...");
                agentBay.delete(session, false);
            }
        }
    }

    /**
     * Example 2: Computer Agent with asynchronous task execution
     * Demonstrates fire-and-forget task execution with status polling
     */
    private static void computerAgentAsyncExample(AgentBay agentBay) {
        Session session = null;
        try {
            // Create a Windows session
            System.out.println("Creating Windows session...");
            CreateSessionParams params = new CreateSessionParams();
            params.setImageId("windows_latest");

            SessionResult sessionResult = agentBay.create(params);
            if (!sessionResult.isSuccess() || sessionResult.getSession() == null) {
                System.err.println("Failed to create session: " + sessionResult.getErrorMessage());
                return;
            }

            session = sessionResult.getSession();
            System.out.println("Session created: " + session.getSessionId());

            // Execute a task asynchronously
            String task = "Create a folder named 'AgentBay' on the Desktop";
            System.out.println("\nExecuting task asynchronously: " + task);

            ExecutionResult result = session.getAgent().getComputer().executeTask(task);

            if (result.isSuccess()) {
                System.out.println("✅ Task started!");
                System.out.println("Task ID: " + result.getTaskId());
                System.out.println("Initial Status: " + result.getTaskStatus());

                // Poll task status
                int maxRetries = 30;
                int retries = 0;
                while (retries < maxRetries) {
                    Thread.sleep(3000);

                    QueryResult status = session.getAgent().getComputer()
                        .getTaskStatus(result.getTaskId());

                    System.out.println("⏳ Status check " + (retries + 1) + ": " +
                        status.getTaskStatus() + " - " + status.getTaskAction());

                    if ("finished".equals(status.getTaskStatus())) {
                        System.out.println("✅ Task completed!");
                        System.out.println("Result: " + status.getTaskProduct());
                        break;
                    } else if ("failed".equals(status.getTaskStatus())) {
                        System.err.println("❌ Task failed");
                        break;
                    }

                    retries++;
                }

                if (retries >= maxRetries) {
                    System.err.println("⚠️ Task timed out");
                }
            } else {
                System.err.println("❌ Failed to start task: " + result.getErrorMessage());
            }

        } catch (Exception e) {
            System.err.println("Error: " + e.getMessage());
            e.printStackTrace();
        } finally {
            if (session != null) {
                System.out.println("\nCleaning up session...");
                agentBay.delete(session, false);
            }
        }
    }

    /**
     * Example 3: Browser Agent with synchronous task execution
     * Demonstrates executing a browser task with natural language
     */
    private static void browserAgentSyncExample(AgentBay agentBay) {
        Session session = null;
        try {
            // Create a browser session
            System.out.println("Creating browser session...");
            CreateSessionParams params = new CreateSessionParams();
            params.setImageId("browser_latest");

            SessionResult sessionResult = agentBay.create(params);
            if (!sessionResult.isSuccess() || sessionResult.getSession() == null) {
                System.err.println("Failed to create session: " + sessionResult.getErrorMessage());
                return;
            }

            session = sessionResult.getSession();
            System.out.println("Session created: " + session.getSessionId());

            // Initialize browser agent
            System.out.println("\nInitializing browser agent...");
            AgentOptions options = new AgentOptions(false, "");
            InitializationResult initResult = session.getAgent().getBrowser().initialize(options);

            if (!initResult.isSuccess()) {
                System.err.println("Failed to initialize browser agent: " + initResult.getErrorMessage());
                return;
            }

            System.out.println("✅ Browser agent initialized");

            // Execute a browser task synchronously
            String task = "Go to example.com and get the page title";
            System.out.println("\nExecuting task: " + task);

            ExecutionResult result = session.getAgent().getBrowser()
                .executeTaskAndWait(task, 30);

            if (result.isSuccess()) {
                System.out.println("✅ Task completed successfully!");
                System.out.println("Task ID: " + result.getTaskId());
                System.out.println("Task Status: " + result.getTaskStatus());
                System.out.println("Task Result: " + result.getTaskResult());
            } else {
                System.err.println("❌ Task failed: " + result.getErrorMessage());
            }

        } catch (Exception e) {
            System.err.println("Error: " + e.getMessage());
            e.printStackTrace();
        } finally {
            if (session != null) {
                System.out.println("\nCleaning up session...");
                agentBay.delete(session, false);
            }
        }
    }

    /**
     * Example 4: Browser Agent with asynchronous task execution
     * Demonstrates async browser task with status monitoring
     */
    private static void browserAgentAsyncExample(AgentBay agentBay) {
        Session session = null;
        try {
            // Create a browser session
            System.out.println("Creating browser session...");
            CreateSessionParams params = new CreateSessionParams();
            params.setImageId("browser_latest");

            SessionResult sessionResult = agentBay.create(params);
            if (!sessionResult.isSuccess() || sessionResult.getSession() == null) {
                System.err.println("Failed to create session: " + sessionResult.getErrorMessage());
                return;
            }

            session = sessionResult.getSession();
            System.out.println("Session created: " + session.getSessionId());

            // Initialize browser agent
            System.out.println("\nInitializing browser agent...");
            AgentOptions options = new AgentOptions(false, "");
            InitializationResult initResult = session.getAgent().getBrowser().initialize(options);

            if (!initResult.isSuccess()) {
                System.err.println("Failed to initialize browser agent: " + initResult.getErrorMessage());
                return;
            }

            System.out.println("✅ Browser agent initialized");

            // Execute a browser task asynchronously
            String task = "Search 'AgentBay documentation' on Baidu";
            System.out.println("\nExecuting task asynchronously: " + task);

            ExecutionResult result = session.getAgent().getBrowser().executeTask(task);

            if (result.isSuccess()) {
                System.out.println("✅ Task started!");
                System.out.println("Task ID: " + result.getTaskId());
                System.out.println("Initial Status: " + result.getTaskStatus());

                // Poll task status
                int maxRetries = 30;
                int retries = 0;
                while (retries < maxRetries) {
                    Thread.sleep(3000);

                    QueryResult status = session.getAgent().getBrowser()
                        .getTaskStatus(result.getTaskId());

                    System.out.println("⏳ Status check " + (retries + 1) + ": " +
                        status.getTaskStatus() + " - " + status.getTaskAction());

                    if ("finished".equals(status.getTaskStatus())) {
                        System.out.println("✅ Task completed!");
                        System.out.println("Result: " + status.getTaskProduct());
                        break;
                    } else if ("failed".equals(status.getTaskStatus())) {
                        System.err.println("❌ Task failed");
                        break;
                    }

                    retries++;
                }

                if (retries >= maxRetries) {
                    System.err.println("⚠️ Task timed out");
                }
            } else {
                System.err.println("❌ Failed to start task: " + result.getErrorMessage());
            }

        } catch (Exception e) {
            System.err.println("Error: " + e.getMessage());
            e.printStackTrace();
        } finally {
            if (session != null) {
                System.out.println("\nCleaning up session...");
                agentBay.delete(session, false);
            }
        }
    }
}
