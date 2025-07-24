package oss

import (
	"fmt"

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

// OSSManager handles OSS operations in the AgentBay cloud environment.
type OSSManager struct {
	Session interface {
		GetAPIKey() string
		GetClient() *mcp.Client
		GetSessionId() string
	}
}

// callMcpToolHelper is a helper that calls the session's CallMcpTool method
func (o *OSSManager) callMcpToolHelper(toolName string, args interface{}, defaultErrorMsg string) (interface{}, error) {
	// Type assertion to access Session's CallMcpTool method
	if sessionWithCallTool, ok := o.Session.(interface {
		CallMcpTool(toolName string, args interface{}, defaultErrorMsg string) (interface{}, error)
	}); ok {
		return sessionWithCallTool.CallMcpTool(toolName, args, defaultErrorMsg)
	}
	return nil, fmt.Errorf("session does not support CallMcpTool method")
}

// Helper function to extract common result fields from CallMcpTool result
func (o *OSSManager) extractCallResult(result interface{}) (string, string, map[string]interface{}, error) {
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

	// Use the session's CallMcpTool method
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
			RequestID: mcpResult.(interface {
				GetRequestID() string
			}).GetRequestID(),
		},
		URL: mcpResult.(interface {
			GetTextContent() string
		}).GetTextContent(),
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
			RequestID: mcpResult.(interface {
				GetRequestID() string
			}).GetRequestID(),
		},
		URL: mcpResult.(interface {
			GetTextContent() string
		}).GetTextContent(),
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
	mcpResult, err := o.callMcpToolHelper("oss_download", args, "error downloading from OSS")
	if err != nil {
		return nil, err
	}

	// Return the result with RequestID
	return &DownloadResult{
		ApiResponse: models.ApiResponse{
			RequestID: mcpResult.(interface {
				GetRequestID() string
			}).GetRequestID(),
		},
		LocalPath: mcpResult.(interface {
			GetTextContent() string
		}).GetTextContent(),
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
	mcpResult, err := o.callMcpToolHelper("oss_download_annon", args, "error downloading anonymously")
	if err != nil {
		return nil, err
	}

	// Return the result with RequestID
	return &DownloadResult{
		ApiResponse: models.ApiResponse{
			RequestID: mcpResult.(interface {
				GetRequestID() string
			}).GetRequestID(),
		},
		LocalPath: mcpResult.(interface {
			GetTextContent() string
		}).GetTextContent(),
	}, nil
}
