package application

import (
	"encoding/json"
	"fmt"

	"github.com/alibabacloud-go/tea/tea"
	mcp "github.com/aliyun/wuying-agentbay-sdk/golang/api/client"
)

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

// ApplicationManager handles application management operations in the AgentBay cloud environment.
type ApplicationManager struct {
	Session interface {
		GetAPIKey() string
		GetClient() *mcp.Client
		GetSessionId() string
	}
}

// NewApplicationManager creates a new ApplicationManager object.
func NewApplicationManager(session interface {
	GetAPIKey() string
	GetClient() *mcp.Client
	GetSessionId() string
}) *ApplicationManager {
	return &ApplicationManager{
		Session: session,
	}
}

// GetInstalledApps retrieves a list of installed applications.
func (am *ApplicationManager) GetInstalledApps(startMenu bool, desktop bool, ignoreSystemApps bool) ([]InstalledApp, error) {
	args := map[string]interface{}{
		"start_menu":         startMenu,
		"desktop":            desktop,
		"ignore_system_apps": ignoreSystemApps,
	}
	argsJSON, err := json.Marshal(args)
	if err != nil {
		return nil, fmt.Errorf("failed to marshal args: %w", err)
	}

	callToolRequest := &mcp.CallMcpToolRequest{
		Authorization: tea.String("Bearer " + am.Session.GetAPIKey()),
		SessionId:     tea.String(am.Session.GetSessionId()),
		Name:          tea.String("get_installed_apps"),
		Args:          tea.String(string(argsJSON)),
	}

	// Log API request
	fmt.Println("API Call: CallMcpTool - get_installed_apps")
	fmt.Printf("Request: SessionId=%s, Args=%s\n", *callToolRequest.SessionId, *callToolRequest.Args)

	response, err := am.Session.GetClient().CallMcpTool(callToolRequest)

	// Log API response
	if err != nil {
		fmt.Println("Error calling CallMcpTool - get_installed_apps:", err)
		return nil, fmt.Errorf("failed to get installed apps: %w", err)
	}
	if response != nil && response.Body != nil {
		fmt.Println("Response from CallMcpTool - get_installed_apps:", response.Body)
	}
	if err != nil {
		return nil, fmt.Errorf("failed to get installed apps: %w", err)
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

	// Parse the JSON text to get the apps array
	var apps []InstalledApp
	if err := json.Unmarshal([]byte(jsonText), &apps); err != nil {
		return nil, fmt.Errorf("failed to unmarshal apps JSON: %w", err)
	}

	return apps, nil
}

// StartApp starts an application with the given command and optional working directory.
func (am *ApplicationManager) StartApp(startCmd string, workDirectory string) ([]Process, error) {
	args := map[string]string{
		"start_cmd": startCmd,
	}
	if workDirectory != "" {
		args["work_directory"] = workDirectory
	}

	argsJSON, err := json.Marshal(args)
	if err != nil {
		return nil, fmt.Errorf("failed to marshal args: %w", err)
	}

	callToolRequest := &mcp.CallMcpToolRequest{
		Authorization: tea.String("Bearer " + am.Session.GetAPIKey()),
		SessionId:     tea.String(am.Session.GetSessionId()),
		Name:          tea.String("start_app"),
		Args:          tea.String(string(argsJSON)),
	}

	// Log API request
	fmt.Println("API Call: CallMcpTool - start_app")
	fmt.Printf("Request: SessionId=%s, Args=%s\n", *callToolRequest.SessionId, *callToolRequest.Args)

	response, err := am.Session.GetClient().CallMcpTool(callToolRequest)

	// Log API response
	if err != nil {
		fmt.Println("Error calling CallMcpTool - start_app:", err)
		return nil, fmt.Errorf("failed to start app: %w", err)
	}
	if response != nil && response.Body != nil {
		fmt.Println("Response from CallMcpTool - start_app:", response.Body)
	}
	if err != nil {
		return nil, fmt.Errorf("failed to start app: %w", err)
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

	// Parse the JSON text to get the processes array
	var processes []Process
	if err := json.Unmarshal([]byte(jsonText), &processes); err != nil {
		return nil, fmt.Errorf("failed to unmarshal processes JSON: %w", err)
	}

	return processes, nil
}

// StopAppByPName stops an application by process name.
func (am *ApplicationManager) StopAppByPName(pname string) error {
	args := map[string]string{
		"pname": pname,
	}
	argsJSON, err := json.Marshal(args)
	if err != nil {
		return fmt.Errorf("failed to marshal args: %w", err)
	}

	callToolRequest := &mcp.CallMcpToolRequest{
		Authorization: tea.String("Bearer " + am.Session.GetAPIKey()),
		SessionId:     tea.String(am.Session.GetSessionId()),
		Name:          tea.String("stop_app_by_pname"),
		Args:          tea.String(string(argsJSON)),
	}

	// Log API request
	fmt.Println("API Call: CallMcpTool - stop_app_by_pname")
	fmt.Printf("Request: SessionId=%s, Args=%s\n", *callToolRequest.SessionId, *callToolRequest.Args)

	response, err := am.Session.GetClient().CallMcpTool(callToolRequest)

	// Log API response
	if err != nil {
		fmt.Println("Error calling CallMcpTool - stop_app_by_pname:", err)
		return fmt.Errorf("failed to stop app by pname: %w", err)
	}
	if response != nil && response.Body != nil {
		fmt.Println("Response from CallMcpTool - stop_app_by_pname:", response.Body)
	}
	if err != nil {
		return fmt.Errorf("failed to stop app by pname: %w", err)
	}

	return nil
}

// StopAppByPID stops an application by process ID.
func (am *ApplicationManager) StopAppByPID(pid int) error {
	args := map[string]int{
		"pid": pid,
	}
	argsJSON, err := json.Marshal(args)
	if err != nil {
		return fmt.Errorf("failed to marshal args: %w", err)
	}

	callToolRequest := &mcp.CallMcpToolRequest{
		Authorization: tea.String("Bearer " + am.Session.GetAPIKey()),
		SessionId:     tea.String(am.Session.GetSessionId()),
		Name:          tea.String("stop_app_by_pid"),
		Args:          tea.String(string(argsJSON)),
	}

	// Log API request
	fmt.Println("API Call: CallMcpTool - stop_app_by_pid")
	fmt.Printf("Request: SessionId=%s, Args=%s\n", *callToolRequest.SessionId, *callToolRequest.Args)

	response, err := am.Session.GetClient().CallMcpTool(callToolRequest)

	// Log API response
	if err != nil {
		fmt.Println("Error calling CallMcpTool - stop_app_by_pid:", err)
		return fmt.Errorf("failed to stop app by pid: %w", err)
	}
	if response != nil && response.Body != nil {
		fmt.Println("Response from CallMcpTool - stop_app_by_pid:", response.Body)
	}
	if err != nil {
		return fmt.Errorf("failed to stop app by pid: %w", err)
	}

	return nil
}

// StopAppByCmd stops an application by stop command.
func (am *ApplicationManager) StopAppByCmd(stopCmd string) error {
	args := map[string]string{
		"stop_cmd": stopCmd,
	}
	argsJSON, err := json.Marshal(args)
	if err != nil {
		return fmt.Errorf("failed to marshal args: %w", err)
	}

	callToolRequest := &mcp.CallMcpToolRequest{
		Authorization: tea.String("Bearer " + am.Session.GetAPIKey()),
		SessionId:     tea.String(am.Session.GetSessionId()),
		Name:          tea.String("stop_app_by_cmd"),
		Args:          tea.String(string(argsJSON)),
	}

	// Log API request
	fmt.Println("API Call: CallMcpTool - stop_app_by_cmd")
	fmt.Printf("Request: SessionId=%s, Args=%s\n", *callToolRequest.SessionId, *callToolRequest.Args)

	response, err := am.Session.GetClient().CallMcpTool(callToolRequest)

	// Log API response
	if err != nil {
		fmt.Println("Error calling CallMcpTool - stop_app_by_cmd:", err)
		return fmt.Errorf("failed to stop app by command: %w", err)
	}
	if response != nil && response.Body != nil {
		fmt.Println("Response from CallMcpTool - stop_app_by_cmd:", response.Body)
	}
	if err != nil {
		return fmt.Errorf("failed to stop app by command: %w", err)
	}

	return nil
}

// ListVisibleApps lists all currently visible applications.
func (am *ApplicationManager) ListVisibleApps() ([]Process, error) {
	args := map[string]interface{}{}
	argsJSON, err := json.Marshal(args)
	if err != nil {
		return nil, fmt.Errorf("failed to marshal args: %w", err)
	}

	callToolRequest := &mcp.CallMcpToolRequest{
		Authorization: tea.String("Bearer " + am.Session.GetAPIKey()),
		SessionId:     tea.String(am.Session.GetSessionId()),
		Name:          tea.String("list_visible_apps"),
		Args:          tea.String(string(argsJSON)),
	}

	// Log API request
	fmt.Println("API Call: CallMcpTool - list_visible_apps")
	fmt.Printf("Request: SessionId=%s, Args=%s\n", *callToolRequest.SessionId, *callToolRequest.Args)

	response, err := am.Session.GetClient().CallMcpTool(callToolRequest)

	// Log API response
	if err != nil {
		fmt.Println("Error calling CallMcpTool - list_visible_apps:", err)
		return nil, fmt.Errorf("failed to list visible apps: %w", err)
	}
	if response != nil && response.Body != nil {
		fmt.Println("Response from CallMcpTool - list_visible_apps:", response.Body)
	}
	if err != nil {
		return nil, fmt.Errorf("failed to list visible apps: %w", err)
	}

	// Parse the response
	data, ok := response.Body.Data.(map[string]any)
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

	// Parse the JSON text to get the processes array
	var processes []Process
	if err := json.Unmarshal([]byte(jsonText), &processes); err != nil {
		return nil, fmt.Errorf("failed to unmarshal processes JSON: %w", err)
	}

	return processes, nil
}
