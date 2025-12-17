package computer

import (
	"encoding/json"
	"fmt"

	mcp "github.com/aliyun/wuying-agentbay-sdk/golang/api/client"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/models"
)

// MouseButton represents mouse button types
type MouseButton string

const (
	MouseButtonLeft       MouseButton = "left"
	MouseButtonRight      MouseButton = "right"
	MouseButtonMiddle     MouseButton = "middle"
	MouseButtonDoubleLeft MouseButton = "double_left"
)

// ScrollDirection represents scroll directions
type ScrollDirection string

const (
	ScrollDirectionUp    ScrollDirection = "up"
	ScrollDirectionDown  ScrollDirection = "down"
	ScrollDirectionLeft  ScrollDirection = "left"
	ScrollDirectionRight ScrollDirection = "right"
)

// Window represents a window in the system
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

// WindowInfo represents window information
type WindowInfo struct {
	WindowID int    `json:"window_id"`
	Title    string `json:"title"`
	PID      int    `json:"pid"`
	PName    string `json:"pname"`
}

// WindowListResult represents the result of listing windows
type WindowListResult struct {
	models.ApiResponse
	Windows []*WindowInfo
}

// WindowDetailResult represents the result of getting window details
type WindowDetailResult struct {
	models.ApiResponse
	Window *Window
}

// WindowResult represents the result of a window action
type WindowResult struct {
	models.ApiResponse
	Success bool
}

// CursorPosition represents the cursor position on screen
type CursorPosition struct {
	models.ApiResponse
	X            int    `json:"x"`
	Y            int    `json:"y"`
	ErrorMessage string `json:"error_message"`
}

// ScreenSize represents the screen dimensions
type ScreenSize struct {
	models.ApiResponse
	Width            int     `json:"width"`
	Height           int     `json:"height"`
	DpiScalingFactor float64 `json:"dpiScalingFactor"`
	ErrorMessage     string  `json:"error_message"`
}

// ScreenshotResult represents the result of a screenshot operation
type ScreenshotResult struct {
	models.ApiResponse
	Data         string `json:"data"`
	ErrorMessage string `json:"error_message"`
}

// BoolResult represents a boolean operation result
type BoolResult struct {
	models.ApiResponse
	Success      bool   `json:"success"`
	ErrorMessage string `json:"error_message"`
}

// Computer handles computer UI automation operations in the AgentBay cloud environment.
// Provides comprehensive desktop automation capabilities including mouse, keyboard,
// window management, application management, and screen operations.
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

// NewComputer creates a new Computer instance
func NewComputer(session interface {
	GetAPIKey() string
	GetClient() *mcp.Client
	GetSessionId() string
	IsVpc() bool
	NetworkInterfaceIp() string
	HttpPort() string
	FindServerForTool(toolName string) string
	CallMcpTool(toolName string, args interface{}, autoGenSession ...bool) (*models.McpToolResult, error)
}) *Computer {
	return &Computer{Session: session}
}

// ClickMouse clicks the mouse at the specified coordinates
//
// Example:
//
//	client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
//	result, _ := client.Create(agentbay.NewCreateSessionParams().WithImageId("windows_latest"))
//	defer result.Session.Delete()
//	clickResult := result.Session.Computer.ClickMouse(500, 300, computer.MouseButtonLeft)
func (c *Computer) ClickMouse(x, y int, button MouseButton) *BoolResult {
	// Validate button parameter
	validButtons := []MouseButton{MouseButtonLeft, MouseButtonRight, MouseButtonMiddle, MouseButtonDoubleLeft}
	isValid := false
	for _, validButton := range validButtons {
		if button == validButton {
			isValid = true
			break
		}
	}
	if !isValid {
		return &BoolResult{
			ApiResponse: models.ApiResponse{
				RequestID: "",
			},
			Success:      false,
			ErrorMessage: fmt.Sprintf("invalid button: %s. Valid options: %v", button, validButtons),
		}
	}

	args := map[string]interface{}{
		"x":      x,
		"y":      y,
		"button": string(button),
	}

	result, err := c.Session.CallMcpTool("click_mouse", args)
	if err != nil {
		return &BoolResult{
			ApiResponse: models.ApiResponse{
				RequestID: "",
			},
			Success:      false,
			ErrorMessage: fmt.Sprintf("failed to call click_mouse: %v", err),
		}
	}

	return &BoolResult{
		ApiResponse: models.ApiResponse{
			RequestID: result.RequestID,
		},
		Success:      result.Success,
		ErrorMessage: result.ErrorMessage,
	}
}

// MoveMouse moves the mouse cursor to specific coordinates
//
// Example:
//
//	client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
//	result, _ := client.Create(agentbay.NewCreateSessionParams().WithImageId("windows_latest"))
//	defer result.Session.Delete()
//	moveResult := result.Session.Computer.MoveMouse(300, 200)
func (c *Computer) MoveMouse(x, y int) *BoolResult {
	args := map[string]interface{}{
		"x": x,
		"y": y,
	}

	result, err := c.Session.CallMcpTool("move_mouse", args)
	if err != nil {
		return &BoolResult{
			ApiResponse: models.ApiResponse{
				RequestID: "",
			},
			Success:      false,
			ErrorMessage: fmt.Sprintf("failed to call move_mouse: %v", err),
		}
	}

	return &BoolResult{
		ApiResponse: models.ApiResponse{
			RequestID: result.RequestID,
		},
		Success:      result.Success,
		ErrorMessage: result.ErrorMessage,
	}
}

// DragMouse drags the mouse from one point to another
//
// Example:
//
//	client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
//	result, _ := client.Create(agentbay.NewCreateSessionParams().WithImageId("windows_latest"))
//	defer result.Session.Delete()
//	dragResult := result.Session.Computer.DragMouse(100, 100, 300, 300, computer.MouseButtonLeft)
func (c *Computer) DragMouse(fromX, fromY, toX, toY int, button MouseButton) *BoolResult {
	// Validate button parameter
	validButtons := []MouseButton{MouseButtonLeft, MouseButtonRight, MouseButtonMiddle}
	isValid := false
	for _, validButton := range validButtons {
		if button == validButton {
			isValid = true
			break
		}
	}
	if !isValid {
		return &BoolResult{
			ApiResponse: models.ApiResponse{
				RequestID: "",
			},
			Success:      false,
			ErrorMessage: fmt.Sprintf("invalid button: %s. Valid options: %v", button, validButtons),
		}
	}

	args := map[string]interface{}{
		"from_x": fromX,
		"from_y": fromY,
		"to_x":   toX,
		"to_y":   toY,
		"button": string(button),
	}

	result, err := c.Session.CallMcpTool("drag_mouse", args)
	if err != nil {
		return &BoolResult{
			ApiResponse: models.ApiResponse{
				RequestID: "",
			},
			Success:      false,
			ErrorMessage: fmt.Sprintf("failed to call drag_mouse: %v", err),
		}
	}

	return &BoolResult{
		ApiResponse: models.ApiResponse{
			RequestID: result.RequestID,
		},
		Success:      result.Success,
		ErrorMessage: result.ErrorMessage,
	}
}

// Scroll scrolls the mouse wheel at specific coordinates
//
// Example:
//
//	client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
//	result, _ := client.Create(agentbay.NewCreateSessionParams().WithImageId("windows_latest"))
//	defer result.Session.Delete()
//	scrollResult := result.Session.Computer.Scroll(400, 300, computer.ScrollDirectionDown, 5)
func (c *Computer) Scroll(x, y int, direction ScrollDirection, amount int) *BoolResult {
	// Validate direction parameter
	validDirections := []ScrollDirection{ScrollDirectionUp, ScrollDirectionDown, ScrollDirectionLeft, ScrollDirectionRight}
	isValid := false
	for _, validDirection := range validDirections {
		if direction == validDirection {
			isValid = true
			break
		}
	}
	if !isValid {
		return &BoolResult{
			ApiResponse: models.ApiResponse{
				RequestID: "",
			},
			Success:      false,
			ErrorMessage: fmt.Sprintf("invalid direction: %s. Valid options: %v", direction, validDirections),
		}
	}

	args := map[string]interface{}{
		"x":         x,
		"y":         y,
		"direction": string(direction),
		"amount":    amount,
	}

	result, err := c.Session.CallMcpTool("scroll", args)
	if err != nil {
		return &BoolResult{
			ApiResponse: models.ApiResponse{
				RequestID: "",
			},
			Success:      false,
			ErrorMessage: fmt.Sprintf("failed to call scroll: %v", err),
		}
	}

	return &BoolResult{
		ApiResponse: models.ApiResponse{
			RequestID: result.RequestID,
		},
		Success:      result.Success,
		ErrorMessage: result.ErrorMessage,
	}
}

// GetCursorPosition gets the current cursor position
//
// Example:
//
//	client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
//	result, _ := client.Create(agentbay.NewCreateSessionParams().WithImageId("windows_latest"))
//	defer result.Session.Delete()
//	position := result.Session.Computer.GetCursorPosition()
func (c *Computer) GetCursorPosition() *CursorPosition {
	args := map[string]interface{}{}

	result, err := c.Session.CallMcpTool("get_cursor_position", args)
	if err != nil {
		return &CursorPosition{
			ApiResponse: models.ApiResponse{
				RequestID: "",
			},
			ErrorMessage: fmt.Sprintf("failed to call get_cursor_position: %v", err),
		}
	}

	if !result.Success {
		return &CursorPosition{
			ApiResponse: models.ApiResponse{
				RequestID: result.RequestID,
			},
			ErrorMessage: result.ErrorMessage,
		}
	}

	// Parse cursor position from JSON
	var position struct {
		X int `json:"x"`
		Y int `json:"y"`
	}
	if err := json.Unmarshal([]byte(result.Data), &position); err != nil {
		return &CursorPosition{
			ApiResponse: models.ApiResponse{
				RequestID: result.RequestID,
			},
			ErrorMessage: fmt.Sprintf("failed to parse cursor position: %v", err),
		}
	}

	return &CursorPosition{
		ApiResponse: models.ApiResponse{
			RequestID: result.RequestID,
		},
		X:            position.X,
		Y:            position.Y,
		ErrorMessage: result.ErrorMessage,
	}
}

// InputText inputs text into the active field
//
// Example:
//
//	client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
//	result, _ := client.Create(agentbay.NewCreateSessionParams().WithImageId("windows_latest"))
//	defer result.Session.Delete()
//	inputResult := result.Session.Computer.InputText("Hello World")
func (c *Computer) InputText(text string) *BoolResult {
	args := map[string]interface{}{
		"text": text,
	}

	result, err := c.Session.CallMcpTool("input_text", args)
	if err != nil {
		return &BoolResult{
			ApiResponse: models.ApiResponse{
				RequestID: "",
			},
			Success:      false,
			ErrorMessage: fmt.Sprintf("failed to call input_text: %v", err),
		}
	}

	return &BoolResult{
		ApiResponse: models.ApiResponse{
			RequestID: result.RequestID,
		},
		Success:      result.Success,
		ErrorMessage: result.ErrorMessage,
	}
}

// PressKeys presses multiple keyboard keys simultaneously
//
// Example:
//
//	client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
//	result, _ := client.Create(agentbay.NewCreateSessionParams().WithImageId("windows_latest"))
//	defer result.Session.Delete()
//	pressResult := result.Session.Computer.PressKeys([]string{"Ctrl", "c"}, false)
func (c *Computer) PressKeys(keys []string, hold bool) *BoolResult {
	args := map[string]interface{}{
		"keys": keys,
		"hold": hold,
	}

	result, err := c.Session.CallMcpTool("press_keys", args)
	if err != nil {
		return &BoolResult{
			ApiResponse: models.ApiResponse{
				RequestID: "",
			},
			Success:      false,
			ErrorMessage: fmt.Sprintf("failed to call press_keys: %v", err),
		}
	}

	return &BoolResult{
		ApiResponse: models.ApiResponse{
			RequestID: result.RequestID,
		},
		Success:      result.Success,
		ErrorMessage: result.ErrorMessage,
	}
}

// ReleaseKeys releases multiple keyboard keys
//
// Example:
//
//	client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
//	result, _ := client.Create(agentbay.NewCreateSessionParams().WithImageId("windows_latest"))
//	defer result.Session.Delete()
//	result.Session.Computer.PressKeys([]string{"Shift"}, true)
//	releaseResult := result.Session.Computer.ReleaseKeys([]string{"Shift"})
func (c *Computer) ReleaseKeys(keys []string) *BoolResult {
	args := map[string]interface{}{
		"keys": keys,
	}

	result, err := c.Session.CallMcpTool("release_keys", args)
	if err != nil {
		return &BoolResult{
			ApiResponse: models.ApiResponse{
				RequestID: "",
			},
			Success:      false,
			ErrorMessage: fmt.Sprintf("failed to call release_keys: %v", err),
		}
	}

	return &BoolResult{
		ApiResponse: models.ApiResponse{
			RequestID: result.RequestID,
		},
		Success:      result.Success,
		ErrorMessage: result.ErrorMessage,
	}
}

// GetScreenSize gets the size of the primary screen
//
// Example:
//
//	client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
//	result, _ := client.Create(agentbay.NewCreateSessionParams().WithImageId("windows_latest"))
//	defer result.Session.Delete()
//	screenSize := result.Session.Computer.GetScreenSize()
func (c *Computer) GetScreenSize() *ScreenSize {
	args := map[string]interface{}{}

	result, err := c.Session.CallMcpTool("get_screen_size", args)
	if err != nil {
		return &ScreenSize{
			ApiResponse: models.ApiResponse{
				RequestID: "",
			},
			ErrorMessage: fmt.Sprintf("failed to call get_screen_size: %v", err),
		}
	}

	if !result.Success {
		return &ScreenSize{
			ApiResponse: models.ApiResponse{
				RequestID: result.RequestID,
			},
			ErrorMessage: result.ErrorMessage,
		}
	}

	// Parse screen size from JSON
	var size struct {
		Width            int     `json:"width"`
		Height           int     `json:"height"`
		DpiScalingFactor float64 `json:"dpiScalingFactor"`
	}
	if err := json.Unmarshal([]byte(result.Data), &size); err != nil {
		return &ScreenSize{
			ApiResponse: models.ApiResponse{
				RequestID: result.RequestID,
			},
			ErrorMessage: fmt.Sprintf("failed to parse screen size: %v", err),
		}
	}

	return &ScreenSize{
		ApiResponse: models.ApiResponse{
			RequestID: result.RequestID,
		},
		Width:            size.Width,
		Height:           size.Height,
		DpiScalingFactor: size.DpiScalingFactor,
		ErrorMessage:     result.ErrorMessage,
	}
}

// Screenshot takes a screenshot of the current screen
//
// Example:
//
//	client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
//	result, _ := client.Create(agentbay.NewCreateSessionParams().WithImageId("windows_latest"))
//	defer result.Session.Delete()
//	screenshot := result.Session.Computer.Screenshot()
func (c *Computer) Screenshot() *ScreenshotResult {
	args := map[string]interface{}{}

	result, err := c.Session.CallMcpTool("system_screenshot", args)
	if err != nil {
		return &ScreenshotResult{
			ApiResponse: models.ApiResponse{
				RequestID: "",
			},
			ErrorMessage: fmt.Sprintf("failed to call system_screenshot: %v", err),
		}
	}

	return &ScreenshotResult{
		ApiResponse: models.ApiResponse{
			RequestID: result.RequestID,
		},
		Data:         result.Data,
		ErrorMessage: result.ErrorMessage,
	}
}

// ListRootWindows lists all root windows
func (c *Computer) ListRootWindows(timeoutMs ...int) (*WindowListResult, error) {
	args := map[string]interface{}{}

	result, err := c.Session.CallMcpTool("list_root_windows", args)
	if err != nil {
		return nil, fmt.Errorf("error listing root windows: %w", err)
	}

	if !result.Success {
		return nil, fmt.Errorf("error listing root windows: %s", result.ErrorMessage)
	}

	var windows []*WindowInfo
	if err := json.Unmarshal([]byte(result.Data), &windows); err != nil {
		return nil, fmt.Errorf("failed to parse window information: %w", err)
	}

	return &WindowListResult{
		ApiResponse: models.ApiResponse{
			RequestID: result.RequestID,
		},
		Windows: windows,
	}, nil
}

// GetActiveWindow gets the currently active window
//
// Example:
//
//	client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
//	result, _ := client.Create(agentbay.NewCreateSessionParams().WithImageId("windows_latest"))
//	defer result.Session.Delete()
//	windowResult, _ := result.Session.Computer.GetActiveWindow()
func (c *Computer) GetActiveWindow() (*WindowDetailResult, error) {
	args := map[string]interface{}{}

	result, err := c.Session.CallMcpTool("get_active_window", args)
	if err != nil {
		return nil, fmt.Errorf("error getting active window: %w", err)
	}

	if !result.Success {
		return nil, fmt.Errorf("error getting active window: %s", result.ErrorMessage)
	}

	var window Window
	if err := json.Unmarshal([]byte(result.Data), &window); err != nil {
		return nil, fmt.Errorf("failed to parse window information: %w", err)
	}

	return &WindowDetailResult{
		ApiResponse: models.ApiResponse{
			RequestID: result.RequestID,
		},
		Window: &window,
	}, nil
}

// ActivateWindow activates the specified window
//
// Example:
//
//	client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
//	result, _ := client.Create(agentbay.NewCreateSessionParams().WithImageId("windows_latest"))
//	defer result.Session.Delete()
//	windowList, _ := result.Session.Computer.ListRootWindows()
//	activateResult, _ := result.Session.Computer.ActivateWindow(windowList.Windows[0].WindowID)
func (c *Computer) ActivateWindow(windowID int) (*WindowResult, error) {
	args := map[string]interface{}{
		"window_id": windowID,
	}

	result, err := c.Session.CallMcpTool("activate_window", args)
	if err != nil {
		return nil, fmt.Errorf("error activating window: %w", err)
	}

	return &WindowResult{
		ApiResponse: models.ApiResponse{
			RequestID: result.RequestID,
		},
		Success: result.Success,
	}, nil
}

// CloseWindow closes the specified window
//
// Example:
//
//	client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
//	result, _ := client.Create(agentbay.NewCreateSessionParams().WithImageId("windows_latest"))
//	defer result.Session.Delete()
//	windowList, _ := result.Session.Computer.ListRootWindows()
//	closeResult, _ := result.Session.Computer.CloseWindow(windowList.Windows[0].WindowID)
func (c *Computer) CloseWindow(windowID int) (*WindowResult, error) {
	args := map[string]interface{}{
		"window_id": windowID,
	}

	result, err := c.Session.CallMcpTool("close_window", args)
	if err != nil {
		return nil, fmt.Errorf("error closing window: %w", err)
	}

	return &WindowResult{
		ApiResponse: models.ApiResponse{
			RequestID: result.RequestID,
		},
		Success: result.Success,
	}, nil
}

// MaximizeWindow maximizes the specified window
//
// Example:
//
//	client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
//	result, _ := client.Create(agentbay.NewCreateSessionParams().WithImageId("windows_latest"))
//	defer result.Session.Delete()
//	windowList, _ := result.Session.Computer.ListRootWindows()
//	maxResult, _ := result.Session.Computer.MaximizeWindow(windowList.Windows[0].WindowID)
func (c *Computer) MaximizeWindow(windowID int) (*WindowResult, error) {
	args := map[string]interface{}{
		"window_id": windowID,
	}

	result, err := c.Session.CallMcpTool("maximize_window", args)
	if err != nil {
		return nil, fmt.Errorf("error maximizing window: %w", err)
	}

	return &WindowResult{
		ApiResponse: models.ApiResponse{
			RequestID: result.RequestID,
		},
		Success: result.Success,
	}, nil
}

// MinimizeWindow minimizes the specified window
//
// Example:
//
//	client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
//	result, _ := client.Create(agentbay.NewCreateSessionParams().WithImageId("windows_latest"))
//	defer result.Session.Delete()
//	windowList, _ := result.Session.Computer.ListRootWindows()
//	minResult, _ := result.Session.Computer.MinimizeWindow(windowList.Windows[0].WindowID)
func (c *Computer) MinimizeWindow(windowID int) (*WindowResult, error) {
	args := map[string]interface{}{
		"window_id": windowID,
	}

	result, err := c.Session.CallMcpTool("minimize_window", args)
	if err != nil {
		return nil, fmt.Errorf("error minimizing window: %w", err)
	}

	return &WindowResult{
		ApiResponse: models.ApiResponse{
			RequestID: result.RequestID,
		},
		Success: result.Success,
	}, nil
}

// RestoreWindow restores the specified window
func (c *Computer) RestoreWindow(windowID int) (*WindowResult, error) {
	args := map[string]interface{}{
		"window_id": windowID,
	}

	result, err := c.Session.CallMcpTool("restore_window", args)
	if err != nil {
		return nil, fmt.Errorf("error restoring window: %w", err)
	}

	return &WindowResult{
		ApiResponse: models.ApiResponse{
			RequestID: result.RequestID,
		},
		Success: result.Success,
	}, nil
}

// ResizeWindow resizes the specified window
func (c *Computer) ResizeWindow(windowID int, width int, height int) (*WindowResult, error) {
	args := map[string]interface{}{
		"window_id": windowID,
		"width":     width,
		"height":    height,
	}

	result, err := c.Session.CallMcpTool("resize_window", args)
	if err != nil {
		return nil, fmt.Errorf("error resizing window: %w", err)
	}

	return &WindowResult{
		ApiResponse: models.ApiResponse{
			RequestID: result.RequestID,
		},
		Success: result.Success,
	}, nil
}

// FullscreenWindow makes the specified window fullscreen
func (c *Computer) FullscreenWindow(windowID int) (*WindowResult, error) {
	args := map[string]interface{}{
		"window_id": windowID,
	}

	result, err := c.Session.CallMcpTool("fullscreen_window", args)
	if err != nil {
		return nil, fmt.Errorf("error making window fullscreen: %w", err)
	}

	return &WindowResult{
		ApiResponse: models.ApiResponse{
			RequestID: result.RequestID,
		},
		Success: result.Success,
	}, nil
}

// FocusMode toggles focus mode on or off
//
// Example:
//
//	client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
//	result, _ := client.Create(agentbay.NewCreateSessionParams().WithImageId("windows_latest"))
//	defer result.Session.Delete()
//	focusResult, _ := result.Session.Computer.FocusMode(true)
func (c *Computer) FocusMode(on bool) (*WindowResult, error) {
	args := map[string]interface{}{
		"on": on,
	}

	result, err := c.Session.CallMcpTool("focus_mode", args)
	if err != nil {
		return nil, fmt.Errorf("error toggling focus mode: %w", err)
	}

	return &WindowResult{
		ApiResponse: models.ApiResponse{
			RequestID: result.RequestID,
		},
		Success: result.Success,
	}, nil
}

// Process represents a running process
type Process struct {
	PName   string `json:"pname"`
	PID     int    `json:"pid"`
	CmdLine string `json:"cmdline,omitempty"`
}

// ProcessListResult wraps process list and RequestID
type ProcessListResult struct {
	models.ApiResponse
	Processes    []Process `json:"processes"`
	ErrorMessage string    `json:"error_message"`
}

// InstalledApp represents an installed application
type InstalledApp struct {
	Name          string `json:"name"`
	StartCmd      string `json:"start_cmd"`
	StopCmd       string `json:"stop_cmd,omitempty"`
	WorkDirectory string `json:"work_directory,omitempty"`
}

// InstalledAppListResult wraps installed app list and RequestID
type InstalledAppListResult struct {
	models.ApiResponse
	Apps         []InstalledApp `json:"apps"`
	ErrorMessage string         `json:"error_message"`
}

// StartApp starts the specified application
//
// Example:
//
//	client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
//	result, _ := client.Create(agentbay.NewCreateSessionParams().WithImageId("windows_latest"))
//	defer result.Session.Delete()
//	processResult, err := result.Session.Computer.StartApp("notepad.exe", "", "")
//	if err != nil {
//		log.Fatal(err)
//	}
func (c *Computer) StartApp(startCmd, workDirectory, activity string) (*ProcessListResult, error) {
	args := map[string]interface{}{
		"start_cmd": startCmd,
	}
	if workDirectory != "" {
		args["work_directory"] = workDirectory
	}
	if activity != "" {
		args["activity"] = activity
	}

	result, err := c.Session.CallMcpTool("start_app", args)
	if err != nil {
		return nil, fmt.Errorf("failed to call start_app: %w", err)
	}

	if !result.Success {
		return nil, fmt.Errorf("failed to start app: %s", result.ErrorMessage)
	}

	// Parse processes from JSON
	var processes []Process
	if err := json.Unmarshal([]byte(result.Data), &processes); err != nil {
		return nil, fmt.Errorf("failed to parse processes: %w", err)
	}

	return &ProcessListResult{
		ApiResponse: models.ApiResponse{
			RequestID: result.RequestID,
		},
		Processes: processes,
	}, nil
}

// GetInstalledApps retrieves a list of installed applications
//
// Example:
//
//	client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
//	result, _ := client.Create(agentbay.NewCreateSessionParams().WithImageId("windows_latest"))
//	defer result.Session.Delete()
//	appsResult, err := result.Session.Computer.GetInstalledApps(true, true, true)
//	if err != nil {
//		log.Fatal(err)
//	}
func (c *Computer) GetInstalledApps(startMenu, desktop, ignoreSystemApps bool) (*InstalledAppListResult, error) {
	args := map[string]interface{}{
		"start_menu":         startMenu,
		"desktop":            desktop,
		"ignore_system_apps": ignoreSystemApps,
	}

	result, err := c.Session.CallMcpTool("get_installed_apps", args)
	if err != nil {
		return nil, fmt.Errorf("failed to call get_installed_apps: %w", err)
	}

	if !result.Success {
		return nil, fmt.Errorf("failed to get installed apps: %s", result.ErrorMessage)
	}

	// Parse installed apps from JSON
	var apps []InstalledApp
	if err := json.Unmarshal([]byte(result.Data), &apps); err != nil {
		return nil, fmt.Errorf("failed to parse installed apps: %w", err)
	}

	return &InstalledAppListResult{
		ApiResponse: models.ApiResponse{
			RequestID: result.RequestID,
		},
		Apps: apps,
	}, nil
}

// ListVisibleApps lists all applications with visible windows
//
// Example:
//
//	client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
//	result, _ := client.Create(agentbay.NewCreateSessionParams().WithImageId("windows_latest"))
//	defer result.Session.Delete()
//	processResult, err := result.Session.Computer.ListVisibleApps()
//	if err != nil {
//		log.Fatal(err)
//	}
func (c *Computer) ListVisibleApps() (*ProcessListResult, error) {
	args := map[string]interface{}{}

	result, err := c.Session.CallMcpTool("list_visible_apps", args)
	if err != nil {
		return nil, fmt.Errorf("failed to call list_visible_apps: %w", err)
	}

	if !result.Success {
		return nil, fmt.Errorf("failed to list visible apps: %s", result.ErrorMessage)
	}

	// Parse processes from JSON
	var processes []Process
	if err := json.Unmarshal([]byte(result.Data), &processes); err != nil {
		return nil, fmt.Errorf("failed to parse processes: %w", err)
	}

	return &ProcessListResult{
		ApiResponse: models.ApiResponse{
			RequestID: result.RequestID,
		},
		Processes: processes,
	}, nil
}

// StopAppByPName stops an application by process name
//
// Example:
//
//	client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
//	result, _ := client.Create(agentbay.NewCreateSessionParams().WithImageId("windows_latest"))
//	defer result.Session.Delete()
//	stopResult := result.Session.Computer.StopAppByPName("notepad.exe")
func (c *Computer) StopAppByPName(pname string) *BoolResult {
	args := map[string]interface{}{
		"pname": pname,
	}

	result, err := c.Session.CallMcpTool("stop_app_by_pname", args)
	if err != nil {
		return &BoolResult{
			ApiResponse: models.ApiResponse{
				RequestID: "",
			},
			Success:      false,
			ErrorMessage: fmt.Sprintf("failed to call stop_app_by_pname: %v", err),
		}
	}

	return &BoolResult{
		ApiResponse: models.ApiResponse{
			RequestID: result.RequestID,
		},
		Success:      result.Success,
		ErrorMessage: result.ErrorMessage,
	}
}

// StopAppByPID stops an application by process ID
//
// Example:
//
//	client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
//	result, _ := client.Create(agentbay.NewCreateSessionParams().WithImageId("windows_latest"))
//	defer result.Session.Delete()
//	stopResult := result.Session.Computer.StopAppByPID(1234)
func (c *Computer) StopAppByPID(pid int) *BoolResult {
	args := map[string]interface{}{
		"pid": pid,
	}

	result, err := c.Session.CallMcpTool("stop_app_by_pid", args)
	if err != nil {
		return &BoolResult{
			ApiResponse: models.ApiResponse{
				RequestID: "",
			},
			Success:      false,
			ErrorMessage: fmt.Sprintf("failed to call stop_app_by_pid: %v", err),
		}
	}

	return &BoolResult{
		ApiResponse: models.ApiResponse{
			RequestID: result.RequestID,
		},
		Success:      result.Success,
		ErrorMessage: result.ErrorMessage,
	}
}

// StopAppByCmd stops an application using the provided stop command
//
// Example:
//
//	client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
//	result, _ := client.Create(agentbay.NewCreateSessionParams().WithImageId("windows_latest"))
//	defer result.Session.Delete()
//	stopResult := result.Session.Computer.StopAppByCmd("taskkill /F /IM notepad.exe")
func (c *Computer) StopAppByCmd(stopCmd string) *BoolResult {
	args := map[string]interface{}{
		"stop_cmd": stopCmd,
	}

	result, err := c.Session.CallMcpTool("stop_app_by_cmd", args)
	if err != nil {
		return &BoolResult{
			ApiResponse: models.ApiResponse{
				RequestID: "",
			},
			Success:      false,
			ErrorMessage: fmt.Sprintf("failed to call stop_app_by_cmd: %v", err),
		}
	}

	return &BoolResult{
		ApiResponse: models.ApiResponse{
			RequestID: result.RequestID,
		},
		Success:      result.Success,
		ErrorMessage: result.ErrorMessage,
	}
}
