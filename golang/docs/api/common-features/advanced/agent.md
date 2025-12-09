# Agent API Reference

## 🤖 Related Tutorial

- [Agent Modules Guide](../../../../../docs/guides/common-features/advanced/agent-modules.md) - Learn about agent modules and custom agents

## Type Agent

```go
type Agent struct {
	Browser		*BrowserUseAgent
	Computer	*ComputerUseAgent
}
```

Agent represents an agent to manipulate applications to complete specific tasks

### Related Functions

### NewAgent

```go
func NewAgent(session McpSession) *Agent
```

NewAgent creates a new Agent instance

## Type AgentOptions

```go
type AgentOptions struct {
	UseVision	bool
	OutputSchema	string
}
```

## Type BrowserUseAgent

```go
type BrowserUseAgent struct {
	Session McpSession
}
```

BrowserUseAgent represents an agent to manipulate a browser to complete specific tasks

### Methods

### ExecuteTask

```go
func (a *BrowserUseAgent) ExecuteTask(task string, maxTryTimes int) *ExecutionResult
```

ExecuteTask executes a specific task described in human language

**Example:**

```go
client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
sessionResult, _ := client.Create(agentbay.NewCreateSessionParams().WithImageId("windows_latest"))
defer sessionResult.Session.Delete()
result := sessionResult.Session.Agent.Browser.ExecuteTask("Find weather in NYC", 10)
```

### GetTaskStatus

```go
func (a *BrowserUseAgent) GetTaskStatus(taskID string) *QueryResult
```

GetTaskStatus gets the status of the task with the given task ID

**Example:**

```go
client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
sessionResult, _ := client.Create(agentbay.NewCreateSessionParams().WithImageId("windows_latest"))
defer sessionResult.Session.Delete()
execResult := sessionResult.Session.Agent.Browser.ExecuteTask("Find weather in NYC", 10)
statusResult := sessionResult.Session.Agent.Browser.GetTaskStatus(execResult.TaskID)
```

### Initialize

```go
func (a *BrowserUseAgent) Initialize(option AgentOptions) *InitializationResult
```

### TerminateTask

```go
func (a *BrowserUseAgent) TerminateTask(taskID string) *ExecutionResult
```

TerminateTask terminates a task with a specified task ID

**Example:**

```go
client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
sessionResult, _ := client.Create(agentbay.NewCreateSessionParams().WithImageId("windows_latest"))
defer sessionResult.Session.Delete()
execResult := sessionResult.Session.Agent.Browser.ExecuteTask("Find weather in NYC", 10)
terminateResult := sessionResult.Session.Agent.Browser.TerminateTask(execResult.TaskID)
```

### Related Functions

### NewBrowserUseAgent

```go
func NewBrowserUseAgent(session McpSession) *BrowserUseAgent
```

## Type ComputerUseAgent

```go
type ComputerUseAgent struct {
	Session McpSession
}
```

ComputerUseAgent represents an agent to manipulate a browser to complete specific tasks

### Methods

### ExecuteTask

```go
func (a *ComputerUseAgent) ExecuteTask(task string, maxTryTimes int) *ExecutionResult
```

ExecuteTask executes a specific task described in human language

**Example:**

```go
client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
sessionResult, _ := client.Create(agentbay.NewCreateSessionParams().WithImageId("windows_latest"))
defer sessionResult.Session.Delete()
result := sessionResult.Session.Agent.Computer.ExecuteTask("Find weather in NYC", 10)
```

### GetTaskStatus

```go
func (a *ComputerUseAgent) GetTaskStatus(taskID string) *QueryResult
```

GetTaskStatus gets the status of the task with the given task ID

**Example:**

```go
client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
sessionResult, _ := client.Create(agentbay.NewCreateSessionParams().WithImageId("windows_latest"))
defer sessionResult.Session.Delete()
execResult := sessionResult.Session.Agent.Computer.ExecuteTask("Find weather in NYC", 10)
statusResult := sessionResult.Session.Agent.Computer.GetTaskStatus(execResult.TaskID)
```

### TerminateTask

```go
func (a *ComputerUseAgent) TerminateTask(taskID string) *ExecutionResult
```

TerminateTask terminates a task with a specified task ID

**Example:**

```go
client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
sessionResult, _ := client.Create(agentbay.NewCreateSessionParams().WithImageId("windows_latest"))
defer sessionResult.Session.Delete()
execResult := sessionResult.Session.Agent.Computer.ExecuteTask("Find weather in NYC", 10)
terminateResult := sessionResult.Session.Agent.Computer.TerminateTask(execResult.TaskID)
```

### Related Functions

### NewComputerUseAgent

```go
func NewComputerUseAgent(session McpSession) *ComputerUseAgent
```

## Type ExecutionResult

```go
type ExecutionResult struct {
	models.ApiResponse
	Success		bool	`json:"success"`
	ErrorMessage	string	`json:"error_message"`
	TaskID		string	`json:"task_id"`
	TaskStatus	string	`json:"task_status"`
	TaskResult	string	`json:"task_result"`
}
```

ExecutionResult represents the result of task execution

## Type InitializationResult

```go
type InitializationResult struct {
	models.ApiResponse
	Success	bool	`json:"success"`
}
```

InitializationResult represents the result of agent initialization

## Type McpSession

```go
type McpSession interface {
	GetAPIKey() string
	GetSessionId() string
	CallMcpTool(toolName string, args interface{}, autoGenSession ...bool) (*models.McpToolResult, error)
}
```

McpSession interface defines the methods needed by Agent

## Type QueryResult

```go
type QueryResult struct {
	models.ApiResponse
	Success		bool	`json:"success"`
	ErrorMessage	string	`json:"error_message"`
	TaskID		string	`json:"task_id"`
	TaskStatus	string	`json:"task_status"`
	TaskAction	string	`json:"task_action"`
	TaskProduct	string	`json:"task_product"`
}
```

QueryResult represents the result of query operations

## Related Resources

- [Session API Reference](../basics/session.md)

---

*Documentation generated automatically from Go source code.*
