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
api_key = os.getenv("AGENTBAY_API_KEY")
if not api_key:
    api_key = "akm-xxx"
    print("Warning: Using default API key.")
agent_bay = AgentBay(api_key=api_key)

# Create session (use appropriate image_id for your needs)
params = CreateSessionParams(image_id="linux_latest")  # or "windows_latest" or mobile_latest
result = agent_bay.create(params)

if result.success:
    session = result.session
    print(f"Session created: {session.session_id}")
    agent_bay.delete(session)
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
    # Don't forget to release the session
else:
    print(f"Error: {result.error_message}")
```

**Key Parameters:**
- `start_menu(bool)`: Whether to include start menu applications.
- `desktop (bool)`: Whether to include desktop applications.
- `ignore_system_apps (bool)`: Whether to ignore system applications.

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
# Method 2: Start application with optional parameters
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
# Method 3: Start application from installed apps list
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
start_result = session.application.start_app(your_start_cmd)
if start_result.success:
    print("Application started successfully!")
    print(f"Found {start_result.data}")
    target_pid = None
    for process in start_result.data:
        print(f"Process: {process.pname} (PID: {process.pid})")
        if 'chrome' in process.pname.lower():
            target_pid = process.pid
            break
    print(f"Application PID: {target_pid}")
    result = session.application.stop_app_by_pid(target_pid)

    if result.success:
        print(f"Successfully stopped process {target_pid}")
    else:
        print(f"Failed to stop process: {result.error_message}")
agent_bay.delete(session)
```

```python
# Method 2: Stop by Process Name
 start_result = session.application.start_app(your_start_cmd)
    if start_result.success:
        print("Application started successfully!")
        print(f"Found {start_result.data}")
        target_pname = None
        for process in start_result.data:
            print(f"Process: {process.pname} (PID: {process.pid})")
            target_pname = process.pname
            break
        print(f"Application target_pname: {target_pname}")

        result = session.application.stop_app_by_pname(target_pname)

        if result.success:
            print(f"Successfully stopped process {target_pname}")
        else:
            print(f"Failed to stop process: {result.error_message}")
agent_bay.delete(session)
```

```python
# Method 3: Stop by Stop Command image_id: mobile_latest
result = session.application.get_installed_apps(
start_menu=True, desktop=False, ignore_system_apps=True
)
if result.success:
    apps = result.data

    # Find specific application
    target_app = None
    for app in apps:
        target_app = app
        break
    if target_app:
        print(f"Starting {target_app.start_cmd} {target_app.stop_cmd}...")
        start_result = session.application.start_app(target_app.start_cmd)

        if start_result.success:
            print("Application started successfully!")
            stop_cmd = target_app.stop_cmd
            result = session.application.stop_app_by_cmd(stop_cmd)
            if result.success:
                print("Successfully stopped application using command")
            else:
                print(f"Failed to stop application: {result.error_message}")
        else:
            print(f"Failed to start application: {start_result.error_message}")
    else:
        print(f"Failed to find application: {result.error_message}")
    agent_bay.delete(session)
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

    # Fullscreen window (alternative to maximize)
    try:
        session.window.fullscreen_window(window_id)
        print("✓ Window set to fullscreen")
    except Exception as e:
        print(f"✗ Failed to set fullscreen: {e}")

    # Close window
    try:
        session.window.close_window(window_id)
        print("✓ Window closed")
    except Exception as e:
        print(f"✗ Failed to close: {e}")

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
    for window in windows_result.windows:
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

<a id="complete-api-reference"></a>
## 📚 Complete API Reference

### Application Manager Methods

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `get_installed_apps()` | `start_menu: bool`, `desktop: bool`, `ignore_system_apps: bool` | `InstalledAppListResult` | Get list of installed applications |
| `start_app()` | `start_cmd: str`, `work_directory: str = ""`, `activity: str = ""` | `ProcessListResult` | Start an application |
| `stop_app_by_pid()` | `pid: int` | `AppOperationResult` | Stop application by process ID |
| `stop_app_by_pname()` | `pname: str` | `AppOperationResult` | Stop application by process name |
| `stop_app_by_cmd()` | `stop_cmd: str` | `AppOperationResult` | Stop application by stop command |
| `list_visible_apps()` | None | `ProcessListResult` | List currently visible applications |

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
