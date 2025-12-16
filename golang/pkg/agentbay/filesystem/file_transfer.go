package filesystem

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"path/filepath"
	"strings"
	"time"

	"github.com/alibabacloud-go/tea/tea"
	mcp "github.com/aliyun/wuying-agentbay-sdk/golang/api/client"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/models"
)

// UploadResult represents the result of a file upload operation.
//
// Fields:
//   - Success: Whether the upload completed successfully
//   - RequestIDUploadURL: Request ID from the GetFileUploadUrl API call
//   - RequestIDSync: Request ID from the context sync API call
//   - HTTPStatus: HTTP status code from the OSS upload request
//   - ETag: ETag returned by OSS after successful upload
//   - BytesSent: Number of bytes uploaded
//   - Path: Remote path where the file was uploaded
//   - Error: Error message if the upload failed
type UploadResult struct {
	models.ApiResponse
	Success            bool
	RequestIDUploadURL string
	RequestIDSync      string
	HTTPStatus         int
	ETag               string
	BytesSent          int64
	Path               string
	Error              string
}

// DownloadResult represents the result of a file download operation.
//
// Fields:
//   - Success: Whether the download completed successfully
//   - RequestIDDownloadURL: Request ID from the GetFileDownloadUrl API call
//   - RequestIDSync: Request ID from the context sync API call
//   - HTTPStatus: HTTP status code from the OSS download request
//   - BytesReceived: Number of bytes downloaded
//   - Path: Remote path from which the file was downloaded
//   - LocalPath: Local path where the file was saved
//   - Error: Error message if the download failed
type DownloadResult struct {
	models.ApiResponse
	Success              bool
	RequestIDDownloadURL string
	RequestIDSync        string
	HTTPStatus           int
	BytesReceived        int64
	Path                 string
	LocalPath            string
	Error                string
}

// ProgressCallback is a callback function for tracking file transfer progress.
// It is called periodically during upload or download with the total bytes transferred so far.
type ProgressCallback func(bytesTransferred int64)

// FileTransferOptions contains configuration options for file transfer operations.
//
// Fields:
//   - HTTPTimeout: Timeout for HTTP requests (default: 60s)
//   - FollowRedirects: Whether to follow HTTP redirects (default: true)
//   - Wait: Whether to wait for sync completion (default: true)
//   - WaitTimeout: Maximum time to wait for sync completion (default: 30s for upload, 300s for download)
//   - PollInterval: Interval between sync status polls (default: 1.5s)
//   - ContentType: Content-Type header for uploads (optional)
//   - Overwrite: Whether to overwrite existing local files on download (default: true)
//   - ProgressCB: Callback for progress tracking (optional)
type FileTransferOptions struct {
	HTTPTimeout     time.Duration
	FollowRedirects bool
	Wait            bool
	WaitTimeout     time.Duration
	PollInterval    time.Duration
	ContentType     string
	Overwrite       bool
	ProgressCB      ProgressCallback
}

// DefaultFileTransferOptions returns the default options for file transfer operations.
//
// Default values:
//   - HTTPTimeout: 60 seconds
//   - FollowRedirects: true
//   - Wait: true
//   - WaitTimeout: 30 seconds
//   - PollInterval: 1.5 seconds
//   - Overwrite: true
//
// Example:
//
//	opts := filesystem.DefaultFileTransferOptions()
//	opts.WaitTimeout = 60 * time.Second
//	uploadResult := session.FileSystem.UploadFile("/local/file.txt", "/tmp/file-transfer/file.txt", opts)
func DefaultFileTransferOptions() *FileTransferOptions {
	return &FileTransferOptions{
		HTTPTimeout:     60 * time.Second,
		FollowRedirects: true,
		Wait:            true,
		WaitTimeout:     30 * time.Second,
		PollInterval:    1500 * time.Millisecond,
		Overwrite:       true,
	}
}

// FileTransfer provides file transfer functionality between local filesystem and cloud disk.
//
// It uses OSS pre-signed URLs for efficient file transfers and integrates with the
// Session Context synchronization mechanism to ensure files are properly synced
// between OSS and the cloud disk.
//
// The file transfer context is automatically loaded when first needed. Files must be
// transferred to/from the /tmp/file-transfer/ directory on the cloud disk.
//
// Workflow for Upload:
//  1. Get OSS pre-signed URL via GetFileUploadUrl
//  2. Upload file to OSS using HTTP PUT
//  3. Trigger context sync (download mode) to copy from OSS to cloud disk
//  4. Optionally wait for sync completion
//
// Workflow for Download:
//  1. Trigger context sync (upload mode) to copy from cloud disk to OSS
//  2. Wait for sync completion
//  3. Get OSS pre-signed URL via GetFileDownloadUrl
//  4. Download file from OSS using HTTP GET
type FileTransfer struct {
	session     FileTransferSession
	contextSvc  FileTransferContextService
	httpTimeout time.Duration

	// Lazy-loaded context information
	contextID   string
	contextPath string

	// Task completion states
	finishedStates map[string]bool
}

// FileTransferSession defines the session interface required by FileTransfer
type FileTransferSession interface {
	GetAPIKey() string
	GetClient() *mcp.Client
	GetSessionId() string
}

// FileTransferContextService defines the context service interface required by FileTransfer
type FileTransferContextService interface {
	GetFileUploadUrl(contextID string, filePath string) (*ContextFileUrlResult, error)
	GetFileDownloadUrl(contextID string, filePath string) (*ContextFileUrlResult, error)
}

// ContextFileUrlResult represents a presigned URL operation result.
// This type is defined here to avoid circular imports with the agentbay package.
type ContextFileUrlResult struct {
	models.ApiResponse
	Success      bool
	Url          string
	ExpireTime   *int64
	ErrorMessage string
}

// ContextServiceAdapter wraps the agentbay.ContextService to implement FileTransferContextService.
// This adapter is used to break the circular dependency between filesystem and agentbay packages.
type ContextServiceAdapter struct {
	GetUploadURLFunc   func(contextID string, filePath string) (success bool, url string, errMsg string, requestID string, expireTime *int64, err error)
	GetDownloadURLFunc func(contextID string, filePath string) (success bool, url string, errMsg string, requestID string, expireTime *int64, err error)
}

// GetFileUploadUrl implements FileTransferContextService interface
func (a *ContextServiceAdapter) GetFileUploadUrl(contextID string, filePath string) (*ContextFileUrlResult, error) {
	success, url, errMsg, requestID, expireTime, err := a.GetUploadURLFunc(contextID, filePath)
	if err != nil {
		return nil, err
	}
	return &ContextFileUrlResult{
		ApiResponse:  models.ApiResponse{RequestID: requestID},
		Success:      success,
		Url:          url,
		ErrorMessage: errMsg,
		ExpireTime:   expireTime,
	}, nil
}

// GetFileDownloadUrl implements FileTransferContextService interface
func (a *ContextServiceAdapter) GetFileDownloadUrl(contextID string, filePath string) (*ContextFileUrlResult, error) {
	success, url, errMsg, requestID, expireTime, err := a.GetDownloadURLFunc(contextID, filePath)
	if err != nil {
		return nil, err
	}
	return &ContextFileUrlResult{
		ApiResponse:  models.ApiResponse{RequestID: requestID},
		Success:      success,
		Url:          url,
		ErrorMessage: errMsg,
		ExpireTime:   expireTime,
	}, nil
}

// ContextManager interface for sync and info operations
type ContextManager interface {
	SyncWithParams(contextId, path, mode string) (*ContextSyncResult, error)
	InfoWithParams(contextId, path, taskType string) (*ContextInfoResult, error)
}

// ContextSyncResult wraps context sync result
type ContextSyncResult struct {
	models.ApiResponse
	Success      bool
	ErrorMessage string
}

// ContextInfoResult wraps context info result
type ContextInfoResult struct {
	models.ApiResponse
	Success           bool
	ContextStatusData []ContextStatusData
	ErrorMessage      string
}

// ContextStatusData represents parsed context status data
type ContextStatusData struct {
	ContextId    string `json:"contextId"`
	Path         string `json:"path"`
	ErrorMessage string `json:"errorMessage"`
	Status       string `json:"status"`
	StartTime    int64  `json:"startTime"`
	FinishTime   int64  `json:"finishTime"`
	TaskType     string `json:"taskType"`
}

// NewFileTransfer creates a new FileTransfer instance.
//
// Parameters:
//   - session: Session interface providing API key, client, and session ID
//   - contextSvc: Context service interface for getting presigned URLs
//
// Returns:
//   - *FileTransfer: A new FileTransfer instance ready for upload/download operations
func NewFileTransfer(session FileTransferSession, contextSvc FileTransferContextService) *FileTransfer {
	return &FileTransfer{
		session:     session,
		contextSvc:  contextSvc,
		httpTimeout: 60 * time.Second,
		finishedStates: map[string]bool{
			"success":    true,
			"successful": true,
			"ok":         true,
			"finished":   true,
			"done":       true,
			"completed":  true,
			"complete":   true,
		},
	}
}

// ensureContextID lazy-loads the file_transfer context ID for this session
func (ft *FileTransfer) ensureContextID() (bool, string) {
	if ft.contextID != "" {
		return true, ""
	}

	request := &mcp.GetAndLoadInternalContextRequest{
		Authorization: tea.String("Bearer " + ft.session.GetAPIKey()),
		SessionId:     tea.String(ft.session.GetSessionId()),
		ContextTypes:  []*string{tea.String("file_transfer")},
	}

	fmt.Printf("🔗 API Call: GetAndLoadInternalContext\n")
	fmt.Printf("  └─ SessionId=%s, ContextTypes=file_transfer\n", ft.session.GetSessionId())

	response, err := ft.session.GetClient().GetAndLoadInternalContext(request)
	if err != nil {
		return false, fmt.Sprintf("GetAndLoadInternalContext failed: %v", err)
	}

	if response == nil || response.Body == nil {
		return false, "Empty response from GetAndLoadInternalContext"
	}

	// Check for API-level errors
	if response.Body.Success != nil && !*response.Body.Success {
		errMsg := "Unknown error"
		if response.Body.Message != nil {
			errMsg = *response.Body.Message
		}
		return false, errMsg
	}

	// Extract context_id and context_path from response
	if response.Body.Data != nil && len(response.Body.Data) > 0 {
		for _, item := range response.Body.Data {
			if item != nil {
				contextID := tea.StringValue(item.ContextId)
				contextPath := tea.StringValue(item.ContextPath)
				if contextID != "" && contextPath != "" {
					ft.contextID = contextID
					ft.contextPath = contextPath
					fmt.Printf("✅ Got file transfer context: ID=%s, Path=%s\n", contextID, contextPath)
					return true, ""
				}
			}
		}
	}

	return false, "Response contains no data"
}

// GetContextPath returns the context path for file transfer operations.
//
// The context path is typically /tmp/file-transfer/ and is loaded lazily
// when first accessed. All file transfer operations should use paths
// within this directory.
//
// Returns:
//   - string: The context path (e.g., "/tmp/file-transfer/")
func (ft *FileTransfer) GetContextPath() string {
	if ft.contextID == "" {
		ft.ensureContextID()
	}
	return ft.contextPath
}

// Upload uploads a local file to the remote cloud disk via OSS pre-signed URL.
//
// The upload process involves:
//  1. Getting an OSS pre-signed URL via GetFileUploadUrl
//  2. Uploading the local file to OSS using HTTP PUT
//  3. Triggering context sync (download mode) to copy from OSS to cloud disk
//  4. Optionally waiting for sync completion
//
// Parameters:
//   - localPath: Absolute path to the local file to upload
//   - remotePath: Absolute path on cloud disk (must be under /tmp/file-transfer/)
//   - opts: Transfer options (nil for defaults)
//
// Returns:
//   - *UploadResult: Result containing success status, bytes sent, request IDs, etc.
//
// Example:
//
//	client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
//	result, _ := client.Create(nil)
//	defer result.Session.Delete()
//	uploadResult := result.Session.FileSystem.UploadFile("/local/file.txt", "/tmp/file-transfer/file.txt", nil)
//	if uploadResult.Success {
//		fmt.Printf("Uploaded %d bytes\n", uploadResult.BytesSent)
//	}
func (ft *FileTransfer) Upload(localPath, remotePath string, opts *FileTransferOptions) *UploadResult {
	if opts == nil {
		opts = DefaultFileTransferOptions()
	}

	// 0. Parameter validation
	if _, err := os.Stat(localPath); os.IsNotExist(err) {
		return &UploadResult{
			Success: false,
			Path:    remotePath,
			Error:   fmt.Sprintf("Local file not found: %s", localPath),
		}
	}

	// Ensure context ID is loaded
	if ft.contextID == "" {
		ok, errMsg := ft.ensureContextID()
		if !ok {
			return &UploadResult{
				Success: false,
				Path:    remotePath,
				Error:   errMsg,
			}
		}
	}

	// 1. Get pre-signed upload URL
	urlRes, err := ft.contextSvc.GetFileUploadUrl(ft.contextID, remotePath)
	if err != nil {
		return &UploadResult{
			Success: false,
			Path:    remotePath,
			Error:   fmt.Sprintf("GetFileUploadUrl failed: %v", err),
		}
	}
	if !urlRes.Success || urlRes.Url == "" {
		return &UploadResult{
			Success:            false,
			RequestIDUploadURL: urlRes.RequestID,
			Path:               remotePath,
			Error:              fmt.Sprintf("GetFileUploadUrl failed: %s", urlRes.ErrorMessage),
		}
	}

	uploadURL := urlRes.Url
	reqIDUpload := urlRes.RequestID

	fmt.Printf("Uploading %s to %s\n", localPath, uploadURL)

	// 2. PUT upload to pre-signed URL
	httpStatus, etag, bytesSent, err := ft.putFile(uploadURL, localPath, opts.ContentType, opts.ProgressCB)
	if err != nil {
		return &UploadResult{
			Success:            false,
			RequestIDUploadURL: reqIDUpload,
			Path:               remotePath,
			Error:              fmt.Sprintf("Upload exception: %v", err),
		}
	}

	fmt.Printf("Upload completed with HTTP %d\n", httpStatus)

	if httpStatus != 200 && httpStatus != 201 && httpStatus != 204 {
		return &UploadResult{
			Success:            false,
			RequestIDUploadURL: reqIDUpload,
			HTTPStatus:         httpStatus,
			ETag:               etag,
			BytesSent:          bytesSent,
			Path:               remotePath,
			Error:              fmt.Sprintf("Upload failed with HTTP %d", httpStatus),
		}
	}

	// 3. Trigger sync to cloud disk (download mode), download from OSS to cloud disk
	var reqIDSync string
	fmt.Println("Triggering sync to cloud disk")
	syncResult, err := ft.awaitSync("download", remotePath, ft.contextID)
	if err != nil {
		return &UploadResult{
			Success:            false,
			RequestIDUploadURL: reqIDUpload,
			RequestIDSync:      reqIDSync,
			HTTPStatus:         httpStatus,
			ETag:               etag,
			BytesSent:          bytesSent,
			Path:               remotePath,
			Error:              fmt.Sprintf("session.context.sync(download) failed: %v", err),
		}
	}
	if syncResult != nil {
		reqIDSync = syncResult.RequestID
	}

	fmt.Printf("Sync request ID: %s\n", reqIDSync)

	// 4. Optionally wait for task completion
	if opts.Wait {
		ok, errMsg := ft.waitForTask(ft.contextID, remotePath, "download", opts.WaitTimeout, opts.PollInterval)
		if !ok {
			return &UploadResult{
				Success:            false,
				RequestIDUploadURL: reqIDUpload,
				RequestIDSync:      reqIDSync,
				HTTPStatus:         httpStatus,
				ETag:               etag,
				BytesSent:          bytesSent,
				Path:               remotePath,
				Error:              fmt.Sprintf("Upload sync not finished: %s", errMsg),
			}
		}
	}

	return &UploadResult{
		Success:            true,
		RequestIDUploadURL: reqIDUpload,
		RequestIDSync:      reqIDSync,
		HTTPStatus:         httpStatus,
		ETag:               etag,
		BytesSent:          bytesSent,
		Path:               remotePath,
	}
}

// Download downloads a remote file from cloud disk to local via OSS pre-signed URL.
//
// The download process involves:
//  1. Triggering context sync (upload mode) to copy from cloud disk to OSS
//  2. Waiting for sync completion
//  3. Getting an OSS pre-signed URL via GetFileDownloadUrl
//  4. Downloading the file from OSS using HTTP GET
//
// Parameters:
//   - remotePath: Absolute path on cloud disk (must be under /tmp/file-transfer/)
//   - localPath: Absolute path where the file will be saved locally
//   - opts: Transfer options (nil for defaults with 300s timeout)
//
// Returns:
//   - *DownloadResult: Result containing success status, bytes received, request IDs, etc.
//
// Example:
//
//	client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
//	result, _ := client.Create(nil)
//	defer result.Session.Delete()
//	downloadResult := result.Session.FileSystem.DownloadFile("/tmp/file-transfer/file.txt", "/local/file.txt", nil)
//	if downloadResult.Success {
//		fmt.Printf("Downloaded %d bytes\n", downloadResult.BytesReceived)
//	}
func (ft *FileTransfer) Download(remotePath, localPath string, opts *FileTransferOptions) *DownloadResult {
	if opts == nil {
		opts = DefaultFileTransferOptions()
		opts.WaitTimeout = 300 * time.Second // Default longer timeout for download
	}

	// Ensure context ID is loaded
	if ft.contextID == "" {
		ok, errMsg := ft.ensureContextID()
		if !ok {
			return &DownloadResult{
				Success:   false,
				Path:      remotePath,
				LocalPath: localPath,
				Error:     errMsg,
			}
		}
	}

	// 1. Trigger cloud disk to OSS sync (upload mode)
	var reqIDSync string
	syncResult, err := ft.awaitSync("upload", remotePath, ft.contextID)
	if err != nil {
		return &DownloadResult{
			Success:       false,
			RequestIDSync: reqIDSync,
			Path:          remotePath,
			LocalPath:     localPath,
			Error:         fmt.Sprintf("session.context.sync(upload) failed: %v", err),
		}
	}
	if syncResult != nil {
		reqIDSync = syncResult.RequestID
	}

	// Wait for task completion (ensure object is ready in OSS)
	if opts.Wait {
		ok, errMsg := ft.waitForTask(ft.contextID, remotePath, "upload", opts.WaitTimeout, opts.PollInterval)
		if !ok {
			return &DownloadResult{
				Success:       false,
				RequestIDSync: reqIDSync,
				Path:          remotePath,
				LocalPath:     localPath,
				Error:         fmt.Sprintf("Download sync not finished: %s", errMsg),
			}
		}
	}

	// 2. Get pre-signed download URL
	urlRes, err := ft.contextSvc.GetFileDownloadUrl(ft.contextID, remotePath)
	if err != nil {
		return &DownloadResult{
			Success:       false,
			RequestIDSync: reqIDSync,
			Path:          remotePath,
			LocalPath:     localPath,
			Error:         fmt.Sprintf("GetFileDownloadUrl failed: %v", err),
		}
	}
	if !urlRes.Success || urlRes.Url == "" {
		return &DownloadResult{
			Success:              false,
			RequestIDDownloadURL: urlRes.RequestID,
			RequestIDSync:        reqIDSync,
			Path:                 remotePath,
			LocalPath:            localPath,
			Error:                fmt.Sprintf("GetFileDownloadUrl failed: %s", urlRes.ErrorMessage),
		}
	}

	downloadURL := urlRes.Url
	reqIDDownload := urlRes.RequestID

	// 3. Create parent directory if needed
	parentDir := filepath.Dir(localPath)
	if parentDir != "" && parentDir != "." {
		if err := os.MkdirAll(parentDir, 0755); err != nil {
			return &DownloadResult{
				Success:              false,
				RequestIDDownloadURL: reqIDDownload,
				RequestIDSync:        reqIDSync,
				Path:                 remotePath,
				LocalPath:            localPath,
				Error:                fmt.Sprintf("Failed to create directory: %v", err),
			}
		}
	}

	// Check if file exists and overwrite is disabled
	if !opts.Overwrite {
		if _, err := os.Stat(localPath); err == nil {
			return &DownloadResult{
				Success:              false,
				RequestIDDownloadURL: reqIDDownload,
				RequestIDSync:        reqIDSync,
				Path:                 remotePath,
				LocalPath:            localPath,
				Error:                fmt.Sprintf("Destination exists and Overwrite=false: %s", localPath),
			}
		}
	}

	// 4. Download and save to local
	httpStatus, bytesReceived, err := ft.getFile(downloadURL, localPath, opts.ProgressCB)
	if err != nil {
		return &DownloadResult{
			Success:              false,
			RequestIDDownloadURL: reqIDDownload,
			RequestIDSync:        reqIDSync,
			Path:                 remotePath,
			LocalPath:            localPath,
			Error:                fmt.Sprintf("Download exception: %v", err),
		}
	}

	if httpStatus != 200 {
		return &DownloadResult{
			Success:              false,
			RequestIDDownloadURL: reqIDDownload,
			RequestIDSync:        reqIDSync,
			HTTPStatus:           httpStatus,
			BytesReceived:        bytesReceived,
			Path:                 remotePath,
			LocalPath:            localPath,
			Error:                fmt.Sprintf("Download failed with HTTP %d", httpStatus),
		}
	}

	return &DownloadResult{
		Success:              true,
		RequestIDDownloadURL: reqIDDownload,
		RequestIDSync:        reqIDSync,
		HTTPStatus:           200,
		BytesReceived:        bytesReceived,
		Path:                 remotePath,
		LocalPath:            localPath,
	}
}

// awaitSync triggers context synchronization
func (ft *FileTransfer) awaitSync(mode, remotePath, contextID string) (*ContextSyncResult, error) {
	mode = strings.ToLower(strings.TrimSpace(mode))

	request := &mcp.SyncContextRequest{
		Authorization: tea.String("Bearer " + ft.session.GetAPIKey()),
		SessionId:     tea.String(ft.session.GetSessionId()),
		Mode:          tea.String(mode),
	}

	if contextID != "" {
		request.ContextId = tea.String(contextID)
	}
	if remotePath != "" {
		request.Path = tea.String(remotePath)
	}

	fmt.Printf("session.context.sync(mode=%s, path=%s, context_id=%s)\n", mode, remotePath, contextID)

	response, err := ft.session.GetClient().SyncContext(request)
	if err != nil {
		return nil, err
	}

	requestID := models.ExtractRequestID(response)

	// Check for API-level errors
	if response != nil && response.Body != nil {
		if response.Body.Success != nil && !*response.Body.Success {
			errMsg := "Unknown error"
			if response.Body.Code != nil && response.Body.Message != nil {
				errMsg = fmt.Sprintf("[%s] %s", *response.Body.Code, *response.Body.Message)
			}
			return nil, fmt.Errorf("%s", errMsg)
		}
	}

	success := false
	if response.Body != nil && response.Body.Success != nil {
		success = *response.Body.Success
	}

	fmt.Printf("   Result: %v\n", success)

	return &ContextSyncResult{
		ApiResponse: models.ApiResponse{
			RequestID: requestID,
		},
		Success: success,
	}, nil
}

// waitForTask polls context info to check if specified task is completed
func (ft *FileTransfer) waitForTask(contextID, remotePath, taskType string, timeout, interval time.Duration) (bool, string) {
	deadline := time.Now().Add(timeout)
	var lastErr string

	for time.Now().Before(deadline) {
		// Get context info
		request := &mcp.GetContextInfoRequest{
			Authorization: tea.String("Bearer " + ft.session.GetAPIKey()),
			SessionId:     tea.String(ft.session.GetSessionId()),
		}
		if contextID != "" {
			request.ContextId = tea.String(contextID)
		}
		if remotePath != "" {
			request.Path = tea.String(remotePath)
		}
		if taskType != "" {
			request.TaskType = tea.String(taskType)
		}

		response, err := ft.session.GetClient().GetContextInfo(request)
		if err != nil {
			lastErr = fmt.Sprintf("info error: %v", err)
			time.Sleep(interval)
			continue
		}

		// Parse response and check task status
		if response != nil && response.Body != nil && response.Body.Data != nil {
			contextStatus := tea.StringValue(response.Body.Data.ContextStatus)
			if contextStatus != "" {
				// Parse the status data
				statusData := ft.parseContextStatus(contextStatus)
				for _, item := range statusData {
					if item.ContextId == contextID &&
						item.Path == remotePath &&
						(taskType == "" || item.TaskType == taskType) {
						if item.ErrorMessage != "" {
							return false, fmt.Sprintf("Task error: %s", item.ErrorMessage)
						}
						if ft.finishedStates[strings.ToLower(item.Status)] {
							return true, ""
						}
					}
				}
			}
		}

		lastErr = "task not finished"
		time.Sleep(interval)
	}

	if lastErr == "" {
		lastErr = "timeout"
	}
	return false, lastErr
}

// parseContextStatus parses the context status JSON string
func (ft *FileTransfer) parseContextStatus(contextStatus string) []ContextStatusData {
	var result []ContextStatusData

	// Parse the nested JSON structure
	// Format: [{"type":"data","data":"[{...}]"}]
	type statusItem struct {
		Type string `json:"type"`
		Data string `json:"data"`
	}

	var items []statusItem
	if err := json.Unmarshal([]byte(contextStatus), &items); err != nil {
		return result
	}

	for _, item := range items {
		if item.Type == "data" {
			var dataItems []ContextStatusData
			if err := json.Unmarshal([]byte(item.Data), &dataItems); err == nil {
				result = append(result, dataItems...)
			}
		}
	}

	return result
}

// putFile uploads a file to the pre-signed URL
func (ft *FileTransfer) putFile(url, filePath, contentType string, progressCB ProgressCallback) (int, string, int64, error) {
	file, err := os.Open(filePath)
	if err != nil {
		return 0, "", 0, err
	}
	defer file.Close()

	fileInfo, err := file.Stat()
	if err != nil {
		return 0, "", 0, err
	}
	fileSize := fileInfo.Size()

	req, err := http.NewRequest(http.MethodPut, url, file)
	if err != nil {
		return 0, "", 0, err
	}

	req.ContentLength = fileSize
	if contentType != "" {
		req.Header.Set("Content-Type", contentType)
	}

	client := &http.Client{
		Timeout: ft.httpTimeout,
	}

	resp, err := client.Do(req)
	if err != nil {
		return 0, "", 0, err
	}
	defer resp.Body.Close()

	// Read response body to complete the request
	io.Copy(io.Discard, resp.Body)

	etag := resp.Header.Get("ETag")
	return resp.StatusCode, etag, fileSize, nil
}

// getFile downloads a file from the pre-signed URL
func (ft *FileTransfer) getFile(url, destPath string, progressCB ProgressCallback) (int, int64, error) {
	client := &http.Client{
		Timeout: ft.httpTimeout,
	}

	resp, err := client.Get(url)
	if err != nil {
		return 0, 0, err
	}
	defer resp.Body.Close()

	if resp.StatusCode != 200 {
		io.Copy(io.Discard, resp.Body)
		return resp.StatusCode, 0, nil
	}

	file, err := os.Create(destPath)
	if err != nil {
		return resp.StatusCode, 0, err
	}
	defer file.Close()

	var bytesReceived int64
	buf := make([]byte, 32*1024) // 32KB buffer
	for {
		n, err := resp.Body.Read(buf)
		if n > 0 {
			_, writeErr := file.Write(buf[:n])
			if writeErr != nil {
				return resp.StatusCode, bytesReceived, writeErr
			}
			bytesReceived += int64(n)
			if progressCB != nil {
				progressCB(bytesReceived)
			}
		}
		if err == io.EOF {
			break
		}
		if err != nil {
			return resp.StatusCode, bytesReceived, err
		}
	}

	return 200, bytesReceived, nil
}
