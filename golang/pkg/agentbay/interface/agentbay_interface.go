package interfaces

import (
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

//go:generate mockgen -destination=../../../tests/pkg/unit/mock/mock_agentbay.go -package=mock github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/interface AgentBayInterface

// AgentBayInterface defines the interface for AgentBay operations
type AgentBayInterface interface {
	// Create creates a new session
	Create(params *agentbay.CreateSessionParams) (*agentbay.SessionResult, error)

	// Delete deletes a session
	Delete(session *agentbay.Session, syncContext ...bool) (*agentbay.DeleteResult, error)


	// ListByLabels lists sessions by labels with pagination
	ListByLabels(params *agentbay.ListSessionParams) (*agentbay.SessionListResult, error)
}
