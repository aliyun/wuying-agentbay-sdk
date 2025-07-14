package filesystem

import (
	"encoding/json"
	"fmt"
	"strconv"
	"strings"

	"github.com/alibabacloud-go/tea/tea"
	mcp "github.com/aliyun/wuying-agentbay-sdk/golang/api/client"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/models"
)

// FileReadResult represents the result of a file read operation
type FileReadResult struct {
	models.ApiResponse // Embedded ApiResponse
	Content            string
}

// FileWriteResult represents the result of a file write operation
type FileWriteResult struct {
	models.ApiResponse // Embedded ApiResponse
	Success            bool
}

// FileExistsResult wraps file existence check result and RequestID
type FileExistsResult struct {
	models.ApiResponse
	Exists bool
}

// FileDirectoryResult represents the result of directory operations
type FileDirectoryResult struct {
	models.ApiResponse // Embedded ApiResponse
	Success            bool
}

// DirectoryListResult wraps directory listing result and RequestID
type DirectoryListResult struct {
	models.ApiResponse
	Entries []*DirectoryEntry
}

// FileInfoResult represents the result of a file info operation
type FileInfoResult struct {
	models.ApiResponse
	FileInfo *FileInfo
}

// SearchFilesResult represents the result of a search files operation
type SearchFilesResult struct {
	models.ApiResponse
	Results []string
}

// FileSystem handles file operations in the AgentBay cloud environment.
type FileSystem struct {
	Session interface {
		GetAPIKey() string
		GetClient() *mcp.Client
		GetSessionId() string
	}
}

// FileInfo represents information about a file or directory
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

// DirectoryEntry represents an entry in a directory listing
type DirectoryEntry struct {
	Name        string `json:"name"`
	IsDirectory bool   `json:"isDirectory"`
}

// callMcpToolResult represents the result of a CallMcpTool operation
type callMcpToolResult struct {
	TextContent string // Extracted text field content
	Data        map[string]interface{}
	IsError     bool
	ErrorMsg    string
	StatusCode  int32
	RequestID   string // Added field to store request ID
}

// callMcpTool calls the MCP tool and checks for errors in the response
func (fs *FileSystem) callMcpTool(toolName string, args interface{}, defaultErrorMsg string) (*callMcpToolResult, error) {
	// Marshal arguments to JSON
	argsJSON, err := json.Marshal(args)
	if err != nil {
		return nil, fmt.Errorf("failed to marshal args: %w", err)
	}

	// Create the request
	callToolRequest := &mcp.CallMcpToolRequest{
		Authorization: tea.String("Bearer " + fs.Session.GetAPIKey()),
		SessionId:     tea.String(fs.Session.GetSessionId()),
		Name:          tea.String(toolName),
		Args:          tea.String(string(argsJSON)),
	}

	// Log API request with content length for file operations
	fmt.Println("API Call: CallMcpTool -", toolName)

	// Handle logging differently based on operation type
	if isFileOperation(toolName) {
		// For file operations, log content length instead of content
		truncatedArgs := truncateContentForLogging(string(argsJSON))
		fmt.Printf("Request: SessionId=%s, Args=%s\n", *callToolRequest.SessionId, truncatedArgs)
	} else {
		// For non-file operations, log normally
		fmt.Printf("Request: SessionId=%s, Args=%s\n", *callToolRequest.SessionId, *callToolRequest.Args)
	}

	// Call the MCP tool
	response, err := fs.Session.GetClient().CallMcpTool(callToolRequest)

	// Log API response
	if err != nil {
		fmt.Println("Error calling CallMcpTool -", toolName, ":", err)
		return nil, fmt.Errorf("failed to call %s: %w", toolName, err)
	}

	// Extract RequestID
	var requestID string
	if response != nil && response.Body != nil && response.Body.RequestId != nil {
		requestID = *response.Body.RequestId
	}

	if response != nil && response.Body != nil {
		if isFileOperation(toolName) {
			// Log content size for file operations instead of full content
			fmt.Println("Response from CallMcpTool -", toolName, "- status:", *response.StatusCode)

			// Log only relevant response information without content
			data, ok := response.Body.Data.(map[string]interface{})
			if ok {
				isError, _ := data["isError"].(bool)
				if isError {
					fmt.Println("Response contains error:", data["isError"])
				} else {
					fmt.Println("Response successful, content length info provided separately")
				}
			}
		} else {
			// Log full response for non-file operations
			fmt.Println("Response from CallMcpTool -", toolName, ":", response.Body)
		}
	}

	// Extract data from response
	data, ok := response.Body.Data.(map[string]interface{})
	if !ok {
		return nil, fmt.Errorf("invalid response data format")
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
		//nolint:govet
		contentArray, ok := data["content"].([]interface{})
		if ok && len(contentArray) > 0 {
			// Extract error message from the first content item
			if len(contentArray) > 0 {
				//nolint:govet
				contentItem, ok := contentArray[0].(map[string]interface{})
				if ok {
					//nolint:govet
					text, ok := contentItem["text"].(string)
					if ok {
						result.ErrorMsg = text
						return result, fmt.Errorf("%s", text)
					}
				}
			}
		}
		return result, fmt.Errorf("%s", defaultErrorMsg)
	}

	// Extract text from content array if it exists
	//nolint:govet
	contentArray, ok := data["content"].([]interface{})
	if ok && len(contentArray) > 0 {
		var textBuilder strings.Builder
		for i, item := range contentArray {
			//nolint:govet
			contentItem, ok := item.(map[string]interface{})
			if !ok {
				continue
			}

			//nolint:govet
			text, ok := contentItem["text"].(string)
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

// isFileOperation checks if the tool operation is file-related and might contain large content
func isFileOperation(toolName string) bool {
	fileOperations := map[string]bool{
		"read_file":           true,
		"write_file":          true,
		"read_multiple_files": true,
	}
	return fileOperations[toolName]
}

// truncateContentForLogging replaces large content with size information in JSON args
func truncateContentForLogging(jsonArgs string) string {
	var args map[string]interface{}
	if err := json.Unmarshal([]byte(jsonArgs), &args); err != nil {
		return fmt.Sprintf("[Could not parse args for logging: %s]", err)
	}

	// Check for content field and replace with length info
	if content, ok := args["content"]; ok {
		contentStr, isString := content.(string)
		if isString {
			contentLength := len(contentStr)
			args["content"] = fmt.Sprintf("[Content length: %d bytes]", contentLength)
		}
	}

	// Check for paths array and log number of paths instead of all paths
	if paths, ok := args["paths"].([]interface{}); ok && len(paths) > 3 {
		args["paths"] = fmt.Sprintf("[%d paths, first few: %v, %v, %v, ...]",
			len(paths), paths[0], paths[1], paths[2])
	}

	// Serialize back to JSON
	modifiedJSON, err := json.Marshal(args)
	if err != nil {
		return fmt.Sprintf("[Could not serialize modified args: %s]", err)
	}

	return string(modifiedJSON)
}

// parseFileInfo parses a file info string into a FileInfo struct
func parseFileInfo(fileInfoStr string) (*FileInfo, error) {
	result := &FileInfo{}
	lines := strings.Split(fileInfoStr, "\n")
	for _, line := range lines {
		if strings.Contains(line, ":") {
			parts := strings.SplitN(line, ":", 2)
			if len(parts) != 2 {
				continue
			}

			key := strings.TrimSpace(parts[0])
			value := strings.TrimSpace(parts[1])

			switch key {
			case "name":
				result.Name = value
			case "path":
				result.Path = value
			case "size":
				size, err := strconv.ParseInt(value, 10, 64)
				if err == nil {
					result.Size = size
				}
			case "isDirectory":
				result.IsDirectory = value == "true"
			case "modified": // Server returns "modified" instead of "modTime"
				result.ModTime = value
			case "permissions": // Server returns "permissions" instead of "mode"
				result.Mode = value
			case "owner":
				result.Owner = value
			case "group":
				result.Group = value
			}
		}
	}
	return result, nil
}

// parseDirectoryListing parses a directory listing string into a slice of DirectoryEntry structs
func parseDirectoryListing(text string) ([]*DirectoryEntry, error) {
	result := []*DirectoryEntry{}
	lines := strings.Split(text, "\n")

	for _, line := range lines {
		line = strings.TrimSpace(line)
		if line == "" {
			continue
		}

		entry := &DirectoryEntry{}
		if strings.HasPrefix(line, "[DIR]") {
			entry.IsDirectory = true
			entry.Name = strings.TrimSpace(strings.TrimPrefix(line, "[DIR]"))
		} else if strings.HasPrefix(line, "[FILE]") {
			entry.IsDirectory = false
			entry.Name = strings.TrimSpace(strings.TrimPrefix(line, "[FILE]"))
		} else {
			// Skip lines that don't match the expected format
			continue
		}

		result = append(result, entry)
	}

	return result, nil
}

// NewFileSystem creates a new FileSystem object.
func NewFileSystem(session interface {
	GetAPIKey() string
	GetClient() *mcp.Client
	GetSessionId() string
}) *FileSystem {
	return &FileSystem{
		Session: session,
	}
}

// CreateDirectory creates a directory.
// API Parameters:
//
//	{
//	  "path": "directory/path/to/create"
//	}
func (fs *FileSystem) CreateDirectory(path string) (*FileDirectoryResult, error) {
	args := map[string]string{
		"path": path,
	}

	// Use the helper method to call MCP tool and check for errors
	mcpResult, err := fs.callMcpTool("create_directory", args, "error creating directory")
	if err != nil {
		return nil, err
	}

	// Return result with RequestID
	return &FileDirectoryResult{
		ApiResponse: models.ApiResponse{
			RequestID: mcpResult.RequestID,
		},
		Success: true,
	}, nil
}

// EditFile edits a file by replacing occurrences of oldText with newText.
// API Parameters:
//
//	{
//	  "path": "file/path/to/edit",
//	  "edits": [
//	    {
//	      "oldText": "text to search for",
//	      "newText": "text to replace with"
//	    },
//	    {
//	      "oldText": "another text to search",
//	      "newText": "another replacement"
//	    }
//	  ],
//	  "dryRun": false  // Optional: Preview changes without applying them
//	}
func (fs *FileSystem) EditFile(path string, edits []map[string]string, dryRun bool) (*FileWriteResult, error) {
	args := map[string]interface{}{
		"path":   path,
		"edits":  edits,
		"dryRun": dryRun,
	}

	// Use the helper method to call MCP tool and check for errors
	mcpResult, err := fs.callMcpTool("edit_file", args, "error editing file")
	if err != nil {
		return nil, err
	}

	// Return result with RequestID
	return &FileWriteResult{
		ApiResponse: models.ApiResponse{
			RequestID: mcpResult.RequestID,
		},
		Success: true,
	}, nil
}

// GetFileInfo gets information about a file or directory.
// API Parameters:
//
//	{
//	  "path": "file/or/directory/path/to/inspect"
//	}
func (fs *FileSystem) GetFileInfo(path string) (*FileInfoResult, error) {
	args := map[string]string{
		"path": path,
	}

	// Use the helper method to call MCP tool and check for errors
	mcpResult, err := fs.callMcpTool("get_file_info", args, "error getting file info")
	if err != nil {
		// Check if it's a "file not found" error
		if strings.Contains(err.Error(), "No such file or directory") {
			return nil, fmt.Errorf("file not found: %s", path)
		}
		return nil, err
	}

	fileInfo, err := parseFileInfo(mcpResult.TextContent)
	if err != nil {
		return nil, fmt.Errorf("error parsing file info: %w", err)
	}

	// Return result with RequestID
	return &FileInfoResult{
		ApiResponse: models.ApiResponse{
			RequestID: mcpResult.RequestID,
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

	// Use the helper method to call MCP tool and check for errors
	mcpResult, err := fs.callMcpTool("list_directory", args, "error listing directory")
	if err != nil {
		return nil, err
	}

	entries, err := parseDirectoryListing(mcpResult.TextContent)
	if err != nil {
		return nil, fmt.Errorf("error parsing directory listing: %w", err)
	}

	// Return result with RequestID
	return &DirectoryListResult{
		ApiResponse: models.ApiResponse{
			RequestID: mcpResult.RequestID,
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

	// Use the helper method to call MCP tool and check for errors
	mcpResult, err := fs.callMcpTool("move_file", args, "error moving file")
	if err != nil {
		return nil, err
	}

	// Return result with RequestID
	return &FileWriteResult{
		ApiResponse: models.ApiResponse{
			RequestID: mcpResult.RequestID,
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

	// Only include optional parameters if they are non-default values
	if offset > 0 {
		args["offset"] = offset
	}
	if length > 0 {
		args["length"] = length
	}

	// Use the enhanced helper method to call MCP tool and check for errors
	mcpResult, err := fs.callMcpTool("read_file", args, "error reading file")
	if err != nil {
		return nil, err
	}

	// Return result with RequestID
	return &FileReadResult{
		ApiResponse: models.ApiResponse{
			RequestID: mcpResult.RequestID,
		},
		Content: mcpResult.TextContent,
	}, nil
}

// ReadMultipleFiles reads the contents of multiple files.
// API Parameters:
//
//	{
//	  "paths": ["file1/path", "file2/path", "file3/path"]
//	}
func (fs *FileSystem) ReadMultipleFiles(paths []string) (map[string]string, error) {
	args := map[string]interface{}{
		"paths": paths,
	}

	// Use the helper method to call MCP tool and check for errors
	mcpResult, err := fs.callMcpTool("read_multiple_files", args, "error reading multiple files")
	if err != nil {
		return nil, err
	}

	// Parse the response into a map of file paths to contents
	result := make(map[string]string)
	lines := strings.Split(mcpResult.TextContent, "\n")
	currentPath := ""
	currentContent := []string{}

	for _, line := range lines {
		// Check if this line contains a file path (ends with a colon)
		colonIndex := strings.Index(line, ":")
		if colonIndex > 0 && currentPath == "" && !strings.Contains(line[:colonIndex], " ") {
			// Extract path (everything before the first colon)
			path := strings.TrimSpace(line[:colonIndex])

			// Start collecting content (everything after the colon)
			currentPath = path

			// If there's content on the same line after the colon, add it
			if len(line) > colonIndex+1 {
				contentStart := strings.TrimSpace(line[colonIndex+1:])
				if contentStart != "" {
					currentContent = append(currentContent, contentStart)
				}
			}
		} else if line == "---" {
			// Save the current file content
			if currentPath != "" {
				result[currentPath] = strings.Join(currentContent, "\n")
				currentPath = ""
				currentContent = []string{}
			}
		} else if currentPath != "" {
			// If we're collecting content for a path, add this line
			currentContent = append(currentContent, line)
		}
	}

	// Save the last file content if exists
	if currentPath != "" {
		result[currentPath] = strings.Join(currentContent, "\n")
	}

	return result, nil
}

// SearchFiles searches for files matching a pattern in a directory.
// API Parameters:
//
//	{
//	  "path": "directory/path/to/start/search",
//	  "pattern": "pattern to match",
//	  "excludePatterns": ["pattern1", "pattern2"]  // Optional: Patterns to exclude
//	}
func (fs *FileSystem) SearchFiles(path, pattern string, excludePatterns []string) (*SearchFilesResult, error) {
	args := map[string]interface{}{
		"path":    path,
		"pattern": pattern,
	}

	// Only include excludePatterns if non-empty
	if len(excludePatterns) > 0 {
		args["excludePatterns"] = excludePatterns
	}

	// Use the helper method to call MCP tool and check for errors
	mcpResult, err := fs.callMcpTool("search_files", args, "error searching files")
	if err != nil {
		return nil, err
	}

	// Parse the response into a list of strings
	var results []string
	for _, line := range strings.Split(mcpResult.TextContent, "\n") {
		line = strings.TrimSpace(line)
		if line != "" {
			results = append(results, line)
		}
	}

	return &SearchFilesResult{
		ApiResponse: models.ApiResponse{
			RequestID: mcpResult.RequestID,
		},
		Results: results,
	}, nil
}

// WriteFile writes content to a file.
// API Parameters:
//
//	{
//	  "path": "file/path/to/write",
//	  "content": "Content to write to the file",
//	  "mode": "overwrite"  // Optional: "overwrite" (default) or "append"
//	}
func (fs *FileSystem) WriteFile(path, content string, mode string) (*FileWriteResult, error) {
	if mode == "" {
		mode = "overwrite"
	}

	args := map[string]interface{}{
		"path":    path,
		"content": content,
		"mode":    mode,
	}

	// Use the enhanced helper method to call MCP tool and check for errors
	mcpResult, err := fs.callMcpTool("write_file", args, "error writing file")
	if err != nil {
		return nil, err
	}

	// Return result with RequestID
	return &FileWriteResult{
		ApiResponse: models.ApiResponse{
			RequestID: mcpResult.RequestID,
		},
		Success: true,
	}, nil
}

// ChunkSize is the default size of chunks for large file operations (60KB)
const ChunkSize = 60 * 1024

// ReadLargeFile reads a large file in chunks to handle size limitations of the underlying API.
// It automatically splits the read operation into multiple requests of chunkSize bytes each.
// If chunkSize is <= 0, the default ChunkSize (60KB) will be used.
func (fs *FileSystem) ReadLargeFile(path string, chunkSize int) (*FileReadResult, error) {
	if chunkSize <= 0 {
		chunkSize = ChunkSize
	}

	// First get the file size
	fileInfoResult, err := fs.GetFileInfo(path)
	if err != nil {
		return nil, fmt.Errorf("failed to get file info: %w", err)
	}

	// Get size from the fileInfo struct
	size := float64(fileInfoResult.FileInfo.Size)

	if size == 0 {
		return nil, fmt.Errorf("couldn't determine file size")
	}

	// Prepare to read the file in chunks
	var result strings.Builder
	offset := 0
	fileSize := int(size)
	var lastRequestID string

	fmt.Printf("ReadLargeFile: Starting chunked read of %s (total size: %d bytes, chunk size: %d bytes)\n",
		path, fileSize, chunkSize)

	chunkCount := 0
	for offset < fileSize {
		// Calculate how much to read in this chunk
		length := chunkSize
		if offset+length > fileSize {
			length = fileSize - offset
		}

		fmt.Printf("ReadLargeFile: Reading chunk %d (%d bytes at offset %d/%d)\n",
			chunkCount+1, length, offset, fileSize)

		// Read the chunk
		chunkResult, err := fs.ReadFile(path, offset, length)
		if err != nil {
			return nil, fmt.Errorf("error reading chunk at offset %d: %w", offset, err)
		}

		// 保存最后一个请求的RequestID
		lastRequestID = chunkResult.RequestID

		// Append the chunk text
		result.WriteString(chunkResult.Content)

		// Move to the next chunk
		offset += length
		chunkCount++
	}

	fmt.Printf("ReadLargeFile: Successfully read %s in %d chunks (total: %d bytes)\n",
		path, chunkCount, fileSize)

	return &FileReadResult{
		ApiResponse: models.ApiResponse{
			RequestID: lastRequestID, // Use the RequestID from the last chunk request
		},
		Content: result.String(),
	}, nil
}

// WriteLargeFile writes a large file in chunks to handle size limitations of the underlying API.
// It automatically splits the write operation into multiple requests of chunkSize bytes each.
// If chunkSize is <= 0, the default ChunkSize (60KB) will be used.
func (fs *FileSystem) WriteLargeFile(path, content string, chunkSize int) (*FileWriteResult, error) {
	if chunkSize <= 0 {
		chunkSize = ChunkSize
	}

	contentLen := len(content)
	var lastRequestID string

	fmt.Printf("WriteLargeFile: Starting chunked write to %s (total size: %d bytes, chunk size: %d bytes)\n",
		path, contentLen, chunkSize)

	// If content is small enough, use the regular WriteFile method
	if contentLen <= chunkSize {
		fmt.Printf("WriteLargeFile: Content size (%d bytes) is smaller than chunk size, using normal WriteFile\n",
			contentLen)
		return fs.WriteFile(path, content, "overwrite")
	}

	// Write the first chunk with "overwrite" mode to create/clear the file
	firstChunkEnd := chunkSize
	if firstChunkEnd > contentLen {
		firstChunkEnd = contentLen
	}

	fmt.Printf("WriteLargeFile: Writing first chunk (0-%d bytes) with overwrite mode\n", firstChunkEnd)
	result, err := fs.WriteFile(path, content[:firstChunkEnd], "overwrite")
	if err != nil {
		return nil, fmt.Errorf("error writing first chunk: %w", err)
	}

	// 保存第一个请求的RequestID
	lastRequestID = result.RequestID

	// Write the remaining chunks with "append" mode
	chunkCount := 1 // Already wrote first chunk
	for offset := firstChunkEnd; offset < contentLen; {
		end := offset + chunkSize
		if end > contentLen {
			end = contentLen
		}

		fmt.Printf("WriteLargeFile: Writing chunk %d (%d-%d bytes) with append mode\n",
			chunkCount+1, offset, end)
		result, err := fs.WriteFile(path, content[offset:end], "append")
		if err != nil {
			return nil, fmt.Errorf("error writing chunk at offset %d: %w", offset, err)
		}

		// 更新RequestID为最后一个请求的ID
		lastRequestID = result.RequestID

		offset = end
		chunkCount++
	}

	fmt.Printf("WriteLargeFile: Successfully wrote %s in %d chunks (total: %d bytes)\n",
		path, chunkCount, contentLen)

	return &FileWriteResult{
		ApiResponse: models.ApiResponse{
			RequestID: lastRequestID, // Use the RequestID from the last chunk request
		},
		Success: true,
	}, nil
}
