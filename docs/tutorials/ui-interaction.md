# UI Interaction Tutorial

AgentBay SDK provides powerful capabilities for interacting with UI elements in the cloud environment. This tutorial will guide you through UI element retrieval, input simulation, and screenshot capture.

## Overview

The UI module allows you to:

- Retrieve UI elements and their properties
- Send key events and input text
- Perform gestures like tap, swipe, and drag
- Capture screenshots

This is particularly useful for automated testing, UI automation, and screen scraping.

## Retrieving UI Elements

### Getting Clickable UI Elements

The following example demonstrates how to retrieve all clickable UI elements in the current view:

```python
from agentbay import AgentBay

# Initialize the SDK and create a session
agent_bay = AgentBay(api_key="your_api_key")
session_result = agent_bay.create()
session = session_result.session

# Get clickable UI elements
result = session.ui.get_clickable_ui_elements()
if result:
    print(f"Found {len(result)} clickable elements")
    for element in result:
        print(f"Element: {element.get('text', 'No text')} (Type: {element.get('type', 'Unknown')})")
else:
    print("Failed to retrieve UI elements")

# Delete the session when done
agent_bay.delete(session)
```

```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

// Initialize the SDK
const agentBay = new AgentBay({ apiKey: 'your_api_key' });

async function getClickableElements() {
  try {
    // Create a session
    const createResponse = await agentBay.create();
    const session = createResponse.session;
    
    // Get clickable UI elements
    const result = await session.ui.getClickableUIElements();
    const elements = JSON.parse(result);
    
    console.log(`Found ${elements.length} clickable elements`);
    elements.forEach(element => {
      console.log(`Element: ${element.text || 'No text'} (Type: ${element.type || 'Unknown'})`);
    });
    
    // Delete the session
    await agentBay.delete(session);
  } catch (error) {
    console.error('Error:', error);
  }
}

getClickableElements();
```

```go
package main

import (
	"fmt"
	"os"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

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

  // Get clickable UI elements
  uiResult, err := session.UI.GetClickableUIElements(2000)
  if err != nil {
    fmt.Printf("Error getting UI elements: %v\n", err)
    os.Exit(1)
  }

  fmt.Printf("Found %d clickable elements\n", len(uiResult.Elements))
  for _, element := range uiResult.Elements {
    fmt.Printf("Element: %s (Type: %s)\n", element.Text, element.Type)
  }

  // Delete the session
  _, err = client.Delete(session)
  if err != nil {
    fmt.Printf("Error deleting session: %v\n", err)
    os.Exit(1)
  }
}
```

### Getting All UI Elements

To retrieve all UI elements, not just the clickable ones:

```python
# Get all UI elements
result = session.ui.get_all_ui_elements()
if result:
    print(f"Found {len(result)} UI elements")
    for element in result:
        print(f"Element: {element.get('class_name', 'Unknown class')} - {element.get('text', 'No text')}")
else:
    print("Failed to retrieve UI elements")
```

## Sending Key Events

You can simulate key presses using the `send_key` method:

```python
from agentbay import AgentBay

# Initialize the SDK and create a session
agent_bay = AgentBay(api_key="your_api_key")
session_result = agent_bay.create()
session = session_result.session

# Send a BACK key press
result = session.ui.send_key(session.ui.KeyCode.BACK)
if result:
    print("Back key sent successfully")
else:
    print("Failed to send back key")

# Send a HOME key press
result = session.ui.send_key(session.ui.KeyCode.HOME)
if result:
    print("Home key sent successfully")
else:
    print("Failed to send home key")

# Delete the session when done
agent_bay.delete(session)
```

```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

// Initialize the SDK
const agentBay = new AgentBay({ apiKey: 'your_api_key' });

async function sendKeyEvents() {
  try {
    // Create a session
    const createResponse = await agentBay.create();
    const session = createResponse.session;
    
    // Send a BACK key press
    await session.ui.sendKey(session.ui.KeyCode.BACK);
    console.log("Back key sent successfully");
    
    // Send a HOME key press
    await session.ui.sendKey(session.ui.KeyCode.HOME);
    console.log("Home key sent successfully");
    
    // Delete the session
    await agentBay.delete(session);
  } catch (error) {
    console.error('Error:', error);
  }
}

sendKeyEvents();
```

## Input Text

To input text into the currently focused field:

```python
# Input text
result = session.ui.input_text("Hello, AgentBay!")
if result:
    print("Text input successful")
else:
    print("Failed to input text")
```

```typescript
// Input text
await session.ui.inputText("Hello, AgentBay!");
console.log("Text input successful");
```

## Performing Gestures

### Tap Gesture

To tap on a specific position on the screen:

```python
# Tap at coordinates (500, 500)
result = session.ui.tap(500, 500)
if result:
    print("Tap gesture performed successfully")
else:
    print("Failed to perform tap gesture")
```

```typescript
// Tap at coordinates (500, 500)
await session.ui.tap(500, 500);
console.log("Tap gesture performed successfully");
```

### Swipe Gesture

To perform a swipe gesture:

```python
# Swipe from (100, 500) to (800, 500)
result = session.ui.swipe(100, 500, 800, 500)
if result:
    print("Swipe gesture performed successfully")
else:
    print("Failed to perform swipe gesture")
```

```typescript
// Swipe from (100, 500) to (800, 500)
await session.ui.swipe(100, 500, 800, 500);
console.log("Swipe gesture performed successfully");
```

## Taking Screenshots

You can capture screenshots of the current screen:

```python
from agentbay import AgentBay
import base64

# Initialize the SDK and create a session
agent_bay = AgentBay(api_key="your_api_key")
session_result = agent_bay.create()
session = session_result.session

# Take a screenshot
result = session.ui.take_screenshot()
if result.success:
    # Save the screenshot as a file
    with open("screenshot.png", "wb") as f:
        f.write(base64.b64decode(result.image_data))
    print("Screenshot saved as 'screenshot.png'")
else:
    print(f"Failed to take screenshot: {result.error_message}")

# Delete the session when done
agent_bay.delete(session)
```

```typescript
import { AgentBay } from 'wuying-agentbay-sdk';
import * as fs from 'fs';

// Initialize the SDK
const agentBay = new AgentBay({ apiKey: 'your_api_key' });

async function takeScreenshot() {
  try {
    // Create a session
    const createResponse = await agentBay.create();
    const session = createResponse.session;
    
    // Take a screenshot
    const result = await session.ui.takeScreenshot();
    
    // Save the screenshot as a file
    fs.writeFileSync('screenshot.png', Buffer.from(result.imageData, 'base64'));
    console.log("Screenshot saved as 'screenshot.png'");
    
    // Delete the session
    await agentBay.delete(session);
  } catch (error) {
    console.error('Error:', error);
  }
}

takeScreenshot();
```

## Clicking on UI Elements

To find and click on a UI element by text:

```python
from agentbay import AgentBay

# Initialize the SDK and create a session
agent_bay = AgentBay(api_key="your_api_key")
session_result = agent_bay.create()
session = session_result.session

# Get all clickable elements
elements = session.ui.get_clickable_ui_elements()

# Find and click on an element with specific text
target_text = "Settings"
element_found = False

for element in elements:
    if element.get('text') == target_text:
        # Get the bounds of the element
        bounds = element.get('bounds')
        if bounds:
            # Parse bounds format "[x1,y1][x2,y2]"
            bounds = bounds.replace('][', ',').strip('[]').split(',')
            x1, y1, x2, y2 = map(int, bounds)
            
            # Calculate center point
            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2
            
            # Tap on the center of the element
            result = session.ui.tap(center_x, center_y)
            if result:
                print(f"Successfully clicked on '{target_text}'")
                element_found = True
                break

if not element_found:
    print(f"Element with text '{target_text}' not found")

# Delete the session when done
agent_bay.delete(session)
```

## Best Practices

1. **Timing**: When interacting with UI elements, sometimes it's necessary to add short delays between operations to allow the UI to update.
2. **Element Identification**: Use descriptive properties like text, resource ID, or class name to reliably identify UI elements.
3. **Error Handling**: Always check the return result of UI operations to ensure they completed successfully.
4. **Resource Management**: After completing UI operations, make sure to delete sessions that are no longer needed.
5. **Robust Automation**: When automating UI interactions, build in retry mechanisms and verification steps to handle unexpected UI changes.

## Related Resources

- [API Reference: UI (Python)](../api-reference/python/ui.md)
- [API Reference: UI (TypeScript)](../api-reference/typescript/ui.md)
- [API Reference: UI (Golang)](../api-reference/golang/ui.md)
- [Examples: UI Interaction](../examples/python/ui_example) 