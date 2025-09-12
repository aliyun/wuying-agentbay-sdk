package agentbay_test

import (
	"testing"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
	"github.com/stretchr/testify/assert"
)

func TestCreateSessionParams_WithEnableRecord(t *testing.T) {
	// Test default value
	params := agentbay.NewCreateSessionParams()
	assert.False(t, params.EnableRecord, "EnableRecord should default to false")

	// Test WithEnableRecord method
	params.WithEnableRecord(true)
	assert.True(t, params.EnableRecord, "EnableRecord should be set to true")

	// Test chaining
	result := params.WithEnableRecord(false).WithLabels(map[string]string{"test": "value"})
	assert.False(t, result.EnableRecord, "EnableRecord should be set to false")
	assert.Equal(t, "value", result.Labels["test"], "Labels should be set correctly")
}

func TestCreateSessionParams_EnableRecordFieldExists(t *testing.T) {
	params := &agentbay.CreateSessionParams{
		Labels:       map[string]string{"env": "test"},
		ImageId:      "test_image",
		IsVpc:        true,
		McpPolicyId:  "test_policy",
		EnableRecord: true,
	}

	assert.True(t, params.EnableRecord, "EnableRecord field should be accessible")
	assert.Equal(t, "test_image", params.ImageId, "ImageId should be set")
	assert.True(t, params.IsVpc, "IsVpc should be set")
	assert.Equal(t, "test_policy", params.McpPolicyId, "McpPolicyId should be set")
}

func TestSession_EnableRecordField(t *testing.T) {
	// Create a mock AgentBay (simplified)
	agentBay := &agentbay.AgentBay{
		APIKey: "test_key",
	}

	// Create a session
	session := agentbay.NewSession(agentBay, "test_session_id")

	// Test default value
	assert.False(t, session.EnableRecord, "EnableRecord should default to false")

	// Test setting EnableRecord
	session.EnableRecord = true
	assert.True(t, session.EnableRecord, "EnableRecord should be settable")
}

func TestCreateSessionParams_EnableRecordWithOtherFields(t *testing.T) {
	params := agentbay.NewCreateSessionParams()

	// Chain multiple method calls including WithEnableRecord
	result := params.
		WithLabels(map[string]string{"project": "test", "env": "development"}).
		WithImageId("browser_latest").
		WithIsVpc(false).
		WithMcpPolicyId("screen_recording_policy").
		WithEnableRecord(true)

	// Verify all fields are set correctly
	assert.Equal(t, map[string]string{"project": "test", "env": "development"}, result.Labels)
	assert.Equal(t, "browser_latest", result.ImageId)
	assert.False(t, result.IsVpc)
	assert.Equal(t, "screen_recording_policy", result.McpPolicyId)
	assert.True(t, result.EnableRecord)
}

func TestCreateSessionParams_EnableRecordBrowserScenario(t *testing.T) {
	// Test a realistic browser recording scenario
	params := agentbay.NewCreateSessionParams().
		WithImageId("browser_latest").
		WithLabels(map[string]string{
			"example":      "browser_replay",
			"session_type": "browser",
			"replay":       "enabled",
		}).
		WithEnableRecord(true)

	assert.True(t, params.EnableRecord, "EnableRecord should be true for browser replay")
	assert.Equal(t, "browser_latest", params.ImageId, "Should use browser image")
	assert.Equal(t, "enabled", params.Labels["replay"], "Replay label should be set")
}
