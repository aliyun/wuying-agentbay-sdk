package agent

import (
	"encoding/json"
	"fmt"
	"time"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/models"
)

// ExecutionResult represents the result of task execution
type ExecutionResult struct {
	models.ApiResponse
	Success      bool   `json:"success"`
	ErrorMessage string `json:"error_message"`
	TaskID       string `json:"task_id"`
	TaskStatus   string `json:"task_status"`
	TaskResult   string `json:"task_result"`
}

// QueryResult represents the result of query operations
type QueryResult struct {
	models.ApiResponse
	Success      bool   `json:"success"`
	ErrorMessage string `json:"error_message"`
	TaskID       string `json:"task_id"`
	TaskStatus   string `json:"task_status"`
	TaskAction   string `json:"task_action"`
	TaskProduct  string `json:"task_product"`
}

// InitializationResult represents the result of agent initialization
type InitializationResult struct {
	models.ApiResponse
	Success bool `json:"success"`
}

// Options for configuring the agent.
// Args:
// use_vision (bool): Whether to use vision to perform actions.
// output_schema(dict): User-defined output schema for the agent's results.

type AgentOptions struct {
	UseVision    bool
	OutputSchema string
}

// ComputerUseAgent represents an agent to manipulate a browser to complete specific tasks
type ComputerUseAgent struct {
	Session McpSession
}

// BrowserUseAgent represents an agent to manipulate a browser to complete specific tasks
type BrowserUseAgent struct {
	Session McpSession
}

// Agent represents an agent to manipulate applications to complete specific tasks
type Agent struct {
	Browser  *BrowserUseAgent
	Computer *ComputerUseAgent
}

// McpSession interface defines the methods needed by Agent
type McpSession interface {
	GetAPIKey() string
	GetSessionId() string
	CallMcpTool(toolName string, args interface{}, autoGenSession ...bool) (*models.McpToolResult, error)
}

func NewBrowserUseAgent(session McpSession) *BrowserUseAgent {
	return &BrowserUseAgent{
		Session: session,
	}
}

func NewComputerUseAgent(session McpSession) *ComputerUseAgent {
	return &ComputerUseAgent{
		Session: session,
	}
}

// NewAgent creates a new Agent instance
func NewAgent(session McpSession) *Agent {
	return &Agent{
		Browser:  NewBrowserUseAgent(session),
		Computer: NewComputerUseAgent(session),
	}
}

// ExecuteTask executes a specific task described in human language
//
// Example:
//
//	client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
//	sessionResult, _ := client.Create(agentbay.NewCreateSessionParams().WithImageId("windows_latest"))
//	defer sessionResult.Session.Delete()
//	result := sessionResult.Session.Agent.Computer.ExecuteTask("Find weather in NYC", 10)
func (a *ComputerUseAgent) ExecuteTask(task string, maxTryTimes int) *ExecutionResult {
	args := map[string]interface{}{
		"task": task,
	}

	result, err := a.Session.CallMcpTool("flux_execute_task", args)
	if err != nil {
		return &ExecutionResult{
			ApiResponse:  models.ApiResponse{RequestID: ""},
			Success:      false,
			ErrorMessage: fmt.Sprintf("Failed to execute: %v", err),
			TaskStatus:   "failed",
			TaskID:       "",
		}
	}

	if !result.Success {
		return &ExecutionResult{
			ApiResponse:  models.ApiResponse{RequestID: result.RequestID},
			Success:      false,
			ErrorMessage: result.ErrorMessage,
			TaskStatus:   "failed",
			TaskID:       "",
		}
	}

	// Parse task ID from response
	var content map[string]interface{}
	if err := json.Unmarshal([]byte(result.Data), &content); err != nil {
		return &ExecutionResult{
			ApiResponse:  models.ApiResponse{RequestID: result.RequestID},
			Success:      false,
			ErrorMessage: fmt.Sprintf("Failed to parse response: %v", err),
			TaskStatus:   "failed",
			TaskID:       "",
		}
	}

	taskID, ok := content["task_id"].(string)
	if !ok {
		return &ExecutionResult{
			ApiResponse:  models.ApiResponse{RequestID: result.RequestID},
			Success:      false,
			ErrorMessage: "Task ID not found in response",
			TaskStatus:   "failed",
			TaskID:       "",
		}
	}

	// Poll for task completion
	triedTime := 0
	for triedTime < maxTryTimes {
		query := a.GetTaskStatus(taskID)
		if !query.Success {
			return &ExecutionResult{
				ApiResponse:  models.ApiResponse{RequestID: result.RequestID},
				Success:      false,
				ErrorMessage: query.ErrorMessage,
				TaskStatus:   "failed",
				TaskID:       taskID,
			}
		}

		taskStatus := query.TaskStatus
		switch taskStatus {
		case "finished":
			return &ExecutionResult{
				ApiResponse:  models.ApiResponse{RequestID: result.RequestID},
				Success:      true,
				ErrorMessage: "",
				TaskID:       taskID,
				TaskStatus:   taskStatus,
				TaskResult:   query.TaskProduct,
			}
		case "failed":
			return &ExecutionResult{
				ApiResponse:  models.ApiResponse{RequestID: result.RequestID},
				Success:      false,
				ErrorMessage: "Failed to execute task.",
				TaskID:       taskID,
				TaskStatus:   taskStatus,
				TaskResult:   query.TaskProduct,
			}
		case "unsupported":
			return &ExecutionResult{
				ApiResponse:  models.ApiResponse{RequestID: result.RequestID},
				Success:      false,
				ErrorMessage: "Unsupported task.",
				TaskID:       taskID,
				TaskStatus:   taskStatus,
				TaskResult:   query.TaskProduct,
			}
		}

		fmt.Printf("Task %s is still running, please wait for a while.\n", taskID)
		time.Sleep(3 * time.Second)
		triedTime++
	}

	return &ExecutionResult{
		ApiResponse:  models.ApiResponse{RequestID: result.RequestID},
		Success:      false,
		ErrorMessage: "Task execution timed out",
		TaskStatus:   "timeout",
		TaskID:       taskID,
		TaskResult:   "",
	}
}

// GetTaskStatus gets the status of the task with the given task ID
//
// Example:
//
//	client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
//	sessionResult, _ := client.Create(agentbay.NewCreateSessionParams().WithImageId("windows_latest"))
//	defer sessionResult.Session.Delete()
//	execResult := sessionResult.Session.Agent.Computer.ExecuteTask("Find weather in NYC", 10)
//	statusResult := sessionResult.Session.Agent.Computer.GetTaskStatus(execResult.TaskID)
func (a *ComputerUseAgent) GetTaskStatus(taskID string) *QueryResult {
	args := map[string]interface{}{
		"task_id": taskID,
	}

	result, err := a.Session.CallMcpTool("flux_get_task_status", args)
	if err != nil {
		return &QueryResult{
			ApiResponse:  models.ApiResponse{RequestID: ""},
			Success:      false,
			ErrorMessage: fmt.Sprintf("Failed to get task status: %v", err),
			TaskStatus:   "failed",
		}
	}

	if !result.Success {
		return &QueryResult{
			ApiResponse:  models.ApiResponse{RequestID: result.RequestID},
			Success:      false,
			ErrorMessage: result.ErrorMessage,
			TaskStatus:   "failed",
		}
	}
	var queryResult map[string]interface{}
	if err := json.Unmarshal([]byte(result.Data), &queryResult); err != nil {
		return &QueryResult{
			ApiResponse:  models.ApiResponse{RequestID: result.RequestID},
			Success:      false,
			ErrorMessage: fmt.Sprintf("Failed to parse response: %v", err),
			TaskStatus:   "failed",
		}
	}
	product, success := queryResult["product"].(string)
	var TaskProduct = product
	if !success {
		TaskProduct = ""
	}
	return &QueryResult{
		ApiResponse: models.ApiResponse{RequestID: result.RequestID},
		Success:     true,
		TaskID:      queryResult["task_id"].(string),
		TaskStatus:  queryResult["status"].(string),
		TaskProduct: TaskProduct,
	}
}

// TerminateTask terminates a task with a specified task ID
//
// Example:
//
//	client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
//	sessionResult, _ := client.Create(agentbay.NewCreateSessionParams().WithImageId("windows_latest"))
//	defer sessionResult.Session.Delete()
//	execResult := sessionResult.Session.Agent.Computer.ExecuteTask("Find weather in NYC", 10)
//	terminateResult := sessionResult.Session.Agent.Computer.TerminateTask(execResult.TaskID)
func (a *ComputerUseAgent) TerminateTask(taskID string) *ExecutionResult {
	fmt.Println("Terminating task")

	args := map[string]interface{}{
		"task_id": taskID,
	}

	result, err := a.Session.CallMcpTool("flux_terminate_task", args)
	if err != nil {
		return &ExecutionResult{
			ApiResponse:  models.ApiResponse{RequestID: ""},
			Success:      false,
			ErrorMessage: fmt.Sprintf("Failed to terminate: %v", err),
			TaskID:       taskID,
			TaskStatus:   "failed",
		}
	}

	var content map[string]interface{}
	if err := json.Unmarshal([]byte(result.Data), &content); err != nil {
		return &ExecutionResult{
			ApiResponse:  models.ApiResponse{RequestID: result.RequestID},
			Success:      false,
			ErrorMessage: fmt.Sprintf("Failed to parse response: %v", err),
			TaskID:       taskID,
			TaskStatus:   "failed",
		}
	}

	terminatedTaskID, ok := content["task_id"].(string)
	if !ok {
		terminatedTaskID = taskID
	}

	status, ok := content["status"].(string)
	if !ok {
		status = "unknown"
	}

	if result.Success {
		return &ExecutionResult{
			ApiResponse:  models.ApiResponse{RequestID: result.RequestID},
			Success:      true,
			ErrorMessage: "",
			TaskID:       terminatedTaskID,
			TaskStatus:   status,
		}
	}

	return &ExecutionResult{
		ApiResponse:  models.ApiResponse{RequestID: result.RequestID},
		Success:      false,
		ErrorMessage: result.ErrorMessage,
		TaskID:       terminatedTaskID,
		TaskStatus:   status,
	}
}

func (a *BrowserUseAgent) Initialize(option AgentOptions) *InitializationResult {
	args := map[string]interface{}{
		"use_vision":    option.UseVision,
		"output_schema": option.OutputSchema,
	}
	result, err := a.Session.CallMcpTool("browser_use_initialize", args)
	if err != nil {
		return &InitializationResult{
			ApiResponse: models.ApiResponse{RequestID: ""},
			Success:     false,
		}
	}

	if !result.Success {
		return &InitializationResult{
			ApiResponse: models.ApiResponse{RequestID: result.RequestID},
			Success:     false,
		}
	}

	return &InitializationResult{
		ApiResponse: models.ApiResponse{RequestID: result.RequestID},
		Success:     true,
	}

}

// ExecuteTask executes a specific task described in human language
//
// Example:
//
//	client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
//	sessionResult, _ := client.Create(agentbay.NewCreateSessionParams().WithImageId("windows_latest"))
//	defer sessionResult.Session.Delete()
//	result := sessionResult.Session.Agent.Browser.ExecuteTask("Find weather in NYC", 10)
func (a *BrowserUseAgent) ExecuteTask(task string, maxTryTimes int) *ExecutionResult {
	args := map[string]interface{}{
		"task": task,
	}

	result, err := a.Session.CallMcpTool("browser_use_execute_task", args)
	if err != nil {
		return &ExecutionResult{
			ApiResponse:  models.ApiResponse{RequestID: ""},
			Success:      false,
			ErrorMessage: fmt.Sprintf("Failed to execute: %v", err),
			TaskStatus:   "failed",
			TaskID:       "",
		}
	}

	if !result.Success {
		return &ExecutionResult{
			ApiResponse:  models.ApiResponse{RequestID: result.RequestID},
			Success:      false,
			ErrorMessage: result.ErrorMessage,
			TaskStatus:   "failed",
			TaskID:       "",
		}
	}

	// Parse task ID from response
	var content map[string]interface{}
	if err := json.Unmarshal([]byte(result.Data), &content); err != nil {
		return &ExecutionResult{
			ApiResponse:  models.ApiResponse{RequestID: result.RequestID},
			Success:      false,
			ErrorMessage: fmt.Sprintf("Failed to parse response: %v", err),
			TaskStatus:   "failed",
			TaskID:       "",
		}
	}

	taskID, ok := content["task_id"].(string)
	if !ok {
		return &ExecutionResult{
			ApiResponse:  models.ApiResponse{RequestID: result.RequestID},
			Success:      false,
			ErrorMessage: "Task ID not found in response",
			TaskStatus:   "failed",
			TaskID:       "",
		}
	}

	// Poll for task completion
	triedTime := 0
	for triedTime < maxTryTimes {
		query := a.GetTaskStatus(taskID)
		if !query.Success {
			return &ExecutionResult{
				ApiResponse:  models.ApiResponse{RequestID: result.RequestID},
				Success:      false,
				ErrorMessage: query.ErrorMessage,
				TaskStatus:   "failed",
				TaskID:       taskID,
			}
		}

		taskStatus := query.TaskStatus
		switch taskStatus {
		case "finished":
			return &ExecutionResult{
				ApiResponse:  models.ApiResponse{RequestID: result.RequestID},
				Success:      true,
				ErrorMessage: "",
				TaskID:       taskID,
				TaskStatus:   taskStatus,
				TaskResult:   query.TaskProduct,
			}
		case "failed":
			return &ExecutionResult{
				ApiResponse:  models.ApiResponse{RequestID: result.RequestID},
				Success:      false,
				ErrorMessage: "Failed to execute task.",
				TaskID:       taskID,
				TaskStatus:   taskStatus,
				TaskResult:   query.TaskProduct,
			}
		case "unsupported":
			return &ExecutionResult{
				ApiResponse:  models.ApiResponse{RequestID: result.RequestID},
				Success:      false,
				ErrorMessage: "Unsupported task.",
				TaskID:       taskID,
				TaskStatus:   taskStatus,
				TaskResult:   query.TaskProduct,
			}
		}

		fmt.Printf("Task %s is still running, please wait for a while.\n", taskID)
		time.Sleep(3 * time.Second)
		triedTime++
	}

	return &ExecutionResult{
		ApiResponse:  models.ApiResponse{RequestID: result.RequestID},
		Success:      false,
		ErrorMessage: "Task execution timed out",
		TaskStatus:   "timeout",
		TaskID:       taskID,
		TaskResult:   "",
	}
}

// GetTaskStatus gets the status of the task with the given task ID
//
// Example:
//
//	client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
//	sessionResult, _ := client.Create(agentbay.NewCreateSessionParams().WithImageId("windows_latest"))
//	defer sessionResult.Session.Delete()
//	execResult := sessionResult.Session.Agent.Browser.ExecuteTask("Find weather in NYC", 10)
//	statusResult := sessionResult.Session.Agent.Browser.GetTaskStatus(execResult.TaskID)
func (a *BrowserUseAgent) GetTaskStatus(taskID string) *QueryResult {
	args := map[string]interface{}{
		"task_id": taskID,
	}

	result, err := a.Session.CallMcpTool("browser_use_get_task_status", args)
	if err != nil {
		return &QueryResult{
			ApiResponse:  models.ApiResponse{RequestID: ""},
			Success:      false,
			ErrorMessage: fmt.Sprintf("Failed to get task status: %v", err),
			TaskStatus:   "failed",
		}
	}

	if !result.Success {
		return &QueryResult{
			ApiResponse:  models.ApiResponse{RequestID: result.RequestID},
			Success:      false,
			ErrorMessage: result.ErrorMessage,
			TaskStatus:   "failed",
		}
	}
	var queryResult map[string]interface{}
	if err := json.Unmarshal([]byte(result.Data), &queryResult); err != nil {
		return &QueryResult{
			ApiResponse:  models.ApiResponse{RequestID: result.RequestID},
			Success:      false,
			ErrorMessage: fmt.Sprintf("Failed to parse response: %v", err),
			TaskStatus:   "failed",
		}
	}
	product, success := queryResult["product"].(string)
	var TaskProduct = product
	if !success {
		TaskProduct = ""
	}
	return &QueryResult{
		ApiResponse: models.ApiResponse{RequestID: result.RequestID},
		Success:     true,
		TaskID:      queryResult["task_id"].(string),
		TaskStatus:  queryResult["status"].(string),
		TaskProduct: TaskProduct,
	}
}

// TerminateTask terminates a task with a specified task ID
//
// Example:
//
//	client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
//	sessionResult, _ := client.Create(agentbay.NewCreateSessionParams().WithImageId("windows_latest"))
//	defer sessionResult.Session.Delete()
//	execResult := sessionResult.Session.Agent.Browser.ExecuteTask("Find weather in NYC", 10)
//	terminateResult := sessionResult.Session.Agent.Browser.TerminateTask(execResult.TaskID)
func (a *BrowserUseAgent) TerminateTask(taskID string) *ExecutionResult {
	fmt.Println("Terminating task")

	args := map[string]interface{}{
		"task_id": taskID,
	}

	result, err := a.Session.CallMcpTool("browser_use_terminate_task", args)
	if err != nil {
		return &ExecutionResult{
			ApiResponse:  models.ApiResponse{RequestID: ""},
			Success:      false,
			ErrorMessage: fmt.Sprintf("Failed to terminate: %v", err),
			TaskID:       taskID,
			TaskStatus:   "failed",
		}
	}

	var content map[string]interface{}
	if err := json.Unmarshal([]byte(result.Data), &content); err != nil {
		return &ExecutionResult{
			ApiResponse:  models.ApiResponse{RequestID: result.RequestID},
			Success:      false,
			ErrorMessage: fmt.Sprintf("Failed to parse response: %v", err),
			TaskID:       taskID,
			TaskStatus:   "failed",
		}
	}

	terminatedTaskID, ok := content["task_id"].(string)
	if !ok {
		terminatedTaskID = taskID
	}

	status, ok := content["status"].(string)
	if !ok {
		status = "unknown"
	}

	if result.Success {
		return &ExecutionResult{
			ApiResponse:  models.ApiResponse{RequestID: result.RequestID},
			Success:      true,
			ErrorMessage: "",
			TaskID:       terminatedTaskID,
			TaskStatus:   status,
		}
	}

	return &ExecutionResult{
		ApiResponse:  models.ApiResponse{RequestID: result.RequestID},
		Success:      false,
		ErrorMessage: result.ErrorMessage,
		TaskID:       terminatedTaskID,
		TaskStatus:   status,
	}
}
