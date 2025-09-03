# Application and Window Operations Guide

This comprehensive guide covers application management and window operations using the AgentBay SDK. Learn how to control applications, manage windows, and automate desktop interactions in cloud environments.

## 📋 Table of Contents

- [Overview](#overview)
- [Application Management](#application-management)
  - [Getting Installed Applications](#getting-installed-applications)
  - [Starting Applications](#starting-applications)
  - [Stopping Applications](#stopping-applications)
  - [Listing Running Applications](#listing-running-applications)
- [Window Operations](#window-operations)
  - [Listing Windows](#listing-windows)
  - [Window Control](#window-control)
  - [Focus Management](#focus-management)
  - [Getting Active Window](#getting-active-window)
- [Complete Workflow Examples](#complete-workflow-examples)
- [Complete API Reference](#complete-api-reference)

<a id="overview"></a>
## 🎯 Overview

AgentBay SDK provides powerful capabilities for application and window management in cloud environments:

1. **Application Management** - Discover, start, and stop applications
2. **Window Operations** - Control window states, positions, and focus
3. **Process Management** - Monitor and manage running processes
4. **Desktop Automation** - Automate complex desktop workflows

These features enable you to build sophisticated desktop automation solutions that can interact with any application in the cloud environment.

<a id="application-management"></a>
## 🚀 Application Management

### Prerequisites

First, create a session with the appropriate environment:

```python
from agentbay import AgentBay
from agentbay.session_params import CreateSessionParams

# Initialize AgentBay
api_key = "your-api-key"
agent_bay = AgentBay(api_key=api_key)

# Create session (use appropriate image_id for your needs)
params = CreateSessionParams(image_id="linux_latest")  # or "windows_latest"
result = agent_bay.create(params)

if result.success:
    session = result.session
    print(f"Session created: {session.session_id}")
else:
    print(f"Failed to create session: {result.error_message}")
```

<a id="getting-installed-applications"></a>
### Getting Installed Applications

Discover all applications available in the system:

```python
# Get installed applications
result = session.application.get_installed_apps(
    start_menu=True,      # Include start menu applications
    desktop=False,        # Exclude desktop shortcuts
    ignore_system_apps=True  # Filter out system applications
)

if result.success:
    apps = result.data
    print(f"Found {len(apps)} installed applications")
    
    # Display application details
    for app in apps[:5]:  # Show first 5 apps
        print(f"Name: {app.name}")
        print(f"Start Command: {app.start_cmd}")
        print(f"Stop Command: {app.stop_cmd if app.stop_cmd else 'N/A'}")
        print(f"Work Directory: {app.work_directory if app.work_directory else 'N/A'}")
        print("---")
else:
    print(f"Error: {result.error_message}")
```

**Key Parameters:**
- `start_menu`: Include applications from start menu/applications folder
- `desktop`: Include desktop shortcuts
- `ignore_system_apps`: Filter out system-level applications

<a id="starting-applications"></a>
### Starting Applications

Launch applications using their start commands:

```python
# Method 1: Start application by command
start_cmd = "/usr/bin/google-chrome-stable"  # Linux example
# start_cmd = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"  # Windows example

result = session.application.start_app(start_cmd)

if result.success:
    processes = result.data
    print(f"Application started successfully with {len(processes)} processes")
    
    for process in processes:
        print(f"Process: {process.pname} (PID: {process.pid})")
else:
    print(f"Failed to start application: {result.error_message}")
```

```python
# Method 1b: Start application with optional parameters
start_cmd = "/usr/bin/google-chrome-stable"
work_directory = "/tmp"  # Optional working directory (use existing directory)
activity = ""  # Optional activity (mainly for mobile apps)

result = session.application.start_app(
    start_cmd=start_cmd,
    work_directory=work_directory,
    activity=activity
)

if result.success:
    processes = result.data
    print(f"Application started with {len(processes)} processes")
else:
    print(f"Failed to start application: {result.error_message}")
```

```python
# Method 2: Start application from installed apps list
result = session.application.get_installed_apps(
    start_menu=True, desktop=False, ignore_system_apps=True
)

if result.success:
    apps = result.data
    
    # Find specific application
    target_app = None
    for app in apps:
        if "chrome" in app.name.lower():
            target_app = app
            break
    
    if target_app:
        print(f"Starting {target_app.name}...")
        start_result = session.application.start_app(target_app.start_cmd)
        
        if start_result.success:
            print("Application started successfully!")
        else:
            print(f"Failed to start: {start_result.error_message}")
    else:
        print("Target application not found")
```

<a id="stopping-applications"></a>
### Stopping Applications

Stop applications using process ID or process name:

```python
# Method 1: Stop by Process ID (PID)
pid = 1234  # Replace with actual PID
result = session.application.stop_app_by_pid(pid)

if result.success:
    print(f"Successfully stopped process {pid}")
else:
    print(f"Failed to stop process: {result.error_message}")
```

```python
# Method 2: Stop by Process Name
process_name = "chrome"
result = session.application.stop_app_by_pname(process_name)

if result.success:
    print(f"Successfully stopped {process_name}")
else:
    print(f"Failed to stop {process_name}: {result.error_message}")
```

```python
# Method 3: Stop by Stop Command
stop_cmd = "pkill chrome"  # Linux example
# stop_cmd = "taskkill /f /im chrome.exe"  # Windows example

result = session.application.stop_app_by_cmd(stop_cmd)

if result.success:
    print("Successfully stopped application using command")
else:
    print(f"Failed to stop application: {result.error_message}")
```

```python
# Method 3: Complete start-stop workflow
def start_and_stop_application(session, app_command, process_name):
    """Complete workflow to start and stop an application"""
    
    # Start application
    print(f"Starting application: {app_command}")
    start_result = session.application.start_app(app_command)
    
    if not start_result.success:
        print(f"Failed to start: {start_result.error_message}")
        return False
    
    processes = start_result.data
    print(f"Started {len(processes)} processes")
    
    # Wait for application to fully load
    import time
    time.sleep(3)
    
    # Stop application
    print(f"Stopping application: {process_name}")
    stop_result = session.application.stop_app_by_pname(process_name)
    
    if stop_result.success:
        print("Application stopped successfully")
        return True
    else:
        print(f"Failed to stop: {stop_result.error_message}")
        return False

# Usage
success = start_and_stop_application(
    session, 
    "/usr/bin/google-chrome-stable", 
    "chrome"
)
```

<a id="listing-running-applications"></a>
### Listing Running Applications

Monitor currently running applications:

```python
# Get all visible applications
result = session.application.list_visible_apps()

if result.success:
    visible_apps = result.data
    print(f"Found {len(visible_apps)} running applications")
    
    for app in visible_apps:
        print(f"Process: {app.pname}")
        print(f"PID: {app.pid}")
        print(f"Command: {app.cmdline}")
        print("---")
else:
    print(f"Error: {result.error_message}")
```

**Process Object Properties:**

The `Process` objects in the returned list contain the following attributes:
- `pname` (str): Process name (may be truncated for long names)
- `pid` (int): Process ID
- `cmdline` (str): Full command line used to start the process

<a id="window-operations"></a>
## 🪟 Window Operations

<a id="listing-windows"></a>
### Listing Windows

Get information about all available windows:

```python
# List all root windows (with optional timeout)
result = session.window.list_root_windows(timeout_ms=5000)  # 5 second timeout

if result.success:
    windows = result.windows  # Note: use .windows, not .data
    print(f"Found {len(windows)} windows")
    
    for window in windows:
        print(f"Title: {window.title}")
        print(f"Window ID: {window.window_id}")
        print(f"Process: {window.pname if window.pname else 'N/A'}")
        print(f"PID: {window.pid if window.pid else 'N/A'}")
        print(f"Position: ({window.absolute_upper_left_x}, {window.absolute_upper_left_y})")
        print(f"Size: {window.width}x{window.height}")
        print(f"Child Windows: {len(window.child_windows)}")
        print("---")
else:
    print(f"Error listing windows: {result.error_message}")
```

**Window Object Properties:**

The `Window` object contains the following attributes:
- `window_id` (int): Unique identifier for the window
- `title` (str): Window title/caption
- `absolute_upper_left_x` (Optional[int]): X-coordinate of window's upper-left corner
- `absolute_upper_left_y` (Optional[int]): Y-coordinate of window's upper-left corner  
- `width` (Optional[int]): Window width in pixels
- `height` (Optional[int]): Window height in pixels
- `pid` (Optional[int]): Process ID that owns the window
- `pname` (Optional[str]): Process name that owns the window
- `child_windows` (List[Window]): List of child windows

<a id="window-control"></a>
### Window Control

Control window states and positions:

```python
def control_window(session, window_id):
    """Demonstrate various window control operations"""
    
    print(f"Controlling window ID: {window_id}")
    
    # Activate window
    try:
        session.window.activate_window(window_id)
        print("✓ Window activated")
    except Exception as e:
        print(f"✗ Failed to activate: {e}")
    
    # Maximize window
    try:
        session.window.maximize_window(window_id)
        print("✓ Window maximized")
    except Exception as e:
        print(f"✗ Failed to maximize: {e}")
    
    # Wait a moment
    import time
    time.sleep(1)
    
    # Minimize window
    try:
        session.window.minimize_window(window_id)
        print("✓ Window minimized")
    except Exception as e:
        print(f"✗ Failed to minimize: {e}")
    
    time.sleep(1)
    
    # Restore window
    try:
        session.window.restore_window(window_id)
        print("✓ Window restored")
    except Exception as e:
        print(f"✗ Failed to restore: {e}")
    
    # Resize window
    try:
        session.window.resize_window(window_id, 800, 600)
        print("✓ Window resized to 800x600")
    except Exception as e:
        print(f"✗ Failed to resize: {e}")
    
    # Close window
    try:
        session.window.close_window(window_id)
        print("✓ Window closed")
    except Exception as e:
        print(f"✗ Failed to close: {e}")
    
    # Fullscreen window (alternative to maximize)
    try:
        session.window.fullscreen_window(window_id)
        print("✓ Window set to fullscreen")
    except Exception as e:
        print(f"✗ Failed to set fullscreen: {e}")

# Usage
windows = session.window.list_root_windows()
if windows.success and windows.windows:  # Note: use .windows, not .data
    control_window(session, windows.windows[0].window_id)
```

<a id="focus-management"></a>
### Focus Management

Control system focus behavior:

```python
# Enable focus mode (prevents focus stealing)
try:
    session.window.focus_mode(True)
    print("Focus mode enabled - windows won't steal focus")
except Exception as e:
    print(f"Failed to enable focus mode: {e}")

# Perform operations while focus mode is active
# ... your window operations here ...

# Disable focus mode
try:
    session.window.focus_mode(False)
    print("Focus mode disabled")
except Exception as e:
    print(f"Failed to disable focus mode: {e}")
```

<a id="getting-active-window"></a>
### Getting Active Window

Get information about the currently active window:

```python
# Get the currently active window (with optional timeout)
result = session.window.get_active_window(timeout_ms=5000)  # 5 second timeout

if result.success:
    active_window = result.window  # Note: use .window, not .data
    print(f"Active Window:")
    print(f"  Title: {active_window.title}")
    print(f"  Window ID: {active_window.window_id}")
    print(f"  Process: {active_window.pname}")
    print(f"  PID: {active_window.pid}")
else:
    print(f"Failed to get active window: {result.error_message}")
```

<a id="complete-workflow-examples"></a>
## 🔄 Complete Workflow Examples

### Example 1: Launch Application and Control Its Window

```python
def launch_and_control_application(session, app_name="Google Chrome"):
    """Complete workflow: find app, launch it, control its window"""
    
    # Step 1: Find the application
    print("Step 1: Finding installed applications...")
    apps_result = session.application.get_installed_apps(
        start_menu=True, desktop=False, ignore_system_apps=True
    )
    
    if not apps_result.success:
        print(f"Failed to get apps: {apps_result.error_message}")
        return False
    
    # Find target application
    target_app = None
    for app in apps_result.data:
        if app_name.lower() in app.name.lower():
            target_app = app
            break
    
    if not target_app:
        print(f"Application '{app_name}' not found")
        return False
    
    print(f"Found application: {target_app.name}")
    
    # Step 2: Launch the application
    print("Step 2: Launching application...")
    start_result = session.application.start_app(target_app.start_cmd)
    
    if not start_result.success:
        print(f"Failed to start app: {start_result.error_message}")
        return False
    
    print(f"Application started with {len(start_result.data)} processes")
    
    # Step 3: Wait for application to load
    print("Step 3: Waiting for application to load...")
    import time
    time.sleep(5)
    
    # Step 4: Find and control the application window
    print("Step 4: Finding application window...")
    windows_result = session.window.list_root_windows()
    
    if not windows_result.success:
        print(f"Failed to list windows: {windows_result.error_message}")
        return False
    
    # Find window belonging to our application
    app_window = None
    for window in windows_result.data:
        if hasattr(window, 'pname') and target_app.name.lower() in window.title.lower():
            app_window = window
            break
    
    if not app_window:
        # Try to get any window if specific match fails
        if windows_result.windows:
            app_window = windows_result.windows[0]
            print("Using first available window")
    
    if app_window:
        print(f"Found window: {app_window.title}")
        
        # Control the window
        try:
            session.window.activate_window(app_window.window_id)
            print("✓ Window activated")
            
            time.sleep(1)
            session.window.maximize_window(app_window.window_id)
            print("✓ Window maximized")
            
        except Exception as e:
            print(f"Window control failed: {e}")
    
    return True

# Usage
success = launch_and_control_application(session, "Google Chrome")
if success:
    print("Workflow completed successfully!")
```

### Example 2: Monitor and Manage Running Applications

```python
def monitor_applications(session, duration_seconds=30):
    """Monitor running applications for a specified duration"""
    
    import time
    start_time = time.time()
    
    print(f"Monitoring applications for {duration_seconds} seconds...")
    
    while time.time() - start_time < duration_seconds:
        # Get current running applications
        result = session.application.list_visible_apps()
        
        if result.success:
            apps = result.data
            print(f"\n[{time.strftime('%H:%M:%S')}] Running applications: {len(apps)}")
            
            for app in apps[:5]:  # Show top 5
                print(f"  {app.pname} (PID: {app.pid})")
        
        # Check active window
        active_result = session.window.get_active_window()
        if active_result.success:
            active = active_result.data
            print(f"  Active: {active.title}")
        
        time.sleep(5)  # Check every 5 seconds

# Usage
monitor_applications(session, 30)
```

<a id="complete-api-reference"></a>
## 📚 Complete API Reference

### Application Manager Methods

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `get_installed_apps()` | `start_menu: bool`, `desktop: bool`, `ignore_system_apps: bool` | `InstalledAppListResult` | Get list of installed applications |
| `start_app()` | `start_cmd: str`, `work_directory: str = ""`, `activity: str = ""` | `ProcessListResult` | Start an application |
| `stop_app_by_pid()` | `pid: int` | `AppOperationResult` | Stop application by process ID |
| `stop_app_by_pname()` | `pname: str` | `AppOperationResult` | Stop application by process name |
| `stop_app_by_cmd()` | `stop_cmd: str` | `AppOperationResult` | Stop application by command |
| `list_visible_apps()` | None | `ProcessListResult` | List currently running applications |

### Window Manager Methods

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `list_root_windows()` | `timeout_ms: int = 3000` | `WindowListResult` | List all root windows |
| `get_active_window()` | `timeout_ms: int = 3000` | `WindowInfoResult` | Get currently active window |
| `activate_window()` | `window_id: int` | `BoolResult` | Activate a window |
| `maximize_window()` | `window_id: int` | `BoolResult` | Maximize a window |
| `minimize_window()` | `window_id: int` | `BoolResult` | Minimize a window |
| `restore_window()` | `window_id: int` | `BoolResult` | Restore a window |
| `close_window()` | `window_id: int` | `BoolResult` | Close a window |
| `fullscreen_window()` | `window_id: int` | `BoolResult` | Make window fullscreen |
| `resize_window()` | `window_id: int`, `width: int`, `height: int` | `BoolResult` | Resize a window |
| `focus_mode()` | `on: bool` | `BoolResult` | Toggle focus mode |

### Return Types

- **InstalledAppListResult**: Contains `success`, `data` (List[InstalledApp]), `error_message`, `request_id`
- **ProcessListResult**: Contains `success`, `data` (List[Process]), `error_message`, `request_id`
- **AppOperationResult**: Contains `success`, `error_message`, `request_id`
- **WindowListResult**: Contains `success`, `windows` (List[Window]), `error_message`, `request_id`
- **WindowInfoResult**: Contains `success`, `window` (Window), `error_message`, `request_id`
- **BoolResult**: Contains `success`, `data` (bool), `error_message`, `request_id`

## 🎯 Summary

This guide covered comprehensive application and window management capabilities:

- **Application Discovery**: Find and list installed applications
- **Application Lifecycle**: Start and stop applications reliably
- **Window Control**: Manage window states, positions, and focus
- **Process Management**: Monitor and control running processes

These features enable you to build sophisticated desktop automation solutions that can interact with any application in cloud environments, making AgentBay SDK a powerful tool for automated testing, workflow automation, and remote desktop management. 