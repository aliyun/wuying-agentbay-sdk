# File System API Reference

## 📁 Related Tutorial

- [File Operations Guide](../../../../../docs/guides/common-features/basics/file-operations.md) - Complete guide to file system operations

## Type ContextFileUrlResult

```go
type ContextFileUrlResult struct {
	models.ApiResponse
	Success		bool
	Url		string
	ExpireTime	*int64
	ErrorMessage	string
}
```

ContextFileUrlResult represents a presigned URL operation result. This type is defined here to avoid
circular imports with the agentbay package.

## Type ContextInfoResult

```go
type ContextInfoResult struct {
	models.ApiResponse
	Success			bool
	ContextStatusData	[]ContextStatusData
	ErrorMessage		string
}
```

ContextInfoResult wraps context info result

## Type ContextManager

```go
type ContextManager interface {
	SyncWithParams(contextId, path, mode string) (*ContextSyncResult, error)
	InfoWithParams(contextId, path, taskType string) (*ContextInfoResult, error)
}
```

ContextManager interface for sync and info operations

## Type ContextServiceAdapter

```go
type ContextServiceAdapter struct {
	GetUploadURLFunc	func(contextID string, filePath string) (success bool, url string, errMsg string, requestID string, expireTime *int64, err error)
	GetDownloadURLFunc	func(contextID string, filePath string) (success bool, url string, errMsg string, requestID string, expireTime *int64, err error)
}
```

ContextServiceAdapter wraps the agentbay.ContextService to implement FileTransferContextService.
This adapter is used to break the circular dependency between filesystem and agentbay packages.

### Methods

### GetFileDownloadUrl

```go
func (a *ContextServiceAdapter) GetFileDownloadUrl(contextID string, filePath string) (*ContextFileUrlResult, error)
```

GetFileDownloadUrl implements FileTransferContextService interface

### GetFileUploadUrl

```go
func (a *ContextServiceAdapter) GetFileUploadUrl(contextID string, filePath string) (*ContextFileUrlResult, error)
```

GetFileUploadUrl implements FileTransferContextService interface

## Type ContextStatusData

```go
type ContextStatusData struct {
	ContextId	string	`json:"contextId"`
	Path		string	`json:"path"`
	ErrorMessage	string	`json:"errorMessage"`
	Status		string	`json:"status"`
	StartTime	int64	`json:"startTime"`
	FinishTime	int64	`json:"finishTime"`
	TaskType	string	`json:"taskType"`
}
```

ContextStatusData represents parsed context status data

## Type ContextSyncResult

```go
type ContextSyncResult struct {
	models.ApiResponse
	Success		bool
	ErrorMessage	string
}
```

ContextSyncResult wraps context sync result

## Type DirectoryEntry

```go
type DirectoryEntry struct {
	Name		string	`json:"name"`
	IsDirectory	bool	`json:"isDirectory"`
}
```

DirectoryEntry represents a directory entry

## Type DirectoryListResult

```go
type DirectoryListResult struct {
	models.ApiResponse
	Entries	[]*DirectoryEntry
}
```

DirectoryListResult wraps directory listing result and RequestID

## Type DownloadResult

```go
type DownloadResult struct {
	models.ApiResponse
	Success			bool
	RequestIDDownloadURL	string
	RequestIDSync		string
	HTTPStatus		int
	BytesReceived		int64
	Path			string
	LocalPath		string
	Error			string
}
```

DownloadResult represents the result of a file download operation.

Fields:
  - Success: Whether the download completed successfully
  - RequestIDDownloadURL: Request ID from the GetFileDownloadUrl API call
  - RequestIDSync: Request ID from the context sync API call
  - HTTPStatus: HTTP status code from the OSS download request
  - BytesReceived: Number of bytes downloaded
  - Path: Remote path from which the file was downloaded
  - LocalPath: Local path where the file was saved
  - Error: Error message if the download failed

## Type FileChangeEvent

```go
type FileChangeEvent struct {
	EventType	string	`json:"eventType"`	// "create", "modify", "delete"
	Path		string	`json:"path"`
	PathType	string	`json:"pathType"`	// "file", "directory"
}
```

FileChangeEvent represents a single file change event

### Methods

### String

```go
func (e *FileChangeEvent) String() string
```

String returns string representation of FileChangeEvent

## Type FileChangeResult

```go
type FileChangeResult struct {
	models.ApiResponse
	Events	[]*FileChangeEvent
	RawData	string
}
```

FileChangeResult wraps file change detection result

### Methods

### GetCreatedFiles

```go
func (r *FileChangeResult) GetCreatedFiles() []string
```

GetCreatedFiles returns list of created file paths

### GetDeletedFiles

```go
func (r *FileChangeResult) GetDeletedFiles() []string
```

GetDeletedFiles returns list of deleted file paths

### GetModifiedFiles

```go
func (r *FileChangeResult) GetModifiedFiles() []string
```

GetModifiedFiles returns list of modified file paths

### HasChanges

```go
func (r *FileChangeResult) HasChanges() bool
```

HasChanges checks if there are any file changes

## Type FileDirectoryResult

```go
type FileDirectoryResult struct {
	models.ApiResponse	// Embedded ApiResponse
	Success			bool
}
```

FileDirectoryResult wraps directory operation result and RequestID

## Type FileExistsResult

```go
type FileExistsResult struct {
	models.ApiResponse
	Exists	bool
}
```

FileExistsResult wraps file existence check result and RequestID

## Type FileInfo

```go
type FileInfo struct {
	Name		string	`json:"name"`
	Path		string	`json:"path"`
	Size		int64	`json:"size"`
	IsDirectory	bool	`json:"isDirectory"`
	ModTime		string	`json:"modTime"`
	Mode		string	`json:"mode"`
	Owner		string	`json:"owner,omitempty"`
	Group		string	`json:"group,omitempty"`
}
```

FileInfo represents file or directory information

## Type FileInfoResult

```go
type FileInfoResult struct {
	models.ApiResponse
	FileInfo	*FileInfo
}
```

FileInfoResult wraps file info result and RequestID

## Type FileReadResult

```go
type FileReadResult struct {
	models.ApiResponse	// Embedded ApiResponse
	Content			string
}
```

FileReadResult wraps file read operation result and RequestID

## Type FileSystem

```go
type FileSystem struct {
	Session	interface {
		GetAPIKey() string
		GetClient() *mcp.Client
		GetSessionId() string
		IsVpc() bool
		NetworkInterfaceIp() string
		HttpPort() string
		FindServerForTool(toolName string) string
		CallMcpTool(toolName string, args interface{}, autoGenSession ...bool) (*models.McpToolResult, error)
	}

	// Lazy-loaded file transfer instance
	fileTransfer		*FileTransfer
	fileTransferOnce	sync.Once
}
```

FileSystem handles file system operations in the AgentBay cloud environment.

### Methods

### CreateDirectory

```go
func (fs *FileSystem) CreateDirectory(path string) (*FileDirectoryResult, error)
```

CreateDirectory creates a new directory.

Parameters:
  - path: Absolute path to the directory to create

Returns:
  - *FileDirectoryResult: Result containing success status and request ID
  - error: Error if the operation fails

Behavior:

- Creates the directory and any necessary parent directories - Fails if the directory already exists
- Returns success if the directory is created successfully

**Example:**

```go
client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
result, _ := client.Create(nil)
defer result.Session.Delete()
createResult, _ := result.Session.FileSystem.CreateDirectory("/tmp/test_directory")
```

### DeleteFile

```go
func (fs *FileSystem) DeleteFile(path string) (*FileWriteResult, error)
```

DeleteFile deletes a file at the specified path.

Parameters:
  - path: Absolute path to the file to delete

Returns:
  - *FileWriteResult: Result containing success status and request ID
  - error: Error if the operation fails

Behavior:

- Deletes the file at the given path - Fails if the file doesn't exist

**Example:**

```go
client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
result, _ := client.Create(nil)
defer result.Session.Delete()
result.Session.FileSystem.WriteFile("/tmp/to_delete.txt", "hello", "overwrite")
deleteResult, _ := result.Session.FileSystem.DeleteFile("/tmp/to_delete.txt")
```

### DownloadFile

```go
func (fs *FileSystem) DownloadFile(remotePath, localPath string, opts *FileTransferOptions) *DownloadResult
```

DownloadFile downloads a file from the remote cloud disk to local via OSS pre-signed URL.

This is a convenience method that uses the session's FileTransfer. The remote path must be under
/tmp/file-transfer/ directory for the transfer to work correctly.

Parameters:
  - remotePath: Absolute path in the cloud disk (must be under /tmp/file-transfer/)
  - localPath: Absolute path where the file will be saved locally
  - opts: Transfer options. If nil, defaults are used (Wait=true, Timeout=300s)

Returns:
  - *DownloadResult: Result containing success status, bytes received, HTTP status, and request IDs

**Example:**

```go
client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
result, _ := client.Create(nil)
defer result.Session.Delete()
downloadResult := result.Session.FileSystem.DownloadFile("/tmp/file-transfer/file.txt", "/local/file.txt", nil)
if downloadResult.Success {
	fmt.Printf("Downloaded %d bytes\n", downloadResult.BytesReceived)
}
```

### EditFile

```go
func (fs *FileSystem) EditFile(path string, edits []map[string]string, dryRun bool) (*FileWriteResult, error)
```

EditFile edits a file with specified changes.

Parameters:
  - path: Absolute path to the file to edit
  - edits: Array of edit operations, each containing "oldText" and "newText" keys
  - dryRun: If true, preview changes without applying them

Returns:
  - *FileWriteResult: Result containing success status and request ID
  - error: Error if the operation fails

Behavior:

- Performs find-and-replace operations on the file content - In dry-run mode, shows what changes
would be made without applying them - All edits are applied sequentially in the order provided

**Example:**

```go
client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
result, _ := client.Create(nil)
defer result.Session.Delete()
result.Session.FileSystem.WriteFile("/tmp/test.txt", "Hello World", "overwrite")
edits := []map[string]string{{"oldText": "Hello", "newText": "Hi"}}
editResult, _ := result.Session.FileSystem.EditFile("/tmp/test.txt", edits, false)
```

### GetFileChange

```go
func (fs *FileSystem) GetFileChange(path string) (*FileChangeResult, error)
```

GetFileChange gets file change information for the specified directory path.

Parameters:
  - path: Absolute path to the directory to monitor

Returns:
  - *FileChangeResult: Result containing detected file changes and request ID
  - error: Error if the operation fails

Behavior:

- Detects file changes (create, modify, delete) since the last check - Returns empty Events array if
no changes detected - Automatically tracks the last checked state for the directory

**Example:**

```go
client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
result, _ := client.Create(nil)
defer result.Session.Delete()
result.Session.FileSystem.CreateDirectory("/tmp/watch_test")
result.Session.FileSystem.GetFileChange("/tmp/watch_test")
result.Session.FileSystem.WriteFile("/tmp/watch_test/file.txt", "content", "overwrite")
changeResult, _ := result.Session.FileSystem.GetFileChange("/tmp/watch_test")
```

### GetFileInfo

```go
func (fs *FileSystem) GetFileInfo(path string) (*FileInfoResult, error)
```

GetFileInfo gets information about a file or directory.

Parameters:
  - path: Absolute path to the file or directory

Returns:
  - *FileInfoResult: Result containing file information and request ID
  - error: Error if the operation fails

Behavior:

- Returns detailed information including size, permissions, modification time - Works for both files
and directories - Fails if the path doesn't exist

**Example:**

```go
client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
result, _ := client.Create(nil)
defer result.Session.Delete()
fileInfo, _ := result.Session.FileSystem.GetFileInfo("/etc/hostname")
```

### GetFileTransfer

```go
func (fs *FileSystem) GetFileTransfer() (*FileTransfer, error)
```

GetFileTransfer returns the FileTransfer instance, initializing it lazily if needed.

FileTransfer provides upload/download functionality between local filesystem and cloud disk using
OSS pre-signed URLs. Files are transferred to/from the /tmp/file-transfer/ directory on the cloud
disk.

Returns:
  - *FileTransfer: The FileTransfer instance
  - error: Error if the session doesn't support file transfer

**Example:**

```go
client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
result, _ := client.Create(nil)
defer result.Session.Delete()
ft, _ := result.Session.FileSystem.GetFileTransfer()
uploadResult := ft.Upload("/local/file.txt", "/tmp/file-transfer/file.txt", nil)
```

### ListDirectory

```go
func (fs *FileSystem) ListDirectory(path string) (*DirectoryListResult, error)
```

ListDirectory lists the contents of a directory. ListDirectory lists all files and directories in a
directory.

Parameters:
  - path: Absolute path to the directory to list

Returns:
  - *DirectoryListResult: Result containing list of entries and request ID
  - error: Error if the operation fails

Behavior:

- Returns list of DirectoryEntry objects with name, type, size, and mtime - Entry types: "file" or
"directory" - Fails if path doesn't exist or is not a directory

**Example:**

```go
client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
result, _ := client.Create(nil)
defer result.Session.Delete()
listResult, _ := result.Session.FileSystem.ListDirectory("/tmp")
```

### MoveFile

```go
func (fs *FileSystem) MoveFile(source, destination string) (*FileWriteResult, error)
```

MoveFile moves a file or directory from source to destination.

Parameters:
  - source: Absolute path to the source file or directory
  - destination: Absolute path to the destination

Returns:
  - *FileWriteResult: Result containing success status and request ID
  - error: Error if the operation fails

Behavior:

- Moves files or directories to a new location - Can be used to rename files/directories - Fails if
source doesn't exist or destination already exists

**Example:**

```go
client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
result, _ := client.Create(nil)
defer result.Session.Delete()
result.Session.FileSystem.WriteFile("/tmp/old.txt", "content", "overwrite")
moveResult, _ := result.Session.FileSystem.MoveFile("/tmp/old.txt", "/tmp/new.txt")
```

### ReadFile

```go
func (fs *FileSystem) ReadFile(path string) (*FileReadResult, error)
```

ReadFile reads the contents of a file. Automatically handles large files by chunking. ReadFile reads
the entire content of a file.

Parameters:
  - path: Absolute path to the file to read

Returns:
  - *FileReadResult: Result containing file content and request ID
  - error: Error if the operation fails

Behavior:

- Automatically handles large files by reading in 50KB chunks - Returns empty string for empty files
- Fails if path is a directory or doesn't exist

**Example:**

```go
client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
result, _ := client.Create(nil)
defer result.Session.Delete()
fileResult, _ := result.Session.FileSystem.ReadFile("/etc/hostname")
```

### ReadMultipleFiles

```go
func (fs *FileSystem) ReadMultipleFiles(paths []string) (map[string]string, error)
```

ReadMultipleFiles reads multiple files and returns their contents as a map.

Parameters:
  - paths: Array of absolute paths to files to read

Returns:
  - map[string]string: Map with file paths as keys and their contents as values
  - error: Error if the operation fails

Behavior:

- Reads multiple files in a single operation - Returns a map with paths as keys and file contents as
values - Fails if any of the specified files don't exist

**Example:**

```go
client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
result, _ := client.Create(nil)
defer result.Session.Delete()
paths := []string{"/etc/hostname", "/etc/os-release"}
contents, _ := result.Session.FileSystem.ReadMultipleFiles(paths)
```

### SearchFiles

```go
func (fs *FileSystem) SearchFiles(path, pattern string, excludePatterns []string) (*SearchFilesResult, error)
```

SearchFiles searches for files matching a wildcard pattern.

Parameters:
  - path: Absolute path to the directory to search in
  - pattern: Wildcard pattern to match against file names. Supports * (any characters) and ? (single
    character). Examples: "*.txt", "test_*", "*config*"
  - excludePatterns: Array of wildcard patterns to exclude from results

Returns:
  - *SearchFilesResult: Result containing matching file paths and request ID
  - error: Error if the operation fails

Behavior:

- Recursively searches the directory and subdirectories - Supports wildcard patterns for matching -
Exclude patterns help filter out unwanted results

**Example:**

```go
client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
result, _ := client.Create(nil)
defer result.Session.Delete()
searchResult, _ := result.Session.FileSystem.SearchFiles("/tmp", "*.txt", []string{})
```

### UploadFile

```go
func (fs *FileSystem) UploadFile(localPath, remotePath string, opts *FileTransferOptions) *UploadResult
```

UploadFile uploads a local file to the remote cloud disk via OSS pre-signed URL.

This is a convenience method that uses the session's FileTransfer. The remote path must be under
/tmp/file-transfer/ directory for the transfer to work correctly.

Parameters:
  - localPath: Absolute path to the local file to upload
  - remotePath: Absolute path in the cloud disk (must be under /tmp/file-transfer/)
  - opts: Transfer options. If nil, defaults are used (Wait=true, Timeout=30s)

Returns:
  - *UploadResult: Result containing success status, bytes sent, HTTP status, ETag, and request IDs

**Example:**

```go
client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
result, _ := client.Create(nil)
defer result.Session.Delete()
uploadResult := result.Session.FileSystem.UploadFile("/local/file.txt", "/tmp/file-transfer/file.txt", nil)
if uploadResult.Success {
	fmt.Printf("Uploaded %d bytes\n", uploadResult.BytesSent)
}
```

### WatchDirectory

```go
func (fs *FileSystem) WatchDirectory(
	path string,
	callback func([]*FileChangeEvent),
	interval time.Duration,
	stopCh <-chan struct{},
) *sync.WaitGroup
```

WatchDirectory watches a directory for file changes and calls the callback function when changes
occur.

Parameters:
  - path: Absolute path to the directory to watch
  - callback: Function called when changes are detected, receives array of FileChangeEvent
  - interval: Polling interval (e.g., 1*time.Second for 1 second)
  - stopCh: Channel to signal when to stop watching

Returns:
  - *sync.WaitGroup: WaitGroup that can be used to wait for monitoring to stop

Behavior:

- Continuously monitors directory for file changes at specified interval - Calls callback function
asynchronously when changes detected - Stops monitoring when stopCh is closed

**Example:**

```go
client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
result, _ := client.Create(nil)
defer result.Session.Delete()
result.Session.FileSystem.CreateDirectory("/tmp/watch")
stopCh := make(chan struct{})
wg := result.Session.FileSystem.WatchDirectory("/tmp/watch", func(events []*filesystem.FileChangeEvent) {}, 1*time.Second, stopCh)
close(stopCh)
wg.Wait()
```

### WatchDirectoryWithDefaults

```go
func (fs *FileSystem) WatchDirectoryWithDefaults(
	path string,
	callback func([]*FileChangeEvent),
	stopCh <-chan struct{},
) *sync.WaitGroup
```

WatchDirectoryWithDefaults watches a directory for file changes with default 500ms polling interval

### WriteFile

```go
func (fs *FileSystem) WriteFile(path, content string, mode string) (*FileWriteResult, error)
```

WriteFile writes content to a file. Automatically handles large files by chunking. WriteFile writes
content to a file.

Parameters:
  - path: Absolute path to the file to write
  - content: Content to write to the file
  - mode: Write mode ("overwrite" or "append")

Returns:
  - *FileWriteResult: Result containing success status and request ID
  - error: Error if the operation fails

Behavior:

- Automatically handles large content by writing in 50KB chunks - Creates parent directories if they
don't exist - "overwrite" mode replaces existing file content - "append" mode adds to existing file
content

**Example:**

```go
client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
result, _ := client.Create(nil)
defer result.Session.Delete()
writeResult, _ := result.Session.FileSystem.WriteFile("/tmp/test.txt", "Hello", "overwrite")
```

### Related Functions

### NewFileSystem

```go
func NewFileSystem(session interface {
	GetAPIKey() string
	GetClient() *mcp.Client
	GetSessionId() string
	IsVpc() bool
	NetworkInterfaceIp() string
	HttpPort() string
	FindServerForTool(toolName string) string
	CallMcpTool(toolName string, args interface{}, autoGenSession ...bool) (*models.McpToolResult, error)
}) *FileSystem
```

NewFileSystem creates a new FileSystem instance

## Type FileTransfer

```go
type FileTransfer struct {
	session		FileTransferSession
	contextSvc	FileTransferContextService
	httpTimeout	time.Duration

	// Lazy-loaded context information
	contextID	string
	contextPath	string

	// Task completion states
	finishedStates	map[string]bool
}
```

FileTransfer provides file transfer functionality between local filesystem and cloud disk.

It uses OSS pre-signed URLs for efficient file transfers and integrates with the Session Context
synchronization mechanism to ensure files are properly synced between OSS and the cloud disk.

The file transfer context is automatically loaded when first needed. Files must be transferred
to/from the /tmp/file-transfer/ directory on the cloud disk.

Workflow for Upload:
 1. Get OSS pre-signed URL via GetFileUploadUrl
 2. Upload file to OSS using HTTP PUT
 3. Trigger context sync (download mode) to copy from OSS to cloud disk
 4. Optionally wait for sync completion

Workflow for Download:
 1. Trigger context sync (upload mode) to copy from cloud disk to OSS
 2. Wait for sync completion
 3. Get OSS pre-signed URL via GetFileDownloadUrl
 4. Download file from OSS using HTTP GET

### Methods

### Download

```go
func (ft *FileTransfer) Download(remotePath, localPath string, opts *FileTransferOptions) *DownloadResult
```

Download downloads a remote file from cloud disk to local via OSS pre-signed URL.

The download process involves:
 1. Triggering context sync (upload mode) to copy from cloud disk to OSS
 2. Waiting for sync completion
 3. Getting an OSS pre-signed URL via GetFileDownloadUrl
 4. Downloading the file from OSS using HTTP GET

Parameters:
  - remotePath: Absolute path on cloud disk (must be under /tmp/file-transfer/)
  - localPath: Absolute path where the file will be saved locally
  - opts: Transfer options (nil for defaults with 300s timeout)

Returns:
  - *DownloadResult: Result containing success status, bytes received, request IDs, etc.

**Example:**

```go
client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
result, _ := client.Create(nil)
defer result.Session.Delete()
downloadResult := result.Session.FileSystem.DownloadFile("/tmp/file-transfer/file.txt", "/local/file.txt", nil)
if downloadResult.Success {
	fmt.Printf("Downloaded %d bytes\n", downloadResult.BytesReceived)
}
```

### GetContextPath

```go
func (ft *FileTransfer) GetContextPath() string
```

GetContextPath returns the context path for file transfer operations.

The context path is typically /tmp/file-transfer/ and is loaded lazily when first accessed. All file
transfer operations should use paths within this directory.

Returns:
  - string: The context path (e.g., "/tmp/file-transfer/")

### Upload

```go
func (ft *FileTransfer) Upload(localPath, remotePath string, opts *FileTransferOptions) *UploadResult
```

Upload uploads a local file to the remote cloud disk via OSS pre-signed URL.

The upload process involves:
 1. Getting an OSS pre-signed URL via GetFileUploadUrl
 2. Uploading the local file to OSS using HTTP PUT
 3. Triggering context sync (download mode) to copy from OSS to cloud disk
 4. Optionally waiting for sync completion

Parameters:
  - localPath: Absolute path to the local file to upload
  - remotePath: Absolute path on cloud disk (must be under /tmp/file-transfer/)
  - opts: Transfer options (nil for defaults)

Returns:
  - *UploadResult: Result containing success status, bytes sent, request IDs, etc.

**Example:**

```go
client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
result, _ := client.Create(nil)
defer result.Session.Delete()
uploadResult := result.Session.FileSystem.UploadFile("/local/file.txt", "/tmp/file-transfer/file.txt", nil)
if uploadResult.Success {
	fmt.Printf("Uploaded %d bytes\n", uploadResult.BytesSent)
}
```

### Related Functions

### NewFileTransfer

```go
func NewFileTransfer(session FileTransferSession, contextSvc FileTransferContextService) *FileTransfer
```

NewFileTransfer creates a new FileTransfer instance.

Parameters:
  - session: Session interface providing API key, client, and session ID
  - contextSvc: Context service interface for getting presigned URLs

Returns:
  - *FileTransfer: A new FileTransfer instance ready for upload/download operations

## Type FileTransferCapableSession

```go
type FileTransferCapableSession interface {
	FileTransferSession
	// GetFileUploadUrl returns a presigned upload URL for the given context and file path
	GetFileUploadUrl(contextID string, filePath string) (success bool, url string, errMsg string, requestID string, expireTime *int64, err error)
	// GetFileDownloadUrl returns a presigned download URL for the given context and file path
	GetFileDownloadUrl(contextID string, filePath string) (success bool, url string, errMsg string, requestID string, expireTime *int64, err error)
}
```

FileTransferCapableSession extends the base session interface with methods required for file
transfer operations (presigned URL generation).

## Type FileTransferContextService

```go
type FileTransferContextService interface {
	GetFileUploadUrl(contextID string, filePath string) (*ContextFileUrlResult, error)
	GetFileDownloadUrl(contextID string, filePath string) (*ContextFileUrlResult, error)
}
```

FileTransferContextService defines the context service interface required by FileTransfer

## Type FileTransferOptions

```go
type FileTransferOptions struct {
	HTTPTimeout	time.Duration
	FollowRedirects	bool
	Wait		bool
	WaitTimeout	time.Duration
	PollInterval	time.Duration
	ContentType	string
	Overwrite	bool
	ProgressCB	ProgressCallback
}
```

FileTransferOptions contains configuration options for file transfer operations.

Fields:
  - HTTPTimeout: Timeout for HTTP requests (default: 60s)
  - FollowRedirects: Whether to follow HTTP redirects (default: true)
  - Wait: Whether to wait for sync completion (default: true)
  - WaitTimeout: Maximum time to wait for sync completion (default: 30s for upload, 300s for
    download)
  - PollInterval: Interval between sync status polls (default: 1.5s)
  - ContentType: Content-Type header for uploads (optional)
  - Overwrite: Whether to overwrite existing local files on download (default: true)
  - ProgressCB: Callback for progress tracking (optional)

### Related Functions

### DefaultFileTransferOptions

```go
func DefaultFileTransferOptions() *FileTransferOptions
```

DefaultFileTransferOptions returns the default options for file transfer operations.

Default values:
  - HTTPTimeout: 60 seconds
  - FollowRedirects: true
  - Wait: true
  - WaitTimeout: 30 seconds
  - PollInterval: 1.5 seconds
  - Overwrite: true

**Example:**

```go
opts := filesystem.DefaultFileTransferOptions()
opts.WaitTimeout = 60 * time.Second
uploadResult := session.FileSystem.UploadFile("/local/file.txt", "/tmp/file-transfer/file.txt", opts)
```

## Type FileTransferSession

```go
type FileTransferSession interface {
	GetAPIKey() string
	GetClient() *mcp.Client
	GetSessionId() string
}
```

FileTransferSession defines the session interface required by FileTransfer

## Type FileWriteResult

```go
type FileWriteResult struct {
	models.ApiResponse	// Embedded ApiResponse
	Success			bool
}
```

FileWriteResult wraps file write operation result and RequestID

## Type ProgressCallback

```go
type ProgressCallback func(bytesTransferred int64)
```

ProgressCallback is a callback function for tracking file transfer progress. It is called
periodically during upload or download with the total bytes transferred so far.

## Type SearchFilesResult

```go
type SearchFilesResult struct {
	models.ApiResponse
	Results	[]string
}
```

SearchFilesResult wraps file search result and RequestID

## Type UploadResult

```go
type UploadResult struct {
	models.ApiResponse
	Success			bool
	RequestIDUploadURL	string
	RequestIDSync		string
	HTTPStatus		int
	ETag			string
	BytesSent		int64
	Path			string
	Error			string
}
```

UploadResult represents the result of a file upload operation.

Fields:
  - Success: Whether the upload completed successfully
  - RequestIDUploadURL: Request ID from the GetFileUploadUrl API call
  - RequestIDSync: Request ID from the context sync API call
  - HTTPStatus: HTTP status code from the OSS upload request
  - ETag: ETag returned by OSS after successful upload
  - BytesSent: Number of bytes uploaded
  - Path: Remote path where the file was uploaded
  - Error: Error message if the upload failed

## Related Resources

- [Session API Reference](session.md)
- [Command API Reference](command.md)

---

*Documentation generated automatically from Go source code.*
