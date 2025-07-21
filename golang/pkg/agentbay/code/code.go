package code

import (
	"encoding/json"
	"fmt"
	"strings"

	"github.com/alibabacloud-go/tea/tea"
	mcp "github.com/aliyun/wuying-agentbay-sdk/golang/api/client"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/models"
)

// CodeResult represents the result of a code execution
type CodeResult struct {
	models.ApiResponse // Embedded ApiResponse
	Output             string
}

// Code handles code execution operations in the AgentBay cloud environment.
type Code struct {
	Session interface {
		GetAPIKey() string
		GetClient() *mcp.Client
		GetSessionId() string
	}
}

// NewCode creates a new Code instance
func NewCode(session interface {
	GetAPIKey() string
	GetClient() *mcp.Client
	GetSessionId() string
}) *Code {
	return &Code{
		Session: session,
	}
}

// callMcpToolResult represents the result of a CallMcpTool operation
type callMcpToolResult struct {
	TextContent string // Extracted text field content
	Data        map[string]interface{}
	IsError     bool
	ErrorMsg    string
	StatusCode  int32
	RequestID   string // Added field to store request ID
}

// callMcpTool calls the MCP tool and checks for errors in the response
func (c *Code) callMcpTool(toolName string, args interface{}, defaultErrorMsg string) (*callMcpToolResult, error) {
	// Marshal arguments to JSON
	argsJSON, err := json.Marshal(args)
	if err != nil {
		return nil, fmt.Errorf("failed to marshal args: %w", err)
	}

	// Create the request
	callToolRequest := &mcp.CallMcpToolRequest{
		Authorization: tea.String("Bearer " + c.Session.GetAPIKey()),
		SessionId:     tea.String(c.Session.GetSessionId()),
		Name:          tea.String(toolName),
		Args:          tea.String(string(argsJSON)),
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
	result := &callMcpToolResult{
		Data:       data,
		StatusCode: *response.StatusCode,
		RequestID:  requestID, // Add RequestID
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

	// Extract text from content array if it exists
	//nolint:govet
	contentArray, ok := data["content"].([]interface{})
	if ok && len(contentArray) > 0 {
		var textBuilder strings.Builder
		for i, item := range contentArray {
			//nolint:govet
			contentItem, ok := item.(map[string]interface{})
			if !ok {
				continue
			}

			//nolint:govet
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

// RunCode executes code in the specified language with a timeout.
// If timeoutS is not provided or is 0, the default timeout of 300 seconds will be used.
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

	// Prepare arguments for the run_code tool
	args := map[string]interface{}{
		"code":      code,
		"language":  language,
		"timeout_s": timeout,
	}

	// Use the enhanced helper method to call MCP tool and check for errors
	mcpResult, err := c.callMcpTool("run_code", args, "error executing code")
	if err != nil {
		return nil, err
	}

	// Return result with RequestID
	return &CodeResult{
		ApiResponse: models.ApiResponse{
			RequestID: mcpResult.RequestID,
		},
		Output: mcpResult.TextContent,
	}, nil
}
