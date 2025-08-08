package agentbay_test

import (
	"testing"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
	"github.com/aliyun/wuying-agentbay-sdk/golang/tests/pkg/unit/mock"
	"github.com/golang/mock/gomock"
	"github.com/stretchr/testify/assert"
)

func TestAgentBay_Create_WithMockClient(t *testing.T) {
	ctrl := gomock.NewController(t)
	defer ctrl.Finish()

	// Create mock AgentBay
	mockAgentBay := mock.NewMockAgentBayInterface(ctrl)

	// Set expected behavior
	params := &agentbay.CreateSessionParams{
		Labels: map[string]string{"env": "test"},
	}
	expectedResult := &agentbay.SessionResult{
		Session: &agentbay.Session{
			SessionID:   "new_session_id",
			ResourceUrl: "http://example.com",
		},
	}
	mockAgentBay.EXPECT().Create(params).Return(expectedResult, nil)

	// Test Create method call
	result, err := mockAgentBay.Create(params)

	// Verify call success
	assert.NoError(t, err)
	assert.NotNil(t, result)
	assert.Equal(t, "new_session_id", result.Session.SessionID)
}

func TestAgentBay_Delete_WithMockClient(t *testing.T) {
	ctrl := gomock.NewController(t)
	defer ctrl.Finish()

	// Create mock AgentBay
	mockAgentBay := mock.NewMockAgentBayInterface(ctrl)

	// Set expected behavior
	session := &agentbay.Session{
		SessionID: "test_session_id",
	}
	expectedResult := &agentbay.DeleteResult{
		Success: true,
	}
	mockAgentBay.EXPECT().Delete(session).Return(expectedResult, nil)

	// Test Delete method call
	result, err := mockAgentBay.Delete(session)

	// Verify call success
	assert.NoError(t, err)
	assert.NotNil(t, result)
	assert.True(t, result.Success)
}

func TestAgentBay_List_WithMockClient(t *testing.T) {
	ctrl := gomock.NewController(t)
	defer ctrl.Finish()

	// Create mock AgentBay
	mockAgentBay := mock.NewMockAgentBayInterface(ctrl)

	// Set expected behavior
	expectedResult := &agentbay.SessionListResult{
		Sessions: []agentbay.Session{
			{SessionID: "session-1"},
			{SessionID: "session-2"},
		},
		NextToken:  "next-page-token",
		MaxResults: 5,
		TotalCount: 15,
	}
	mockAgentBay.EXPECT().List().Return(expectedResult, nil)

	// Test List method call
	result, err := mockAgentBay.List()

	// Verify call success
	assert.NoError(t, err)
	assert.NotNil(t, result)
	assert.Len(t, result.Sessions, 2)
	assert.Equal(t, "session-1", result.Sessions[0].SessionID)
	assert.Equal(t, "session-2", result.Sessions[1].SessionID)
	assert.Equal(t, "next-page-token", result.NextToken)
	assert.Equal(t, int32(5), result.MaxResults)
	assert.Equal(t, int32(15), result.TotalCount)
}

func TestAgentBay_ListByLabels_WithMockClient(t *testing.T) {
	ctrl := gomock.NewController(t)
	defer ctrl.Finish()

	// Create mock AgentBay
	mockAgentBay := mock.NewMockAgentBayInterface(ctrl)

	// Set expected behavior
	params := &agentbay.ListSessionParams{
		MaxResults: 10,
		NextToken:  "next-token",
		Labels:     map[string]string{"env": "test"},
	}
	expectedResult := &agentbay.SessionListResult{
		Sessions: []agentbay.Session{
			{SessionID: "session-1"},
			{SessionID: "session-2"},
		},
		NextToken:  "next-page-token",
		MaxResults: 10,
		TotalCount: 20,
	}
	mockAgentBay.EXPECT().ListByLabels(params).Return(expectedResult, nil)

	// Test ListByLabels method call
	result, err := mockAgentBay.ListByLabels(params)

	// Verify call success
	assert.NoError(t, err)
	assert.NotNil(t, result)
	assert.Len(t, result.Sessions, 2)
	assert.Equal(t, "session-1", result.Sessions[0].SessionID)
	assert.Equal(t, "session-2", result.Sessions[1].SessionID)
	assert.Equal(t, "next-page-token", result.NextToken)
	assert.Equal(t, int32(10), result.MaxResults)
	assert.Equal(t, int32(20), result.TotalCount)
}

func TestAgentBay_Error_WithMockClient(t *testing.T) {
	ctrl := gomock.NewController(t)
	defer ctrl.Finish()

	// Create mock AgentBay
	mockAgentBay := mock.NewMockAgentBayInterface(ctrl)

	// Set expected behavior - return error
	mockAgentBay.EXPECT().List().Return(nil, assert.AnError)

	// Test error case
	result, err := mockAgentBay.List()

	// Verify error handling
	assert.Error(t, err)
	assert.Nil(t, result)
}
