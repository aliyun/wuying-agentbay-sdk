package integration

import (
	"os"
	"strings"
	"testing"

	"github.com/alibabacloud-go/tea/dara"
	"github.com/aliyun/wuying-agentbay-sdk/golang/api/client"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
	"github.com/stretchr/testify/assert"
)

func TestGetCdpLink_WithBrowserSession(t *testing.T) {
	// Skip if no API key
	apiKey := os.Getenv("AGENTBAY_API_KEY")
	if apiKey == "" {
		t.Skip("AGENTBAY_API_KEY environment variable not set")
	}

	// Create AgentBay client
	agentBayClient, err := agentbay.NewAgentBay(apiKey, nil)
	assert.NoError(t, err)

	// Create browser session
	params := agentbay.NewCreateSessionParams().WithImageId("browser_latest")
	result, err := agentBayClient.Create(params)
	assert.NoError(t, err)
	assert.NotNil(t, result)
	assert.True(t, result.Success)
	assert.NotNil(t, result.Session)

	session := result.Session
	defer session.Delete()

	// Test GetCdpLink
	request := &client.GetCdpLinkRequest{
		Authorization: dara.String("Bearer " + apiKey),
		SessionId:     dara.String(session.GetSessionID()),
	}

	response, err := agentBayClient.Client.GetCdpLink(request)

	// Check if API is available
	if err != nil && strings.Contains(err.Error(), "InvalidAction.NotFound") {
		t.Skip("GetCdpLink API not yet available in production")
		return
	}

	assert.NoError(t, err)
	assert.NotNil(t, response)
	assert.NotNil(t, response.Body)
	assert.True(t, *response.Body.Success)
	assert.NotNil(t, response.Body.Data)
	assert.NotNil(t, response.Body.Data.Url)

	url := *response.Body.Data.Url
	assert.True(t, strings.HasPrefix(url, "ws://") || strings.HasPrefix(url, "wss://"),
		"CDP URL should start with ws:// or wss://")

	t.Logf("CDP URL: %s", url)
}

func TestGetCdpLink_WithInvalidSession(t *testing.T) {
	// Skip if no API key
	apiKey := os.Getenv("AGENTBAY_API_KEY")
	if apiKey == "" {
		t.Skip("AGENTBAY_API_KEY environment variable not set")
	}

	// Create AgentBay client
	agentBayClient, err := agentbay.NewAgentBay(apiKey, nil)
	assert.NoError(t, err)

	// Test GetCdpLink with invalid session
	request := &client.GetCdpLinkRequest{
		Authorization: dara.String("Bearer " + apiKey),
		SessionId:     dara.String("invalid-session-id-12345"),
	}

	_, err = agentBayClient.Client.GetCdpLink(request)

	// Should get an error for invalid session
	assert.Error(t, err)
	assert.True(t,
		strings.Contains(err.Error(), "InvalidMcpSession.NotFound") ||
			strings.Contains(err.Error(), "InvalidAction.NotFound"),
		"Expected InvalidMcpSession.NotFound or InvalidAction.NotFound error")
}
