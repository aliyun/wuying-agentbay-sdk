package oss

import (
	"fmt"

	mcp "github.com/aliyun/wuying-agentbay-sdk/golang/api/client"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/models"
)

// EnvInitResult represents the result of OSS environment initialization
type EnvInitResult struct {
	models.ApiResponse
	Result string
}

// UploadResult represents the result of a file upload operation
type UploadResult struct {
	models.ApiResponse
	URL string
}

// DownloadResult represents the result of a file download operation
type DownloadResult struct {
	models.ApiResponse
	LocalPath string
}

// OSSManager handles Object Storage Service operations in the AgentBay cloud environment
type OSSManager struct {
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

// NewOss creates a new OSS manager instance
func NewOss(session interface {
	GetAPIKey() string
	GetClient() *mcp.Client
	GetSessionId() string
	IsVpc() bool
	NetworkInterfaceIp() string
	HttpPort() string
	FindServerForTool(toolName string) string
	CallMcpTool(toolName string, args interface{}, autoGenSession ...bool) (*models.McpToolResult, error)
}) *OSSManager {
	return &OSSManager{
		Session: session,
	}
}

// EnvInit initializes OSS environment variables with STS temporary credentials.
// All three credential parameters (accessKeyId, accessKeySecret, securityToken) are required for security.
//
// Example:
//
//	client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
//	result, _ := client.Create(nil)
//	defer result.Session.Delete()
//	ossResult, _ := result.Session.Oss.EnvInit("stsAccessKeyId", "stsAccessKeySecret", "stsToken", "endpoint", "cn-hangzhou")
func (o *OSSManager) EnvInit(accessKeyId, accessKeySecret, securityToken, endpoint, region string) (*EnvInitResult, error) {
	// Build arguments map
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

	result, err := o.Session.CallMcpTool("oss_env_init", args)
	if err != nil {
		return nil, fmt.Errorf("error initializing OSS environment: %w", err)
	}

	return &EnvInitResult{
		ApiResponse: models.ApiResponse{
			RequestID: result.RequestID,
		},
		Result: result.Data,
	}, nil
}

// Upload uploads a local file or directory to the specified OSS bucket
//
// Note: Before calling this API, you must call EnvInit to initialize the OSS environment.
//
// Example:
//
//	client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
//	result, _ := client.Create(nil)
//	defer result.Session.Delete()
//	result.Session.Oss.EnvInit("accessKeyId", "accessKeySecret", "token", "endpoint", "cn-hangzhou")
//	uploadResult, _ := result.Session.Oss.Upload("my-bucket", "my-object", "/tmp/file.txt")
func (o *OSSManager) Upload(bucket, object, path string) (*UploadResult, error) {
	args := map[string]interface{}{
		"bucket": bucket,
		"object": object,
		"path":   path,
	}

	result, err := o.Session.CallMcpTool("oss_upload", args)
	if err != nil {
		return nil, fmt.Errorf("error uploading to OSS: %w", err)
	}

	return &UploadResult{
		ApiResponse: models.ApiResponse{
			RequestID: result.RequestID,
		},
		URL: result.Data,
	}, nil
}

// UploadAnonymous uploads a local file or directory to the specified URL using HTTP PUT
//
// Note: Before calling this API, you must call EnvInit to initialize the OSS environment.
//
// Example:
//
//	client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
//	result, _ := client.Create(nil)
//	defer result.Session.Delete()
//	result.Session.Oss.EnvInit("accessKeyId", "accessKeySecret", "token", "endpoint", "cn-hangzhou")
//	uploadResult, _ := result.Session.Oss.UploadAnonymous("https://example.com/upload", "/tmp/file.txt")
func (o *OSSManager) UploadAnonymous(url, path string) (*UploadResult, error) {
	args := map[string]interface{}{
		"url":  url,
		"path": path,
	}

	result, err := o.Session.CallMcpTool("oss_upload_annon", args)
	if err != nil {
		return nil, fmt.Errorf("error uploading anonymously: %w", err)
	}

	return &UploadResult{
		ApiResponse: models.ApiResponse{
			RequestID: result.RequestID,
		},
		URL: result.Data,
	}, nil
}

// Download downloads an object from the specified OSS bucket to the given local path
//
// Note: Before calling this API, you must call EnvInit to initialize the OSS environment.
//
// Example:
//
//	client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
//	result, _ := client.Create(nil)
//	defer result.Session.Delete()
//	result.Session.Oss.EnvInit("accessKeyId", "accessKeySecret", "token", "endpoint", "cn-hangzhou")
//	downloadResult, _ := result.Session.Oss.Download("my-bucket", "my-object", "/tmp/file.txt")
func (o *OSSManager) Download(bucket, object, path string) (*DownloadResult, error) {
	args := map[string]interface{}{
		"bucket": bucket,
		"object": object,
		"path":   path,
	}

	result, err := o.Session.CallMcpTool("oss_download", args)
	if err != nil {
		return nil, fmt.Errorf("error downloading from OSS: %w", err)
	}

	return &DownloadResult{
		ApiResponse: models.ApiResponse{
			RequestID: result.RequestID,
		},
		LocalPath: path,
	}, nil
}

// DownloadAnonymous downloads a file from the specified URL to the given local path
//
// Note: Before calling this API, you must call EnvInit to initialize the OSS environment.
//
// Example:
//
//	client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
//	result, _ := client.Create(nil)
//	defer result.Session.Delete()
//	result.Session.Oss.EnvInit("accessKeyId", "accessKeySecret", "token", "endpoint", "cn-hangzhou")
//	downloadResult, _ := result.Session.Oss.DownloadAnonymous("https://example.com/file.txt", "/tmp/file.txt")
func (o *OSSManager) DownloadAnonymous(url, path string) (*DownloadResult, error) {
	args := map[string]interface{}{
		"url":  url,
		"path": path,
	}

	result, err := o.Session.CallMcpTool("oss_download_annon", args)
	if err != nil {
		return nil, fmt.Errorf("error downloading anonymously: %w", err)
	}

	return &DownloadResult{
		ApiResponse: models.ApiResponse{
			RequestID: result.RequestID,
		},
		LocalPath: path,
	}, nil
}
