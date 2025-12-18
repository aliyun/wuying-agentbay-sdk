# Class: Computer

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

## Table of contents


### Methods

- [activateWindow](#activatewindow)
- [clickMouse](#clickmouse)
- [closeWindow](#closewindow)
- [dragMouse](#dragmouse)
- [focusMode](#focusmode)
- [fullscreenWindow](#fullscreenwindow)
- [inputText](#inputtext)
- [listRootWindows](#listrootwindows)
- [listVisibleApps](#listvisibleapps)
- [maximizeWindow](#maximizewindow)
- [minimizeWindow](#minimizewindow)
- [moveMouse](#movemouse)
- [pressKeys](#presskeys)
- [releaseKeys](#releasekeys)
- [resizeWindow](#resizewindow)
- [restoreWindow](#restorewindow)
- [screenshot](#screenshot)
- [scroll](#scroll)
- [startApp](#startapp)
- [stopAppByCmd](#stopappbycmd)
- [stopAppByPID](#stopappbypid)
- [stopAppByPName](#stopappbypname)

## Methods

### activateWindow

▸ **activateWindow**(`windowId`): `Promise`\<`BoolResult`\>

Activates the specified window.

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `windowId` | `number` | ID of the window to activate |

#### Returns

`Promise`\<`BoolResult`\>

Promise resolving to result with success status

**`Example`**

```typescript
const agentBay = new AgentBay({ apiKey: 'your_api_key' });
const result = await agentBay.create({ imageId: 'windows_latest' });
if (result.success) {
  const windows = await result.session.computer.listRootWindows();
  await result.session.computer.activateWindow(windows.windows[0].id);
  await result.session.delete();
}
```

___

### clickMouse

▸ **clickMouse**(`x`, `y`, `button?`): `Promise`\<`OperationResult`\>

Click mouse at specified coordinates.

#### Parameters

| Name | Type | Default value | Description |
| :------ | :------ | :------ | :------ |
| `x` | `number` | `undefined` | X coordinate for the click |
| `y` | `number` | `undefined` | Y coordinate for the click |
| `button` | `string` | `MouseButton.LEFT` | Mouse button to click (default: 'left'). Valid values: 'left', 'right', 'middle', 'double_left' |

#### Returns

`Promise`\<`OperationResult`\>

Promise resolving to result with success status

**`Example`**

```typescript
const agentBay = new AgentBay({ apiKey: 'your_api_key' });
const result = await agentBay.create({ imageId: 'windows_latest' });
if (result.success) {
  const clickResult = await result.session.computer.clickMouse(100, 100, 'left');
  console.log('Clicked:', clickResult.success);
  await result.session.delete();
}
```

___

### closeWindow

▸ **closeWindow**(`windowId`): `Promise`\<`BoolResult`\>

Closes the specified window.

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `windowId` | `number` | ID of the window to close |

#### Returns

`Promise`\<`BoolResult`\>

Promise resolving to result with success status

**`Example`**

```typescript
const agentBay = new AgentBay({ apiKey: process.env.AGENTBAY_API_KEY });
const result = await agentBay.create({ imageId: 'windows_latest' });
if (result.success) {
  await result.session.computer.startApp('notepad.exe');
  const win = await result.session.computer.getActiveWindow();
  await result.session.computer.closeWindow(win.window!.id);
  await result.session.delete();
}
```

___

### dragMouse

▸ **dragMouse**(`fromX`, `fromY`, `toX`, `toY`, `button?`): `Promise`\<`OperationResult`\>

Drag mouse from one position to another.

#### Parameters

| Name | Type | Default value | Description |
| :------ | :------ | :------ | :------ |
| `fromX` | `number` | `undefined` | Starting X coordinate |
| `fromY` | `number` | `undefined` | Starting Y coordinate |
| `toX` | `number` | `undefined` | Ending X coordinate |
| `toY` | `number` | `undefined` | Ending Y coordinate |
| `button` | `string` | `MouseButton.LEFT` | Mouse button to use for drag (default: 'left'). Valid values: 'left', 'right', 'middle' |

#### Returns

`Promise`\<`OperationResult`\>

Promise resolving to result with success status

**`Example`**

```typescript
const agentBay = new AgentBay({ apiKey: process.env.AGENTBAY_API_KEY });
const result = await agentBay.create({ imageId: 'windows_latest' });
if (result.success) {
  const dragResult = await result.session.computer.dragMouse(100, 100, 300, 300, 'left');
  console.log('Dragged:', dragResult.success);
  await result.session.delete();
}
```

___

### focusMode

▸ **focusMode**(`on`): `Promise`\<`BoolResult`\>

Toggles focus mode on or off.

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `on` | `boolean` | Whether to enable (true) or disable (false) focus mode |

#### Returns

`Promise`\<`BoolResult`\>

Promise resolving to result with success status

**`Example`**

```typescript
const agentBay = new AgentBay({ apiKey: process.env.AGENTBAY_API_KEY });
const result = await agentBay.create({ imageId: 'windows_latest' });
if (result.success) {
  await result.session.computer.focusMode(true);
  await result.session.computer.focusMode(false);
  await result.session.delete();
}
```

___

### fullscreenWindow

▸ **fullscreenWindow**(`windowId`): `Promise`\<`BoolResult`\>

Makes the specified window fullscreen.

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `windowId` | `number` | ID of the window to make fullscreen |

#### Returns

`Promise`\<`BoolResult`\>

Promise resolving to result with success status

**`Example`**

```typescript
const agentBay = new AgentBay({ apiKey: process.env.AGENTBAY_API_KEY });
const result = await agentBay.create({ imageId: 'windows_latest' });
if (result.success) {
  await result.session.computer.startApp('notepad.exe');
  const win = await result.session.computer.getActiveWindow();
  await result.session.computer.fullscreenWindow(win.window!.id);
  await result.session.delete();
}
```

### inputText

▸ **inputText**(`text`): `Promise`\<`OperationResult`\>

Input text at the current cursor position.

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `text` | `string` | Text to input |

#### Returns

`Promise`\<`OperationResult`\>

Promise resolving to result with success status

**`Example`**

```typescript
const agentBay = new AgentBay({ apiKey: process.env.AGENTBAY_API_KEY });
const result = await agentBay.create({ imageId: 'windows_latest' });
if (result.success) {
  await result.session.computer.inputText('Hello AgentBay!');
  await result.session.delete();
}
```

___

### listRootWindows

▸ **listRootWindows**(`timeoutMs?`): `Promise`\<`WindowListResult`\>

Lists all root windows.

#### Parameters

| Name | Type | Default value | Description |
| :------ | :------ | :------ | :------ |
| `timeoutMs` | `number` | `3000` | Timeout in milliseconds (default: 3000) |

#### Returns

`Promise`\<`WindowListResult`\>

Promise resolving to result containing array of root windows

**`Example`**

```typescript
const agentBay = new AgentBay({ apiKey: process.env.AGENTBAY_API_KEY });
const result = await agentBay.create({ imageId: 'windows_latest' });
if (result.success) {
  const windows = await result.session.computer.listRootWindows();
  console.log(`Found ${windows.windows.length} windows`);
  await result.session.delete();
}
```

___

### listVisibleApps

▸ **listVisibleApps**(): `Promise`\<`ProcessListResult`\>

Lists all visible applications.

#### Returns

`Promise`\<`ProcessListResult`\>

Promise resolving to result containing array of visible application processes

**`Example`**

```typescript
const agentBay = new AgentBay({ apiKey: 'your_api_key' });
const result = await agentBay.create({ imageId: 'windows_latest' });
if (result.success) {
  const apps = await result.session.computer.listVisibleApps();
  console.log(`Found ${apps.data.length} visible apps`);
  await result.session.delete();
}
```

___

### maximizeWindow

▸ **maximizeWindow**(`windowId`): `Promise`\<`BoolResult`\>

Maximizes the specified window.

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `windowId` | `number` | ID of the window to maximize |

#### Returns

`Promise`\<`BoolResult`\>

Promise resolving to result with success status

**`Example`**

```typescript
const agentBay = new AgentBay({ apiKey: process.env.AGENTBAY_API_KEY });
const result = await agentBay.create({ imageId: 'windows_latest' });
if (result.success) {
  await result.session.computer.startApp('notepad.exe');
  const win = await result.session.computer.getActiveWindow();
  await result.session.computer.maximizeWindow(win.window!.id);
  await result.session.delete();
}
```

___

### minimizeWindow

▸ **minimizeWindow**(`windowId`): `Promise`\<`BoolResult`\>

Minimizes the specified window.

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `windowId` | `number` | ID of the window to minimize |

#### Returns

`Promise`\<`BoolResult`\>

Promise resolving to result with success status

**`Example`**

```typescript
const agentBay = new AgentBay({ apiKey: process.env.AGENTBAY_API_KEY });
const result = await agentBay.create({ imageId: 'windows_latest' });
if (result.success) {
  await result.session.computer.startApp('notepad.exe');
  const win = await result.session.computer.getActiveWindow();
  await result.session.computer.minimizeWindow(win.window!.id);
  await result.session.delete();
}
```

___

### moveMouse

▸ **moveMouse**(`x`, `y`): `Promise`\<`OperationResult`\>

Move mouse to specified coordinates.

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `x` | `number` | X coordinate to move to |
| `y` | `number` | Y coordinate to move to |

#### Returns

`Promise`\<`OperationResult`\>

Promise resolving to result with success status

**`Example`**

```typescript
const agentBay = new AgentBay({ apiKey: process.env.AGENTBAY_API_KEY });
const result = await agentBay.create({ imageId: 'windows_latest' });
if (result.success) {
  await result.session.computer.moveMouse(300, 400);
  const pos = await result.session.computer.getCursorPosition();
  console.log(`Position: (${pos.x}, ${pos.y})`);
  await result.session.delete();
}
```

___

### pressKeys

▸ **pressKeys**(`keys`, `hold?`): `Promise`\<`OperationResult`\>

Press one or more keys.

#### Parameters

| Name | Type | Default value | Description |
| :------ | :------ | :------ | :------ |
| `keys` | `string`[] | `undefined` | Array of key names to press |
| `hold` | `boolean` | `false` | Whether to hold the keys down (default: false) |

#### Returns

`Promise`\<`OperationResult`\>

Promise resolving to result with success status

**`Example`**

```typescript
const agentBay = new AgentBay({ apiKey: process.env.AGENTBAY_API_KEY });
const result = await agentBay.create({ imageId: 'windows_latest' });
if (result.success) {
  await result.session.computer.pressKeys(['Ctrl', 'c'], true);
  await result.session.computer.releaseKeys(['Ctrl', 'c']);
  await result.session.delete();
}
```

___

### releaseKeys

▸ **releaseKeys**(`keys`): `Promise`\<`OperationResult`\>

Release previously pressed keys.

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `keys` | `string`[] | Array of key names to release |

#### Returns

`Promise`\<`OperationResult`\>

Promise resolving to result with success status

**`Example`**

```typescript
const agentBay = new AgentBay({ apiKey: process.env.AGENTBAY_API_KEY });
const result = await agentBay.create({ imageId: 'windows_latest' });
if (result.success) {
  await result.session.computer.pressKeys(['Ctrl'], true);
  await result.session.computer.releaseKeys(['Ctrl']);
  await result.session.delete();
}
```

___

### resizeWindow

▸ **resizeWindow**(`windowId`, `width`, `height`): `Promise`\<`BoolResult`\>

Resizes the specified window.

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `windowId` | `number` | ID of the window to resize |
| `width` | `number` | New width of the window |
| `height` | `number` | New height of the window |

#### Returns

`Promise`\<`BoolResult`\>

Promise resolving to result with success status

**`Example`**

```typescript
const agentBay = new AgentBay({ apiKey: process.env.AGENTBAY_API_KEY });
const result = await agentBay.create({ imageId: 'windows_latest' });
if (result.success) {
  await result.session.computer.startApp('notepad.exe');
  const win = await result.session.computer.getActiveWindow();
  await result.session.computer.resizeWindow(win.window!.id, 800, 600);
  await result.session.delete();
}
```

___

### restoreWindow

▸ **restoreWindow**(`windowId`): `Promise`\<`BoolResult`\>

Restores the specified window.

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `windowId` | `number` | ID of the window to restore |

#### Returns

`Promise`\<`BoolResult`\>

Promise resolving to result with success status

**`Example`**

```typescript
const agentBay = new AgentBay({ apiKey: process.env.AGENTBAY_API_KEY });
const result = await agentBay.create({ imageId: 'windows_latest' });
if (result.success) {
  await result.session.computer.startApp('notepad.exe');
  const win = await result.session.computer.getActiveWindow();
  await result.session.computer.minimizeWindow(win.window!.id);
  await result.session.computer.restoreWindow(win.window!.id);
  await result.session.delete();
}
```

___

### screenshot

▸ **screenshot**(): `Promise`\<`ScreenshotResult`\>

Take a screenshot.

#### Returns

`Promise`\<`ScreenshotResult`\>

Promise resolving to result containing screenshot URL

**`Example`**

```typescript
const agentBay = new AgentBay({ apiKey: process.env.AGENTBAY_API_KEY });
const result = await agentBay.create({ imageId: 'windows_latest' });
if (result.success) {
  const screenshot = await result.session.computer.screenshot();
  console.log('Screenshot URL:', screenshot.data);
  await result.session.delete();
}
```

___

### scroll

▸ **scroll**(`x`, `y`, `direction?`, `amount?`): `Promise`\<`OperationResult`\>

Scroll at specified coordinates.

#### Parameters

| Name | Type | Default value | Description |
| :------ | :------ | :------ | :------ |
| `x` | `number` | `undefined` | X coordinate to scroll at |
| `y` | `number` | `undefined` | Y coordinate to scroll at |
| `direction` | `string` | `ScrollDirection.UP` | Scroll direction (default: 'up'). Valid values: 'up', 'down', 'left', 'right' |
| `amount` | `number` | `1` | Scroll amount (default: 1) |

#### Returns

`Promise`\<`OperationResult`\>

Promise resolving to result with success status

**`Example`**

```typescript
const agentBay = new AgentBay({ apiKey: process.env.AGENTBAY_API_KEY });
const result = await agentBay.create({ imageId: 'windows_latest' });
if (result.success) {
  await result.session.computer.scroll(400, 300, 'up', 3);
  await result.session.delete();
}
```

___

### startApp

▸ **startApp**(`startCmd`, `workDirectory?`, `activity?`): `Promise`\<`ProcessListResult`\>

Starts the specified application.

#### Parameters

| Name | Type | Default value | Description |
| :------ | :------ | :------ | :------ |
| `startCmd` | `string` | `undefined` | The command to start the application (e.g., 'notepad.exe', 'calculator:') |
| `workDirectory` | `string` | `""` | The working directory for the application (optional) |
| `activity` | `string` | `""` | The activity parameter (optional, primarily for mobile use) |

#### Returns

`Promise`\<`ProcessListResult`\>

Promise resolving to result containing array of started processes

**`Example`**

```typescript
const agentBay = new AgentBay({ apiKey: 'your_api_key' });
const result = await agentBay.create({ imageId: 'windows_latest' });
if (result.success) {
  const startResult = await result.session.computer.startApp('notepad.exe');
  console.log(`Started ${startResult.data.length} process(es)`);
  await result.session.delete();
}
```

___

### stopAppByCmd

▸ **stopAppByCmd**(`cmd`): `Promise`\<`BoolResult`\>

Stops an application by stop command.

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `cmd` | `string` | The command to stop the application |

#### Returns

`Promise`\<`BoolResult`\>

Promise resolving to result with success status

**`Example`**

```typescript
const agentBay = new AgentBay({ apiKey: 'your_api_key' });
const result = await agentBay.create({ imageId: 'windows_latest' });
if (result.success) {
  await result.session.computer.startApp('notepad.exe');
  await result.session.computer.stopAppByCmd('taskkill /IM notepad.exe /F');
  await result.session.delete();
}
```

___

### stopAppByPID

▸ **stopAppByPID**(`pid`): `Promise`\<`BoolResult`\>

Stops an application by process ID.

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `pid` | `number` | The process ID to stop |

#### Returns

`Promise`\<`BoolResult`\>

Promise resolving to result with success status

**`Example`**

```typescript
const agentBay = new AgentBay({ apiKey: 'your_api_key' });
const result = await agentBay.create({ imageId: 'windows_latest' });
if (result.success) {
  const startResult = await result.session.computer.startApp('notepad.exe');
  const pid = startResult.data[0].pid;
  await result.session.computer.stopAppByPID(pid);
  await result.session.delete();
}
```

___

### stopAppByPName

▸ **stopAppByPName**(`pname`): `Promise`\<`BoolResult`\>

Stops an application by process name.

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `pname` | `string` | The process name to stop (e.g., 'notepad.exe', 'chrome.exe') |

#### Returns

`Promise`\<`BoolResult`\>

Promise resolving to result with success status

**`Example`**

```typescript
const agentBay = new AgentBay({ apiKey: 'your_api_key' });
const result = await agentBay.create({ imageId: 'windows_latest' });
if (result.success) {
  await result.session.computer.startApp('notepad.exe');
  await result.session.computer.stopAppByPName('notepad.exe');
  await result.session.delete();
}
```

## Best Practices

1. Verify screen coordinates before mouse operations
2. Use appropriate delays between UI interactions
3. Handle window focus changes properly
4. Take screenshots for verification and debugging
5. Use keyboard shortcuts for efficient automation
6. Clean up windows and applications after automation

