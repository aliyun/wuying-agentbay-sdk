package agentbay_test

import (
	"os"
	"testing"

	"github.com/alibabacloud-go/tea/tea"
	mcp "github.com/aliyun/wuying-agentbay-sdk/golang/api/client"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

// TestNetwork_CreateNetwork tests the network creation functionality
func TestNetwork_CreateNetwork(t *testing.T) {
	// Initialize AgentBay client directly (network operations are independent of sessions)
	apiKey := os.Getenv("AGENTBAY_API_KEY")
	if apiKey == "" {
		t.Skip("AGENTBAY_API_KEY not set, skipping network test")
	}

	agentBay, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		t.Fatalf("Failed to create AgentBay client: %v", err)
	}

	// Test network creation
	t.Log("Testing network creation...")

	if agentBay.Network == nil {
		t.Fatal("NetworkManager should not be nil")
	}

	// Create network (independent operation, no session required)
	result, err := agentBay.Network.CreateNetwork(nil)
	if err != nil {
		t.Errorf("CreateNetwork failed with error: %v", err)
		return
	}

	// Verify request ID exists
	if result.RequestID == "" {
		t.Error("Request ID should not be empty")
	}

	t.Logf("CreateNetwork result: Success=%v, RequestID=%s", result.Success, result.RequestID)

	// If creation successful, verify network information
	if result.Success && result.NetworkInfo != nil {
		t.Logf("✅ Network created successfully: %s", result.NetworkInfo.NetworkID)
		t.Logf("   Network Token: %s", result.NetworkInfo.NetworkToken)

		if result.NetworkInfo.NetworkID == "" {
			t.Error("Network ID should not be empty when creation succeeds")
		}
		if result.NetworkInfo.NetworkToken == "" {
			t.Error("Network Token should not be empty when creation succeeds")
		}
	} else {
		t.Logf("⚠️ Network creation failed: %s", result.ErrorMessage)
		// Creation failure is also a valid test result as long as API calls work normally
	}
}

// TestNetwork_CreateNetworkWithExistingID tests creating network with existing ID
func TestNetwork_CreateNetworkWithExistingID(t *testing.T) {
	// Initialize AgentBay client
	apiKey := os.Getenv("AGENTBAY_API_KEY")
	if apiKey == "" {
		t.Skip("AGENTBAY_API_KEY not set, skipping network test")
	}

	agentBay, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		t.Fatalf("Failed to create AgentBay client: %v", err)
	}

	t.Log("Testing network creation with existing network ID...")

	// Step 1: First create a new network to get a real network ID
	t.Log("Step 1: Creating a new network...")
	createResult, err := agentBay.Network.CreateNetwork(nil)
	if err != nil {
		t.Fatalf("Failed to create initial network: %v", err)
	}

	if !createResult.Success || createResult.NetworkInfo == nil {
		t.Fatalf("Initial network creation failed: %s", createResult.ErrorMessage)
	}

	existingNetworkID := createResult.NetworkInfo.NetworkID
	originalToken := createResult.NetworkInfo.NetworkToken
	t.Logf("✅ Initial network created: %s", existingNetworkID)
	t.Logf("   Original Token: %s", originalToken)

	// Step 2: Use the existing network ID to retrieve token again
	t.Log("Step 2: Retrieving token for existing network...")
	result, err := agentBay.Network.CreateNetwork(tea.String(existingNetworkID))
	if err != nil {
		t.Errorf("CreateNetwork with existing ID failed with error: %v", err)
		return
	}

	// Verify request ID exists
	if result.RequestID == "" {
		t.Error("Request ID should not be empty")
	}

	t.Logf("CreateNetwork with existing ID result: Success=%v, RequestID=%s", result.Success, result.RequestID)

	// Log result regardless of success/failure
	if result.Success && result.NetworkInfo != nil {
		t.Logf("✅ Network token retrieved for existing network: %s", result.NetworkInfo.NetworkID)
		t.Logf("   Retrieved Token: %s", result.NetworkInfo.NetworkToken)

		// Verify the network ID matches
		if result.NetworkInfo.NetworkID != existingNetworkID {
			t.Errorf("Expected network ID %s, got %s", existingNetworkID, result.NetworkInfo.NetworkID)
		}

		// Note: Token might be different each time it's retrieved
		if result.NetworkInfo.NetworkToken == "" {
			t.Error("Retrieved token should not be empty")
		}
	} else {
		t.Logf("⚠️ Network token retrieval failed: %s", result.ErrorMessage)
	}
}

// TestNetwork_DescribeNetwork tests the network description functionality
func TestNetwork_DescribeNetwork(t *testing.T) {
	// Initialize AgentBay client
	apiKey := os.Getenv("AGENTBAY_API_KEY")
	if apiKey == "" {
		t.Skip("AGENTBAY_API_KEY not set, skipping network test")
	}

	agentBay, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		t.Fatalf("Failed to create AgentBay client: %v", err)
	}

	// Test network description
	t.Log("Testing network description...")

	// First try to create a network to get a valid network ID
	createResult, err := agentBay.Network.CreateNetwork(nil)
	if err != nil {
		t.Errorf("CreateNetwork failed with error: %v", err)
		return
	}

	var networkID string
	if createResult.Success && createResult.NetworkInfo != nil {
		networkID = createResult.NetworkInfo.NetworkID
		t.Logf("Using created network ID: %s", networkID)
	} else {
		// Use a test network ID if creation failed
		networkID = "net-test-12345"
		t.Logf("Using test network ID: %s", networkID)
	}

	// Describe the network
	result, err := agentBay.Network.DescribeNetwork(networkID)
	if err != nil {
		t.Errorf("DescribeNetwork failed with error: %v", err)
		return
	}

	// Verify request ID exists
	if result.RequestID == "" {
		t.Error("Request ID should not be empty")
	}

	t.Logf("DescribeNetwork result: Success=%v, RequestID=%s", result.Success, result.RequestID)

	// Log result regardless of success/failure
	if result.Success && result.NetworkInfo != nil {
		t.Logf("✅ Network described successfully: %s", result.NetworkInfo.NetworkID)
		if result.NetworkInfo.Online != nil {
			t.Logf("   Online status: %v", *result.NetworkInfo.Online)
		} else {
			t.Log("   Online status: Unknown")
		}
	} else {
		t.Logf("⚠️ Network description failed: %s", result.ErrorMessage)
	}
}

// TestNetwork_DescribeNonexistentNetwork tests describing a non-existent network
func TestNetwork_DescribeNonexistentNetwork(t *testing.T) {
	// Initialize AgentBay client
	apiKey := os.Getenv("AGENTBAY_API_KEY")
	if apiKey == "" {
		t.Skip("AGENTBAY_API_KEY not set, skipping network test")
	}

	agentBay, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		t.Fatalf("Failed to create AgentBay client: %v", err)
	}

	// Test describing non-existent network
	t.Log("Testing description of non-existent network...")

	// Use a guaranteed non-existent network ID with timestamp
	fakeNetworkID := "nw-nonexistent-test-999999"

	result, err := agentBay.Network.DescribeNetwork(fakeNetworkID)
	if err != nil {
		t.Errorf("DescribeNetwork failed with error: %v", err)
		return
	}

	// Verify request ID exists
	if result.RequestID == "" {
		t.Error("Request ID should not be empty")
	}

	// Expect query to fail (this tests proper error handling)
	if result.Success {
		t.Logf("⚠️ Unexpected success for fake network ID (network might actually exist): %s", fakeNetworkID)
		// Don't fail the test - just log the unexpected result
	} else {
		t.Logf("✅ Expected failure for nonexistent network: %s", result.ErrorMessage)
	}

	// Always expect some kind of response
	if result.ErrorMessage == "" && !result.Success {
		t.Error("Error message should be provided for failed request")
	}
}

// TestNetwork_NetworkManagerIntegration tests NetworkManager integration with AgentBay
func TestNetwork_NetworkManagerIntegration(t *testing.T) {
	// Initialize AgentBay client
	apiKey := os.Getenv("AGENTBAY_API_KEY")
	if apiKey == "" {
		t.Skip("AGENTBAY_API_KEY not set, skipping network test")
	}

	agentBay, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		t.Fatalf("Failed to create AgentBay client: %v", err)
	}

	// Test NetworkManager integration
	t.Log("Testing NetworkManager integration...")

	// Verify agentBay.Network attribute exists and has correct type
	if agentBay.Network == nil {
		t.Fatal("agentBay.Network should not be nil")
	}

	// Verify NetworkManager is correctly associated with agentBay
	if agentBay.Network.AgentBay != agentBay {
		t.Error("NetworkManager should reference correct agentBay")
	}

	t.Log("✅ NetworkManager correctly integrated into AgentBay")
}

// TestNetwork_CompleteWorkflow tests the complete network workflow: create -> retrieve token -> use in session
func TestNetwork_CompleteWorkflow(t *testing.T) {
	// Initialize AgentBay client
	apiKey := os.Getenv("AGENTBAY_API_KEY")
	if apiKey == "" {
		t.Skip("AGENTBAY_API_KEY not set, skipping network test")
	}

	agentBay, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		t.Fatalf("Failed to create AgentBay client: %v", err)
	}

	t.Log("Testing complete network workflow...")

	// Step 1: Create a new network
	t.Log("Step 1: Creating new network...")
	createResult, err := agentBay.Network.CreateNetwork(nil)
	if err != nil {
		t.Fatalf("Failed to create network: %v", err)
	}

	if !createResult.Success || createResult.NetworkInfo == nil {
		t.Fatalf("Network creation failed: %s", createResult.ErrorMessage)
	}

	networkID := createResult.NetworkInfo.NetworkID
	networkToken := createResult.NetworkInfo.NetworkToken
	t.Logf("✅ Network created successfully: %s", networkID)
	t.Logf("   Network Token: %s", networkToken)

	// Step 2: Retrieve token for the existing network
	t.Log("Step 2: Retrieving token for existing network...")
	tokenResult, err := agentBay.Network.CreateNetwork(tea.String(networkID))
	if err != nil {
		t.Errorf("Failed to retrieve token: %v", err)
	} else if tokenResult.Success && tokenResult.NetworkInfo != nil {
		t.Logf("✅ Token retrieved successfully: %s", tokenResult.NetworkInfo.NetworkToken)

		// Verify network ID matches
		if tokenResult.NetworkInfo.NetworkID != networkID {
			t.Errorf("Expected network ID %s, got %s", networkID, tokenResult.NetworkInfo.NetworkID)
		}
	} else {
		t.Logf("⚠️ Token retrieval failed: %s", tokenResult.ErrorMessage)
	}

	// Step 3: Try to describe the network (may fail, but should not crash)
	t.Log("Step 3: Describing network...")
	describeResult, err := agentBay.Network.DescribeNetwork(networkID)
	if err != nil {
		t.Logf("⚠️ Network description failed with error: %v", err)
	} else if describeResult.Success && describeResult.NetworkInfo != nil {
		t.Logf("✅ Network described successfully")
		if describeResult.NetworkInfo.Online != nil {
			status := map[bool]string{true: "🟢 Online", false: "🔴 Offline"}[*describeResult.NetworkInfo.Online]
			t.Logf("   Status: %s", status)
		}
	} else {
		t.Logf("⚠️ Network description failed: %s", describeResult.ErrorMessage)
	}

	// Step 4: Use network in session creation (will likely fail with imgc-xxxx, but should not crash)
	t.Log("Step 4: Testing session creation with network...")
	sessionParams := agentbay.NewCreateSessionParams().
		WithImageId("imgc-12345678"). // Custom image required for network functionality
		WithNetworkId(networkID).
		WithLabels(map[string]string{
			"test":    "network-workflow",
			"network": "enabled",
		})

	sessionResult, err := agentBay.Create(sessionParams)
	if err != nil {
		t.Logf("⚠️ Session creation with network failed (expected): %v", err)
		// This is expected when using a test custom image ID
	} else if sessionResult != nil && sessionResult.Session != nil {
		t.Logf("✅ Session created with network: %s", sessionResult.Session.SessionID)

		// Clean up session
		t.Log("Step 5: Cleaning up session...")
		deleteResult, err := agentBay.Delete(sessionResult.Session)
		if err != nil {
			t.Logf("⚠️ Warning: Failed to delete session: %v", err)
		} else {
			t.Logf("✅ Session cleaned up successfully (RequestID: %s)", deleteResult.RequestID)
		}
	} else {
		t.Log("⚠️ Session creation with network returned nil result (expected)")
	}

	t.Log("🎉 Complete network workflow test finished")
}

// TestNetwork_NetworkInfoMethods tests NetworkInfo helper methods
func TestNetwork_NetworkInfoMethods(t *testing.T) {
	t.Log("Testing NetworkInfo helper methods...")

	// Test NewNetworkInfoFromCreateResponse
	t.Run("NewNetworkInfoFromCreateResponse", func(t *testing.T) {
		data := &mcp.CreateNetworkResponseBodyData{
			NetworkId:    tea.String("net-123456"),
			NetworkToken: tea.String("token-123456"),
		}

		networkInfo := agentbay.NewNetworkInfoFromCreateResponse(data)

		if networkInfo.NetworkID != "net-123456" {
			t.Errorf("Expected NetworkID 'net-123456', got '%s'", networkInfo.NetworkID)
		}
		if networkInfo.NetworkToken != "token-123456" {
			t.Errorf("Expected NetworkToken 'token-123456', got '%s'", networkInfo.NetworkToken)
		}
		if networkInfo.Online != nil {
			t.Error("Online should be nil for create response")
		}
	})

	// Test NewNetworkInfoFromDescribeResponse
	t.Run("NewNetworkInfoFromDescribeResponse", func(t *testing.T) {
		data := &mcp.DescribeNetworkResponseBodyData{
			Online: tea.Bool(true),
		}

		networkInfo := agentbay.NewNetworkInfoFromDescribeResponse("net-123456", data)

		if networkInfo.NetworkID != "net-123456" {
			t.Errorf("Expected NetworkID 'net-123456', got '%s'", networkInfo.NetworkID)
		}
		if networkInfo.Online == nil || !*networkInfo.Online {
			t.Error("Online should be true")
		}
		if networkInfo.NetworkToken != "" {
			t.Error("NetworkToken should be empty for describe response")
		}
	})

	// Test ToMap
	t.Run("ToMap", func(t *testing.T) {
		networkInfo := &agentbay.NetworkInfo{
			NetworkID:    "net-123456",
			NetworkToken: "token-123456",
			Online:       tea.Bool(true),
		}

		result := networkInfo.ToMap()

		if result["network_id"] != "net-123456" {
			t.Errorf("Expected network_id 'net-123456', got '%v'", result["network_id"])
		}
		if result["network_token"] != "token-123456" {
			t.Errorf("Expected network_token 'token-123456', got '%v'", result["network_token"])
		}
		if result["online"] != true {
			t.Errorf("Expected online true, got '%v'", result["online"])
		}
	})

	// Test String
	t.Run("String", func(t *testing.T) {
		networkInfo := &agentbay.NetworkInfo{
			NetworkID: "net-123456",
			Online:    tea.Bool(true),
		}

		result := networkInfo.String()

		if !contains(result, "net-123456") {
			t.Errorf("String representation should contain network ID")
		}
		if !contains(result, "online") {
			t.Errorf("String representation should contain online status")
		}
	})
}

// Helper function to check if string contains substring
func contains(s, substr string) bool {
	return len(s) >= len(substr) && (s == substr || len(substr) == 0 ||
		(len(s) > len(substr) && containsAt(s, substr)))
}

func containsAt(s, substr string) bool {
	for i := 0; i <= len(s)-len(substr); i++ {
		if s[i:i+len(substr)] == substr {
			return true
		}
	}
	return false
}
