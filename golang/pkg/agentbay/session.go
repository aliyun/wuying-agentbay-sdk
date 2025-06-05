package agentbay

import (
	"fmt"

	"github.com/alibabacloud-go/tea/tea"
	mcp "github.com/aliyun/wuying-agentbay-sdk/golang/api/client"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/adb"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/application"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/command"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/filesystem"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/window"
)

// Session represents a session in the AgentBay cloud environment.
type Session struct {
	AgentBay  *AgentBay
	SessionID string

	// File, command, and adb handlers
	FileSystem *filesystem.FileSystem
	Command    *command.Command
	Adb        *adb.Adb

	// Application and window management
	Application *application.ApplicationManager
	Window      *window.WindowManager
}

// NewSession creates a new Session object.
func NewSession(agentBay *AgentBay, sessionID string) *Session {
	session := &Session{
		AgentBay:  agentBay,
		SessionID: sessionID,
	}

	// Initialize filesystem, command, and adb handlers
	session.FileSystem = filesystem.NewFileSystem(session)
	session.Command = command.NewCommand(session)
	session.Adb = adb.NewAdb(session)

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
func (s *Session) Delete() error {
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
		return err
	}
	if response != nil && response.Body != nil {
		fmt.Println("Response from ReleaseMcpSession:", response.Body)
	}

	s.AgentBay.Sessions.Delete(s.SessionID)
	return nil
}

// SetLabels sets the labels for this session.
func (s *Session) SetLabels(labels string) error {
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
		return err
	}
	if response != nil && response.Body != nil {
		fmt.Println("Response from SetLabel:", response.Body)
	}

	return nil
}

// GetLabels gets the labels for this session.
func (s *Session) GetLabels() (string, error) {
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
		return "", err
	}
	if response != nil && response.Body != nil {
		fmt.Println("Response from GetLabel:", response.Body)
	}

	if response != nil && response.Body != nil && response.Body.Data != nil && response.Body.Data.Labels != nil {
		return *response.Body.Data.Labels, nil
	}

	return "", nil
}
