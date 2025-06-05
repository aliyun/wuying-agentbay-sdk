package window

import (
	"encoding/json"
	"fmt"

	"github.com/alibabacloud-go/tea/tea"
	mcp "github.com/aliyun/wuying-agentbay-sdk/golang/api/client"
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

// WindowManager handles window management operations in the AgentBay cloud environment.
type WindowManager struct {
	Session interface {
		GetAPIKey() string
		GetClient() *mcp.Client
		GetSessionId() string
	}
}

// NewWindowManager creates a new WindowManager object.
func NewWindowManager(session interface {
	GetAPIKey() string
	GetClient() *mcp.Client
	GetSessionId() string
}) *WindowManager {
	return &WindowManager{
		Session: session,
	}
}

// GetWindowInfoByPName gets detailed window information for a process by name.
func (wm *WindowManager) GetWindowInfoByPName(pname string) ([]Window, error) {
	args := map[string]string{
		"pname": pname,
	}
	argsJSON, err := json.Marshal(args)
	if err != nil {
		return nil, fmt.Errorf("failed to marshal args: %w", err)
	}

	callToolRequest := &mcp.CallMcpToolRequest{
		Authorization: tea.String("Bearer " + wm.Session.GetAPIKey()),
		SessionId:     tea.String(wm.Session.GetSessionId()),
		Name:          tea.String("get_window_info_by_pname"),
		Args:          tea.String(string(argsJSON)),
	}

	// Log API request
	fmt.Println("API Call: CallMcpTool - get_window_info_by_pname")
	fmt.Printf("Request: SessionId=%s, Args=%s\n", *callToolRequest.SessionId, *callToolRequest.Args)

	response, err := wm.Session.GetClient().CallMcpTool(callToolRequest)

	// Log API response
	if err != nil {
		fmt.Println("Error calling CallMcpTool - get_window_info_by_pname:", err)
		return nil, fmt.Errorf("failed to get window info by pname: %w", err)
	}
	if response != nil && response.Body != nil {
		fmt.Println("Response from CallMcpTool - get_window_info_by_pname:", response.Body)
	}
	if err != nil {
		return nil, fmt.Errorf("failed to get window info by pname: %w", err)
	}

	// Parse the response
	data, ok := response.Body.Data.(map[string]interface{})
	if !ok {
		return nil, fmt.Errorf("invalid response data format")
	}

	// Extract content array
	content, ok := data["content"].([]interface{})
	if !ok || len(content) == 0 {
		return nil, fmt.Errorf("invalid or empty content array in response")
	}

	// Extract text field from the first content item
	contentItem, ok := content[0].(map[string]interface{})
	if !ok {
		return nil, fmt.Errorf("invalid content item format")
	}

	jsonText, ok := contentItem["text"].(string)
	if !ok {
		return nil, fmt.Errorf("text field not found or not a string")
	}

	// Parse the JSON text to get the windows array
	var windows []Window
	if err := json.Unmarshal([]byte(jsonText), &windows); err != nil {
		return nil, fmt.Errorf("failed to unmarshal windows JSON: %w", err)
	}

	return windows, nil
}

// GetWindowInfoByPID gets detailed window information for a process by ID.
func (wm *WindowManager) GetWindowInfoByPID(pid int) ([]Window, error) {
	args := map[string]int{
		"pid": pid,
	}
	argsJSON, err := json.Marshal(args)
	if err != nil {
		return nil, fmt.Errorf("failed to marshal args: %w", err)
	}

	callToolRequest := &mcp.CallMcpToolRequest{
		Authorization: tea.String("Bearer " + wm.Session.GetAPIKey()),
		SessionId:     tea.String(wm.Session.GetSessionId()),
		Name:          tea.String("get_window_info_by_pid"),
		Args:          tea.String(string(argsJSON)),
	}

	// Log API request
	fmt.Println("API Call: CallMcpTool - get_window_info_by_pid")
	fmt.Printf("Request: SessionId=%s, Args=%s\n", *callToolRequest.SessionId, *callToolRequest.Args)

	response, err := wm.Session.GetClient().CallMcpTool(callToolRequest)

	// Log API response
	if err != nil {
		fmt.Println("Error calling CallMcpTool - get_window_info_by_pid:", err)
		return nil, fmt.Errorf("failed to get window info by pid: %w", err)
	}
	if response != nil && response.Body != nil {
		fmt.Println("Response from CallMcpTool - get_window_info_by_pid:", response.Body)
	}
	if err != nil {
		return nil, fmt.Errorf("failed to get window info by pid: %w", err)
	}

	// Parse the response
	data, ok := response.Body.Data.(map[string]interface{})
	if !ok {
		return nil, fmt.Errorf("invalid response data format")
	}

	// Extract content array
	content, ok := data["content"].([]interface{})
	if !ok || len(content) == 0 {
		return nil, fmt.Errorf("invalid or empty content array in response")
	}

	// Extract text field from the first content item
	contentItem, ok := content[0].(map[string]interface{})
	if !ok {
		return nil, fmt.Errorf("invalid content item format")
	}

	jsonText, ok := contentItem["text"].(string)
	if !ok {
		return nil, fmt.Errorf("text field not found or not a string")
	}

	// Parse the JSON text to get the windows array
	var windows []Window
	if err := json.Unmarshal([]byte(jsonText), &windows); err != nil {
		return nil, fmt.Errorf("failed to unmarshal windows JSON: %w", err)
	}

	return windows, nil
}

// ListRootWindows lists all root windows in the system.
func (wm *WindowManager) ListRootWindows() ([]Window, error) {
	args := map[string]interface{}{}
	argsJSON, err := json.Marshal(args)
	if err != nil {
		return nil, fmt.Errorf("failed to marshal args: %w", err)
	}

	callToolRequest := &mcp.CallMcpToolRequest{
		Authorization: tea.String("Bearer " + wm.Session.GetAPIKey()),
		SessionId:     tea.String(wm.Session.GetSessionId()),
		Name:          tea.String("list_root_windows"),
		Args:          tea.String(string(argsJSON)),
	}

	// Log API request
	fmt.Println("API Call: CallMcpTool - list_root_windows")
	fmt.Printf("Request: SessionId=%s, Args=%s\n", *callToolRequest.SessionId, *callToolRequest.Args)

	response, err := wm.Session.GetClient().CallMcpTool(callToolRequest)

	// Log API response
	if err != nil {
		fmt.Println("Error calling CallMcpTool - list_root_windows:", err)
		return nil, fmt.Errorf("failed to list root windows: %w", err)
	}
	if response != nil && response.Body != nil {
		fmt.Println("Response from CallMcpTool - list_root_windows:", response.Body)
	}
	if err != nil {
		return nil, fmt.Errorf("failed to list root windows: %w", err)
	}

	// Parse the response
	data, ok := response.Body.Data.(map[string]interface{})
	if !ok {
		return nil, fmt.Errorf("invalid response data format")
	}

	// Extract content array
	content, ok := data["content"].([]interface{})
	if !ok || len(content) == 0 {
		return nil, fmt.Errorf("invalid or empty content array in response")
	}

	// Extract text field from the first content item
	contentItem, ok := content[0].(map[string]interface{})
	if !ok {
		return nil, fmt.Errorf("invalid content item format")
	}

	jsonText, ok := contentItem["text"].(string)
	if !ok {
		return nil, fmt.Errorf("text field not found or not a string")
	}

	// Parse the JSON text to get the windows array
	var windows []Window
	if err := json.Unmarshal([]byte(jsonText), &windows); err != nil {
		return nil, fmt.Errorf("failed to unmarshal windows JSON: %w", err)
	}

	return windows, nil
}

// GetActiveWindow gets the currently active window.
func (wm *WindowManager) GetActiveWindow() (*Window, error) {
	args := map[string]interface{}{}
	argsJSON, err := json.Marshal(args)
	if err != nil {
		return nil, fmt.Errorf("failed to marshal args: %w", err)
	}

	callToolRequest := &mcp.CallMcpToolRequest{
		Authorization: tea.String("Bearer " + wm.Session.GetAPIKey()),
		SessionId:     tea.String(wm.Session.GetSessionId()),
		Name:          tea.String("get_active_window"),
		Args:          tea.String(string(argsJSON)),
	}

	// Log API request
	fmt.Println("API Call: CallMcpTool - get_active_window")
	fmt.Printf("Request: SessionId=%s, Args=%s\n", *callToolRequest.SessionId, *callToolRequest.Args)

	response, err := wm.Session.GetClient().CallMcpTool(callToolRequest)

	// Log API response
	if err != nil {
		fmt.Println("Error calling CallMcpTool - get_active_window:", err)
		return nil, fmt.Errorf("failed to get active window: %w", err)
	}
	if response != nil && response.Body != nil {
		fmt.Println("Response from CallMcpTool - get_active_window:", response.Body)
	}
	if err != nil {
		return nil, fmt.Errorf("failed to get active window: %w", err)
	}

	// Parse the response
	data, ok := response.Body.Data.(map[string]interface{})
	if !ok {
		return nil, fmt.Errorf("invalid response data format")
	}

	// Extract content array
	content, ok := data["content"].([]interface{})
	if !ok || len(content) == 0 {
		return nil, fmt.Errorf("invalid or empty content array in response")
	}

	// Extract text field from the first content item
	contentItem, ok := content[0].(map[string]interface{})
	if !ok {
		return nil, fmt.Errorf("invalid content item format")
	}

	jsonText, ok := contentItem["text"].(string)
	if !ok {
		return nil, fmt.Errorf("text field not found or not a string")
	}

	// Parse the JSON text to get the window
	var window Window
	if err := json.Unmarshal([]byte(jsonText), &window); err != nil {
		return nil, fmt.Errorf("failed to unmarshal window JSON: %w", err)
	}

	return &window, nil
}

// ActivateWindow activates a window by ID.
func (wm *WindowManager) ActivateWindow(windowID int) error {
	args := map[string]int{
		"window_id": windowID,
	}
	argsJSON, err := json.Marshal(args)
	if err != nil {
		return fmt.Errorf("failed to marshal args: %w", err)
	}

	callToolRequest := &mcp.CallMcpToolRequest{
		Authorization: tea.String("Bearer " + wm.Session.GetAPIKey()),
		SessionId:     tea.String(wm.Session.GetSessionId()),
		Name:          tea.String("activate_window"),
		Args:          tea.String(string(argsJSON)),
	}

	// Log API request
	fmt.Println("API Call: CallMcpTool - activate_window")
	fmt.Printf("Request: SessionId=%s, Args=%s\n", *callToolRequest.SessionId, *callToolRequest.Args)

	response, err := wm.Session.GetClient().CallMcpTool(callToolRequest)

	// Log API response
	if err != nil {
		fmt.Println("Error calling CallMcpTool - activate_window:", err)
		return fmt.Errorf("failed to activate window: %w", err)
	}
	if response != nil && response.Body != nil {
		fmt.Println("Response from CallMcpTool - activate_window:", response.Body)
	}
	if err != nil {
		return fmt.Errorf("failed to activate window: %w", err)
	}

	return nil
}

// MaximizeWindow maximizes a window by ID.
func (wm *WindowManager) MaximizeWindow(windowID int) error {
	args := map[string]int{
		"window_id": windowID,
	}
	argsJSON, err := json.Marshal(args)
	if err != nil {
		return fmt.Errorf("failed to marshal args: %w", err)
	}

	callToolRequest := &mcp.CallMcpToolRequest{
		Authorization: tea.String("Bearer " + wm.Session.GetAPIKey()),
		SessionId:     tea.String(wm.Session.GetSessionId()),
		Name:          tea.String("maximize_window"),
		Args:          tea.String(string(argsJSON)),
	}

	// Log API request
	fmt.Println("API Call: CallMcpTool - maximize_window")
	fmt.Printf("Request: SessionId=%s, Args=%s\n", *callToolRequest.SessionId, *callToolRequest.Args)

	response, err := wm.Session.GetClient().CallMcpTool(callToolRequest)

	// Log API response
	if err != nil {
		fmt.Println("Error calling CallMcpTool - maximize_window:", err)
		return fmt.Errorf("failed to maximize window: %w", err)
	}
	if response != nil && response.Body != nil {
		fmt.Println("Response from CallMcpTool - maximize_window:", response.Body)
	}
	if err != nil {
		return fmt.Errorf("failed to maximize window: %w", err)
	}

	return nil
}

// MinimizeWindow minimizes a window by ID.
func (wm *WindowManager) MinimizeWindow(windowID int) error {
	args := map[string]int{
		"window_id": windowID,
	}
	argsJSON, err := json.Marshal(args)
	if err != nil {
		return fmt.Errorf("failed to marshal args: %w", err)
	}

	callToolRequest := &mcp.CallMcpToolRequest{
		Authorization: tea.String("Bearer " + wm.Session.GetAPIKey()),
		SessionId:     tea.String(wm.Session.GetSessionId()),
		Name:          tea.String("minimize_window"),
		Args:          tea.String(string(argsJSON)),
	}

	// Log API request
	fmt.Println("API Call: CallMcpTool - minimize_window")
	fmt.Printf("Request: SessionId=%s, Args=%s\n", *callToolRequest.SessionId, *callToolRequest.Args)

	response, err := wm.Session.GetClient().CallMcpTool(callToolRequest)

	// Log API response
	if err != nil {
		fmt.Println("Error calling CallMcpTool - minimize_window:", err)
		return fmt.Errorf("failed to minimize window: %w", err)
	}
	if response != nil && response.Body != nil {
		fmt.Println("Response from CallMcpTool - minimize_window:", response.Body)
	}
	if err != nil {
		return fmt.Errorf("failed to minimize window: %w", err)
	}

	return nil
}

// RestoreWindow restores a window by ID.
func (wm *WindowManager) RestoreWindow(windowID int) error {
	args := map[string]int{
		"window_id": windowID,
	}
	argsJSON, err := json.Marshal(args)
	if err != nil {
		return fmt.Errorf("failed to marshal args: %w", err)
	}

	callToolRequest := &mcp.CallMcpToolRequest{
		Authorization: tea.String("Bearer " + wm.Session.GetAPIKey()),
		SessionId:     tea.String(wm.Session.GetSessionId()),
		Name:          tea.String("restore_window"),
		Args:          tea.String(string(argsJSON)),
	}

	// Log API request
	fmt.Println("API Call: CallMcpTool - restore_window")
	fmt.Printf("Request: SessionId=%s, Args=%s\n", *callToolRequest.SessionId, *callToolRequest.Args)

	response, err := wm.Session.GetClient().CallMcpTool(callToolRequest)

	// Log API response
	if err != nil {
		fmt.Println("Error calling CallMcpTool - restore_window:", err)
		return fmt.Errorf("failed to restore window: %w", err)
	}
	if response != nil && response.Body != nil {
		fmt.Println("Response from CallMcpTool - restore_window:", response.Body)
	}
	if err != nil {
		return fmt.Errorf("failed to restore window: %w", err)
	}

	return nil
}

// CloseWindow closes a window by ID.
func (wm *WindowManager) CloseWindow(windowID int) error {
	args := map[string]int{
		"window_id": windowID,
	}
	argsJSON, err := json.Marshal(args)
	if err != nil {
		return fmt.Errorf("failed to marshal args: %w", err)
	}

	callToolRequest := &mcp.CallMcpToolRequest{
		Authorization: tea.String("Bearer " + wm.Session.GetAPIKey()),
		SessionId:     tea.String(wm.Session.GetSessionId()),
		Name:          tea.String("close_window"),
		Args:          tea.String(string(argsJSON)),
	}

	// Log API request
	fmt.Println("API Call: CallMcpTool - close_window")
	fmt.Printf("Request: SessionId=%s, Args=%s\n", *callToolRequest.SessionId, *callToolRequest.Args)

	response, err := wm.Session.GetClient().CallMcpTool(callToolRequest)

	// Log API response
	if err != nil {
		fmt.Println("Error calling CallMcpTool - close_window:", err)
		return fmt.Errorf("failed to close window: %w", err)
	}
	if response != nil && response.Body != nil {
		fmt.Println("Response from CallMcpTool - close_window:", response.Body)
	}
	if err != nil {
		return fmt.Errorf("failed to close window: %w", err)
	}

	return nil
}

// FullscreenWindow toggles fullscreen mode for a window by ID.
func (wm *WindowManager) FullscreenWindow(windowID int) error {
	args := map[string]int{
		"window_id": windowID,
	}
	argsJSON, err := json.Marshal(args)
	if err != nil {
		return fmt.Errorf("failed to marshal args: %w", err)
	}

	callToolRequest := &mcp.CallMcpToolRequest{
		Authorization: tea.String("Bearer " + wm.Session.GetAPIKey()),
		SessionId:     tea.String(wm.Session.GetSessionId()),
		Name:          tea.String("fullscreen_window"),
		Args:          tea.String(string(argsJSON)),
	}

	// Log API request
	fmt.Println("API Call: CallMcpTool - fullscreen_window")
	fmt.Printf("Request: SessionId=%s, Args=%s\n", *callToolRequest.SessionId, *callToolRequest.Args)

	response, err := wm.Session.GetClient().CallMcpTool(callToolRequest)

	// Log API response
	if err != nil {
		fmt.Println("Error calling CallMcpTool - fullscreen_window:", err)
		return fmt.Errorf("failed to fullscreen window: %w", err)
	}
	if response != nil && response.Body != nil {
		fmt.Println("Response from CallMcpTool - fullscreen_window:", response.Body)
	}
	if err != nil {
		return fmt.Errorf("failed to fullscreen window: %w", err)
	}

	return nil
}

// ResizeWindow resizes a window by ID.
func (wm *WindowManager) ResizeWindow(windowID, width, height int) error {
	args := map[string]int{
		"window_id": windowID,
		"width":     width,
		"height":    height,
	}
	argsJSON, err := json.Marshal(args)
	if err != nil {
		return fmt.Errorf("failed to marshal args: %w", err)
	}

	callToolRequest := &mcp.CallMcpToolRequest{
		Authorization: tea.String("Bearer " + wm.Session.GetAPIKey()),
		SessionId:     tea.String(wm.Session.GetSessionId()),
		Name:          tea.String("resize_window"),
		Args:          tea.String(string(argsJSON)),
	}

	// Log API request
	fmt.Println("API Call: CallMcpTool - resize_window")
	fmt.Printf("Request: SessionId=%s, Args=%s\n", *callToolRequest.SessionId, *callToolRequest.Args)

	response, err := wm.Session.GetClient().CallMcpTool(callToolRequest)

	// Log API response
	if err != nil {
		fmt.Println("Error calling CallMcpTool - resize_window:", err)
		return fmt.Errorf("failed to resize window: %w", err)
	}
	if response != nil && response.Body != nil {
		fmt.Println("Response from CallMcpTool - resize_window:", response.Body)
	}
	if err != nil {
		return fmt.Errorf("failed to resize window: %w", err)
	}

	return nil
}

// FocusMode enables or disables focus mode.
func (wm *WindowManager) FocusMode(on bool) error {
	args := map[string]bool{
		"on": on,
	}
	argsJSON, err := json.Marshal(args)
	if err != nil {
		return fmt.Errorf("failed to marshal args: %w", err)
	}

	callToolRequest := &mcp.CallMcpToolRequest{
		Authorization: tea.String("Bearer " + wm.Session.GetAPIKey()),
		SessionId:     tea.String(wm.Session.GetSessionId()),
		Name:          tea.String("focus_mode"),
		Args:          tea.String(string(argsJSON)),
	}

	// Log API request
	fmt.Println("API Call: CallMcpTool - focus_mode")
	fmt.Printf("Request: SessionId=%s, Args=%s\n", *callToolRequest.SessionId, *callToolRequest.Args)

	response, err := wm.Session.GetClient().CallMcpTool(callToolRequest)

	// Log API response
	if err != nil {
		fmt.Println("Error calling CallMcpTool - focus_mode:", err)
		return fmt.Errorf("failed to set focus mode: %w", err)
	}
	if response != nil && response.Body != nil {
		fmt.Println("Response from CallMcpTool - focus_mode:", response.Body)
	}
	if err != nil {
		return fmt.Errorf("failed to set focus mode: %w", err)
	}

	return nil
}
