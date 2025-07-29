package ui

import (
	"encoding/json"
	"fmt"
	"net/http"
	"strings"
	"time"

	"github.com/alibabacloud-go/tea/tea"
	mcp "github.com/aliyun/wuying-agentbay-sdk/golang/api/client"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/models"
)

// UIResult wraps UI operation result and RequestID
type UIResult struct {
	models.ApiResponse
	ComponentID string
	Success     bool
}

// TextInputResult wraps text input result and RequestID
type TextInputResult struct {
	models.ApiResponse
	Text string
}

// UIElementsResult wraps UI elements list and RequestID
type UIElementsResult struct {
	models.ApiResponse
	Elements []*UIElement
}

// KeyActionResult wraps keyboard action result and RequestID
type KeyActionResult struct {
	models.ApiResponse
	Success bool
}

// SwipeResult wraps swipe operation result and RequestID
type SwipeResult struct {
	models.ApiResponse
	Success bool
}

// UIElement represents a UI element in the UI hierarchy
type UIElement struct {
	Bounds     string       `json:"bounds"`
	ClassName  string       `json:"className"`
	Text       string       `json:"text"`
	Type       string       `json:"type"`
	ResourceId string       `json:"resourceId"`
	Index      int          `json:"index"`
	IsParent   bool         `json:"isParent"`
	Children   []*UIElement `json:"children,omitempty"`
}

// KeyCode constants for mobile device input
var KeyCode = struct {
	HOME        int
	BACK        int
	VOLUME_UP   int
	VOLUME_DOWN int
	POWER       int
	MENU        int
}{
	HOME:        3,
	BACK:        4,
	VOLUME_UP:   24,
	VOLUME_DOWN: 25,
	POWER:       26,
	MENU:        82,
}

// UIManager handles UI operations in the AgentBay cloud environment.
type UIManager struct {
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

// NewUI creates a new UI object
func NewUI(session interface {
	GetAPIKey() string
	GetClient() *mcp.Client
	GetSessionId() string
	IsVpc() bool
	NetworkInterfaceIp() string
	HttpPort() string
	FindServerForTool(toolName string) string
}) *UIManager {
	return &UIManager{
		Session: session,
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

// callMcpTool is an internal helper to call MCP tool and handle errors
func (u *UIManager) callMcpTool(name string, args interface{}, defaultErrorMsg string) (*callMcpToolResult, error) {
	// Marshal arguments to JSON
	argsJSON, err := json.Marshal(args)
	if err != nil {
		return nil, fmt.Errorf("failed to marshal args: %w", err)
	}

	// Check if this is a VPC session
	if u.Session.IsVpc() {
		return u.callMcpToolVPC(name, string(argsJSON), defaultErrorMsg)
	}

	// Non-VPC mode: use traditional API call
	return u.callMcpToolAPI(name, string(argsJSON), defaultErrorMsg)
}

// callMcpToolVPC handles VPC-based MCP tool calls
func (u *UIManager) callMcpToolVPC(toolName, argsJSON, defaultErrorMsg string) (*callMcpToolResult, error) {
	// VPC mode: Use HTTP request to the VPC endpoint
	fmt.Println("API Call: CallMcpTool (VPC) -", toolName)
	fmt.Printf("Request: Args=%s\n", argsJSON)

	// Find server for this tool
	server := u.Session.FindServerForTool(toolName)
	if server == "" {
		return nil, fmt.Errorf("server not found for tool: %s", toolName)
	}

	// Construct VPC URL with query parameters
	baseURL := fmt.Sprintf("http://%s:%s/callTool", u.Session.NetworkInterfaceIp(), u.Session.HttpPort())

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
	q.Add("apiKey", u.Session.GetAPIKey())
	req.URL.RawQuery = q.Encode()

	// Set content type header
	req.Header.Set("Content-Type", "application/x-www-form-urlencoded")

	// Send HTTP request
	client := &http.Client{Timeout: 30 * time.Second}
	resp, err := client.Do(req)
	if err != nil {
		fmt.Println("Error calling VPC CallMcpTool -", toolName, ":", err)
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
func (u *UIManager) callMcpToolAPI(toolName, argsJSON, defaultErrorMsg string) (*callMcpToolResult, error) {
	// Check if client is nil
	client := u.Session.GetClient()
	if client == nil {
		return nil, fmt.Errorf("client is nil, failed to call %s", toolName)
	}

	// Create the request
	callToolRequest := &mcp.CallMcpToolRequest{
		Authorization: tea.String("Bearer " + u.Session.GetAPIKey()),
		SessionId:     tea.String(u.Session.GetSessionId()),
		Name:          tea.String(toolName),
		Args:          tea.String(argsJSON),
	}

	// Log API request
	fmt.Println("API Call: CallMcpTool -", toolName)
	fmt.Printf("Request: SessionId=%s, Args=%s\n", *callToolRequest.SessionId, *callToolRequest.Args)

	// Call the MCP tool
	response, err := client.CallMcpTool(callToolRequest)
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
		//nolint:govet
		contentArray, ok := data["content"].([]interface{})
		if ok && len(contentArray) > 0 {
			// Extract error message from the first content item
			if len(contentArray) > 0 {
				//nolint:govet
				contentItem, ok := contentArray[0].(map[string]interface{})
				if ok {
					//nolint:govet
					text, ok := contentItem["text"].(string)
					if ok {
						result.ErrorMsg = text
						return result, fmt.Errorf("%s", text)
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

// GetClickableUIElements retrieves all clickable UI elements within the specified timeout
func (u *UIManager) GetClickableUIElements(timeoutMs int) (*UIElementsResult, error) {
	if timeoutMs <= 0 {
		timeoutMs = 2000 // Default timeout
	}

	args := map[string]interface{}{
		"timeout_ms": timeoutMs,
	}

	result, err := u.callMcpTool("get_clickable_ui_elements", args, "failed to get clickable UI elements")
	if err != nil {
		return nil, err
	}

	// Parse the JSON string into a slice of UIElement structs
	var elements []*UIElement
	if err := json.Unmarshal([]byte(result.TextContent), &elements); err != nil {
		return nil, fmt.Errorf("failed to parse UI elements: %w", err)
	}

	return &UIElementsResult{
		ApiResponse: models.ApiResponse{
			RequestID: result.RequestID,
		},
		Elements: elements,
	}, nil
}

// GetAllUIElements retrieves all UI elements within the specified timeout
func (u *UIManager) GetAllUIElements(timeoutMs int) (*UIElementsResult, error) {
	if timeoutMs <= 0 {
		timeoutMs = 2000 // Default timeout
	}

	args := map[string]interface{}{
		"timeout_ms": timeoutMs,
	}

	result, err := u.callMcpTool("get_all_ui_elements", args, "failed to get all UI elements")
	if err != nil {
		return nil, err
	}

	// Parse the JSON string into a slice of UIElement structs
	var elements []*UIElement
	if err := json.Unmarshal([]byte(result.TextContent), &elements); err != nil {
		return nil, fmt.Errorf("failed to parse UI elements: %w", err)
	}

	return &UIElementsResult{
		ApiResponse: models.ApiResponse{
			RequestID: result.RequestID,
		},
		Elements: elements,
	}, nil
}

// SendKey sends a key press event
func (u *UIManager) SendKey(key int) (*KeyActionResult, error) {
	args := map[string]interface{}{
		"key": key,
	}

	result, err := u.callMcpTool("send_key", args, "failed to send key")
	if err != nil {
		return nil, err
	}

	return &KeyActionResult{
		ApiResponse: models.ApiResponse{
			RequestID: result.RequestID,
		},
		Success: true,
	}, nil
}

// InputText inputs text at the current cursor position
func (u *UIManager) InputText(text string) (*TextInputResult, error) {
	args := map[string]string{
		"text": text,
	}

	result, err := u.callMcpTool("input_text", args, "failed to input text")
	if err != nil {
		return nil, err
	}

	return &TextInputResult{
		ApiResponse: models.ApiResponse{
			RequestID: result.RequestID,
		},
		Text: text,
	}, nil
}

// Swipe performs a swipe gesture from (startX,startY) to (endX,endY) over durationMs milliseconds
func (u *UIManager) Swipe(startX, startY, endX, endY, durationMs int) (*SwipeResult, error) {
	args := map[string]interface{}{
		"start_x":     startX,
		"start_y":     startY,
		"end_x":       endX,
		"end_y":       endY,
		"duration_ms": durationMs,
	}

	result, err := u.callMcpTool("swipe", args, "failed to swipe")
	if err != nil {
		return nil, err
	}

	return &SwipeResult{
		ApiResponse: models.ApiResponse{
			RequestID: result.RequestID,
		},
		Success: true,
	}, nil
}

// Click performs a mouse click at (x,y) with the specified button
func (u *UIManager) Click(x, y int, button string) (*UIResult, error) {
	if button == "" {
		button = "left"
	}

	if button != "left" && button != "right" && button != "middle" {
		return nil, fmt.Errorf("invalid button: %s. Must be 'left', 'right', or 'middle'", button)
	}

	args := map[string]interface{}{
		"x":      x,
		"y":      y,
		"button": button,
	}

	result, err := u.callMcpTool("click", args, "failed to click")
	if err != nil {
		return nil, err
	}

	return &UIResult{
		ApiResponse: models.ApiResponse{
			RequestID: result.RequestID,
		},
		Success: true,
	}, nil
}

// Screenshot takes a screenshot of the current screen and returns the path to the image
func (u *UIManager) Screenshot() (*UIResult, error) {
	result, err := u.callMcpTool("system_screenshot", nil, "failed to take screenshot")
	if err != nil {
		return nil, err
	}

	return &UIResult{
		ApiResponse: models.ApiResponse{
			RequestID: result.RequestID,
		},
		Success: true,
	}, nil
}
