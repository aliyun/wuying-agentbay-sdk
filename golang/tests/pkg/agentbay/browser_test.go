package agentbay

import (
	"testing"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/browser"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func TestSession_BrowserIntegration(t *testing.T) {
	// Create a mock AgentBay instance
	apiKey := "test-api-key"

	ab, err := agentbay.NewAgentBay(apiKey)
	require.NoError(t, err)
	require.NotNil(t, ab)

	// Create a session
	session := agentbay.NewSession(ab, "test-session-123")
	require.NotNil(t, session)
	require.NotNil(t, session.Browser)

	t.Run("Browser is initialized on session creation", func(t *testing.T) {
		assert.NotNil(t, session.Browser)
		assert.False(t, session.Browser.IsInitialized())
	})

	t.Run("Browser has access to session methods", func(t *testing.T) {
		// These methods should be accessible through the session
		apiKey := session.GetAPIKey()
		sessionID := session.GetSessionID()

		assert.Equal(t, "test-api-key", apiKey)
		assert.Equal(t, "test-session-123", sessionID)
	})
}

func TestBrowserOption_BrowserType(t *testing.T) {
	tests := []struct {
		name          string
		browserType   string
		shouldBeValid bool
	}{
		{
			name:          "chromium",
			browserType:   "chromium",
			shouldBeValid: true,
		},
		{
			name:          "chrome",
			browserType:   "chrome",
			shouldBeValid: true,
		},
		{
			name:          "firefox (invalid)",
			browserType:   "firefox",
			shouldBeValid: false,
		},
		{
			name:          "edge (invalid)",
			browserType:   "edge",
			shouldBeValid: false,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			option := browser.NewBrowserOption()
			browserType := tt.browserType
			option.BrowserType = &browserType

			err := option.Validate()
			if tt.shouldBeValid {
				assert.NoError(t, err)
			} else {
				assert.Error(t, err)
				assert.Contains(t, err.Error(), "browserType must be 'chrome' or 'chromium'")
			}
		})
	}
}

// Removed tests for private toMap methods - these are internal implementation details
// The functionality is tested through integration tests
