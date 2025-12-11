package agentbay

import (
	"encoding/json"
	"fmt"
	"net/http"
	"net/url"
	"strings"
	"time"

	"math/rand"

	"github.com/alibabacloud-go/tea/dara"
	"github.com/alibabacloud-go/tea/tea"
	mcp "github.com/aliyun/wuying-agentbay-sdk/golang/api/client"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/agent"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/browser"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/code"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/command"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/computer"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/filesystem"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/mobile"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/models"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/oss"
)

// SessionResult wraps Session object and RequestID
type SessionResult struct {
	models.ApiResponse
	Session      *Session
	Success      bool
	ErrorMessage string
}

// SessionListResult wraps Session list and RequestID
type SessionListResult struct {
	models.ApiResponse
	SessionIds []string // Session IDs
	NextToken  string   // Token for the next page
	MaxResults int32    // Number of results per page
	TotalCount int32    // Total number of results
}

// InfoResult wraps SessionInfo and RequestID
type InfoResult struct {
	models.ApiResponse
	Info *SessionInfo
}

// LabelResult wraps label operation result and RequestID
type LabelResult struct {
	models.ApiResponse
	Labels string
}

// LinkResult wraps link result and RequestID
type LinkResult struct {
	models.ApiResponse
	Link string
}

// DeleteResult wraps deletion operation result and RequestID
type DeleteResult struct {
	models.ApiResponse
	Success      bool
	ErrorMessage string
}

// McpTool represents an MCP tool with complete information
type McpTool struct {
	Name        string                 `json:"name"`        // Tool name
	Description string                 `json:"description"` // Tool description
	InputSchema map[string]interface{} `json:"inputSchema"` // Input parameter schema
	Server      string                 `json:"server"`      // Server name that provides this tool
	Tool        string                 `json:"tool"`        // Tool identifier
}

// GetName returns the tool name
func (m *McpTool) GetName() string {
	return m.Name
}

// GetServer returns the server name that provides this tool
func (m *McpTool) GetServer() string {
	return m.Server
}

// McpToolsResult wraps MCP tools list and RequestID
type McpToolsResult struct {
	models.ApiResponse
	Tools []McpTool
}

// SessionInfo contains information about a session.
type SessionInfo struct {
	SessionId            string
	ResourceUrl          string
	AppId                string
	AuthCode             string
	ConnectionProperties string
	ResourceId           string
	ResourceType         string
	Ticket               string
}

// Session represents a session in the AgentBay cloud environment.
type Session struct {
	AgentBay  *AgentBay
	SessionID string
	ImageId   string // ImageId used when creating this session

	// VPC-related information
	IsVpcEnabled       bool   // Whether this session uses VPC resources
	NetworkInterfaceIP string // Network interface IP for VPC sessions
	HttpPortNumber     string // HTTP port for VPC sessions
	Token              string // Token for VPC sessions

	// Resource URL for accessing the session
	ResourceUrl string

	// Browser replay enabled flag
	EnableBrowserReplay bool

	// File, command and code handlers
	FileSystem *filesystem.FileSystem
	Command    *command.Command
	Code       *code.Code
	Oss        *oss.OSSManager

	// Platform-specific automation modules
	Computer *computer.Computer
	Mobile   *mobile.Mobile

	// Browser for web automation
	Browser *browser.Browser

	// Agent for task execution
	Agent *agent.Agent

	// Context management
	Context *ContextManager

	// MCP tools available for this session
	McpTools []McpTool
}

// NewSession creates a new Session object.
func NewSession(agentBay *AgentBay, sessionID string) *Session {
	session := &Session{
		AgentBay:  agentBay,
		SessionID: sessionID,
	}

	// Initialize filesystem, command and code handlers
	session.FileSystem = filesystem.NewFileSystem(session)
	session.Command = command.NewCommand(session)
	session.Code = code.NewCode(session)
	session.Oss = oss.NewOss(session)

	// Initialize Browser
	session.Browser = browser.NewBrowser(session)

	// Initialize platform-specific automation modules
	session.Computer = computer.NewComputer(session)
	session.Mobile = mobile.NewMobile(session)

	// Initialize Agent
	session.Agent = agent.NewAgent(session)

	// Initialize context manager
	session.Context = NewContextManager(session)
	return session
}

// GetAPIKey returns the API key for this session.
func (s *Session) GetAPIKey() string {
	return s.AgentBay.APIKey
}

// GetClient returns the HTTP client for this session.
func (s *Session) GetClient() *mcp.Client {
	return s.AgentBay.Client
}

// GetSessionId returns the session ID for this session.
func (s *Session) GetSessionId() string {
	return s.SessionID
}

// GetImageID returns the image ID for this session.
func (s *Session) GetImageID() string {
	return s.ImageId
}

// GetSessionID returns the session ID for this session (browser interface method).
func (s *Session) GetSessionID() string {
	return s.SessionID
}

// GetEnableBrowserReplay returns whether browser replay is enabled for this session.
func (s *Session) GetEnableBrowserReplay() bool {
	return s.EnableBrowserReplay
}

// IsVPCEnabled returns whether this session uses VPC resources.
func (s *Session) IsVPCEnabled() bool {
	return s.IsVpcEnabled
}

// GetNetworkInterfaceIP returns the network interface IP for VPC sessions.
func (s *Session) GetNetworkInterfaceIP() string {
	return s.NetworkInterfaceIP
}

// GetHttpPortNumber returns the HTTP port for VPC sessions.
func (s *Session) GetHttpPortNumber() string {
	return s.HttpPortNumber
}

// Wrapper methods for browser.SessionInterface compatibility

// CallMcpTool is a wrapper that converts the result to browser.McpToolResult
func (s *Session) CallMcpToolForBrowser(toolName string, args interface{}) (*browser.McpToolResult, error) {
	result, err := s.CallMcpTool(toolName, args)
	if err != nil {
		return nil, err
	}

	// Convert models.McpToolResult to browser.McpToolResult
	return &browser.McpToolResult{
		Success:      result.Success,
		Data:         result.Data,
		ErrorMessage: result.ErrorMessage,
	}, nil
}

// GetLinkForBrowser is a wrapper that converts the result to browser.LinkResult
func (s *Session) GetLinkForBrowser(protocolType *string, port *int32, options *string) (*browser.LinkResult, error) {
	result, err := s.GetLink(protocolType, port, options)
	if err != nil {
		return nil, err
	}

	// Convert LinkResult to browser.LinkResult
	return &browser.LinkResult{
		Link: result.Link,
	}, nil
}

// GetCommand returns the command handler for this session.
func (s *Session) GetCommand() *command.Command {
	return s.Command
}

// Delete deletes this session.
// Delete deletes the session and releases all associated resources.
//
// Parameters:
//   - syncContext: Optional boolean to synchronize context data before deletion.
//     If true, uploads all context data to OSS. Defaults to false.
//
// Returns:
//   - *DeleteResult: Result containing success status and request ID
//   - error: Error if the operation fails
//
// Behavior:
//
// - If syncContext is true: Uploads all context data to OSS before deletion
// - If syncContext is false: Deletes immediately without sync
// - Continues with deletion even if context sync fails
// - Releases all associated resources (browser, computer, mobile, etc.)
//
// Example:
//
//	client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
//	result, _ := client.Create(nil)
//	defer result.Session.Delete()
//	deleteResult, _ := result.Session.Delete()
func (s *Session) Delete(syncContext ...bool) (*DeleteResult, error) {
	userRequestedSync := len(syncContext) > 0 && syncContext[0]

	if userRequestedSync {
		syncStartTime := time.Now()

		// Use the new sync method without callback (sync mode)
		var syncResult *ContextSyncResult
		var err error

		// Sync all contexts
		syncResult, err = s.Context.SyncWithCallback("", "", "", nil, 150, 1500)
		fmt.Printf("🔄 Synced all contexts\n")

		if err != nil {
			syncDuration := time.Since(syncStartTime)
			logOperationError("Delete", fmt.Sprintf("Failed to trigger context sync after %v: %v", syncDuration, err), false)
			// Continue with deletion even if sync fails
		} else {
			syncDuration := time.Since(syncStartTime)
			if syncResult.Success {
				// Context sync successful, continue silently (logged in SyncWithCallback)
				_ = syncDuration
			} else {
				// Context sync failed, continue with deletion
				_ = syncDuration
			}
		}
	}

	releaseSessionRequest := &mcp.ReleaseMcpSessionRequest{
		Authorization: tea.String("Bearer " + s.GetAPIKey()),
		SessionId:     tea.String(s.SessionID),
	}

	// Log API request
	requestParams := fmt.Sprintf("SessionId=%s", *releaseSessionRequest.SessionId)
	logAPICall("ReleaseMcpSession", requestParams)

	response, err := s.GetClient().ReleaseMcpSession(releaseSessionRequest)

	// Log API response
	if err != nil {
		logOperationError("ReleaseMcpSession", err.Error(), true)
		return nil, err
	}

	// Extract RequestID
	requestID := models.ExtractRequestID(response)

	// Check for API-level errors
	if response.Body != nil {
		if response.Body.Success != nil && !*response.Body.Success {
			errorMsg := "Failed to delete session"
			if response.Body.Code != nil && response.Body.Message != nil {
				errorMsg = fmt.Sprintf("[%s] %s", *response.Body.Code, *response.Body.Message)
			} else if response.Body.Code != nil {
				errorMsg = fmt.Sprintf("[%s] Failed to delete session", *response.Body.Code)
			}
			logOperationError("ReleaseMcpSession", errorMsg, false)
			return &DeleteResult{
				ApiResponse: models.ApiResponse{
					RequestID: requestID,
				},
				Success:      false,
				ErrorMessage: errorMsg,
			}, nil
		}
	}

	// Log successful deletion
	keyFields := map[string]interface{}{
		"session_id": s.SessionID,
	}
	responseJSON, _ := json.MarshalIndent(response.Body, "", "  ")
	logAPIResponseWithDetails("ReleaseMcpSession", requestID, true, keyFields, string(responseJSON))

	return &DeleteResult{
		ApiResponse: models.ApiResponse{
			RequestID: requestID,
		},
		Success: true,
	}, nil
}

// ValidateLabels validates labels parameter for label operations.
// Returns error message if validation fails, empty string if validation passes
func (s *Session) ValidateLabels(labels map[string]string) string {
	// Check if labels is nil
	if labels == nil {
		return "Labels cannot be nil. Please provide a valid labels map."
	}

	// Check if labels map is empty
	if len(labels) == 0 {
		return "Labels cannot be empty. Please provide at least one label."
	}

	for key, value := range labels {
		// Check key validity
		if key == "" || len(strings.TrimSpace(key)) == 0 {
			return "Label keys cannot be empty. Please provide valid keys."
		}

		// Check value validity
		if value == "" || len(strings.TrimSpace(value)) == 0 {
			return "Label values cannot be empty. Please provide valid values."
		}
	}

	// Validation passed
	return ""
}

// SetLabels sets the labels for this session.
//
// Parameters:
//   - labels: Labels to set for the session as a map of key-value pairs
//
// Returns:
//   - *LabelResult: Result containing request ID
//   - error: Error if validation fails or operation fails
//
// Behavior:
//
// - Validates that labels map is not nil or empty
// - All keys and values must be non-empty strings
// - Converts labels to JSON and sends to the backend
// - Labels can be used for session filtering and organization
//
// Example:
//
//	client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
//	result, _ := client.Create(nil)
//	defer result.Session.Delete()
//	labels := map[string]string{"env": "test"}
//	labelResult, _ := result.Session.SetLabels(labels)
func (s *Session) SetLabels(labels map[string]string) (*LabelResult, error) {
	// Validate labels using the validation function
	if validationError := s.ValidateLabels(labels); validationError != "" {
		return &LabelResult{
			ApiResponse: models.ApiResponse{
				RequestID: "",
			},
			Labels: "",
		}, fmt.Errorf("%s", validationError)
	}

	// Convert labels to JSON string
	labelsJSON, err := json.Marshal(labels)
	if err != nil {
		return &LabelResult{
			ApiResponse: models.ApiResponse{
				RequestID: "",
			},
			Labels: "",
		}, fmt.Errorf("failed to marshal labels to JSON: %v", err)
	}

	setLabelRequest := &mcp.SetLabelRequest{
		Authorization: tea.String("Bearer " + s.GetAPIKey()),
		Labels:        tea.String(string(labelsJSON)),
		SessionId:     tea.String(s.SessionID),
	}

	// Log API request
	requestParams := fmt.Sprintf("SessionId=%s, Labels=%s", *setLabelRequest.SessionId, *setLabelRequest.Labels)
	logAPICall("SetLabel", requestParams)

	response, err := s.GetClient().SetLabel(setLabelRequest)

	// Log API response
	if err != nil {
		logOperationError("SetLabel", err.Error(), true)
		return nil, err
	}

	// Extract RequestID
	requestID := models.ExtractRequestID(response)

	// Log successful response
	keyFields := map[string]interface{}{
		"session_id":   s.SessionID,
		"labels_count": len(labels),
	}
	responseJSON, _ := json.MarshalIndent(response.Body, "", "  ")
	logAPIResponseWithDetails("SetLabel", requestID, true, keyFields, string(responseJSON))

	return &LabelResult{
		ApiResponse: models.ApiResponse{
			RequestID: requestID,
		},
		Labels: string(labelsJSON),
	}, nil
}

// GetLabels gets the labels for this session.
//
// Returns:
//   - *LabelResult: Result containing labels as JSON string and request ID
//   - error: Error if the operation fails
//
// Behavior:
//
// - Retrieves the labels that were previously set for this session
// - Returns labels as a JSON string
// - Can be used to identify and filter sessions
//
// Example:
//
//	client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
//	result, _ := client.Create(nil)
//	defer result.Session.Delete()
//	labelResult, _ := result.Session.GetLabels()
func (s *Session) GetLabels() (*LabelResult, error) {
	getLabelRequest := &mcp.GetLabelRequest{
		Authorization: tea.String("Bearer " + s.GetAPIKey()),
		SessionId:     tea.String(s.SessionID),
	}

	// Log API request
	requestParams := fmt.Sprintf("SessionId=%s", *getLabelRequest.SessionId)
	logAPICall("GetLabel", requestParams)

	response, err := s.GetClient().GetLabel(getLabelRequest)

	// Log API response
	if err != nil {
		logOperationError("GetLabel", err.Error(), true)
		return nil, err
	}

	// Extract RequestID
	requestID := models.ExtractRequestID(response)

	var labels string
	var labelsCount int = 0
	if response != nil && response.Body != nil && response.Body.Data != nil && response.Body.Data.Labels != nil {
		labels = *response.Body.Data.Labels
		// Parse labels to count them
		var labelsMap map[string]interface{}
		if err := json.Unmarshal([]byte(labels), &labelsMap); err == nil {
			labelsCount = len(labelsMap)
		}
	}

	// Log successful response
	keyFields := map[string]interface{}{
		"session_id":   s.SessionID,
		"labels_count": labelsCount,
	}
	responseJSON, _ := json.MarshalIndent(response.Body, "", "  ")
	logAPIResponseWithDetails("GetLabel", requestID, true, keyFields, string(responseJSON))

	return &LabelResult{
		ApiResponse: models.ApiResponse{
			RequestID: requestID,
		},
		Labels: labels,
	}, nil
}

// GetLink gets the link for this session.
// GetLink retrieves an access link for the session.
//
// Parameters:
//   - protocolType: Protocol type for the link (optional, reserved for future use)
//   - port: Specific port number to access (must be in range [30100, 30199])
//   - options: Additional options (optional)
//
// Returns:
//   - *LinkResult: Result containing the access URL and request ID
//   - error: Error if port is out of range or operation fails
//
// Behavior:
//
// - Without port: Returns the default session access URL
// - With port: Returns URL for accessing specific port-mapped service
// - Port must be in range [30100, 30199] for port forwarding
//
// Example:
//
//	client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
//	result, _ := client.Create(nil)
//	defer result.Session.Delete()
//	port := int32(30100)
//	linkResult, _ := result.Session.GetLink(nil, &port, nil)
func (s *Session) GetLink(protocolType *string, port *int32, options *string) (*LinkResult, error) {
	// Validate port range if port is provided
	if port != nil {
		if *port < 30100 || *port > 30199 {
			return nil, fmt.Errorf("invalid port value: %d. Port must be an integer in the range [30100, 30199]", *port)
		}
	}

	getLinkRequest := &mcp.GetLinkRequest{
		Authorization: tea.String("Bearer " + s.GetAPIKey()),
		SessionId:     tea.String(s.SessionID),
		ProtocolType:  protocolType,
		Port:          port,
		Option:        options,
	}

	// Log API request
	requestParams := fmt.Sprintf("SessionId=%s", *getLinkRequest.SessionId)
	if getLinkRequest.ProtocolType != nil {
		requestParams += fmt.Sprintf(", ProtocolType=%s", *getLinkRequest.ProtocolType)
	}
	if getLinkRequest.Port != nil {
		requestParams += fmt.Sprintf(", Port=%d", *getLinkRequest.Port)
	}
	if getLinkRequest.Option != nil {
		requestParams += ", Options=provided"
	}
	logAPICall("GetLink", requestParams)

	response, err := s.GetClient().GetLink(getLinkRequest)

	// Log API response
	if err != nil {
		logOperationError("GetLink", err.Error(), true)
		return nil, err
	}

	// Extract RequestID
	requestID := models.ExtractRequestID(response)

	var link string
	if response != nil && response.Body != nil && response.Body.Data != nil {
		data := response.Body.Data
		if data.Url != nil {
			link = *data.Url
		}
	}

	// Log successful response
	keyFields := map[string]interface{}{
		"session_id": s.SessionID,
		"url":        link,
	}
	if getLinkRequest.ProtocolType != nil {
		keyFields["protocol_type"] = *getLinkRequest.ProtocolType
	}
	if getLinkRequest.Port != nil {
		keyFields["port"] = *getLinkRequest.Port
	}
	responseJSON, _ := json.MarshalIndent(response.Body, "", "  ")
	logAPIResponseWithDetails("GetLink", requestID, true, keyFields, string(responseJSON))

	return &LinkResult{
		ApiResponse: models.ApiResponse{
			RequestID: requestID,
		},
		Link: link,
	}, nil
}

// Info gets information about this session.
// Info retrieves detailed information about the current session.
//
// Returns:
//   - *InfoResult: Result containing SessionInfo object and request ID
//   - error: Error if the operation fails or session not found
//
// Behavior:
//
// - Retrieves current session metadata from the backend
// - Includes resource URL, type, and connection properties
// - Information is fetched in real-time from the API
//
// Example:
//
//	client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
//	result, _ := client.Create(nil)
//	defer result.Session.Delete()
//	infoResult, _ := result.Session.Info()
func (s *Session) Info() (*InfoResult, error) {
	getMcpResourceRequest := &mcp.GetMcpResourceRequest{
		Authorization: tea.String("Bearer " + s.GetAPIKey()),
		SessionId:     tea.String(s.SessionID),
	}

	// Log API request
	requestParams := fmt.Sprintf("SessionId=%s", *getMcpResourceRequest.SessionId)
	logAPICall("GetMcpResource", requestParams)

	response, err := s.GetClient().GetMcpResource(getMcpResourceRequest)

	// Log API response
	if err != nil {
		// Check if this is an expected business error (e.g., session not found)
		errorStr := err.Error()
		errorCode := ""

		// Try to extract error code from the error
		if strings.Contains(errorStr, "InvalidMcpSession.NotFound") || strings.Contains(errorStr, "NotFound") {
			errorCode = "InvalidMcpSession.NotFound"
		}

		if errorCode == "InvalidMcpSession.NotFound" {
			// This is an expected error - session doesn't exist
			// Use info level logging without stack trace, but with red color for visibility
			logInfoWithColor(fmt.Sprintf("Session not found: %s", s.SessionID))
			LogDebug(fmt.Sprintf("GetMcpResource error details: %s", errorStr))
			return &InfoResult{
				ApiResponse: models.ApiResponse{
					RequestID: "",
				},
				Info: nil,
			}, fmt.Errorf("Session %s not found", s.SessionID)
		}

		// This is an unexpected error - log with full error
		logOperationError("GetMcpResource", err.Error(), true)
		return nil, err
	}

	// Extract RequestID
	requestID := models.ExtractRequestID(response)

	if response != nil && response.Body != nil && response.Body.Data != nil {
		sessionInfo := &SessionInfo{
			SessionId:            "",
			ResourceUrl:          "",
			AppId:                "",
			AuthCode:             "",
			ConnectionProperties: "",
			ResourceId:           "",
			ResourceType:         "",
			Ticket:               "",
		}

		if response.Body.Data.SessionId != nil {
			sessionInfo.SessionId = *response.Body.Data.SessionId
		}

		if response.Body.Data.ResourceUrl != nil {
			sessionInfo.ResourceUrl = *response.Body.Data.ResourceUrl
		}

		// Transfer DesktopInfo fields to SessionInfo
		if response.Body.Data.DesktopInfo != nil {
			if response.Body.Data.DesktopInfo.AppId != nil {
				sessionInfo.AppId = *response.Body.Data.DesktopInfo.AppId
			}
			if response.Body.Data.DesktopInfo.AuthCode != nil {
				sessionInfo.AuthCode = *response.Body.Data.DesktopInfo.AuthCode
			}
			if response.Body.Data.DesktopInfo.ConnectionProperties != nil {
				sessionInfo.ConnectionProperties = *response.Body.Data.DesktopInfo.ConnectionProperties
			}
			if response.Body.Data.DesktopInfo.ResourceId != nil {
				sessionInfo.ResourceId = *response.Body.Data.DesktopInfo.ResourceId
			}
			if response.Body.Data.DesktopInfo.ResourceType != nil {
				sessionInfo.ResourceType = *response.Body.Data.DesktopInfo.ResourceType
			}
			if response.Body.Data.DesktopInfo.Ticket != nil {
				sessionInfo.Ticket = *response.Body.Data.DesktopInfo.Ticket
			}
		}

		// Log successful response
		keyFields := map[string]interface{}{
			"session_id":    sessionInfo.SessionId,
			"resource_url":  sessionInfo.ResourceUrl,
			"resource_type": sessionInfo.ResourceType,
		}
		if sessionInfo.AppId != "" {
			keyFields["app_id"] = sessionInfo.AppId
		}
		if sessionInfo.ResourceId != "" {
			keyFields["resource_id"] = sessionInfo.ResourceId
		}
		responseJSON, _ := json.MarshalIndent(response.Body, "", "  ")
		logAPIResponseWithDetails("GetMcpResource", requestID, true, keyFields, string(responseJSON))

		return &InfoResult{
			ApiResponse: models.ApiResponse{
				RequestID: requestID,
			},
			Info: sessionInfo,
		}, nil
	}

	return nil, fmt.Errorf("failed to get session info: empty response data")
}

// ListMcpTools lists MCP tools available for this session.
// It uses the ImageId from the session creation, or "linux_latest" as default.
//
// Returns:
//   - *McpToolsResult: Result containing list of MCP tools and request ID
//   - error: Error if the operation fails
//
// Behavior:
//
// - Uses the ImageId from session creation
// - Defaults to "linux_latest" if ImageId is empty
// - Retrieves all available MCP tools for the specified image
// - Updates the session's McpTools field with the retrieved tools
//
// Example:
//
//	client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
//	result, _ := client.Create(nil)
//	defer result.Session.Delete()
//	toolsResult, _ := result.Session.ListMcpTools()
func (s *Session) ListMcpTools() (*McpToolsResult, error) {
	// Use session's ImageId, or default to "linux_latest" if empty
	imageId := s.ImageId
	if imageId == "" {
		imageId = "linux_latest"
	}

	listMcpToolsRequest := &mcp.ListMcpToolsRequest{
		Authorization: tea.String("Bearer " + s.GetAPIKey()),
		ImageId:       tea.String(imageId),
	}

	// Log API request
	requestParams := fmt.Sprintf("ImageId=%s", *listMcpToolsRequest.ImageId)
	logAPICall("ListMcpTools", requestParams)

	response, err := s.GetClient().ListMcpTools(listMcpToolsRequest)

	// Log API response
	if err != nil {
		logOperationError("ListMcpTools", err.Error(), true)
		return nil, err
	}

	// Extract RequestID
	requestID := models.ExtractRequestID(response)

	// Parse the response data
	var tools []McpTool
	if response != nil && response.Body != nil && response.Body.Data != nil {
		// The Data field is a JSON string, so we need to unmarshal it
		var toolsData []map[string]interface{}
		if err := json.Unmarshal([]byte(*response.Body.Data), &toolsData); err != nil {
			logOperationError("ListMcpTools", fmt.Sprintf("Error unmarshaling tools data: %v", err), false)
			return &McpToolsResult{
				ApiResponse: models.ApiResponse{
					RequestID: requestID,
				},
				Tools: []McpTool{},
			}, nil
		}

		// Convert the parsed data to McpTool structs
		for _, toolData := range toolsData {
			tool := McpTool{}
			if name, ok := toolData["name"].(string); ok {
				tool.Name = name
			}
			if description, ok := toolData["description"].(string); ok {
				tool.Description = description
			}
			if inputSchema, ok := toolData["inputSchema"].(map[string]interface{}); ok {
				tool.InputSchema = inputSchema
			}
			if server, ok := toolData["server"].(string); ok {
				tool.Server = server
			}
			if toolIdentifier, ok := toolData["tool"].(string); ok {
				tool.Tool = toolIdentifier
			}
			tools = append(tools, tool)
		}
	}

	s.McpTools = tools // Update the session's McpTools field

	// Log successful response
	keyFields := map[string]interface{}{
		"image_id":    imageId,
		"tools_count": len(tools),
	}
	responseJSON, _ := json.MarshalIndent(response.Body, "", "  ")
	logAPIResponseWithDetails("ListMcpTools", requestID, true, keyFields, string(responseJSON))

	return &McpToolsResult{
		ApiResponse: models.ApiResponse{
			RequestID: requestID,
		},
		Tools: tools,
	}, nil
}

// IsVpc returns whether this session uses VPC resources
func (s *Session) IsVpc() bool {
	return s.IsVpcEnabled
}

// NetworkInterfaceIp returns the network interface IP for VPC sessions
func (s *Session) NetworkInterfaceIp() string {
	return s.NetworkInterfaceIP
}

// HttpPort returns the HTTP port for VPC sessions
func (s *Session) HttpPort() string {
	return s.HttpPortNumber
}

// GetToken returns the token for VPC sessions
func (s *Session) GetToken() string {
	return s.Token
}

// GetMcpTools returns the MCP tools available for this session
func (s *Session) GetMcpTools() []interface{} {
	result := make([]interface{}, len(s.McpTools))
	for i, tool := range s.McpTools {
		result[i] = &tool
	}
	return result
}

// FindServerForTool searches for the server that provides the given tool
func (s *Session) FindServerForTool(toolName string) string {
	for _, tool := range s.McpTools {
		if tool.Name == toolName {
			return tool.Server
		}
	}
	return ""
}

// CallMcpTool calls the MCP tool and handles both VPC and non-VPC scenarios
//
// This is the unified public API for calling MCP tools. All feature modules
// (Command, Code, Agent, etc.) use this method internally.
//
// Parameters:
//   - toolName: Name of the MCP tool to call
//   - args: Arguments to pass to the tool (typically a map or struct)
//   - autoGenSession: Optional boolean to auto-generate session if not exists (default: false)
//
// Returns:
//   - *models.McpToolResult: Result containing:
//   - Success: Whether the tool call was successful
//   - Data: Tool output data (text content extracted from response)
//   - ErrorMessage: Error message if the call failed
//   - RequestID: Unique identifier for the API request
//   - error: Error if the call fails at the transport level
//
// Behavior:
//
// - Automatically detects VPC vs non-VPC mode
// - In VPC mode, uses HTTP requests to the VPC endpoint
// - In non-VPC mode, uses traditional API calls
// - Parses response data to extract text content from content[0].text
// - Handles the isError flag in responses
// - Returns structured error information
//
// Example:
//
//	client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
//	result, _ := client.Create(nil)
//	defer result.Session.Delete()
//	args := map[string]interface{}{"command": "ls -la"}
//	toolResult, _ := result.Session.CallMcpTool("execute_command", args)
func (s *Session) CallMcpTool(toolName string, args interface{}, autoGenSession ...bool) (*models.McpToolResult, error) {
	// Normalize press_keys arguments for better case compatibility
	if toolName == "press_keys" {
		// Try to extract and normalize the keys field
		if argsMap, ok := args.(map[string]interface{}); ok {
			if keys, exists := argsMap["keys"]; exists {
				if keysArray, isArray := keys.([]interface{}); isArray {
					// Convert []interface{} to []string
					keysStr := make([]string, 0, len(keysArray))
					for _, k := range keysArray {
						if keyStr, isString := k.(string); isString {
							keysStr = append(keysStr, keyStr)
						}
					}
					// Normalize keys
					normalizedKeys := NormalizeKeys(keysStr)
					// Convert back to []interface{}
					normalizedKeysInterface := make([]interface{}, len(normalizedKeys))
					for i, k := range normalizedKeys {
						normalizedKeysInterface[i] = k
					}
					// Create a copy of args to avoid modifying the original
					argsCopy := make(map[string]interface{})
					for k, v := range argsMap {
						argsCopy[k] = v
					}
					argsCopy["keys"] = normalizedKeysInterface
					args = argsCopy
					LogDebug(fmt.Sprintf("Normalized press_keys arguments: %v", argsCopy))
				}
			}
		}
	}

	// Marshal arguments to JSON
	argsJSON, err := json.Marshal(args)
	if err != nil {
		return &models.McpToolResult{
			Success:      false,
			Data:         "",
			ErrorMessage: fmt.Sprintf("Failed to marshal args: %v", err),
			RequestID:    "",
		}, nil
	}

	// Extract autoGenSession parameter (default: false)
	autoGen := false
	if len(autoGenSession) > 0 {
		autoGen = autoGenSession[0]
	}

	// Check if this is a VPC session
	if s.IsVpc() {
		return s.callMcpToolVPC(toolName, string(argsJSON))
	}

	// Non-VPC mode: use traditional API call
	return s.callMcpToolAPI(toolName, string(argsJSON), autoGen)
}

// callMcpToolVPC handles VPC-based MCP tool calls
func (s *Session) callMcpToolVPC(toolName, argsJSON string) (*models.McpToolResult, error) {
	// VPC mode: Use HTTP request to the VPC endpoint
	requestParams := fmt.Sprintf("Tool=%s, ArgsLength=%d", toolName, len(argsJSON))
	logAPICall("CallMcpTool(VPC)", requestParams)

	// Find server for this tool
	server := s.FindServerForTool(toolName)
	if server == "" {
		logOperationError("CallMcpTool(VPC)", fmt.Sprintf("server not found for tool: %s", toolName), false)
		return &models.McpToolResult{
			Success:      false,
			Data:         "",
			ErrorMessage: fmt.Sprintf("server not found for tool: %s", toolName),
			RequestID:    "",
		}, nil
	}

	// Check VPC network configuration
	if s.NetworkInterfaceIp() == "" || s.HttpPort() == "" {
		logOperationError("CallMcpTool(VPC)", fmt.Sprintf("VPC network configuration incomplete: networkInterfaceIp=%s, httpPort=%s", s.NetworkInterfaceIp(), s.HttpPort()), false)
		return &models.McpToolResult{
			Success:      false,
			Data:         "",
			ErrorMessage: fmt.Sprintf("VPC network configuration incomplete: networkInterfaceIp=%s, httpPort=%s", s.NetworkInterfaceIp(), s.HttpPort()),
			RequestID:    "",
		}, nil
	}

	// Construct VPC URL with query parameters
	baseURL := fmt.Sprintf("http://%s:%s/callTool", s.NetworkInterfaceIp(), s.HttpPort())
	params := url.Values{}
	params.Add("server", server)
	params.Add("tool", toolName)
	params.Add("args", argsJSON)
	params.Add("token", s.GetToken())
	// Add requestId for debugging purposes
	requestID := fmt.Sprintf("vpc-%d-%d", time.Now().UnixMilli(), rand.Intn(1000000000))
	params.Add("requestId", requestID)

	fullURL := fmt.Sprintf("%s?%s", baseURL, params.Encode())

	// Send HTTP request
	response, err := http.Get(fullURL)
	if err != nil {
		logOperationError("CallMcpTool(VPC)", fmt.Sprintf("VPC request failed: %v", err), true)
		return &models.McpToolResult{
			Success:      false,
			Data:         "",
			ErrorMessage: fmt.Sprintf("VPC request failed: %v", err),
			RequestID:    "",
		}, nil
	}
	defer response.Body.Close()

	if response.StatusCode != http.StatusOK {
		logOperationError("CallMcpTool(VPC)", fmt.Sprintf("VPC request failed with status: %d", response.StatusCode), false)
		return &models.McpToolResult{
			Success:      false,
			Data:         "",
			ErrorMessage: fmt.Sprintf("VPC request failed with status: %d", response.StatusCode),
			RequestID:    "",
		}, nil
	}

	// Parse response
	var responseData interface{}
	if err := json.NewDecoder(response.Body).Decode(&responseData); err != nil {
		logOperationError("CallMcpTool(VPC)", fmt.Sprintf("Failed to parse VPC response: %v", err), true)
		return &models.McpToolResult{
			Success:      false,
			Data:         "",
			ErrorMessage: fmt.Sprintf("Failed to parse VPC response: %v", err),
			RequestID:    "",
		}, nil
	}

	// Extract text content from the response
	textContent := s.extractTextContentFromResponse(responseData)

	// Log successful VPC call
	keyFields := map[string]interface{}{
		"tool_name":       toolName,
		"server":          server,
		"network_ip":      s.NetworkInterfaceIp(),
		"port":            s.HttpPort(),
		"response_length": len(textContent),
	}
	responseJSON, _ := json.Marshal(responseData)
	logAPIResponseWithDetails("CallMcpTool(VPC)", requestID, true, keyFields, string(responseJSON))

	// For run_code tool, extract and log the actual code execution output
	if toolName == "run_code" && textContent != "" {
		logCodeExecutionOutput(requestID, textContent)
	}

	return &models.McpToolResult{
		Success:      true,
		Data:         textContent,
		ErrorMessage: "",
		RequestID:    requestID, // Include the generated request ID
	}, nil
}

// callMcpToolAPI handles traditional API-based MCP tool calls
func (s *Session) callMcpToolAPI(toolName, argsJSON string, autoGenSession bool) (*models.McpToolResult, error) {
	// Helper function to convert string to *string
	stringPtr := func(s string) *string { return &s }
	boolPtr := func(b bool) *bool { return &b }

	callToolRequest := &mcp.CallMcpToolRequest{
		Authorization:  stringPtr(fmt.Sprintf("Bearer %s", s.GetAPIKey())),
		SessionId:      stringPtr(s.SessionID),
		Name:           stringPtr(toolName),
		Args:           stringPtr(argsJSON),
		AutoGenSession: boolPtr(autoGenSession),
		ExternalUserId: stringPtr(""),
		ImageId:        stringPtr(""),
	}

	// Log API request
	requestParams := fmt.Sprintf("Tool=%s, SessionId=%s, ArgsLength=%d", toolName, s.SessionID, len(argsJSON))
	logAPICall("CallMcpTool", requestParams)

	response, err := s.GetClient().CallMcpTool(callToolRequest)

	// Log API response
	if err != nil {
		logOperationError("CallMcpTool", fmt.Sprintf("API request failed: %v", err), true)
		return &models.McpToolResult{
			Success:      false,
			Data:         "",
			ErrorMessage: fmt.Sprintf("API request failed: %v", err),
			RequestID:    "",
		}, nil
	}

	// Extract request ID
	requestID := ""
	if response.Body != nil && response.Body.GetRequestId() != nil {
		requestID = *response.Body.GetRequestId()
	}

	// Check for API-level errors
	if response.Body != nil && response.Body.Data != nil {
		// Log successful response
		var responseLength int = 0
		if dataStr, ok := response.Body.Data.(string); ok {
			responseLength = len(dataStr)
		}

		keyFields := map[string]interface{}{
			"tool_name":       toolName,
			"session_id":      s.SessionID,
			"response_length": responseLength,
		}
		responseJSON, _ := json.MarshalIndent(response.Body, "", "  ")
		logAPIResponseWithDetails("CallMcpTool", requestID, true, keyFields, string(responseJSON))

		// For run_code tool, extract and log the actual code execution output
		if toolName == "run_code" && response.Body.Data != nil {
			var dataStr string
			if str, ok := response.Body.Data.(string); ok {
				dataStr = str
			} else if dataBytes, err := json.Marshal(response.Body.Data); err == nil {
				dataStr = string(dataBytes)
			}
			if dataStr != "" {
				logCodeExecutionOutput(requestID, dataStr)
			}
		}

		// Parse response data to extract text content
		var dataObj map[string]interface{}
		if str, ok := response.Body.Data.(string); ok {
			// If data is a string, try to parse it as JSON
			if err := json.Unmarshal([]byte(str), &dataObj); err != nil {
				// If parsing fails, return the raw string
				return &models.McpToolResult{
					Success:      true,
					Data:         str,
					ErrorMessage: "",
					RequestID:    requestID,
				}, nil
			}
		} else if obj, ok := response.Body.Data.(map[string]interface{}); ok {
			// If data is already a map, use it directly
			dataObj = obj
		} else {
			// For other types, try to marshal and unmarshal
			if dataBytes, err := json.Marshal(response.Body.Data); err == nil {
				if err := json.Unmarshal(dataBytes, &dataObj); err != nil {
					// If parsing fails, return the marshaled string
					return &models.McpToolResult{
						Success:      true,
						Data:         string(dataBytes),
						ErrorMessage: "",
						RequestID:    requestID,
					}, nil
				}
			}
		}

		// Extract text content from the parsed data
		textContent := s.extractTextContentFromResponse(dataObj)

		// Check for errors in the response
		isError := false
		if isErrorVal, exists := dataObj["isError"]; exists {
			if isErrorBool, ok := isErrorVal.(bool); ok {
				isError = isErrorBool
			}
		}

		if isError {
			logOperationError("CallMcpTool", fmt.Sprintf("Tool returned error: %s", textContent), false)
			return &models.McpToolResult{
				Success:      false,
				Data:         "",
				ErrorMessage: textContent,
				RequestID:    requestID,
			}, nil
		}

		return &models.McpToolResult{
			Success:      true,
			Data:         textContent,
			ErrorMessage: "",
			RequestID:    requestID,
		}, nil
	}

	// Handle empty or error response
	errorMsg := "Empty response from CallMcpTool"
	logOperationError("CallMcpTool", errorMsg, false)
	return &models.McpToolResult{
		Success:      false,
		Data:         "",
		ErrorMessage: errorMsg,
		RequestID:    requestID,
	}, nil
}

// extractTextContentFromResponse extracts text content from various response formats
func (s *Session) extractTextContentFromResponse(data interface{}) string {
	if data == nil {
		return ""
	}

	// Try to extract text from different response formats
	if dataMap, ok := data.(map[string]interface{}); ok {
		// Check for content array first
		if content, exists := dataMap["content"]; exists {
			if contentArray, isArray := content.([]interface{}); isArray && len(contentArray) > 0 {
				if contentItem, isMap := contentArray[0].(map[string]interface{}); isMap {
					if text, textExists := contentItem["text"]; textExists {
						if textStr, isString := text.(string); isString {
							return textStr
						}
					}
				}
			}
		}

		// Check for direct result field
		if result, exists := dataMap["result"]; exists {
			if resultMap, isMap := result.(map[string]interface{}); isMap {
				if content, contentExists := resultMap["content"]; contentExists {
					if contentArray, isArray := content.([]interface{}); isArray && len(contentArray) > 0 {
						if contentItem, isMap := contentArray[0].(map[string]interface{}); isMap {
							if text, textExists := contentItem["text"]; textExists {
								if textStr, isString := text.(string); isString {
									return textStr
								}
							}
						}
					}
				}
			}
		}
	}

	// If no text content found, return JSON representation
	if dataBytes, err := json.Marshal(data); err == nil {
		return string(dataBytes)
	}

	return ""
}

// Pause synchronously pauses this session, putting it into a dormant state to reduce resource usage and costs.
// Pause puts the session into a PAUSED state where computational resources are significantly reduced.
// The session state is preserved and can be resumed later to continue work.
//
// Parameters:
//   - timeout: Timeout in seconds to wait for the session to pause. Defaults to 600 seconds.
//   - pollInterval: Interval in seconds between status polls. Defaults to 2.0 seconds.
//
// Returns:
//   - *models.SessionPauseResult: Result containing success status, request ID, and error message if any.
//   - error: Error if the operation fails at the transport level
//
// Behavior:
//
// - Initiates pause operation through the PauseSessionAsync API
// - Polls session status until PAUSED state or timeout
// - Returns detailed result with success status and request tracking
//
// Exceptions:
//
// - Returns error result (not Go error) for API-level errors like invalid session ID
// - Returns error result for timeout conditions
// - Returns Go error for transport-level failures
//
// Example:
//
//	client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"))
//	result, _ := client.Create(nil)
//	defer result.Session.Delete()
//	pauseResult, _ := result.Session.Pause(300, 2.0)
func (s *Session) Pause(timeout int, pollInterval float64) (*models.SessionPauseResult, error) {
	// Set default values if not provided
	if timeout <= 0 {
		timeout = 600
	}
	if pollInterval <= 0 {
		pollInterval = 2.0
	}

	// Create pause request
	request := &mcp.PauseSessionAsyncRequest{}
	request.SetAuthorization(fmt.Sprintf("Bearer %s", s.GetAPIKey()))
	request.SetSessionId(s.SessionID)

	// Call PauseSessionAsync API to initiate the pause operation
	response, err := s.GetClient().PauseSessionAsync(request)
	if err != nil {
		return &models.SessionPauseResult{
			ApiResponse:  models.WithRequestID(""),
			Success:      false,
			ErrorMessage: fmt.Sprintf("Failed to call PauseSessionAsync API: %v", err),
		}, nil
	}

	// Extract request ID
	requestID := models.ExtractRequestID(response)

	// Check for API-level errors
	if response.Body == nil {
		return &models.SessionPauseResult{
			ApiResponse:  models.WithRequestID(requestID),
			Success:      false,
			ErrorMessage: "Invalid response body",
		}, nil
	}

	body := response.Body
	if !dara.IsNil(body.Success) && !*body.Success {
		errorMessage := fmt.Sprintf("[%s] %s", tea.StringValue(body.Code), tea.StringValue(body.Message))
		if errorMessage == "[]" {
			errorMessage = "Unknown error"
		}
		return &models.SessionPauseResult{
			ApiResponse:  models.WithRequestID(requestID),
			Success:      false,
			ErrorMessage: errorMessage,
			Code:         tea.StringValue(body.Code),
			Message:      tea.StringValue(body.Message),
			HTTPCode:     tea.Int32Value(body.HttpStatusCode),
		}, nil
	}

	// Pause initiated successfully
	fmt.Printf("PauseSessionAsync: Session %s pause initiated successfully\n", s.SessionID)

	// Poll for session status until PAUSED or timeout
	startTime := time.Now()
	maxAttempts := int(float64(timeout) / pollInterval)

	for attempt := 0; attempt < maxAttempts; attempt++ {
		// Get session status
		getSessionResult, err := s.AgentBay.GetSession(s.SessionID)
		if err != nil || !getSessionResult.Success {
			errorMessage := "Failed to get session status"
			if err != nil {
				errorMessage = fmt.Sprintf("Failed to get session status: %v", err)
			} else if getSessionResult.ErrorMessage != "" {
				errorMessage = fmt.Sprintf("Failed to get session status: %s", getSessionResult.ErrorMessage)
			}
			return &models.SessionPauseResult{
				ApiResponse:  models.WithRequestID(getSessionResult.GetRequestID()),
				Success:      false,
				ErrorMessage: errorMessage,
			}, nil
		}

		// Check session status
		if getSessionResult.Data != nil {
			status := getSessionResult.Data.Status
			if status == "" {
				status = "UNKNOWN"
			}
			fmt.Printf("Session status: %s (attempt %d/%d)\n", status, attempt+1, maxAttempts)

			// Check if session is paused
			if status == "PAUSED" {
				elapsed := time.Since(startTime)
				fmt.Printf("Session paused successfully in %v\n", elapsed)
				return &models.SessionPauseResult{
					ApiResponse: models.WithRequestID(getSessionResult.GetRequestID()),
					Success:     true,
					Status:      status,
				}, nil
			} else if status == "PAUSING" {
				// Normal transitioning state, continue polling
			} else {
				// Any other status is unexpected - pause API succeeded but session is not pausing/paused
				elapsed := time.Since(startTime)
				errorMessage := fmt.Sprintf("Session pause failed: unexpected state '%s' after %v", status, elapsed)
				fmt.Printf("%s\n", errorMessage)
				return &models.SessionPauseResult{
					ApiResponse:  models.WithRequestID(getSessionResult.GetRequestID()),
					Success:      false,
					ErrorMessage: errorMessage,
					Status:       status,
				}, nil
			}
		}

		// Wait before next query (using time.Sleep to avoid blocking)
		// Only wait if we're not at the last attempt
		if attempt < maxAttempts-1 {
			time.Sleep(time.Duration(pollInterval*1000) * time.Millisecond)
		}
	}

	// Timeout
	elapsed := time.Since(startTime)
	errorMessage := fmt.Sprintf("Session pause timed out after %v", elapsed)
	fmt.Printf("ERROR: %s\n", errorMessage)
	return &models.SessionPauseResult{
		ApiResponse:  models.WithRequestID(""),
		Success:      false,
		ErrorMessage: errorMessage,
	}, nil
}

// Resume synchronously resumes this session from a paused state to continue work.
// Resume restores the session from PAUSED state back to RUNNING state.
// All previous session state and data are preserved during resume operation.
//
// Parameters:
//   - timeout: Timeout in seconds to wait for the session to resume. Defaults to 600 seconds.
//   - pollInterval: Interval in seconds between status polls. Defaults to 2.0 seconds.
//
// Returns:
//   - *models.SessionResumeResult: Result containing success status, request ID, and error message if any.
//   - error: Error if the operation fails at the transport level
//
// Behavior:
//
// - Initiates resume operation through the ResumeSessionAsync API
// - Polls session status until RUNNING state or timeout
// - Returns detailed result with success status and request tracking
//
// Exceptions:
//
// - Returns error result (not Go error) for API-level errors like invalid session ID
// - Returns error result for timeout conditions
// - Returns Go error for transport-level failures
//
// Example:
//
//	client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"))
//	result, _ := client.Create(nil)
//	defer result.Session.Delete()
//	result.Session.Pause(300, 2.0)
//	resumeResult, _ := result.Session.Resume(300, 2.0)
func (s *Session) Resume(timeout int, pollInterval float64) (*models.SessionResumeResult, error) {
	// Set default values if not provided
	if timeout <= 0 {
		timeout = 600
	}
	if pollInterval <= 0 {
		pollInterval = 2.0
	}

	// Create resume request
	request := &mcp.ResumeSessionAsyncRequest{}
	request.SetAuthorization(fmt.Sprintf("Bearer %s", s.GetAPIKey()))
	request.SetSessionId(s.SessionID)

	// Call ResumeSessionAsync API to initiate the resume operation
	response, err := s.GetClient().ResumeSessionAsync(request)
	if err != nil {
		return &models.SessionResumeResult{
			ApiResponse:  models.WithRequestID(""),
			Success:      false,
			ErrorMessage: fmt.Sprintf("Failed to call ResumeSessionAsync API: %v", err),
		}, nil
	}

	// Extract request ID
	requestID := models.ExtractRequestID(response)

	// Check for API-level errors
	if response.Body == nil {
		return &models.SessionResumeResult{
			ApiResponse:  models.WithRequestID(requestID),
			Success:      false,
			ErrorMessage: "Invalid response body",
		}, nil
	}

	body := response.Body
	if !dara.IsNil(body.Success) && !*body.Success {
		errorMessage := fmt.Sprintf("[%s] %s", tea.StringValue(body.Code), tea.StringValue(body.Message))
		if errorMessage == "[]" {
			errorMessage = "Unknown error"
		}
		return &models.SessionResumeResult{
			ApiResponse:  models.WithRequestID(requestID),
			Success:      false,
			ErrorMessage: errorMessage,
			Code:         tea.StringValue(body.Code),
			Message:      tea.StringValue(body.Message),
			HTTPCode:     tea.Int32Value(body.HttpStatusCode),
		}, nil
	}

	// Resume initiated successfully
	fmt.Printf("ResumeSessionAsync: Session %s resume initiated successfully\n", s.SessionID)

	// Poll for session status until RUNNING or timeout
	startTime := time.Now()
	maxAttempts := int(float64(timeout) / pollInterval)

	for attempt := 0; attempt < maxAttempts; attempt++ {
		// Get session status
		getSessionResult, err := s.AgentBay.GetSession(s.SessionID)
		if err != nil || !getSessionResult.Success {
			errorMessage := "Failed to get session status"
			if err != nil {
				errorMessage = fmt.Sprintf("Failed to get session status: %v", err)
			} else if getSessionResult.ErrorMessage != "" {
				errorMessage = fmt.Sprintf("Failed to get session status: %s", getSessionResult.ErrorMessage)
			}
			return &models.SessionResumeResult{
				ApiResponse:  models.WithRequestID(getSessionResult.GetRequestID()),
				Success:      false,
				ErrorMessage: errorMessage,
			}, nil
		}

		// Check session status
		if getSessionResult.Data != nil {
			status := getSessionResult.Data.Status
			if status == "" {
				status = "UNKNOWN"
			}
			fmt.Printf("Session status: %s (attempt %d/%d)\n", status, attempt+1, maxAttempts)

			// Check if session is running
			if status == "RUNNING" {
				elapsed := time.Since(startTime)
				fmt.Printf("Session resumed successfully in %v\n", elapsed)
				return &models.SessionResumeResult{
					ApiResponse: models.WithRequestID(getSessionResult.GetRequestID()),
					Success:     true,
					Status:      status,
				}, nil
			} else if status == "RESUMING" {
				// Normal transitioning state, continue polling
			} else {
				// Any other status is unexpected - resume API succeeded but session is not resuming/running
				elapsed := time.Since(startTime)
				errorMessage := fmt.Sprintf("Session resume failed: unexpected state '%s' after %v", status, elapsed)
				fmt.Printf("%s\n", errorMessage)
				return &models.SessionResumeResult{
					ApiResponse:  models.WithRequestID(getSessionResult.GetRequestID()),
					Success:      false,
					ErrorMessage: errorMessage,
					Status:       status,
				}, nil
			}
		}

		// Wait before next query (using time.Sleep to avoid blocking)
		// Only wait if we're not at the last attempt
		if attempt < maxAttempts-1 {
			time.Sleep(time.Duration(pollInterval*1000) * time.Millisecond)
		}
	}

	// Timeout
	elapsed := time.Since(startTime)
	errorMessage := fmt.Sprintf("Session resume timed out after %v", elapsed)
	fmt.Printf("ERROR: %s\n", errorMessage)
	return &models.SessionResumeResult{
		ApiResponse:  models.WithRequestID(""),
		Success:      false,
		ErrorMessage: errorMessage,
	}, nil
}
