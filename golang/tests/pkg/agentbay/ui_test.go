package agentbay_test

import (
	"fmt"
	"testing"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/ui"
	"github.com/aliyun/wuying-agentbay-sdk/golang/tests/pkg/agentbay/testutil"
)

func TestUI_Screenshot(t *testing.T) {
	// Initialize AgentBay client
	apiKey := testutil.GetTestAPIKey(t)
	agentBay, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		t.Fatalf("Error initializing AgentBay client: %v", err)
	}

	// Create a session with mobile_latest image
	fmt.Println("Creating a new session for UI testing...")
	params := agentbay.NewCreateSessionParams().WithImageId("mobile_latest")
	sessionResult, err := agentBay.Create(params)
	if err != nil {
		t.Fatalf("Error creating session: %v", err)
	}

	session := sessionResult.Session
	t.Logf("Session created with ID: %s (RequestID: %s)",
		session.SessionID, sessionResult.RequestID)

	// IMPORTANT: Ensure cleanup of the session after test
	defer func() {
		fmt.Println("Cleaning up: Deleting the session...")
		deleteResult, err := agentBay.Delete(session)
		if err != nil {
			t.Logf("Warning: Error deleting session: %v", err)
		} else {
			t.Logf("Session successfully deleted (RequestID: %s)",
				deleteResult.RequestID)
		}
	}()

	// Test UI screenshot functionality
	if session.UI != nil {
		fmt.Println("Taking a screenshot...")
		screenshotResult, err := session.UI.Screenshot()
		if err != nil {
			t.Logf("Note: Screenshot capture failed: %v", err)
		} else {
			t.Logf("Screenshot captured successfully (RequestID: %s)",
				screenshotResult.RequestID)

			// Check if the operation was successful
			if !screenshotResult.Success {
				t.Errorf("Screenshot operation returned unsuccessful status")
			}

			// Check component ID
			if screenshotResult.ComponentID == "" {
				t.Logf("Warning: Empty component ID from Screenshot operation")
			}
		}
	} else {
		t.Logf("Note: UI interface is nil, skipping UI test")
	}
}

func TestUI_GetClickableUIElements(t *testing.T) {
	// Initialize AgentBay client
	apiKey := testutil.GetTestAPIKey(t)
	agentBay, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		t.Fatalf("Error initializing AgentBay client: %v", err)
	}

	// Create a session with mobile_latest image
	fmt.Println("Creating a new session for UI testing...")
	params := agentbay.NewCreateSessionParams().WithImageId("mobile_latest")
	sessionResult, err := agentBay.Create(params)
	if err != nil {
		t.Fatalf("Error creating session: %v", err)
	}

	session := sessionResult.Session
	t.Logf("Session created with ID: %s (RequestID: %s)",
		session.SessionID, sessionResult.RequestID)

	// IMPORTANT: Ensure cleanup of the session after test
	defer func() {
		fmt.Println("Cleaning up: Deleting the session...")
		deleteResult, err := agentBay.Delete(session)
		if err != nil {
			t.Logf("Warning: Error deleting session: %v", err)
		} else {
			t.Logf("Session successfully deleted (RequestID: %s)",
				deleteResult.RequestID)
		}
	}()

	// Test UI get clickable elements functionality
	if session.UI != nil {
		fmt.Println("Getting clickable UI elements...")
		elementsResult, err := session.UI.GetClickableUIElements(2000)
		if err != nil {
			t.Logf("Note: GetClickableUIElements failed: %v", err)
		} else {
			t.Logf("Found %d clickable UI elements (RequestID: %s)",
				len(elementsResult.Elements), elementsResult.RequestID)

			// Print the first element if available
			if len(elementsResult.Elements) > 0 {
				t.Logf("First element: Type=%s, Text=%s",
					elementsResult.Elements[0].Type, elementsResult.Elements[0].Text)
			}
		}
	} else {
		t.Logf("Note: UI interface is nil, skipping UI test")
	}
}

func TestUI_GetAllUIElements(t *testing.T) {
	// Initialize AgentBay client
	apiKey := testutil.GetTestAPIKey(t)
	agentBay, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		t.Fatalf("Error initializing AgentBay client: %v", err)
	}

	// Create a session with mobile_latest image
	fmt.Println("Creating a new session for UI testing...")
	params := agentbay.NewCreateSessionParams().WithImageId("mobile_latest")
	sessionResult, err := agentBay.Create(params)
	if err != nil {
		t.Fatalf("Error creating session: %v", err)
	}

	session := sessionResult.Session
	t.Logf("Session created with ID: %s (RequestID: %s)",
		session.SessionID, sessionResult.RequestID)

	// IMPORTANT: Ensure cleanup of the session after test
	defer func() {
		fmt.Println("Cleaning up: Deleting the session...")
		deleteResult, err := agentBay.Delete(session)
		if err != nil {
			t.Logf("Warning: Error deleting session: %v", err)
		} else {
			t.Logf("Session successfully deleted (RequestID: %s)",
				deleteResult.RequestID)
		}
	}()

	// Test UI get all elements functionality
	if session.UI != nil {
		fmt.Println("Getting all UI elements...")
		elementsResult, err := session.UI.GetAllUIElements(2000)
		if err != nil {
			t.Logf("Note: GetAllUIElements failed: %v", err)
		} else {
			t.Logf("Found %d UI elements (RequestID: %s)",
				len(elementsResult.Elements), elementsResult.RequestID)

			// Print the first element if available
			if len(elementsResult.Elements) > 0 {
				t.Logf("First element: Type=%s, Text=%s, ResourceId=%s",
					elementsResult.Elements[0].Type,
					elementsResult.Elements[0].Text,
					elementsResult.Elements[0].ResourceId)
			}
		}
	} else {
		t.Logf("Note: UI interface is nil, skipping UI test")
	}
}

func TestUI_SendKey(t *testing.T) {
	// Initialize AgentBay client
	apiKey := testutil.GetTestAPIKey(t)
	agentBay, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		t.Fatalf("Error initializing AgentBay client: %v", err)
	}

	// Create a session with mobile_latest image
	fmt.Println("Creating a new session for UI testing...")
	params := agentbay.NewCreateSessionParams().WithImageId("mobile_latest")
	sessionResult, err := agentBay.Create(params)
	if err != nil {
		t.Fatalf("Error creating session: %v", err)
	}

	session := sessionResult.Session
	t.Logf("Session created with ID: %s (RequestID: %s)",
		session.SessionID, sessionResult.RequestID)

	// IMPORTANT: Ensure cleanup of the session after test
	defer func() {
		fmt.Println("Cleaning up: Deleting the session...")
		deleteResult, err := agentBay.Delete(session)
		if err != nil {
			t.Logf("Warning: Error deleting session: %v", err)
		} else {
			t.Logf("Session successfully deleted (RequestID: %s)",
				deleteResult.RequestID)
		}
	}()

	// Test UI send key functionality
	if session.UI != nil {
		fmt.Println("Sending HOME key...")
		keyResult, err := session.UI.SendKey(ui.KeyCode.HOME)
		if err != nil {
			t.Logf("Note: SendKey failed: %v", err)
		} else {
			t.Logf("SendKey successful (RequestID: %s, Success: %v)",
				keyResult.RequestID, keyResult.Success)
		}
	} else {
		t.Logf("Note: UI interface is nil, skipping UI test")
	}
}

func TestUI_InputText(t *testing.T) {
	// Initialize AgentBay client
	apiKey := testutil.GetTestAPIKey(t)
	agentBay, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		t.Fatalf("Error initializing AgentBay client: %v", err)
	}

	// Create a session with mobile_latest image
	fmt.Println("Creating a new session for UI testing...")
	params := agentbay.NewCreateSessionParams().WithImageId("mobile_latest")
	sessionResult, err := agentBay.Create(params)
	if err != nil {
		t.Fatalf("Error creating session: %v", err)
	}

	session := sessionResult.Session
	t.Logf("Session created with ID: %s (RequestID: %s)",
		session.SessionID, sessionResult.RequestID)

	// IMPORTANT: Ensure cleanup of the session after test
	defer func() {
		fmt.Println("Cleaning up: Deleting the session...")
		deleteResult, err := agentBay.Delete(session)
		if err != nil {
			t.Logf("Warning: Error deleting session: %v", err)
		} else {
			t.Logf("Session successfully deleted (RequestID: %s)",
				deleteResult.RequestID)
		}
	}()

	// Test UI input text functionality
	if session.UI != nil {
		fmt.Println("Inputting text...")
		testText := "Hello AgentBay!"
		textResult, err := session.UI.InputText(testText)
		if err != nil {
			t.Logf("Note: InputText failed: %v", err)
		} else {
			t.Logf("InputText successful (RequestID: %s, Text: %s)",
				textResult.RequestID, textResult.Text)
		}
	} else {
		t.Logf("Note: UI interface is nil, skipping UI test")
	}
}

func TestUI_Click(t *testing.T) {
	// Initialize AgentBay client
	apiKey := testutil.GetTestAPIKey(t)
	agentBay, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		t.Fatalf("Error initializing AgentBay client: %v", err)
	}

	// Create a session with mobile_latest image
	fmt.Println("Creating a new session for UI testing...")
	params := agentbay.NewCreateSessionParams().WithImageId("mobile_latest")
	sessionResult, err := agentBay.Create(params)
	if err != nil {
		t.Fatalf("Error creating session: %v", err)
	}

	session := sessionResult.Session
	t.Logf("Session created with ID: %s (RequestID: %s)",
		session.SessionID, sessionResult.RequestID)

	// IMPORTANT: Ensure cleanup of the session after test
	defer func() {
		fmt.Println("Cleaning up: Deleting the session...")
		deleteResult, err := agentBay.Delete(session)
		if err != nil {
			t.Logf("Warning: Error deleting session: %v", err)
		} else {
			t.Logf("Session successfully deleted (RequestID: %s)",
				deleteResult.RequestID)
		}
	}()

	// Test UI click functionality
	if session.UI != nil {
		fmt.Println("Clicking at position (100, 100)...")
		clickResult, err := session.UI.Click(100, 100, "left")
		if err != nil {
			t.Logf("Note: Click failed: %v", err)
		} else {
			t.Logf("Click successful (RequestID: %s, Success: %v)",
				clickResult.RequestID, clickResult.Success)
		}
	} else {
		t.Logf("Note: UI interface is nil, skipping UI test")
	}
}

func TestUI_Swipe(t *testing.T) {
	// Initialize AgentBay client
	apiKey := testutil.GetTestAPIKey(t)
	agentBay, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		t.Fatalf("Error initializing AgentBay client: %v", err)
	}

	// Create a session with mobile_latest image
	fmt.Println("Creating a new session for UI testing...")
	params := agentbay.NewCreateSessionParams().WithImageId("mobile_latest")
	sessionResult, err := agentBay.Create(params)
	if err != nil {
		t.Fatalf("Error creating session: %v", err)
	}

	session := sessionResult.Session
	t.Logf("Session created with ID: %s (RequestID: %s)",
		session.SessionID, sessionResult.RequestID)

	// IMPORTANT: Ensure cleanup of the session after test
	defer func() {
		fmt.Println("Cleaning up: Deleting the session...")
		deleteResult, err := agentBay.Delete(session)
		if err != nil {
			t.Logf("Warning: Error deleting session: %v", err)
		} else {
			t.Logf("Session successfully deleted (RequestID: %s)",
				deleteResult.RequestID)
		}
	}()

	// Test UI swipe functionality
	if session.UI != nil {
		fmt.Println("Swiping from (100, 500) to (100, 100)...")
		swipeResult, err := session.UI.Swipe(100, 500, 100, 100, 500)
		if err != nil {
			t.Logf("Note: Swipe failed: %v", err)
		} else {
			t.Logf("Swipe successful (RequestID: %s, Success: %v)",
				swipeResult.RequestID, swipeResult.Success)
		}
	} else {
		t.Logf("Note: UI interface is nil, skipping UI test")
	}
}
