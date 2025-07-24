package filesystem

import (
	"encoding/json"
	"fmt"
	"strings"

	mcp "github.com/aliyun/wuying-agentbay-sdk/golang/api/client"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/models"
)

// FileReadResult wraps file read operation result and RequestID
type FileReadResult struct {
	models.ApiResponse // Embedded ApiResponse
	Content            string
}

// FileWriteResult wraps file write operation result and RequestID
type FileWriteResult struct {
	models.ApiResponse // Embedded ApiResponse
	Success            bool
}

// FileExistsResult wraps file existence check result and RequestID
type FileExistsResult struct {
	models.ApiResponse
	Exists bool
}

// FileDirectoryResult wraps directory operation result and RequestID
type FileDirectoryResult struct {
	models.ApiResponse // Embedded ApiResponse
	Success            bool
}

// DirectoryListResult wraps directory listing result and RequestID
type DirectoryListResult struct {
	models.ApiResponse
	Entries []*DirectoryEntry
}

// FileInfoResult wraps file info result and RequestID
type FileInfoResult struct {
	models.ApiResponse
	FileInfo *FileInfo
}

// SearchFilesResult wraps file search result and RequestID
type SearchFilesResult struct {
	models.ApiResponse
	Results []string
}

// FileSystem handles file system operations in the AgentBay cloud environment.
type FileSystem struct {
	Session interface {
		GetAPIKey() string
		GetClient() *mcp.Client
		GetSessionId() string
	}
}

// FileInfo represents file or directory information
type FileInfo struct {
	Name        string `json:"name"`
	Path        string `json:"path"`
	Size        int64  `json:"size"`
	IsDirectory bool   `json:"isDirectory"`
	ModTime     string `json:"modTime"`
	Mode        string `json:"mode"`
	Owner       string `json:"owner,omitempty"`
	Group       string `json:"group,omitempty"`
}

// DirectoryEntry represents a directory entry
type DirectoryEntry struct {
	Name        string `json:"name"`
	IsDirectory bool   `json:"isDirectory"`
}

// callMcpToolHelper is a helper that calls the session's CallMcpTool method
func (fs *FileSystem) callMcpToolHelper(toolName string, args interface{}, defaultErrorMsg string) (interface{}, error) {
	// Type assertion to access Session's CallMcpTool method
	if sessionWithCallTool, ok := fs.Session.(interface {
		CallMcpTool(toolName string, args interface{}, defaultErrorMsg string) (interface{}, error)
	}); ok {
		return sessionWithCallTool.CallMcpTool(toolName, args, defaultErrorMsg)
	}
	return nil, fmt.Errorf("session does not support CallMcpTool method")
}

// Helper function to extract common result fields from CallMcpTool result
func (fs *FileSystem) extractCallResult(result interface{}) (string, string, map[string]interface{}, error) {
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

// Helper function to check if a tool name is a file operation
func isFileOperation(toolName string) bool {
	fileOperations := []string{
		"read_file", "write_file", "read_multiple_files", "read_large_file", "write_large_file",
		"edit_file", "get_file_info", "search_files",
	}
	for _, op := range fileOperations {
		if op == toolName {
			return true
		}
	}
	return false
}

// Helper function to truncate content for logging
func truncateContentForLogging(jsonArgs string) string {
	const maxLength = 200
	if len(jsonArgs) <= maxLength {
		return jsonArgs
	}
	return jsonArgs[:maxLength] + "... (truncated)"
}

// Helper function to parse file info from string
func parseFileInfo(fileInfoStr string) (*FileInfo, error) {
	var fileInfo FileInfo
	err := json.Unmarshal([]byte(fileInfoStr), &fileInfo)
	if err != nil {
		return nil, fmt.Errorf("failed to parse file info: %w", err)
	}
	return &fileInfo, nil
}

// Helper function to parse directory listing from string
func parseDirectoryListing(text string) ([]*DirectoryEntry, error) {
	var entries []*DirectoryEntry
	err := json.Unmarshal([]byte(text), &entries)
	if err != nil {
		return nil, fmt.Errorf("failed to parse directory listing: %w", err)
	}
	return entries, nil
}

// NewFileSystem creates a new FileSystem instance
func NewFileSystem(session interface {
	GetAPIKey() string
	GetClient() *mcp.Client
	GetSessionId() string
}) *FileSystem {
	return &FileSystem{
		Session: session,
	}
}

// CreateDirectory creates a new directory.
// API Parameters:
//
//	{
//	  "path": "directory/path/to/create"
//	}
func (fs *FileSystem) CreateDirectory(path string) (*FileDirectoryResult, error) {
	args := map[string]string{
		"path": path,
	}

	// Use the session's CallMcpTool method
	result, err := fs.callMcpToolHelper("create_directory", args, "error creating directory")
	if err != nil {
		return nil, err
	}

	// Extract result fields using helper
	requestID, _, _, err := fs.extractCallResult(result)
	if err != nil {
		return nil, err
	}

	// Return result with RequestID
	return &FileDirectoryResult{
		ApiResponse: models.ApiResponse{
			RequestID: requestID,
		},
		Success: true,
	}, nil
}

// EditFile edits a file with specified changes.
// API Parameters:
//
//	{
//	  "path": "file/path/to/edit",
//	  "edits": [
//	    {
//	      "type": "insert",
//	      "line": 1,
//	      "content": "new content"
//	    }
//	  ],
//	  "dry_run": false
//	}
func (fs *FileSystem) EditFile(path string, edits []map[string]string, dryRun bool) (*FileWriteResult, error) {
	args := map[string]interface{}{
		"path":    path,
		"edits":   edits,
		"dry_run": dryRun,
	}

	// Use the session's CallMcpTool method
	result, err := fs.callMcpToolHelper("edit_file", args, "error editing file")
	if err != nil {
		return nil, err
	}

	// Extract result fields using helper
	requestID, _, _, err := fs.extractCallResult(result)
	if err != nil {
		return nil, err
	}

	// Return result with RequestID
	return &FileWriteResult{
		ApiResponse: models.ApiResponse{
			RequestID: requestID,
		},
		Success: true,
	}, nil
}

// GetFileInfo gets information about a file or directory.
// API Parameters:
//
//	{
//	  "path": "file/or/directory/path"
//	}
func (fs *FileSystem) GetFileInfo(path string) (*FileInfoResult, error) {
	args := map[string]string{
		"path": path,
	}

	// Use the session's CallMcpTool method
	result, err := fs.callMcpToolHelper("get_file_info", args, "error getting file info")
	if err != nil {
		// Check if it's a "file not found" error
		if strings.Contains(err.Error(), "No such file or directory") {
			return nil, fmt.Errorf("file not found: %s", path)
		}
		return nil, err
	}

	// Extract result fields using helper
	requestID, textContent, _, err := fs.extractCallResult(result)
	if err != nil {
		return nil, err
	}

	fileInfo, err := parseFileInfo(textContent)
	if err != nil {
		return nil, fmt.Errorf("error parsing file info: %w", err)
	}

	// Return result with RequestID
	return &FileInfoResult{
		ApiResponse: models.ApiResponse{
			RequestID: requestID,
		},
		FileInfo: fileInfo,
	}, nil
}

// ListDirectory lists the contents of a directory.
// API Parameters:
//
//	{
//	  "path": "directory/path/to/list"
//	}
func (fs *FileSystem) ListDirectory(path string) (*DirectoryListResult, error) {
	args := map[string]string{
		"path": path,
	}

	// Use the session's CallMcpTool method
	result, err := fs.callMcpToolHelper("list_directory", args, "error listing directory")
	if err != nil {
		return nil, err
	}

	// Extract result fields using helper
	requestID, textContent, _, err := fs.extractCallResult(result)
	if err != nil {
		return nil, err
	}

	entries, err := parseDirectoryListing(textContent)
	if err != nil {
		return nil, fmt.Errorf("error parsing directory listing: %w", err)
	}

	// Return result with RequestID
	return &DirectoryListResult{
		ApiResponse: models.ApiResponse{
			RequestID: requestID,
		},
		Entries: entries,
	}, nil
}

// MoveFile moves a file or directory from source to destination.
// API Parameters:
//
//	{
//	  "source": "source/file/or/directory/path",
//	  "destination": "destination/file/or/directory/path"
//	}
func (fs *FileSystem) MoveFile(source, destination string) (*FileWriteResult, error) {
	args := map[string]string{
		"source":      source,
		"destination": destination,
	}

	// Use the session's CallMcpTool method
	result, err := fs.callMcpToolHelper("move_file", args, "error moving file")
	if err != nil {
		return nil, err
	}

	// Extract result fields using helper
	requestID, _, _, err := fs.extractCallResult(result)
	if err != nil {
		return nil, err
	}

	// Return result with RequestID
	return &FileWriteResult{
		ApiResponse: models.ApiResponse{
			RequestID: requestID,
		},
		Success: true,
	}, nil
}

// ReadFile reads the contents of a file.
// API Parameters:
//
//	{
//	  "path": "file/path/to/read",
//	  "offset": 0,  // Optional: Starting offset for reading
//	  "length": 0   // Optional: Number of bytes to read (0 means read all)
//	}
func (fs *FileSystem) ReadFile(path string, optionalParams ...int) (*FileReadResult, error) {
	// Handle optional parameters for backward compatibility
	offset, length := 0, 0
	if len(optionalParams) > 0 {
		offset = optionalParams[0]
	}
	if len(optionalParams) > 1 {
		length = optionalParams[1]
	}

	args := map[string]interface{}{
		"path": path,
	}
	if offset > 0 {
		args["offset"] = offset
	}
	if length > 0 {
		args["length"] = length
	}

	// Use the session's CallMcpTool method
	result, err := fs.callMcpToolHelper("read_file", args, "error reading file")
	if err != nil {
		return nil, err
	}

	// Extract result fields using helper
	requestID, textContent, _, err := fs.extractCallResult(result)
	if err != nil {
		return nil, err
	}

	// Return result with RequestID
	return &FileReadResult{
		ApiResponse: models.ApiResponse{
			RequestID: requestID,
		},
		Content: textContent,
	}, nil
}

// ReadMultipleFiles reads multiple files and returns their contents as a map.
// API Parameters:
//
//	{
//	  "paths": ["file1.txt", "file2.txt", "file3.txt"]
//	}
func (fs *FileSystem) ReadMultipleFiles(paths []string) (map[string]string, error) {
	args := map[string]interface{}{
		"paths": paths,
	}

	// Use the session's CallMcpTool method
	result, err := fs.callMcpToolHelper("read_multiple_files", args, "error reading multiple files")
	if err != nil {
		return nil, err
	}

	// Extract result fields using helper
	_, textContent, _, err := fs.extractCallResult(result)
	if err != nil {
		return nil, err
	}

	// Parse the result
	lines := strings.Split(textContent, "\n")
	fileContents := make(map[string]string)

	for _, line := range lines {
		line = strings.TrimSpace(line)
		if line == "" {
			continue
		}

		// Parse each line as "path:content"
		parts := strings.SplitN(line, ":", 2)
		if len(parts) == 2 {
			filePath := strings.TrimSpace(parts[0])
			content := strings.TrimSpace(parts[1])
			fileContents[filePath] = content
		}
	}

	return fileContents, nil
}

// SearchFiles searches for files matching a pattern.
// API Parameters:
//
//	{
//	  "path": "directory/path/to/search",
//	  "pattern": "*.txt",
//	  "exclude_patterns": ["*.tmp", "*.log"]
//	}
func (fs *FileSystem) SearchFiles(path, pattern string, excludePatterns []string) (*SearchFilesResult, error) {
	args := map[string]interface{}{
		"path":             path,
		"pattern":          pattern,
		"exclude_patterns": excludePatterns,
	}

	// Use the session's CallMcpTool method
	result, err := fs.callMcpToolHelper("search_files", args, "error searching files")
	if err != nil {
		return nil, err
	}

	// Extract result fields using helper
	requestID, textContent, _, err := fs.extractCallResult(result)
	if err != nil {
		return nil, err
	}

	// Parse the result
	var results []string
	for _, line := range strings.Split(textContent, "\n") {
		line = strings.TrimSpace(line)
		if line != "" {
			results = append(results, line)
		}
	}

	// Return result with RequestID
	return &SearchFilesResult{
		ApiResponse: models.ApiResponse{
			RequestID: requestID,
		},
		Results: results,
	}, nil
}

// WriteFile writes content to a file.
// API Parameters:
//
//	{
//	  "path": "file/path/to/write",
//	  "content": "file content",
//	  "mode": "0644"  // Optional: File permissions
//	}
func (fs *FileSystem) WriteFile(path, content string, mode string) (*FileWriteResult, error) {
	args := map[string]interface{}{
		"path":    path,
		"content": content,
	}
	if mode != "" {
		args["mode"] = mode
	}

	// Use the session's CallMcpTool method
	result, err := fs.callMcpToolHelper("write_file", args, "error writing file")
	if err != nil {
		return nil, err
	}

	// Extract result fields using helper
	requestID, _, _, err := fs.extractCallResult(result)
	if err != nil {
		return nil, err
	}

	// Return result with RequestID
	return &FileWriteResult{
		ApiResponse: models.ApiResponse{
			RequestID: requestID,
		},
		Success: true,
	}, nil
}

// ReadLargeFile reads a large file in chunks.
// API Parameters:
//
//	{
//	  "path": "large/file/path",
//	  "chunk_size": 8192
//	}
func (fs *FileSystem) ReadLargeFile(path string, chunkSize int) (*FileReadResult, error) {
	args := map[string]interface{}{
		"path":       path,
		"chunk_size": chunkSize,
	}

	// Use the session's CallMcpTool method
	result, err := fs.callMcpToolHelper("read_large_file", args, "error reading large file")
	if err != nil {
		return nil, err
	}

	// Extract result fields using helper
	requestID, textContent, _, err := fs.extractCallResult(result)
	if err != nil {
		return nil, err
	}

	// Return result with RequestID
	return &FileReadResult{
		ApiResponse: models.ApiResponse{
			RequestID: requestID,
		},
		Content: textContent,
	}, nil
}

// WriteLargeFile writes content to a file in chunks.
// API Parameters:
//
//	{
//	  "path": "large/file/path",
//	  "content": "large file content",
//	  "chunk_size": 8192
//	}
func (fs *FileSystem) WriteLargeFile(path, content string, chunkSize int) (*FileWriteResult, error) {
	args := map[string]interface{}{
		"path":       path,
		"content":    content,
		"chunk_size": chunkSize,
	}

	// Use the session's CallMcpTool method
	result, err := fs.callMcpToolHelper("write_large_file", args, "error writing large file")
	if err != nil {
		return nil, err
	}

	// Extract result fields using helper
	requestID, _, _, err := fs.extractCallResult(result)
	if err != nil {
		return nil, err
	}

	// Return result with RequestID
	return &FileWriteResult{
		ApiResponse: models.ApiResponse{
			RequestID: requestID,
		},
		Success: true,
	}, nil
}
