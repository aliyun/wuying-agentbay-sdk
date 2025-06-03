package agentbay

import (
	"fmt"
	"os"
	"sync"

	openapi "github.com/alibabacloud-go/darabonba-openapi/v2/client"
	"github.com/alibabacloud-go/tea/tea"
	mcp "github.com/aliyun/wuying-agentbay-sdk/golang/api/client"
)

// AgentBay represents the main client for interacting with the AgentBay cloud runtime environment.
type AgentBay struct {
	APIKey   string
	RegionId string
	Client   *mcp.Client
	Sessions sync.Map
}

// NewAgentBay creates a new AgentBay client.
// If apiKey is empty, it will look for the AGENTBAY_API_KEY environment variable.
func NewAgentBay(apiKey string) (*AgentBay, error) {
	if apiKey == "" {
		apiKey = os.Getenv("AGENTBAY_API_KEY")
		if apiKey == "" {
			return nil, fmt.Errorf("API key is required. Provide it as a parameter or set the AGENTBAY_API_KEY environment variable")
		}
	}

	// Load configuration
	config := LoadConfig()

	// 创建 OpenAPI 客户端配置
	apiConfig := &openapi.Config{
		RegionId: tea.String(config.RegionID),
		Endpoint: tea.String(config.Endpoint),
	}
	apiConfig.ReadTimeout = tea.Int(config.TimeoutMs)
	client, err := mcp.NewClient(apiConfig)
	if err != nil {
		return nil, fmt.Errorf("create openapi client fails")
	}

	return &AgentBay{
		APIKey:   apiKey,
		RegionId: config.RegionID,
		Client:   client,
	}, nil
}

// Create creates a new session in the AgentBay cloud environment.
func (a *AgentBay) Create() (*Session, error) {
	createSessionRequest := &mcp.CreateMcpSessionRequest{
		Authorization: tea.String("Bearer " + a.APIKey),
	}
	response, err := a.Client.CreateMcpSession(createSessionRequest)
	if err != nil {
		fmt.Println("Error calling createSessionRequest:", err)
		return nil, err
	}
	fmt.Println(response)
	// 使用 session.go 中的 Create 函数创建新的 Session
	session := NewSession(a, *response.Body.Data.SessionId)
	a.Sessions.Store(session.SessionID, *session)
	return session, nil
}

// List lists all available sessions.
func (a *AgentBay) List() ([]Session, error) {
	var sessions []Session
	a.Sessions.Range(func(key, value interface{}) bool {
		if session, ok := value.(Session); ok {
			sessions = append(sessions, session)
		}
		return true
	})
	return sessions, nil
}

// Delete deletes a session by ID.
func (a *AgentBay) Delete(session *Session) error {
	err := session.Delete()
	if err == nil {
		a.Sessions.Delete(session.SessionID)
	}
	return err
}
