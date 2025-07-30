package application

import (
	"encoding/json"
	"fmt"
	"net/http"
	"strings"
	"time"

	"github.com/alibabacloud-go/tea/tea"
	mcp "github.com/aliyun/wuying-agentbay-sdk/golang/api/client"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/models"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/utils"
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
		IsVpc() bool
		NetworkInterfaceIp() string
		HttpPort() string
		FindServerForTool(toolName string) string
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

// callMcpTool calls the MCP tool and checks for errors in the response
func (am *ApplicationManager) callMcpTool(toolName string, args interface{}, defaultErrorMsg string) (*callMcpToolHelperResult, error) {
	// Marshal arguments to JSON
	argsJSON, err := json.Marshal(args)
	if err != nil {
		return nil, fmt.Errorf("failed to marshal args: %w", err)
	}

	// Check if this is a VPC session
	if am.Session.IsVpc() {
		return am.callMcpToolVPC(toolName, string(argsJSON), defaultErrorMsg)
	}

	// Non-VPC mode: use traditional API call
	return am.callMcpToolAPI(toolName, string(argsJSON), defaultErrorMsg)
}

// callMcpToolVPC handles VPC-based MCP tool calls
func (am *ApplicationManager) callMcpToolVPC(toolName, argsJSON, defaultErrorMsg string) (*callMcpToolHelperResult, error) {
	// VPC mode: Use HTTP request to the VPC endpoint
	fmt.Println("API Call: CallMcpTool (VPC) -", toolName)
	fmt.Printf("Request: Args=%s\n", argsJSON)

	// Find server for this tool
	server := am.Session.FindServerForTool(toolName)
	if server == "" {
		return nil, fmt.Errorf("server not found for tool: %s", toolName)
	}

	// Construct VPC URL with query parameters
	baseURL := fmt.Sprintf("http://%s:%s/callTool", am.Session.NetworkInterfaceIp(), am.Session.HttpPort())

	// Create URL with query parameters
	req, err := http.NewRequest("GET", baseURL, nil)
	if err != nil {
		return nil, fmt.Errorf("failed to create VPC HTTP request: %w", err)
	}

	// Add query parameters
	q := req.URL.Query()
	q.Add("server", server)
	q.Add("tool", toolName)
	q.Add("args", argsJSON)
	q.Add("apiKey", am.Session.GetAPIKey())
	req.URL.RawQuery = q.Encode()

	// Set content type header
	req.Header.Set("Content-Type", "application/x-www-form-urlencoded")

	// Send HTTP request
	client := &http.Client{Timeout: 30 * time.Second}
	resp, err := client.Do(req)
	if err != nil {
		sanitizedErr := utils.SanitizeError(err)
		fmt.Println("Error calling VPC CallMcpTool -", toolName, ":", sanitizedErr)
		return nil, fmt.Errorf("failed to call VPC %s: %w", toolName, err)
	}
	defer resp.Body.Close()

	// Parse response
	var responseData map[string]interface{}
	if err := json.NewDecoder(resp.Body).Decode(&responseData); err != nil {
		return nil, fmt.Errorf("failed to decode VPC response: %w", err)
	}

	fmt.Println("Response from VPC CallMcpTool -", toolName, ":", responseData)

	// Create result object for VPC response
	result := &callMcpToolHelperResult{
		Data:       responseData,
		StatusCode: int32(resp.StatusCode),
		RequestID:  "", // VPC requests don't have traditional request IDs
	}

	// Extract the actual result from the nested VPC response structure
	var actualResult map[string]interface{}
	if dataStr, ok := responseData["data"].(string); ok {
		var dataMap map[string]interface{}
		if err := json.Unmarshal([]byte(dataStr), &dataMap); err == nil {
			if resultData, ok := dataMap["result"].(map[string]interface{}); ok {
				actualResult = resultData
			}
		}
	} else if data, ok := responseData["data"].(map[string]interface{}); ok {
		if resultData, ok := data["result"].(map[string]interface{}); ok {
			actualResult = resultData
		}
	}
	if actualResult == nil {
		actualResult = responseData
	}

	// Check if there's an error in the VPC response
	if isError, ok := actualResult["isError"].(bool); ok && isError {
		result.IsError = true
		if errMsg, ok := actualResult["error"].(string); ok {
			result.ErrorMsg = errMsg
			return result, fmt.Errorf("%s", errMsg)
		}
		return result, fmt.Errorf("%s", defaultErrorMsg)
	}

	// Extract content array if it exists for VPC response
	if contentArray, ok := actualResult["content"].([]interface{}); ok {
		result.Content = make([]map[string]interface{}, len(contentArray))
		for i, item := range contentArray {
			if contentItem, ok := item.(map[string]interface{}); ok {
				result.Content[i] = contentItem
				if i == 0 && result.TextContent == "" {
					if text, ok := contentItem["text"].(string); ok {
						result.TextContent = text
					}
				}
			}
		}
	}

	return result, nil
}

// callMcpToolAPI handles traditional API-based MCP tool calls
func (am *ApplicationManager) callMcpToolAPI(toolName, argsJSON, defaultErrorMsg string) (*callMcpToolHelperResult, error) {
	// Create the request
	callToolRequest := &mcp.CallMcpToolRequest{
		Authorization: tea.String("Bearer " + am.Session.GetAPIKey()),
		SessionId:     tea.String(am.Session.GetSessionId()),
		Name:          tea.String(toolName),
		Args:          tea.String(argsJSON),
	}

	// Log API request
	fmt.Println("API Call: CallMcpTool -", toolName)
	fmt.Printf("Request: SessionId=%s, Args=%s\n", *callToolRequest.SessionId, *callToolRequest.Args)

	// Call the MCP tool
	response, err := am.Session.GetClient().CallMcpTool(callToolRequest)

	// Log API response
	if err != nil {
		sanitizedErr := utils.SanitizeError(err)
		fmt.Println("Error calling CallMcpTool -", toolName, ":", sanitizedErr)
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

		// Try to extract the error message from the response
		if errContent, exists := data["content"]; exists {
			if contentArray, isArray := errContent.([]interface{}); isArray && len(contentArray) > 0 {
				if firstContent, isMap := contentArray[0].(map[string]interface{}); isMap {
					if text, exists := firstContent["text"]; exists {
						if textStr, isStr := text.(string); isStr {
							result.ErrorMsg = textStr
							return result, fmt.Errorf("%s", textStr)
						}
					}
				}
			}
		}
		return result, fmt.Errorf("%s", defaultErrorMsg)
	}

	// Extract content array if it exists
	if contentArray, ok := data["content"].([]interface{}); ok {
		result.Content = make([]map[string]interface{}, len(contentArray))
		var textParts []string

		for i, item := range contentArray {
			if contentItem, ok := item.(map[string]interface{}); ok {
				result.Content[i] = contentItem

				// Extract text for TextContent field
				if text, ok := contentItem["text"].(string); ok {
					textParts = append(textParts, text)
				}
			}
		}

		// Join all text parts
		if len(textParts) > 0 {
			result.TextContent = strings.Join(textParts, "\n")
		}
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
	IsVpc() bool
	NetworkInterfaceIp() string
	HttpPort() string
	FindServerForTool(toolName string) string
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
	mcpResult, err := am.callMcpTool("get_installed_apps", args, "error getting installed apps")
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
	mcpResult, err := am.callMcpTool("start_app", args, "error starting app")
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
	mcpResult, err := am.callMcpTool("stop_app_by_pname", args, "error stopping app by process name")
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
	mcpResult, err := am.callMcpTool("stop_app_by_pid", args, "error stopping app by PID")
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
	mcpResult, err := am.callMcpTool("stop_app_by_cmd", args, "error stopping app by command")
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
	mcpResult, err := am.callMcpTool("list_visible_apps", nil, "error listing visible apps")
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
