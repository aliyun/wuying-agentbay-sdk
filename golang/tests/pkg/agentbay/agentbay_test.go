package agentbay_test

import (
	"fmt"
	"os"
	"testing"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
	"github.com/aliyun/wuying-agentbay-sdk/golang/tests/pkg/agentbay/testutil"
)

func TestNewAgentBay(t *testing.T) {
	// Test with API key provided directly
	testAPIKey := testutil.GetTestAPIKey(t)
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
	apiKey := testutil.GetTestAPIKey(t)
	agentBay, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		t.Fatalf("Error initializing AgentBay client: %v", err)
	}

	// Create a session
	fmt.Println("Creating a new session...")
	result, err := agentBay.Create(nil)
	if err != nil {
		t.Fatalf("Error creating session: %v", err)
	}

	// Check if RequestID exists
	if result.RequestID == "" {
		t.Logf("Warning: Expected non-empty RequestID")
	} else {
		t.Logf("Request ID: %s", result.RequestID)
	}

	session := result.Session
	t.Logf("Session created with ID: %s", session.SessionID)

	// Ensure session ID is not empty
	if session.SessionID == "" {
		t.Errorf("Expected non-empty session ID")
	}

	// List all sessions
	fmt.Println("Listing sessions...")
	listResult, err := agentBay.ListByLabels(nil)
	if err != nil {
		t.Fatalf("Error listing sessions: %v", err)
	}

	sessionIds := listResult.SessionIds

	// Ensure at least one session (the one we just created)
	if len(sessionIds) < 1 {
		t.Errorf("Expected at least 1 session, got %d", len(sessionIds))
	}

	// Check if our created session is in the list
	found := false
	for _, sessionId := range sessionIds {
		if sessionId == session.SessionID {
			found = true
			break
		}
	}
	if !found {
		t.Errorf("Created session with ID %s not found in sessions list", session.SessionID)
	}

	// Delete the session
	fmt.Println("Deleting the session...")
	deleteResult, err := agentBay.Delete(session)
	if err != nil {
		t.Fatalf("Error deleting session: %v", err)
	}

	// Check delete result
	if !deleteResult.Success {
		t.Errorf("Delete operation reported as unsuccessful")
	}

	// List sessions again to ensure it's deleted
	listResult, err = agentBay.ListByLabels(nil)
	if err != nil {
		t.Fatalf("Error listing sessions after deletion: %v", err)
	}

	sessionIds = listResult.SessionIds

	// Check if the deleted session is not in the list
	for _, sessionId := range sessionIds {
		if sessionId == session.SessionID {
			t.Errorf("Session with ID %s still exists after deletion", session.SessionID)
		}
	}
}

// TestAgentBay_ListByLabels tests the functionality of listing sessions by labels
func TestAgentBay_ListByLabels(t *testing.T) {
	// Initialize AgentBay client
	apiKey := testutil.GetTestAPIKey(t)
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
	resultA, err := agentBayClient.Create(paramsA)
	if err != nil {
		t.Logf("Error creating session with labels A: %v", err)
		t.Skip("Skipping test as session creation failed")
		return
	}

	sessionA := resultA.Session
	t.Logf("Session A created with ID: %s", sessionA.SessionID)

	// Ensure cleanup of session A
	defer func() {
		t.Log("Cleaning up session A...")
		_, err := agentBayClient.Delete(sessionA)
		if err != nil {
			t.Logf("Warning: Error deleting session A: %v", err)
		}
	}()

	// Create session with labels B
	t.Log("Creating session with labels B...")
	paramsB := agentbay.NewCreateSessionParams().WithLabels(labelsB)
	resultB, err := agentBayClient.Create(paramsB)
	if err != nil {
		t.Logf("Error creating session with labels B: %v", err)
		t.Skip("Skipping test as session creation failed")
		return
	}

	sessionB := resultB.Session
	t.Logf("Session B created with ID: %s", sessionB.SessionID)

	// Ensure cleanup of session B
	defer func() {
		t.Log("Cleaning up session B...")
		_, err := agentBayClient.Delete(sessionB)
		if err != nil {
			t.Logf("Warning: Error deleting session B: %v", err)
		}
	}()

	// Test 1: List all sessions
	t.Log("Listing all sessions...")
	listResult, err := agentBayClient.ListByLabels(nil)
	if err != nil {
		t.Fatalf("Error listing all sessions: %v", err)
	}

	sessionIds := listResult.SessionIds
	t.Logf("Found %d sessions in total", len(sessionIds))

	// Test 2: List sessions by environment=development label
	t.Log("Listing sessions with environment=development...")
	devParams := agentbay.NewListSessionParams()
	devParams.Labels = map[string]string{"environment": "development"}
	devResult, err := agentBayClient.ListByLabels(devParams)
	if err != nil {
		t.Logf("Error listing sessions by environment=development: %v", err)
	} else {
		devSessionIds := devResult.SessionIds
		t.Logf("Found %d sessions with environment=development", len(devSessionIds))

		// Verify that session A is in the results
		foundSessionA := false
		for _, sessionId := range devSessionIds {
			if sessionId == sessionA.SessionID {
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
	teamBParams := agentbay.NewListSessionParams()
	teamBParams.Labels = map[string]string{"owner": "team-b"}
	teamBResult, err := agentBayClient.ListByLabels(teamBParams)
	if err != nil {
		t.Logf("Error listing sessions by owner=team-b: %v", err)
	} else {
		teamBSessionIds := teamBResult.SessionIds
		t.Logf("Found %d sessions with owner=team-b", len(teamBSessionIds))

		// Verify that session B is in the results
		foundSessionB := false
		for _, sessionId := range teamBSessionIds {
			if sessionId == sessionB.SessionID {
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
	multiParams := agentbay.NewListSessionParams()
	multiParams.Labels = map[string]string{
		"environment": "testing",
		"project":     "project-y",
	}
	multiResult, err := agentBayClient.ListByLabels(multiParams)
	if err != nil {
		t.Logf("Error listing sessions by multiple labels: %v", err)
	} else {
		multiLabelSessionIds := multiResult.SessionIds
		t.Logf("Found %d sessions with environment=testing AND project=project-y", len(multiLabelSessionIds))

		// Verify that session B is in the results and session A is not
		foundSessionA := false
		foundSessionB := false
		for _, sessionId := range multiLabelSessionIds {
			if sessionId == sessionA.SessionID {
				foundSessionA = true
			}
			if sessionId == sessionB.SessionID {
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
	nonExistentParams := agentbay.NewListSessionParams()
	nonExistentParams.Labels = map[string]string{"non-existent": "value"}
	nonExistentResult, err := agentBayClient.ListByLabels(nonExistentParams)
	if err != nil {
		t.Logf("Error listing sessions by non-existent label: %v", err)
	} else {
		nonExistentSessionIds := nonExistentResult.SessionIds
		t.Logf("Found %d sessions with non-existent label", len(nonExistentSessionIds))
		if len(nonExistentSessionIds) > 0 {
			t.Logf("Warning: Found sessions with non-existent label, this might indicate an issue")
		}
	}

	t.Log("Test completed successfully")
}
