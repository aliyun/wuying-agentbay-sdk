# Computer API Reference

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

## Type BoolResult

```go
type BoolResult struct {
	models.ApiResponse
	Success		bool	`json:"success"`
	ErrorMessage	string	`json:"error_message"`
}
```

BoolResult represents a boolean operation result

## Type Computer

```go
type Computer struct {
	Session interface {
		GetAPIKey() string
		GetClient() *mcp.Client
		GetSessionId() string
		IsVpc() bool
		NetworkInterfaceIp() string
		HttpPort() string
		FindServerForTool(toolName string) string
		CallMcpTool(toolName string, args interface{}, autoGenSession ...bool) (*models.McpToolResult, error)
	}
}
```

Computer handles computer UI automation operations in the AgentBay cloud environment. Provides
comprehensive desktop automation capabilities including mouse, keyboard, window management,
application management, and screen operations.

### Methods

### ActivateWindow

```go
func (c *Computer) ActivateWindow(windowID int) (*WindowResult, error)
```

ActivateWindow activates the specified window

**Example:**

```go
client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
result, _ := client.Create(agentbay.NewCreateSessionParams().WithImageId("windows_latest"))
defer result.Session.Delete()
windowList, _ := result.Session.Computer.ListRootWindows()
activateResult, _ := result.Session.Computer.ActivateWindow(windowList.Windows[0].WindowID)
```

### ClickMouse

```go
func (c *Computer) ClickMouse(x, y int, button MouseButton) *BoolResult
```

ClickMouse clicks the mouse at the specified coordinates

**Example:**

```go
client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
result, _ := client.Create(agentbay.NewCreateSessionParams().WithImageId("windows_latest"))
defer result.Session.Delete()
clickResult := result.Session.Computer.ClickMouse(500, 300, computer.MouseButtonLeft)
```

### CloseWindow

```go
func (c *Computer) CloseWindow(windowID int) (*WindowResult, error)
```

CloseWindow closes the specified window

**Example:**

```go
client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
result, _ := client.Create(agentbay.NewCreateSessionParams().WithImageId("windows_latest"))
defer result.Session.Delete()
windowList, _ := result.Session.Computer.ListRootWindows()
closeResult, _ := result.Session.Computer.CloseWindow(windowList.Windows[0].WindowID)
```

### DragMouse

```go
func (c *Computer) DragMouse(fromX, fromY, toX, toY int, button MouseButton) *BoolResult
```

DragMouse drags the mouse from one point to another

**Example:**

```go
client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
result, _ := client.Create(agentbay.NewCreateSessionParams().WithImageId("windows_latest"))
defer result.Session.Delete()
dragResult := result.Session.Computer.DragMouse(100, 100, 300, 300, computer.MouseButtonLeft)
```

### FocusMode

```go
func (c *Computer) FocusMode(on bool) (*WindowResult, error)
```

FocusMode toggles focus mode on or off

**Example:**

```go
client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
result, _ := client.Create(agentbay.NewCreateSessionParams().WithImageId("windows_latest"))
defer result.Session.Delete()
focusResult, _ := result.Session.Computer.FocusMode(true)
```

### FullscreenWindow

```go
func (c *Computer) FullscreenWindow(windowID int) (*WindowResult, error)
```

FullscreenWindow makes the specified window fullscreen

### GetActiveWindow

```go
func (c *Computer) GetActiveWindow() (*WindowDetailResult, error)
```

GetActiveWindow gets the currently active window

**Example:**

```go
client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
result, _ := client.Create(agentbay.NewCreateSessionParams().WithImageId("windows_latest"))
defer result.Session.Delete()
windowResult, _ := result.Session.Computer.GetActiveWindow()
```

### GetCursorPosition

```go
func (c *Computer) GetCursorPosition() *CursorPosition
```

GetCursorPosition gets the current cursor position

**Example:**

```go
client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
result, _ := client.Create(agentbay.NewCreateSessionParams().WithImageId("windows_latest"))
defer result.Session.Delete()
position := result.Session.Computer.GetCursorPosition()
```

### GetInstalledApps

```go
func (c *Computer) GetInstalledApps(startMenu, desktop, ignoreSystemApps bool) (*InstalledAppListResult, error)
```

GetInstalledApps retrieves a list of installed applications

**Example:**

```go
client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
result, _ := client.Create(agentbay.NewCreateSessionParams().WithImageId("windows_latest"))
defer result.Session.Delete()
appsResult, err := result.Session.Computer.GetInstalledApps(true, true, true)
if err != nil {
	log.Fatal(err)
}
```

### GetScreenSize

```go
func (c *Computer) GetScreenSize() *ScreenSize
```

GetScreenSize gets the size of the primary screen

**Example:**

```go
client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
result, _ := client.Create(agentbay.NewCreateSessionParams().WithImageId("windows_latest"))
defer result.Session.Delete()
screenSize := result.Session.Computer.GetScreenSize()
```

### InputText

```go
func (c *Computer) InputText(text string) *BoolResult
```

InputText inputs text into the active field

**Example:**

```go
client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
result, _ := client.Create(agentbay.NewCreateSessionParams().WithImageId("windows_latest"))
defer result.Session.Delete()
inputResult := result.Session.Computer.InputText("Hello World")
```

### ListRootWindows

```go
func (c *Computer) ListRootWindows(timeoutMs ...int) (*WindowListResult, error)
```

ListRootWindows lists all root windows

### ListVisibleApps

```go
func (c *Computer) ListVisibleApps() (*ProcessListResult, error)
```

ListVisibleApps lists all applications with visible windows

**Example:**

```go
client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
result, _ := client.Create(agentbay.NewCreateSessionParams().WithImageId("windows_latest"))
defer result.Session.Delete()
processResult, err := result.Session.Computer.ListVisibleApps()
if err != nil {
	log.Fatal(err)
}
```

### MaximizeWindow

```go
func (c *Computer) MaximizeWindow(windowID int) (*WindowResult, error)
```

MaximizeWindow maximizes the specified window

**Example:**

```go
client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
result, _ := client.Create(agentbay.NewCreateSessionParams().WithImageId("windows_latest"))
defer result.Session.Delete()
windowList, _ := result.Session.Computer.ListRootWindows()
maxResult, _ := result.Session.Computer.MaximizeWindow(windowList.Windows[0].WindowID)
```

### MinimizeWindow

```go
func (c *Computer) MinimizeWindow(windowID int) (*WindowResult, error)
```

MinimizeWindow minimizes the specified window

**Example:**

```go
client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
result, _ := client.Create(agentbay.NewCreateSessionParams().WithImageId("windows_latest"))
defer result.Session.Delete()
windowList, _ := result.Session.Computer.ListRootWindows()
minResult, _ := result.Session.Computer.MinimizeWindow(windowList.Windows[0].WindowID)
```

### MoveMouse

```go
func (c *Computer) MoveMouse(x, y int) *BoolResult
```

MoveMouse moves the mouse cursor to specific coordinates

**Example:**

```go
client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
result, _ := client.Create(agentbay.NewCreateSessionParams().WithImageId("windows_latest"))
defer result.Session.Delete()
moveResult := result.Session.Computer.MoveMouse(300, 200)
```

### PressKeys

```go
func (c *Computer) PressKeys(keys []string, hold bool) *BoolResult
```

PressKeys presses multiple keyboard keys simultaneously

**Example:**

```go
client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
result, _ := client.Create(agentbay.NewCreateSessionParams().WithImageId("windows_latest"))
defer result.Session.Delete()
pressResult := result.Session.Computer.PressKeys([]string{"Ctrl", "c"}, false)
```

### ReleaseKeys

```go
func (c *Computer) ReleaseKeys(keys []string) *BoolResult
```

ReleaseKeys releases multiple keyboard keys

**Example:**

```go
client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
result, _ := client.Create(agentbay.NewCreateSessionParams().WithImageId("windows_latest"))
defer result.Session.Delete()
result.Session.Computer.PressKeys([]string{"Shift"}, true)
releaseResult := result.Session.Computer.ReleaseKeys([]string{"Shift"})
```

### ResizeWindow

```go
func (c *Computer) ResizeWindow(windowID int, width int, height int) (*WindowResult, error)
```

ResizeWindow resizes the specified window

### RestoreWindow

```go
func (c *Computer) RestoreWindow(windowID int) (*WindowResult, error)
```

RestoreWindow restores the specified window

### Screenshot

```go
func (c *Computer) Screenshot() *ScreenshotResult
```

Screenshot takes a screenshot of the current screen

**Example:**

```go
client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
result, _ := client.Create(agentbay.NewCreateSessionParams().WithImageId("windows_latest"))
defer result.Session.Delete()
screenshot := result.Session.Computer.Screenshot()
```

### Scroll

```go
func (c *Computer) Scroll(x, y int, direction ScrollDirection, amount int) *BoolResult
```

Scroll scrolls the mouse wheel at specific coordinates

**Example:**

```go
client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
result, _ := client.Create(agentbay.NewCreateSessionParams().WithImageId("windows_latest"))
defer result.Session.Delete()
scrollResult := result.Session.Computer.Scroll(400, 300, computer.ScrollDirectionDown, 5)
```

### StartApp

```go
func (c *Computer) StartApp(startCmd, workDirectory, activity string) (*ProcessListResult, error)
```

StartApp starts the specified application

**Example:**

```go
client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
result, _ := client.Create(agentbay.NewCreateSessionParams().WithImageId("windows_latest"))
defer result.Session.Delete()
processResult, err := result.Session.Computer.StartApp("notepad.exe", "", "")
if err != nil {
	log.Fatal(err)
}
```

### StopAppByCmd

```go
func (c *Computer) StopAppByCmd(stopCmd string) *BoolResult
```

StopAppByCmd stops an application using the provided stop command

**Example:**

```go
client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
result, _ := client.Create(agentbay.NewCreateSessionParams().WithImageId("windows_latest"))
defer result.Session.Delete()
stopResult := result.Session.Computer.StopAppByCmd("taskkill /F /IM notepad.exe")
```

### StopAppByPID

```go
func (c *Computer) StopAppByPID(pid int) *BoolResult
```

StopAppByPID stops an application by process ID

**Example:**

```go
client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
result, _ := client.Create(agentbay.NewCreateSessionParams().WithImageId("windows_latest"))
defer result.Session.Delete()
stopResult := result.Session.Computer.StopAppByPID(1234)
```

### StopAppByPName

```go
func (c *Computer) StopAppByPName(pname string) *BoolResult
```

StopAppByPName stops an application by process name

**Example:**

```go
client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
result, _ := client.Create(agentbay.NewCreateSessionParams().WithImageId("windows_latest"))
defer result.Session.Delete()
stopResult := result.Session.Computer.StopAppByPName("notepad.exe")
```

### Related Functions

### NewComputer

```go
func NewComputer(session interface {
	GetAPIKey() string
	GetClient() *mcp.Client
	GetSessionId() string
	IsVpc() bool
	NetworkInterfaceIp() string
	HttpPort() string
	FindServerForTool(toolName string) string
	CallMcpTool(toolName string, args interface{}, autoGenSession ...bool) (*models.McpToolResult, error)
}) *Computer
```

NewComputer creates a new Computer instance

## Type CursorPosition

```go
type CursorPosition struct {
	models.ApiResponse
	X		int	`json:"x"`
	Y		int	`json:"y"`
	ErrorMessage	string	`json:"error_message"`
}
```

CursorPosition represents the cursor position on screen

## Type InstalledApp

```go
type InstalledApp struct {
	Name		string	`json:"name"`
	StartCmd	string	`json:"start_cmd"`
	StopCmd		string	`json:"stop_cmd,omitempty"`
	WorkDirectory	string	`json:"work_directory,omitempty"`
}
```

InstalledApp represents an installed application

## Type InstalledAppListResult

```go
type InstalledAppListResult struct {
	models.ApiResponse
	Apps		[]InstalledApp	`json:"apps"`
	ErrorMessage	string		`json:"error_message"`
}
```

InstalledAppListResult wraps installed app list and RequestID

## Type MouseButton

```go
type MouseButton string
```

MouseButton represents mouse button types

## Type Process

```go
type Process struct {
	PName	string	`json:"pname"`
	PID	int	`json:"pid"`
	CmdLine	string	`json:"cmdline,omitempty"`
}
```

Process represents a running process

## Type ProcessListResult

```go
type ProcessListResult struct {
	models.ApiResponse
	Processes	[]Process	`json:"processes"`
	ErrorMessage	string		`json:"error_message"`
}
```

ProcessListResult wraps process list and RequestID

## Type ScreenSize

```go
type ScreenSize struct {
	models.ApiResponse
	Width			int	`json:"width"`
	Height			int	`json:"height"`
	DpiScalingFactor	float64	`json:"dpiScalingFactor"`
	ErrorMessage		string	`json:"error_message"`
}
```

ScreenSize represents the screen dimensions

## Type ScreenshotResult

```go
type ScreenshotResult struct {
	models.ApiResponse
	Data		string	`json:"data"`
	ErrorMessage	string	`json:"error_message"`
}
```

ScreenshotResult represents the result of a screenshot operation

## Type ScrollDirection

```go
type ScrollDirection string
```

ScrollDirection represents scroll directions

## Type Window

```go
type Window struct {
	WindowID		int		`json:"window_id"`
	Title			string		`json:"title"`
	AbsoluteUpperLeftX	int		`json:"absolute_upper_left_x,omitempty"`
	AbsoluteUpperLeftY	int		`json:"absolute_upper_left_y,omitempty"`
	Width			int		`json:"width,omitempty"`
	Height			int		`json:"height,omitempty"`
	PID			int		`json:"pid,omitempty"`
	PName			string		`json:"pname,omitempty"`
	ChildWindows		[]Window	`json:"child_windows,omitempty"`
}
```

Window represents a window in the system

## Type WindowDetailResult

```go
type WindowDetailResult struct {
	models.ApiResponse
	Window	*Window
}
```

WindowDetailResult represents the result of getting window details

## Type WindowInfo

```go
type WindowInfo struct {
	WindowID	int	`json:"window_id"`
	Title		string	`json:"title"`
	PID		int	`json:"pid"`
	PName		string	`json:"pname"`
}
```

WindowInfo represents window information

## Type WindowListResult

```go
type WindowListResult struct {
	models.ApiResponse
	Windows	[]*WindowInfo
}
```

WindowListResult represents the result of listing windows

## Type WindowResult

```go
type WindowResult struct {
	models.ApiResponse
	Success	bool
}
```

WindowResult represents the result of a window action

## Best Practices

1. Verify screen coordinates before mouse operations
2. Use appropriate delays between UI interactions
3. Handle window focus changes properly
4. Take screenshots for verification and debugging
5. Use keyboard shortcuts for efficient automation
6. Clean up windows and applications after automation

---

*Documentation generated automatically from Go source code.*
