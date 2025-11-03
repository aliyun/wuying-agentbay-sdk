package mobile

import (
	"encoding/json"
	"fmt"
	"strings"

	"github.com/alibabacloud-go/tea/tea"
	mcp "github.com/aliyun/wuying-agentbay-sdk/golang/api/client"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/command"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/models"
)

// UIElement represents a UI element structure
type UIElement struct {
	Bounds      *UIBounds    `json:"bounds,omitempty"`
	ClassName   string       `json:"className,omitempty"`
	ContentDesc string       `json:"contentDesc,omitempty"`
	ElementID   string       `json:"elementId,omitempty"`
	Package     string       `json:"package,omitempty"`
	ResourceID  string       `json:"resourceId,omitempty"`
	Text        string       `json:"text,omitempty"`
	Type        string       `json:"type,omitempty"`
	Children    []*UIElement `json:"children,omitempty"`
}

// UnmarshalJSON custom unmarshaler to handle string format bounds
func (e *UIElement) UnmarshalJSON(data []byte) error {
	// Define an auxiliary type to avoid recursion
	type Alias UIElement
	aux := &struct {
		BoundsRaw interface{} `json:"bounds"`
		*Alias
	}{
		Alias: (*Alias)(e),
	}

	if err := json.Unmarshal(data, &aux); err != nil {
		return err
	}

	// Handle bounds field which can be either string or object
	if aux.BoundsRaw != nil {
		switch v := aux.BoundsRaw.(type) {
		case string:
			// Parse string format: "left,top,right,bottom"
			e.Bounds = parseBoundsString(v)
		case map[string]interface{}:
			// Parse object format
			if boundsJSON, err := json.Marshal(v); err == nil {
				var bounds UIBounds
				if err := json.Unmarshal(boundsJSON, &bounds); err == nil {
					e.Bounds = &bounds
				}
			}
		}
	}

	return nil
}

// parseBoundsString parses bounds string format "left,top,right,bottom"
func parseBoundsString(s string) *UIBounds {
	parts := strings.Split(s, ",")
	if len(parts) != 4 {
		return nil
	}

	var left, top, right, bottom int
	if _, err := fmt.Sscanf(s, "%d,%d,%d,%d", &left, &top, &right, &bottom); err != nil {
		return nil
	}

	return &UIBounds{
		Left:   left,
		Top:    top,
		Right:  right,
		Bottom: bottom,
	}
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

// AdbUrlResult represents the result of ADB URL retrieval operation
type AdbUrlResult struct {
	models.ApiResponse
	URL          string `json:"url"`
	Success      bool   `json:"success"`
	ErrorMessage string `json:"error_message"`
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

// Mobile handles mobile UI automation operations and configuration in the AgentBay cloud environment.
// Provides touch operations, UI element interactions, application management, screenshot capabilities,
// and mobile environment configuration.
type Mobile struct {
	Session interface {
		GetAPIKey() string
		GetClient() *mcp.Client
		GetSessionId() string
		GetImageID() string
		IsVpc() bool
		NetworkInterfaceIp() string
		HttpPort() string
		FindServerForTool(toolName string) string
		CallMcpTool(toolName string, args interface{}, autoGenSession ...bool) (*models.McpToolResult, error)
	}
	command *command.Command
}

// SessionWithCommand extends the basic session interface to include Command access
type SessionWithCommand interface {
	GetAPIKey() string
	GetClient() *mcp.Client
	GetSessionId() string
	IsVpc() bool
	NetworkInterfaceIp() string
	HttpPort() string
	FindServerForTool(toolName string) string
	CallMcpTool(toolName string, args interface{}, autoGenSession ...bool) (*models.McpToolResult, error)
	GetCommand() *command.Command
}

// NewMobile creates a new Mobile instance for UI automation
func NewMobile(session interface {
	GetAPIKey() string
	GetClient() *mcp.Client
	GetSessionId() string
	GetImageID() string
	IsVpc() bool
	NetworkInterfaceIp() string
	HttpPort() string
	FindServerForTool(toolName string) string
	CallMcpTool(toolName string, args interface{}, autoGenSession ...bool) (*models.McpToolResult, error)
}) *Mobile {
	mobile := &Mobile{
		Session: session,
	}

	// Try to get command from session if it implements SessionWithCommand interface
	if sessionWithCmd, ok := session.(SessionWithCommand); ok {
		mobile.command = sessionWithCmd.GetCommand()
	}

	return mobile
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

// StopAppByCmd stops an application using the provided stop command
func (m *Mobile) StopAppByCmd(stopCmd string) *BoolResult {
	args := map[string]interface{}{
		"stop_cmd": stopCmd,
	}

	result, err := m.Session.CallMcpTool("stop_app_by_cmd", args)
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

// Configure configures mobile settings from MobileExtraConfig
func (m *Mobile) Configure(mobileConfig *models.MobileExtraConfig) error {
	if mobileConfig == nil {
		return fmt.Errorf("no mobile configuration provided")
	}

	// Configure resolution lock
	if err := m.setResolutionLock(mobileConfig.LockResolution); err != nil {
		return fmt.Errorf("failed to set resolution lock: %v", err)
	}

	// Configure app management rules
	if mobileConfig.AppManagerRule != nil && mobileConfig.AppManagerRule.RuleType != "" {
		appRule := mobileConfig.AppManagerRule
		packageNames := appRule.AppPackageNameList

		if len(packageNames) > 0 && (appRule.RuleType == "White" || appRule.RuleType == "Black") {
			if appRule.RuleType == "White" {
				if err := m.setAppWhitelist(packageNames); err != nil {
					return fmt.Errorf("failed to set app whitelist: %v", err)
				}
			} else {
				if err := m.setAppBlacklist(packageNames); err != nil {
					return fmt.Errorf("failed to set app blacklist: %v", err)
				}
			}
		} else if len(packageNames) == 0 {
			return fmt.Errorf("no package names provided for %s list", appRule.RuleType)
		}
	}

	// Configure navigation bar visibility
	if err := m.setNavigationBarVisibility(mobileConfig.HideNavigationBar); err != nil {
		return fmt.Errorf("failed to set navigation bar visibility: %v", err)
	}

	// Configure uninstall blacklist
	if len(mobileConfig.UninstallBlacklist) > 0 {
		if err := m.setUninstallBlacklist(mobileConfig.UninstallBlacklist); err != nil {
			return fmt.Errorf("failed to set uninstall blacklist: %v", err)
		}
	}

	return nil
}

// SetResolutionLock sets display resolution lock for mobile devices
func (m *Mobile) SetResolutionLock(enable bool) error {
	return m.setResolutionLock(enable)
}

// setResolutionLock internal method to set resolution lock
func (m *Mobile) setResolutionLock(enable bool) error {
	var templateName string
	if enable {
		templateName = "resolution_lock_enable"
	} else {
		templateName = "resolution_lock_disable"
	}

	template, exists := command.GetMobileCommandTemplate(templateName)
	if !exists {
		return fmt.Errorf("resolution lock template not found: %s", templateName)
	}

	return m.executeTemplateCommand(template, templateName)
}

// setAppWhitelist sets app whitelist configuration
func (m *Mobile) setAppWhitelist(packageNames []string) error {
	template, exists := command.GetMobileCommandTemplate("app_whitelist")
	if !exists {
		return fmt.Errorf("app whitelist template not found")
	}

	// Replace placeholder with actual package names (newline-separated for file content)
	packageList := strings.Join(packageNames, "\n")
	command := strings.ReplaceAll(template, "{package_list}", packageList)

	return m.executeTemplateCommand(command, fmt.Sprintf("App whitelist configuration (%d packages)", len(packageNames)))
}

// setAppBlacklist sets app blacklist configuration
func (m *Mobile) setAppBlacklist(packageNames []string) error {
	template, exists := command.GetMobileCommandTemplate("app_blacklist")
	if !exists {
		return fmt.Errorf("app blacklist template not found")
	}

	// Replace placeholder with actual package names (newline-separated for file content)
	packageList := strings.Join(packageNames, "\n")
	command := strings.ReplaceAll(template, "{package_list}", packageList)

	return m.executeTemplateCommand(command, fmt.Sprintf("App blacklist configuration (%d packages)", len(packageNames)))
}

// setNavigationBarVisibility sets navigation bar visibility
func (m *Mobile) setNavigationBarVisibility(hide bool) error {
	var templateName string
	if hide {
		templateName = "hide_navigation_bar"
	} else {
		templateName = "show_navigation_bar"
	}

	template, exists := command.GetMobileCommandTemplate(templateName)
	if !exists {
		return fmt.Errorf("navigation bar template not found: %s", templateName)
	}

	description := fmt.Sprintf("Navigation bar visibility (hide: %t)", hide)
	return m.executeTemplateCommand(template, description)
}

// setUninstallBlacklist sets uninstall protection blacklist
func (m *Mobile) setUninstallBlacklist(packageNames []string) error {
	template, exists := command.GetMobileCommandTemplate("uninstall_blacklist")
	if !exists {
		return fmt.Errorf("uninstall blacklist template not found")
	}

	// Replace placeholder with actual package names (semicolon-separated for property value)
	packageList := strings.Join(packageNames, ";")
	command := strings.ReplaceAll(template, "{package_list}", packageList)

	description := fmt.Sprintf("Uninstall blacklist configuration (%d packages)", len(packageNames))
	return m.executeTemplateCommand(command, description)
}

// SetNavigationBarVisibility sets navigation bar visibility for mobile devices
func (m *Mobile) SetNavigationBarVisibility(hide bool) error {
	return m.setNavigationBarVisibility(hide)
}

// SetUninstallBlacklist sets uninstall protection blacklist for mobile devices
func (m *Mobile) SetUninstallBlacklist(packageNames []string) error {
	return m.setUninstallBlacklist(packageNames)
}

// SetAppWhitelist sets app whitelist for mobile devices
func (m *Mobile) SetAppWhitelist(packageNames []string) error {
	return m.setAppWhitelist(packageNames)
}

// SetAppBlacklist sets app blacklist for mobile devices
func (m *Mobile) SetAppBlacklist(packageNames []string) error {
	return m.setAppBlacklist(packageNames)
}

// executeTemplateCommand executes a mobile command template
func (m *Mobile) executeTemplateCommand(commandTemplate, description string) error {
	if m.command == nil {
		return fmt.Errorf("command service not available")
	}

	fmt.Printf("Executing %s\n", description)

	result, err := m.command.ExecuteCommand(commandTemplate)
	if err != nil {
		return fmt.Errorf("failed to execute %s: %v", description, err)
	}

	if result != nil && result.Output != "" {
		fmt.Printf("✅ %s completed successfully\n", description)
	}

	return nil
}

// GetAdbUrl retrieves the ADB connection URL for the mobile environment.
// This method is only supported in mobile environments (mobile_latest image).
// It uses the provided ADB public key to establish the connection and returns
// the ADB connect URL.
func (m *Mobile) GetAdbUrl(adbkeyPub string) *AdbUrlResult {
	// Build options JSON with adbkey_pub
	optionsMap := map[string]string{"adbkey_pub": adbkeyPub}
	optionsJSON, err := json.Marshal(optionsMap)
	if err != nil {
		errorMsg := fmt.Sprintf("Failed to marshal options: %v", err)
		return &AdbUrlResult{
			ApiResponse:  models.ApiResponse{RequestID: ""},
			URL:          "",
			Success:      false,
			ErrorMessage: errorMsg,
		}
	}

	// Call GetLink API directly with protocol_type="adb" and options
	protocolType := "adb"
	optionsStr := string(optionsJSON)

	getLinkRequest := &mcp.GetLinkRequest{
		Authorization: tea.String("Bearer " + m.Session.GetAPIKey()),
		SessionId:     tea.String(m.Session.GetSessionId()),
		ProtocolType:  tea.String(protocolType),
		Port:          nil,
		Option:        tea.String(optionsStr),
	}

	// Log the API call (blue color)
	fmt.Printf("\033[34m🔗 API Call: GetLink\033[0m\n")
	fmt.Printf("   └─ SessionId=%s, ProtocolType=%s, Options=provided\n", m.Session.GetSessionId(), protocolType)

	response, err := m.Session.GetClient().GetLink(getLinkRequest)
	if err != nil {
		errorMsg := fmt.Sprintf("Failed to get ADB URL: %v", err)
		fmt.Printf("\033[31m❌ API Response Failed: GetLink\033[0m\n")
		fmt.Printf("   └─ Error: %s\n", errorMsg)
		return &AdbUrlResult{
			ApiResponse:  models.ApiResponse{RequestID: ""},
			URL:          "",
			Success:      false,
			ErrorMessage: errorMsg,
		}
	}

	// Extract request ID from response
	requestID := ""
	if response.Body != nil && response.Body.RequestId != nil {
		requestID = tea.StringValue(response.Body.RequestId)
	}

	// Extract URL from response
	url := ""
	if response.Body != nil && response.Body.Data != nil && response.Body.Data.Url != nil {
		url = tea.StringValue(response.Body.Data.Url)
	}

	// Log the successful response (green color, no masking for user convenience)
	fmt.Printf("\033[32m✅ API Response: GetLink, RequestId=%s\033[0m\n", requestID)
	if url != "" {
		fmt.Printf("\033[32m   └─ url=%s\033[0m\n", url)
	}

	return &AdbUrlResult{
		ApiResponse:  models.ApiResponse{RequestID: requestID},
		URL:          url,
		Success:      true,
		ErrorMessage: "",
	}
}
