# Computer UI Automation Guide

This guide covers computer UI automation capabilities in AgentBay SDK for desktop environments, including mouse operations, keyboard operations, and screen operations.

**Verified System Images:** These features have been verified to work with `windows_latest` and `linux_latest` system images.

## 📋 Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Mouse Operations](#mouse-operations)
- [Keyboard Operations](#keyboard-operations)
- [Screen Operations](#screen-operations)
- [Best Practices](#best-practices)
- [Common Use Cases](#common-use-cases)
- [Troubleshooting](#troubleshooting)

<a id="overview"></a>
## 🎯 Overview

AgentBay provides powerful computer UI automation capabilities for interacting with Windows desktop environments in the cloud. You can:

1. **Mouse Operations** - Click, move, drag, and scroll with precise control
2. **Keyboard Operations** - Type text and send key combinations
3. **Screen Operations** - Capture screenshots and get screen information

All operations are performed through the `session.computer` module, which provides a comprehensive API for desktop automation tasks.

<a id="prerequisites"></a>
## ⚙️ Prerequisites

Computer UI automation requires creating a session with a computer use system image. The following images have been verified:
- `windows_latest` - Windows desktop environment
- `linux_latest` - Linux desktop environment

```python
from agentbay import AgentBay
from agentbay.session_params import CreateSessionParams

agent_bay = AgentBay()
# Use windows_latest or linux_latest
session_params = CreateSessionParams(image_id="windows_latest")
session = agent_bay.create(session_params).session
```

<a id="mouse-operations"></a>
## 🖱️ Mouse Operations

### Click Operations

The `click_mouse()` method supports multiple click types:

```python
session_params = CreateSessionParams(image_id="windows_latest")
session = agent_bay.create(session_params).session

# Left click
result = session.computer.click_mouse(x=500, y=300, button="left")
if result.success:
    print("Left click successful")
# Output: Left click successful

# Right click
result = session.computer.click_mouse(x=500, y=300, button="right")
if result.success:
    print("Right click successful")
# Output: Right click successful

# Middle click
result = session.computer.click_mouse(x=500, y=300, button="middle")
if result.success:
    print("Middle click successful")
# Output: Middle click successful

# Double left click
result = session.computer.click_mouse(x=500, y=300, button="double_left")
if result.success:
    print("Double click successful")
# Output: Double click successful

agent_bay.delete(session)
```

**Supported button types:** `"left"`, `"right"`, `"middle"`, `"double_left"`

### Move Mouse

Move the mouse cursor to specific coordinates:

```python
session_params = CreateSessionParams(image_id="windows_latest")
session = agent_bay.create(session_params).session

result = session.computer.move_mouse(x=600, y=400)
if result.success:
    print("Mouse moved successfully")
# Output: Mouse moved successfully

agent_bay.delete(session)
```

### Drag Operations

Drag the mouse from one point to another:

```python
session_params = CreateSessionParams(image_id="windows_latest")
session = agent_bay.create(session_params).session

result = session.computer.drag_mouse(
    from_x=100, 
    from_y=100, 
    to_x=200, 
    to_y=200, 
    button="left"
)
if result.success:
    print("Drag operation successful")
# Output: Drag operation successful

agent_bay.delete(session)
```

**Supported button types for drag:** `"left"`, `"right"`, `"middle"`

### Scroll Operations

Scroll the mouse wheel at specific coordinates:

```python
session_params = CreateSessionParams(image_id="windows_latest")
session = agent_bay.create(session_params).session

# Scroll up
result = session.computer.scroll(x=500, y=500, direction="up", amount=3)
if result.success:
    print("Scrolled up successfully")
# Output: Scrolled up successfully

# Scroll down
result = session.computer.scroll(x=500, y=500, direction="down", amount=5)
if result.success:
    print("Scrolled down successfully")
# Output: Scrolled down successfully

agent_bay.delete(session)
```

**Supported directions:** `"up"`, `"down"`, `"left"`, `"right"`

### Get Cursor Position

Retrieve the current mouse cursor position:

```python
import json

session_params = CreateSessionParams(image_id="windows_latest")
session = agent_bay.create(session_params).session

result = session.computer.get_cursor_position()
if result.success:
    cursor_data = json.loads(result.data)
    print(f"Cursor at x={cursor_data['x']}, y={cursor_data['y']}")
# Output: Cursor at x=512, y=384

agent_bay.delete(session)
```

<a id="keyboard-operations"></a>
## ⌨️ Keyboard Operations

### Text Input

Type text into the active window or field:

```python
session_params = CreateSessionParams(image_id="windows_latest")
session = agent_bay.create(session_params).session

result = session.computer.input_text("Hello AgentBay!")
if result.success:
    print("Text input successful")
# Output: Text input successful

agent_bay.delete(session)
```

### Press Keys

Press key combinations (supports modifier keys):

```python
session_params = CreateSessionParams(image_id="windows_latest")
session = agent_bay.create(session_params).session

# Press Ctrl+A to select all
result = session.computer.press_keys(keys=["Ctrl", "a"])
if result.success:
    print("Keys pressed successfully")
# Output: Keys pressed successfully

# Press Ctrl+C to copy
result = session.computer.press_keys(keys=["Ctrl", "c"])
if result.success:
    print("Copy command sent")
# Output: Copy command sent

agent_bay.delete(session)
```

### Release Keys

Release specific keys (useful when keys are held):

```python
session_params = CreateSessionParams(image_id="windows_latest")
session = agent_bay.create(session_params).session

# Hold Ctrl key
session.computer.press_keys(keys=["Ctrl"], hold=True)

# ... perform other operations ...

# Release Ctrl key
result = session.computer.release_keys(keys=["Ctrl"])
if result.success:
    print("Keys released successfully")
# Output: Keys released successfully

agent_bay.delete(session)
```

<a id="screen-operations"></a>
## 📸 Screen Operations

### Take Screenshot

Capture a screenshot of the current screen:

```python
import base64

session_params = CreateSessionParams(image_id="windows_latest")
session = agent_bay.create(session_params).session

result = session.computer.screenshot()
if result.success:
    # Save screenshot to file
    with open("screenshot.png", "wb") as f:
        if isinstance(result.data, str):
            f.write(base64.b64decode(result.data))
        else:
            f.write(result.data)
    print("Screenshot saved")
# Output: Screenshot saved

agent_bay.delete(session)
```

### Get Screen Size

Retrieve screen dimensions and DPI scaling factor:

```python
import json

session_params = CreateSessionParams(image_id="windows_latest")
session = agent_bay.create(session_params).session

result = session.computer.get_screen_size()
if result.success:
    screen_data = json.loads(result.data)
    print(f"Screen width: {screen_data['width']}")
    print(f"Screen height: {screen_data['height']}")
    print(f"DPI scaling factor: {screen_data['dpiScalingFactor']}")
# Output: Screen width: 1024
# Output: Screen height: 768
# Output: DPI scaling factor: 1.0

agent_bay.delete(session)
```

<a id="best-practices"></a>
## 💡 Best Practices

### 1. Always Use Computer Use Images

Computer UI automation requires a computer use system image. Verified images:

```python
# Correct - Use windows_latest or linux_latest
session_params = CreateSessionParams(image_id="windows_latest")
session = agent_bay.create(session_params).session

# Also correct - Linux desktop environment
session_params = CreateSessionParams(image_id="linux_latest")
session = agent_bay.create(session_params).session

# Incorrect - will not work for computer operations
session_params = CreateSessionParams(image_id="mobile_latest")
session = agent_bay.create(session_params).session
```

### 2. Check Operation Results

Always verify operation success before proceeding:

```python
result = session.computer.click_mouse(x=100, y=200, button="left")
if not result.success:
    print(f"Click failed: {result.error_message}")
    # Handle error appropriately
```

### 3. Clean Up Sessions

Always clean up sessions after use:

```python
try:
    session_params = CreateSessionParams(image_id="windows_latest")
    session = agent_bay.create(session_params).session
    
    # Your automation code here
    result = session.computer.click_mouse(x=100, y=200)
    
finally:
    agent_bay.delete(session)
```

### 4. Handle Screenshot Data Properly

Screenshots may be returned as base64 strings or raw bytes:

```python
import base64

result = session.computer.screenshot()
if result.success:
    with open("screenshot.png", "wb") as f:
        if isinstance(result.data, str):
            f.write(base64.b64decode(result.data))
        else:
            f.write(result.data)
```

### 5. Use Appropriate Coordinates

Ensure coordinates are within screen bounds:

```python
import json

# Get screen size first
size_result = session.computer.get_screen_size()
if size_result.success:
    screen_data = json.loads(size_result.data)
    max_x = screen_data['width']
    max_y = screen_data['height']
    
    # Use coordinates within bounds
    if 0 <= x < max_x and 0 <= y < max_y:
        session.computer.click_mouse(x=x, y=y, button="left")
```

<a id="common-use-cases"></a>
## 🎨 Common Use Cases

### Example 1: Automated Form Filling

```python
from agentbay import AgentBay
from agentbay.session_params import CreateSessionParams

agent_bay = AgentBay()
session_params = CreateSessionParams(image_id="windows_latest")
session = agent_bay.create(session_params).session

try:
    # Click on first field
    session.computer.click_mouse(x=300, y=200, button="left")
    
    # Enter name
    session.computer.input_text("John Doe")
    
    # Tab to next field
    session.computer.press_keys(keys=["Tab"])
    
    # Enter email
    session.computer.input_text("john.doe@example.com")
    
    # Click submit button
    session.computer.click_mouse(x=400, y=500, button="left")
    
finally:
    agent_bay.delete(session)
```

### Example 2: Screen Capture and Analysis

```python
import base64
import json
from agentbay import AgentBay
from agentbay.session_params import CreateSessionParams

agent_bay = AgentBay()
session_params = CreateSessionParams(image_id="windows_latest")
session = agent_bay.create(session_params).session

try:
    # Get screen information
    size_result = session.computer.get_screen_size()
    screen_data = json.loads(size_result.data)
    print(f"Screen: {screen_data['width']}x{screen_data['height']}")
    # Output: Screen: 1024x768
    
    # Take screenshot
    screenshot_result = session.computer.screenshot()
    if screenshot_result.success:
        with open("analysis.png", "wb") as f:
            f.write(base64.b64decode(screenshot_result.data))
        print("Screenshot captured for analysis")
    # Output: Screenshot captured for analysis
    
finally:
    agent_bay.delete(session)
```

### Example 3: Drag and Drop Operation

```python
from agentbay import AgentBay
from agentbay.session_params import CreateSessionParams

agent_bay = AgentBay()
session_params = CreateSessionParams(image_id="windows_latest")
session = agent_bay.create(session_params).session

try:
    # Drag file from source to destination
    result = session.computer.drag_mouse(
        from_x=150,
        from_y=200,
        to_x=400,
        to_y=300,
        button="left"
    )
    
    if result.success:
        print("File moved successfully")
    # Output: File moved successfully
    
finally:
    agent_bay.delete(session)
```

<a id="troubleshooting"></a>
## 🆘 Troubleshooting

### Common Issues

1. **"Tool not found" errors**
   - Ensure you're using a computer use image (`windows_latest` or `linux_latest`)
   - Verify the session was created successfully
   - Check that API key and endpoint are configured correctly

2. **Coordinates out of bounds**
   - Use `get_screen_size()` to determine valid coordinate ranges
   - Verify coordinates are positive integers within screen dimensions

3. **Screenshot data handling errors**
   - Check if data is base64 string or raw bytes
   - Use proper decoding as shown in examples

4. **Key combination not working**
   - Verify key names are correct (e.g., "Ctrl", not "Control")
   - Ensure keys are pressed in the correct order
   - Use `release_keys()` if keys remain held

### Getting Help

For more assistance:
- Check the [API Reference](../../api-reference.md)
- Review [Session Management Guide](../common-features/basics/session-management.md)
- See [Troubleshooting Guide](../../troubleshooting/README.md)

## 📚 Related Guides

- [Session Management Guide](../common-features/basics/session-management.md) - Learn about session lifecycle
- [Application and Window Operations](application-window-operations.md) - Manage applications and windows
- [Command Execution](../common-features/basics/command-execution.md) - Execute shell commands
- [Mobile UI Automation](../mobile-use/mobile-ui-automation.md) - Mobile device automation
