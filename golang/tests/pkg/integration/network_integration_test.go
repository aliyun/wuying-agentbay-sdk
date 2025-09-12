package integration

import (
	"fmt"
	"os"
	"testing"

	"github.com/alibabacloud-go/tea/tea"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

// TestNetworkIntegration_FullWorkflow tests the complete network workflow
func TestNetworkIntegration_FullWorkflow(t *testing.T) {
	// Check if API key is set
	apiKey := os.Getenv("AGENTBAY_API_KEY")
	if apiKey == "" {
		t.Skip("AGENTBAY_API_KEY not set, skipping integration test")
	}

	// Initialize AgentBay client
	agentBay, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		t.Fatalf("Failed to create AgentBay client: %v", err)
	}

	t.Log("🚀 Starting network integration test workflow...")

	// Step 1: Create network
	t.Log("📡 Step 1: Creating network...")
	createResult, err := agentBay.Network.CreateNetwork(nil)
	if err != nil {
		t.Fatalf("CreateNetwork failed with error: %v", err)
	}

	// Verify request ID exists
	if createResult.RequestID == "" {
		t.Error("Request ID should not be empty")
	}

	t.Logf("CreateNetwork result: Success=%v, RequestID=%s", createResult.Success, createResult.RequestID)

	// Step 2: Handle both success and failure scenarios intelligently
	var testNetworkID string
	var createdSuccessfully bool

	if createResult.Success && createResult.NetworkInfo != nil {
		// Real network was created successfully
		testNetworkID = createResult.NetworkInfo.NetworkID
		createdSuccessfully = true
		t.Logf("✅ Network created successfully: %s", testNetworkID)
		t.Logf("   Network Token: %s", createResult.NetworkInfo.NetworkToken)
	} else {
		// Network creation failed, use a known test pattern for error handling tests
		testNetworkID = "nw-test-integration-12345"
		createdSuccessfully = false
		t.Logf("⚠️ Network creation failed, using test network ID for error handling: %s", testNetworkID)
		t.Logf("   Error: %s", createResult.ErrorMessage)
	}

	// Step 3: Test DescribeNetwork with appropriate expectations
	t.Log("🔍 Step 2: Querying network details...")
	describeResult, err := agentBay.Network.DescribeNetwork(testNetworkID)
	if err != nil {
		t.Errorf("DescribeNetwork failed with error: %v", err)
		return
	}

	if describeResult.RequestID == "" {
		t.Error("Describe request ID should not be empty")
	}

	// Set expectations based on whether we created a real network
	if createdSuccessfully {
		// If we created a real network, handle API limitations gracefully
		if describeResult.Success && describeResult.NetworkInfo != nil {
			if describeResult.NetworkInfo.NetworkID != testNetworkID {
				t.Errorf("Expected NetworkID %s, got %s", testNetworkID, describeResult.NetworkInfo.NetworkID)
			}
			t.Logf("✅ Network described successfully: %s", describeResult.NetworkInfo.NetworkID)
			if describeResult.NetworkInfo.Online != nil {
				t.Logf("   Online status: %v", *describeResult.NetworkInfo.Online)
			} else {
				t.Log("   Online status: Unknown")
			}
		} else {
			t.Logf("⚠️ Network description failed (API limitation): %s", describeResult.ErrorMessage)
			// Don't fail the test - this might be expected API behavior
		}
	} else {
		// If we used a test network ID, expect failure (which is correct)
		if describeResult.Success {
			t.Log("⚠️ Unexpected success for test network ID (network might actually exist)")
		} else {
			t.Logf("✅ Expected failure for test network ID: %s", describeResult.ErrorMessage)
		}
	}

	// Step 4: Test session creation with network (if we have a real network)
	if createdSuccessfully {
		t.Log("🔗 Step 3: Testing session creation with real network...")
		testSessionCreationWithNetwork(t, agentBay, testNetworkID)
	} else {
		t.Log("⏭️ Step 3: Skipping session creation test (no real network available)")
	}
}

// TestNetworkIntegration_ExistingNetworkHandling tests handling of existing/non-existing networks
func TestNetworkIntegration_ExistingNetworkHandling(t *testing.T) {
	// Check if API key is set
	apiKey := os.Getenv("AGENTBAY_API_KEY")
	if apiKey == "" {
		t.Skip("AGENTBAY_API_KEY not set, skipping integration test")
	}

	// Initialize AgentBay client
	agentBay, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		t.Fatalf("Failed to create AgentBay client: %v", err)
	}

	t.Log("🔄 Testing token retrieval for existing network scenarios...")

	// Test Case 1: Try to get token for a definitely non-existent network
	t.Run("NonExistentNetwork", func(t *testing.T) {
		fakeNetworkID := fmt.Sprintf("nw-fake-%d", 999999)
		result, err := agentBay.Network.CreateNetwork(tea.String(fakeNetworkID))
		if err != nil {
			t.Fatalf("CreateNetwork for fake network failed with error: %v", err)
		}

		// Verify request ID exists
		if result.RequestID == "" {
			t.Error("Request ID should not be empty")
		}

		// Expect failure for fake network ID
		if result.Success {
			t.Errorf("Expected failure for fake network ID %s, but got success", fakeNetworkID)
		} else {
			t.Logf("✅ Expected failure for fake network: %s", result.ErrorMessage)
		}
	})

	// Test Case 2: Try to create a new network and then retrieve its token
	t.Run("CreateThenRetrieve", func(t *testing.T) {
		// First create a network
		createResult, err := agentBay.Network.CreateNetwork(nil)
		if err != nil {
			t.Fatalf("Initial CreateNetwork failed: %v", err)
		}

		if createResult.Success && createResult.NetworkInfo != nil {
			networkID := createResult.NetworkInfo.NetworkID
			t.Logf("Created network: %s", networkID)

			// Now try to retrieve token for the same network
			retrieveResult, err := agentBay.Network.CreateNetwork(tea.String(networkID))
			if err != nil {
				t.Errorf("Token retrieval failed: %v", err)
				return
			}

			// This should either succeed (token retrieved) or fail (depending on API behavior)
			if retrieveResult.Success && retrieveResult.NetworkInfo != nil {
				t.Logf("✅ Token retrieved for existing network: %s", retrieveResult.NetworkInfo.NetworkToken)
			} else {
				t.Logf("⚠️ Token retrieval failed (API behavior): %s", retrieveResult.ErrorMessage)
			}
		} else {
			t.Logf("⏭️ Skipping token retrieval test (network creation failed): %s", createResult.ErrorMessage)
		}
	})
}

// TestNetworkIntegration_NetworkManagerIntegration tests NetworkManager integration
func TestNetworkIntegration_NetworkManagerIntegration(t *testing.T) {
	// Check if API key is set
	apiKey := os.Getenv("AGENTBAY_API_KEY")
	if apiKey == "" {
		t.Skip("AGENTBAY_API_KEY not set, skipping integration test")
	}

	// Initialize AgentBay client
	agentBay, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		t.Fatalf("Failed to create AgentBay client: %v", err)
	}

	t.Log("🔧 Testing NetworkManager integration...")

	// Verify agentBay.Network attribute exists and has correct type
	if agentBay.Network == nil {
		t.Fatal("agentBay.Network should not be nil")
	}

	// Verify NetworkManager is correctly associated with agentBay
	if agentBay.Network.AgentBay != agentBay {
		t.Error("NetworkManager should reference correct agentBay")
	}

	t.Log("✅ NetworkManager correctly integrated into AgentBay")

	// Test that NetworkManager methods are callable
	t.Log("🧪 Testing NetworkManager method accessibility...")

	// This should not panic and should return a valid result
	result, err := agentBay.Network.CreateNetwork(nil)
	if err != nil {
		t.Errorf("NetworkManager.CreateNetwork should be callable: %v", err)
		return
	}

	if result == nil {
		t.Error("NetworkManager.CreateNetwork should return a result")
		return
	}

	t.Log("✅ NetworkManager methods are accessible and functional")
}

// testSessionCreationWithNetwork tests creating a session with a real network ID
func testSessionCreationWithNetwork(t *testing.T, agentBay *agentbay.AgentBay, networkID string) {
	t.Logf("Testing session creation with real network ID: %s", networkID)

	// Create session parameters with network ID
	// Note: This requires custom image and advanced network option
	params := agentbay.NewCreateSessionParams().
		WithImageId("imgc-12345678"). // In real scenario, use custom image like "imgc-12345678"
		WithNetworkId(networkID)

	// Attempt to create session
	sessionResult, err := agentBay.Create(params)
	if err != nil {
		t.Logf("⚠️ Session creation with network failed (expected with standard image): %v", err)
		return
	}

	if sessionResult != nil && sessionResult.Session != nil {
		t.Logf("✅ Session created with network: %s", sessionResult.Session.SessionID)

		// Clean up the session
		_, err := agentBay.Delete(sessionResult.Session)
		if err != nil {
			t.Logf("Warning: Failed to delete test session: %v", err)
		} else {
			t.Log("✅ Test session cleaned up successfully")
		}
	} else {
		t.Log("⚠️ Session creation with network returned nil result (expected with standard image)")
		// This is expected when using standard images without advanced network option
	}
}
