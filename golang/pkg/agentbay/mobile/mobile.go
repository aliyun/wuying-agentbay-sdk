package mobile

import (
	"encoding/json"
	"fmt"

	mcp "github.com/aliyun/wuying-agentbay-sdk/golang/api/client"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/models"
)

// UIElement represents a UI element structure
type UIElement struct {
	Bounds      *UIBounds `json:"bounds,omitempty"`
	ClassName   string    `json:"className,omitempty"`
	ContentDesc string    `json:"contentDesc,omitempty"`
	ElementID   string    `json:"elementId,omitempty"`
	Package     string    `json:"package,omitempty"`
	ResourceID  string    `json:"resourceId,omitempty"`
	Text        string    `json:"text,omitempty"`
	Type        string    `json:"type,omitempty"`
}

// UIBounds represents the bounds of a UI element
type UIBounds struct {
	Bottom int `json:"bottom"`
	Left   int `json:"left"`
	Right  int `json:"right"`
	Top    int `json:"top"`
}

// UIElementsResult represents the result containing UI elements
type UIElementsResult struct {
	models.ApiResponse
	Elements     []*UIElement `json:"elements"`
	ErrorMessage string       `json:"error_message"`
}

// InstalledApp represents an installed application
type InstalledApp struct {
	Name          string `json:"name"`
	StartCmd      string `json:"start_cmd"`
	StopCmd       string `json:"stop_cmd,omitempty"`
	WorkDirectory string `json:"work_directory,omitempty"`
}

// Process represents a running process
type Process struct {
	PName   string `json:"pname"`
	PID     int    `json:"pid"`
	CmdLine string `json:"cmdline,omitempty"`
}

// InstalledAppListResult wraps installed app list and RequestID
type InstalledAppListResult struct {
	models.ApiResponse
	Apps         []InstalledApp `json:"apps"`
	ErrorMessage string         `json:"error_message"`
}

// ProcessListResult wraps process list and RequestID
type ProcessListResult struct {
	models.ApiResponse
	Processes    []Process `json:"processes"`
	ErrorMessage string    `json:"error_message"`
}

// BoolResult represents a boolean operation result
type BoolResult struct {
	models.ApiResponse
	Success      bool   `json:"success"`
	ErrorMessage string `json:"error_message"`
}

// ScreenshotResult represents the result of a screenshot operation
type ScreenshotResult struct {
	models.ApiResponse
	Data         string `json:"data"`
	ErrorMessage string `json:"error_message"`
}

// Mobile handles mobile UI automation operations in the AgentBay cloud environment.
// Provides touch operations, UI element interactions, application management, and screenshot capabilities.
type Mobile struct {
	Session interface {
		GetAPIKey() string
		GetClient() *mcp.Client
		GetSessionId() string
		IsVpc() bool
		NetworkInterfaceIp() string
		HttpPort() string
		FindServerForTool(toolName string) string
		CallMcpTool(toolName string, args interface{}) (*models.McpToolResult, error)
	}
}

// NewMobile creates a new Mobile instance
func NewMobile(session interface {
	GetAPIKey() string
	GetClient() *mcp.Client
	GetSessionId() string
	IsVpc() bool
	NetworkInterfaceIp() string
	HttpPort() string
	FindServerForTool(toolName string) string
	CallMcpTool(toolName string, args interface{}) (*models.McpToolResult, error)
}) *Mobile {
	return &Mobile{Session: session}
}

// Tap taps on the screen at specific coordinates
func (m *Mobile) Tap(x, y int) *BoolResult {
	args := map[string]interface{}{
		"x": x,
		"y": y,
	}

	result, err := m.Session.CallMcpTool("tap", args)
	if err != nil {
		return &BoolResult{
			ApiResponse: models.ApiResponse{
				RequestID: "",
			},
			Success:      false,
			ErrorMessage: fmt.Sprintf("failed to call tap: %v", err),
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

// Swipe performs a swipe gesture on the screen
func (m *Mobile) Swipe(startX, startY, endX, endY, durationMs int) *BoolResult {
	args := map[string]interface{}{
		"start_x":     startX,
		"start_y":     startY,
		"end_x":       endX,
		"end_y":       endY,
		"duration_ms": durationMs,
	}

	result, err := m.Session.CallMcpTool("swipe", args)
	if err != nil {
		return &BoolResult{
			ApiResponse: models.ApiResponse{
				RequestID: "",
			},
			Success:      false,
			ErrorMessage: fmt.Sprintf("failed to call swipe: %v", err),
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

// InputText inputs text into the active field
func (m *Mobile) InputText(text string) *BoolResult {
	args := map[string]interface{}{
		"text": text,
	}

	result, err := m.Session.CallMcpTool("input_text", args)
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

// SendKey sends a key press event
func (m *Mobile) SendKey(key int) *BoolResult {
	args := map[string]interface{}{
		"key": key,
	}

	result, err := m.Session.CallMcpTool("send_key", args)
	if err != nil {
		return &BoolResult{
			ApiResponse: models.ApiResponse{
				RequestID: "",
			},
			Success:      false,
			ErrorMessage: fmt.Sprintf("failed to call send_key: %v", err),
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

// GetClickableUIElements retrieves all clickable UI elements within the specified timeout
func (m *Mobile) GetClickableUIElements(timeoutMs int) *UIElementsResult {
	args := map[string]interface{}{
		"timeout_ms": timeoutMs,
	}

	result, err := m.Session.CallMcpTool("get_clickable_ui_elements", args)
	if err != nil {
		return &UIElementsResult{
			ApiResponse: models.ApiResponse{
				RequestID: "",
			},
			ErrorMessage: fmt.Sprintf("failed to call get_clickable_ui_elements: %v", err),
		}
	}

	if !result.Success {
		return &UIElementsResult{
			ApiResponse: models.ApiResponse{
				RequestID: result.RequestID,
			},
			ErrorMessage: result.ErrorMessage,
		}
	}

	// Parse UI elements from JSON
	var elements []*UIElement
	if err := json.Unmarshal([]byte(result.Data), &elements); err != nil {
		return &UIElementsResult{
			ApiResponse: models.ApiResponse{
				RequestID: result.RequestID,
			},
			ErrorMessage: fmt.Sprintf("failed to parse UI elements: %v", err),
		}
	}

	return &UIElementsResult{
		ApiResponse: models.ApiResponse{
			RequestID: result.RequestID,
		},
		Elements:     elements,
		ErrorMessage: result.ErrorMessage,
	}
}

// GetAllUIElements retrieves all UI elements within the specified timeout
func (m *Mobile) GetAllUIElements(timeoutMs int) *UIElementsResult {
	args := map[string]interface{}{
		"timeout_ms": timeoutMs,
	}

	result, err := m.Session.CallMcpTool("get_all_ui_elements", args)
	if err != nil {
		return &UIElementsResult{
			ApiResponse: models.ApiResponse{
				RequestID: "",
			},
			ErrorMessage: fmt.Sprintf("failed to call get_all_ui_elements: %v", err),
		}
	}

	if !result.Success {
		return &UIElementsResult{
			ApiResponse: models.ApiResponse{
				RequestID: result.RequestID,
			},
			ErrorMessage: result.ErrorMessage,
		}
	}

	// Parse UI elements from JSON
	var elements []*UIElement
	if err := json.Unmarshal([]byte(result.Data), &elements); err != nil {
		return &UIElementsResult{
			ApiResponse: models.ApiResponse{
				RequestID: result.RequestID,
			},
			ErrorMessage: fmt.Sprintf("failed to parse UI elements: %v", err),
		}
	}

	return &UIElementsResult{
		ApiResponse: models.ApiResponse{
			RequestID: result.RequestID,
		},
		Elements:     elements,
		ErrorMessage: result.ErrorMessage,
	}
}

// GetInstalledApps retrieves a list of installed applications
func (m *Mobile) GetInstalledApps(startMenu, desktop, ignoreSystemApps bool) *InstalledAppListResult {
	args := map[string]interface{}{
		"start_menu":         startMenu,
		"desktop":            desktop,
		"ignore_system_apps": ignoreSystemApps,
	}

	result, err := m.Session.CallMcpTool("get_installed_apps", args)
	if err != nil {
		return &InstalledAppListResult{
			ApiResponse: models.ApiResponse{
				RequestID: "",
			},
			ErrorMessage: fmt.Sprintf("failed to call get_installed_apps: %v", err),
		}
	}

	if !result.Success {
		return &InstalledAppListResult{
			ApiResponse: models.ApiResponse{
				RequestID: result.RequestID,
			},
			ErrorMessage: result.ErrorMessage,
		}
	}

	// Parse installed apps from JSON
	var apps []InstalledApp
	if err := json.Unmarshal([]byte(result.Data), &apps); err != nil {
		return &InstalledAppListResult{
			ApiResponse: models.ApiResponse{
				RequestID: result.RequestID,
			},
			ErrorMessage: fmt.Sprintf("failed to parse installed apps: %v", err),
		}
	}

	return &InstalledAppListResult{
		ApiResponse: models.ApiResponse{
			RequestID: result.RequestID,
		},
		Apps:         apps,
		ErrorMessage: result.ErrorMessage,
	}
}

// StartApp starts a specified application
func (m *Mobile) StartApp(startCmd, workDirectory, activity string) *ProcessListResult {
	args := map[string]interface{}{
		"start_cmd":      startCmd,
		"work_directory": workDirectory,
		"activity":       activity,
	}

	result, err := m.Session.CallMcpTool("start_app", args)
	if err != nil {
		return &ProcessListResult{
			ApiResponse: models.ApiResponse{
				RequestID: "",
			},
			ErrorMessage: fmt.Sprintf("failed to call start_app: %v", err),
		}
	}

	if !result.Success {
		return &ProcessListResult{
			ApiResponse: models.ApiResponse{
				RequestID: result.RequestID,
			},
			ErrorMessage: result.ErrorMessage,
		}
	}

	// Parse processes from JSON
	var processes []Process
	if err := json.Unmarshal([]byte(result.Data), &processes); err != nil {
		return &ProcessListResult{
			ApiResponse: models.ApiResponse{
				RequestID: result.RequestID,
			},
			ErrorMessage: fmt.Sprintf("failed to parse processes: %v", err),
		}
	}

	return &ProcessListResult{
		ApiResponse: models.ApiResponse{
			RequestID: result.RequestID,
		},
		Processes:    processes,
		ErrorMessage: result.ErrorMessage,
	}
}

// StopAppByPName stops an application by process name
func (m *Mobile) StopAppByPName(pname string) *BoolResult {
	args := map[string]interface{}{
		"pname": pname,
	}

	result, err := m.Session.CallMcpTool("stop_app_by_pname", args)
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

// Screenshot takes a screenshot of the current screen
func (m *Mobile) Screenshot() *ScreenshotResult {
	args := map[string]interface{}{}

	result, err := m.Session.CallMcpTool("system_screenshot", args)
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
