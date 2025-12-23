# Agent API Reference

The Agent module provides natural language-driven task execution capabilities for both desktop (Computer) and browser (Browser) automation.

## Overview

The Agent module is accessible via `session.getAgent()` and provides two sub-agents:
- **Computer Agent** (`session.getAgent().getComputer()`) - For desktop automation tasks
- **Browser Agent** (`session.getAgent().getBrowser()`) - For browser automation tasks (BETA)

## Architecture

```
Session
└── getAgent() → Agent
    ├── getComputer() → Agent.Computer
    │   ├── executeTask(String task)
    │   ├── executeTaskAndWait(String task, int maxTryTimes)
    │   ├── getTaskStatus(String taskId)
    │   └── terminateTask(String taskId)
    │
    └── getBrowser() → Agent.Browser
        ├── initialize(AgentOptions options)
        ├── executeTask(String task)
        ├── executeTaskAndWait(String task, int maxTryTimes)
        ├── getTaskStatus(String taskId)
        └── terminateTask(String taskId)
```

## Differences: agent.browser vs browser.agent

| Feature | `session.getAgent().getBrowser()` | `session.getBrowser().getAgent()` |
|---------|----------------------------------|-----------------------------------|
| Access Path | `session.getAgent().getBrowser()` | `session.getBrowser().getAgent()` |
| Framework | browser-use | Playwright + PageUse |
| MCP Tools | `browser_use_*` | `page_use_*` |
| Operation Style | Natural language tasks | Specific operations (act, extract, observe) |
| Granularity | Coarse (task-level) | Fine (element-level) |
| Use Case | High-level task automation | Precise page automation & data extraction |
| Example | `executeTask("Submit the form")` | `act("Click #submit button")` |
| Status | BETA | Stable |

---

## Agent.Computer

Desktop automation agent using natural language instructions. Uses `flux_*` MCP tools.

### executeTask

Execute a task asynchronously without waiting for completion (non-blocking).

```java
public ExecutionResult executeTask(String task)
```

**Parameters:**
- `task` (String) - Task description in human language

**Returns:**
- `ExecutionResult` - Contains success status, task ID, and initial status

**Example:**
```java
ExecutionResult result = session.getAgent().getComputer()
    .executeTask("Open Chrome browser");
System.out.println("Task ID: " + result.getTaskId());
System.out.println("Status: " + result.getTaskStatus());

// Poll for completion
QueryResult status = session.getAgent().getComputer()
    .getTaskStatus(result.getTaskId());
```

---

### executeTaskAndWait

Execute a task synchronously, blocking until completion or timeout.

```java
public ExecutionResult executeTaskAndWait(String task, int maxTryTimes)
```

**Parameters:**
- `task` (String) - Task description in human language
- `maxTryTimes` (int) - Maximum number of status checks (polls every 3 seconds)

**Returns:**
- `ExecutionResult` - Contains success status, task ID, status, and result

**Example:**
```java
ExecutionResult result = session.getAgent().getComputer()
    .executeTaskAndWait("Create a folder named 'test' on Desktop", 20);

if (result.isSuccess()) {
    System.out.println("Task completed!");
    System.out.println("Result: " + result.getTaskResult());
} else {
    System.err.println("Task failed: " + result.getErrorMessage());
}
```

---

### getTaskStatus

Query the current status of a running task.

```java
public QueryResult getTaskStatus(String taskId)
```

**Parameters:**
- `taskId` (String) - The ID of the task to query

**Returns:**
- `QueryResult` - Contains task status, current action, and product

**Task Status Values:**
- `"running"` - Task is executing
- `"finished"` - Task completed successfully
- `"failed"` - Task failed
- `"unsupported"` - Task type not supported

**Example:**
```java
QueryResult status = session.getAgent().getComputer()
    .getTaskStatus(taskId);

System.out.println("Status: " + status.getTaskStatus());
System.out.println("Action: " + status.getTaskAction());
System.out.println("Product: " + status.getTaskProduct());
```

---

### terminateTask

Terminate a running task.

```java
public ExecutionResult terminateTask(String taskId)
```

**Parameters:**
- `taskId` (String) - The ID of the task to terminate

**Returns:**
- `ExecutionResult` - Contains success status and termination result

**Example:**
```java
ExecutionResult result = session.getAgent().getComputer()
    .terminateTask(taskId);

if (result.isSuccess()) {
    System.out.println("Task terminated successfully");
}
```

---

## Agent.Browser

Browser automation agent using natural language instructions. Uses `browser_use_*` MCP tools.

⚠️ **Status: BETA** - This feature is still in beta and may have limitations.

### initialize

Initialize the browser agent before use.

```java
public InitializationResult initialize(AgentOptions options)
```

**Parameters:**
- `options` (AgentOptions) - Configuration options (can be null for defaults)
  - `useVision` (boolean) - Enable vision-based interaction
  - `outputSchema` (String) - Custom output schema

**Returns:**
- `InitializationResult` - Contains success status

**Example:**
```java
AgentOptions options = new AgentOptions(false, "");
InitializationResult result = session.getAgent().getBrowser()
    .initialize(options);

if (result.isSuccess()) {
    System.out.println("Browser agent initialized");
}
```

---

### executeTask

Execute a browser task asynchronously without waiting for completion.

```java
public ExecutionResult executeTask(String task)
```

**Parameters:**
- `task` (String) - Browser task description in human language

**Returns:**
- `ExecutionResult` - Contains success status, task ID, and initial status

**Example:**
```java
ExecutionResult result = session.getAgent().getBrowser()
    .executeTask("Search for 'AgentBay' on Google");

System.out.println("Task ID: " + result.getTaskId());
```

---

### executeTaskAndWait

Execute a browser task synchronously, blocking until completion.

```java
public ExecutionResult executeTaskAndWait(String task, int maxTryTimes)
```

**Parameters:**
- `task` (String) - Browser task description in human language
- `maxTryTimes` (int) - Maximum number of status checks (polls every 3 seconds)

**Returns:**
- `ExecutionResult` - Contains success status, task ID, status, and result

**Example:**
```java
ExecutionResult result = session.getAgent().getBrowser()
    .executeTaskAndWait("Go to example.com and get the page title", 20);

if (result.isSuccess()) {
    System.out.println("Result: " + result.getTaskResult());
}
```

---

### getTaskStatus

Query the current status of a browser task.

```java
public QueryResult getTaskStatus(String taskId)
```

**Parameters:**
- `taskId` (String) - The ID of the task to query

**Returns:**
- `QueryResult` - Contains task status, current action, and product

**Example:**
```java
QueryResult status = session.getAgent().getBrowser()
    .getTaskStatus(taskId);

System.out.println("Status: " + status.getTaskStatus());
System.out.println("Action: " + status.getTaskAction());
```

---

### terminateTask

Terminate a running browser task.

```java
public ExecutionResult terminateTask(String taskId)
```

**Parameters:**
- `taskId` (String) - The ID of the task to terminate

**Returns:**
- `ExecutionResult` - Contains success status

**Example:**
```java
ExecutionResult result = session.getAgent().getBrowser()
    .terminateTask(taskId);
```

---

## Model Classes

### ExecutionResult

Result object returned from task execution operations.

**Fields:**
- `requestId` (String) - API request identifier
- `success` (boolean) - Whether the operation succeeded
- `errorMessage` (String) - Error description if failed
- `taskId` (String) - Unique task identifier
- `taskStatus` (String) - Current task status
- `taskResult` (String) - Task output/result (for completed tasks)

---

### QueryResult

Result object returned from status query operations.

**Fields:**
- `requestId` (String) - API request identifier
- `success` (boolean) - Whether the query succeeded
- `errorMessage` (String) - Error description if failed
- `taskId` (String) - Task identifier
- `taskStatus` (String) - Current task status
- `taskAction` (String) - Current action being performed
- `taskProduct` (String) - Task output/product

---

### InitializationResult

Result object returned from initialization operations.

**Fields:**
- `requestId` (String) - API request identifier
- `success` (boolean) - Whether initialization succeeded
- `errorMessage` (String) - Error description if failed

---

### AgentOptions

Configuration options for browser agent initialization.

**Fields:**
- `useVision` (boolean) - Enable vision-based page interaction
- `outputSchema` (String) - Custom JSON schema for output format

**Example:**
```java
AgentOptions options = new AgentOptions();
options.setUseVision(false);
options.setOutputSchema("");
```

---

## Complete Examples

### Example 1: Computer Agent - Sync Execution

```java
// Create session
CreateSessionParams params = new CreateSessionParams();
params.setImageId("windows_latest");
SessionResult sessionResult = agentBay.create(params);
Session session = sessionResult.getSession();

// Execute task synchronously
String task = "Open Notepad and type 'Hello World'";
ExecutionResult result = session.getAgent().getComputer()
    .executeTaskAndWait(task, 30);

if (result.isSuccess()) {
    System.out.println("✅ Completed: " + result.getTaskResult());
}

// Cleanup
agentBay.delete(session, false);
```

---

### Example 2: Computer Agent - Async Execution

```java
// Create session
Session session = agentBay.create(params).getSession();

// Start task asynchronously
ExecutionResult result = session.getAgent().getComputer()
    .executeTask("Create a folder named 'test'");

System.out.println("Task started: " + result.getTaskId());

// Poll for completion
while (true) {
    QueryResult status = session.getAgent().getComputer()
        .getTaskStatus(result.getTaskId());

    System.out.println("Status: " + status.getTaskStatus());

    if ("finished".equals(status.getTaskStatus())) {
        System.out.println("Result: " + status.getTaskProduct());
        break;
    } else if ("failed".equals(status.getTaskStatus())) {
        System.err.println("Task failed");
        break;
    }

    Thread.sleep(3000);
}

// Cleanup
agentBay.delete(session, false);
```

---

### Example 3: Browser Agent - Sync Execution

```java
// Create browser session
CreateSessionParams params = new CreateSessionParams();
params.setImageId("browser_latest");
Session session = agentBay.create(params).getSession();

// Initialize browser agent
AgentOptions options = new AgentOptions(false, "");
session.getAgent().getBrowser().initialize(options);

// Execute browser task
String task = "Go to example.com and extract the page title";
ExecutionResult result = session.getAgent().getBrowser()
    .executeTaskAndWait(task, 30);

if (result.isSuccess()) {
    System.out.println("✅ Result: " + result.getTaskResult());
}

// Cleanup
agentBay.delete(session, false);
```

---

### Example 4: Error Handling

```java
ExecutionResult result = session.getAgent().getComputer()
    .executeTaskAndWait(task, 30);

if (result.isSuccess()) {
    System.out.println("Success: " + result.getTaskResult());
} else {
    System.err.println("Failed: " + result.getErrorMessage());
    System.err.println("Task ID: " + result.getTaskId());
    System.err.println("Status: " + result.getTaskStatus());
}
```

---

## Best Practices

### 1. Task Timeout Configuration

Set `maxTryTimes` based on task complexity:
- Simple tasks (e.g., open application): 10-20 tries (30-60 seconds)
- Medium tasks (e.g., file operations): 20-40 tries (1-2 minutes)
- Complex tasks (e.g., multi-step workflows): 40-100 tries (2-5 minutes)

### 2. Error Handling

Always check `result.isSuccess()` before accessing task results:

```java
if (result.isSuccess()) {
    // Process result
} else {
    // Handle error
    logger.error("Task failed: {}", result.getErrorMessage());
}
```

### 3. Resource Cleanup

Always delete sessions after use to avoid resource leaks:

```java
try {
    // Task execution
} finally {
    if (session != null) {
        agentBay.delete(session, false);
    }
}
```

### 4. Task Descriptions

Write clear, specific task descriptions:

✅ **Good:**
- "Open Notepad, type 'Hello World', and save as hello.txt on Desktop"
- "Go to example.com, fill the search box with 'test', and click submit"

❌ **Bad:**
- "Do something with notepad"
- "Search"

### 5. Status Monitoring

For async tasks, implement proper polling with backoff:

```java
int retries = 0;
int maxRetries = 30;
while (retries < maxRetries) {
    QueryResult status = agent.getTaskStatus(taskId);

    if ("finished".equals(status.getTaskStatus()) ||
        "failed".equals(status.getTaskStatus())) {
        break;
    }

    Thread.sleep(3000);
    retries++;
}
```

---

## Troubleshooting

### Task Timeout

If tasks frequently timeout:
1. Increase `maxTryTimes`
2. Break complex tasks into smaller steps
3. Check session resources (CPU/memory)

### Task Unsupported

If you receive `unsupported` status:
1. Verify the task is within agent capabilities
2. Simplify the task description
3. Use more specific instructions

### Initialization Failed

If browser agent initialization fails:
1. Verify session is using `browser_latest` image
2. Check API key permissions
3. Ensure browser resources are available

---

## Related Documentation

- [Python Agent API](../../../../python/docs/api/sync/agent.md) - Python equivalent
- [Computer Module](./Computer-API.md) - Low-level desktop automation
- [Browser Module](./Browser-API.md) - Low-level browser automation
- [BrowserAgent Module](./BrowserAgent-API.md) - Playwright-based browser agent

---

## See Also

- [AgentExample.java](../src/main/java/com/aliyun/agentbay/examples/AgentExample.java) - Complete working examples
- [TestAgentIntegration.java](../src/test/java/com/aliyun/agentbay/test/TestAgentIntegration.java) - Integration tests
