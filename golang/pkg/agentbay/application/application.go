package application

import (
	"encoding/json"
	"fmt"
	"strings"

	"github.com/alibabacloud-go/tea/tea"
	mcp "github.com/aliyun/wuying-agentbay-sdk/golang/api/client"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/models"
)

// Application represents an application
type Application struct {
	ID      string `json:"id"`
	Name    string `json:"name"`
	CmdLine string `json:"cmdline,omitempty"`
}

// InstalledApp represents an installed application
type InstalledApp struct {
	Name          string `json:"name"`
	StartCmd      string `json:"start_cmd"`
	StopCmd       string `json:"stop_cmd,omitempty"`
	WorkDirectory string `json:"work_directory,omitempty"`
}

// Process represents a running process
type Process struct {
	PName   string `json:"pname"`
	PID     int    `json:"pid"`
	CmdLine string `json:"cmdline,omitempty"`
}

// ApplicationListResult wraps application list and RequestID
type ApplicationListResult struct {
	models.ApiResponse
	Applications []Application
}

// AppOperationResult wraps application operation result and RequestID
type AppOperationResult struct {
	models.ApiResponse
	Success bool
}

// ProcessListResult wraps process list and RequestID
type ProcessListResult struct {
	models.ApiResponse
	Processes []Process
}

// ApplicationManager handles application management operations in the AgentBay cloud environment.
type ApplicationManager struct {
	Session interface {
		GetAPIKey() string
		GetClient() *mcp.Client
		GetSessionId() string
	}
}

// callMcpToolHelperResult represents the result of a CallMcpTool operation
type callMcpToolHelperResult struct {
	Data        map[string]interface{}
	Content     []map[string]interface{}
	TextContent string
	IsError     bool
	ErrorMsg    string
	StatusCode  int32
	RequestID   string
}

// callMcpToolHelper calls the MCP tool and checks for errors in the response
func (am *ApplicationManager) callMcpToolHelper(toolName string, args interface{}, defaultErrorMsg string) (*callMcpToolHelperResult, error) {
	// Marshal arguments to JSON
	argsJSON, err := json.Marshal(args)
	if err != nil {
		return nil, fmt.Errorf("failed to marshal args: %w", err)
	}

	// Create the request
	callToolRequest := &mcp.CallMcpToolRequest{
		Authorization: tea.String("Bearer " + am.Session.GetAPIKey()),
		SessionId:     tea.String(am.Session.GetSessionId()),
		Name:          tea.String(toolName),
		Args:          tea.String(string(argsJSON)),
	}

	// Log API request
	fmt.Println("API Call: CallMcpTool -", toolName)
	fmt.Printf("Request: SessionId=%s, Args=%s\n", *callToolRequest.SessionId, *callToolRequest.Args)

	// Call the MCP tool
	response, err := am.Session.GetClient().CallMcpTool(callToolRequest)

	// Log API response
	if err != nil {
		fmt.Println("Error calling CallMcpTool -", toolName, ":", err)
		return nil, fmt.Errorf("failed to call %s: %w", toolName, err)
	}
	if response != nil && response.Body != nil {
		fmt.Println("Response from CallMcpTool -", toolName, ":", response.Body)
	}

	// Extract data from response
	data, ok := response.Body.Data.(map[string]interface{})
	if !ok {
		return nil, fmt.Errorf("invalid response data format")
	}

	// Extract RequestID
	var requestID string
	if response != nil && response.Body != nil && response.Body.RequestId != nil {
		requestID = *response.Body.RequestId
	}

	// Create result object
	result := &callMcpToolHelperResult{
		Data:       data,
		StatusCode: *response.StatusCode,
		RequestID:  requestID,
	}

	// Check if there's an error in the response
	//nolint:govet
	isError, ok := data["isError"].(bool)
	if ok && isError {
		result.IsError = true

		// Try to extract the error message from the content field
		//nolint:govet
		contentArray, ok := data["content"].([]interface{})
		if ok && len(contentArray) > 0 {
			// Convert content array to a more usable format
			result.Content = make([]map[string]interface{}, 0, len(contentArray))
			for _, item := range contentArray {
				contentItem, ok := item.(map[string]interface{})
				if !ok {
					continue
				}
				result.Content = append(result.Content, contentItem)
			}

			// Extract error message from the first content item
			if len(result.Content) > 0 {
				//nolint:govet
				text, ok := result.Content[0]["text"].(string)
				if ok {
					result.ErrorMsg = text
					return result, fmt.Errorf("%s", text)
				}
			}
		}
		return result, fmt.Errorf("%s", defaultErrorMsg)
	}

	// Extract content array if it exists
	//nolint:govet
	contentArray, ok := data["content"].([]interface{})
	if ok {
		result.Content = make([]map[string]interface{}, 0, len(contentArray))
		for _, item := range contentArray {
			//nolint:govet
			contentItem, ok := item.(map[string]interface{})
			if !ok {
				continue
			}
			result.Content = append(result.Content, contentItem)
		}

		// Extract text content from the content items
		var textBuilder strings.Builder
		for _, item := range result.Content {
			//nolint:govet
			text, ok := item["text"].(string)
			if !ok {
				continue
			}

			if textBuilder.Len() > 0 {
				textBuilder.WriteString("\n")
			}
			textBuilder.WriteString(text)
		}
		result.TextContent = textBuilder.String()
	}

	return result, nil
}

// parseInstalledAppsFromJSON parses JSON string into array of InstalledApp objects
func parseInstalledAppsFromJSON(jsonStr string) ([]InstalledApp, error) {
	var apps []InstalledApp
	err := json.Unmarshal([]byte(jsonStr), &apps)
	if err != nil {
		return nil, fmt.Errorf("failed to parse applications JSON: %w", err)
	}
	return apps, nil
}

// parseProcessesFromJSON parses JSON string into array of Process objects
func parseProcessesFromJSON(jsonStr string) ([]Process, error) {
	var processes []Process
	err := json.Unmarshal([]byte(jsonStr), &processes)
	if err != nil {
		return nil, fmt.Errorf("failed to parse processes JSON: %w", err)
	}
	return processes, nil
}

// NewApplicationManager creates a new ApplicationManager object.
func NewApplicationManager(session interface {
	GetAPIKey() string
	GetClient() *mcp.Client
	GetSessionId() string
}) *ApplicationManager {
	return &ApplicationManager{
		Session: session,
	}
}

// GetInstalledApps retrieves a list of installed applications.
func (am *ApplicationManager) GetInstalledApps(startMenu bool, desktop bool, ignoreSystemApps bool) (*ApplicationListResult, error) {
	args := map[string]interface{}{
		"start_menu":         startMenu,
		"desktop":            desktop,
		"ignore_system_apps": ignoreSystemApps,
	}

	// Use enhanced helper method to call MCP tool and check for errors
	mcpResult, err := am.callMcpToolHelper("get_installed_apps", args, "error getting installed apps")
	if err != nil {
		return nil, err
	}

	// Parse application list
	installedApps, err := parseInstalledAppsFromJSON(mcpResult.TextContent)
	if err != nil {
		return nil, err
	}

	// Convert to Application type
	var applications []Application
	for _, app := range installedApps {
		applications = append(applications, Application{
			ID:      app.Name, // Use Name as ID
			Name:    app.Name,
			CmdLine: app.StartCmd,
		})
	}

	return &ApplicationListResult{
		ApiResponse: models.ApiResponse{
			RequestID: mcpResult.RequestID,
		},
		Applications: applications,
	}, nil
}

// StartApp starts an application with the given command, optional working directory, and optional activity.
func (am *ApplicationManager) StartApp(startCmd string, workDirectory string, activity string) (*ProcessListResult, error) {
	args := map[string]interface{}{
		"start_cmd": startCmd,
	}
	if workDirectory != "" {
		args["work_directory"] = workDirectory
	}
	if activity != "" {
		args["activity"] = activity
	}

	// 使用增强的辅助方法调用MCP工具并检查错误
	mcpResult, err := am.callMcpToolHelper("start_app", args, "error starting app")
	if err != nil {
		return nil, err
	}

	// 解析进程列表
	processes, err := parseProcessesFromJSON(mcpResult.TextContent)
	if err != nil {
		return nil, err
	}

	return &ProcessListResult{
		ApiResponse: models.ApiResponse{
			RequestID: mcpResult.RequestID,
		},
		Processes: processes,
	}, nil
}

// StopAppByPName stops an application by process name.
func (am *ApplicationManager) StopAppByPName(pname string) (*AppOperationResult, error) {
	args := map[string]string{
		"pname": pname,
	}

	// 使用增强的辅助方法调用MCP工具并检查错误
	mcpResult, err := am.callMcpToolHelper("stop_app_by_pname", args, "error stopping app by process name")
	if err != nil {
		return nil, err
	}

	return &AppOperationResult{
		ApiResponse: models.ApiResponse{
			RequestID: mcpResult.RequestID,
		},
		Success: true,
	}, nil
}

// StopAppByPID stops an application by process ID.
func (am *ApplicationManager) StopAppByPID(pid int) (*AppOperationResult, error) {
	args := map[string]interface{}{
		"pid": pid,
	}

	// 使用增强的辅助方法调用MCP工具并检查错误
	mcpResult, err := am.callMcpToolHelper("stop_app_by_pid", args, "error stopping app by PID")
	if err != nil {
		return nil, err
	}

	return &AppOperationResult{
		ApiResponse: models.ApiResponse{
			RequestID: mcpResult.RequestID,
		},
		Success: true,
	}, nil
}

// StopAppByCmd stops an application by stop command.
func (am *ApplicationManager) StopAppByCmd(stopCmd string) (*AppOperationResult, error) {
	args := map[string]string{
		"stop_cmd": stopCmd,
	}

	// 使用增强的辅助方法调用MCP工具并检查错误
	mcpResult, err := am.callMcpToolHelper("stop_app_by_cmd", args, "error stopping app by command")
	if err != nil {
		return nil, err
	}

	return &AppOperationResult{
		ApiResponse: models.ApiResponse{
			RequestID: mcpResult.RequestID,
		},
		Success: true,
	}, nil
}

// ListVisibleApps returns a list of currently visible applications.
func (am *ApplicationManager) ListVisibleApps() (*ProcessListResult, error) {
	// 使用增强的辅助方法调用MCP工具并检查错误
	mcpResult, err := am.callMcpToolHelper("list_visible_apps", nil, "error listing visible apps")
	if err != nil {
		return nil, err
	}

	// 解析进程列表
	processes, err := parseProcessesFromJSON(mcpResult.TextContent)
	if err != nil {
		return nil, err
	}

	return &ProcessListResult{
		ApiResponse: models.ApiResponse{
			RequestID: mcpResult.RequestID,
		},
		Processes: processes,
	}, nil
}
