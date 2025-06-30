# Session Class API Reference

The `Session` class represents a session in the AgentBay cloud environment. A session is a container for executing commands and manipulating files. Each session has its own isolated environment.

## Properties

### Python

- `session_id`: The ID of the session.
- `resource_url`: The resource URL associated with the session.
- `filesystem`: The FileSystem instance for this session.
- `command`: The Command instance for this session.
- `ui`: The UI instance for this session.
- `application`: The Application instance for this session.
- `window`: The Window instance for this session.

### TypeScript

- `sessionId`: The ID of the session.
- `resourceUrl`: The resource URL associated with the session.
- `filesystem`: The FileSystem instance for this session.
- `command`: The Command instance for this session.
- `ui`: The UI instance for this session.
- `application`: The Application instance for this session.
- `window`: The Window instance for this session.

### Golang

- `SessionID`: The ID of the session.
- `ResourceUrl`: The resource URL associated with the session.
- `FileSystem`: The FileSystem instance for this session.
- `Command`: The Command instance for this session.
- `UI`: The UI instance for this session.
- `Application`: The Application instance for this session.
- `Window`: The Window instance for this session.

## Methods

### delete / Delete

Deletes the session.

#### Python

```python
delete() -> DeleteResult
```

**Returns:**
- `DeleteResult`: A result object containing success status, request ID, and error message if the deletion failed.

**Note:**
The return type has been updated to return a structured `DeleteResult` object instead of a boolean value. This provides more detailed information about the operation result.

#### TypeScript

```typescript
delete(): Promise<boolean>
```

**Returns:**
- `Promise<boolean>`: A promise that resolves to true if the session was deleted successfully, false otherwise.

**Throws:**
- `APIError`: If the session deletion fails.

#### Golang

```go
Delete() (*DeleteResult, error)
```

**Returns:**
- `*DeleteResult`: A result object containing success status and RequestID.
- `error`: An error if the session deletion fails.

**DeleteResult Structure:**
```go
type DeleteResult struct {
    RequestID string // Unique request identifier for debugging
    Success   bool   // Whether the deletion was successful
}
```

### set_labels / setLabels / SetLabels

Sets labels for the session. Labels are key-value pairs that can be used to categorize and filter sessions.

#### Python

```python
set_labels(labels: Dict[str, str]) -> OperationResult
```

**Parameters:**
- `labels` (Dict[str, str]): A dictionary of labels to set for the session.

**Returns:**
- `OperationResult`: A result object containing success status, request ID, and error message if any.

**Raises:**
- `AgentBayError`: If setting the labels fails due to API errors or other issues.

#### TypeScript

```typescript
setLabels(labels: Record<string, string>): Promise<void>
```

**Parameters:**
- `labels` (Record<string, string>): An object of labels to set for the session.

**Throws:**
- `APIError`: If setting the labels fails.

#### Golang

```go
SetLabels(labels map[string]string) error
```

**Parameters:**
- `labels` (map[string]string): A map of labels to set for the session.

**Returns:**
- `error`: An error if setting the labels fails.

### get_labels / getLabels / GetLabels

Gets the labels for the session.

#### Python

```python
get_labels() -> OperationResult
```

**Returns:**
- `OperationResult`: A result object containing the labels as data, success status, request ID, and error message if any.

**Raises:**
- `AgentBayError`: If getting the labels fails due to API errors or other issues.

#### TypeScript

```typescript
getLabels(): Promise<Record<string, string>>
```

**Returns:**
- `Promise<Record<string, string>>`: A promise that resolves to an object of labels for the session.

**Throws:**
- `APIError`: If getting the labels fails.

#### Golang

```go
GetLabels() (map[string]string, error)
```

**Returns:**
- `map[string]string`: A map of labels for the session.
- `error`: An error if getting the labels fails.

### get_link / getLink / GetLink

Gets the public link for the session which can be used to access the session from a browser.

#### Python

```python
get_link(protocol_type: Optional[str] = None, port: Optional[int] = None) -> OperationResult
```

**Parameters:**
- `protocol_type` (str, optional): The protocol type for the link (e.g., "http", "https").
- `port` (int, optional): The port number for the link.

**Returns:**
- `OperationResult`: A result object containing the link as data, success status, request ID, and error message if any.

**Raises:**
- `AgentBayError`: If getting the link fails due to API errors or other issues.

#### TypeScript

```typescript
getLink(): Promise<string>
```

**Returns:**
- `Promise<string>`: A promise that resolves to the link for the session.

**Throws:**
- `APIError`: If getting the link fails.

#### Golang

```go
GetLink() (string, error)
```

**Returns:**
- `string`: The link for the session.
- `error`: An error if getting the link fails.

### info / Info

Gets information about the session, including the session ID, resource URL, and desktop information.

#### Python

```python
info() -> Dict[str, Any]
```

**Returns:**
- `Dict[str, Any]`: A dictionary containing information about the session, with the following keys:
  - `session_id` (str): The ID of the session.
  - `resource_url` (str): The resource URL associated with the session.
  - `app_id` (str, optional): The application ID associated with the desktop.
  - `auth_code` (str, optional): The authentication code for the desktop.
  - `connection_properties` (str, optional): Connection properties for the desktop.
  - `resource_id` (str, optional): The resource ID of the desktop.
  - `resource_type` (str, optional): The type of the desktop resource.

**Raises:**
- `AgentBayError`: If getting the session information fails.

#### TypeScript

```typescript
info(): Promise<{
  sessionId: string;
  resourceUrl: string;
  appId?: string;
  authCode?: string;
  connectionProperties?: string;
  resourceId?: string;
  resourceType?: string;
}>
```

**Returns:**
- `Promise<SessionInfo>`: A promise that resolves to an object containing information about the session.

**Throws:**
- `APIError`: If getting the session information fails.

#### Golang

```go
Info() (*SessionInfo, error)
```

**Returns:**
- `*SessionInfo`: An object containing information about the session.
- `error`: An error if getting the session information fails.

## Related Classes

The Session class provides access to several other classes that provide specific functionality:

- [FileSystem](filesystem.md): Provides methods for file operations within a session.
- [Command](command.md): Provides methods for executing commands within a session.
- [UI](ui.md): Provides methods for interacting with the UI elements in the cloud environment.
- [Application](../concepts/applications.md): Provides methods for managing applications in the cloud environment.
- [Window](../concepts/applications.md): Provides methods for managing windows in the cloud environment.

## Usage Examples

### Python

```python
# Create a session with labels
params = CreateSessionParams()
params.labels = {
    "purpose": "demo",
    "environment": "development"
}
session = agent_bay.create(params)

# Use the session to execute a command
result = session.command.execute_command("ls -la")

# Use the session to read a file
content = session.filesystem.read_file("/etc/hosts")

# Get installed applications
apps = session.application.get_installed_apps(include_system_apps=True,
                                             include_store_apps=False,
                                             include_desktop_apps=True)

# List visible applications
processes = session.application.list_visible_apps()

# List root windows
windows = session.window.list_root_windows()

# Get active window
active_window = session.window.get_active_window()

# Get session labels
labels = session.get_labels()

# Get session info
session_info = session.info()
print(f"Session ID: {session_info['session_id']}")
print(f"Resource URL: {session_info['resource_url']}")
print(f"App ID: {session_info.get('app_id')}")
print(f"Auth Code: {session_info.get('auth_code')}")
print(f"Connection Properties: {session_info.get('connection_properties')}")
print(f"Resource ID: {session_info.get('resource_id')}")
print(f"Resource Type: {session_info.get('resource_type')}")

# Delete the session
session.delete()
```

### TypeScript

```typescript
// Create a session with labels
const session = await agentBay.create({
  labels: {
    purpose: 'demo',
    environment: 'development'
  }
});

// Use the session to execute a command
const result = await session.command.executeCommand('ls -la');

// Use the session to read a file
const content = await session.filesystem.readFile('/etc/hosts');

// Get installed applications
const apps = await session.application.getInstalledApps(true, false, true);

// List visible applications
const processes = await session.application.listVisibleApps();

// List root windows
const windows = await session.window.listRootWindows();

// Get active window
const activeWindow = await session.window.getActiveWindow();

// Get session labels
const labels = await session.getLabels();

// Get session info
const sessionInfo = await session.info();
log(`Session ID: ${sessionInfo.sessionId}`);
log(`Resource URL: ${sessionInfo.resourceUrl}`);
log(`App ID: ${sessionInfo.appId}`);
log(`Auth Code: ${sessionInfo.authCode}`);
log(`Connection Properties: ${sessionInfo.connectionProperties}`);
log(`Resource ID: ${sessionInfo.resourceId}`);
log(`Resource Type: ${sessionInfo.resourceType}`);

// Delete the session
await session.delete();
```

### Golang

```go
// Create a session with labels
params := agentbay.NewCreateSessionParams().
    WithLabels(map[string]string{
        "purpose":     "demo",
        "environment": "development",
    })
sessionResult, err := client.Create(params)
if err != nil {
    // Handle error
}
session := sessionResult.Session
fmt.Printf("Session created with ID: %s (RequestID: %s)\n", session.SessionID, sessionResult.RequestID)

// Use the session to execute a command
commandResult, err := session.Command.ExecuteCommand("ls -la")
if err != nil {
    // Handle error
}
fmt.Printf("Command output: %s (RequestID: %s)\n", commandResult.Output, commandResult.RequestID)

// Use the session to read a file
readResult, err := session.FileSystem.ReadFile("/etc/hosts")
if err != nil {
    // Handle error
}
fmt.Printf("File content: %s (RequestID: %s)\n", readResult.Content, readResult.RequestID)

// Get installed applications
appsResult, err := session.Application.GetInstalledApps(true, false, true)
if err != nil {
    // Handle error
}
fmt.Printf("Found %d installed apps (RequestID: %s)\n", len(appsResult.Apps), appsResult.RequestID)

// List visible applications
processesResult, err := session.Application.ListVisibleApps()
if err != nil {
    // Handle error
}
fmt.Printf("Found %d visible processes (RequestID: %s)\n", len(processesResult.Processes), processesResult.RequestID)

// List root windows
windowsResult, err := session.Window.ListRootWindows()
if err != nil {
    // Handle error
}
fmt.Printf("Found %d root windows (RequestID: %s)\n", len(windowsResult.Windows), windowsResult.RequestID)

// Get active window
activeWindowResult, err := session.Window.GetActiveWindow()
if err != nil {
    // Handle error
}
if activeWindowResult.Window != nil {
    fmt.Printf("Active window: %s (ID: %d, PID: %d) (RequestID: %s)\n",
        activeWindowResult.Window.Title, activeWindowResult.Window.WindowID,
        activeWindowResult.Window.PID, activeWindowResult.RequestID)
}

// Get session labels
labelsResult, err := session.GetLabels()
if err != nil {
    // Handle error
}
fmt.Printf("Session labels: %v (RequestID: %s)\n", labelsResult.Labels, labelsResult.RequestID)

// Get session info
infoResult, err := session.Info()
if err != nil {
    // Handle error
}
sessionInfo := infoResult.Info
fmt.Printf("Session ID: %s (RequestID: %s)\n", sessionInfo.SessionId, infoResult.RequestID)
fmt.Printf("Resource URL: %s\n", sessionInfo.ResourceUrl)
fmt.Printf("App ID: %s\n", sessionInfo.AppId)
fmt.Printf("Auth Code: %s\n", sessionInfo.AuthCode)
fmt.Printf("Connection Properties: %s\n", sessionInfo.ConnectionProperties)
fmt.Printf("Resource ID: %s\n", sessionInfo.ResourceId)
fmt.Printf("Resource Type: %s\n", sessionInfo.ResourceType)

// Delete the session
deleteResult, err := session.Delete()
if err != nil {
    // Handle error
}
fmt.Printf("Session deleted successfully (RequestID: %s)\n", deleteResult.RequestID)
```

## Related Resources

- [Sessions Concept](../concepts/sessions.md): Learn more about sessions in the AgentBay cloud environment.
- [AgentBay Class](agentbay.md): The main entry point for creating and managing sessions.
