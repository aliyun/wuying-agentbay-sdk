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
	t.Logf("Session ResourceUrl: %s", session.ResourceUrl)

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

func TestSession_GetLinkMethod(t *testing.T) {
	// Initialize AgentBay client
	apiKey := getTestAPIKey(t)
	agentBay, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		t.Fatalf("Error initializing AgentBay client: %v", err)
	}

	// Create a session
	fmt.Println("Creating a new session for GetLink testing...")
	sessionParams := agentbay.NewCreateSessionParams().WithImageId("imgc-07if81c4ktj9shiru")
	session, err := agentBay.Create(sessionParams)
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

	// Test GetLink method
	fmt.Println("Testing session.GetLink method...")
	link, err := session.GetLink()
	if err != nil {
		t.Fatalf("Error getting session link: %v", err)
	}

	// Verify the link
	if link == "" {
		t.Errorf("Expected non-empty link from GetLink")
	} else {
		t.Logf("Session link: %s", link)
	}
}

func TestSession_InfoMethod(t *testing.T) {
	// Initialize AgentBay client
	apiKey := getTestAPIKey(t)
	agentBay, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		t.Fatalf("Error initializing AgentBay client: %v", err)
	}

	// Create a session
	fmt.Println("Creating a new session for info testing...")
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

	// Test Info method
	fmt.Println("Testing session.Info method...")
	sessionInfo, err := session.Info()
	if err != nil {
		t.Fatalf("Error getting session info: %v", err)
	}

	// Verify the session info
	if sessionInfo == nil {
		t.Fatalf("Expected non-nil SessionInfo")
	}

	// Check SessionId field
	if sessionInfo.SessionId == "" {
		t.Errorf("Expected non-empty SessionId in SessionInfo")
	}
	if sessionInfo.SessionId != session.SessionID {
		t.Errorf("Expected SessionId to be '%s', got '%s'", session.SessionID, sessionInfo.SessionId)
	}

	// Check ResourceUrl field
	if sessionInfo.ResourceUrl == "" {
		t.Errorf("Expected non-empty ResourceUrl in SessionInfo")
	}
	t.Logf("Session ResourceUrl from Info: %s", sessionInfo.ResourceUrl)

	// Verify that session.ResourceUrl was updated with the value from the API response
	if session.ResourceUrl != sessionInfo.ResourceUrl {
		t.Errorf("Expected session.ResourceUrl to be updated with the value from sessionInfo.ResourceUrl")
	}

	// Log DesktopInfo fields (these may be empty depending on the API response)
	t.Logf("DesktopInfo - AppId: %s", sessionInfo.AppId)
	t.Logf("DesktopInfo - AuthCode: %s", sessionInfo.AuthCode)
	t.Logf("DesktopInfo - ConnectionProperties: %s", sessionInfo.ConnectionProperties)
	t.Logf("DesktopInfo - ResourceId: %s", sessionInfo.ResourceId)
	t.Logf("DesktopInfo - ResourceType: %s", sessionInfo.ResourceType)
}
