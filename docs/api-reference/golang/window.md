# Window Class

The Window class provides methods for managing windows in the AgentBay cloud environment, including listing windows, getting the active window, and manipulating window states.

## Class Properties

###

```python
class Window:
    def __init__(self, session):
        self.session = session
```

## Data Types


Represents a window in the system.


```go
type Window struct {
    WindowID           int      `json:"window_id"`
    Title              string   `json:"title"`
    AbsoluteUpperLeftX int      `json:"absolute_upper_left_x,omitempty"`
    AbsoluteUpperLeftY int      `json:"absolute_upper_left_y,omitempty"`
    Width              int      `json:"width,omitempty"`
    Height             int      `json:"height,omitempty"`
    PID                int      `json:"pid,omitempty"`
    PName              string   `json:"pname,omitempty"`
    ChildWindows       []Window `json:"child_windows,omitempty"`
}
```

## Methods


Lists all root windows in the system.


```go
func (wm *WindowManager) ListRootWindows() (string, error)
```

**Returns:**
- `string`: A JSON string containing the list of root windows.
- `error`: An error if the operation fails.


Gets the currently active window.


```go
func (wm *WindowManager) GetActiveWindow() (string, error)
```

**Returns:**
- `string`: A JSON string containing the active window.
- `error`: An error if the operation fails.


Activates (brings to front) a window by ID.


```go
func (wm *WindowManager) ActivateWindow(windowID int) error
```

**Parameters:**
- `windowID` (int): The ID of the window to activate.

**Returns:**
- `error`: An error if the operation fails.


Minimizes a window by ID.


```go
func (wm *WindowManager) MinimizeWindow(windowID int) error
```

**Parameters:**
- `windowID` (int): The ID of the window to minimize.

**Returns:**
- `error`: An error if the operation fails.


Maximizes a window by ID.


```go
func (wm *WindowManager) MaximizeWindow(windowID int) error
```

**Parameters:**
- `windowID` (int): The ID of the window to maximize.

**Returns:**
- `error`: An error if the operation fails.


Restores a window by ID (from minimized or maximized state).


```go
func (wm *WindowManager) RestoreWindow(windowID int) error
```

**Parameters:**
- `windowID` (int): The ID of the window to restore.

**Returns:**
- `error`: An error if the operation fails.


Makes a window fullscreen by ID.


```go
func (wm *WindowManager) FullscreenWindow(windowID int) error
```

**Parameters:**
- `windowID` (int): The ID of the window to make fullscreen.

**Returns:**
- `error`: An error if the operation fails.


Resizes a window by ID to the specified width and height.


```go
func (wm *WindowManager) ResizeWindow(windowID, width, height int) error
```

**Parameters:**
- `windowID` (int): The ID of the window to resize.
- `width` (int): The new width of the window.
- `height` (int): The new height of the window.

**Returns:**
- `error`: An error if the operation fails.


Closes a window by ID.


```go
func (wm *WindowManager) CloseWindow(windowID int) error
```

**Parameters:**
- `windowID` (int): The ID of the window to close.

**Returns:**
- `error`: An error if the operation fails.


Enables or disables focus mode, which prevents window switching.


```go
func (wm *WindowManager) FocusMode(on bool) error
```

**Parameters:**
- `on` (bool): True to enable focus mode, False to disable it.

**Returns:**
- `error`: An error if the operation fails.

## Usage Examples

###

```python
# Create a session
session = agent_bay.create()

# List root windows
root_windows = session.window.list_root_windows()
for window in root_windows:
    print(f"Window: {window.title} (ID: {window.window_id}, Process: {window.pname}, PID: {window.pid})")

# Get active window
active_window = session.window.get_active_window()
print(f"Active window: {active_window.title} (ID: {active_window.window_id})")

# Manipulate windows
if root_windows:
    window_id = root_windows[0].window_id
    
    # Maximize window
    session.window.maximize_window(window_id)
    print("Window maximized")
    
    # Restore window
    session.window.restore_window(window_id)
    print("Window restored")
    
    # Resize window
    session.window.resize_window(window_id, 800, 600)
    print("Window resized")
    
    # Activate window
    session.window.activate_window(window_id)
    print("Window activated")
```

## Related Resources

- [Session Class](session.md): The session class that provides access to the Window class.
- [Application Class](application.md): The application class for managing applications in the cloud environment.
- [Applications Concept](../concepts/applications.md): Conceptual information about applications and windows in the AgentBay cloud environment. 