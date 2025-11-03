package mock

import (
	mcp "github.com/aliyun/wuying-agentbay-sdk/golang/api/client"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/models"
	"github.com/stretchr/testify/mock"
)

// MockSessionForComputer is a mock implementation of the session interface for Computer/Mobile testing
type MockSessionForComputer struct {
	mock.Mock
}

// GetAPIKey returns the API key
func (m *MockSessionForComputer) GetAPIKey() string {
	args := m.Called()
	return args.String(0)
}

// GetClient returns the client instance
func (m *MockSessionForComputer) GetClient() *mcp.Client {
	args := m.Called()
	return args.Get(0).(*mcp.Client)
}

// GetSessionId returns the session ID
func (m *MockSessionForComputer) GetSessionId() string {
	args := m.Called()
	return args.String(0)
}

// IsVpc returns whether this session uses VPC resources
func (m *MockSessionForComputer) IsVpc() bool {
	args := m.Called()
	return args.Bool(0)
}

// NetworkInterfaceIp returns the network interface IP for VPC sessions
func (m *MockSessionForComputer) NetworkInterfaceIp() string {
	args := m.Called()
	return args.String(0)
}

// HttpPort returns the HTTP port for VPC sessions
func (m *MockSessionForComputer) HttpPort() string {
	args := m.Called()
	return args.String(0)
}

// FindServerForTool searches for the server that provides the given tool
func (m *MockSessionForComputer) FindServerForTool(toolName string) string {
	args := m.Called(toolName)
	return args.String(0)
}

// CallMcpTool calls an MCP tool with the given arguments
func (m *MockSessionForComputer) CallMcpTool(toolName string, args interface{}, autoGenSession ...bool) (*models.McpToolResult, error) {
	mockArgs := m.Called(toolName, args)
	return mockArgs.Get(0).(*models.McpToolResult), mockArgs.Error(1)
}

// GetImageID returns the image ID for this session
func (m *MockSessionForComputer) GetImageID() string {
	args := m.Called()
	return args.String(0)
}

// GetLink gets the link for this session
func (m *MockSessionForComputer) GetLink(protocolType *string, port *int32, options *string) (*agentbay.LinkResult, error) {
	args := m.Called(protocolType, port, options)
	if args.Get(0) == nil {
		return nil, args.Error(1)
	}
	return args.Get(0).(*agentbay.LinkResult), args.Error(1)
}
