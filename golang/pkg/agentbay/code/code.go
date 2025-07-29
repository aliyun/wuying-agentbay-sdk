package code

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"strings"
	"time"

	"github.com/alibabacloud-go/tea/tea"
	mcp "github.com/aliyun/wuying-agentbay-sdk/golang/api/client"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/models"
)

// CodeResult represents the result of a code execution
type CodeResult struct {
	models.ApiResponse // Embedded ApiResponse
	Output             string
}

// CallMcpToolResult represents the result of a CallMcpTool operation
type CallMcpToolResult struct {
	TextContent string // Extracted text field content
	Data        map[string]interface{}
	Content     []map[string]interface{} // Content array from response
	IsError     bool
	ErrorMsg    string
	StatusCode  int32
	RequestID   string // RequestID from the response
}

// GetRequestID returns the request ID
func (r *CallMcpToolResult) GetRequestID() string {
	return r.RequestID
}

// GetTextContent returns the extracted text content
func (r *CallMcpToolResult) GetTextContent() string {
	return r.TextContent
}

// GetData returns the data map
func (r *CallMcpToolResult) GetData() map[string]interface{} {
	return r.Data
}

// GetContent returns the content array
func (r *CallMcpToolResult) GetContent() []map[string]interface{} {
	return r.Content
}

// GetIsError returns whether there was an error
func (r *CallMcpToolResult) GetIsError() bool {
	return r.IsError
}

// GetErrorMsg returns the error message
func (r *CallMcpToolResult) GetErrorMsg() string {
	return r.ErrorMsg
}

// GetStatusCode returns the status code
func (r *CallMcpToolResult) GetStatusCode() int32 {
	return r.StatusCode
}

// Code handles code execution operations in the AgentBay cloud environment.
type Code struct {
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

// NewCode creates a new Code instance
func NewCode(session interface {
	GetAPIKey() string
	GetClient() *mcp.Client
	GetSessionId() string
	IsVpc() bool
	NetworkInterfaceIp() string
	HttpPort() string
	FindServerForTool(toolName string) string
}) *Code {
	return &Code{
		Session: session,
	}
}

// CallMcpTool calls the MCP tool and handles both VPC and non-VPC scenarios
func (c *Code) CallMcpTool(toolName string, args interface{}, defaultErrorMsg string) (*CallMcpToolResult, error) {
	// Marshal arguments to JSON
	argsJSON, err := json.Marshal(args)
	if err != nil {
		return nil, fmt.Errorf("failed to marshal args: %w", err)
	}

	// Check if this is a VPC session
	if c.Session.IsVpc() {
		return c.callMcpToolVPC(toolName, string(argsJSON), defaultErrorMsg)
	}

	// Non-VPC mode: use traditional API call
	return c.callMcpToolAPI(toolName, string(argsJSON), defaultErrorMsg)
}

// callMcpToolVPC handles VPC-based MCP tool calls
func (c *Code) callMcpToolVPC(toolName, argsJSON, defaultErrorMsg string) (*CallMcpToolResult, error) {
	// VPC mode: Use HTTP request to the VPC endpoint
	fmt.Println("API Call: CallMcpTool (VPC) -", toolName)
	fmt.Printf("Request: Args=%s\n", argsJSON)

	// Find server for this tool
	server := c.Session.FindServerForTool(toolName)
	if server == "" {
		return nil, fmt.Errorf("server not found for tool: %s", toolName)
	}

	// Construct VPC URL
	url := fmt.Sprintf("http://%s:%s/callTool", c.Session.NetworkInterfaceIp(), c.Session.HttpPort())

	// Prepare request body
	requestBody := map[string]interface{}{
		"server": server,
		"tool":   toolName,
		"args":   argsJSON,
		"apikey": c.Session.GetAPIKey(),
	}

	bodyJSON, err := json.Marshal(requestBody)
	if err != nil {
		return nil, fmt.Errorf("failed to marshal VPC request body: %w", err)
	}

	// Create HTTP request
	req, err := http.NewRequest("POST", url, bytes.NewBuffer(bodyJSON))
	if err != nil {
		return nil, fmt.Errorf("failed to create VPC HTTP request: %w", err)
	}
	req.Header.Set("Content-Type", "application/json")

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
	result := &CallMcpToolResult{
		Data:       responseData,
		StatusCode: int32(resp.StatusCode),
		RequestID:  "", // VPC requests don't have traditional request IDs
	}

	// Check if there's an error in the VPC response
	if isError, ok := responseData["isError"].(bool); ok && isError {
		result.IsError = true
		if errMsg, ok := responseData["error"].(string); ok {
			result.ErrorMsg = errMsg
			return result, fmt.Errorf("%s", errMsg)
		}
		return result, fmt.Errorf("%s", defaultErrorMsg)
	}

	// Extract content array if it exists for VPC response
	if contentArray, ok := responseData["content"].([]interface{}); ok {
		result.Content = make([]map[string]interface{}, len(contentArray))
		for i, item := range contentArray {
			if contentItem, ok := item.(map[string]interface{}); ok {
				result.Content[i] = contentItem
			}
		}
	}

	return result, nil
}

// callMcpToolAPI handles traditional API-based MCP tool calls
func (c *Code) callMcpToolAPI(toolName, argsJSON, defaultErrorMsg string) (*CallMcpToolResult, error) {
	// Create the request
	callToolRequest := &mcp.CallMcpToolRequest{
		Authorization: tea.String("Bearer " + c.Session.GetAPIKey()),
		SessionId:     tea.String(c.Session.GetSessionId()),
		Name:          tea.String(toolName),
		Args:          tea.String(argsJSON),
	}

	// Log API request
	fmt.Println("API Call: CallMcpTool -", toolName)
	fmt.Printf("Request: SessionId=%s, Args=%s\n", *callToolRequest.SessionId, *callToolRequest.Args)

	// Call the MCP tool
	response, err := c.Session.GetClient().CallMcpTool(callToolRequest)

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
	result := &CallMcpToolResult{
		Data:       data,
		StatusCode: *response.StatusCode,
		RequestID:  requestID,
	}

	// Check if there's an error in the response
	if isError, ok := data["isError"].(bool); ok && isError {
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

// callMcpToolHelper is a helper that calls the local CallMcpTool method
func (c *Code) callMcpToolHelper(toolName string, args interface{}, defaultErrorMsg string) (*CallMcpToolResult, error) {
	return c.CallMcpTool(toolName, args, defaultErrorMsg)
}

// Helper function to extract common result fields from CallMcpTool result
func (c *Code) extractCallResult(result *CallMcpToolResult) (string, string, map[string]interface{}, error) {
	if result.GetIsError() {
		return "", "", nil, fmt.Errorf(result.GetErrorMsg())
	}
	return result.GetRequestID(), result.GetTextContent(), result.GetData(), nil
}

// RunCode executes code in the session environment.
func (c *Code) RunCode(code string, language string, timeoutS ...int) (*CodeResult, error) {
	// Set default timeout if not provided
	timeout := 300
	if len(timeoutS) > 0 && timeoutS[0] > 0 {
		timeout = timeoutS[0]
	}

	// Validate language
	if language != "python" && language != "javascript" {
		return nil, fmt.Errorf("unsupported language: %s. Supported languages are 'python' and 'javascript'", language)
	}

	args := map[string]interface{}{
		"code":      code,
		"language":  language,
		"timeout_s": timeout,
	}

	// Use the local CallMcpTool method
	result, err := c.callMcpToolHelper("run_code", args, "error executing code")
	if err != nil {
		return nil, err
	}

	// Extract result fields using helper
	requestID, textContent, _, err := c.extractCallResult(result)
	if err != nil {
		return nil, err
	}

	return &CodeResult{
		ApiResponse: models.ApiResponse{
			RequestID: requestID,
		},
		Output: textContent,
	}, nil
}
