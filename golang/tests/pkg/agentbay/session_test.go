package agentbay_test

import (
	"fmt"
	"testing"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

func TestSession_Properties(t *testing.T) {
	// Initialize AgentBay client
	apiKey := getTestAPIKey(t)
	agentBay, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		t.Fatalf("Error initializing AgentBay client: %v", err)
	}

	// Create a session
	fmt.Println("Creating a new session for session testing...")
	session, err := agentBay.Create(nil)
	if err != nil {
		t.Fatalf("Error creating session: %v", err)
	}
	t.Logf("Session created with ID: %s", session.SessionID)
	defer func() {
		// Clean up the session after test
		fmt.Println("Cleaning up: Deleting the session...")
		err := agentBay.Delete(session)
		if err != nil {
			t.Logf("Warning: Error deleting session: %v", err)
		}
	}()

	// Test session properties
	if session.SessionID == "" {
		t.Errorf("Expected non-empty session ID")
	}
	if session.AgentBay != agentBay {
		t.Errorf("Expected AgentBay to be the same instance")
	}

	// Test GetSessionId method
	sessionID := session.GetSessionId()
	if sessionID != session.SessionID {
		t.Errorf("Expected GetSessionId to return '%s', got '%s'", session.SessionID, sessionID)
	}

	// Test GetAPIKey method
	apiKeyFromSession := session.GetAPIKey()
	if apiKeyFromSession != apiKey {
		t.Errorf("Expected GetAPIKey to return '%s', got '%s'", apiKey, apiKeyFromSession)
	}

	// Test GetClient method
	client := session.GetClient()
	if client == nil {
		t.Errorf("Expected GetClient to return a non-nil client")
	}
}

func TestSession_DeleteMethod(t *testing.T) {
	// Initialize AgentBay client
	apiKey := getTestAPIKey(t)
	agentBay, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		t.Fatalf("Error initializing AgentBay client: %v", err)
	}

	// Create a session
	fmt.Println("Creating a new session for delete testing...")
	session, err := agentBay.Create(nil)
	if err != nil {
		t.Fatalf("Error creating session: %v", err)
	}
	t.Logf("Session created with ID: %s", session.SessionID)

	// Test Delete method
	fmt.Println("Testing session.Delete method...")
	err = session.Delete()
	if err != nil {
		t.Fatalf("Error deleting session: %v", err)
	}

	// Verify the session was deleted by trying to list sessions
	sessions, err := agentBay.List()
	if err != nil {
		t.Fatalf("Error listing sessions: %v", err)
	}

	// Check if the deleted session is not in the list
	for _, s := range sessions {
		if s.SessionID == session.SessionID {
			t.Errorf("Session with ID %s still exists after deletion", session.SessionID)
		}
	}
}
