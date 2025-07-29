package oss

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

// UploadResult wraps upload result and RequestID
type UploadResult struct {
	models.ApiResponse
	URL string
}

// DownloadResult wraps download result and RequestID
type DownloadResult struct {
	models.ApiResponse
	LocalPath string
}

// EnvInitResult wraps OSS environment initialization result and RequestID
type EnvInitResult struct {
	models.ApiResponse
	Result string
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

// OSSManager handles OSS operations in the AgentBay cloud environment.
type OSSManager struct {
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

// CallMcpTool calls the MCP tool and handles both VPC and non-VPC scenarios
func (o *OSSManager) CallMcpTool(toolName string, args interface{}, defaultErrorMsg string) (*CallMcpToolResult, error) {
	// Marshal arguments to JSON
	argsJSON, err := json.Marshal(args)
	if err != nil {
		return nil, fmt.Errorf("failed to marshal args: %w", err)
	}

	// Check if this is a VPC session
	if o.Session.IsVpc() {
		return o.callMcpToolVPC(toolName, string(argsJSON), defaultErrorMsg)
	}

	// Non-VPC mode: use traditional API call
	return o.callMcpToolAPI(toolName, string(argsJSON), defaultErrorMsg)
}

// callMcpToolVPC handles VPC-based MCP tool calls
func (o *OSSManager) callMcpToolVPC(toolName, argsJSON, defaultErrorMsg string) (*CallMcpToolResult, error) {
	// VPC mode: Use HTTP request to the VPC endpoint
	fmt.Println("API Call: CallMcpTool (VPC) -", toolName)
	fmt.Printf("Request: Args=%s\n", argsJSON)

	// Find server for this tool
	server := o.Session.FindServerForTool(toolName)
	if server == "" {
		return nil, fmt.Errorf("server not found for tool: %s", toolName)
	}

	// Construct VPC URL
	url := fmt.Sprintf("http://%s:%s/callTool", o.Session.NetworkInterfaceIp(), o.Session.HttpPort())

	// Prepare request body
	requestBody := map[string]interface{}{
		"server": server,
		"tool":   toolName,
		"args":   argsJSON,
		"apikey": o.Session.GetAPIKey(),
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
func (o *OSSManager) callMcpToolAPI(toolName, argsJSON, defaultErrorMsg string) (*CallMcpToolResult, error) {
	// Create the request
	callToolRequest := &mcp.CallMcpToolRequest{
		Authorization: tea.String("Bearer " + o.Session.GetAPIKey()),
		SessionId:     tea.String(o.Session.GetSessionId()),
		Name:          tea.String(toolName),
		Args:          tea.String(argsJSON),
	}

	// Log API request
	fmt.Println("API Call: CallMcpTool -", toolName)
	fmt.Printf("Request: SessionId=%s, Args=%s\n", *callToolRequest.SessionId, *callToolRequest.Args)

	// Call the MCP tool
	response, err := o.Session.GetClient().CallMcpTool(callToolRequest)

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
func (o *OSSManager) callMcpToolHelper(toolName string, args interface{}, defaultErrorMsg string) (*CallMcpToolResult, error) {
	return o.CallMcpTool(toolName, args, defaultErrorMsg)
}

// Helper function to extract common result fields from CallMcpTool result
func (o *OSSManager) extractCallResult(result *CallMcpToolResult) (string, string, map[string]interface{}, error) {
	if result.GetIsError() {
		return "", "", nil, fmt.Errorf(result.GetErrorMsg())
	}
	return result.GetRequestID(), result.GetTextContent(), result.GetData(), nil
}

// NewOss creates a new Oss object.
func NewOss(session interface {
	GetAPIKey() string
	GetClient() *mcp.Client
	GetSessionId() string
	IsVpc() bool
	NetworkInterfaceIp() string
	HttpPort() string
	FindServerForTool(toolName string) string
}) *OSSManager {
	return &OSSManager{
		Session: session,
	}
}

// EnvInit initializes the OSS environment.
func (o *OSSManager) EnvInit(accessKeyId, accessKeySecret, securityToken, endpoint, region string) (*EnvInitResult, error) {
	args := map[string]interface{}{
		"access_key_id":     accessKeyId,
		"access_key_secret": accessKeySecret,
		"security_token":    securityToken,
	}

	// Add optional parameters if provided
	if endpoint != "" {
		args["endpoint"] = endpoint
	}
	if region != "" {
		args["region"] = region
	}

	// Use the local CallMcpTool method
	result, err := o.callMcpToolHelper("oss_env_init", args, "error initializing OSS environment")
	if err != nil {
		return nil, err
	}

	// Extract result fields using helper
	requestID, textContent, _, err := o.extractCallResult(result)
	if err != nil {
		return nil, err
	}

	return &EnvInitResult{
		ApiResponse: models.ApiResponse{
			RequestID: requestID,
		},
		Result: textContent,
	}, nil
}

// Upload uploads a local file or directory to OSS.
func (o *OSSManager) Upload(bucket, object, path string) (*UploadResult, error) {
	// Prepare arguments for the oss_upload tool
	args := map[string]interface{}{
		"bucket": bucket,
		"object": object,
		"path":   path,
	}

	// Use the helper method to call MCP tool and check for errors
	mcpResult, err := o.callMcpToolHelper("oss_upload", args, "error uploading to OSS")
	if err != nil {
		return nil, err
	}

	// Return the result with RequestID
	return &UploadResult{
		ApiResponse: models.ApiResponse{
			RequestID: mcpResult.GetRequestID(),
		},
		URL: mcpResult.GetTextContent(),
	}, nil
}

// UploadAnonymous uploads a local file or directory to a URL anonymously.
func (o *OSSManager) UploadAnonymous(url, path string) (*UploadResult, error) {
	// Prepare arguments for the oss_upload_annon tool
	args := map[string]interface{}{
		"url":  url,
		"path": path,
	}

	// Use the helper method to call MCP tool and check for errors
	mcpResult, err := o.callMcpToolHelper("oss_upload_annon", args, "error uploading anonymously")
	if err != nil {
		return nil, err
	}

	// Return the result with RequestID
	return &UploadResult{
		ApiResponse: models.ApiResponse{
			RequestID: mcpResult.GetRequestID(),
		},
		URL: mcpResult.GetTextContent(),
	}, nil
}

// Download downloads a file from the specified OSS bucket to a local path.
func (o *OSSManager) Download(bucket, object, path string) (*DownloadResult, error) {
	// Prepare arguments for the oss_download tool
	args := map[string]interface{}{
		"bucket": bucket,
		"object": object,
		"path":   path,
	}

	// Use the helper method to call MCP tool and check for errors
	mcpResult, err := o.callMcpToolHelper("oss_download", args, "error downloading from OSS")
	if err != nil {
		return nil, err
	}

	// Return the result with RequestID
	return &DownloadResult{
		ApiResponse: models.ApiResponse{
			RequestID: mcpResult.GetRequestID(),
		},
		LocalPath: mcpResult.GetTextContent(),
	}, nil
}

// DownloadAnonymous downloads a file from the specified URL to a local path.
func (o *OSSManager) DownloadAnonymous(url, path string) (*DownloadResult, error) {
	// Prepare arguments for the oss_download_annon tool
	args := map[string]interface{}{
		"url":  url,
		"path": path,
	}

	// Use the helper method to call MCP tool and check for errors
	mcpResult, err := o.callMcpToolHelper("oss_download_annon", args, "error downloading anonymously")
	if err != nil {
		return nil, err
	}

	// Return the result with RequestID
	return &DownloadResult{
		ApiResponse: models.ApiResponse{
			RequestID: mcpResult.GetRequestID(),
		},
		LocalPath: mcpResult.GetTextContent(),
	}, nil
}
