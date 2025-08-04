package agentbay_test

import (
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
	labels := map[string]string{"key1": "label1", "key2": "label2"}
	expectedResult := &agentbay.LabelResult{
		Labels: "label1,label2",
	}
	mockSession.EXPECT().SetLabels(labels).Return(expectedResult, nil)

	// Test SetLabels method call
	result, err := mockSession.SetLabels(labels)

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
	mockSession.EXPECT().SetLabels(labels).Return(nil, assert.AnError)

	// Test error case
	result, err := mockSession.SetLabels(labels)

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

func TestSession_ListMcpTools_WithMockClient(t *testing.T) {
	ctrl := gomock.NewController(t)
	defer ctrl.Finish()

	// Create mock Session
	mockSession := mock.NewMockSessionInterface(ctrl)

	// Set expected behavior based on the actual API response from integration test
	tools := []agentbay.McpTool{
		{
			Name:        "get_resource",
			Description: "The command to retrieve  a wuying mcp runtime URL when user wants to get access to this runtime. Each retrieved URL will expire after a single use",
			InputSchema: map[string]interface{}{
				"type":       "object",
				"properties": map[string]interface{}{},
				"required":   []interface{}{},
			},
			Server: "mcp-server",
			Tool:   "get_resource",
		},
		{
			Name:        "system_screenshot",
			Description: "Captures a full-screen screenshot of the current display and returns a shareable URL. The screenshot is automatically processed and stored securely. The generated URL will expire after 64 minutes for security purposes.",
			InputSchema: map[string]interface{}{
				"type":       "object",
				"properties": map[string]interface{}{},
				"required":   []interface{}{},
			},
			Server: "mcp-server",
			Tool:   "system_screenshot",
		},
	}
	expectedResult := &agentbay.McpToolsResult{
		Tools: tools,
	}
	expectedResult.RequestID = "test-request-id"
	
	mockSession.EXPECT().ListMcpTools().Return(expectedResult, nil)

	// Test ListMcpTools method call
	result, err := mockSession.ListMcpTools()

	// Verify call success
	assert.NoError(t, err)
	assert.NotNil(t, result)
	assert.Equal(t, "test-request-id", result.RequestID)
	assert.Len(t, result.Tools, 2)
	assert.Equal(t, "get_resource", result.Tools[0].Name)
	assert.Equal(t, "The command to retrieve  a wuying mcp runtime URL when user wants to get access to this runtime. Each retrieved URL will expire after a single use", result.Tools[0].Description)
	assert.Equal(t, "mcp-server", result.Tools[0].Server)
	assert.Equal(t, "get_resource", result.Tools[0].Tool)
	assert.Equal(t, "system_screenshot", result.Tools[1].Name)
	assert.Equal(t, "Captures a full-screen screenshot of the current display and returns a shareable URL. The screenshot is automatically processed and stored securely. The generated URL will expire after 64 minutes for security purposes.", result.Tools[1].Description)
	assert.Equal(t, "mcp-server", result.Tools[1].Server)
	assert.Equal(t, "system_screenshot", result.Tools[1].Tool)
}
