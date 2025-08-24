# Window Class

The Window class provides methods for managing windows in the AgentBay cloud environment, including listing windows, getting the active window, and manipulating window states.

## Overview

The Window class is accessed through a session instance and provides methods for window management in the cloud environment.

## Data Types


Represents a window in the system.


```typescript
interface Window {
    window_id: number;         // The unique identifier of the window
    title: string;             // The title of the window
    absolute_upper_left_x?: number; // The X coordinate of the upper left corner (optional)
    absolute_upper_left_y?: number; // The Y coordinate of the upper left corner (optional)
    width?: number;            // The width of the window (optional)
    height?: number;           // The height of the window (optional)
    pid?: number;              // The process ID of the process that owns the window (optional)
    pname?: string;            // The name of the process that owns the window (optional)
    child_windows?: Window[];  // The child windows of this window (optional)
}
```


```typescript
async listRootWindows(): Promise<Window[]>
```

**Returns:**
- `Promise<Window[]>`: A promise that resolves to a list of root windows.

**Throws:**
- `APIError`: If there's an error listing the root windows.


```typescript
async getActiveWindow(): Promise<Window>
```

**Returns:**
- `Promise<Window>`: A promise that resolves to the currently active window.

**Throws:**
- `APIError`: If there's an error getting the active window.


```typescript
async activateWindow(windowId: number): Promise<boolean>
```

**Parameters:**
- `windowId` (number): The ID of the window to activate.

**Returns:**
- `Promise<boolean>`: A promise that resolves to true if the operation was successful, false otherwise.

**Throws:**
- `APIError`: If there's an error activating the window.


```typescript
async minimizeWindow(windowId: number): Promise<boolean>
```

**Parameters:**
- `windowId` (number): The ID of the window to minimize.

**Returns:**
- `Promise<boolean>`: A promise that resolves to true if the operation was successful, false otherwise.

**Throws:**
- `APIError`: If there's an error minimizing the window.


```typescript
async maximizeWindow(windowId: number): Promise<boolean>
```

**Parameters:**
- `windowId` (number): The ID of the window to maximize.

**Returns:**
- `Promise<boolean>`: A promise that resolves to true if the operation was successful, false otherwise.

**Throws:**
- `APIError`: If there's an error maximizing the window.


```typescript
async restoreWindow(windowId: number): Promise<boolean>
```

**Parameters:**
- `windowId` (number): The ID of the window to restore.

**Returns:**
- `Promise<boolean>`: A promise that resolves to true if the operation was successful, false otherwise.

**Throws:**
- `APIError`: If there's an error restoring the window.


```typescript
async fullscreenWindow(windowId: number): Promise<boolean>
```

**Parameters:**
- `windowId` (number): The ID of the window to make fullscreen.

**Returns:**
- `Promise<boolean>`: A promise that resolves to true if the operation was successful, false otherwise.

**Throws:**
- `APIError`: If there's an error making the window fullscreen.


```typescript
async resizeWindow(windowId: number, width: number, height: number): Promise<boolean>
```

**Parameters:**
- `windowId` (number): The ID of the window to resize.
- `width` (number): The new width of the window.
- `height` (number): The new height of the window.

**Returns:**
- `Promise<boolean>`: A promise that resolves to true if the operation was successful, false otherwise.

**Throws:**
- `APIError`: If there's an error resizing the window.


```typescript
async closeWindow(windowId: number): Promise<boolean>
```

**Parameters:**
- `windowId` (number): The ID of the window to close.

**Returns:**
- `Promise<boolean>`: A promise that resolves to true if the operation was successful, false otherwise.

**Throws:**
- `APIError`: If there's an error closing the window.


```typescript
async focusMode(on: boolean): Promise<boolean>
```

**Parameters:**
- `on` (boolean): True to enable focus mode, False to disable it.

**Returns:**
- `Promise<boolean>`: A promise that resolves to true if the operation was successful, false otherwise.

**Throws:**
- `APIError`: If there's an error setting focus mode.
