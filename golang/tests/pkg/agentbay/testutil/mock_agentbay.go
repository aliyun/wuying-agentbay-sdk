package testutil

import (
	"github.com/alibabacloud-go/tea/tea"
	"github.com/aliyun/wuying-agentbay-sdk/golang/api/client"
	"github.com/stretchr/testify/mock"
)

// MockAgentBay is a mock implementation of AgentBay for testing
type MockAgentBay struct {
	mock.Mock
}

// GetAPIKey mocks the GetAPIKey method
func (m *MockAgentBay) GetAPIKey() string {
	args := m.Called()
	return args.String(0)
}

// GetClient mocks the GetClient method
func (m *MockAgentBay) GetClient() *client.Client {
	args := m.Called()
	return args.Get(0).(*client.Client)
}

// Sessions mocks the Sessions field
func (m *MockAgentBay) Sessions() interface{} {
	args := m.Called()
	return args.Get(0)
}

// MockClient is a mock implementation of the client for testing
type MockClient struct {
	mock.Mock
}

// ReleaseMcpSession mocks the ReleaseMcpSession method (deprecated, use DeleteSessionAsync)
func (m *MockClient) ReleaseMcpSession(request *client.ReleaseMcpSessionRequest) (*client.ReleaseMcpSessionResponse, error) {
	args := m.Called(request)
	if args.Get(0) == nil {
		return nil, args.Error(1)
	}
	return args.Get(0).(*client.ReleaseMcpSessionResponse), args.Error(1)
}

// DeleteSessionAsync mocks the DeleteSessionAsync method
func (m *MockClient) DeleteSessionAsync(request *client.DeleteSessionAsyncRequest) (*client.DeleteSessionAsyncResponse, error) {
	args := m.Called(request)
	if args.Get(0) == nil {
		return nil, args.Error(1)
	}
	return args.Get(0).(*client.DeleteSessionAsyncResponse), args.Error(1)
}

// GetSession mocks the GetSession method
func (m *MockClient) GetSession(request *client.GetSessionRequest) (*client.GetSessionResponse, error) {
	args := m.Called(request)
	if args.Get(0) == nil {
		return nil, args.Error(1)
	}
	return args.Get(0).(*client.GetSessionResponse), args.Error(1)
}

// CreateMockReleaseMcpSessionResponse creates a mock response for ReleaseMcpSession (deprecated)
func CreateMockReleaseMcpSessionResponse(success bool, requestID string) *client.ReleaseMcpSessionResponse {
	response := &client.ReleaseMcpSessionResponse{}
	response.Body = &client.ReleaseMcpSessionResponseBody{
		RequestId: tea.String(requestID),
		Success:   tea.Bool(success),
	}
	return response
}

// CreateMockDeleteSessionAsyncResponse creates a mock response for DeleteSessionAsync
func CreateMockDeleteSessionAsyncResponse(success bool, requestID string) *client.DeleteSessionAsyncResponse {
	response := &client.DeleteSessionAsyncResponse{}
	response.Body = &client.DeleteSessionAsyncResponseBody{
		RequestId: tea.String(requestID),
		Success:   tea.Bool(success),
	}
	return response
}

// CreateMockGetSessionResponse creates a mock response for GetSession
// status can be "RUNNING", "FINISH", "PAUSED", etc.
// If status is "FINISH" or returns NotFound error, it means session is deleted
func CreateMockGetSessionResponse(sessionID string, status string, success bool, requestID string) *client.GetSessionResponse {
	response := &client.GetSessionResponse{}
	response.Body = &client.GetSessionResponseBody{
		RequestId: tea.String(requestID),
	}
	if success {
		response.Body.Data = &client.GetSessionResponseBodyData{
			SessionId: tea.String(sessionID),
			Status:    tea.String(status),
		}
	}
	return response
}
