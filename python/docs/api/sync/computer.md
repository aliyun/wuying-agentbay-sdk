# Computer API Reference

> **💡 Async Version**: This documentation covers the synchronous API. For async/await support, see [`AsyncComputer`](../async/async-computer.md) which provides the same functionality with async methods.

## 🖥️ Related Tutorial

- [Computer Use Guide](../../../../docs/guides/computer-use/README.md) - Automate desktop applications

## Overview

The Computer module provides comprehensive desktop automation capabilities including mouse operations,
keyboard input, screen capture, and window management. It enables automated UI testing and RPA workflows.


## Requirements

- Requires `windows_latest` image for computer use features

## Data Types

### MouseButton

Mouse button constants: Left, Right, Middle, DoubleLeft

### ScrollDirection

Scroll direction constants: Up, Down, Left, Right

### KeyModifier

Keyboard modifier keys: Ctrl, Alt, Shift, Win

## Important Notes

- Key names in PressKeys and ReleaseKeys are case-sensitive
- Coordinate validation: x and y must be non-negative integers
- Drag operation requires valid start and end coordinates
- Screenshot operations may have size limitations



Computer module for desktop UI automation.
Handles mouse operations, keyboard operations, window management,
application management, and screen operations.

## Computer

```python
class Computer(BaseService)
```

Handles computer UI automation operations in the AgentBay cloud environment.
Provides comprehensive desktop automation capabilities including mouse, keyboard,
window management, application management, and screen operations.

### \_\_init\_\_

```python
def __init__(self, session)
```

Initialize a Computer object.

**Arguments**:

    session: The session object that provides access to the AgentBay API.

### click\_mouse

```python
def click_mouse(
        x: int,
        y: int,
        button: Union[MouseButton, str] = MouseButton.LEFT) -> BoolResult
```

Clicks the mouse at the specified screen coordinates.

**Arguments**:

- `x` _int_ - X coordinate in pixels (0 is left edge of screen).
- `y` _int_ - Y coordinate in pixels (0 is top edge of screen).
- `button` _Union[MouseButton, str], optional_ - Mouse button to click. Options:
  - MouseButton.LEFT or "left": Single left click
  - MouseButton.RIGHT or "right": Right click (context menu)
  - MouseButton.MIDDLE or "middle": Middle click (scroll wheel)
  - MouseButton.DOUBLE_LEFT or "double_left": Double left click
  Defaults to MouseButton.LEFT.
  

**Returns**:

    BoolResult: Object containing:
  - success (bool): Whether the click succeeded
  - data (bool): True if successful, None otherwise
  - error_message (str): Error description if failed
  

**Raises**:

    ValueError: If button is not one of the valid options.
  
  Behavior:
  - Clicks at the exact pixel coordinates provided
  - Does not move the mouse cursor before clicking
  - For double-click, use MouseButton.DOUBLE_LEFT
  - Right-click typically opens context menus
  

**Example**:

```python
session = agent_bay.create().session
session.computer.click_mouse(100, 200)
session.computer.click_mouse(300, 400, MouseButton.RIGHT)
session.delete()
```


**Notes**:

- Coordinates are absolute screen positions, not relative to windows
- Use `get_screen_size()` to determine valid coordinate ranges
- Consider using `move_mouse()` first if you need to see cursor movement
- For UI automation, consider using higher-level methods from `ui` module


**See Also**:

move_mouse, drag_mouse, get_cursor_position, get_screen_size

### move\_mouse

```python
def move_mouse(x: int, y: int) -> BoolResult
```

Moves the mouse to the specified coordinates.

**Arguments**:

- `x` _int_ - X coordinate.
- `y` _int_ - Y coordinate.
  

**Returns**:

    BoolResult: Result object containing success status and error message if any.
  

**Example**:

```python
session = agent_bay.create().session
session.computer.move_mouse(500, 300)
position = session.computer.get_cursor_position()
print(f"Cursor at: {position.data}")
session.delete()
```


**Notes**:

- Moves the cursor smoothly to the target position
- Does not click after moving
- Use get_cursor_position() to verify the new position


**See Also**:

click_mouse, drag_mouse, get_cursor_position

### drag\_mouse

```python
def drag_mouse(
        from_x: int,
        from_y: int,
        to_x: int,
        to_y: int,
        button: Union[MouseButton, str] = MouseButton.LEFT) -> BoolResult
```

Drags the mouse from one point to another.

**Arguments**:

- `from_x` _int_ - Starting X coordinate.
- `from_y` _int_ - Starting Y coordinate.
- `to_x` _int_ - Ending X coordinate.
- `to_y` _int_ - Ending Y coordinate.
- `button` _Union[MouseButton, str], optional_ - Button type. Can be MouseButton enum or string.
  Valid values: MouseButton.LEFT, MouseButton.RIGHT, MouseButton.MIDDLE
  or their string equivalents. Defaults to MouseButton.LEFT.
    Note: DOUBLE_LEFT is not supported for drag operations.
  

**Returns**:

    BoolResult: Result object containing success status and error message if any.
  

**Raises**:

    ValueError: If button is not a valid option.
  

**Example**:

```python
session = agent_bay.create().session
session.computer.drag_mouse(100, 100, 300, 300)
session.computer.drag_mouse(200, 200, 400, 400, MouseButton.RIGHT)
session.delete()
```


**Notes**:

- Performs a click-and-drag operation from start to end coordinates
- Useful for selecting text, moving windows, or drawing
- DOUBLE_LEFT button is not supported for drag operations
- Use LEFT, RIGHT, or MIDDLE button only


**See Also**:

click_mouse, move_mouse

### scroll

```python
def scroll(x: int,
           y: int,
           direction: Union[ScrollDirection, str] = ScrollDirection.UP,
           amount: int = 1) -> BoolResult
```

Scrolls the mouse wheel at the specified coordinates.

**Arguments**:

- `x` _int_ - X coordinate.
- `y` _int_ - Y coordinate.
- `direction` _Union[ScrollDirection, str], optional_ - Scroll direction. Can be ScrollDirection enum or string.
  Valid values: ScrollDirection.UP, ScrollDirection.DOWN, ScrollDirection.LEFT, ScrollDirection.RIGHT
  or their string equivalents. Defaults to ScrollDirection.UP.
- `amount` _int, optional_ - Scroll amount. Defaults to 1.
  

**Returns**:

    BoolResult: Result object containing success status and error message if any.
  

**Raises**:

    ValueError: If direction is not a valid option.
  

**Example**:

```python
session = agent_bay.create().session
session.computer.scroll(500, 500, ScrollDirection.DOWN, 3)
session.computer.scroll(500, 500, ScrollDirection.UP, 2)
session.delete()
```


**Notes**:

- Scroll operations are performed at the specified coordinates
- The amount parameter controls how many scroll units to move
- Larger amounts result in faster scrolling
- Useful for navigating long documents or web pages


**See Also**:

click_mouse, move_mouse

### get\_cursor\_position

```python
def get_cursor_position() -> OperationResult
```

Gets the current cursor position.

**Returns**:

    OperationResult: Result object containing cursor position data
  with keys 'x' and 'y', and error message if any.
  

**Example**:

```python
session = agent_bay.create().session
session.computer.move_mouse(800, 600)
position = session.computer.get_cursor_position()
print(f"Cursor is at x={position.data['x']}, y={position.data['y']}")
session.delete()
```


**Notes**:

- Returns the absolute screen coordinates
- Useful for verifying mouse movements
- Position is in pixels from top-left corner (0, 0)


**See Also**:

move_mouse, click_mouse, get_screen_size

### input\_text

```python
def input_text(text: str) -> BoolResult
```

Types text into the currently focused input field.

**Arguments**:

- `text` _str_ - The text to input. Supports Unicode characters.
  

**Returns**:

    BoolResult: Object with success status and error message if any.
  

**Example**:

```python
session = agent_bay.create().session
session.computer.click_mouse(500, 300)
session.computer.input_text("Hello, World!")
session.delete()
```


**Notes**:

- Requires an input field to be focused first
- Use click_mouse() or UI automation to focus the field
- Supports special characters and Unicode


**See Also**:

press_keys, click_mouse

### press\_keys

```python
def press_keys(keys: List[str], hold: bool = False) -> BoolResult
```

Presses the specified keys.

**Arguments**:

- `keys` _List[str]_ - List of keys to press (e.g., ["Ctrl", "a"]).
- `hold` _bool, optional_ - Whether to hold the keys. Defaults to False.
  

**Returns**:

    BoolResult: Result object containing success status and error message if any.
  

**Example**:

```python
session = agent_bay.create().session
session.computer.press_keys(["Ctrl", "c"])
session.computer.press_keys(["Ctrl", "v"])
session.delete()
```


**Notes**:

- Key names are case-sensitive
- When hold=True, remember to call release_keys() afterwards
- Supports modifier keys like Ctrl, Alt, Shift
- Can press multiple keys simultaneously for shortcuts


**See Also**:

release_keys, input_text

### release\_keys

```python
def release_keys(keys: List[str]) -> BoolResult
```

Releases the specified keys.

**Arguments**:

- `keys` _List[str]_ - List of keys to release (e.g., ["Ctrl", "a"]).
  

**Returns**:

    BoolResult: Result object containing success status and error message if any.
  

**Example**:

```python
session = agent_bay.create().session
session.computer.press_keys(["Shift"], hold=True)
session.computer.input_text("hello")
session.computer.release_keys(["Shift"])
session.delete()
```


**Notes**:

- Should be used after press_keys() with hold=True
- Key names are case-sensitive
- Releases all keys specified in the list


**See Also**:

press_keys, input_text

### get\_screen\_size

```python
def get_screen_size() -> OperationResult
```

Gets the screen size and DPI scaling factor.

**Returns**:

    OperationResult: Result object containing screen size data
  with keys 'width', 'height', and 'dpiScalingFactor',
  and error message if any.
  

**Example**:

```python
result = agent_bay.create()
session = result.session
size = session.computer.get_screen_size()
print(
  f"Screen: {size.data['width']}x{size.data['height']}, DPI: {size.data['dpiScalingFactor']}"
)
session.delete()
```


**Notes**:

- Returns the full screen dimensions in pixels
- DPI scaling factor affects coordinate calculations on high-DPI displays
- Use this to determine valid coordinate ranges for mouse operations


**See Also**:

click_mouse, move_mouse, screenshot

### screenshot

```python
def screenshot() -> OperationResult
```

Takes a screenshot of the current screen.

**Returns**:

    OperationResult: Result object containing the path to the screenshot
  and error message if any.
  

**Example**:

```python
session = agent_bay.create().session
screenshot = session.computer.screenshot()
print(f"Screenshot URL: {screenshot.data}")
session.delete()
```


**Notes**:

- Returns an OSS URL to the screenshot image
- Screenshot captures the entire screen
- Useful for debugging and verification
- Image format is typically PNG


**See Also**:

get_screen_size

### list\_root\_windows

```python
def list_root_windows(timeout_ms: int = 3000) -> WindowListResult
```

Lists all root windows.

**Arguments**:

- `timeout_ms` _int, optional_ - Timeout in milliseconds. Defaults to 3000.
  

**Returns**:

    WindowListResult: Result object containing list of windows and error message if any.
  

**Example**:

```python
session = agent_bay.create().session
windows = session.computer.list_root_windows()
for window in windows.windows:
  print(f"Window: {window.title}, ID: {window.window_id}")
session.delete()
```

### get\_active\_window

```python
def get_active_window() -> WindowInfoResult
```

Gets the currently active window.

**Returns**:

    WindowInfoResult: Result object containing active window info and error message if any.
  

**Example**:

```python
session = agent_bay.create().session
active = session.computer.get_active_window()
print(f"Active window: {active.window.title}")
session.delete()
```

### activate\_window

```python
def activate_window(window_id: int) -> BoolResult
```

Activates the specified window.

**Arguments**:

- `window_id` _int_ - The ID of the window to activate.
  

**Returns**:

    BoolResult: Result object containing success status and error message if any.
  

**Example**:

```python
session = agent_bay.create().session
windows = session.computer.list_root_windows()
if windows.windows:
  session.computer.activate_window(windows.windows[0].window_id)
session.delete()
```


**Notes**:

- The window must exist in the system
- Use list_root_windows() to get available window IDs
- Activating a window brings it to the foreground


**See Also**:

list_root_windows, get_active_window, close_window

### close\_window

```python
def close_window(window_id: int) -> BoolResult
```

Closes the specified window.

**Arguments**:

- `window_id` _int_ - The ID of the window to close.
  

**Returns**:

    BoolResult: Result object containing success status and error message if any.
  

**Example**:

```python
session = agent_bay.create().session
windows = session.computer.list_root_windows()
if windows.windows:
  session.computer.close_window(windows.windows[0].window_id)
session.delete()
```


**Notes**:

- The window must exist in the system
- Use list_root_windows() to get available window IDs
- Closing a window terminates it permanently


**See Also**:

list_root_windows, activate_window, minimize_window

### maximize\_window

```python
def maximize_window(window_id: int) -> BoolResult
```

Maximizes the specified window.

**Arguments**:

- `window_id` _int_ - The ID of the window to maximize.
  

**Returns**:

    BoolResult: Result object containing success status and error message if any.
  

**Example**:

```python
session = agent_bay.create().session
active = session.computer.get_active_window()
if active.window:
  session.computer.maximize_window(active.window.window_id)
session.delete()
```


**Notes**:

- The window must exist in the system
- Maximizing expands the window to fill the screen
- Use restore_window() to return to previous size


**See Also**:

minimize_window, restore_window, fullscreen_window, resize_window

### minimize\_window

```python
def minimize_window(window_id: int) -> BoolResult
```

Minimizes the specified window.

**Arguments**:

- `window_id` _int_ - The ID of the window to minimize.
  

**Returns**:

    BoolResult: Result object containing success status and error message if any.
  

**Example**:

```python
session = agent_bay.create().session
active = session.computer.get_active_window()
if active.window:
  session.computer.minimize_window(active.window.window_id)
session.delete()
```


**Notes**:

- The window must exist in the system
- Minimizing hides the window in the taskbar
- Use restore_window() or activate_window() to bring it back


**See Also**:

maximize_window, restore_window, activate_window

### restore\_window

```python
def restore_window(window_id: int) -> BoolResult
```

Restores the specified window.

**Arguments**:

- `window_id` _int_ - The ID of the window to restore.
  

**Returns**:

    BoolResult: Result object containing success status and error message if any.
  

**Example**:

```python
session = agent_bay.create().session
active = session.computer.get_active_window()
if active.window:
  wid = active.window.window_id
  session.computer.minimize_window(wid)
  session.computer.restore_window(wid)
session.delete()
```


**Notes**:

- The window must exist in the system
- Restoring returns a minimized or maximized window to its normal state
- Works for windows that were previously minimized or maximized


**See Also**:

minimize_window, maximize_window, activate_window

### resize\_window

```python
def resize_window(window_id: int, width: int, height: int) -> BoolResult
```

Resizes the specified window.

**Arguments**:

- `window_id` _int_ - The ID of the window to resize.
- `width` _int_ - New width of the window.
- `height` _int_ - New height of the window.
  

**Returns**:

    BoolResult: Result object containing success status and error message if any.
  

**Example**:

```python
session = agent_bay.create().session
active = session.computer.get_active_window()
if active.window:
  session.computer.resize_window(active.window.window_id, 800, 600)
session.delete()
```


**Notes**:

- The window must exist in the system
- Width and height are in pixels
- Some windows may have minimum or maximum size constraints


**See Also**:

maximize_window, restore_window, get_screen_size

### fullscreen\_window

```python
def fullscreen_window(window_id: int) -> BoolResult
```

Makes the specified window fullscreen.

**Arguments**:

- `window_id` _int_ - The ID of the window to make fullscreen.
  

**Returns**:

    BoolResult: Result object containing success status and error message if any.
  

**Example**:

```python
session = agent_bay.create().session
active = session.computer.get_active_window()
if active.window:
  session.computer.fullscreen_window(active.window.window_id)
session.delete()
```


**Notes**:

- The window must exist in the system
- Fullscreen mode hides window borders and taskbar
- Different from maximize_window() which keeps window borders
- Press F11 or ESC to exit fullscreen in most applications


**See Also**:

maximize_window, restore_window

### focus\_mode

```python
def focus_mode(on: bool) -> BoolResult
```

Toggles focus mode on or off.

**Arguments**:

- `on` _bool_ - True to enable focus mode, False to disable it.
  

**Returns**:

    BoolResult: Result object containing success status and error message if any.
  

**Example**:

```python
session = agent_bay.create().session
session.computer.focus_mode(True)
session.computer.focus_mode(False)
session.delete()
```


**Notes**:

- Focus mode helps reduce distractions by managing window focus
- When enabled, may prevent background windows from stealing focus
- Behavior depends on the window manager and OS settings


**See Also**:

activate_window, get_active_window

### get\_installed\_apps

```python
def get_installed_apps(
        start_menu: bool = True,
        desktop: bool = False,
        ignore_system_apps: bool = True) -> InstalledAppListResult
```

Gets the list of installed applications.

**Arguments**:

- `start_menu` _bool, optional_ - Whether to include start menu applications. Defaults to True.
- `desktop` _bool, optional_ - Whether to include desktop applications. Defaults to False.
- `ignore_system_apps` _bool, optional_ - Whether to ignore system applications. Defaults to True.
  

**Returns**:

    InstalledAppListResult: Result object containing list of installed apps and error message if any.
  

**Example**:

```python
session = agent_bay.create().session
apps = session.computer.get_installed_apps()
for app in apps.data:
  print(f"{app.name}: {app.start_cmd}")
session.delete()
```


**Notes**:

- start_menu parameter includes applications from Windows Start Menu
- desktop parameter includes shortcuts from Desktop
- ignore_system_apps parameter filters out system applications
- Each app object contains name, start_cmd, stop_cmd, and work_directory


**See Also**:

start_app, list_visible_apps, stop_app_by_pname

### start\_app

```python
def start_app(start_cmd: str,
              work_directory: str = "",
              activity: str = "") -> ProcessListResult
```

Starts the specified application.

**Arguments**:

- `start_cmd` _str_ - The command to start the application.
- `work_directory` _str, optional_ - Working directory for the application. Defaults to "".
- `activity` _str, optional_ - Activity name to launch (for mobile apps). Defaults to "".
  

**Returns**:

    ProcessListResult: Result object containing list of processes started and error message if any.
  

**Example**:

```python
session = agent_bay.create().session
processes = session.computer.start_app("notepad.exe")
print(f"Started {len(processes.data)} process(es)")
session.delete()
```


**Notes**:

- The start_cmd can be an executable name or full path
- work_directory is optional and defaults to the system default
- activity parameter is for mobile apps (Android)
- Returns process information for all started processes


**See Also**:

get_installed_apps, stop_app_by_pname, list_visible_apps

### list\_visible\_apps

```python
def list_visible_apps() -> ProcessListResult
```

Lists all applications with visible windows.

Returns detailed process information for applications that have visible windows,
including process ID, name, command line, and other system information.
This is useful for system monitoring and process management tasks.

**Returns**:

    ProcessListResult: Result object containing list of visible applications
  with detailed process information.
  

**Example**:

```python
session = agent_bay.create().session
apps = session.computer.list_visible_apps()
for app in apps.data:
  print(f"App: {app.pname}, PID: {app.pid}")
session.delete()
```


**Notes**:

- Only returns applications with visible windows
- Hidden or minimized windows may not appear
- Useful for monitoring currently active applications
- Process information includes PID, name, and command line


**See Also**:

get_installed_apps, start_app, stop_app_by_pname, stop_app_by_pid

### stop\_app\_by\_pname

```python
def stop_app_by_pname(pname: str) -> AppOperationResult
```

Stops an application by process name.

**Arguments**:

- `pname` _str_ - The process name of the application to stop.
  

**Returns**:

    AppOperationResult: Result object containing success status and error message if any.
  

**Example**:

```python
session = agent_bay.create().session
session.computer.start_app("notepad.exe")
result = session.computer.stop_app_by_pname("notepad.exe")
session.delete()
```


**Notes**:

- The process name should match exactly (case-sensitive on some systems)
- This will stop all processes matching the given name
- If multiple instances are running, all will be terminated
- The .exe extension may be required on Windows


**See Also**:

start_app, stop_app_by_pid, stop_app_by_cmd, list_visible_apps

### stop\_app\_by\_pid

```python
def stop_app_by_pid(pid: int) -> AppOperationResult
```

Stops an application by process ID.

**Arguments**:

- `pid` _int_ - The process ID of the application to stop.
  

**Returns**:

    AppOperationResult: Result object containing success status and error message if any.
  

**Example**:

```python
session = agent_bay.create().session
processes = session.computer.start_app("notepad.exe")
pid = processes.data[0].pid
result = session.computer.stop_app_by_pid(pid)
session.delete()
```


**Notes**:

- PID must be a valid process ID
- More precise than stopping by name (only stops specific process)
- The process must be owned by the session or have appropriate permissions
- PID can be obtained from start_app() or list_visible_apps()


**See Also**:

start_app, stop_app_by_pname, stop_app_by_cmd, list_visible_apps

### stop\_app\_by\_cmd

```python
def stop_app_by_cmd(stop_cmd: str) -> AppOperationResult
```

Stops an application by stop command.

**Arguments**:

- `stop_cmd` _str_ - The command to stop the application.
  

**Returns**:

    AppOperationResult: Result object containing success status and error message if any.
  

**Example**:

```python
session = agent_bay.create().session
apps = session.computer.get_installed_apps()
if apps.data and apps.data[0].stop_cmd:
  result = session.computer.stop_app_by_cmd(apps.data[0].stop_cmd)
session.delete()
```


**Notes**:

- The stop_cmd should be the command registered to stop the application
- Typically obtained from get_installed_apps() which returns app metadata
- Some applications may not have a stop command defined
- The command is executed as-is without shell interpretation


**See Also**:

get_installed_apps, start_app, stop_app_by_pname, stop_app_by_pid

## Best Practices

1. Verify screen coordinates before mouse operations
2. Use appropriate delays between UI interactions
3. Handle window focus changes properly
4. Take screenshots for verification and debugging
5. Use keyboard shortcuts for efficient automation
6. Clean up windows and applications after automation

## See Also

- [Synchronous vs Asynchronous API](../../../docs/guides/async-programming/sync-vs-async.md)

---

*Documentation generated automatically from source code using pydoc-markdown.*
