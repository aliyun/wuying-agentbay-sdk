# AgentBay API Reference

## 🚀 Related Tutorial

- [First Session Tutorial](../../../../../docs/quickstart/first-session.md) - Get started with creating your first AgentBay session

## Type AgentBayConfig

```go
type AgentBayConfig struct {
	cfg	*Config
	envFile	string
}
```

AgentBayConfig holds optional configuration for the AgentBay client.

## Type AgentBay

```go
type AgentBay struct {
	APIKey		string
	Client		*mcp.Client
	Sessions	sync.Map
	Context		*ContextService
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

## Functions

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

## Related Resources

- [Session API Reference](session.md)
- [Context API Reference](context.md)

---

*Documentation generated automatically from Go source code.*
