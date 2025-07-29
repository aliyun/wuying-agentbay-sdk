package command

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

// CommandResult represents the result of a command execution
type CommandResult struct {
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

// Command handles command execution operations in the AgentBay cloud environment.
type Command struct {
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

// NewCommand creates a new Command instance
func NewCommand(session interface {
	GetAPIKey() string
	GetClient() *mcp.Client
	GetSessionId() string
	IsVpc() bool
	NetworkInterfaceIp() string
	HttpPort() string
	FindServerForTool(toolName string) string
}) *Command {
	return &Command{
		Session: session,
	}
}

// CallMcpTool calls the MCP tool and handles both VPC and non-VPC scenarios
func (c *Command) CallMcpTool(toolName string, args interface{}, defaultErrorMsg string) (*CallMcpToolResult, error) {
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
func (c *Command) callMcpToolVPC(toolName, argsJSON, defaultErrorMsg string) (*CallMcpToolResult, error) {
	// VPC mode: Use HTTP request to the VPC endpoint
	fmt.Println("API Call: CallMcpTool (VPC) -", toolName)
	fmt.Printf("Request: Args=%s\n", argsJSON)

	// Find server for this tool
	server := c.Session.FindServerForTool(toolName)
	if server == "" {
		return nil, fmt.Errorf("server not found for tool: %s", toolName)
	}

	// Construct VPC URL with query parameters
	baseURL := fmt.Sprintf("http://%s:%s/callTool", c.Session.NetworkInterfaceIp(), c.Session.HttpPort())

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
	q.Add("apiKey", c.Session.GetAPIKey())
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
	result := &CallMcpToolResult{
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
func (c *Command) callMcpToolAPI(toolName, argsJSON, defaultErrorMsg string) (*CallMcpToolResult, error) {
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

// ExecuteCommand executes a command in the session environment.
func (c *Command) ExecuteCommand(command string, timeoutMs ...int) (*CommandResult, error) {
	// Set default timeout if not provided
	timeout := 1000
	if len(timeoutMs) > 0 && timeoutMs[0] > 0 {
		timeout = timeoutMs[0]
	}

	args := map[string]interface{}{
		"command":    command,
		"timeout_ms": timeout,
	}

	// Use local CallMcpTool method instead of type assertion
	result, err := c.CallMcpTool("shell", args, "Failed to execute command")
	if err != nil {
		return nil, err
	}

	return &CommandResult{
		ApiResponse: models.ApiResponse{
			RequestID: result.GetRequestID(),
		},
		Output: result.GetTextContent(),
	}, nil
}
