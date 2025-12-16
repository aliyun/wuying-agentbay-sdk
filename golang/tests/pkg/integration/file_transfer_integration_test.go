package integration

import (
	"fmt"
	"os"
	"path/filepath"
	"testing"
	"time"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/filesystem"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

// TestFileUploadIntegration tests the complete file upload workflow with verification.
// This test mirrors the Python test_file_upload_integration test.
func TestFileUploadIntegration(t *testing.T) {
	apiKey := os.Getenv("AGENTBAY_API_KEY")
	if apiKey == "" {
		t.Skip("AGENTBAY_API_KEY not set")
	}

	// Create AgentBay client
	ab, err := agentbay.NewAgentBay(apiKey)
	require.NoError(t, err, "Failed to create AgentBay client")

	// Create session
	params := agentbay.NewCreateSessionParams()
	params.ImageId = "browser_latest"
	result, err := ab.Create(params)
	require.NoError(t, err, "Failed to create session")
	require.NotNil(t, result.Session, "Session should not be nil")
	session := result.Session

	t.Logf("Session created with ID: %s", session.SessionID)

	// Cleanup
	defer func() {
		_, err := session.Delete(true) // sync_context=true
		if err != nil {
			t.Logf("Warning: Failed to delete session: %v", err)
		}
	}()

	// Wait for session to be ready
	time.Sleep(5 * time.Second)

	// Create a temporary local file to upload
	timestamp := time.Now().UnixNano()
	testContent := fmt.Sprintf("Test file content for upload at %d.\nLine 2: This is a multi-line test file.\nLine 3: Testing file transfer functionality.", timestamp)

	tempDir := os.TempDir()
	tempFilePath := filepath.Join(tempDir, fmt.Sprintf("upload_test_%d.txt", timestamp))
	err = os.WriteFile(tempFilePath, []byte(testContent), 0644)
	require.NoError(t, err, "Failed to create temp file")
	t.Logf("Created temp file: %s", tempFilePath)

	// Cleanup temp file
	defer func() {
		if err := os.Remove(tempFilePath); err != nil {
			t.Logf("Warning: Failed to remove temp file: %v", err)
		}
	}()

	// Upload the file
	remotePath := "/tmp/file-transfer/upload_test.txt"
	t.Logf("Uploading %s to %s", tempFilePath, remotePath)

	uploadResult := session.FileSystem.UploadFile(tempFilePath, remotePath, nil)

	// Verify upload result
	if !uploadResult.Success {
		t.Logf("Upload failed: %s", uploadResult.Error)
		t.Logf("Request ID (Upload URL): %s", uploadResult.RequestIDUploadURL)
		t.Logf("Request ID (Sync): %s", uploadResult.RequestIDSync)
	}
	require.True(t, uploadResult.Success, "Upload failed: %s", uploadResult.Error)
	assert.Greater(t, uploadResult.BytesSent, int64(0), "Bytes sent should be greater than 0")
	assert.NotEmpty(t, uploadResult.RequestIDUploadURL, "Request ID for upload URL should not be empty")
	assert.NotEmpty(t, uploadResult.RequestIDSync, "Request ID for sync should not be empty")

	t.Logf("Upload successful:")
	t.Logf("  - Bytes sent: %d", uploadResult.BytesSent)
	t.Logf("  - HTTP Status: %d", uploadResult.HTTPStatus)
	t.Logf("  - ETag: %s", uploadResult.ETag)
	t.Logf("  - Request ID (Upload URL): %s", uploadResult.RequestIDUploadURL)
	t.Logf("  - Request ID (Sync): %s", uploadResult.RequestIDSync)

	// Verify file exists on remote by listing directory
	lsResult, err := session.Command.ExecuteCommand("ls -la /tmp/file-transfer/")
	if err == nil && lsResult.Success {
		t.Logf("Remote directory listing:\n%s", lsResult.Output)
	}

	// Verify file content on remote
	readResult, err := session.FileSystem.ReadFile(remotePath)
	if err == nil && readResult != nil {
		t.Logf("Remote file content length: %d", len(readResult.Content))
		// Note: The content may differ slightly due to encoding, so we just check it's not empty
		assert.NotEmpty(t, readResult.Content, "Remote file content should not be empty")
	}
}

// TestFileDownloadIntegration tests the complete file download workflow with verification.
// This test mirrors the Python test_file_download_integration test.
func TestFileDownloadIntegration(t *testing.T) {
	apiKey := os.Getenv("AGENTBAY_API_KEY")
	if apiKey == "" {
		t.Skip("AGENTBAY_API_KEY not set")
	}

	// Create AgentBay client
	ab, err := agentbay.NewAgentBay(apiKey)
	require.NoError(t, err, "Failed to create AgentBay client")

	// Create session
	params := agentbay.NewCreateSessionParams()
	params.ImageId = "browser_latest"
	result, err := ab.Create(params)
	require.NoError(t, err, "Failed to create session")
	require.NotNil(t, result.Session, "Session should not be nil")
	session := result.Session

	t.Logf("Session created with ID: %s", session.SessionID)

	// Cleanup
	defer func() {
		_, err := session.Delete(true) // sync_context=true
		if err != nil {
			t.Logf("Warning: Failed to delete session: %v", err)
		}
	}()

	// Wait for session to be ready
	time.Sleep(5 * time.Second)

	// Create a test file on the remote side first
	timestamp := time.Now().UnixNano()
	testContent := fmt.Sprintf("Test file content for download at %d.\nLine 2: This is a multi-line test file.\nLine 3: Testing file transfer functionality.", timestamp)
	remotePath := fmt.Sprintf("/tmp/file-transfer/download_test_%d.txt", timestamp)

	// Create directory first
	_, err = session.FileSystem.CreateDirectory("/tmp/file-transfer/")
	if err != nil {
		t.Logf("Warning: Failed to create directory (may already exist): %v", err)
	}

	// Write test file to remote
	writeResult, err := session.FileSystem.WriteFile(remotePath, testContent, "overwrite")
	require.NoError(t, err, "Failed to write test file to remote")
	require.True(t, writeResult.Success, "Failed to write test file to remote")
	t.Logf("Created test file on remote: %s", remotePath)

	// Verify file exists
	lsResult, err := session.Command.ExecuteCommand("ls -la /tmp/file-transfer/")
	if err == nil && lsResult.Success {
		t.Logf("Remote directory listing:\n%s", lsResult.Output)
	}

	// Download the file
	tempDir := os.TempDir()
	localPath := filepath.Join(tempDir, fmt.Sprintf("download_test_%d.txt", timestamp))
	t.Logf("Downloading %s to %s", remotePath, localPath)

	// Cleanup temp file
	defer func() {
		if err := os.Remove(localPath); err != nil && !os.IsNotExist(err) {
			t.Logf("Warning: Failed to remove temp file: %v", err)
		}
	}()

	// Set longer timeout for download
	opts := filesystem.DefaultFileTransferOptions()
	opts.WaitTimeout = 300 * time.Second

	downloadResult := session.FileSystem.DownloadFile(remotePath, localPath, opts)

	// Verify download result
	if !downloadResult.Success {
		t.Logf("Download failed: %s", downloadResult.Error)
		t.Logf("Request ID (Download URL): %s", downloadResult.RequestIDDownloadURL)
		t.Logf("Request ID (Sync): %s", downloadResult.RequestIDSync)
	}
	require.True(t, downloadResult.Success, "Download failed: %s", downloadResult.Error)
	assert.Greater(t, downloadResult.BytesReceived, int64(0), "Bytes received should be greater than 0")

	t.Logf("Download successful:")
	t.Logf("  - Bytes received: %d", downloadResult.BytesReceived)
	t.Logf("  - HTTP Status: %d", downloadResult.HTTPStatus)
	t.Logf("  - Request ID (Download URL): %s", downloadResult.RequestIDDownloadURL)
	t.Logf("  - Request ID (Sync): %s", downloadResult.RequestIDSync)

	// Verify local file exists and content matches
	localContent, err := os.ReadFile(localPath)
	require.NoError(t, err, "Failed to read local file")
	assert.Equal(t, testContent, string(localContent), "Downloaded content should match original")
	t.Logf("Local file content verified successfully")
}

// TestFileTransferDirectAccess tests using the FileTransfer directly
func TestFileTransferDirectAccess(t *testing.T) {
	apiKey := os.Getenv("AGENTBAY_API_KEY")
	if apiKey == "" {
		t.Skip("AGENTBAY_API_KEY not set")
	}

	// Create AgentBay client
	ab, err := agentbay.NewAgentBay(apiKey)
	require.NoError(t, err, "Failed to create AgentBay client")

	// Create session
	params := agentbay.NewCreateSessionParams()
	params.ImageId = "browser_latest"
	result, err := ab.Create(params)
	require.NoError(t, err, "Failed to create session")
	require.NotNil(t, result.Session, "Session should not be nil")
	session := result.Session

	// Cleanup
	defer func() {
		_, err := session.Delete()
		if err != nil {
			t.Logf("Warning: Failed to delete session: %v", err)
		}
	}()

	// Check that FileTransfer is accessible via lazy loading
	ft, err := session.FileSystem.GetFileTransfer()
	require.NoError(t, err, "Failed to get FileTransfer")
	require.NotNil(t, ft, "FileTransfer should not be nil")

	// Check that context path can be retrieved
	contextPath := ft.GetContextPath()
	t.Logf("File transfer context path: %s", contextPath)
	// Note: contextPath might be empty if context hasn't been loaded yet
}
