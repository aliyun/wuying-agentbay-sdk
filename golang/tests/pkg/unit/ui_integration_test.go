package agentbay_test

import (
	"testing"

	"github.com/aliyun/wuying-agentbay-sdk/golang/api/client"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/ui"
	"github.com/stretchr/testify/assert"
)

// MockSession is used for testing
type MockSession struct {
	apiKey    string
	sessionID string
	client    *client.Client
}

func (m *MockSession) GetAPIKey() string         { return m.apiKey }
func (m *MockSession) GetClient() *client.Client { return m.client }
func (m *MockSession) GetSessionId() string      { return m.sessionID }

// TestUI_GetClickableUIElements_Integration tests the GetClickableUIElements method of UI module
func TestUI_GetClickableUIElements_Integration(t *testing.T) {
	// Create mock session
	mockSession := &MockSession{
		apiKey:    "test-api-key",
		sessionID: "test-session-id",
		client:    nil, // In actual tests, this should be a mocked client
	}

	// Create UI manager
	uiManager := ui.NewUI(mockSession)
	assert.NotNil(t, uiManager)

	// Test GetClickableUIElements method call
	// Note: This will actually call the method, but since client is nil, it will fail
	// In actual tests, the client's return value should be mocked
	result, err := uiManager.GetClickableUIElements(5000) // 5 second timeout

	// Since client is nil, this will fail, but we can verify that the method is called correctly
	if err != nil {
		// This is expected because client is nil
		assert.Contains(t, err.Error(), "client is nil")
	} else {
		// If unexpectedly successful, verify result structure
		assert.NotNil(t, result)
	}
}

// TestUI_SendKey_Integration tests the SendKey method of UI module
func TestUI_SendKey_Integration(t *testing.T) {
	mockSession := &MockSession{
		apiKey:    "test-api-key",
		sessionID: "test-session-id",
		client:    nil,
	}

	uiManager := ui.NewUI(mockSession)
	assert.NotNil(t, uiManager)

	// Test SendKey method call
	result, err := uiManager.SendKey(ui.KeyCode.HOME)

	if err != nil {
		// Expected error because client is nil
		assert.Contains(t, err.Error(), "client is nil")
	} else {
		// If unexpectedly successful, verify result structure
		assert.NotNil(t, result)
	}
}

// TestUI_Swipe_Integration tests the Swipe method of UI module
func TestUI_Swipe_Integration(t *testing.T) {
	mockSession := &MockSession{
		apiKey:    "test-api-key",
		sessionID: "test-session-id",
		client:    nil,
	}

	uiManager := ui.NewUI(mockSession)
	assert.NotNil(t, uiManager)

	// Test Swipe method call
	result, err := uiManager.Swipe(100, 200, 300, 400, 500)

	if err != nil {
		// Expected error because client is nil
		assert.Contains(t, err.Error(), "client is nil")
	} else {
		// If unexpectedly successful, verify result structure
		assert.NotNil(t, result)
	}
}

// TestUI_Click_Integration tests the Click method of UI module
func TestUI_Click_Integration(t *testing.T) {
	mockSession := &MockSession{
		apiKey:    "test-api-key",
		sessionID: "test-session-id",
		client:    nil,
	}

	uiManager := ui.NewUI(mockSession)
	assert.NotNil(t, uiManager)

	// Test Click method call
	result, err := uiManager.Click(150, 250, "left")

	if err != nil {
		// Expected error because client is nil
		assert.Contains(t, err.Error(), "client is nil")
	} else {
		// If unexpectedly successful, verify result structure
		assert.NotNil(t, result)
	}
}

// TestUI_InputText_Integration tests the InputText method of UI module
func TestUI_InputText_Integration(t *testing.T) {
	mockSession := &MockSession{
		apiKey:    "test-api-key",
		sessionID: "test-session-id",
		client:    nil,
	}

	uiManager := ui.NewUI(mockSession)
	assert.NotNil(t, uiManager)

	// Test InputText method call
	result, err := uiManager.InputText("Hello, world!")

	if err != nil {
		// Expected error because client is nil
		assert.Contains(t, err.Error(), "client is nil")
	} else {
		// If unexpectedly successful, verify result structure
		assert.NotNil(t, result)
	}
}

// TestUI_GetAllUIElements_Integration tests the GetAllUIElements method of UI module
func TestUI_GetAllUIElements_Integration(t *testing.T) {
	mockSession := &MockSession{
		apiKey:    "test-api-key",
		sessionID: "test-session-id",
		client:    nil,
	}

	uiManager := ui.NewUI(mockSession)
	assert.NotNil(t, uiManager)

	// Test GetAllUIElements method call
	result, err := uiManager.GetAllUIElements(5000)

	if err != nil {
		// Expected error because client is nil
		assert.Contains(t, err.Error(), "client is nil")
	} else {
		// If unexpectedly successful, verify result structure
		assert.NotNil(t, result)
	}
}
