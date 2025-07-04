package unit

import (
	"os"
	"testing"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

// TestAgentBayInitializationWithEnvVar tests initializing AgentBay with an API key from environment variable
func TestAgentBayInitializationWithEnvVar(t *testing.T) {
	// Save original env and restore after test
	originalAPIKey := os.Getenv("AGENTBAY_API_KEY")
	defer os.Setenv("AGENTBAY_API_KEY", originalAPIKey)

	// Set environment variable
	os.Setenv("AGENTBAY_API_KEY", "test-api-key")

	// Initialize AgentBay
	ab, err := agentbay.NewAgentBay("")

	// Verify results
	if err != nil {
		t.Fatalf("Expected no error, got %v", err)
	}
	if ab == nil {
		t.Fatal("Expected non-nil AgentBay instance")
	}
	if ab.APIKey != "test-api-key" {
		t.Errorf("Expected API key 'test-api-key', got '%s'", ab.APIKey)
	}
}

// TestAgentBayInitializationWithProvidedKey tests initializing AgentBay with a provided API key
func TestAgentBayInitializationWithProvidedKey(t *testing.T) {
	// Initialize AgentBay with provided key
	ab, err := agentbay.NewAgentBay("provided-api-key")

	// Verify results
	if err != nil {
		t.Fatalf("Expected no error, got %v", err)
	}
	if ab == nil {
		t.Fatal("Expected non-nil AgentBay instance")
	}
	if ab.APIKey != "provided-api-key" {
		t.Errorf("Expected API key 'provided-api-key', got '%s'", ab.APIKey)
	}
}

// TestAgentBayInitializationWithoutAPIKey tests initialization failure when no API key is available
func TestAgentBayInitializationWithoutAPIKey(t *testing.T) {
	// Save original env and restore after test
	originalAPIKey := os.Getenv("AGENTBAY_API_KEY")
	defer os.Setenv("AGENTBAY_API_KEY", originalAPIKey)

	// Clear environment variable
	os.Unsetenv("AGENTBAY_API_KEY")

	// Initialize AgentBay without providing key
	ab, err := agentbay.NewAgentBay("")

	// Verify results
	if err == nil {
		t.Fatal("Expected error, got nil")
	}
	if ab != nil {
		t.Fatal("Expected nil AgentBay instance")
	}
	if err.Error() != "API key is required. Provide it as a parameter or set the AGENTBAY_API_KEY environment variable" {
		t.Errorf("Unexpected error message: %s", err.Error())
	}
}

// TestCreate tests creating a session with parameters
func TestCreate(t *testing.T) {
	// Skip the actual API call in unit tests
	t.Skip("Skipping API call in unit test")

	// In a real test, you would:
	// 1. Initialize AgentBay
	// 2. Create test session parameters
	// 3. Create a session
	// 4. Verify the results
}

// TestList tests listing all sessions
func TestList(t *testing.T) {
	// Initialize AgentBay with API key
	ab, err := agentbay.NewAgentBay("test-api-key")
	if err != nil {
		t.Fatalf("Error initializing AgentBay: %v", err)
	}

	// List all sessions
	result, err := ab.List()
	if err != nil {
		t.Fatalf("Error listing sessions: %v", err)
	}
	if result == nil {
		t.Fatal("Expected non-nil result")
	}

	// Since this is a new instance with no sessions, the list should be empty
	if len(result.Sessions) != 0 {
		t.Errorf("Expected empty session list, got %d sessions", len(result.Sessions))
	}
}

// TestListByLabels tests listing sessions by labels
func TestListByLabels(t *testing.T) {
	// Skip the actual API call in unit tests
	t.Skip("Skipping API call in unit test")

	// In a real test, you would:
	// 1. Initialize AgentBay
	// 2. Create list parameters
	// 3. List sessions by labels
	// 4. Verify the results
}
