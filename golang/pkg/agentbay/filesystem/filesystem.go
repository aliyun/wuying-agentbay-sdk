package filesystem

import (
	"encoding/json"
	"fmt"
	"net/http"
	"strings"
	"time"

	"github.com/alibabacloud-go/tea/tea"
	mcp "github.com/aliyun/wuying-agentbay-sdk/golang/api/client"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/models"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/utils"
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

// FileSystem handles file system operations in the AgentBay cloud environment.
type FileSystem struct {
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

// CallMcpTool calls the MCP tool and handles both VPC and non-VPC scenarios
func (fs *FileSystem) CallMcpTool(toolName string, args interface{}, defaultErrorMsg string) (*CallMcpToolResult, error) {
	// Marshal arguments to JSON
	argsJSON, err := json.Marshal(args)
	if err != nil {
		return nil, fmt.Errorf("failed to marshal args: %w", err)
	}

	// Check if this is a VPC session
	if fs.Session.IsVpc() {
		return fs.callMcpToolVPC(toolName, string(argsJSON), defaultErrorMsg)
	}

	// Non-VPC mode: use traditional API call
	return fs.callMcpToolAPI(toolName, string(argsJSON), defaultErrorMsg)
}

// callMcpToolVPC handles VPC-based MCP tool calls
func (fs *FileSystem) callMcpToolVPC(toolName, argsJSON, defaultErrorMsg string) (*CallMcpToolResult, error) {
	// VPC mode: Use HTTP request to the VPC endpoint
	fmt.Println("API Call: CallMcpTool (VPC) -", toolName)
	fmt.Printf("Request: Args=%s\n", argsJSON)

	// Find server for this tool
	server := fs.Session.FindServerForTool(toolName)
	if server == "" {
		return nil, fmt.Errorf("server not found for tool: %s", toolName)
	}

	// Construct VPC URL with query parameters
	baseURL := fmt.Sprintf("http://%s:%s/callTool", fs.Session.NetworkInterfaceIp(), fs.Session.HttpPort())

	// Create URL with query parameters
	req, err := http.NewRequest("GET", baseURL, nil)
	if err != nil {
		return nil, fmt.Errorf("failed to create VPC HTTP request: %w", err)
	}

	// Add query parameters
	q := req.URL.Query()
	q.Add("server", server)
	q.Add("tool", toolName)
	q.Add("args", argsJSON)
	q.Add("apiKey", fs.Session.GetAPIKey())
	req.URL.RawQuery = q.Encode()

	// Set content type header
	req.Header.Set("Content-Type", "application/x-www-form-urlencoded")

	// Send HTTP request
	client := &http.Client{Timeout: 30 * time.Second}
	resp, err := client.Do(req)
	if err != nil {
		sanitizedErr := utils.SanitizeError(err)
		fmt.Println("Error calling VPC CallMcpTool -", toolName, ":", sanitizedErr)
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

	// Extract the actual result from the nested VPC response structure
	var actualResult map[string]interface{}

	// Check if data field is a string (JSON) or a map
	if dataStr, ok := responseData["data"].(string); ok {
		var dataMap map[string]interface{}
		if err := json.Unmarshal([]byte(dataStr), &dataMap); err != nil {
			// If JSON parsing fails, continue with fallback
		} else {
			if resultData, ok := dataMap["result"].(map[string]interface{}); ok {
				actualResult = resultData
			}
		}
	} else if data, ok := responseData["data"].(map[string]interface{}); ok {
		if resultData, ok := data["result"].(map[string]interface{}); ok {
			actualResult = resultData
		}
	}

	// If we couldn't find the nested result, use the top-level response
	if actualResult == nil {
		actualResult = responseData
	}

	// Check if there's an error in the VPC response
	if isError, ok := actualResult["isError"].(bool); ok && isError {
		result.IsError = true
		if errMsg, ok := actualResult["error"].(string); ok {
			result.ErrorMsg = errMsg
			return result, fmt.Errorf("%s", errMsg)
		}
		return result, fmt.Errorf("%s", defaultErrorMsg)
	}

	// Extract content array if it exists for VPC response
	if contentArray, ok := actualResult["content"].([]interface{}); ok {
		result.Content = make([]map[string]interface{}, len(contentArray))
		for i, item := range contentArray {
			if contentItem, ok := item.(map[string]interface{}); ok {
				result.Content[i] = contentItem
				// Extract text content from the first text item
				if i == 0 && result.TextContent == "" {
					if text, ok := contentItem["text"].(string); ok {
						result.TextContent = text
					}
				}
			}
		}
	}

	return result, nil
}

// callMcpToolAPI handles traditional API-based MCP tool calls
func (fs *FileSystem) callMcpToolAPI(toolName, argsJSON, defaultErrorMsg string) (*CallMcpToolResult, error) {
	// Create the request
	callToolRequest := &mcp.CallMcpToolRequest{
		Authorization: tea.String("Bearer " + fs.Session.GetAPIKey()),
		SessionId:     tea.String(fs.Session.GetSessionId()),
		Name:          tea.String(toolName),
		Args:          tea.String(argsJSON),
	}

	// Log API request
	fmt.Println("API Call: CallMcpTool -", toolName)
	fmt.Printf("Request: SessionId=%s, Args=%s\n", *callToolRequest.SessionId, *callToolRequest.Args)

	// Call the MCP tool
	response, err := fs.Session.GetClient().CallMcpTool(callToolRequest)

	// Log API response
	if err != nil {
		sanitizedErr := utils.SanitizeError(err)
		fmt.Println("Error calling CallMcpTool -", toolName, ":", sanitizedErr)
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

// Helper function to extract common result fields from CallMcpTool result
func (fs *FileSystem) extractCallResult(result *CallMcpToolResult) (string, string, map[string]interface{}, error) {
	if result.GetIsError() {
		return "", "", nil, fmt.Errorf(result.GetErrorMsg())
	}
	return result.GetRequestID(), result.GetTextContent(), result.GetData(), nil
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
	IsVpc() bool
	NetworkInterfaceIp() string
	HttpPort() string
	FindServerForTool(toolName string) string
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
	result, err := fs.CallMcpTool("create_directory", args, "error creating directory")
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
	result, err := fs.CallMcpTool("edit_file", args, "error editing file")
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
	result, err := fs.CallMcpTool("get_file_info", args, "error getting file info")
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
	result, err := fs.CallMcpTool("list_directory", args, "error listing directory")
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
	result, err := fs.CallMcpTool("move_file", args, "error moving file")
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
	result, err := fs.CallMcpTool("read_file", args, "error reading file")
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
	result, err := fs.CallMcpTool("read_multiple_files", args, "error reading multiple files")
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
	result, err := fs.CallMcpTool("search_files", args, "error searching files")
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
	result, err := fs.CallMcpTool("write_file", args, "error writing file")
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
	result, err := fs.CallMcpTool("read_large_file", args, "error reading large file")
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
	result, err := fs.CallMcpTool("write_large_file", args, "error writing large file")
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
