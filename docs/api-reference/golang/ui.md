# UI Class API Reference

The `UI` class provides methods for interacting with UI elements in the AgentBay cloud environment. This includes retrieving UI elements, sending key events, inputting text, performing gestures, and taking screenshots.

## Properties

###

- `KeyCode`: Constants for key codes that can be used with the `send_key` method.
  - `HOME`: Home key (3)
  - `BACK`: Back key (4)
  - `VOLUME_UP`: Volume up key (24)
  - `VOLUME_DOWN`: Volume down key (25)
  - `POWER`: Power key (26)
  - `MENU`: Menu key (82)

## Methods


Retrieves all clickable UI elements within the specified timeout.


```go
GetClickableUIElements(timeoutMs int) (*UIElementsResult, error)
```

**Parameters:**
- `timeoutMs` (int): The timeout in milliseconds. If <= 0, default is 2000ms.

**Returns:**
- `*UIElementsResult`: A result object containing clickable UI elements and RequestID.
- `error`: An error if the operation fails.

**UIElementsResult Structure:**
```go
type UIElementsResult struct {
    RequestID string      // Unique request identifier for debugging
    Elements  []*UIElement // Array of UI elements
}

type UIElement struct {
    Bounds     string       // Bounds of the element
    ClassName  string       // CSS class name
    Text       string       // Text content
    Type       string       // Element type
    ResourceId string       // Resource ID
    Index      int          // Element index
    IsParent   bool         // Whether this element is a parent
    Children   []*UIElement // Child elements
}
```


Retrieves all UI elements within the specified timeout.


```go
GetAllUIElements(timeoutMs int) (*UIElementsResult, error)
```

**Parameters:**
- `timeoutMs` (int): The timeout in milliseconds. If <= 0, default is 2000ms.

**Returns:**
- `*UIElementsResult`: A result object containing all UI elements and RequestID.
- `error`: An error if the operation fails.


Sends a key press event.


```go
SendKey(key int) (*KeyActionResult, error)
```

**Parameters:**
- `key` (int): The key code to send. Use the `KeyCode` constants.

**Returns:**
- `*KeyActionResult`: A result object containing success status and RequestID.
- `error`: An error if the operation fails.

**KeyActionResult Structure:**
```go
type KeyActionResult struct {
    RequestID string // Unique request identifier for debugging
    Success   bool   // Whether the key press was successful
}
```


Inputs text into the active field.


```go
InputText(text string) (*TextInputResult, error)
```

**Parameters:**
- `text` (string): The text to input.

**Returns:**
- `*TextInputResult`: A result object containing the input text and RequestID.
- `error`: An error if the operation fails.

**TextInputResult Structure:**
```go
type TextInputResult struct {
    RequestID string // Unique request identifier for debugging
    Text      string // The text that was input
}
```


Performs a swipe gesture on the screen.


```go
Swipe(startX, startY, endX, endY, durationMs int) (*SwipeResult, error)
```

**Parameters:**
- `startX` (int): The starting X coordinate.
- `startY` (int): The starting Y coordinate.
- `endX` (int): The ending X coordinate.
- `endY` (int): The ending Y coordinate.
- `durationMs` (int): The duration of the swipe in milliseconds.

**Returns:**
- `*SwipeResult`: A result object containing success status and RequestID.
- `error`: An error if the operation fails.

**SwipeResult Structure:**
```go
type SwipeResult struct {
    RequestID string // Unique request identifier for debugging
    Success   bool   // Whether the swipe was successful
}
```


Clicks on the screen at the specified coordinates.


```go
Click(x, y int, button string) (*UIResult, error)
```

**Parameters:**
- `x` (int): The X coordinate.
- `y` (int): The Y coordinate.
- `button` (string): The mouse button to use. If empty, default is 'left'.

**Returns:**
- `*UIResult`: A result object containing success status and RequestID.
- `error`: An error if the operation fails.

**UIResult Structure:**
```go
type UIResult struct {
    RequestID  string // Unique request identifier for debugging
    ComponentID string // Component ID (if applicable)
    Success    bool   // Whether the operation was successful
}
```


Takes a screenshot of the current screen.


```go
Screenshot() (*UIResult, error)
```

**Returns:**
- `*UIResult`: A result object containing success status and RequestID.
- `error`: An error if the operation fails.

## UI Element Structure

UI elements returned by `getClickableUIElements` and `getAllUIElements` have the following structure:

```typescript
interface UIElement {
  bounds: string;
  className: string;
  text: string;
  type: string;
  resourceId: string;
  index: number;
  isParent: boolean;
  children: UIElement[];
}
```

## Usage Examples

###

```python
# Take a screenshot
screenshot = session.ui.screenshot()
print(f"Screenshot data length: {len(screenshot)} characters")

# Get all UI elements
elements = session.ui.get_all_ui_elements()
print(f"Retrieved {len(elements)} UI elements")

# Get clickable UI elements
clickable_elements = session.ui.get_clickable_ui_elements()
print(f"Retrieved {len(clickable_elements)} clickable UI elements")

# Send a key press
result = session.ui.send_key(KeyCode.HOME)
print(f"Send key result: {result}")

# Input text
session.ui.input_text("Hello, world!")

# Perform a swipe gesture
session.ui.swipe(100, 500, 100, 100, 500)

# Click on the screen
session.ui.click(200, 300)
```

## Related Resources

- [Session Class](session.md): The Session class that provides access to the UI class.