package interfaces

import (
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/models"
)

//go:generate mockgen -destination=../../../tests/pkg/unit/mock/mock_agentbay.go -package=mock github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/interface AgentBayInterface

// AgentBayInterface defines the interface for AgentBay operations
type AgentBayInterface interface {
	// Create creates a new session
	Create(params *agentbay.CreateSessionParams) (*agentbay.SessionResult, error)

	// Delete deletes a session
	Delete(session *agentbay.Session, syncContext ...bool) (*agentbay.DeleteResult, error)

	// List returns paginated list of Sessions filtered by labels
	List(labels map[string]string, page *int, limit *int32) (*agentbay.SessionListResult, error)

	// Pause synchronously pauses a session
	Pause(session *agentbay.Session, timeout int, pollInterval float64) (*models.SessionPauseResult, error)

	// Resume synchronously resumes a session
	Resume(session *agentbay.Session, timeout int, pollInterval float64) (*models.SessionResumeResult, error)
}
