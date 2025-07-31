# Agent Class API Reference

The `Agent` type provides AI-powered capabilities for executing tasks, checking task status, and terminating tasks within a session. It enables natural language task execution and monitoring.

## Constructor

### NewAgent

```go
func NewAgent(session McpSession) *Agent
```

**Parameters:**
- `session` (McpSession): The Session instance that this Agent belongs to.

**Returns:**
- `*Agent`: A new Agent instance.

## Methods

### ExecuteTask

Executes a specific task described in human language.

```go
ExecuteTask(task string, maxTryTimes int) *ExecutionResult
```

**Parameters:**
- `task` (string): Task description in human language.
- `maxTryTimes` (int): Maximum number of retry attempts.

**Returns:**
- `*ExecutionResult`: Result object containing success status, task ID, task status, and error message if any.

**Example:**
```go
package main

import (
	"fmt"
	"os"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

func main() {
	// Initialize the SDK
	client, err := agentbay.NewAgentBay("your_api_key", nil)
	if err != nil {
		fmt.Printf("Error initializing AgentBay client: %v\n", err)
		os.Exit(1)
	}

	// Create a session
	sessionResult, err := client.Create(nil)
	if err != nil {
		fmt.Printf("Error creating session: %v\n", err)
		os.Exit(1)
	}

	session := sessionResult.Session

	// Execute a task using the Agent
	taskDescription := "Find the current weather in New York City"
	executionResult := session.Agent.ExecuteTask(taskDescription, 10)

	if executionResult.Success {
		fmt.Printf("Task completed successfully with status: %s\n", executionResult.TaskStatus)
		fmt.Printf("Task ID: %s\n", executionResult.TaskID)
	} else {
		fmt.Printf("Task failed: %s\n", executionResult.ErrorMessage)
	}
}
```

### GetTaskStatus

Gets the status of the task with the given task ID.

```go
GetTaskStatus(taskID string) *QueryResult
```

**Parameters:**
- `taskID` (string): Task ID

**Returns:**
- `*QueryResult`: Result object containing success status, output, and error message if any.

**Example:**
```go
// Get the status of a specific task
taskID := "task_12345"
statusResult := session.Agent.GetTaskStatus(taskID)

if statusResult.Success {
	fmt.Printf("Task output: %s\n", statusResult.Output)
} else {
	fmt.Printf("Failed to get task status: %s\n", statusResult.ErrorMessage)
}
```

### TerminateTask

Terminates a task with a specified task ID.

```go
TerminateTask(taskID string) *ExecutionResult
```

**Parameters:**
- `taskID` (string): The ID of the running task.

**Returns:**
- `*ExecutionResult`: Result object containing success status, task ID, task status, and error message if any.

**Example:**
```go
// Terminate a running task
taskID := "task_12345"
terminateResult := session.Agent.TerminateTask(taskID)

if terminateResult.Success {
	fmt.Printf("Task terminated successfully with status: %s\n", terminateResult.TaskStatus)
} else {
	fmt.Printf("Failed to terminate task: %s\n", terminateResult.ErrorMessage)
}
```