package agentbay

import (
	"encoding/json"
	"fmt"
	"time"

	"github.com/alibabacloud-go/tea/tea"
	mcp "github.com/aliyun/wuying-agentbay-sdk/golang/api/client"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/application"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/code"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/command"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/filesystem"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/models"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/oss"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/ui"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/window"
)

// SessionResult wraps Session object and RequestID
type SessionResult struct {
	models.ApiResponse
	Session *Session
}

// SessionListResult wraps Session list and RequestID
type SessionListResult struct {
	models.ApiResponse
	Sessions   []Session
	NextToken  string // Token for the next page
	MaxResults int32  // Number of results per page
	TotalCount int32  // Total number of results
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
	Success bool
}

// McpTool represents an MCP tool with complete information
type McpTool struct {
	Name        string                 `json:"name"`        // Tool name
	Description string                 `json:"description"` // Tool description
	InputSchema map[string]interface{} `json:"inputSchema"` // Input parameter schema
	Server      string                 `json:"server"`      // Server name that provides this tool
	Tool        string                 `json:"tool"`        // Tool identifier
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
	AgentBay    *AgentBay
	SessionID   string
	ResourceUrl string
	ImageId     string // ImageId used when creating this session

	// File, command and code handlers
	FileSystem *filesystem.FileSystem
	Command    *command.Command
	Code       *code.Code
	Oss        *oss.OSSManager

	// UI, application and window management
	UI          *ui.UIManager
	Application *application.ApplicationManager
	Window      *window.WindowManager

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

	// Initialize UI
	session.UI = ui.NewUI(session)

	// Initialize application and window managers
	session.Application = application.NewApplicationManager(session)
	session.Window = window.NewWindowManager(session)

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

// Delete deletes this session.
func (s *Session) Delete(syncContext ...bool) (*DeleteResult, error) {
	shouldSync := len(syncContext) > 0 && syncContext[0]

	// If syncContext is true, trigger file uploads first
	if shouldSync {
		fmt.Println("Triggering context synchronization before session deletion...")

		// Trigger file upload
		syncResult, err := s.Context.Sync()
		if err != nil {
			fmt.Printf("Warning: Failed to trigger context sync: %v\n", err)
			// Continue with deletion even if sync fails
		} else if !syncResult.Success {
			fmt.Println("Warning: Context sync operation returned failure status")
			// Continue with deletion even if sync fails
		}

		// Wait for uploads to complete
		const maxRetries = 150  // Maximum number of retries
		const retryInterval = 2 // Seconds to wait between retries

		for retry := 0; retry < maxRetries; retry++ {
			// Get context status data
			infoResult, err := s.Context.Info()
			if err != nil {
				fmt.Printf("Error getting context info on attempt %d: %v\n", retry+1, err)
				time.Sleep(time.Duration(retryInterval) * time.Second)
				continue
			}

			// Check if all upload context items have status "Success" or "Failed"
			allCompleted := true
			hasFailure := false
			hasUploads := false

			for _, item := range infoResult.ContextStatusData {
				// We only care about upload tasks
				if item.TaskType != "upload" {
					continue
				}

				hasUploads = true
				fmt.Printf("Upload context %s status: %s, path: %s\n", item.ContextId, item.Status, item.Path)

				if item.Status != "Success" && item.Status != "Failed" {
					allCompleted = false
					break
				}

				if item.Status == "Failed" {
					hasFailure = true
					fmt.Printf("Upload failed for context %s: %s\n", item.ContextId, item.ErrorMessage)
				}
			}

			if allCompleted || !hasUploads {
				if hasFailure {
					fmt.Println("Context upload completed with failures")
				} else if hasUploads {
					fmt.Println("Context upload completed successfully")
				} else {
					fmt.Println("No upload tasks found")
				}
				break
			}

			fmt.Printf("Waiting for context upload to complete, attempt %d/%d\n", retry+1, maxRetries)
			time.Sleep(time.Duration(retryInterval) * time.Second)
		}
	}

	releaseSessionRequest := &mcp.ReleaseMcpSessionRequest{
		Authorization: tea.String("Bearer " + s.GetAPIKey()),
		SessionId:     tea.String(s.SessionID),
	}

	// Log API request
	fmt.Println("API Call: ReleaseMcpSession")
	fmt.Printf("Request: SessionId=%s\n", *releaseSessionRequest.SessionId)

	response, err := s.GetClient().ReleaseMcpSession(releaseSessionRequest)

	// Log API response
	if err != nil {
		fmt.Println("Error calling ReleaseMcpSession:", err)
		return nil, err
	}

	// Extract RequestID
	requestID := models.ExtractRequestID(response)

	if response != nil && response.Body != nil {
		fmt.Println("Response from ReleaseMcpSession:", response.Body)
	}

	// Check if the response is success
	success := true
	if response != nil && response.Body != nil {
		// Default to true if Success field doesn't exist
		if response.Body.Success != nil {
			success = *response.Body.Success
		}
	}

	if !success {
		return &DeleteResult{
			ApiResponse: models.ApiResponse{
				RequestID: requestID,
			},
			Success: false,
		}, nil
	}

	s.AgentBay.Sessions.Delete(s.SessionID)

	return &DeleteResult{
		ApiResponse: models.ApiResponse{
			RequestID: requestID,
		},
		Success: true,
	}, nil
}

// SetLabels sets the labels for this session.
func (s *Session) SetLabels(labels string) (*LabelResult, error) {
	setLabelRequest := &mcp.SetLabelRequest{
		Authorization: tea.String("Bearer " + s.GetAPIKey()),
		Labels:        tea.String(labels),
		SessionId:     tea.String(s.SessionID),
	}

	// Log API request
	fmt.Println("API Call: SetLabel")
	fmt.Printf("Request: SessionId=%s, Labels=%s\n", *setLabelRequest.SessionId, *setLabelRequest.Labels)

	response, err := s.GetClient().SetLabel(setLabelRequest)

	// Log API response
	if err != nil {
		fmt.Println("Error calling SetLabel:", err)
		return nil, err
	}

	// Extract RequestID
	requestID := models.ExtractRequestID(response)

	if response != nil && response.Body != nil {
		fmt.Println("Response from SetLabel:", response.Body)
	}

	return &LabelResult{
		ApiResponse: models.ApiResponse{
			RequestID: requestID,
		},
		Labels: labels,
	}, nil
}

// GetLabels gets the labels for this session.
func (s *Session) GetLabels() (*LabelResult, error) {
	getLabelRequest := &mcp.GetLabelRequest{
		Authorization: tea.String("Bearer " + s.GetAPIKey()),
		SessionId:     tea.String(s.SessionID),
	}

	// Log API request
	fmt.Println("API Call: GetLabel")
	fmt.Printf("Request: SessionId=%s\n", *getLabelRequest.SessionId)

	response, err := s.GetClient().GetLabel(getLabelRequest)

	// Log API response
	if err != nil {
		fmt.Println("Error calling GetLabel:", err)
		return nil, err
	}

	// Extract RequestID
	requestID := models.ExtractRequestID(response)

	if response != nil && response.Body != nil {
		fmt.Println("Response from GetLabel:", response.Body)
	}

	var labels string
	if response != nil && response.Body != nil && response.Body.Data != nil && response.Body.Data.Labels != nil {
		labels = *response.Body.Data.Labels
	}

	return &LabelResult{
		ApiResponse: models.ApiResponse{
			RequestID: requestID,
		},
		Labels: labels,
	}, nil
}

// GetLink gets the link for this session.
func (s *Session) GetLink(protocolType *string, port *int32) (*LinkResult, error) {
	getLinkRequest := &mcp.GetLinkRequest{
		Authorization: tea.String("Bearer " + s.GetAPIKey()),
		SessionId:     tea.String(s.SessionID),
		ProtocolType:  protocolType,
		Port:          port,
	}

	// Log API request
	fmt.Println("API Call: GetLink")
	fmt.Printf("Request: SessionId=%s", *getLinkRequest.SessionId)
	if getLinkRequest.ProtocolType != nil {
		fmt.Printf(", ProtocolType=%s", *getLinkRequest.ProtocolType)
	}
	if getLinkRequest.Port != nil {
		fmt.Printf(", Port=%d", *getLinkRequest.Port)
	}
	fmt.Println()

	response, err := s.GetClient().GetLink(getLinkRequest)

	// Log API response
	if err != nil {
		fmt.Println("Error calling GetLink:", err)
		return nil, err
	}

	// Extract RequestID
	requestID := models.ExtractRequestID(response)

	if response != nil && response.Body != nil {
		fmt.Println("Response from GetLink:", response.Body)
	}

	var link string
	if response != nil && response.Body != nil && response.Body.Data != nil {
		data := response.Body.Data
		fmt.Printf("Data: %v\n", data)
		if data.Url != nil {
			link = *data.Url
		}
	}

	return &LinkResult{
		ApiResponse: models.ApiResponse{
			RequestID: requestID,
		},
		Link: link,
	}, nil
}

// Info gets information about this session.
func (s *Session) Info() (*InfoResult, error) {
	getMcpResourceRequest := &mcp.GetMcpResourceRequest{
		Authorization: tea.String("Bearer " + s.GetAPIKey()),
		SessionId:     tea.String(s.SessionID),
	}

	// Log API request
	fmt.Println("API Call: GetMcpResource")
	fmt.Printf("Request: SessionId=%s\n", *getMcpResourceRequest.SessionId)

	response, err := s.GetClient().GetMcpResource(getMcpResourceRequest)

	// Log API response
	if err != nil {
		fmt.Println("Error calling GetMcpResource:", err)
		return nil, err
	}

	// Extract RequestID
	requestID := models.ExtractRequestID(response)

	if response != nil && response.Body != nil {
		fmt.Println("Response from GetMcpResource:", response.Body)
	}

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
			// Update the session's ResourceUrl with the latest value
			s.ResourceUrl = *response.Body.Data.ResourceUrl
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
	fmt.Println("API Call: ListMcpTools")
	fmt.Printf("Request: ImageId=%s\n", *listMcpToolsRequest.ImageId)

	response, err := s.GetClient().ListMcpTools(listMcpToolsRequest)

	// Log API response
	if err != nil {
		fmt.Println("Error calling ListMcpTools:", err)
		return nil, err
	}

	// Extract RequestID
	requestID := models.ExtractRequestID(response)

	if response != nil && response.Body != nil {
		fmt.Println("Response from ListMcpTools:", response.Body)
	}

	// Parse the response data
	var tools []McpTool
	if response != nil && response.Body != nil && response.Body.Data != nil {
		// The Data field is a JSON string, so we need to unmarshal it
		var toolsData []map[string]interface{}
		if err := json.Unmarshal([]byte(*response.Body.Data), &toolsData); err != nil {
			fmt.Printf("Error unmarshaling tools data: %v\n", err)
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

	return &McpToolsResult{
		ApiResponse: models.ApiResponse{
			RequestID: requestID,
		},
		Tools: tools,
	}, nil
}
