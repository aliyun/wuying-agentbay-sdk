# Agent Module Usage Guide

This document provides comprehensive guidance on using the Agent module of the AgentBay SDK across all supported languages. The Agent module enables AI-powered task execution within cloud sessions using natural language descriptions.

## Overview

The Agent module allows developers to execute complex tasks using human-readable instructions, monitor task status, and terminate running tasks. This capability extends the functionality of cloud sessions by adding AI-powered automation.

## Getting Started

### Prerequisites

To use the Agent module, you need:
1. AgentBay SDK installed for your preferred language
2. Valid API key
3. Understanding of session management concepts

### Creating a Session with Agent Capabilities

The Agent module is automatically available on all sessions created with the AgentBay SDK:

```python
from agentbay import AgentBay

# Initialize the SDK
agent_bay = AgentBay(api_key="your_api_key")

# Create a session
session_result = agent_bay.create()
if session_result.success:
    session = session_result.session
    print(f"Session created with ID: {session.session_id}")
    # The Agent module is now accessible via session.agent
```

```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

// Initialize the SDK
const agentBay = new AgentBay({ apiKey: 'your_api_key' });

// Create a session
async function createSession() {
  const sessionResult = await agentBay.create();
  if (sessionResult.success) {
    const session = sessionResult.session;
    console.log(`Session created with ID: ${session.sessionId}`);
    // The Agent module is now accessible via session.agent
    return session;
  }
}
```

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
    fmt.Printf("Session created with ID: %s\n", session.SessionID)
    // The Agent module is now accessible via session.Agent
}
```

## Executing Tasks

The primary function of the Agent module is to execute tasks described in natural language:

```python
# Execute a task using the Agent
task_description = "Find the current weather in New York City"
execution_result = session.agent.execute_task(task_description, max_try_times=10)

if execution_result.success:
    print(f"Task completed successfully with status: {execution_result.task_status}")
    print(f"Task ID: {execution_result.task_id}")
else:
    print(f"Task failed: {execution_result.error_message}")
```

```typescript
// Execute a task using the Agent
async function executeAgentTask() {
  const taskDescription = "Find the current weather in New York City";
  const executionResult = await session.agent.executeTask(taskDescription, 10);

  if (executionResult.success) {
    console.log(`Task completed successfully with status: ${executionResult.taskStatus}`);
    console.log(`Task ID: ${executionResult.taskId}`);
  } else {
    console.log(`Task failed: ${executionResult.errorMessage}`);
  }
}
```

```go
// Execute a task using the Agent
taskDescription := "Find the current weather in New York City"
executionResult := session.Agent.ExecuteTask(taskDescription, 10)

if executionResult.Success {
    fmt.Printf("Task completed successfully with status: %s\n", executionResult.TaskStatus)
    fmt.Printf("Task ID: %s\n", executionResult.TaskID)
} else {
    fmt.Printf("Task failed: %s\n", executionResult.ErrorMessage)
}
```

## Monitoring Task Status

You can check the status of a specific task using its task ID:

```python
# Get the status of a specific task
task_id = "task_12345"
status_result = session.agent.get_task_status(task_id)

if status_result.success:
    print(f"Task output: {status_result.output}")
else:
    print(f"Failed to get task status: {status_result.error_message}")
```

```typescript
// Get the status of a specific task
async function checkTaskStatus(taskId: string) {
  const statusResult = await session.agent.getTaskStatus(taskId);
  
  if (statusResult.success) {
    console.log(`Task output: ${statusResult.output}`);
  } else {
    console.log(`Failed to get task status: ${statusResult.errorMessage}`);
  }
}
```

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

## Terminating Tasks

You can terminate running tasks when needed:

```python
# Terminate a running task
task_id = "task_12345"
terminate_result = session.agent.terminate_task(task_id)

if terminate_result.success:
    print(f"Task terminated successfully with status: {terminate_result.task_status}")
else:
    print(f"Failed to terminate task: {terminate_result.error_message}")
```

```typescript
// Terminate a running task
async function terminateAgentTask(taskId: string) {
  const terminateResult = await session.agent.terminateTask(taskId);
  
  if (terminateResult.success) {
    console.log(`Task terminated successfully with status: ${terminateResult.taskStatus}`);
  } else {
    console.log(`Failed to terminate task: ${terminateResult.errorMessage}`);
  }
}
```

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

## Best Practices

1. **Task Descriptions**:
   - Use clear and specific natural language descriptions
   - Include relevant context for complex tasks
   - Break down complex workflows into smaller tasks when possible

2. **Error Handling**:
   - Always check the return results of Agent operations
   - Handle potential errors gracefully
   - Implement retry logic for transient failures

3. **Task Monitoring**:
   - Monitor long-running tasks periodically
   - Set appropriate timeout values
   - Implement proper cleanup for terminated tasks

4. **Resource Management**:
   - Terminate tasks that are no longer needed
   - Handle task completion in a timely manner
   - Avoid creating excessive concurrent tasks

5. **Performance Optimization**:
   - Use appropriate max_try_times values based on task complexity
   - Implement efficient polling intervals
   - Batch related tasks when possible

## Limitations

1. **Task Complexity**: Very complex or ambiguous tasks may fail or produce unexpected results
2. **Execution Time**: Tasks are subject to timeout limits
3. **Resource Constraints**: Task execution is subject to cloud resource limitations
4. **Language Support**: Task descriptions should be in supported languages

## Troubleshooting

### Common Issues

1. **Task Execution Failures**:
   - Verify the task description is clear and specific
   - Check if the task is supported by the system
   - Review error messages for specific failure reasons

2. **Status Polling Issues**:
   - Ensure the task ID is valid
   - Check network connectivity
   - Verify the session is still active

3. **Task Termination Failures**:
   - Confirm the task is still running
   - Check if the task supports termination
   - Review error messages for specific failure reasons

4. **Timeout Issues**:
   - Increase max_try_times for long-running tasks
   - Break complex tasks into smaller subtasks
   - Optimize task descriptions for efficiency

## Integration with Other Modules

The Agent module can be combined with other session capabilities:

1. **FileSystem Operations**: Tasks can include file operations
2. **Command Execution**: Tasks can execute shell commands
3. **Code Execution**: Tasks can run code in various languages
4. **UI Interaction**: Tasks can interact with user interfaces
5. **Browser Automation**: Tasks can control web browsers (Python/TypeScript)

## API Reference

For detailed API documentation, see:
- [Python Agent API](../api-reference/python/agent.md)
- [TypeScript Agent API](../api-reference/typescript/agent.md)
- [Golang Agent API](../api-reference/golang/agent.md)