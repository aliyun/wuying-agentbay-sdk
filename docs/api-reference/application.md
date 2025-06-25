# Application Class

The Application class provides methods for managing applications in the AgentBay cloud environment, including listing installed applications, starting applications, and stopping running processes.

## Class Properties

### Python

```python
class Application:
    def __init__(self, session):
        self.session = session
```

### TypeScript

```typescript
class Application {
    private session: Session;

    constructor(session: Session) {
        this.session = session;
    }
}
```

### Golang

```go
type ApplicationManager struct {
    Session interface {
        GetAPIKey() string
        GetClient() *mcp.Client
        GetSessionId() string
    }
}
```

## Data Types

### InstalledApp

Represents an installed application.

#### Python

```python
class InstalledApp:
    name: str          # The name of the application
    start_cmd: str     # The command used to start the application
    stop_cmd: str      # The command used to stop the application (optional)
    work_directory: str # The working directory for the application (optional)
```

#### TypeScript

```typescript
interface InstalledApp {
    name: string;       // The name of the application
    start_cmd: string;  // The command used to start the application
    stop_cmd?: string;  // The command used to stop the application (optional)
    work_directory?: string; // The working directory for the application (optional)
}
```

#### Golang

```go
type InstalledApp struct {
    Name          string `json:"name"`
    StartCmd      string `json:"start_cmd"`
    StopCmd       string `json:"stop_cmd,omitempty"`
    WorkDirectory string `json:"work_directory,omitempty"`
}
```

### Process

Represents a running process.

#### Python

```python
class Process:
    pname: str    # The name of the process
    pid: int      # The process ID
    cmdline: str  # The command line used to start the process (optional)
```

#### TypeScript

```typescript
interface Process {
    pname: string;   // The name of the process
    pid: number;     // The process ID
    cmdline?: string; // The command line used to start the process (optional)
}
```

#### Golang

```go
type Process struct {
    PName   string `json:"pname"`
    PID     int    `json:"pid"`
    CmdLine string `json:"cmdline,omitempty"`
}
```

## Methods

### get_installed_apps / getInstalledApps / GetInstalledApps

Retrieves a list of installed applications.

#### Python

```python
def get_installed_apps(self, include_system_apps: bool = True, include_store_apps: bool = False, include_desktop_apps: bool = True) -> List[InstalledApp]:
```

**Parameters:**
- `include_system_apps` (bool, optional): Whether to include system applications. Default is True.
- `include_store_apps` (bool, optional): Whether to include store applications. Default is False.
- `include_desktop_apps` (bool, optional): Whether to include desktop applications. Default is True.

**Returns:**
- `List[InstalledApp]`: A list of installed applications.

**Raises:**
- `ApplicationError`: If there's an error retrieving the installed applications.

#### TypeScript

```typescript
async getInstalledApps(includeSystemApps: boolean = true, includeStoreApps: boolean = false, includeDesktopApps: boolean = true): Promise<InstalledApp[]>
```

**Parameters:**
- `includeSystemApps` (boolean, optional): Whether to include system applications. Default is true.
- `includeStoreApps` (boolean, optional): Whether to include store applications. Default is false.
- `includeDesktopApps` (boolean, optional): Whether to include desktop applications. Default is true.

**Returns:**
- `Promise<InstalledApp[]>`: A promise that resolves to a list of installed applications.

**Throws:**
- `APIError`: If there's an error retrieving the installed applications.

#### Golang

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

### start_app / startApp / StartApp

Starts an application with the given command and optional working directory.

#### Python

```python
def start_app(self, start_cmd: str, work_directory: str = "") -> List[Process]:
```

**Parameters:**
- `start_cmd` (str): The command used to start the application.
- `work_directory` (str, optional): The working directory for the application. Default is an empty string.

**Returns:**
- `List[Process]`: A list of processes started.

**Raises:**
- `ApplicationError`: If there's an error starting the application.

#### TypeScript

```typescript
async startApp(startCmd: string, workDirectory: string = ""): Promise<Process[]>
```

**Parameters:**
- `startCmd` (string): The command used to start the application.
- `workDirectory` (string, optional): The working directory for the application. Default is an empty string.

**Returns:**
- `Promise<Process[]>`: A promise that resolves to a list of processes started.

**Throws:**
- `APIError`: If there's an error starting the application.

#### Golang

```go
func (am *ApplicationManager) StartApp(startCmd string, workDirectory string) (string, error)
```

**Parameters:**
- `startCmd` (string): The command used to start the application.
- `workDirectory` (string): The working directory for the application.

**Returns:**
- `string`: A JSON string containing the list of processes started.
- `error`: An error if the operation fails.

### stop_app_by_pname / stopAppByPName / StopAppByPName

Stops an application by process name.

#### Python

```python
def stop_app_by_pname(self, pname: str) -> bool:
```

**Parameters:**
- `pname` (str): The name of the process to stop.

**Returns:**
- `bool`: True if the operation was successful, False otherwise.

**Raises:**
- `ApplicationError`: If there's an error stopping the application.

#### TypeScript

```typescript
async stopAppByPName(pname: string): Promise<boolean>
```

**Parameters:**
- `pname` (string): The name of the process to stop.

**Returns:**
- `Promise<boolean>`: A promise that resolves to true if the operation was successful, false otherwise.

**Throws:**
- `APIError`: If there's an error stopping the application.

#### Golang

```go
func (am *ApplicationManager) StopAppByPName(pname string) (string, error)
```

**Parameters:**
- `pname` (string): The name of the process to stop.

**Returns:**
- `string`: A success message if the operation was successful.
- `error`: An error if the operation fails.

### stop_app_by_pid / stopAppByPid / StopAppByPID

Stops an application by process ID.

#### Python

```python
def stop_app_by_pid(self, pid: int) -> bool:
```

**Parameters:**
- `pid` (int): The process ID to stop.

**Returns:**
- `bool`: True if the operation was successful, False otherwise.

**Raises:**
- `ApplicationError`: If there's an error stopping the application.

#### TypeScript

```typescript
async stopAppByPid(pid: number): Promise<boolean>
```

**Parameters:**
- `pid` (number): The process ID to stop.

**Returns:**
- `Promise<boolean>`: A promise that resolves to true if the operation was successful, false otherwise.

**Throws:**
- `APIError`: If there's an error stopping the application.

#### Golang

```go
func (am *ApplicationManager) StopAppByPID(pid int) (string, error)
```

**Parameters:**
- `pid` (int): The process ID to stop.

**Returns:**
- `string`: A success message if the operation was successful.
- `error`: An error if the operation fails.

### stop_app_by_cmd / stopAppByCmd / StopAppByCmd

Stops an application by stop command.

#### Python

```python
def stop_app_by_cmd(self, stop_cmd: str) -> bool:
```

**Parameters:**
- `stop_cmd` (str): The command used to stop the application.

**Returns:**
- `bool`: True if the operation was successful, False otherwise.

**Raises:**
- `ApplicationError`: If there's an error stopping the application.

#### TypeScript

```typescript
async stopAppByCmd(stopCmd: string): Promise<boolean>
```

**Parameters:**
- `stopCmd` (string): The command used to stop the application.

**Returns:**
- `Promise<boolean>`: A promise that resolves to true if the operation was successful, false otherwise.

**Throws:**
- `APIError`: If there's an error stopping the application.

#### Golang

```go
func (am *ApplicationManager) StopAppByCmd(stopCmd string) (string, error)
```

**Parameters:**
- `stopCmd` (string): The command used to stop the application.

**Returns:**
- `string`: A success message if the operation was successful.
- `error`: An error if the operation fails.

### list_visible_apps / listVisibleApps / ListVisibleApps

Lists all currently visible applications.

#### Python

```python
def list_visible_apps(self) -> List[Process]:
```

**Returns:**
- `List[Process]`: A list of visible processes.

**Raises:**
- `ApplicationError`: If there's an error listing the visible applications.

#### TypeScript

```typescript
async listVisibleApps(): Promise<Process[]>
```

**Returns:**
- `Promise<Process[]>`: A promise that resolves to a list of visible processes.

**Throws:**
- `APIError`: If there's an error listing the visible applications.

#### Golang

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

### Python

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

### TypeScript

```typescript
// Create a session
const session = await agentBay.create();

// Get installed applications
const apps = await session.application.getInstalledApps(true, false, true);
for (const app of apps) {
  console.log(`Application: ${app.name}`);
}

// Start an application
const processes = await session.application.startApp('/usr/bin/google-chrome-stable');
for (const process of processes) {
  console.log(`Started process: ${process.pname} (PID: ${process.pid})`);
}

// List visible applications
const visibleApps = await session.application.listVisibleApps();
for (const app of visibleApps) {
  console.log(`Visible application: ${app.pname} (PID: ${app.pid})`);
}

// Stop an application by PID
const success = await session.application.stopAppByPid(processes[0].pid);
console.log(`Application stopped: ${success}`);
```

### Golang

```go
// Create a session
sessionResult, err := client.Create(nil)
if err != nil {
    // Handle error
}
session := sessionResult.Session

// Get installed applications
appsResult, err := session.Application.GetInstalledApps(true, false, true)
if err != nil {
    // Handle error
}
fmt.Printf("Found %d installed applications (RequestID: %s)\n", len(appsResult.Apps), appsResult.RequestID)
for _, app := range appsResult.Apps {
    fmt.Printf("Application: %s\n", app.Name)
}

// Start an application
processesResult, err := session.Application.StartApp("/usr/bin/google-chrome-stable", "")
if err != nil {
    // Handle error
}
fmt.Printf("Started %d processes (RequestID: %s)\n", len(processesResult.Processes), processesResult.RequestID)
for _, process := range processesResult.Processes {
    fmt.Printf("Started process: %s (PID: %d)\n", process.PName, process.PID)
}

// List visible applications
visibleAppsResult, err := session.Application.ListVisibleApps()
if err != nil {
    // Handle error
}
fmt.Printf("Found %d visible applications (RequestID: %s)\n", len(visibleAppsResult.Processes), visibleAppsResult.RequestID)
for _, app := range visibleAppsResult.Processes {
    fmt.Printf("Visible application: %s (PID: %d)\n", app.PName, app.PID)
}

// Stop an application by PID
stopResult, err := session.Application.StopAppByPID(processesResult.Processes[0].PID)
if err != nil {
    // Handle error
}
fmt.Printf("Application stopped successfully (RequestID: %s)\n", stopResult.RequestID)
```

## Related Resources

- [Session Class](session.md): The session class that provides access to the Application class.
- [Window Class](window.md): The window class for managing windows in the cloud environment.
- [Applications Concept](../concepts/applications.md): Conceptual information about applications in the AgentBay cloud environment. 