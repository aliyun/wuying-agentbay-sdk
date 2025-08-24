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


```typescript
getClickableUIElements(timeoutMs?: number): Promise<string>
```

**Parameters:**
- `timeoutMs` (number, optional): The timeout in milliseconds. Default is 2000ms.

**Returns:**
- `Promise<string>`: A promise that resolves to a string representation of clickable UI elements.

**Throws:**
- `APIError`: If the operation fails.


```typescript
getAllUIElements(timeoutMs?: number): Promise<string>
```

**Parameters:**
- `timeoutMs` (number, optional): The timeout in milliseconds. Default is 2000ms.

**Returns:**
- `Promise<string>`: A promise that resolves to a string representation of all UI elements.

**Throws:**
- `APIError`: If the operation fails.


```typescript
sendKey(key: number): Promise<string>
```

**Parameters:**
- `key` (number): The key code to send. Use the `KeyCode` constants.

**Returns:**
- `Promise<string>`: A promise that resolves to the response text.

**Throws:**
- `APIError`: If the operation fails.


```typescript
inputText(text: string): Promise<string>
```

**Parameters:**
- `text` (string): The text to input.

**Returns:**
- `Promise<string>`: A promise that resolves to the response text.

**Throws:**
- `APIError`: If the operation fails.


```typescript
swipe(startX: number, startY: number, endX: number, endY: number, durationMs?: number): Promise<string>
```

**Parameters:**
- `startX` (number): The starting X coordinate.
- `startY` (number): The starting Y coordinate.
- `endX` (number): The ending X coordinate.
- `endY` (number): The ending Y coordinate.
- `durationMs` (number, optional): The duration of the swipe in milliseconds. Default is 300ms.

**Returns:**
- `Promise<string>`: A promise that resolves to the response text.

**Throws:**
- `APIError`: If the operation fails.


```typescript
click(x: number, y: number, button?: string): Promise<string>
```

**Parameters:**
- `x` (number): The X coordinate.
- `y` (number): The Y coordinate.
- `button` (string, optional): The mouse button to use. Default is 'left'.

**Returns:**
- `Promise<string>`: A promise that resolves to the response text.

**Throws:**
- `APIError`: If the operation fails.


```typescript
screenshot(): Promise<string>
```

**Returns:**
- `Promise<string>`: A promise that resolves to the screenshot data.

**Throws:**
- `APIError`: If the operation fails.
