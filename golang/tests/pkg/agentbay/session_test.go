package agentbay_test

import (
	"fmt"
	"testing"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
	"github.com/aliyun/wuying-agentbay-sdk/golang/tests/pkg/agentbay/testutil"
)

func TestSession_Properties(t *testing.T) {
	// Initialize AgentBay client
	apiKey := testutil.GetTestAPIKey(t)
	agentBay, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		t.Fatalf("Error initializing AgentBay client: %v", err)
	}

	// Create a session
	fmt.Println("Creating a new session for session testing...")
	sessionResult, err := agentBay.Create(nil)
	if err != nil {
		t.Fatalf("Error creating session: %v", err)
	}

	// Verify RequestID from Create operation
	if sessionResult.RequestID == "" {
		t.Errorf("Create method did not return RequestID")
	} else {
		t.Logf("Create method successfully returned RequestID: %s", sessionResult.RequestID)
	}

	session := sessionResult.Session
	t.Logf("Session created with ID: %s", session.SessionID)

	defer func() {
		// Clean up the session after test
		fmt.Println("Cleaning up: Deleting the session...")
		deleteResult, err := agentBay.Delete(session)
		if err != nil {
			t.Logf("Warning: Error deleting session: %v", err)
		} else {
			// Verify RequestID from Delete operation
			if deleteResult.RequestID == "" {
				t.Errorf("Delete method did not return RequestID")
			} else {
				t.Logf("Session deleted (RequestID: %s)", deleteResult.RequestID)
			}
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

	// Test Info method and verify RequestID
	infoResult, err := session.Info()
	if err != nil {
		t.Errorf("Error getting session info: %v", err)
	} else {
		if infoResult.RequestID == "" {
			t.Errorf("Info method did not return RequestID")
		} else {
			t.Logf("Info method successfully returned RequestID: %s", infoResult.RequestID)
		}
	}
}

func TestSession_DeleteMethod(t *testing.T) {
	// Initialize AgentBay client
	apiKey := testutil.GetTestAPIKey(t)
	agentBay, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		t.Fatalf("Error initializing AgentBay client: %v", err)
	}

	// Create a session
	fmt.Println("Creating a new session for delete testing...")
	sessionResult, err := agentBay.Create(nil)
	if err != nil {
		t.Fatalf("Error creating session: %v", err)
	}

	// Verify RequestID from Create operation
	if sessionResult.RequestID == "" {
		t.Errorf("Create method did not return RequestID")
	} else {
		t.Logf("Create method successfully returned RequestID: %s", sessionResult.RequestID)
	}

	session := sessionResult.Session
	t.Logf("Session created with ID: %s", session.SessionID)

	// Test Delete method
	fmt.Println("Testing session.Delete method...")
	deleteResult, err := session.Delete()
	if err != nil {
		t.Fatalf("Error deleting session: %v", err)
	}

	// Verify RequestID from Delete operation
	if deleteResult.RequestID == "" {
		t.Errorf("Delete method did not return RequestID")
	} else {
		t.Logf("Session deleted (RequestID: %s)", deleteResult.RequestID)
	}

	// Verify the session was deleted by trying to list sessions
	listResult, err := agentBay.List()
	if err != nil {
		t.Fatalf("Error listing sessions: %v", err)
	}

	// Note: List method is a local operation and does not return RequestID
	t.Logf("Sessions listed (local operation, no RequestID)")

	// Check if the deleted session is not in the list
	for _, s := range listResult.Sessions {
		if s.SessionID == session.SessionID {
			t.Errorf("Session with ID %s still exists after deletion", session.SessionID)
		}
	}
}

func TestSession_GetLinkMethod(t *testing.T) {
	// Initialize AgentBay client
	apiKey := testutil.GetTestAPIKey(t)
	agentBay, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		t.Fatalf("Error initializing AgentBay client: %v", err)
	}

	// Create a session
	fmt.Println("Creating a new session for GetLink testing...")
	sessionParams := agentbay.NewCreateSessionParams().WithImageId("browser-use-debian-12")
	sessionResult, err := agentBay.Create(sessionParams)
	if err != nil {
		t.Fatalf("Error creating session: %v", err)
	}

	// Verify RequestID from Create operation
	if sessionResult.RequestID == "" {
		t.Errorf("Create method did not return RequestID")
	} else {
		t.Logf("Create method successfully returned RequestID: %s", sessionResult.RequestID)
	}

	session := sessionResult.Session
	t.Logf("Session created with ID: %s", session.SessionID)

	defer func() {
		// Clean up the session after test
		fmt.Println("Cleaning up: Deleting the session...")
		deleteResult, err := agentBay.Delete(session)
		if err != nil {
			t.Logf("Warning: Error deleting session: %v", err)
		} else {
			// Verify RequestID from Delete operation
			if deleteResult.RequestID == "" {
				t.Errorf("Delete method did not return RequestID")
			} else {
				t.Logf("Session deleted (RequestID: %s)", deleteResult.RequestID)
			}
		}
	}()

	// Test GetLink method
	fmt.Println("Testing session.GetLink method...")
	linkResult, err := session.GetLink()
	if err != nil {
		t.Fatalf("Error getting session link: %v", err)
	}

	// Verify RequestID from GetLink operation
	if linkResult.RequestID == "" {
		t.Errorf("GetLink method did not return RequestID")
	} else {
		t.Logf("Session link retrieved (RequestID: %s)", linkResult.RequestID)
	}

	// Verify the link
	if linkResult.Link == "" {
		t.Errorf("Expected non-empty link from GetLink")
	} else {
		t.Logf("Session link: %s", linkResult.Link)
	}
}

func TestSession_InfoMethod(t *testing.T) {
	// Initialize AgentBay client
	apiKey := testutil.GetTestAPIKey(t)
	agentBay, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		t.Fatalf("Error initializing AgentBay client: %v", err)
	}

	// Create a session
	fmt.Println("Creating a new session for info testing...")
	sessionResult, err := agentBay.Create(nil)
	if err != nil {
		t.Fatalf("Error creating session: %v", err)
	}

	// Verify RequestID from Create operation
	if sessionResult.RequestID == "" {
		t.Errorf("Create method did not return RequestID")
	} else {
		t.Logf("Create method successfully returned RequestID: %s", sessionResult.RequestID)
	}

	session := sessionResult.Session
	t.Logf("Session created with ID: %s", session.SessionID)

	defer func() {
		// Clean up the session after test
		fmt.Println("Cleaning up: Deleting the session...")
		deleteResult, err := agentBay.Delete(session)
		if err != nil {
			t.Logf("Warning: Error deleting session: %v", err)
		} else {
			// Verify RequestID from Delete operation
			if deleteResult.RequestID == "" {
				t.Errorf("Delete method did not return RequestID")
			} else {
				t.Logf("Session deleted (RequestID: %s)", deleteResult.RequestID)
			}
		}
	}()

	// Test Info method
	fmt.Println("Testing session.Info method...")
	infoResult, err := session.Info()
	if err != nil {
		t.Fatalf("Error getting session info: %v", err)
	}

	// Verify RequestID from Info operation
	if infoResult.RequestID == "" {
		t.Errorf("Info method did not return RequestID")
	} else {
		t.Logf("Session info retrieved (RequestID: %s)", infoResult.RequestID)
	}

	// Verify the session info
	if infoResult.Info == nil {
		t.Fatalf("Expected non-nil SessionInfo")
	}

	// Check SessionId field
	if infoResult.Info.SessionId == "" {
		t.Errorf("Expected non-empty SessionId in SessionInfo")
	}
	if infoResult.Info.SessionId != session.SessionID {
		t.Errorf("Expected SessionId to be '%s', got '%s'", session.SessionID, infoResult.Info.SessionId)
	}

	// Check ResourceUrl field
	if infoResult.Info.ResourceUrl == "" {
		t.Errorf("Expected non-empty ResourceUrl in SessionInfo")
	}
	t.Logf("Session ResourceUrl from Info: %s", infoResult.Info.ResourceUrl)

	// Verify that session.ResourceUrl was updated with the value from the API response
	if session.ResourceUrl != infoResult.Info.ResourceUrl {
		t.Errorf("Expected session.ResourceUrl to be updated with the value from sessionInfo.ResourceUrl")
	}

	// Log DesktopInfo fields (these may be empty depending on the API response)
	t.Logf("DesktopInfo - AppId: %s", infoResult.Info.AppId)
	t.Logf("DesktopInfo - AuthCode: %s", infoResult.Info.AuthCode)
	t.Logf("DesktopInfo - ConnectionProperties: %s", infoResult.Info.ConnectionProperties)
	t.Logf("DesktopInfo - ResourceId: %s", infoResult.Info.ResourceId)
	t.Logf("DesktopInfo - ResourceType: %s", infoResult.Info.ResourceType)
}
