package code

import (
	"encoding/json"
	"fmt"
	"strings"

	mcp "github.com/aliyun/wuying-agentbay-sdk/golang/api/client"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/models"
)

// CodeExecutionError represents an error during code execution
type CodeExecutionError struct {
	Name      string `json:"name"`
	Value     string `json:"value"`
	Traceback string `json:"traceback"`
}

// CodeExecutionLogs represents stdout and stderr logs
type CodeExecutionLogs struct {
	Stdout []string `json:"stdout"`
	Stderr []string `json:"stderr"`
}

// CodeExecutionResultItem represents a single result item (text, image, etc.)
type CodeExecutionResultItem struct {
	Text         string      `json:"text,omitempty"`
	HTML         string      `json:"html,omitempty"`
	Markdown     string      `json:"markdown,omitempty"`
	PNG          string      `json:"png,omitempty"`
	JPEG         string      `json:"jpeg,omitempty"`
	SVG          string      `json:"svg,omitempty"`
	Latex        string      `json:"latex,omitempty"`
	JSON         interface{} `json:"json,omitempty"`
	Chart        interface{} `json:"chart,omitempty"`
	IsMainResult bool        `json:"is_main_result,omitempty"`
}

// CodeResult represents the result of a code execution
type CodeResult struct {
	models.ApiResponse // Embedded ApiResponse

	// Legacy/Simple output
	Output string

	// Enhanced fields
	Success        bool                      `json:"success"`
	Result         string                    `json:"result"` // Legacy compatible result text
	ErrorMessage   string                    `json:"error_message,omitempty"`
	Logs           *CodeExecutionLogs        `json:"logs,omitempty"`
	Results        []CodeExecutionResultItem `json:"results,omitempty"`
	Error          *CodeExecutionError       `json:"error,omitempty"`
	ExecutionTime  float64                   `json:"execution_time,omitempty"`
	ExecutionCount *int                      `json:"execution_count,omitempty"`
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
		CallMcpTool(toolName string, args interface{}, autoGenSession ...bool) (*models.McpToolResult, error)
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
	CallMcpTool(toolName string, args interface{}, autoGenSession ...bool) (*models.McpToolResult, error)
}) *Code {
	return &Code{
		Session: session,
	}
}

// backendResponse represents the raw JSON structure returned by the backend tool
type backendResponse struct {
	ExecutionError string   `json:"executionError"`
	Result         []string `json:"result"` // List of JSON strings
	Stdout         []string `json:"stdout"`
	Stderr         []string `json:"stderr"`
	TraceID        string   `json:"traceId"`
	// Try both cases just in case
	ExecutionTime   float64 `json:"executionTime"`
	ExecutionTimeSn float64 `json:"execution_time"`
	ExecutionCount  *int    `json:"executionCount"`
	ExecutionCntSn  *int    `json:"execution_count"`
}

func parseBackendResponse(data string) (*CodeResult, error) {
	var raw backendResponse
	if err := json.Unmarshal([]byte(data), &raw); err != nil {
		return nil, err
	}

	// Check if it's actually the expected structure (e.g. has result or stdout/stderr keys)
	// If unmarshal into empty struct, it might succeed but be empty.
	// But since Result/Stdout are slices, they will be nil or empty.
	// We can check if data looks like JSON object.
	// But let's assume if Unmarshal works and we find keys, it's good.

	logs := &CodeExecutionLogs{
		Stdout: raw.Stdout,
		Stderr: raw.Stderr,
	}
	if logs.Stdout == nil {
		logs.Stdout = []string{}
	}
	if logs.Stderr == nil {
		logs.Stderr = []string{}
	}

	execTime := raw.ExecutionTime
	if execTime == 0 {
		execTime = raw.ExecutionTimeSn
	}

	execCount := raw.ExecutionCount
	if execCount == nil {
		execCount = raw.ExecutionCntSn
	}

	res := &CodeResult{
		Success:        true,
		Logs:           logs,
		ExecutionTime:  execTime,
		ExecutionCount: execCount,
	}

	// Parse Results
	for _, resultStr := range raw.Result {
		var itemMap map[string]interface{}
		if err := json.Unmarshal([]byte(resultStr), &itemMap); err != nil {
			continue
		}

		item := CodeExecutionResultItem{
			JSON:  itemMap["json"],
			Chart: itemMap["chart"],
		}

		if val, ok := itemMap["isMainResult"].(bool); ok {
			item.IsMainResult = val
		}

		// Map MIME types to fields
		if val, ok := itemMap["text/plain"].(string); ok {
			item.Text = val
		}
		if val, ok := itemMap["text/html"].(string); ok {
			item.HTML = val
		}
		if val, ok := itemMap["text/markdown"].(string); ok {
			item.Markdown = val
		}
		if val, ok := itemMap["image/png"].(string); ok {
			item.PNG = val
		}
		if val, ok := itemMap["image/jpeg"].(string); ok {
			item.JPEG = val
		}
		if val, ok := itemMap["image/svg+xml"].(string); ok {
			item.SVG = val
		}
		if val, ok := itemMap["text/latex"].(string); ok {
			item.Latex = val
		}
		// Handle JSON and Chart mime types
		if val, ok := itemMap["application/json"]; ok {
			item.JSON = val
		}
		if val, ok := itemMap["application/vnd.vegalite.v4+json"]; ok {
			item.Chart = val
		}
		if val, ok := itemMap["application/vnd.vegalite.v5+json"]; ok {
			item.Chart = val
		}
		if val, ok := itemMap["application/vnd.vega.v5+json"]; ok {
			item.Chart = val
		}

		res.Results = append(res.Results, item)
	}
	if res.Results == nil {
		res.Results = []CodeExecutionResultItem{}
	}

	// Handle Error
	if raw.ExecutionError != "" {
		res.Success = false
		res.Error = &CodeExecutionError{
			Value: raw.ExecutionError,
			// Name and Traceback might not be parsed from simple string
		}
		res.ErrorMessage = raw.ExecutionError
	}

	// Construct Result/Output string for backward compatibility
	foundText := false
	for _, r := range res.Results {
		if r.IsMainResult && r.Text != "" {
			res.Output = r.Text
			res.Result = r.Text
			foundText = true
			break
		}
	}
	if !foundText && len(res.Results) > 0 && res.Results[0].Text != "" {
		res.Output = res.Results[0].Text
		res.Result = res.Results[0].Text
		foundText = true
	}
	if !foundText && len(res.Logs.Stdout) > 0 {
		res.Output = strings.Join(res.Logs.Stdout, "")
		res.Result = res.Output
	}

	return res, nil
}

// RunCode executes code in the session environment.
// timeoutS: The timeout for the code execution in seconds. Default is 60s.
// Note: Due to gateway limitations, each request cannot exceed 60 seconds.
//
// Example:
//
//	client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
//	sessionResult, _ := client.Create(agentbay.NewCreateSessionParams().WithImageId("code_latest"))
//	defer sessionResult.Session.Delete()
//	codeResult, _ := sessionResult.Session.Code.RunCode("print('Hello')", "python")
func (c *Code) RunCode(code string, language string, timeoutS ...int) (*CodeResult, error) {
	// Set default timeout if not provided
	timeout := 60
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

	// Use Session's CallMcpTool method
	result, err := c.Session.CallMcpTool("run_code", args)
	if err != nil {
		return nil, fmt.Errorf("failed to execute code: %w", err)
	}

	var codeRes *CodeResult
	var parseErr error

	if result.Success {
		codeRes, parseErr = parseBackendResponse(result.Data)
	} else {
		// Try parsing error message if it looks like JSON
		if strings.HasPrefix(strings.TrimSpace(result.ErrorMessage), "{") {
			codeRes, parseErr = parseBackendResponse(result.ErrorMessage)
			if codeRes != nil {
				codeRes.Success = false
			}
		} else {
			// Not JSON error, real failure
			return nil, fmt.Errorf("code execution failed: %s", result.ErrorMessage)
		}
	}

	// If parsing failed or result was not enhanced
	if parseErr != nil || codeRes == nil {
		if !result.Success {
			return nil, fmt.Errorf("code execution failed: %s", result.ErrorMessage)
		}
		// Legacy fallback
		codeRes = &CodeResult{
			Success: true,
			Output:  result.Data,
			Result:  result.Data,
		}
	}

	codeRes.RequestID = result.RequestID
	codeRes.ApiResponse = models.ApiResponse{RequestID: result.RequestID}

	return codeRes, nil
}
