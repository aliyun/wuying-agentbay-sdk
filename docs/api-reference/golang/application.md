# Application Class

The Application class provides methods for managing applications in the AgentBay cloud environment, including listing installed applications, starting applications, and stopping running processes.

## Class Properties

###

```python
class Application:
    def __init__(self, session):
        self.session = session
```

## Data Types


Represents an installed application.


```go
type InstalledApp struct {
    Name          string `json:"name"`
    StartCmd      string `json:"start_cmd"`
    StopCmd       string `json:"stop_cmd,omitempty"`
    WorkDirectory string `json:"work_directory,omitempty"`
}
```


Represents a running process.


```go
type Process struct {
    PName   string `json:"pname"`
    PID     int    `json:"pid"`
    CmdLine string `json:"cmdline,omitempty"`
}
```

## Methods


Retrieves a list of installed applications.


```go
func (am *ApplicationManager) GetInstalledApps(includeSystemApps bool, includeStoreApps bool, includeDesktopApps bool) (*InstalledAppsResult, error)
```

**Parameters:**
- `includeSystemApps` (bool): Whether to include system applications.
- `includeStoreApps` (bool): Whether to include store applications.
- `includeDesktopApps` (bool): Whether to include desktop applications.

**Returns:**
- `*InstalledAppsResult`: A result object containing the list of installed applications and RequestID.
- `error`: An error if the operation fails.

**InstalledAppsResult Structure:**
```go
type InstalledAppsResult struct {
    RequestID string         // Unique request identifier for debugging
    Apps      []*InstalledApp // Array of installed applications
}

type InstalledApp struct {
    Name        string // Application name
    Path        string // Application path
    Version     string // Application version
    Description string // Application description
}
```


Starts an application with the given command and optional working directory.


```go
func (am *ApplicationManager) StartApp(startCmd string, workDirectory string) (string, error)
```

**Parameters:**
- `startCmd` (string): The command used to start the application.
- `workDirectory` (string): The working directory for the application.

**Returns:**
- `string`: A JSON string containing the list of processes started.
- `error`: An error if the operation fails.


Stops an application by process name.


```go
func (am *ApplicationManager) StopAppByPName(pname string) (string, error)
```

**Parameters:**
- `pname` (string): The name of the process to stop.

**Returns:**
- `string`: A success message if the operation was successful.
- `error`: An error if the operation fails.


Stops an application by process ID.


```go
func (am *ApplicationManager) StopAppByPID(pid int) (string, error)
```

**Parameters:**
- `pid` (int): The process ID to stop.

**Returns:**
- `string`: A success message if the operation was successful.
- `error`: An error if the operation fails.


Stops an application by stop command.


```go
func (am *ApplicationManager) StopAppByCmd(stopCmd string) (string, error)
```

**Parameters:**
- `stopCmd` (string): The command used to stop the application.

**Returns:**
- `string`: A success message if the operation was successful.
- `error`: An error if the operation fails.


Lists all currently visible applications.


```go
func (am *ApplicationManager) ListVisibleApps() (*VisibleAppsResult, error)
```

**Returns:**
- `*VisibleAppsResult`: A result object containing the list of visible processes and RequestID.
- `error`: An error if the operation fails.

**VisibleAppsResult Structure:**
```go
type VisibleAppsResult struct {
    RequestID string     // Unique request identifier for debugging
    Processes []*Process // Array of visible processes
}

type Process struct {
    PName string // Process name
    PID   int    // Process ID
}
```

## Usage Examples

###

```python
# Create a session
session = agent_bay.create()

# Get installed applications
apps = session.application.get_installed_apps(
    include_system_apps=True,
    include_store_apps=False,
    include_desktop_apps=True
)
for app in apps:
    print(f"Application: {app.name}")

# Start an application
processes = session.application.start_app("/usr/bin/google-chrome-stable")
for process in processes:
    print(f"Started process: {process.pname} (PID: {process.pid})")

# List visible applications
visible_apps = session.application.list_visible_apps()
for app in visible_apps:
    print(f"Visible application: {app.pname} (PID: {app.pid})")

# Stop an application by PID
success = session.application.stop_app_by_pid(processes[0].pid)
print(f"Application stopped: {success}")
```

## Related Resources

- [Session Class](session.md): The session class that provides access to the Application class.
- [Window Class](window.md): The window class for managing windows in the cloud environment.
- [Applications Concept](../concepts/applications.md): Conceptual information about applications in the AgentBay cloud environment. 