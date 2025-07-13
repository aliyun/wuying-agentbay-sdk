package ui

import (
	"encoding/json"
	"fmt"
	"strings"

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
	}
}

// NewUI creates a new UI object
func NewUI(session interface {
	GetAPIKey() string
	GetClient() *mcp.Client
	GetSessionId() string
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
}

// callMcpTool is an internal helper to call MCP tool and handle errors
func (u *UIManager) callMcpTool(name string, args interface{}, defaultErrorMsg string) (*callMcpToolResult, error) {
	// Check if client is nil
	client := u.Session.GetClient()
	if client == nil {
		return nil, fmt.Errorf("client is nil, failed to call %s", name)
	}

	argsJSON, err := json.Marshal(args)
	if err != nil {
		return nil, fmt.Errorf("failed to marshal args: %w", err)
	}

	// Create the request
	callToolRequest := &mcp.CallMcpToolRequest{
		Authorization: tea.String("Bearer " + u.Session.GetAPIKey()),
		SessionId:     tea.String(u.Session.GetSessionId()),
		Name:          tea.String(name),
		Args:          tea.String(string(argsJSON)),
	}

	// Log API request
	fmt.Println("API Call: CallMcpTool -", name)
	fmt.Printf("Request: SessionId=%s, Args=%s\n", *callToolRequest.SessionId, *callToolRequest.Args)

	// Call the MCP tool
	response, err := client.CallMcpTool(callToolRequest)
	if err != nil {
		fmt.Println("Error calling CallMcpTool -", name, ":", err)
		return nil, fmt.Errorf("failed to call %s: %w", name, err)
	}
	if response != nil && response.Body != nil {
		fmt.Println("Response from CallMcpTool -", name, ":", response.Body)
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
		contentArray, ok := data["content"].([]interface{})
		if ok && len(contentArray) > 0 {
			// Extract error message from the first content item
			if len(contentArray) > 0 {
				contentItem, ok := contentArray[0].(map[string]interface{})
				if ok {
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

	// Extract text from content array if it exists
	contentArray, ok := data["content"].([]interface{})
	if ok && len(contentArray) > 0 {
		var textBuilder strings.Builder
		for i, item := range contentArray {
			contentItem, ok := item.(map[string]interface{})
			if !ok {
				continue
			}

			text, ok := contentItem["text"].(string)
			if !ok {
				continue
			}

			if i > 0 {
				textBuilder.WriteString("\n")
			}
			textBuilder.WriteString(text)
		}
		result.TextContent = textBuilder.String()
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
