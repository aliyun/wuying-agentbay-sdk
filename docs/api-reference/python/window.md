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


```python
class Window:
    window_id: int            # The unique identifier of the window
    title: str                # The title of the window
    absolute_upper_left_x: int # The X coordinate of the upper left corner (optional)
    absolute_upper_left_y: int # The Y coordinate of the upper left corner (optional)
    width: int                # The width of the window (optional)
    height: int               # The height of the window (optional)
    pid: int                  # The process ID of the process that owns the window (optional)
    pname: str                # The name of the process that owns the window (optional)
    child_windows: List[Window] # The child windows of this window (optional)
```


```python
def list_root_windows(self) -> List[Window]:
```

**Returns:**
- `List[Window]`: A list of root windows.

**Raises:**
- `WindowError`: If there's an error listing the root windows.


```python
def get_active_window(self) -> Window:
```

**Returns:**
- `Window`: The currently active window.

**Raises:**
- `WindowError`: If there's an error getting the active window.


```python
def activate_window(self, window_id: int) -> bool:
```

**Parameters:**
- `window_id` (int): The ID of the window to activate.

**Returns:**
- `bool`: True if the operation was successful, False otherwise.

**Raises:**
- `WindowError`: If there's an error activating the window.


```python
def minimize_window(self, window_id: int) -> bool:
```

**Parameters:**
- `window_id` (int): The ID of the window to minimize.

**Returns:**
- `bool`: True if the operation was successful, False otherwise.

**Raises:**
- `WindowError`: If there's an error minimizing the window.


```python
def maximize_window(self, window_id: int) -> bool:
```

**Parameters:**
- `window_id` (int): The ID of the window to maximize.

**Returns:**
- `bool`: True if the operation was successful, False otherwise.

**Raises:**
- `WindowError`: If there's an error maximizing the window.


```python
def restore_window(self, window_id: int) -> bool:
```

**Parameters:**
- `window_id` (int): The ID of the window to restore.

**Returns:**
- `bool`: True if the operation was successful, False otherwise.

**Raises:**
- `WindowError`: If there's an error restoring the window.


```python
def fullscreen_window(self, window_id: int) -> bool:
```

**Parameters:**
- `window_id` (int): The ID of the window to make fullscreen.

**Returns:**
- `bool`: True if the operation was successful, False otherwise.

**Raises:**
- `WindowError`: If there's an error making the window fullscreen.


```python
def resize_window(self, window_id: int, width: int, height: int) -> bool:
```

**Parameters:**
- `window_id` (int): The ID of the window to resize.
- `width` (int): The new width of the window.
- `height` (int): The new height of the window.

**Returns:**
- `bool`: True if the operation was successful, False otherwise.

**Raises:**
- `WindowError`: If there's an error resizing the window.


```python
def close_window(self, window_id: int) -> bool:
```

**Parameters:**
- `window_id` (int): The ID of the window to close.

**Returns:**
- `bool`: True if the operation was successful, False otherwise.

**Raises:**
- `WindowError`: If there's an error closing the window.


```python
def focus_mode(self, on: bool) -> bool:
```

**Parameters:**
- `on` (bool): True to enable focus mode, False to disable it.

**Returns:**
- `bool`: True if the operation was successful, False otherwise.

**Raises:**
- `WindowError`: If there's an error setting focus mode.
