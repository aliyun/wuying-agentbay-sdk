package oss

import (
	"encoding/json"
	"fmt"
	"strings"

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

// OSSManager handles object storage operations in the AgentBay cloud environment.
type OSSManager struct {
	Session interface {
		GetAPIKey() string
		GetClient() *mcp.Client
		GetSessionId() string
	}
}

// callMcpToolResult represents the result of a CallMcpTool operation
type callMcpToolResult struct {
	Data        map[string]interface{}
	Content     []map[string]interface{}
	TextContent string // Extracted text field content
	IsError     bool
	ErrorMsg    string
	StatusCode  int32
	RequestID   string // Added field to store request ID
}

// callMcpTool calls the MCP tool and checks for errors in the response
func (o *OSSManager) callMcpTool(toolName string, args interface{}, defaultErrorMsg string) (*callMcpToolResult, error) {
	// Marshal arguments to JSON
	argsJSON, err := json.Marshal(args)
	if err != nil {
		return nil, fmt.Errorf("failed to marshal args: %w", err)
	}

	// Create the request
	callToolRequest := &mcp.CallMcpToolRequest{
		Authorization: tea.String("Bearer " + o.Session.GetAPIKey()),
		SessionId:     tea.String(o.Session.GetSessionId()),
		Name:          tea.String(toolName),
		Args:          tea.String(string(argsJSON)),
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
	result := &callMcpToolResult{
		Data:       data,
		StatusCode: *response.StatusCode,
		RequestID:  requestID, // Add RequestID
	}

	// Check if there's an error in the response
	isError, ok := data["isError"].(bool)
	if ok && isError {
		result.IsError = true

		// Try to extract the error message from the content field
		contentArray, ok := data["content"].([]interface{})
		if ok && len(contentArray) > 0 {
			// Convert content array to a more usable format
			result.Content = make([]map[string]interface{}, 0, len(contentArray))
			for _, item := range contentArray {
				contentItem, ok := item.(map[string]interface{})
				if !ok {
					continue
				}
				result.Content = append(result.Content, contentItem)
			}

			// Extract error message from the first content item
			if len(result.Content) > 0 {
				text, ok := result.Content[0]["text"].(string)
				if ok {
					result.ErrorMsg = text
					return result, fmt.Errorf("%s", text)
				}
			}
		}
		return result, fmt.Errorf("%s", defaultErrorMsg)
	}

	// Extract content array if it exists
	contentArray, ok := data["content"].([]interface{})
	if ok {
		result.Content = make([]map[string]interface{}, 0, len(contentArray))
		for _, item := range contentArray {
			contentItem, ok := item.(map[string]interface{})
			if !ok {
				continue
			}
			result.Content = append(result.Content, contentItem)
		}

		// Extract text content from the content items
		var textBuilder strings.Builder
		for i, item := range result.Content {
			text, ok := item["text"].(string)
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

// NewOss creates a new Oss object.
func NewOss(session interface {
	GetAPIKey() string
	GetClient() *mcp.Client
	GetSessionId() string
}) *OSSManager {
	return &OSSManager{
		Session: session,
	}
}

// EnvInit creates and initializes OSS environment variables with the specified credentials.
func (o *OSSManager) EnvInit(accessKeyId, accessKeySecret, securityToken, endpoint, region string) (*EnvInitResult, error) {
	// Prepare arguments for the oss_env_init tool
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

	// Use the helper method to call MCP tool and check for errors
	mcpResult, err := o.callMcpTool("oss_env_init", args, "error initializing OSS environment")
	if err != nil {
		return nil, err
	}

	// Return result with RequestID
	return &EnvInitResult{
		ApiResponse: models.ApiResponse{
			RequestID: mcpResult.RequestID,
		},
		Result: mcpResult.TextContent,
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
	mcpResult, err := o.callMcpTool("oss_upload", args, "error uploading to OSS")
	if err != nil {
		return nil, err
	}

	// Return the result with RequestID
	return &UploadResult{
		ApiResponse: models.ApiResponse{
			RequestID: mcpResult.RequestID,
		},
		URL: mcpResult.TextContent,
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
	mcpResult, err := o.callMcpTool("oss_upload_annon", args, "error uploading anonymously")
	if err != nil {
		return nil, err
	}

	// Return the result with RequestID
	return &UploadResult{
		ApiResponse: models.ApiResponse{
			RequestID: mcpResult.RequestID,
		},
		URL: mcpResult.TextContent,
	}, nil
}

// Download downloads an object from OSS to a local file.
func (o *OSSManager) Download(bucket, object, path string) (*DownloadResult, error) {
	// Prepare arguments for the oss_download tool
	args := map[string]interface{}{
		"bucket": bucket,
		"object": object,
		"path":   path,
	}

	// Use the helper method to call MCP tool and check for errors
	mcpResult, err := o.callMcpTool("oss_download", args, "error downloading from OSS")
	if err != nil {
		return nil, err
	}

	// Return the result with RequestID
	return &DownloadResult{
		ApiResponse: models.ApiResponse{
			RequestID: mcpResult.RequestID,
		},
		LocalPath: mcpResult.TextContent,
	}, nil
}

// DownloadAnonymous downloads a file from a URL anonymously to a local file.
func (o *OSSManager) DownloadAnonymous(url, path string) (*DownloadResult, error) {
	// Prepare arguments for the oss_download_annon tool
	args := map[string]interface{}{
		"url":  url,
		"path": path,
	}

	// Use the helper method to call MCP tool and check for errors
	mcpResult, err := o.callMcpTool("oss_download_annon", args, "error downloading anonymously")
	if err != nil {
		return nil, err
	}

	// Return the result with RequestID
	return &DownloadResult{
		ApiResponse: models.ApiResponse{
			RequestID: mcpResult.RequestID,
		},
		LocalPath: mcpResult.TextContent,
	}, nil
}
