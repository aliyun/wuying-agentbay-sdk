package interfaces

import (
	"github.com/aliyun/wuying-agentbay-sdk/golang/api/client"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

//go:generate mockgen -destination=../../../tests/pkg/unit/mock/mock_session.go -package=mock github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/interface SessionInterface

// SessionInterface defines the interface for session operations
type SessionInterface interface {
	// GetAPIKey returns the API key
	GetAPIKey() string

	// GetClient returns the client instance
	GetClient() *client.Client

	// GetSessionId returns the session ID
	GetSessionId() string

	// Delete deletes this session
	Delete() (*agentbay.DeleteResult, error)

	// SetLabels sets the labels for this session
	SetLabels(labels string) (*agentbay.LabelResult, error)

	// GetLabels gets the labels for this session
	GetLabels() (*agentbay.LabelResult, error)

	// GetLink gets the link for this session
	GetLink(protocolType *string, port *int32) (*agentbay.LinkResult, error)

	// Info gets information about this session
	Info() (*agentbay.InfoResult, error)
}
