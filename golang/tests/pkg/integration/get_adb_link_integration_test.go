package integration

import (
	"encoding/json"
	"os"
	"strings"
	"testing"

	"github.com/alibabacloud-go/tea/dara"
	"github.com/aliyun/wuying-agentbay-sdk/golang/api/client"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
	"github.com/stretchr/testify/assert"
)

func TestGetAdbLink_WithMobileSession(t *testing.T) {
	// Skip if no API key
	apiKey := os.Getenv("AGENTBAY_API_KEY")
	if apiKey == "" {
		t.Skip("AGENTBAY_API_KEY environment variable not set")
	}

	// Create AgentBay client
	agentBayClient, err := agentbay.NewAgentBay(apiKey, nil)
	assert.NoError(t, err)

	// Create mobile session
	params := agentbay.NewCreateSessionParams().WithImageId("mobile_latest")
	result, err := agentBayClient.Create(params)
	assert.NoError(t, err)
	assert.NotNil(t, result)
	assert.True(t, result.Success)
	assert.NotNil(t, result.Session)

	session := result.Session
	defer session.Delete()

	// Build options with adbkey_pub
	optionsMap := map[string]string{"adbkey_pub": "test-adb-public-key"}
	optionsJSON, err := json.Marshal(optionsMap)
	assert.NoError(t, err)

	// Test GetAdbLink
	request := &client.GetAdbLinkRequest{
		Authorization: dara.String("Bearer " + apiKey),
		SessionId:     dara.String(session.GetSessionID()),
		Option:        dara.String(string(optionsJSON)),
	}

	response, err := agentBayClient.Client.GetAdbLink(request)

	// Check if API is available
	if err != nil && strings.Contains(err.Error(), "InvalidAction.NotFound") {
		t.Skip("GetAdbLink API not yet available in production")
		return
	}

	assert.NoError(t, err)
	assert.NotNil(t, response)
	assert.NotNil(t, response.Body)
	assert.True(t, *response.Body.Success)
	assert.NotNil(t, response.Body.Data)
	assert.NotNil(t, response.Body.Data.Url)

	url := *response.Body.Data.Url
	assert.True(t, strings.Contains(strings.ToLower(url), "adb") || strings.Contains(url, ":"),
		"ADB URL should contain 'adb' or ':'")

	t.Logf("ADB URL: %s", url)
}

func TestGetAdbLink_WithInvalidSession(t *testing.T) {
	// Skip if no API key
	apiKey := os.Getenv("AGENTBAY_API_KEY")
	if apiKey == "" {
		t.Skip("AGENTBAY_API_KEY environment variable not set")
	}

	// Create AgentBay client
	agentBayClient, err := agentbay.NewAgentBay(apiKey, nil)
	assert.NoError(t, err)

	// Build options with adbkey_pub
	optionsMap := map[string]string{"adbkey_pub": "test-key"}
	optionsJSON, err := json.Marshal(optionsMap)
	assert.NoError(t, err)

	// Test GetAdbLink with invalid session
	request := &client.GetAdbLinkRequest{
		Authorization: dara.String("Bearer " + apiKey),
		SessionId:     dara.String("invalid-session-id-12345"),
		Option:        dara.String(string(optionsJSON)),
	}

	_, err = agentBayClient.Client.GetAdbLink(request)

	// Should get an error for invalid session
	assert.Error(t, err)
	assert.True(t,
		strings.Contains(err.Error(), "InvalidMcpSession.NotFound") ||
			strings.Contains(err.Error(), "InvalidAction.NotFound"),
		"Expected InvalidMcpSession.NotFound or InvalidAction.NotFound error")
}
