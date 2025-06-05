# Applications and Windows

The Wuying AgentBay SDK provides capabilities for managing applications and windows in the cloud environment through the Application and Window interfaces.

## Application Management

The Application interface allows you to interact with applications in the cloud environment, including listing installed applications, starting applications, and stopping running processes.

### Application Properties

Applications have the following main properties:

- **Name**: The name of the application.
- **StartCmd**: The command used to start the application.
- **StopCmd**: The command used to stop the application (optional).
- **WorkDirectory**: The working directory for the application (optional).

### Process Properties

Processes have the following main properties:

- **PName**: The name of the process.
- **PID**: The process ID.
- **CmdLine**: The command line used to start the process (optional).

### Application Operations

The Application interface provides the following operations:

1. **GetInstalledApps**: Retrieves a list of installed applications.
2. **StartApp**: Starts an application with the given command and optional working directory.
3. **StopAppByPName**: Stops an application by process name.
4. **StopAppByPID**: Stops an application by process ID.
5. **StopAppByCmd**: Stops an application by stop command.
6. **ListVisibleApps**: Lists all currently visible applications.

## Window Management

The Window interface allows you to interact with windows in the cloud environment, including listing windows, getting the active window, and manipulating window states.

### Window Properties

Windows have the following main properties:

- **WindowID**: The unique identifier of the window.
- **Title**: The title of the window.
- **PName**: The name of the process that owns the window.
- **PID**: The process ID of the process that owns the window.

### Window Operations

The Window interface provides the following operations:

1. **ListRootWindows**: Lists all root windows in the system.
2. **GetActiveWindow**: Gets the currently active window.
3. **ActivateWindow**: Activates (brings to front) a window by ID.
4. **MinimizeWindow**: Minimizes a window by ID.
5. **MaximizeWindow**: Maximizes a window by ID.
6. **RestoreWindow**: Restores a window by ID (from minimized or maximized state).
7. **FullscreenWindow**: Makes a window fullscreen by ID.
8. **ResizeWindow**: Resizes a window by ID to the specified width and height.
9. **CloseWindow**: Closes a window by ID.
10. **FocusMode**: Enables or disables focus mode, which prevents window switching.

## Usage Examples

### Golang

```go
// Get installed applications
apps, err := session.Application.GetInstalledApps(true, false, true)
if err != nil {
    fmt.Printf("Error getting installed applications: %v\n", err)
    return
}
for _, app := range apps {
    fmt.Printf("Application: %s\n", app.Name)
}

// Start an application
processes, err := session.Application.StartApp("/usr/bin/google-chrome-stable", "")
if err != nil {
    fmt.Printf("Error starting application: %v\n", err)
    return
}
for _, process := range processes {
    fmt.Printf("Started process: %s (PID: %d)\n", process.PName, process.PID)
}

// List root windows
rootWindows, err := session.Window.ListRootWindows()
if err != nil {
    fmt.Printf("Error listing root windows: %v\n", err)
    return
}
for _, window := range rootWindows {
    fmt.Printf("Window: %s (ID: %d, Process: %s, PID: %d)\n", 
               window.Title, window.WindowID, window.PName, window.PID)
}

// Get active window
activeWindow, err := session.Window.GetActiveWindow()
if err != nil {
    fmt.Printf("Error getting active window: %v\n", err)
    return
}
fmt.Printf("Active window: %s (ID: %d)\n", activeWindow.Title, activeWindow.WindowID)

// Manipulate windows
windowID := rootWindows[0].WindowID
err = session.Window.MaximizeWindow(windowID)
if err != nil {
    fmt.Printf("Error maximizing window: %v\n", err)
    return
}

// Stop an application by PID
err = session.Application.StopAppByPID(processes[0].PID)
if err != nil {
    fmt.Printf("Error stopping application: %v\n", err)
    return
}
```

### Python

```python
# Get installed applications
try:
    apps = session.application.get_installed_apps(
        include_system_apps=True,
        include_store_apps=False,
        include_desktop_apps=True
    )
    for app in apps:
        print(f"Application: {app.name}")
except Exception as e:
    print(f"Error getting installed applications: {e}")

# Start an application
try:
    processes = session.application.start_app("/usr/bin/google-chrome-stable")
    for process in processes:
        print(f"Started process: {process.pname} (PID: {process.pid})")
except Exception as e:
    print(f"Error starting application: {e}")

# List root windows
try:
    root_windows = session.window.list_root_windows()
    for window in root_windows:
        print(f"Window: {window.title} (ID: {window.window_id}, Process: {window.pname}, PID: {window.pid})")
except Exception as e:
    print(f"Error listing root windows: {e}")

# Get active window
try:
    active_window = session.window.get_active_window()
    print(f"Active window: {active_window.title} (ID: {active_window.window_id})")
except Exception as e:
    print(f"Error getting active window: {e}")

# Manipulate windows
try:
    window_id = root_windows[0].window_id
    session.window.maximize_window(window_id)
except Exception as e:
    print(f"Error maximizing window: {e}")

# Stop an application by PID
try:
    session.application.stop_app_by_pid(processes[0].pid)
except Exception as e:
    print(f"Error stopping application: {e}")
```

### TypeScript

```typescript
// Get installed applications
try {
  const apps = await session.application.getInstalledApps(true, false, true);
  for (const app of apps) {
    console.log(`Application: ${app.name}`);
  }
} catch (error) {
  console.error(`Error getting installed applications: ${error}`);
}

// Start an application
try {
  const processes = await session.application.startApp('/usr/bin/google-chrome-stable');
  for (const process of processes) {
    console.log(`Started process: ${process.pname} (PID: ${process.pid})`);
  }
} catch (error) {
  console.error(`Error starting application: ${error}`);
}

// List root windows
try {
  const rootWindows = await session.window.listRootWindows();
  for (const window of rootWindows) {
    console.log(`Window: ${window.title} (ID: ${window.window_id}, Process: ${window.pname}, PID: ${window.pid})`);
  }
} catch (error) {
  console.error(`Error listing root windows: ${error}`);
}

// Get active window
try {
  const activeWindow = await session.window.getActiveWindow();
  console.log(`Active window: ${activeWindow.title} (ID: ${activeWindow.window_id})`);
} catch (error) {
  console.error(`Error getting active window: ${error}`);
}

// Manipulate windows
try {
  const windowId = rootWindows[0].window_id;
  await session.window.maximizeWindow(windowId);
} catch (error) {
  console.error(`Error maximizing window: ${error}`);
}

// Stop an application by PID
try {
  await session.application.stopAppByPid(processes[0].pid);
} catch (error) {
  console.error(`Error stopping application: ${error}`);
}
```

## Common Use Cases

1. **Application Automation**: Automate application workflows by starting applications, interacting with their windows, and stopping them when done.
2. **Window Management**: Manage window layouts, focus, and visibility for better user experience.
3. **Process Monitoring**: Monitor running processes and their associated windows.
4. **Focus Mode**: Enable focus mode to prevent window switching during important tasks.

## Related Resources

- [Sessions](sessions.md)
- [Contexts](contexts.md)
- [Application Window Example](../../golang/examples/application_window/README.md)
