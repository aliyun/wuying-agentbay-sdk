package window

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

// ApiResponse is the base class for all API responses, containing RequestID
type ApiResponse struct {
	RequestID string
}

// GetRequestID returns the RequestID of the API call
func (r *ApiResponse) GetRequestID() string {
	return r.RequestID
}

// WindowResult wraps window operation result and RequestID
type WindowResult struct {
	models.ApiResponse
	Success bool
}

// WindowListResult wraps window list and RequestID
type WindowListResult struct {
	models.ApiResponse
	Windows []Window
}

// WindowDetailResult wraps single window information and RequestID
type WindowDetailResult struct {
	models.ApiResponse
	Window *Window
}

// Window represents a window in the system
type Window struct {
	WindowID           int      `json:"window_id"`
	Title              string   `json:"title"`
	AbsoluteUpperLeftX int      `json:"absolute_upper_left_x,omitempty"`
	AbsoluteUpperLeftY int      `json:"absolute_upper_left_y,omitempty"`
	Width              int      `json:"width,omitempty"`
	Height             int      `json:"height,omitempty"`
	PID                int      `json:"pid,omitempty"`
	PName              string   `json:"pname,omitempty"`
	ChildWindows       []Window `json:"child_windows,omitempty"`
}

// WindowManager handles window management operations in the AgentBay cloud environment.
type WindowManager struct {
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

// callMcpToolResult represents the result of a CallMcpTool operation
type callMcpToolResult struct {
	TextContent string
	Data        map[string]interface{}
	IsError     bool
	ErrorMsg    string
	StatusCode  int32
	RequestID   string
	Content     []map[string]interface{}
}

// callMcpTool calls the MCP tool and checks for errors in the response
func (wm *WindowManager) callMcpTool(toolName string, args interface{}, defaultErrorMsg string) (*callMcpToolResult, error) {
	// Marshal arguments to JSON
	argsJSON, err := json.Marshal(args)
	if err != nil {
		return nil, fmt.Errorf("failed to marshal args: %w", err)
	}

	// Check if this is a VPC session
	if wm.Session.IsVpc() {
		return wm.callMcpToolVPC(toolName, string(argsJSON), defaultErrorMsg)
	}

	// Non-VPC mode: use traditional API call
	return wm.callMcpToolAPI(toolName, string(argsJSON), defaultErrorMsg)
}

// callMcpToolVPC handles VPC-based MCP tool calls
func (wm *WindowManager) callMcpToolVPC(toolName, argsJSON, defaultErrorMsg string) (*callMcpToolResult, error) {
	// VPC mode: Use HTTP request to the VPC endpoint
	fmt.Println("API Call: CallMcpTool (VPC) -", toolName)
	fmt.Printf("Request: Args=%s\n", argsJSON)

	// Find server for this tool
	server := wm.Session.FindServerForTool(toolName)
	if server == "" {
		return nil, fmt.Errorf("server not found for tool: %s", toolName)
	}

	// Construct VPC URL with query parameters
	baseURL := fmt.Sprintf("http://%s:%s/callTool", wm.Session.NetworkInterfaceIp(), wm.Session.HttpPort())

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
	q.Add("apiKey", wm.Session.GetAPIKey())
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
	result := &callMcpToolResult{
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
func (wm *WindowManager) callMcpToolAPI(toolName, argsJSON, defaultErrorMsg string) (*callMcpToolResult, error) {
	// Create the request
	callToolRequest := &mcp.CallMcpToolRequest{
		Authorization: tea.String("Bearer " + wm.Session.GetAPIKey()),
		SessionId:     tea.String(wm.Session.GetSessionId()),
		Name:          tea.String(toolName),
		Args:          tea.String(argsJSON),
	}

	// Log API request
	fmt.Println("API Call: CallMcpTool -", toolName)
	fmt.Printf("Request: SessionId=%s, Args=%s\n", *callToolRequest.SessionId, *callToolRequest.Args)

	// Call the MCP tool
	response, err := wm.Session.GetClient().CallMcpTool(callToolRequest)
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
	result := &callMcpToolResult{
		Data:       data,
		StatusCode: *response.StatusCode,
		RequestID:  requestID,
	}

	// Check if there's an error in the response
	isError, ok := data["isError"].(bool)
	if ok && isError {
		result.IsError = true

		// Try to extract the error message from the content field
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

	// Extract text content from response
	if contentArray, ok := data["content"].([]interface{}); ok {
		var textParts []string
		for _, item := range contentArray {
			if contentItem, ok := item.(map[string]interface{}); ok {
				if text, ok := contentItem["text"].(string); ok {
					textParts = append(textParts, text)
				}
			}
		}
		if len(textParts) > 0 {
			result.TextContent = strings.Join(textParts, "\n")
		}
	}

	return result, nil
}

// NewWindowManager creates a new WindowManager object.
func NewWindowManager(session interface {
	GetAPIKey() string
	GetClient() *mcp.Client
	GetSessionId() string
	IsVpc() bool
	NetworkInterfaceIp() string
	HttpPort() string
	FindServerForTool(toolName string) string
}) *WindowManager {
	return &WindowManager{
		Session: session,
	}
}

// ListRootWindows lists all root windows in the system.
func (wm *WindowManager) ListRootWindows() (*WindowListResult, error) {
	args := map[string]interface{}{}

	// Use the helper method to call MCP tool and check for errors
	mcpResult, err := wm.callMcpTool("list_root_windows", args, "error listing root windows")
	if err != nil {
		return nil, err
	}

	// Parse the JSON data into Window objects
	var windows []Window
	err = json.Unmarshal([]byte(mcpResult.TextContent), &windows)
	if err != nil {
		return nil, fmt.Errorf("failed to parse window data: %w", err)
	}

	return &WindowListResult{
		ApiResponse: models.ApiResponse{
			RequestID: mcpResult.RequestID,
		},
		Windows: windows,
	}, nil
}

// GetActiveWindow gets the currently active window.
func (wm *WindowManager) GetActiveWindow() (*WindowDetailResult, error) {
	args := map[string]interface{}{}

	// Use the helper method to call MCP tool and check for errors
	mcpResult, err := wm.callMcpTool("get_active_window", args, "error getting active window")
	if err != nil {
		return nil, err
	}

	// Parse the JSON data into a Window object
	var window Window
	err = json.Unmarshal([]byte(mcpResult.TextContent), &window)
	if err != nil {
		return nil, fmt.Errorf("failed to parse window data: %w", err)
	}

	return &WindowDetailResult{
		ApiResponse: models.ApiResponse{
			RequestID: mcpResult.RequestID,
		},
		Window: &window,
	}, nil
}

// ActivateWindow activates a window with the specified window ID.
func (wm *WindowManager) ActivateWindow(windowID int) (*WindowResult, error) {
	args := map[string]interface{}{
		"window_id": windowID,
	}

	// Use the helper method to call MCP tool and check for errors
	mcpResult, err := wm.callMcpTool("activate_window", args, "error activating window")
	if err != nil {
		return nil, err
	}

	return &WindowResult{
		ApiResponse: models.ApiResponse{
			RequestID: mcpResult.RequestID,
		},
		Success: true,
	}, nil
}

// MaximizeWindow maximizes a window with the specified window ID.
func (wm *WindowManager) MaximizeWindow(windowID int) (*WindowResult, error) {
	args := map[string]interface{}{
		"window_id": windowID,
	}

	// Use the helper method to call MCP tool and check for errors
	mcpResult, err := wm.callMcpTool("maximize_window", args, "error maximizing window")
	if err != nil {
		return nil, err
	}

	return &WindowResult{
		ApiResponse: models.ApiResponse{
			RequestID: mcpResult.RequestID,
		},
		Success: true,
	}, nil
}

// MinimizeWindow minimizes a window with the specified window ID.
func (wm *WindowManager) MinimizeWindow(windowID int) (*WindowResult, error) {
	args := map[string]interface{}{
		"window_id": windowID,
	}

	// Use the helper method to call MCP tool and check for errors
	mcpResult, err := wm.callMcpTool("minimize_window", args, "error minimizing window")
	if err != nil {
		return nil, err
	}

	return &WindowResult{
		ApiResponse: models.ApiResponse{
			RequestID: mcpResult.RequestID,
		},
		Success: true,
	}, nil
}

// RestoreWindow restores a window with the specified window ID.
func (wm *WindowManager) RestoreWindow(windowID int) (*WindowResult, error) {
	args := map[string]interface{}{
		"window_id": windowID,
	}

	// Use the helper method to call MCP tool and check for errors
	mcpResult, err := wm.callMcpTool("restore_window", args, "error restoring window")
	if err != nil {
		return nil, err
	}

	return &WindowResult{
		ApiResponse: models.ApiResponse{
			RequestID: mcpResult.RequestID,
		},
		Success: true,
	}, nil
}

// CloseWindow closes a window with the specified window ID.
func (wm *WindowManager) CloseWindow(windowID int) (*WindowResult, error) {
	args := map[string]interface{}{
		"window_id": windowID,
	}

	// Use the helper method to call MCP tool and check for errors
	mcpResult, err := wm.callMcpTool("close_window", args, "error closing window")
	if err != nil {
		return nil, err
	}

	return &WindowResult{
		ApiResponse: models.ApiResponse{
			RequestID: mcpResult.RequestID,
		},
		Success: true,
	}, nil
}

// FullscreenWindow toggles fullscreen mode for a window with the specified window ID.
func (wm *WindowManager) FullscreenWindow(windowID int) (*WindowResult, error) {
	args := map[string]interface{}{
		"window_id": windowID,
	}

	// Use the helper method to call MCP tool and check for errors
	mcpResult, err := wm.callMcpTool("fullscreen_window", args, "error toggling fullscreen mode")
	if err != nil {
		return nil, err
	}

	return &WindowResult{
		ApiResponse: models.ApiResponse{
			RequestID: mcpResult.RequestID,
		},
		Success: true,
	}, nil
}

// ResizeWindow resizes a window by ID.
func (wm *WindowManager) ResizeWindow(windowID int, width int, height int) (*WindowResult, error) {
	args := map[string]interface{}{
		"window_id": windowID,
		"width":     width,
		"height":    height,
	}

	// Use the helper method to call MCP tool and check for errors
	mcpResult, err := wm.callMcpTool("resize_window", args, "error resizing window")
	if err != nil {
		return nil, err
	}

	// Return result with RequestID
	return &WindowResult{
		ApiResponse: models.ApiResponse{
			RequestID: mcpResult.RequestID,
		},
		Success: true,
	}, nil
}

// FocusMode enables or disables focus mode.
func (wm *WindowManager) FocusMode(on bool) (*WindowResult, error) {
	args := map[string]interface{}{
		"on": on,
	}

	// Use the helper method to call MCP tool and check for errors
	mcpResult, err := wm.callMcpTool("focus_mode", args, "error setting focus mode")
	if err != nil {
		return nil, err
	}

	return &WindowResult{
		ApiResponse: models.ApiResponse{
			RequestID: mcpResult.RequestID,
		},
		Success: true,
	}, nil
}
