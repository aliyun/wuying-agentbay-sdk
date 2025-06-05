package agentbay_test

import (
	"fmt"
	"os"
	"strings"
	"testing"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

// Helper function to check if a string contains "tool not found"
func containsToolNotFound(s string) bool {
	return strings.Contains(strings.ToLower(s), "tool not found")
}

// Get API key for testing
func getTestAPIKey(t *testing.T) string {
	apiKey := os.Getenv("AGENTBAY_API_KEY")
	if apiKey == "" {
		apiKey = "akm-xxx" // Replace with your test API key
		t.Logf("Warning: Using default API key. Set AGENTBAY_API_KEY environment variable for testing.")
	}
	return apiKey
}

func TestNewAgentBay(t *testing.T) {
	// Test with API key provided directly
	testAPIKey := getTestAPIKey(t)
	client, err := agentbay.NewAgentBay(testAPIKey)
	if err != nil {
		t.Fatalf("Expected no error, got %v", err)
	}
	if client.APIKey != testAPIKey {
		t.Errorf("Expected API key to be '%s', got '%s'", testAPIKey, client.APIKey)
	}

	// Test with API key from environment variable
	os.Setenv("AGENTBAY_API_KEY", "env_api_key")
	defer os.Unsetenv("AGENTBAY_API_KEY")

	client, err = agentbay.NewAgentBay("")
	if err != nil {
		t.Fatalf("Expected no error, got %v", err)
	}
	if client.APIKey != "env_api_key" {
		t.Errorf("Expected API key to be 'env_api_key', got '%s'", client.APIKey)
	}

	// Test with no API key
	os.Unsetenv("AGENTBAY_API_KEY")
	_, err = agentbay.NewAgentBay("")
	if err == nil {
		t.Fatal("Expected error for missing API key, got nil")
	}
}

func TestAgentBay_Create_List_Delete(t *testing.T) {
	// Initialize AgentBay client
	apiKey := getTestAPIKey(t)
	agentBay, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		t.Fatalf("Error initializing AgentBay client: %v", err)
	}

	// Create a session
	fmt.Println("Creating a new session...")
	session, err := agentBay.Create(nil)
	if err != nil {
		t.Fatalf("Error creating session: %v", err)
	}
	t.Logf("Session created with ID: %s", session.SessionID)

	// Ensure session ID is not empty
	if session.SessionID == "" {
		t.Errorf("Expected non-empty session ID")
	}

	// List all sessions
	fmt.Println("Listing sessions...")
	sessions, err := agentBay.List()
	if err != nil {
		t.Fatalf("Error listing sessions: %v", err)
	}

	// Ensure at least one session (the one we just created)
	if len(sessions) < 1 {
		t.Errorf("Expected at least 1 session, got %d", len(sessions))
	}

	// Check if our created session is in the list
	found := false
	for _, s := range sessions {
		if s.SessionID == session.SessionID {
			found = true
			break
		}
	}
	if !found {
		t.Errorf("Created session with ID %s not found in sessions list", session.SessionID)
	}

	// Delete the session
	fmt.Println("Deleting the session...")
	err = agentBay.Delete(session)
	if err != nil {
		t.Fatalf("Error deleting session: %v", err)
	}

	// List sessions again to ensure it's deleted
	sessions, err = agentBay.List()
	if err != nil {
		t.Fatalf("Error listing sessions after deletion: %v", err)
	}

	// Check if the deleted session is not in the list
	for _, s := range sessions {
		if s.SessionID == session.SessionID {
			t.Errorf("Session with ID %s still exists after deletion", session.SessionID)
		}
	}
}

// TestAgentBay_ListByLabels tests the functionality of listing sessions by labels
func TestAgentBay_ListByLabels(t *testing.T) {
	// Initialize AgentBay client
	apiKey := getTestAPIKey(t)
	agentBayClient, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		t.Fatalf("Error initializing AgentBay client: %v", err)
	}

	// Define two sets of labels for different sessions
	labelsA := map[string]string{
		"environment": "development",
		"owner":       "team-a",
		"project":     "project-x",
	}

	labelsB := map[string]string{
		"environment": "testing",
		"owner":       "team-b",
		"project":     "project-y",
	}

	// Create session with labels A
	t.Log("Creating session with labels A...")
	paramsA := agentbay.NewCreateSessionParams().WithLabels(labelsA)
	sessionA, err := agentBayClient.Create(paramsA)
	if err != nil {
		t.Logf("Error creating session with labels A: %v", err)
		t.Skip("Skipping test as session creation failed")
		return
	}
	t.Logf("Session A created with ID: %s", sessionA.SessionID)

	// Ensure cleanup of session A
	defer func() {
		t.Log("Cleaning up session A...")
		err := agentBayClient.Delete(sessionA)
		if err != nil {
			t.Logf("Warning: Error deleting session A: %v", err)
		}
	}()

	// Create session with labels B
	t.Log("Creating session with labels B...")
	paramsB := agentbay.NewCreateSessionParams().WithLabels(labelsB)
	sessionB, err := agentBayClient.Create(paramsB)
	if err != nil {
		t.Logf("Error creating session with labels B: %v", err)
		t.Skip("Skipping test as session creation failed")
		return
	}
	t.Logf("Session B created with ID: %s", sessionB.SessionID)

	// Ensure cleanup of session B
	defer func() {
		t.Log("Cleaning up session B...")
		err := agentBayClient.Delete(sessionB)
		if err != nil {
			t.Logf("Warning: Error deleting session B: %v", err)
		}
	}()

	// Test 1: List all sessions
	t.Log("Listing all sessions...")
	allSessions, err := agentBayClient.List()
	if err != nil {
		t.Fatalf("Error listing all sessions: %v", err)
	}
	t.Logf("Found %d sessions in total", len(allSessions))

	// Test 2: List sessions by environment=development label
	t.Log("Listing sessions with environment=development...")
	devSessions, err := agentBayClient.ListByLabels(map[string]string{"environment": "development"})
	if err != nil {
		t.Logf("Error listing sessions by environment=development: %v", err)
	} else {
		t.Logf("Found %d sessions with environment=development", len(devSessions))

		// Verify that session A is in the results
		foundSessionA := false
		for _, s := range devSessions {
			if s.SessionID == sessionA.SessionID {
				foundSessionA = true
				break
			}
		}

		if !foundSessionA {
			t.Errorf("Expected to find session A in development environment results")
		}
	}

	// Test 3: List sessions by owner=team-b label
	t.Log("Listing sessions with owner=team-b...")
	teamBSessions, err := agentBayClient.ListByLabels(map[string]string{"owner": "team-b"})
	if err != nil {
		t.Logf("Error listing sessions by owner=team-b: %v", err)
	} else {
		t.Logf("Found %d sessions with owner=team-b", len(teamBSessions))

		// Verify that session B is in the results
		foundSessionB := false
		for _, s := range teamBSessions {
			if s.SessionID == sessionB.SessionID {
				foundSessionB = true
				break
			}
		}

		if !foundSessionB {
			t.Errorf("Expected to find session B in team-b owner results")
		}
	}

	// Test 4: List sessions with multiple labels (environment=testing AND project=project-y)
	t.Log("Listing sessions with environment=testing AND project=project-y...")
	multiLabelSessions, err := agentBayClient.ListByLabels(map[string]string{
		"environment": "testing",
		"project":     "project-y",
	})
	if err != nil {
		t.Logf("Error listing sessions by multiple labels: %v", err)
	} else {
		t.Logf("Found %d sessions with environment=testing AND project=project-y", len(multiLabelSessions))

		// Verify that session B is in the results and session A is not
		foundSessionA := false
		foundSessionB := false
		for _, s := range multiLabelSessions {
			if s.SessionID == sessionA.SessionID {
				foundSessionA = true
			}
			if s.SessionID == sessionB.SessionID {
				foundSessionB = true
			}
		}

		if foundSessionA {
			t.Errorf("Did not expect to find session A in multi-label results")
		}
		if !foundSessionB {
			t.Errorf("Expected to find session B in multi-label results")
		}
	}

	// Test 5: List sessions with non-existent label
	t.Log("Listing sessions with non-existent label...")
	nonExistentSessions, err := agentBayClient.ListByLabels(map[string]string{"non-existent": "value"})
	if err != nil {
		t.Logf("Error listing sessions by non-existent label: %v", err)
	} else {
		t.Logf("Found %d sessions with non-existent label", len(nonExistentSessions))
		if len(nonExistentSessions) > 0 {
			t.Logf("Warning: Found sessions with non-existent label, this might indicate an issue")
		}
	}

	t.Log("Test completed successfully")
}
