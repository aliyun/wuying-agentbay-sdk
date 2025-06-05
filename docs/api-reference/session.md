# Session Class API Reference

The `Session` class represents a session in the AgentBay cloud environment. A session is a container for executing commands and manipulating files. Each session has its own isolated environment.

## Properties

### Python

- `session_id`: The ID of the session.
- `filesystem`: The FileSystem instance for this session.
- `command`: The Command instance for this session.
- `adb`: The Adb instance for this session.
- `application`: The Application instance for this session.
- `window`: The Window instance for this session.

### TypeScript

- `sessionId`: The ID of the session.
- `filesystem`: The FileSystem instance for this session.
- `command`: The Command instance for this session.
- `adb`: The Adb instance for this session.
- `application`: The Application instance for this session.
- `window`: The Window instance for this session.

### Golang

- `SessionID`: The ID of the session.
- `FileSystem`: The FileSystem instance for this session.
- `Command`: The Command instance for this session.
- `Adb`: The Adb instance for this session.
- `Application`: The Application instance for this session.
- `Window`: The Window instance for this session.

## Methods

### delete / Delete

Deletes the session.

#### Python

```python
delete() -> bool
```

**Returns:**
- `bool`: True if the session was deleted successfully, False otherwise.

**Raises:**
- `AgentBayError`: If the session deletion fails.

#### TypeScript

```typescript
delete(): Promise<boolean>
```

**Returns:**
- `Promise<boolean>`: A promise that resolves to true if the session was deleted successfully, false otherwise.

**Throws:**
- `Error`: If the session deletion fails.

#### Golang

```go
Delete() error
```

**Returns:**
- `error`: An error if the session deletion fails.

### set_labels / setLabels / SetLabels

Sets labels for the session. Labels are key-value pairs that can be used to categorize and filter sessions.

#### Python

```python
set_labels(labels: Dict[str, str]) -> None
```

**Parameters:**
- `labels` (Dict[str, str]): A dictionary of labels to set for the session.

**Raises:**
- `AgentBayError`: If setting the labels fails.

#### TypeScript

```typescript
setLabels(labels: Record<string, string>): Promise<void>
```

**Parameters:**
- `labels` (Record<string, string>): An object of labels to set for the session.

**Throws:**
- `Error`: If setting the labels fails.

#### Golang

```go
SetLabels(labelsJSON string) error
```

**Parameters:**
- `labelsJSON` (string): A JSON string of labels to set for the session.

**Returns:**
- `error`: An error if setting the labels fails.

### get_labels / getLabels / GetLabels

Gets the labels for the session.

#### Python

```python
get_labels() -> Dict[str, str]
```

**Returns:**
- `Dict[str, str]`: A dictionary of labels for the session.

**Raises:**
- `AgentBayError`: If getting the labels fails.

#### TypeScript

```typescript
getLabels(): Promise<Record<string, string>>
```

**Returns:**
- `Promise<Record<string, string>>`: A promise that resolves to an object of labels for the session.

**Throws:**
- `Error`: If getting the labels fails.

#### Golang

```go
GetLabels() (string, error)
```

**Returns:**
- `string`: A JSON string of labels for the session.
- `error`: An error if getting the labels fails.

## Related Classes

The Session class provides access to several other classes that provide specific functionality:

- [FileSystem](filesystem.md): Provides methods for reading files within a session.
- [Command](command.md): Provides methods for executing commands within a session.
- [Adb](adb.md): Provides methods for executing ADB shell commands within a mobile environment (Android).
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
session, err := client.Create(params)
if err != nil {
    // Handle error
}

// Use the session to execute a command
result, err := session.Command.ExecuteCommand("ls -la")
if err != nil {
    // Handle error
}

// Use the session to read a file
content, err := session.FileSystem.ReadFile("/etc/hosts")
if err != nil {
    // Handle error
}

// Get installed applications
apps, err := session.Application.GetInstalledApps(true, false, true)
if err != nil {
    // Handle error
}

// List visible applications
processes, err := session.Application.ListVisibleApps()
if err != nil {
    // Handle error
}

// List root windows
windows, err := session.Window.ListRootWindows()
if err != nil {
    // Handle error
}

// Get active window
activeWindow, err := session.Window.GetActiveWindow()
if err != nil {
    // Handle error
}

// Get session labels
labels, err := session.GetLabels()
if err != nil {
    // Handle error
}

// Delete the session
err = client.Delete(session)
if err != nil {
    // Handle error
}
```

## Related Resources

- [Sessions Concept](../concepts/sessions.md): Learn more about sessions in the AgentBay cloud environment.
- [AgentBay Class](agentbay.md): The main entry point for creating and managing sessions.
