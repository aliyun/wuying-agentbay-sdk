package agentbay

import (
	"fmt"

	"github.com/alibabacloud-go/tea/tea"
	mcp "github.com/aliyun/wuying-agentbay-sdk/golang/api/client"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/application"
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
	Sessions []Session
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

// SessionInfo contains information about a session.
type SessionInfo struct {
	SessionId            string
	ResourceUrl          string
	AppId                string
	AuthCode             string
	ConnectionProperties string
	ResourceId           string
	ResourceType         string
}

// Session represents a session in the AgentBay cloud environment.
type Session struct {
	AgentBay    *AgentBay
	SessionID   string
	ResourceUrl string

	// File and command handlers
	FileSystem *filesystem.FileSystem
	Command    *command.Command
	Oss        *oss.OSSManager

	// UI, application and window management
	UI          *ui.UIManager
	Application *application.ApplicationManager
	Window      *window.WindowManager
}

// NewSession creates a new Session object.
func NewSession(agentBay *AgentBay, sessionID string) *Session {
	session := &Session{
		AgentBay:  agentBay,
		SessionID: sessionID,
	}

	// Initialize filesystem and command handlers
	session.FileSystem = filesystem.NewFileSystem(session)
	session.Command = command.NewCommand(session)
	session.Oss = oss.NewOss(session)

	// Initialize UI
	session.UI = ui.NewUI(session)

	// Initialize application and window managers
	session.Application = application.NewApplicationManager(session)
	session.Window = window.NewWindowManager(session)
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
func (s *Session) Delete() (*DeleteResult, error) {
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
func (s *Session) GetLink() (*LinkResult, error) {
	getLinkRequest := &mcp.GetLinkRequest{
		Authorization: tea.String("Bearer " + s.GetAPIKey()),
		SessionId:     tea.String(s.SessionID),
	}

	// Log API request
	fmt.Println("API Call: GetLink")
	fmt.Printf("Request: SessionId=%s\n", *getLinkRequest.SessionId)

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
		link = *response.Body.Data
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
