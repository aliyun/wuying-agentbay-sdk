package code

import (
	"fmt"

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

// callMcpToolHelper is a helper that calls the session's CallMcpTool method
func (c *Code) callMcpToolHelper(toolName string, args interface{}, defaultErrorMsg string) (interface{}, error) {
	// Type assertion to access Session's CallMcpTool method
	if sessionWithCallTool, ok := c.Session.(interface {
		CallMcpTool(toolName string, args interface{}, defaultErrorMsg string) (interface{}, error)
	}); ok {
		return sessionWithCallTool.CallMcpTool(toolName, args, defaultErrorMsg)
	}
	return nil, fmt.Errorf("session does not support CallMcpTool method")
}

// Helper function to extract common result fields from CallMcpTool result
func (c *Code) extractCallResult(result interface{}) (string, string, map[string]interface{}, error) {
	if callResult, ok := result.(interface {
		GetRequestID() string
		GetTextContent() string
		GetData() map[string]interface{}
		GetIsError() bool
		GetErrorMsg() string
	}); ok {
		if callResult.GetIsError() {
			return "", "", nil, fmt.Errorf(callResult.GetErrorMsg())
		}
		return callResult.GetRequestID(), callResult.GetTextContent(), callResult.GetData(), nil
	}
	return "", "", nil, fmt.Errorf("invalid result type from CallMcpTool")
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

	// Use the session's CallMcpTool method
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
