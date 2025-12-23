package com.aliyun.agentbay.agent;

import com.aliyun.agentbay.model.*;
import com.aliyun.agentbay.service.BaseService;
import com.aliyun.agentbay.session.Session;
import com.google.gson.Gson;
import com.google.gson.JsonObject;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.HashMap;
import java.util.Map;

/**
 * Agent for natural language driven task execution.
 * Provides high-level task automation capabilities for both computer and browser operations.
 */
public class Agent extends BaseService {
    private static final Logger logger = LoggerFactory.getLogger(Agent.class);
    private static final Gson gson = new Gson();

    private final Computer computer;
    private final Browser browser;

    public Agent(Session session) {
        super(session);
        this.computer = new Computer(session);
        this.browser = new Browser(session);
    }

    /**
     * Get the Computer agent for desktop task execution.
     *
     * @return Computer agent instance
     */
    public Computer getComputer() {
        return computer;
    }

    /**
     * Get the Browser agent for browser task execution.
     *
     * @return Browser agent instance
     */
    public Browser getBrowser() {
        return browser;
    }

    /**
     * Computer agent for desktop automation with natural language.
     * Uses flux_* MCP tools for task execution.
     */
    public static class Computer extends BaseService {
        private static final Logger logger = LoggerFactory.getLogger(Computer.class);

        public Computer(Session session) {
            super(session);
        }

        /**
         * Execute a task in human language without waiting for completion (non-blocking).
         *
         * This is a fire-and-return interface that immediately provides a task ID.
         * Call getTaskStatus to check the task status. You can control the timeout
         * of the task execution in your own code by setting the frequency of calling
         * getTaskStatus and the maxTryTimes.
         *
         * @param task Task description in human language
         * @return ExecutionResult containing success status, task ID, task status, and error message if any
         *
         * @example
         * <pre>
         * ExecutionResult result = session.getAgent().getComputer().executeTask("Open Chrome browser");
         * System.out.println("Task ID: " + result.getTaskId() + ", Status: " + result.getTaskStatus());
         * QueryResult status = session.getAgent().getComputer().getTaskStatus(result.getTaskId());
         * System.out.println("Task status: " + status.getTaskStatus());
         * </pre>
         */
        public ExecutionResult executeTask(String task) {
            try {
                Map<String, Object> args = new HashMap<>();
                args.put("task", task);

                OperationResult result = callMcpTool("flux_execute_task", args);

                if (result.isSuccess()) {
                    JsonObject content = gson.fromJson(result.getData(), JsonObject.class);
                    String taskId = content.has("task_id") ? content.get("task_id").getAsString() : "";

                    return new ExecutionResult(
                        result.getRequestId(),
                        true,
                        "",
                        taskId,
                        "running"
                    );
                } else {
                    logger.error("Task execute failed");
                    return new ExecutionResult(
                        result.getRequestId(),
                        false,
                        result.getErrorMessage() != null ? result.getErrorMessage() : "Failed to execute task",
                        "",
                        "failed"
                    );
                }
            } catch (Exception e) {
                logger.error("Failed to execute task", e);
                return new ExecutionResult(
                    "",
                    false,
                    "Failed to execute: " + e.getMessage(),
                    "",
                    "failed"
                );
            }
        }

        /**
         * Execute a specific task described in human language synchronously.
         *
         * This is a synchronous interface that blocks until the task is completed or
         * an error occurs, or timeout happens. The default polling interval is 3 seconds,
         * so set a proper maxTryTimes according to your task complexity.
         *
         * @param task Task description in human language
         * @param maxTryTimes Maximum number of retries
         * @return ExecutionResult containing success status, task ID, task status, task result, and error message if any
         *
         * @example
         * <pre>
         * ExecutionResult result = session.getAgent().getComputer()
         *     .executeTaskAndWait("Open Chrome browser", 20);
         * System.out.println("Task result: " + result.getTaskResult());
         * </pre>
         */
        public ExecutionResult executeTaskAndWait(String task, int maxTryTimes) {
            try {
                Map<String, Object> args = new HashMap<>();
                args.put("task", task);

                OperationResult result = callMcpTool("flux_execute_task", args);

                if (result.isSuccess()) {
                    JsonObject content = gson.fromJson(result.getData(), JsonObject.class);
                    String taskId = content.has("task_id") ? content.get("task_id").getAsString() : "";

                    int triedTime = 0;
                    while (triedTime < maxTryTimes) {
                        QueryResult query = getTaskStatus(taskId);

                        if ("finished".equals(query.getTaskStatus())) {
                            return new ExecutionResult(
                                result.getRequestId(),
                                true,
                                "",
                                taskId,
                                query.getTaskStatus(),
                                query.getTaskProduct()
                            );
                        } else if ("failed".equals(query.getTaskStatus())) {
                            return new ExecutionResult(
                                result.getRequestId(),
                                false,
                                "Failed to execute task.",
                                taskId,
                                query.getTaskStatus(),
                                ""
                            );
                        } else if ("unsupported".equals(query.getTaskStatus())) {
                            return new ExecutionResult(
                                result.getRequestId(),
                                false,
                                "Unsupported task.",
                                taskId,
                                query.getTaskStatus(),
                                ""
                            );
                        }

                        logger.info("⏳ Task {} running 🚀: {}.", taskId, query.getTaskAction());

                        Thread.sleep(3000);
                        triedTime++;
                    }

                    logger.warn("⚠️ task execution timeout!");
                    return new ExecutionResult(
                        result.getRequestId(),
                        false,
                        "Task timeout.",
                        taskId,
                        "failed",
                        "Task timeout."
                    );
                } else {
                    logger.error("❌ Task execution failed");
                    return new ExecutionResult(
                        result.getRequestId(),
                        false,
                        result.getErrorMessage() != null ? result.getErrorMessage() : "Failed to execute task",
                        "",
                        "failed",
                        "Task Failed"
                    );
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                return new ExecutionResult(
                    "",
                    false,
                    "Task interrupted: " + e.getMessage(),
                    "",
                    "failed",
                    "Task Failed"
                );
            } catch (Exception e) {
                logger.error("Failed to execute task", e);
                return new ExecutionResult(
                    "",
                    false,
                    "Failed to execute: " + e.getMessage(),
                    "",
                    "failed",
                    "Task Failed"
                );
            }
        }

        /**
         * Get the status of the task with the given task ID.
         *
         * @param taskId The ID of the task to query
         * @return QueryResult containing success status, task status, task action, task product, and error message if any
         *
         * @example
         * <pre>
         * ExecutionResult result = session.getAgent().getComputer()
         *     .executeTask("Query the weather in Shanghai with Baidu");
         * QueryResult status = session.getAgent().getComputer().getTaskStatus(result.getTaskId());
         * System.out.println("Status: " + status.getTaskStatus() + ", Action: " + status.getTaskAction());
         * </pre>
         */
        public QueryResult getTaskStatus(String taskId) {
            try {
                Map<String, Object> args = new HashMap<>();
                args.put("task_id", taskId);

                OperationResult result = callMcpTool("flux_get_task_status", args);

                if (result.isSuccess()) {
                    JsonObject content = gson.fromJson(result.getData(), JsonObject.class);

                    return new QueryResult(
                        result.getRequestId(),
                        true,
                        "",
                        content.has("task_id") ? content.get("task_id").getAsString() : taskId,
                        content.has("status") ? content.get("status").getAsString() : "finished",
                        content.has("action") ? content.get("action").getAsString() : "",
                        content.has("product") ? content.get("product").getAsString() : ""
                    );
                } else {
                    return new QueryResult(
                        result.getRequestId(),
                        false,
                        result.getErrorMessage() != null ? result.getErrorMessage() : "Failed to get task status",
                        taskId,
                        "failed"
                    );
                }
            } catch (Exception e) {
                logger.error("Failed to get task status", e);
                return new QueryResult(
                    "",
                    false,
                    "Failed to get task status: " + e.getMessage(),
                    taskId,
                    "failed"
                );
            }
        }

        /**
         * Terminate a task with a specified task ID.
         *
         * @param taskId The ID of the running task to terminate
         * @return ExecutionResult containing success status, task ID, task status, and error message if any
         *
         * @example
         * <pre>
         * ExecutionResult result = session.getAgent().getComputer()
         *     .executeTask("Query the weather in Shanghai with Baidu");
         * ExecutionResult terminateResult = session.getAgent().getComputer()
         *     .terminateTask(result.getTaskId());
         * System.out.println("Terminated: " + terminateResult.isSuccess());
         * </pre>
         */
        public ExecutionResult terminateTask(String taskId) {
            logger.info("Terminating task");
            try {
                Map<String, Object> args = new HashMap<>();
                args.put("task_id", taskId);

                OperationResult result = callMcpTool("flux_terminate_task", args);

                if (result.isSuccess()) {
                    JsonObject content = gson.fromJson(result.getData(), JsonObject.class);
                    String returnedTaskId = content.has("task_id") ? content.get("task_id").getAsString() : taskId;

                    return new ExecutionResult(
                        result.getRequestId(),
                        true,
                        "",
                        returnedTaskId,
                        content.has("status") ? content.get("status").getAsString() : "finished"
                    );
                } else {
                    return new ExecutionResult(
                        result.getRequestId(),
                        false,
                        result.getErrorMessage() != null ? result.getErrorMessage() : "Failed to terminate task",
                        taskId,
                        "failed"
                    );
                }
            } catch (Exception e) {
                logger.error("Failed to terminate task", e);
                return new ExecutionResult(
                    "",
                    false,
                    "Failed to terminate: " + e.getMessage(),
                    taskId,
                    "failed"
                );
            }
        }
    }

    /**
     * Browser agent for browser automation with natural language.
     * Uses browser_use_* MCP tools for task execution.
     * Still in BETA.
     */
    public static class Browser extends BaseService {
        private static final Logger logger = LoggerFactory.getLogger(Browser.class);

        public Browser(Session session) {
            super(session);
        }

        /**
         * Initialize the browser agent with options.
         *
         * @param options Options for the agent (can be null for default options)
         * @return InitializationResult containing success status and error message if any
         *
         * @example
         * <pre>
         * AgentOptions options = new AgentOptions(false, "");
         * InitializationResult result = session.getAgent().getBrowser().initialize(options);
         * System.out.println("Initialized: " + result.isSuccess());
         * </pre>
         */
        public InitializationResult initialize(AgentOptions options) {
            logger.info("Initialize Browser Use Agent...");
            try {
                Map<String, Object> args = new HashMap<>();
                if (options != null) {
                    args.put("use_vision", options.isUseVision());
                    args.put("output_schema", options.getOutputSchema());
                } else {
                    args.put("use_vision", false);
                    args.put("output_schema", "");
                }

                OperationResult result = callMcpTool("browser_use_initialize", args);

                if (result.isSuccess()) {
                    return new InitializationResult(
                        result.getRequestId(),
                        true,
                        ""
                    );
                } else {
                    return new InitializationResult(
                        result.getRequestId(),
                        false,
                        "Failed to initialize browser use agent"
                    );
                }
            } catch (Exception e) {
                logger.error("Failed to initialize", e);
                return new InitializationResult(
                    "",
                    false,
                    "Failed to initialize: " + e.getMessage()
                );
            }
        }

        /**
         * Execute a browser task in human language without waiting for completion (non-blocking).
         *
         * This is a fire-and-return interface that immediately provides a task ID.
         * Call getTaskStatus to check the task status. You can control the timeout
         * of the task execution in your own code by setting the frequency of calling
         * getTaskStatus and the maxTryTimes.
         *
         * @param task Task description in human language
         * @return ExecutionResult containing success status, task ID, task status, and error message if any
         *
         * @example
         * <pre>
         * ExecutionResult result = session.getAgent().getBrowser()
         *     .executeTask("Query the weather in Shanghai with Baidu");
         * System.out.println("Task ID: " + result.getTaskId() + ", Status: " + result.getTaskStatus());
         * QueryResult status = session.getAgent().getBrowser().getTaskStatus(result.getTaskId());
         * System.out.println("Task status: " + status.getTaskStatus());
         * </pre>
         */
        public ExecutionResult executeTask(String task) {
            try {
                Map<String, Object> args = new HashMap<>();
                args.put("task", task);

                OperationResult result = callMcpTool("browser_use_execute_task", args);

                if (result.isSuccess()) {
                    JsonObject content = gson.fromJson(result.getData(), JsonObject.class);
                    String taskId = content.has("task_id") ? content.get("task_id").getAsString() : "";

                    return new ExecutionResult(
                        result.getRequestId(),
                        true,
                        "",
                        taskId,
                        "running"
                    );
                } else {
                    logger.error("Task execute failed");
                    return new ExecutionResult(
                        result.getRequestId(),
                        false,
                        result.getErrorMessage() != null ? result.getErrorMessage() : "Failed to execute task",
                        "",
                        "failed"
                    );
                }
            } catch (Exception e) {
                logger.error("Failed to execute task", e);
                return new ExecutionResult(
                    "",
                    false,
                    "Failed to execute: " + e.getMessage(),
                    "",
                    "failed"
                );
            }
        }

        /**
         * Execute a specific task described in human language synchronously.
         *
         * This is a synchronous interface that blocks until the task is completed or
         * an error occurs, or timeout happens. The default polling interval is 3 seconds,
         * so set a proper maxTryTimes according to your task complexity.
         *
         * @param task Task description in human language
         * @param maxTryTimes Maximum number of retries
         * @return ExecutionResult containing success status, task ID, task status, task result, and error message if any
         *
         * @example
         * <pre>
         * ExecutionResult result = session.getAgent().getBrowser()
         *     .executeTaskAndWait("Query the weather in Shanghai with Baidu", 20);
         * System.out.println("Task result: " + result.getTaskResult());
         * </pre>
         */
        public ExecutionResult executeTaskAndWait(String task, int maxTryTimes) {
            try {
                Map<String, Object> args = new HashMap<>();
                args.put("task", task);

                OperationResult result = callMcpTool("browser_use_execute_task", args);

                if (result.isSuccess()) {
                    JsonObject content = gson.fromJson(result.getData(), JsonObject.class);
                    String taskId = content.has("task_id") ? content.get("task_id").getAsString() : "";

                    int triedTime = 0;
                    while (triedTime < maxTryTimes) {
                        QueryResult query = getTaskStatus(taskId);

                        if ("finished".equals(query.getTaskStatus())) {
                            return new ExecutionResult(
                                result.getRequestId(),
                                true,
                                "",
                                taskId,
                                query.getTaskStatus(),
                                query.getTaskProduct()
                            );
                        } else if ("failed".equals(query.getTaskStatus())) {
                            return new ExecutionResult(
                                result.getRequestId(),
                                false,
                                "Failed to execute task.",
                                taskId,
                                query.getTaskStatus(),
                                ""
                            );
                        } else if ("unsupported".equals(query.getTaskStatus())) {
                            return new ExecutionResult(
                                result.getRequestId(),
                                false,
                                "Unsupported task.",
                                taskId,
                                query.getTaskStatus(),
                                ""
                            );
                        }

                        logger.info("⏳ Task {} running 🚀: {}.", taskId, query.getTaskAction());

                        Thread.sleep(3000);
                        triedTime++;
                    }

                    logger.warn("⚠️ task execution timeout!");
                    return new ExecutionResult(
                        result.getRequestId(),
                        false,
                        "Task timeout.",
                        taskId,
                        "failed",
                        "Task timeout."
                    );
                } else {
                    logger.error("❌ Task execution failed");
                    return new ExecutionResult(
                        result.getRequestId(),
                        false,
                        result.getErrorMessage() != null ? result.getErrorMessage() : "Failed to execute task",
                        "",
                        "failed",
                        "Task Failed"
                    );
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                return new ExecutionResult(
                    "",
                    false,
                    "Task interrupted: " + e.getMessage(),
                    "",
                    "failed",
                    "Task Failed"
                );
            } catch (Exception e) {
                logger.error("Failed to execute task", e);
                return new ExecutionResult(
                    "",
                    false,
                    "Failed to execute: " + e.getMessage(),
                    "",
                    "failed",
                    "Task Failed"
                );
            }
        }

        /**
         * Get the status of the task with the given task ID.
         *
         * @param taskId The ID of the task to query
         * @return QueryResult containing success status, task status, task action, task product, and error message if any
         *
         * @example
         * <pre>
         * ExecutionResult result = session.getAgent().getBrowser()
         *     .executeTask("Open Chrome browser");
         * QueryResult status = session.getAgent().getBrowser().getTaskStatus(result.getTaskId());
         * System.out.println("Status: " + status.getTaskStatus() + ", Action: " + status.getTaskAction());
         * </pre>
         */
        public QueryResult getTaskStatus(String taskId) {
            try {
                Map<String, Object> args = new HashMap<>();
                args.put("task_id", taskId);

                OperationResult result = callMcpTool("browser_use_get_task_status", args);

                if (result.isSuccess()) {
                    JsonObject content = gson.fromJson(result.getData(), JsonObject.class);

                    return new QueryResult(
                        result.getRequestId(),
                        true,
                        "",
                        content.has("task_id") ? content.get("task_id").getAsString() : taskId,
                        content.has("status") ? content.get("status").getAsString() : "finished",
                        content.has("action") ? content.get("action").getAsString() : "",
                        content.has("product") ? content.get("product").getAsString() : ""
                    );
                } else {
                    return new QueryResult(
                        result.getRequestId(),
                        false,
                        result.getErrorMessage() != null ? result.getErrorMessage() : "Failed to get task status",
                        taskId,
                        "failed"
                    );
                }
            } catch (Exception e) {
                logger.error("Failed to get task status", e);
                return new QueryResult(
                    "",
                    false,
                    "Failed to get task status: " + e.getMessage(),
                    taskId,
                    "failed"
                );
            }
        }

        /**
         * Terminate a task with a specified task ID.
         *
         * @param taskId The ID of the running task to terminate
         * @return ExecutionResult containing success status, task ID, task status, and error message if any
         *
         * @example
         * <pre>
         * ExecutionResult result = session.getAgent().getBrowser()
         *     .executeTask("Open Chrome browser");
         * ExecutionResult terminateResult = session.getAgent().getBrowser()
         *     .terminateTask(result.getTaskId());
         * System.out.println("Terminated: " + terminateResult.isSuccess());
         * </pre>
         */
        public ExecutionResult terminateTask(String taskId) {
            logger.info("Terminating task");
            try {
                Map<String, Object> args = new HashMap<>();
                args.put("task_id", taskId);

                OperationResult result = callMcpTool("browser_use_terminate_task", args);

                if (result.isSuccess()) {
                    JsonObject content = gson.fromJson(result.getData(), JsonObject.class);
                    String returnedTaskId = content.has("task_id") ? content.get("task_id").getAsString() : taskId;

                    return new ExecutionResult(
                        result.getRequestId(),
                        true,
                        "",
                        returnedTaskId,
                        content.has("status") ? content.get("status").getAsString() : "finished"
                    );
                } else {
                    return new ExecutionResult(
                        result.getRequestId(),
                        false,
                        result.getErrorMessage() != null ? result.getErrorMessage() : "Failed to terminate task",
                        taskId,
                        "failed"
                    );
                }
            } catch (Exception e) {
                logger.error("Failed to terminate task", e);
                return new ExecutionResult(
                    "",
                    false,
                    "Failed to terminate: " + e.getMessage(),
                    taskId,
                    "failed"
                );
            }
        }
    }

}
