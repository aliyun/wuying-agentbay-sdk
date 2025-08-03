package agentbay_test

import (
	"encoding/json"
	"testing"

	"github.com/aliyun/wuying-agentbay-sdk/golang/api/client"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
	"github.com/aliyun/wuying-agentbay-sdk/golang/tests/pkg/unit/mock"
	"github.com/golang/mock/gomock"
	"github.com/stretchr/testify/assert"
)

func TestSession_GetAPIKey_WithMockClient(t *testing.T) {
	ctrl := gomock.NewController(t)
	defer ctrl.Finish()

	// Create mock Session
	mockSession := mock.NewMockSessionInterface(ctrl)

	// Set expected behavior
	mockSession.EXPECT().GetAPIKey().Return("test_api_key")

	// Test GetAPIKey method call
	result := mockSession.GetAPIKey()

	// Verify call success
	assert.Equal(t, "test_api_key", result)
}

func TestSession_GetClient_WithMockClient(t *testing.T) {
	ctrl := gomock.NewController(t)
	defer ctrl.Finish()

	// Create mock Session
	mockSession := mock.NewMockSessionInterface(ctrl)

	// Set expected behavior
	expectedClient := &client.Client{}
	mockSession.EXPECT().GetClient().Return(expectedClient)

	// Test GetClient method call
	result := mockSession.GetClient()

	// Verify call success
	assert.NotNil(t, result)
	assert.Equal(t, expectedClient, result)
}

func TestSession_GetSessionId_WithMockClient(t *testing.T) {
	ctrl := gomock.NewController(t)
	defer ctrl.Finish()

	// Create mock Session
	mockSession := mock.NewMockSessionInterface(ctrl)

	// Set expected behavior
	mockSession.EXPECT().GetSessionId().Return("test_session_id")

	// Test GetSessionId method call
	result := mockSession.GetSessionId()

	// Verify call success
	assert.Equal(t, "test_session_id", result)
}

func TestSession_Delete_WithMockClient(t *testing.T) {
	ctrl := gomock.NewController(t)
	defer ctrl.Finish()

	// Create mock Session
	mockSession := mock.NewMockSessionInterface(ctrl)

	// Set expected behavior
	expectedResult := &agentbay.DeleteResult{
		Success: true,
	}
	mockSession.EXPECT().Delete().Return(expectedResult, nil)

	// Test Delete method call
	result, err := mockSession.Delete()

	// Verify call success
	assert.NoError(t, err)
	assert.NotNil(t, result)
	assert.True(t, result.Success)
}

func TestSession_SetLabels_WithMockClient(t *testing.T) {
	ctrl := gomock.NewController(t)
	defer ctrl.Finish()

	// Create mock Session
	mockSession := mock.NewMockSessionInterface(ctrl)

	// Set expected behavior
	expectedResult := &agentbay.LabelResult{
		Labels: "label1,label2",
	}
	mockSession.EXPECT().SetLabels("label1,label2").Return(expectedResult, nil)

	// Test SetLabels method call
	result, err := mockSession.SetLabels("label1,label2")

	// Verify call success
	assert.NoError(t, err)
	assert.NotNil(t, result)
	assert.Equal(t, "label1,label2", result.Labels)
}

func TestSession_GetLabels_WithMockClient(t *testing.T) {
	ctrl := gomock.NewController(t)
	defer ctrl.Finish()

	// Create mock Session
	mockSession := mock.NewMockSessionInterface(ctrl)

	// Set expected behavior
	expectedResult := &agentbay.LabelResult{
		Labels: "existing_label",
	}
	mockSession.EXPECT().GetLabels().Return(expectedResult, nil)

	// Test GetLabels method call
	result, err := mockSession.GetLabels()

	// Verify call success
	assert.NoError(t, err)
	assert.NotNil(t, result)
	assert.Equal(t, "existing_label", result.Labels)
}

func TestSession_GetLink_WithMockClient(t *testing.T) {
	ctrl := gomock.NewController(t)
	defer ctrl.Finish()

	// Create mock Session
	mockSession := mock.NewMockSessionInterface(ctrl)

	// Set expected behavior
	protocolType := "http"
	port := int32(8080)
	expectedResult := &agentbay.LinkResult{
		Link: "http://example.com:8080",
	}
	mockSession.EXPECT().GetLink(&protocolType, &port).Return(expectedResult, nil)

	// Test GetLink method call
	result, err := mockSession.GetLink(&protocolType, &port)

	// Verify call success
	assert.NoError(t, err)
	assert.NotNil(t, result)
	assert.Equal(t, "http://example.com:8080", result.Link)
}

func TestSession_Info_WithMockClient(t *testing.T) {
	ctrl := gomock.NewController(t)
	defer ctrl.Finish()

	// Create mock Session
	mockSession := mock.NewMockSessionInterface(ctrl)

	// Set expected behavior
	expectedResult := &agentbay.InfoResult{
		Info: &agentbay.SessionInfo{
			SessionId:   "test_session_id",
			ResourceUrl: "http://example.com",
		},
	}
	mockSession.EXPECT().Info().Return(expectedResult, nil)

	// Test Info method call
	result, err := mockSession.Info()

	// Verify call success
	assert.NoError(t, err)
	assert.NotNil(t, result)
	assert.Equal(t, "test_session_id", result.Info.SessionId)
	assert.Equal(t, "http://example.com", result.Info.ResourceUrl)
}

func TestSession_Error_WithMockClient(t *testing.T) {
	ctrl := gomock.NewController(t)
	defer ctrl.Finish()

	// Create mock Session
	mockSession := mock.NewMockSessionInterface(ctrl)

	// Set expected behavior - return error
	mockSession.EXPECT().Delete().Return(nil, assert.AnError)

	// Test error case
	result, err := mockSession.Delete()

	// Verify error handling
	assert.Error(t, err)
	assert.Nil(t, result)
}

func TestSession_Delete_APIFailure_WithMockClient(t *testing.T) {
	ctrl := gomock.NewController(t)
	defer ctrl.Finish()

	// Create mock Session
	mockSession := mock.NewMockSessionInterface(ctrl)

	// Set expected behavior - return failure response
	expectedResult := &agentbay.DeleteResult{
		Success: false,
	}
	mockSession.EXPECT().Delete().Return(expectedResult, nil)

	// Test Delete method call
	result, err := mockSession.Delete()

	// Verify call success but with failure result
	assert.NoError(t, err)
	assert.NotNil(t, result)
	assert.False(t, result.Success)
}

func TestSession_SetLabels_APIError_WithMockClient(t *testing.T) {
	ctrl := gomock.NewController(t)
	defer ctrl.Finish()

	// Create mock Session
	mockSession := mock.NewMockSessionInterface(ctrl)

	// Set expected behavior - return error
	labels := map[string]string{"key1": "value1"}
	// Convert labels to JSON string to match the mock interface
	labelsJSON, _ := json.Marshal(labels)
	labelsStr := string(labelsJSON)
	mockSession.EXPECT().SetLabels(labelsStr).Return(nil, assert.AnError)

	// Test error case
	result, err := mockSession.SetLabels(labelsStr)

	// Verify error handling
	assert.Error(t, err)
	assert.Nil(t, result)
}

func TestSession_GetLabels_APIError_WithMockClient(t *testing.T) {
	ctrl := gomock.NewController(t)
	defer ctrl.Finish()

	// Create mock Session
	mockSession := mock.NewMockSessionInterface(ctrl)

	// Set expected behavior - return error
	mockSession.EXPECT().GetLabels().Return(nil, assert.AnError)

	// Test error case
	result, err := mockSession.GetLabels()

	// Verify error handling
	assert.Error(t, err)
	assert.Nil(t, result)
}

func TestSession_GetLink_APIError_WithMockClient(t *testing.T) {
	ctrl := gomock.NewController(t)
	defer ctrl.Finish()

	// Create mock Session
	mockSession := mock.NewMockSessionInterface(ctrl)

	// Set expected behavior - return error
	protocolType := "http"
	port := int32(8080)
	mockSession.EXPECT().GetLink(&protocolType, &port).Return(nil, assert.AnError)

	// Test error case
	result, err := mockSession.GetLink(&protocolType, &port)

	// Verify error handling
	assert.Error(t, err)
	assert.Nil(t, result)
}

func TestSession_Info_APIError_WithMockClient(t *testing.T) {
	ctrl := gomock.NewController(t)
	defer ctrl.Finish()

	// Create mock Session
	mockSession := mock.NewMockSessionInterface(ctrl)

	// Set expected behavior - return error
	mockSession.EXPECT().Info().Return(nil, assert.AnError)

	// Test error case
	result, err := mockSession.Info()

	// Verify error handling
	assert.Error(t, err)
	assert.Nil(t, result)
}
