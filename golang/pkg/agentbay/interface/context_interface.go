package interfaces

import (
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

//go:generate mockgen -destination=../../../tests/pkg/unit/mock/mock_context.go -package=mock github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/interface ContextInterface

// ContextInterface defines the interface for context operations
type ContextInterface interface {
	// List lists all available contexts with pagination support
	List(params *agentbay.ContextListParams) (*agentbay.ContextListResult, error)

	// Get gets a context by name, optionally creates it if it doesn't exist
	Get(name string, create bool) (*agentbay.ContextResult, error)

	// Create creates a new context with the given name
	Create(name string) (*agentbay.ContextCreateResult, error)

	// Update updates the specified context
	Update(context *agentbay.Context) (*agentbay.ContextModifyResult, error)

	// Delete deletes the specified context
	Delete(context *agentbay.Context) (*agentbay.ContextDeleteResult, error)
}
