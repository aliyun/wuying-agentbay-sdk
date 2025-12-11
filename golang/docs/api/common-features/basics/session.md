# Session API Reference

## 🔧 Related Tutorial

- [Session Management Guide](../../../../../docs/guides/common-features/basics/session-management.md) - Detailed tutorial on session lifecycle and management

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

## Type LinkResult

```go
type LinkResult struct {
	models.ApiResponse
	Link	string
}
```

LinkResult wraps link result and RequestID

## Type DeleteResult

```go
type DeleteResult struct {
	models.ApiResponse
	Success		bool
	ErrorMessage	string
}
```

DeleteResult wraps deletion operation result and RequestID

## Type McpToolsResult

```go
type McpToolsResult struct {
	models.ApiResponse
	Tools	[]McpTool
}
```

McpToolsResult wraps MCP tools list and RequestID

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

## Functions

### NewSession

```go
func NewSession(agentBay *AgentBay, sessionID string) *Session
```

NewSession creates a new Session object.

### NewCreateSessionParams

```go
func NewCreateSessionParams() *CreateSessionParams
```

NewCreateSessionParams creates a new CreateSessionParams with default values.

## Related Resources

- [FileSystem API Reference](filesystem.md)
- [Command API Reference](command.md)
- [Context API Reference](context.md)
- [Context Manager API Reference](context-manager.md)
- [OSS API Reference](../advanced/oss.md)

---

*Documentation generated automatically from Go source code.*
