# Window Management Tutorial

AgentBay SDK provides methods for managing windows in the cloud environment. This tutorial will guide you through listing, activating, and manipulating windows.

## Overview

The Window module allows you to:

- List all root windows and their child windows
- Get the currently active window
- Activate specific windows
- Resize, move, and manipulate windows
- Get window properties like position and dimensions

This is particularly useful for automating desktop applications and UI testing.

## Listing Windows

### Listing Root Windows

The following example demonstrates how to list all root windows:

```python
from agentbay import AgentBay

# Initialize the SDK and create a session
agent_bay = AgentBay(api_key="your_api_key")
session_result = agent_bay.create()
session = session_result.session

# List all root windows
windows = session.window.list_root_windows()
print(f"Found {len(windows)} root windows:")
for window in windows:
    print(f"Window ID: {window.window_id}, Title: {window.title}")

# Delete the session when done
agent_bay.delete(session)
```

```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

// Initialize the SDK
const agentBay = new AgentBay({ apiKey: 'your_api_key' });

async function listRootWindows() {
  try {
    // Create a session
    const createResponse = await agentBay.create();
    const session = createResponse.session;
    
    // List all root windows
    const windows = await session.window.listRootWindows();
    console.log(`Found ${windows.length} root windows:`);
    windows.forEach(window => {
      console.log(`Window ID: ${window.window_id}, Title: ${window.title}`);
    });
    
    // Delete the session
    await agentBay.delete(session);
  } catch (error) {
    console.error('Error:', error);
  }
}

listRootWindows();
```

```go
package main

import (
	"encoding/json"
	"fmt"
	"os"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

type Window struct {
	WindowID int    `json:"window_id"`
	Title    string `json:"title"`
}

func main() {
  // Initialize the SDK
  client, err := agentbay.NewAgentBay("your_api_key")
  if err != nil {
    fmt.Printf("Error initializing AgentBay client: %v\n", err)
    os.Exit(1)
  }

  // Create a session
  result, err := client.Create(nil)
  if err != nil {
    fmt.Printf("Error creating session: %v\n", err)
    os.Exit(1)
  }

  session := result.Session

  // List all root windows
  windowsJson, err := session.Window.ListRootWindows()
  if err != nil {
    fmt.Printf("Error listing windows: %v\n", err)
    os.Exit(1)
  }

  var windows []Window
  err = json.Unmarshal([]byte(windowsJson), &windows)
  if err != nil {
    fmt.Printf("Error parsing window data: %v\n", err)
    os.Exit(1)
  }

  fmt.Printf("Found %d root windows:\n", len(windows))
  for _, window := range windows {
    fmt.Printf("Window ID: %d, Title: %s\n", window.WindowID, window.Title)
  }

  // Delete the session
  _, err = client.Delete(session)
  if err != nil {
    fmt.Printf("Error deleting session: %v\n", err)
    os.Exit(1)
  }
}
```

### Getting the Active Window

To retrieve the currently active window:

```python
from agentbay import AgentBay

# Initialize the SDK and create a session
agent_bay = AgentBay(api_key="your_api_key")
session_result = agent_bay.create()
session = session_result.session

# Get the active window
active_window = session.window.get_active_window()
print(f"Active window - ID: {active_window.window_id}, Title: {active_window.title}")

# Get additional properties if available
if hasattr(active_window, 'width') and hasattr(active_window, 'height'):
    print(f"Window size: {active_window.width} x {active_window.height}")
if hasattr(active_window, 'absolute_upper_left_x') and hasattr(active_window, 'absolute_upper_left_y'):
    print(f"Window position: ({active_window.absolute_upper_left_x}, {active_window.absolute_upper_left_y})")

# Delete the session when done
agent_bay.delete(session)
```

```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

// Initialize the SDK
const agentBay = new AgentBay({ apiKey: 'your_api_key' });

async function getActiveWindow() {
  try {
    // Create a session
    const createResponse = await agentBay.create();
    const session = createResponse.session;
    
    // Get the active window
    const activeWindow = await session.window.getActiveWindow();
    console.log(`Active window - ID: ${activeWindow.window_id}, Title: ${activeWindow.title}`);
    
    // Get additional properties if available
    if (activeWindow.width && activeWindow.height) {
      console.log(`Window size: ${activeWindow.width} x ${activeWindow.height}`);
    }
    if (activeWindow.absolute_upper_left_x !== undefined && activeWindow.absolute_upper_left_y !== undefined) {
      console.log(`Window position: (${activeWindow.absolute_upper_left_x}, ${activeWindow.absolute_upper_left_y})`);
    }
    
    // Delete the session
    await agentBay.delete(session);
  } catch (error) {
    console.error('Error:', error);
  }
}

getActiveWindow();
```

## Window Manipulation

### Activating a Window

To bring a specific window to the foreground:

```python
from agentbay import AgentBay

# Initialize the SDK and create a session
agent_bay = AgentBay(api_key="your_api_key")
session_result = agent_bay.create()
session = session_result.session

# List all root windows
windows = session.window.list_root_windows()

# Find a window by title
target_title = "Calculator"
target_window = None

for window in windows:
    if target_title in window.title:
        target_window = window
        break

if target_window:
    # Activate the window
    result = session.window.activate_window(target_window.window_id)
    if result:
        print(f"Successfully activated window: {target_window.title}")
    else:
        print(f"Failed to activate window: {target_window.title}")
else:
    print(f"Window with title containing '{target_title}' not found")

# Delete the session when done
agent_bay.delete(session)
```

```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

// Initialize the SDK
const agentBay = new AgentBay({ apiKey: 'your_api_key' });

async function activateWindow() {
  try {
    // Create a session
    const createResponse = await agentBay.create();
    const session = createResponse.session;
    
    // List all root windows
    const windows = await session.window.listRootWindows();
    
    // Find a window by title
    const targetTitle = "Calculator";
    const targetWindow = windows.find(window => window.title.includes(targetTitle));
    
    if (targetWindow) {
      // Activate the window
      const result = await session.window.activateWindow(targetWindow.window_id);
      if (result) {
        console.log(`Successfully activated window: ${targetWindow.title}`);
      } else {
        console.log(`Failed to activate window: ${targetWindow.title}`);
      }
    } else {
      console.log(`Window with title containing '${targetTitle}' not found`);
    }
    
    // Delete the session
    await agentBay.delete(session);
  } catch (error) {
    console.error('Error:', error);
  }
}

activateWindow();
```

### Moving a Window

To move a window to a new position:

```python
from agentbay import AgentBay

# Initialize the SDK and create a session
agent_bay = AgentBay(api_key="your_api_key")
session_result = agent_bay.create()
session = session_result.session

# Get the active window
active_window = session.window.get_active_window()

# Move the window to position (100, 100)
result = session.window.move_window(active_window.window_id, 100, 100)
if result:
    print(f"Successfully moved window to (100, 100)")
else:
    print("Failed to move window")

# Delete the session when done
agent_bay.delete(session)
```

### Resizing a Window

To resize a window:

```python
from agentbay import AgentBay

# Initialize the SDK and create a session
agent_bay = AgentBay(api_key="your_api_key")
session_result = agent_bay.create()
session = session_result.session

# Get the active window
active_window = session.window.get_active_window()

# Resize the window to 800x600
result = session.window.resize_window(active_window.window_id, 800, 600)
if result:
    print(f"Successfully resized window to 800x600")
else:
    print("Failed to resize window")

# Delete the session when done
agent_bay.delete(session)
```

## Working with Child Windows

To get child windows of a parent window:

```python
from agentbay import AgentBay

# Initialize the SDK and create a session
agent_bay = AgentBay(api_key="your_api_key")
session_result = agent_bay.create()
session = session_result.session

# List all root windows
windows = session.window.list_root_windows()

# Find a window that has child windows
for window in windows:
    if hasattr(window, 'child_windows') and window.child_windows:
        print(f"Window '{window.title}' has {len(window.child_windows)} child windows:")
        for child in window.child_windows:
            print(f"  Child window - ID: {child.window_id}, Title: {child.title}")
        break

# Delete the session when done
agent_bay.delete(session)
```

## Best Practices

1. **Window Identification**: Use window titles or IDs to reliably identify windows.
2. **Error Handling**: Always check the return result of window operations to ensure they completed successfully.
3. **Resource Management**: After completing operations, make sure to delete sessions that are no longer needed.
4. **Window State**: Be aware that window states can change due to user interaction or other processes.
5. **Resilient Automation**: When automating window operations, build in retry mechanisms and verification steps to handle unexpected window changes.

## Related Resources

- [API Reference: Window (Python)](../api-reference/python/window.md)
- [API Reference: Window (TypeScript)](../api-reference/typescript/window.md)
- [API Reference: Window (Golang)](../api-reference/golang/window.md)
- [Examples: Window Operations](../examples/python/application_window) 