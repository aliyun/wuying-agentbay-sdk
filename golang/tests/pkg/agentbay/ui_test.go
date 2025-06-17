package agentbay_test

import (
	"fmt"
	"testing"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/ui"
)

func TestUI_Screenshot(t *testing.T) {
	// Initialize AgentBay client
	apiKey := getTestAPIKey(t)
	agentBay, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		t.Fatalf("Error initializing AgentBay client: %v", err)
	}

	// Create a session with mobile_latest image
	fmt.Println("Creating a new session for UI testing...")
	params := agentbay.NewCreateSessionParams().WithImageId("mobile_latest")
	session, err := agentBay.Create(params)
	if err != nil {
		t.Fatalf("Error creating session: %v", err)
	}
	t.Logf("Session created with ID: %s", session.SessionID)

	// IMPORTANT: Ensure cleanup of the session after test
	defer func() {
		fmt.Println("Cleaning up: Deleting the session...")
		err := agentBay.Delete(session)
		if err != nil {
			t.Logf("Warning: Error deleting session: %v", err)
		} else {
			t.Log("Session successfully deleted")
		}
	}()

	// Test UI screenshot functionality
	if session.UI != nil {
		fmt.Println("Taking a screenshot...")
		screenshot, err := session.UI.Screenshot()
		if err != nil {
			t.Logf("Note: Screenshot capture failed: %v", err)
		} else {
			t.Logf("Screenshot captured, data length: %d bytes", len(screenshot))
			// Check if response contains "tool not found"
			if containsToolNotFound(screenshot) {
				t.Errorf("UI.Screenshot returned 'tool not found'")
			}
		}
	} else {
		t.Logf("Note: UI interface is nil, skipping UI test")
	}
}

func TestUI_GetClickableUIElements(t *testing.T) {
	// Initialize AgentBay client
	apiKey := getTestAPIKey(t)
	agentBay, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		t.Fatalf("Error initializing AgentBay client: %v", err)
	}

	// Create a session with mobile_latest image
	fmt.Println("Creating a new session for UI testing...")
	params := agentbay.NewCreateSessionParams().WithImageId("mobile_latest")
	session, err := agentBay.Create(params)
	if err != nil {
		t.Fatalf("Error creating session: %v", err)
	}
	t.Logf("Session created with ID: %s", session.SessionID)

	// IMPORTANT: Ensure cleanup of the session after test
	defer func() {
		fmt.Println("Cleaning up: Deleting the session...")
		err := agentBay.Delete(session)
		if err != nil {
			t.Logf("Warning: Error deleting session: %v", err)
		} else {
			t.Log("Session successfully deleted")
		}
	}()

	// Test UI get clickable elements functionality
	if session.UI != nil {
		fmt.Println("Getting clickable UI elements...")
		elements, err := session.UI.GetClickableUIElements(2000)
		if err != nil {
			t.Logf("Note: GetClickableUIElements failed: %v", err)
		} else {
			t.Logf("Found %d clickable UI elements", len(elements))
		}
	} else {
		t.Logf("Note: UI interface is nil, skipping UI test")
	}
}

func TestUI_GetAllUIElements(t *testing.T) {
	// Initialize AgentBay client
	apiKey := getTestAPIKey(t)
	agentBay, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		t.Fatalf("Error initializing AgentBay client: %v", err)
	}

	// Create a session with mobile_latest image
	fmt.Println("Creating a new session for UI testing...")
	params := agentbay.NewCreateSessionParams().WithImageId("mobile_latest")
	session, err := agentBay.Create(params)
	if err != nil {
		t.Fatalf("Error creating session: %v", err)
	}
	t.Logf("Session created with ID: %s", session.SessionID)

	// IMPORTANT: Ensure cleanup of the session after test
	defer func() {
		fmt.Println("Cleaning up: Deleting the session...")
		err := agentBay.Delete(session)
		if err != nil {
			t.Logf("Warning: Error deleting session: %v", err)
		} else {
			t.Log("Session successfully deleted")
		}
	}()

	// Test UI get all elements functionality
	if session.UI != nil {
		fmt.Println("Getting all UI elements...")
		elements, err := session.UI.GetAllUIElements(2000)
		if err != nil {
			t.Logf("Note: GetAllUIElements failed: %v", err)
		} else {
			t.Logf("Found %d UI elements", len(elements))
			// Print the first element if available
			if len(elements) > 0 {
				t.Logf("First element: %v", elements[0])
			}
		}
	} else {
		t.Logf("Note: UI interface is nil, skipping UI test")
	}
}

func TestUI_SendKey(t *testing.T) {
	// Initialize AgentBay client
	apiKey := getTestAPIKey(t)
	agentBay, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		t.Fatalf("Error initializing AgentBay client: %v", err)
	}

	// Create a session with mobile_latest image
	fmt.Println("Creating a new session for UI testing...")
	params := agentbay.NewCreateSessionParams().WithImageId("mobile_latest")
	session, err := agentBay.Create(params)
	if err != nil {
		t.Fatalf("Error creating session: %v", err)
	}
	t.Logf("Session created with ID: %s", session.SessionID)

	// IMPORTANT: Ensure cleanup of the session after test
	defer func() {
		fmt.Println("Cleaning up: Deleting the session...")
		err := agentBay.Delete(session)
		if err != nil {
			t.Logf("Warning: Error deleting session: %v", err)
		} else {
			t.Log("Session successfully deleted")
		}
	}()

	// Test UI send key functionality
	if session.UI != nil {
		fmt.Println("Sending HOME key...")
		result, err := session.UI.SendKey(ui.KeyCode.HOME)
		if err != nil {
			t.Logf("Note: SendKey failed: %v", err)
		} else {
			t.Logf("SendKey result: %v", result)
		}
	} else {
		t.Logf("Note: UI interface is nil, skipping UI test")
	}
}

func TestUI_InputText(t *testing.T) {
	// Initialize AgentBay client
	apiKey := getTestAPIKey(t)
	agentBay, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		t.Fatalf("Error initializing AgentBay client: %v", err)
	}

	// Create a session with mobile_latest image
	fmt.Println("Creating a new session for UI testing...")
	params := agentbay.NewCreateSessionParams().WithImageId("mobile_latest")
	session, err := agentBay.Create(params)
	if err != nil {
		t.Fatalf("Error creating session: %v", err)
	}
	t.Logf("Session created with ID: %s", session.SessionID)

	// IMPORTANT: Ensure cleanup of the session after test
	defer func() {
		fmt.Println("Cleaning up: Deleting the session...")
		err := agentBay.Delete(session)
		if err != nil {
			t.Logf("Warning: Error deleting session: %v", err)
		} else {
			t.Log("Session successfully deleted")
		}
	}()

	// Test UI input text functionality
	if session.UI != nil {
		text := "Hello, world!"
		fmt.Printf("Inputting text: %s\n", text)
		err := session.UI.InputText(text)
		if err != nil {
			t.Logf("Note: InputText failed: %v", err)
		} else {
			t.Logf("InputText successful")
		}
	} else {
		t.Logf("Note: UI interface is nil, skipping UI test")
	}
}

func TestUI_Click(t *testing.T) {
	// Initialize AgentBay client
	apiKey := getTestAPIKey(t)
	agentBay, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		t.Fatalf("Error initializing AgentBay client: %v", err)
	}

	// Create a session with mobile_latest image
	fmt.Println("Creating a new session for UI testing...")
	params := agentbay.NewCreateSessionParams().WithImageId("mobile_latest")
	session, err := agentBay.Create(params)
	if err != nil {
		t.Fatalf("Error creating session: %v", err)
	}
	t.Logf("Session created with ID: %s", session.SessionID)

	// IMPORTANT: Ensure cleanup of the session after test
	defer func() {
		fmt.Println("Cleaning up: Deleting the session...")
		err := agentBay.Delete(session)
		if err != nil {
			t.Logf("Warning: Error deleting session: %v", err)
		} else {
			t.Log("Session successfully deleted")
		}
	}()

	// Test UI click functionality
	if session.UI != nil {
		x, y := 100, 200
		fmt.Printf("Clicking at coordinates (%d, %d)...\n", x, y)
		err := session.UI.Click(x, y, "left")
		if err != nil {
			t.Logf("Note: Click failed: %v", err)
		} else {
			t.Logf("Click successful")
		}
	} else {
		t.Logf("Note: UI interface is nil, skipping UI test")
	}
}

func TestUI_Swipe(t *testing.T) {
	// Initialize AgentBay client
	apiKey := getTestAPIKey(t)
	agentBay, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		t.Fatalf("Error initializing AgentBay client: %v", err)
	}

	// Create a session with mobile_latest image
	fmt.Println("Creating a new session for UI testing...")
	params := agentbay.NewCreateSessionParams().WithImageId("mobile_latest")
	session, err := agentBay.Create(params)
	if err != nil {
		t.Fatalf("Error creating session: %v", err)
	}
	t.Logf("Session created with ID: %s", session.SessionID)

	// IMPORTANT: Ensure cleanup of the session after test
	defer func() {
		fmt.Println("Cleaning up: Deleting the session...")
		err := agentBay.Delete(session)
		if err != nil {
			t.Logf("Warning: Error deleting session: %v", err)
		} else {
			t.Log("Session successfully deleted")
		}
	}()

	// Test UI swipe functionality
	if session.UI != nil {
		startX, startY, endX, endY, durationMs := 100, 200, 300, 400, 500
		fmt.Printf("Swiping from (%d, %d) to (%d, %d) in %dms...\n", startX, startY, endX, endY, durationMs)
		err := session.UI.Swipe(startX, startY, endX, endY, durationMs)
		if err != nil {
			t.Logf("Note: Swipe failed: %v", err)
		} else {
			t.Logf("Swipe successful")
		}
	} else {
		t.Logf("Note: UI interface is nil, skipping UI test")
	}
}
