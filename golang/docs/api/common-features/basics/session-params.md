# Session Params API Reference

## Type AgentBay

```go
type AgentBay struct {
	APIKey		string
	Client		*mcp.Client
	Context		*ContextService
	MobileSimulate	*MobileSimulateService
	config		Config
}
```

AgentBay represents the main client for interacting with the AgentBay cloud runtime environment.

### Methods

### Create

```go
func (a *AgentBay) Create(params *CreateSessionParams) (*SessionResult, error)
```

Create creates a new session in the AgentBay cloud environment. If params is nil, default parameters
will be used. Create creates a new AgentBay session with specified configuration.

Parameters:
  - params: Configuration parameters for the session (optional)
  - Labels: Key-value pairs for session metadata
  - ImageId: Custom image ID for the session environment
  - IsVpc: Whether to create a VPC session
  - PolicyId: Security policy ID
  - ExtraConfigs: Additional configuration options

Returns:
  - *SessionResult: Result containing Session object and request ID
  - error: Error if the operation fails

Behavior:

- Creates a new isolated cloud runtime environment - Waits for session to be ready before returning
- For VPC sessions, includes VPC-specific configuration

**Example:**

```go
client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
result, _ := client.Create(nil)
defer result.Session.Delete()
```

### Delete

```go
func (a *AgentBay) Delete(session *Session, syncContext ...bool) (*DeleteResult, error)
```

Delete deletes a session from the AgentBay cloud environment.

Parameters:
  - session: The session to delete
  - syncContext: Optional boolean to synchronize context data before deletion. If true, uploads all
    context data to OSS. Defaults to false.

Returns:
  - *DeleteResult: Result containing success status and request ID
  - error: Error if the operation fails

Behavior:

- If syncContext is true: Uploads all context data to OSS before deletion - If syncContext is false:
Deletes immediately without sync - Continues with deletion even if context sync fails - Releases all
associated resources

**Example:**

```go
client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
result, _ := client.Create(nil)
client.Delete(result.Session, true)
```

### Get

```go
func (a *AgentBay) Get(sessionID string) (*SessionResult, error)
```

Get retrieves a session by its ID. This method calls the GetSession API and returns a SessionResult
containing the Session object and request ID.

Parameters:
  - sessionID: The ID of the session to retrieve

Returns:
  - *SessionResult: Result containing the Session instance, request ID, and success status
  - error: An error if the operation fails

**Example:**

```go
client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
createResult, _ := client.Create(nil)
sessionID := createResult.Session.SessionID
result, _ := client.Get(sessionID)
defer result.Session.Delete()
```

### GetRegionID

```go
func (a *AgentBay) GetRegionID() string
```

GetRegionID returns the region ID from config

### GetSession

```go
func (a *AgentBay) GetSession(sessionID string) (*GetSessionResult, error)
```

GetSession retrieves session information by session ID

### List

```go
func (a *AgentBay) List(labels map[string]string, page *int, limit *int32) (*SessionListResult, error)
```

List returns paginated list of session IDs filtered by labels.

Parameters:
  - labels: Optional labels to filter sessions (can be nil for no filtering)
  - page: Optional page number for pagination (starting from 1, nil or 0 for first page)
  - limit: Optional maximum number of items per page (nil or 0 uses default of 10)

Returns:
  - *SessionListResult: Paginated list of session IDs that match the labels
  - error: An error if the operation fails

**Example:**

```go
client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
result, _ := client.List(nil, nil, nil)
```

### Pause

```go
func (ab *AgentBay) Pause(session *Session, timeout int, pollInterval float64) (*models.SessionPauseResult, error)
```

Pause synchronously pauses a session, putting it into a dormant state to reduce resource usage and
costs. Pause puts the session into a PAUSED state where computational resources are significantly
reduced. The session state is preserved and can be resumed later to continue work.

Parameters:
  - session: The session to pause.
  - timeout: Timeout in seconds to wait for the session to pause. Defaults to 600 seconds.
  - pollInterval: Interval in seconds between status polls. Defaults to 2.0 seconds.

Returns:
  - *models.SessionPauseResult: Result containing success status, request ID, and error message if
    any.
  - error: Error if the operation fails at the transport level

Behavior:

- Delegates to session's Pause method for actual implementation - Returns detailed result with
success status and request tracking

Exceptions:

- Returns error result (not Go error) for API-level errors like invalid session ID - Returns error
result for timeout conditions - Returns Go error for transport-level failures

**Example:**

```go
client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"))
result, _ := client.Create(nil)
defer result.Session.Delete()
pauseResult, _ := client.Pause(result.Session, 300, 2.0)
client.Resume(result.Session, 300, 2.0)
```

### Resume

```go
func (ab *AgentBay) Resume(session *Session, timeout int, pollInterval float64) (*models.SessionResumeResult, error)
```

Resume synchronously resumes a session from a paused state to continue work. Resume restores the
session from PAUSED state back to RUNNING state. All previous session state and data are preserved
during resume operation.

Parameters:
  - session: The session to resume.
  - timeout: Timeout in seconds to wait for the session to resume. Defaults to 600 seconds.
  - pollInterval: Interval in seconds between status polls. Defaults to 2.0 seconds.

Returns:
  - *models.SessionResumeResult: Result containing success status, request ID, and error message if
    any.
  - error: Error if the operation fails at the transport level

Behavior:

- Delegates to session's Resume method for actual implementation - Returns detailed result with
success status and request tracking

Exceptions:

- Returns error result (not Go error) for API-level errors like invalid session ID - Returns error
result for timeout conditions - Returns Go error for transport-level failures

**Example:**

```go
client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"))
result, _ := client.Create(nil)
defer result.Session.Delete()
client.Pause(result.Session, 300, 2.0)
resumeResult, _ := client.Resume(result.Session, 300, 2.0)
```

### Related Functions

### NewAgentBay

```go
func NewAgentBay(apiKey string, opts ...Option) (*AgentBay, error)
```

NewAgentBay creates a new AgentBay client. If apiKey is empty, it will look for the AGENTBAY_API_KEY
environment variable.

### NewAgentBayWithDefaults

```go
func NewAgentBayWithDefaults(apiKey string) (*AgentBay, error)
```

NewAgentBayWithDefaults creates a new AgentBay client using default configuration. This is a
convenience function that allows calling NewAgentBay without a config parameter.

## Type AgentBayConfig

```go
type AgentBayConfig struct {
	cfg	*Config
	envFile	string
}
```

AgentBayConfig holds optional configuration for the AgentBay client.

## Type BWList

```go
type BWList struct {
	// WhiteLists defines the white lists
	WhiteLists []*WhiteList `json:"whiteLists,omitempty"`
}
```

BWList defines the black and white list configuration

## Type Config

```go
type Config struct {
	Endpoint	string	`json:"endpoint"`
	TimeoutMs	int	`json:"timeout_ms"`
	RegionID	string	`json:"region_id"`
}
```

Config stores SDK configuration

## Type Context

```go
type Context struct {
	// ID is the unique identifier of the context.
	ID	string

	// Name is the name of the context.
	Name	string

	// CreatedAt is the date and time when the Context was created.
	CreatedAt	string

	// LastUsedAt is the date and time when the Context was last used.
	LastUsedAt	string
}
```

Context represents a persistent storage context in the AgentBay cloud environment.

## Type ContextClearResult

```go
type ContextClearResult struct {
	models.ApiResponse
	Success		bool
	Status		string	// Current status of the clearing task ("clearing", "available", etc.)
	ContextID	string
	ErrorMessage	string
}
```

ContextClearResult wraps context clear operation result and RequestID

## Type ContextCreateResult

```go
type ContextCreateResult struct {
	models.ApiResponse
	ContextID	string
}
```

ContextCreateResult wraps context creation result and RequestID

## Type ContextDeleteResult

```go
type ContextDeleteResult struct {
	models.ApiResponse
	Success		bool
	ErrorMessage	string
}
```

ContextDeleteResult wraps context deletion result and RequestID

## Type ContextFileDeleteResult

```go
type ContextFileDeleteResult struct {
	models.ApiResponse
	Success		bool
	ErrorMessage	string
}
```

ContextFileDeleteResult represents the result of deleting a file in a context.

## Type ContextFileEntry

```go
type ContextFileEntry struct {
	FileID		string
	FileName	string
	FilePath	string
	FileType	string
	GmtCreate	string
	GmtModified	string
	Size		int64
	Status		string
}
```

ContextFileEntry represents a file item in a context.

## Type ContextFileListResult

```go
type ContextFileListResult struct {
	models.ApiResponse
	Success		bool
	Entries		[]*ContextFileEntry
	Count		*int32
	ErrorMessage	string
}
```

ContextFileListResult represents the result of listing files under a context path.

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

ContextFileUrlResult represents a presigned URL operation result.

## Type ContextInfo

```go
type ContextInfo struct {
	Name	string
	ID	string
}
```

ContextInfo represents a context in the GetSession response

## Type ContextInfoResult

```go
type ContextInfoResult struct {
	models.ApiResponse
	Success			bool
	ContextStatusData	[]ContextStatusData	// Parsed context status data
	ErrorMessage		string
}
```

ContextInfoResult wraps context info result and RequestID

## Type ContextListParams

```go
type ContextListParams struct {
	MaxResults	int32	// Number of results per page
	NextToken	string	// Token for the next page
	SessionId	string	// Optional session id filter
}
```

ContextListParams contains parameters for listing contexts

### Related Functions

### NewContextListParams

```go
func NewContextListParams() *ContextListParams
```

NewContextListParams creates a new ContextListParams with default values

## Type ContextListResult

```go
type ContextListResult struct {
	models.ApiResponse
	Success		bool
	Contexts	[]*Context
	NextToken	string
	MaxResults	int32
	TotalCount	int32
	ErrorMessage	string
}
```

ContextListResult wraps context list and RequestID

## Type ContextManager

```go
type ContextManager struct {
	Session interface {
		GetAPIKey() string
		GetClient() *mcp.Client
		GetSessionId() string
	}
}
```

ContextManager handles context operations for a specific session.

### Methods

### Info

```go
func (cm *ContextManager) Info() (*ContextInfoResult, error)
```

Info retrieves context information for the current session.

**Example:**

```go
client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
result, _ := client.Create(nil)
defer result.Session.Delete()
info, _ := result.Session.Context.Info()
```

### InfoWithParams

```go
func (cm *ContextManager) InfoWithParams(contextId, path, taskType string) (*ContextInfoResult, error)
```

InfoWithParams retrieves context information for the current session with optional parameters.

### Sync

```go
func (cm *ContextManager) Sync() (*ContextSyncResult, error)
```

Sync synchronizes the context for the current session.

### SyncWithCallback

```go
func (cm *ContextManager) SyncWithCallback(contextId, path, mode string, callback SyncCallback, maxRetries int, retryInterval int) (*ContextSyncResult, error)
```

SyncWithCallback synchronizes the context with callback support (dual-mode). If callback is
provided, it runs in background and calls callback when complete. If callback is nil, it waits for
completion before returning.

Example (Synchronous mode - waits for completion):


package main

import (

	"fmt"

	"os"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"

)

func main() {

	client, err := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)

	if err != nil {

		fmt.Printf("Error: %v\n", err)

		os.Exit(1)

	}

	result, err := client.Create(nil)

	if err != nil {

		fmt.Printf("Error: %v\n", err)

		os.Exit(1)

	}

	session := result.Session


	// Get or create a context

	contextResult, err := client.Context.Get("my-context", true)

	if err != nil {

		fmt.Printf("Error: %v\n", err)

		os.Exit(1)

	}


	// Synchronous mode: callback is nil, so it waits for completion

	syncResult, err := session.Context.SyncWithCallback(

		contextResult.ContextID,

		"/mnt/persistent",

		"upload",

		nil,  // No callback - synchronous mode

		10,   // maxRetries

		1000, // retryInterval in milliseconds

	)

	if err != nil {

		fmt.Printf("Error: %v\n", err)

		os.Exit(1)

	}

	fmt.Printf("Sync completed - Success: %v\n", syncResult.Success)


	// Output: No sync tasks found

	// Output: Sync completed - Success: true


	session.Delete()

}

Example (Asynchronous mode - with callback):


package main

import (

	"fmt"

	"os"

	"time"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"

)

func main() {

	client, err := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)

	if err != nil {

		fmt.Printf("Error: %v\n", err)

		os.Exit(1)

	}

	result, err := client.Create(nil)

	if err != nil {

		fmt.Printf("Error: %v\n", err)

		os.Exit(1)

	}

	session := result.Session


	// Get or create a context

	contextResult, err := client.Context.Get("my-context", true)

	if err != nil {

		fmt.Printf("Error: %v\n", err)

		os.Exit(1)

	}


	// Asynchronous mode: with callback, returns immediately

	syncResult, err := session.Context.SyncWithCallback(

		contextResult.ContextID,

		"/mnt/persistent",

		"upload",

		func(success bool) {

			if success {

				fmt.Println("Context sync completed successfully")

			} else {

				fmt.Println("Context sync failed or timed out")

			}

		},

		150,  // maxRetries

		1500, // retryInterval in milliseconds

	)

	if err != nil {

		fmt.Printf("Error: %v\n", err)

		os.Exit(1)

	}

	fmt.Printf("Sync triggered - Success: %v\n", syncResult.Success)


	// Wait for callback to complete

	time.Sleep(5 * time.Second)


	// Output: Sync triggered - Success: true

	// Output: Context sync completed successfully


	session.Delete()

}

### SyncWithParams

```go
func (cm *ContextManager) SyncWithParams(contextId, path, mode string) (*ContextSyncResult, error)
```

SyncWithParams synchronizes the context for the current session with optional parameters.

**Example:**

```go
client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
result, _ := client.Create(nil)
defer result.Session.Delete()
session := result.Session
_, _ = session.Context.SyncWithCallback(
	"project-data",
	"/mnt/shared",
	"upload",
	func(success bool, message string) {
		fmt.Printf("Sync callback -> success: %v message: %s\n", success, message)
	},
	20,
	500,
)
```

### Related Functions

### NewContextManager

```go
func NewContextManager(session interface {
	GetAPIKey() string
	GetClient() *mcp.Client
	GetSessionId() string
}) *ContextManager
```

NewContextManager creates a new ContextManager object.

## Type ContextModifyResult

```go
type ContextModifyResult struct {
	models.ApiResponse
	Success		bool
	ErrorMessage	string
}
```

ContextModifyResult wraps context modification result and RequestID

## Type ContextResult

```go
type ContextResult struct {
	models.ApiResponse
	Success		bool
	ContextID	string
	Context		*Context
	ErrorMessage	string
}
```

ContextResult wraps context operation result and RequestID

## Type ContextService

```go
type ContextService struct {
	// AgentBay is the AgentBay instance.
	AgentBay *AgentBay
}
```

ContextService provides methods to manage persistent contexts in the AgentBay cloud environment.

### Methods

### Clear

```go
func (cs *ContextService) Clear(contextID string, timeoutSeconds int, pollIntervalSeconds float64) (*ContextClearResult, error)
```

Clear synchronously clears the context's persistent data and waits for the final result. This method
wraps the ClearAsync and GetClearStatus polling logic.

The clearing process transitions through the following states: - "clearing": Data clearing is in
progress - "available": Clearing completed successfully (final success state)

Parameters:
  - contextID: Unique ID of the context to clear
  - timeout: Timeout in seconds to wait for task completion (default: 60)
  - pollInterval: Interval in seconds between status polls (default: 2)

Returns a ContextClearResult object containing the final task result. The status field will be
"available" on success, or other states if interrupted.

### ClearAsync

```go
func (cs *ContextService) ClearAsync(contextID string) (*ContextClearResult, error)
```

ClearAsync asynchronously initiates a task to clear the context's persistent data. This is a
non-blocking method that returns immediately after initiating the clearing task. The context's state
will transition to "clearing" while the operation is in progress.

Parameters:
  - contextID: Unique ID of the context to clear

Returns:
  - *ContextClearResult: Result containing task status and request ID
  - error: Error if the operation fails

**Example:**

```go
client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
contextResult, _ := client.Context.Get("my-context", true)
clearResult, _ := client.Context.ClearAsync(contextResult.ContextID)
```

### Create

```go
func (cs *ContextService) Create(name string) (*ContextCreateResult, error)
```

Create creates a new context with the given name.

Parameters:
  - name: The name for the new context.

Returns:
  - *ContextCreateResult: A result object containing the created context ID and request ID.
  - error: An error if the operation fails.

**Example:**

```go
client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
createResult, _ := client.Context.Create("my-context")
```

### Delete

```go
func (cs *ContextService) Delete(context *Context) (*ContextDeleteResult, error)
```

Delete deletes the specified context.

Parameters:
  - context: The context object to delete

Returns:
  - *ContextDeleteResult: Result containing success status and request ID
  - error: Error if the operation fails

**Example:**

```go
client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
contextResult, _ := client.Context.Get("my-context", true)
client.Context.Delete(contextResult.Context)
```

### DeleteFile

```go
func (cs *ContextService) DeleteFile(contextID string, filePath string) (*ContextFileDeleteResult, error)
```

DeleteFile deletes a file in a context.

Parameters:
  - contextID: The ID of the context
  - filePath: The path to the file to delete

Returns:
  - *ContextFileDeleteResult: Result containing success status and request ID
  - error: Error if the operation fails

**Example:**

```go
client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
contextResult, _ := client.Context.Get("my-context", true)
client.Context.DeleteFile(contextResult.ContextID, "/data/file.txt")
```

### Get

```go
func (cs *ContextService) Get(name string, create bool) (*ContextResult, error)
```

Get gets a context by name. Optionally creates it if it doesn't exist. Get retrieves an existing
context or creates a new one.

Parameters:
  - name: The name of the context to retrieve or create
  - create: If true, creates the context if it doesn't exist

Returns:
  - *ContextResult: Result containing Context object and request ID
  - error: Error if the operation fails

**Example:**

```go
client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
contextResult, _ := client.Context.Get("my-context", true)
```

### GetClearStatus

```go
func (cs *ContextService) GetClearStatus(contextID string) (*ContextClearResult, error)
```

GetClearStatus queries the status of the clearing task. This method calls GetContext API directly
with contextID and parses the raw response to extract the state field, which indicates the current
clearing status.

Parameters:
  - contextID: Unique ID of the context to check

Returns:
  - *ContextClearResult: Result containing current task status and request ID
  - error: Error if the operation fails

State Transitions:
  - "clearing": Data clearing is in progress
  - "available": Clearing completed successfully (final success state)
  - "in-use": Context is being used
  - "pre-available": Context is being prepared

**Example:**

```go
client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
contextResult, _ := client.Context.Get("my-context", true)
statusResult, _ := client.Context.GetClearStatus(contextResult.ContextID)
```

### GetFileDownloadUrl

```go
func (cs *ContextService) GetFileDownloadUrl(contextID string, filePath string) (*ContextFileUrlResult, error)
```

GetFileDownloadUrl gets a presigned download URL for a file in a context.

Parameters:
  - contextID: The ID of the context
  - filePath: The path to the file in the context

Returns:
  - *ContextFileUrlResult: Result containing the presigned URL, expire time, and request ID
  - error: Error if the operation fails

**Example:**

```go
client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
contextResult, _ := client.Context.Get("my-context", true)
urlResult, _ := client.Context.GetFileDownloadUrl(contextResult.ContextID, "/data/file.txt")
```

### GetFileUploadUrl

```go
func (cs *ContextService) GetFileUploadUrl(contextID string, filePath string) (*ContextFileUrlResult, error)
```

GetFileUploadUrl gets a presigned upload URL for a file in a context.

Parameters:
  - contextID: The ID of the context
  - filePath: The path to the file in the context

Returns:
  - *ContextFileUrlResult: Result containing the presigned URL, expire time, and request ID
  - error: Error if the operation fails

**Example:**

```go
client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
contextResult, _ := client.Context.Get("my-context", true)
urlResult, _ := client.Context.GetFileUploadUrl(contextResult.ContextID, "/data/file.txt")
```

### List

```go
func (cs *ContextService) List(params *ContextListParams) (*ContextListResult, error)
```

List lists all available contexts with pagination support.

Parameters:
  - params: *ContextListParams (optional) - Pagination parameters. If nil, default values are used
    (MaxResults=10).

Returns:
  - *ContextListResult: A result object containing the list of Context objects, pagination info,
    and RequestID.
  - error: An error if the operation fails.

**Example:**

```go
client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
result, _ := client.Context.List(nil)
```

### ListFiles

```go
func (cs *ContextService) ListFiles(contextID string, parentFolderPath string, pageNumber int32, pageSize int32) (*ContextFileListResult, error)
```

ListFiles lists files under a specific folder path in a context.

Parameters:
  - contextID: The ID of the context
  - parentFolderPath: The parent folder path to list files from
  - pageNumber: The page number for pagination
  - pageSize: The number of items per page

Returns:
  - *ContextFileListResult: Result containing the list of files and request ID
  - error: Error if the operation fails

**Example:**

```go
client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
contextResult, _ := client.Context.Get("my-context", true)
fileList, _ := client.Context.ListFiles(contextResult.ContextID, "/", 1, 10)
```

### Update

```go
func (cs *ContextService) Update(context *Context) (*ContextModifyResult, error)
```

Update updates the specified context. Returns a result with success status. Update modifies an
existing context's properties.

Parameters:
  - context: Context object with updated properties

Returns:
  - *ContextModifyResult: Result containing success status and request ID
  - error: Error if the operation fails

**Example:**

```go
client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
contextResult, _ := client.Context.Get("my-context", true)
contextResult.Context.Name = "new-name"
client.Context.Update(contextResult.Context)
```

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

ContextStatusData represents the parsed context status data

## Type ContextStatusItem

```go
type ContextStatusItem struct {
	Type	string	`json:"type"`
	Data	string	`json:"data"`
}
```

ContextStatusItem represents an item in the context status response

## Type ContextSync

```go
type ContextSync struct {
	// ContextID is the ID of the context to synchronize
	ContextID	string	`json:"contextId"`
	// Path is the path where the context should be mounted
	Path	string	`json:"path"`
	// Policy defines the synchronization policy
	Policy	*SyncPolicy	`json:"policy,omitempty"`
}
```

ContextSync defines the context synchronization configuration

### Methods

### WithPolicy

```go
func (cs *ContextSync) WithPolicy(policy *SyncPolicy) (*ContextSync, error)
```

WithPolicy sets the policy and returns the context sync for chaining

### Related Functions

### NewContextSync

```go
func NewContextSync(contextID, path string, policy *SyncPolicy) (*ContextSync, error)
```

NewContextSync creates a new context sync configuration

## Type ContextSyncResult

```go
type ContextSyncResult struct {
	models.ApiResponse
	Success		bool
	ErrorMessage	string
}
```

ContextSyncResult wraps context sync result and RequestID

## Type CreateSessionParams

```go
type CreateSessionParams struct {
	// Labels are custom labels for the Session. These can be used for organizing and filtering sessions.
	Labels	map[string]string

	// ImageId specifies the image ID to use for the session.
	ImageId	string

	// ContextSync is a list of context synchronization configurations.
	// These configurations define how contexts should be synchronized and mounted.
	ContextSync	[]*ContextSync

	// IsVpc specifies whether to create a VPC-based session. Defaults to false.
	IsVpc	bool

	// PolicyId specifies the policy ID to apply when creating the session.
	PolicyId	string

	// ExtraConfigs contains extra configuration settings for different session types
	ExtraConfigs	*models.ExtraConfigs

	// Framework specifies the framework name for tracking (e.g., "langchain"). Empty string means direct call.
	Framework	string

	// EnableBrowserReplay specifies whether to enable browser recording for this session.
	EnableBrowserReplay	bool
}
```

CreateSessionParams provides a way to configure the parameters for creating a new session in the
AgentBay cloud environment.

### Methods

### AddContextSync

```go
func (p *CreateSessionParams) AddContextSync(contextID, path string, policy *SyncPolicy) *CreateSessionParams
```

AddContextSync adds a context sync configuration to the session parameters.

### AddContextSyncConfig

```go
func (p *CreateSessionParams) AddContextSyncConfig(contextSync *ContextSync) *CreateSessionParams
```

AddContextSyncConfig adds a pre-configured context sync to the session parameters.

### GetExtraConfigsJSON

```go
func (p *CreateSessionParams) GetExtraConfigsJSON() (string, error)
```

GetExtraConfigsJSON returns the extra configs as a JSON string.

### GetLabelsJSON

```go
func (p *CreateSessionParams) GetLabelsJSON() (string, error)
```

GetLabelsJSON returns the labels as a JSON string.

### WithContextSync

```go
func (p *CreateSessionParams) WithContextSync(contextSyncs []*ContextSync) *CreateSessionParams
```

WithContextSync sets the context sync configurations for the session parameters.

### WithEnableBrowserReplay

```go
func (p *CreateSessionParams) WithEnableBrowserReplay(enableBrowserReplay bool) *CreateSessionParams
```

WithEnableBrowserReplay sets the browser replay flag for the session parameters and returns the
updated parameters.

### WithExtraConfigs

```go
func (p *CreateSessionParams) WithExtraConfigs(extraConfigs *models.ExtraConfigs) *CreateSessionParams
```

WithExtraConfigs sets the extra configurations for the session parameters and returns the updated
parameters.

### WithImageId

```go
func (p *CreateSessionParams) WithImageId(imageId string) *CreateSessionParams
```

WithImageId sets the image ID for the session parameters and returns the updated parameters.

### WithIsVpc

```go
func (p *CreateSessionParams) WithIsVpc(isVpc bool) *CreateSessionParams
```

WithIsVpc sets the VPC flag for the session parameters and returns the updated parameters.

### WithLabels

```go
func (p *CreateSessionParams) WithLabels(labels map[string]string) *CreateSessionParams
```

WithLabels sets the labels for the session parameters and returns the updated parameters.

### WithPolicyId

```go
func (p *CreateSessionParams) WithPolicyId(policyId string) *CreateSessionParams
```

WithPolicyId sets the policy ID for the session parameters and returns the updated parameters.

### Related Functions

### NewCreateSessionParams

```go
func NewCreateSessionParams() *CreateSessionParams
```

NewCreateSessionParams creates a new CreateSessionParams with default values.

## Type DeletePolicy

```go
type DeletePolicy struct {
	// SyncLocalFile enables synchronization of local file deletions
	SyncLocalFile bool `json:"syncLocalFile"`
}
```

DeletePolicy defines the delete policy for context synchronization

### Related Functions

### NewDeletePolicy

```go
func NewDeletePolicy() *DeletePolicy
```

NewDeletePolicy creates a new delete policy with default values

## Type DeleteResult

```go
type DeleteResult struct {
	models.ApiResponse
	Success		bool
	ErrorMessage	string
}
```

DeleteResult wraps deletion operation result and RequestID

## Type DeprecationConfig

```go
type DeprecationConfig struct {
	// Enabled controls whether deprecation warnings are shown
	Enabled	bool
	// Level controls the severity of deprecation warnings
	Level	DeprecationLevel
	// ShowStackTrace controls whether to show stack trace in warnings
	ShowStackTrace	bool
}
```

DeprecationConfig holds configuration for deprecation warnings

### Related Functions

### DefaultDeprecationConfig

```go
func DefaultDeprecationConfig() *DeprecationConfig
```

DefaultDeprecationConfig returns the default deprecation configuration

### GetDeprecationConfig

```go
func GetDeprecationConfig() *DeprecationConfig
```

GetDeprecationConfig returns the current global deprecation configuration

## Type DeprecationLevel

```go
type DeprecationLevel int
```

DeprecationLevel represents the level of deprecation warning

## Type DownloadPolicy

```go
type DownloadPolicy struct {
	// AutoDownload enables automatic download
	AutoDownload	bool	`json:"autoDownload"`
	// DownloadStrategy defines the download strategy
	DownloadStrategy	DownloadStrategy	`json:"downloadStrategy"`
}
```

DownloadPolicy defines the download policy for context synchronization

### Related Functions

### NewDownloadPolicy

```go
func NewDownloadPolicy() *DownloadPolicy
```

NewDownloadPolicy creates a new download policy with default values

## Type DownloadStrategy

```go
type DownloadStrategy string
```

DownloadStrategy defines the download strategy for context synchronization

## Type ExtractPolicy

```go
type ExtractPolicy struct {
	// Extract enables file extraction
	Extract	bool	`json:"extract"`
	// DeleteSrcFile enables deletion of source file after extraction
	DeleteSrcFile	bool	`json:"deleteSrcFile"`
	// ExtractToCurrentFolder enables extraction to current folder
	ExtractToCurrentFolder	bool	`json:"extractToCurrentFolder"`
}
```

ExtractPolicy defines the extract policy for context synchronization

### Related Functions

### NewExtractPolicy

```go
func NewExtractPolicy() *ExtractPolicy
```

NewExtractPolicy creates a new extract policy with default values

## Type GetSessionData

```go
type GetSessionData struct {
	AppInstanceID		string
	ResourceID		string
	SessionID		string
	Success			bool
	HttpPort		string
	NetworkInterfaceIP	string
	Token			string
	VpcResource		bool
	ResourceUrl		string
	Status			string
	Contexts		[]ContextInfo
}
```

GetSessionData represents the data returned by GetSession API

## Type GetSessionResult

```go
type GetSessionResult struct {
	models.ApiResponse
	HttpStatusCode	int32
	Code		string
	Success		bool
	Data		*GetSessionData
	ErrorMessage	string
}
```

GetSessionResult represents the result of GetSession operation

## Type InfoResult

```go
type InfoResult struct {
	models.ApiResponse
	Info	*SessionInfo
}
```

InfoResult wraps SessionInfo and RequestID

## Type LabelResult

```go
type LabelResult struct {
	models.ApiResponse
	Labels	string
}
```

LabelResult wraps label operation result and RequestID

## Type Lifecycle

```go
type Lifecycle string
```

Lifecycle defines the lifecycle options for recycle policy

## Type LinkResult

```go
type LinkResult struct {
	models.ApiResponse
	Link	string
}
```

LinkResult wraps link result and RequestID

## Type ListSessionParams

```go
type ListSessionParams struct {
	MaxResults	int32			// Number of results per page
	NextToken	string			// Token for the next page
	Labels		map[string]string	// Labels to filter by
}
```

ListSessionParams contains parameters for listing sessions

### Related Functions

### NewListSessionParams

```go
func NewListSessionParams() *ListSessionParams
```

NewListSessionParams creates a new ListSessionParams with default values

## Type LoggerConfig

```go
type LoggerConfig struct {
	Level		string
	LogFile		string
	MaxFileSize	string
	EnableConsole	*bool
}
```

LoggerConfig holds configuration for file logging

## Type MappingPolicy

```go
type MappingPolicy struct {
	// Path is the original path from a different OS that should be mapped to the current context path
	Path string `json:"path"`
}
```

MappingPolicy defines the mapping policy for cross-platform context synchronization

### Related Functions

### NewMappingPolicy

```go
func NewMappingPolicy() *MappingPolicy
```

NewMappingPolicy creates a new mapping policy with default values

## Type McpTool

```go
type McpTool struct {
	Name		string			`json:"name"`		// Tool name
	Description	string			`json:"description"`	// Tool description
	InputSchema	map[string]interface{}	`json:"inputSchema"`	// Input parameter schema
	Server		string			`json:"server"`		// Server name that provides this tool
	Tool		string			`json:"tool"`		// Tool identifier
}
```

McpTool represents an MCP tool with complete information

### Methods

### GetName

```go
func (m *McpTool) GetName() string
```

GetName returns the tool name

### GetServer

```go
func (m *McpTool) GetServer() string
```

GetServer returns the server name that provides this tool

## Type McpToolsResult

```go
type McpToolsResult struct {
	models.ApiResponse
	Tools	[]McpTool
}
```

McpToolsResult wraps MCP tools list and RequestID

## Type MobileSimulateService

```go
type MobileSimulateService struct {
	agentBay		*AgentBay
	contextService		*ContextService
	simulateEnable		bool
	simulateMode		models.MobileSimulateMode
	contextID		string
	contextSync		*ContextSync
	mobileDevInfoPath	string
	useInternalContext	bool
}
```

MobileSimulateService provides methods to manage persistent mobile dev info and sync to the mobile
device

### Methods

### GetSimulateConfig

```go
func (m *MobileSimulateService) GetSimulateConfig() *models.MobileSimulateConfig
```

GetSimulateConfig gets the simulate config Returns:
  - MobileSimulateConfig: The simulate config
  - Simulate: The simulate feature enable flag
  - SimulatePath: The path of the mobile dev info file
  - SimulateMode: The simulate mode
  - SimulatedContextID: The context ID of the mobile info

### GetSimulateContextID

```go
func (m *MobileSimulateService) GetSimulateContextID() string
```

GetSimulateContextID gets the simulate context id

### GetSimulateEnable

```go
func (m *MobileSimulateService) GetSimulateEnable() bool
```

GetSimulateEnable gets the simulate enable flag

### GetSimulateMode

```go
func (m *MobileSimulateService) GetSimulateMode() models.MobileSimulateMode
```

GetSimulateMode gets the simulate mode

### SetSimulateContextID

```go
func (m *MobileSimulateService) SetSimulateContextID(contextID string)
```

SetSimulateContextID sets a previously saved simulate context id Please make sure the context id is
provided by MobileSimulateService but not user side created context

### SetSimulateEnable

```go
func (m *MobileSimulateService) SetSimulateEnable(enable bool)
```

SetSimulateEnable sets the simulate enable flag

### SetSimulateMode

```go
func (m *MobileSimulateService) SetSimulateMode(mode models.MobileSimulateMode)
```

SetSimulateMode sets the simulate mode mode: The simulate mode
  - PropertiesOnly: Simulate only device properties
  - SensorsOnly: Simulate only device sensors
  - PackagesOnly: Simulate only installed packages
  - ServicesOnly: Simulate only system services
  - All: Simulate all aspects of the device

### UploadMobileInfo

```go
func (m *MobileSimulateService) UploadMobileInfo(mobileDevInfoContent string, contextSync *ContextSync) *MobileSimulateUploadResult
```

UploadMobileInfo uploads the mobile simulate dev info

Args:
  - mobileDevInfoContent: The mobile simulate dev info content to upload
  - contextSync: Optional
  - If not provided, a new context sync will be created for the mobile simulate service and this
    context id will return by the MobileSimulateUploadResult. User can use this context id to do
    persistent mobile simulate across sessions.
  - If provided, the mobile simulate dev info will be uploaded to the context sync in a specific
    path.

Returns:
  - MobileSimulateUploadResult: The result of the upload operation
  - Success: Whether the operation was successful
  - MobileSimulateContextID: The context ID of the mobile info
  - ErrorMessage: The error message if the operation failed

Notes:


If context_sync is not provided, a new context sync will be created for the mobile simulate.

If context_sync is provided, the mobile simulate dev info will be uploaded to the context sync.

If the mobile simulate dev info already exists in the context sync, the context sync will be updated.

If the mobile simulate dev info does not exist in the context sync, the context sync will be created.

If the upload operation fails, the error message will be returned.

### Related Functions

### NewMobileSimulateService

```go
func NewMobileSimulateService(agentBay *AgentBay) (*MobileSimulateService, error)
```

NewMobileSimulateService creates a new MobileSimulateService instance

## Type MobileSimulateUploadResult

```go
type MobileSimulateUploadResult struct {
	Success			bool
	MobileSimulateContextID	string
	ErrorMessage		string
}
```

MobileSimulateUploadResult represents the result of uploading mobile info

## Type Option

```go
type Option func(*AgentBayConfig)
```

Option is a function that sets optional parameters for AgentBay client.

### Related Functions

### WithConfig

```go
func WithConfig(cfg *Config) Option
```

WithConfig returns an Option that sets the configuration for the AgentBay client.

### WithEnvFile

```go
func WithEnvFile(envFile string) Option
```

WithEnvFile returns an Option that sets a custom .env file path for the AgentBay client.

## Type RecyclePolicy

```go
type RecyclePolicy struct {
	// Lifecycle defines how long the context data should be retained
	Lifecycle	Lifecycle	`json:"lifecycle"`
	// Paths specifies which directories or files should be subject to the recycle policy
	Paths	[]string	`json:"paths"`
}
```

RecyclePolicy defines the recycle policy for context synchronization

The RecyclePolicy determines how long context data should be retained and which paths are subject to
the policy.

Lifecycle field determines the data retention period:
  - Lifecycle1Day: Keep data for 1 day
  - Lifecycle3Days: Keep data for 3 days
  - Lifecycle5Days: Keep data for 5 days
  - Lifecycle10Days: Keep data for 10 days
  - Lifecycle15Days: Keep data for 15 days
  - Lifecycle30Days: Keep data for 30 days
  - Lifecycle90Days: Keep data for 90 days
  - Lifecycle180Days: Keep data for 180 days
  - Lifecycle360Days: Keep data for 360 days
  - LifecycleForever: Keep data permanently (default)

Paths field specifies which directories or files should be subject to the recycle policy:
  - Must use exact directory/file paths
  - Wildcard patterns (* ? [ ]) are NOT supported
  - Empty string "" means apply to all paths in the context
  - Multiple paths can be specified as a slice
  - Default: []string{""} (applies to all paths)

### Related Functions

### NewRecyclePolicy

```go
func NewRecyclePolicy() *RecyclePolicy
```

NewRecyclePolicy creates a new recycle policy with default values

## Type Session

```go
type Session struct {
	AgentBay	*AgentBay
	SessionID	string
	ImageId		string	// ImageId used when creating this session

	// VPC-related information
	IsVpcEnabled		bool	// Whether this session uses VPC resources
	NetworkInterfaceIP	string	// Network interface IP for VPC sessions
	HttpPortNumber		string	// HTTP port for VPC sessions
	Token			string	// Token for VPC sessions

	// Resource URL for accessing the session
	ResourceUrl	string

	// Browser replay enabled flag
	EnableBrowserReplay	bool

	// File, command and code handlers
	FileSystem	*filesystem.FileSystem
	Command		*command.Command
	Code		*code.Code
	Oss		*oss.OSSManager

	// Platform-specific automation modules
	Computer	*computer.Computer
	Mobile		*mobile.Mobile

	// Browser for web automation
	Browser	*browser.Browser

	// Agent for task execution
	Agent	*agent.Agent

	// Context management
	Context	*ContextManager

	// MCP tools available for this session
	McpTools	[]McpTool
}
```

Session represents a session in the AgentBay cloud environment.

### Methods

### CallMcpToolForBrowser

```go
func (s *Session) CallMcpToolForBrowser(toolName string, args interface{}) (*browser.McpToolResult, error)
```

CallMcpTool is a wrapper that converts the result to browser.McpToolResult

### Delete

```go
func (s *Session) Delete(syncContext ...bool) (*DeleteResult, error)
```

Delete deletes this session. Delete deletes the session and releases all associated resources.

Parameters:
  - syncContext: Optional boolean to synchronize context data before deletion. If true, uploads all
    context data to OSS. Defaults to false.

Returns:
  - *DeleteResult: Result containing success status and request ID
  - error: Error if the operation fails

Behavior:

- If syncContext is true: Uploads all context data to OSS before deletion - If syncContext is false:
Deletes immediately without sync - Continues with deletion even if context sync fails - Releases all
associated resources (browser, computer, mobile, etc.)

**Example:**

```go
client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
result, _ := client.Create(nil)
defer result.Session.Delete()
deleteResult, _ := result.Session.Delete()
```

### FindServerForTool

```go
func (s *Session) FindServerForTool(toolName string) string
```

FindServerForTool searches for the server that provides the given tool

### GetEnableBrowserReplay

```go
func (s *Session) GetEnableBrowserReplay() bool
```

GetEnableBrowserReplay returns whether browser replay is enabled for this session.

### GetLabels

```go
func (s *Session) GetLabels() (*LabelResult, error)
```

GetLabels gets the labels for this session.

Returns:
  - *LabelResult: Result containing labels as JSON string and request ID
  - error: Error if the operation fails

Behavior:

- Retrieves the labels that were previously set for this session - Returns labels as a JSON string -
Can be used to identify and filter sessions

**Example:**

```go
client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
result, _ := client.Create(nil)
defer result.Session.Delete()
labelResult, _ := result.Session.GetLabels()
```

### GetLink

```go
func (s *Session) GetLink(protocolType *string, port *int32, options *string) (*LinkResult, error)
```

GetLink gets the link for this session. GetLink retrieves an access link for the session.

Parameters:
  - protocolType: Protocol type for the link (optional, reserved for future use)
  - port: Specific port number to access (must be in range [30100, 30199])
  - options: Additional options (optional)

Returns:
  - *LinkResult: Result containing the access URL and request ID
  - error: Error if port is out of range or operation fails

Behavior:

- Without port: Returns the default session access URL - With port: Returns URL for accessing
specific port-mapped service - Port must be in range [30100, 30199] for port forwarding

**Example:**

```go
client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
result, _ := client.Create(nil)
defer result.Session.Delete()
port := int32(30100)
linkResult, _ := result.Session.GetLink(nil, &port, nil)
```

### GetLinkForBrowser

```go
func (s *Session) GetLinkForBrowser(protocolType *string, port *int32, options *string) (*browser.LinkResult, error)
```

GetLinkForBrowser is a wrapper that converts the result to browser.LinkResult

### GetToken

```go
func (s *Session) GetToken() string
```

GetToken returns the token for VPC sessions

### Info

```go
func (s *Session) Info() (*InfoResult, error)
```

Info gets information about this session. Info retrieves detailed information about the current
session.

Returns:
  - *InfoResult: Result containing SessionInfo object and request ID
  - error: Error if the operation fails or session not found

Behavior:

- Retrieves current session metadata from the backend - Includes resource URL, type, and connection
properties - Information is fetched in real-time from the API

**Example:**

```go
client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
result, _ := client.Create(nil)
defer result.Session.Delete()
infoResult, _ := result.Session.Info()
```

### ListMcpTools

```go
func (s *Session) ListMcpTools() (*McpToolsResult, error)
```

ListMcpTools lists MCP tools available for this session. It uses the ImageId from the session
creation, or "linux_latest" as default.

Returns:
  - *McpToolsResult: Result containing list of MCP tools and request ID
  - error: Error if the operation fails

Behavior:

- Uses the ImageId from session creation - Defaults to "linux_latest" if ImageId is empty -
Retrieves all available MCP tools for the specified image - Updates the session's McpTools field
with the retrieved tools

**Example:**

```go
client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
result, _ := client.Create(nil)
defer result.Session.Delete()
toolsResult, _ := result.Session.ListMcpTools()
```

### Pause

```go
func (s *Session) Pause(timeout int, pollInterval float64) (*models.SessionPauseResult, error)
```

Pause synchronously pauses this session, putting it into a dormant state to reduce resource
usage and costs. Pause puts the session into a PAUSED state where computational resources are
significantly reduced. The session state is preserved and can be resumed later to continue work.

Parameters:
  - timeout: Timeout in seconds to wait for the session to pause. Defaults to 600 seconds.
  - pollInterval: Interval in seconds between status polls. Defaults to 2.0 seconds.

Returns:
  - *models.SessionPauseResult: Result containing success status, request ID, and error message if
    any.
  - error: Error if the operation fails at the transport level

Behavior:

- Initiates pause operation through the PauseSessionAsync API - Polls session status until PAUSED
state or timeout - Returns detailed result with success status and request tracking

Exceptions:

- Returns error result (not Go error) for API-level errors like invalid session ID - Returns error
result for timeout conditions - Returns Go error for transport-level failures

**Example:**

```go
client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"))
result, _ := client.Create(nil)
defer result.Session.Delete()
pauseResult, _ := result.Session.Pause(300, 2.0)
```

### Resume

```go
func (s *Session) Resume(timeout int, pollInterval float64) (*models.SessionResumeResult, error)
```

Resume synchronously resumes this session from a paused state to continue work. Resume restores the
session from PAUSED state back to RUNNING state. All previous session state and data are preserved
during resume operation.

Parameters:
  - timeout: Timeout in seconds to wait for the session to resume. Defaults to 600 seconds.
  - pollInterval: Interval in seconds between status polls. Defaults to 2.0 seconds.

Returns:
  - *models.SessionResumeResult: Result containing success status, request ID, and error message if
    any.
  - error: Error if the operation fails at the transport level

Behavior:

- Initiates resume operation through the ResumeSessionAsync API - Polls session status until RUNNING
state or timeout - Returns detailed result with success status and request tracking

Exceptions:

- Returns error result (not Go error) for API-level errors like invalid session ID - Returns error
result for timeout conditions - Returns Go error for transport-level failures

**Example:**

```go
client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"))
result, _ := client.Create(nil)
defer result.Session.Delete()
result.Session.Pause(300, 2.0)
resumeResult, _ := result.Session.Resume(300, 2.0)
```

### SetLabels

```go
func (s *Session) SetLabels(labels map[string]string) (*LabelResult, error)
```

SetLabels sets the labels for this session.

Parameters:
  - labels: Labels to set for the session as a map of key-value pairs

Returns:
  - *LabelResult: Result containing request ID
  - error: Error if validation fails or operation fails

Behavior:

- Validates that labels map is not nil or empty - All keys and values must be non-empty strings
- Converts labels to JSON and sends to the backend - Labels can be used for session filtering and
organization

**Example:**

```go
client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
result, _ := client.Create(nil)
defer result.Session.Delete()
labels := map[string]string{"env": "test"}
labelResult, _ := result.Session.SetLabels(labels)
```

### Related Functions

### NewSession

```go
func NewSession(agentBay *AgentBay, sessionID string) *Session
```

NewSession creates a new Session object.

## Type SessionInfo

```go
type SessionInfo struct {
	SessionId		string
	ResourceUrl		string
	AppId			string
	AuthCode		string
	ConnectionProperties	string
	ResourceId		string
	ResourceType		string
	Ticket			string
}
```

SessionInfo contains information about a session.

## Type SessionListResult

```go
type SessionListResult struct {
	models.ApiResponse
	SessionIds	[]string	// Session IDs
	NextToken	string		// Token for the next page
	MaxResults	int32		// Number of results per page
	TotalCount	int32		// Total number of results
}
```

SessionListResult wraps Session list and RequestID

## Type SessionResult

```go
type SessionResult struct {
	models.ApiResponse
	Session		*Session
	Success		bool
	ErrorMessage	string
}
```

SessionResult wraps Session object and RequestID

## Type SyncCallback

```go
type SyncCallback func(success bool)
```

SyncCallback defines the callback function type for async sync operations

## Type SyncPolicy

```go
type SyncPolicy struct {
	// UploadPolicy defines the upload policy
	UploadPolicy	*UploadPolicy	`json:"uploadPolicy,omitempty"`
	// DownloadPolicy defines the download policy
	DownloadPolicy	*DownloadPolicy	`json:"downloadPolicy,omitempty"`
	// DeletePolicy defines the delete policy
	DeletePolicy	*DeletePolicy	`json:"deletePolicy,omitempty"`
	// ExtractPolicy defines the extract policy
	ExtractPolicy	*ExtractPolicy	`json:"extractPolicy,omitempty"`
	// RecyclePolicy defines the recycle policy
	RecyclePolicy	*RecyclePolicy	`json:"recyclePolicy,omitempty"`
	// BWList defines the black and white list
	BWList	*BWList	`json:"bwList,omitempty"`
	// MappingPolicy defines the mapping policy for cross-platform context synchronization
	MappingPolicy	*MappingPolicy	`json:"mappingPolicy,omitempty"`
}
```

SyncPolicy defines the synchronization policy

### Related Functions

### NewSyncPolicy

```go
func NewSyncPolicy() *SyncPolicy
```

NewSyncPolicy creates a new sync policy with default values

## Type UploadMode

```go
type UploadMode string
```

UploadMode defines the upload mode for context synchronization

## Type UploadPolicy

```go
type UploadPolicy struct {
	// AutoUpload enables automatic upload
	AutoUpload	bool	`json:"autoUpload"`
	// UploadStrategy defines the upload strategy
	UploadStrategy	UploadStrategy	`json:"uploadStrategy"`
	// UploadMode defines the upload mode
	UploadMode	UploadMode	`json:"uploadMode"`
}
```

UploadPolicy defines the upload policy for context synchronization

### Related Functions

### NewUploadPolicy

```go
func NewUploadPolicy() *UploadPolicy
```

NewUploadPolicy creates a new upload policy with default values

## Type UploadStrategy

```go
type UploadStrategy string
```

UploadStrategy defines the upload strategy for context synchronization

## Type WhiteList

```go
type WhiteList struct {
	// Path is the path to include in the white list
	Path	string	`json:"path"`
	// ExcludePaths are the paths to exclude from the white list
	ExcludePaths	[]string	`json:"excludePaths,omitempty"`
}
```

WhiteList defines the white list configuration

## Type configManager

```go
type configManager struct{}
```

configManager implementation for backward compatibility

## Functions

### Deprecated

```go
func Deprecated(reason, replacement, version string)
```

Deprecated marks a function or method as deprecated and emits a warning

### GetLogLevel

```go
func GetLogLevel() int
```

GetLogLevel returns the current global log level

**Example:**

```go
package main
import (
	"fmt"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)
func main() {

	// Set log level to DEBUG

	agentbay.SetLogLevel(agentbay.LOG_DEBUG)

	// Check current level

	currentLevel := agentbay.GetLogLevel()
	fmt.Printf("Current log level: %d\n", currentLevel)
}
```

### GetSupportedKeyNames

```go
func GetSupportedKeyNames() map[string]map[string]string
```

GetSupportedKeyNames returns a dictionary of all supported key name mappings.

Returns:


A map with categories and their supported key names

**Example:**

```go
mappings := GetSupportedKeyNames()
fmt.Println(mappings["modifierKeys"])  // map[ctrl:Ctrl alt:Alt ...]
```

### LogDebug

```go
func LogDebug(message string)
```

LogDebug logs a debug message

**Example:**

```go
agentbay.LogDebug("Processing request parameters")
```

### LogInfo

```go
func LogInfo(message string)
```

LogInfo logs an informational message

**Example:**

```go
agentbay.LogInfo("Session created successfully")
```

### NormalizeKeys

```go
func NormalizeKeys(keys []string) []string
```

NormalizeKeys normalizes a list of key names to the correct case format for press_keys tool.

This function automatically converts key names to the format expected by the press_keys MCP tool,
improving case compatibility and user experience.

**Example:**

```go
NormalizeKeys([]string{"CTRL", "C"})           // returns ["Ctrl", "c"]
NormalizeKeys([]string{"ctrl", "shift", "Z"})  // returns ["Ctrl", "Shift", "z"]
NormalizeKeys([]string{"alt", "TAB"})          // returns ["Alt", "Tab"]
NormalizeKeys([]string{"win", "d"})            // returns ["Win", "d"]
Note:
  - Modifier keys are converted to Title Case (Ctrl, Alt, Shift, Win)
  - Function keys are converted to Title Case (Tab, Enter, Escape)
  - Letter keys are converted to lowercase (a, b, c)
  - Number keys remain unchanged (0, 1, 2)
  - Unknown keys are returned as-is
```

### NormalizeSingleKey

```go
func NormalizeSingleKey(key string) string
```

NormalizeSingleKey normalizes a single key name to the correct case format.

Rules:
  - Letter keys (a-z): Convert to lowercase
  - Number keys (0-9): Keep as-is
  - Modifier keys: Convert to Title Case (Ctrl, Alt, Shift, Win, etc.)
  - Function keys: Convert to Title Case (Tab, Enter, Escape, etc.)
  - Arrow keys: Convert to Title Case (ArrowUp, ArrowDown, etc.)
  - F-keys: Convert to correct format (F1, F2, ..., F12)
  - Unknown keys: Return as-is

**Example:**

```go
NormalizeSingleKey("A")        // returns "a"
NormalizeSingleKey("ctrl")     // returns "Ctrl"
NormalizeSingleKey("CTRL")     // returns "Ctrl"
NormalizeSingleKey("TAB")      // returns "Tab"
NormalizeSingleKey("f1")       // returns "F1"
```

### SetDeprecationConfig

```go
func SetDeprecationConfig(config *DeprecationConfig)
```

SetDeprecationConfig sets the global deprecation configuration

### SetLogLevel

```go
func SetLogLevel(level int)
```

SetLogLevel sets the global log level

**Example:**

```go
agentbay.SetLogLevel(agentbay.LOG_DEBUG)
```

### SetupLogger

```go
func SetupLogger(config LoggerConfig)
```

SetupLogger configures the logger with file logging support

**Example:**

```go
config := agentbay.LoggerConfig{Level: "DEBUG", LogFile: "/tmp/agentbay.log"}
agentbay.SetupLogger(config)
```

---

*Documentation generated automatically from Go source code.*
