package interfaces

import (
	"github.com/aliyun/wuying-agentbay-sdk/golang/api/client"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

//go:generate mockgen -destination=../../../tests/pkg/unit/mock/mock_agentbay.go -package=mock github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/interface AgentBayInterface

// AgentBayInterface defines the interface for AgentBay operations
type AgentBayInterface interface {
	// GetAPIKey gets the API Key
	GetAPIKey() string

	// GetClient gets the client
	GetClient() *client.Client

	// Create creates a new session
	Create(params *agentbay.CreateSessionParams) (*agentbay.SessionResult, error)

	// Delete deletes a session
	Delete(session *agentbay.Session) (*agentbay.DeleteResult, error)

	// List lists all sessions
	List() (*agentbay.SessionListResult, error)

	// ListByLabels lists sessions by labels with pagination
	ListByLabels(params *agentbay.ListSessionParams) (*agentbay.SessionListResult, error)
}
