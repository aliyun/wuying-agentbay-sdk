package agentbay

import (
	"fmt"

	"github.com/alibabacloud-go/tea/tea"
	mcp "github.com/aliyun/wuying-agentbay-sdk/golang/api/client"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/adb"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/command"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/filesystem"
)

// Session represents a session in the AgentBay cloud environment.
type Session struct {
	AgentBay  *AgentBay
	SessionID string

	// File, command, and adb handlers
	FileSystem *filesystem.FileSystem
	Command    *command.Command
	Adb        *adb.Adb
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
	response, err := s.GetClient().ReleaseMcpSession(releaseSessionRequest)
	if err != nil {
		fmt.Println("Error calling releaseSessionRequest:", err)
		return err
	}
	fmt.Println(response)
	s.AgentBay.Sessions.Delete(s.SessionID)
	return nil
}
