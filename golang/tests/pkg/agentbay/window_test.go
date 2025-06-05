package agentbay_test

import (
	"fmt"
	"testing"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

func TestWindow_ListRootWindows(t *testing.T) {
	// Initialize AgentBay client
	apiKey := getTestAPIKey(t)
	agentBay, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		t.Fatalf("Error initializing AgentBay client: %v", err)
	}

	// Create a session
	fmt.Println("Creating a new session for window testing...")
	session, err := agentBay.Create(nil)
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

	// Test ListRootWindows
	if session.Window != nil {
		fmt.Println("Listing root windows...")
		rootWindows, err := session.Window.ListRootWindows()
		if err != nil {
			t.Logf("Note: ListRootWindows failed: %v", err)
		} else {
			t.Logf("Found %d root windows", len(rootWindows))

			// Verify we got some windows
			if len(rootWindows) == 0 {
				t.Logf("Warning: No root windows found")
			} else {
				// Print the first 3 windows or fewer if less than 3 are available
				count := min(len(rootWindows), 3)
				for i := 0; i < count; i++ {
					t.Logf("Window %d: %s (ID: %d)", i+1, rootWindows[i].Title, rootWindows[i].WindowID)
				}

				// Verify window properties
				for _, window := range rootWindows {
					if window.WindowID <= 0 {
						t.Errorf("Found window with invalid ID: %d", window.WindowID)
					}
				}
			}

			// Check if response contains "tool not found"
			if len(rootWindows) > 0 && containsToolNotFound(rootWindows[0].Title) {
				t.Errorf("Window.ListRootWindows returned 'tool not found'")
			}
		}
	} else {
		t.Logf("Note: Window interface is nil, skipping window test")
	}
}

func TestWindow_GetActiveWindow(t *testing.T) {
	// Initialize AgentBay client
	apiKey := getTestAPIKey(t)
	agentBay, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		t.Fatalf("Error initializing AgentBay client: %v", err)
	}

	// Create a session
	fmt.Println("Creating a new session for active window testing...")
	session, err := agentBay.Create(nil)
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

	// Test GetActiveWindow
	if session.Window != nil {
		fmt.Println("Getting active window...")
		activeWindow, err := session.Window.GetActiveWindow()
		if err != nil {
			t.Logf("Note: GetActiveWindow failed: %v", err)
		} else {
			t.Logf("Active window: %s (ID: %d, Process: %s, PID: %d)",
				activeWindow.Title, activeWindow.WindowID, activeWindow.PName, activeWindow.PID)

			// Verify window properties
			if activeWindow.WindowID <= 0 {
				t.Errorf("Active window has invalid ID: %d", activeWindow.WindowID)
			}
			if activeWindow.PID <= 0 {
				t.Errorf("Active window has invalid PID: %d", activeWindow.PID)
			}

			// Check if response contains "tool not found"
			if containsToolNotFound(activeWindow.Title) || containsToolNotFound(activeWindow.PName) {
				t.Errorf("Window.GetActiveWindow returned 'tool not found'")
			}
		}
	} else {
		t.Logf("Note: Window interface is nil, skipping window test")
	}
}

func TestWindow_FocusMode(t *testing.T) {
	// Initialize AgentBay client
	apiKey := getTestAPIKey(t)
	agentBay, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		t.Fatalf("Error initializing AgentBay client: %v", err)
	}

	// Create a session
	fmt.Println("Creating a new session for focus mode testing...")
	session, err := agentBay.Create(nil)
	if err != nil {
		t.Fatalf("Error creating session: %v", err)
	}
	t.Logf("Session created with ID: %s", session.SessionID)

	// IMPORTANT: Ensure cleanup of the session after test
	defer func() {
		// Make sure to disable focus mode before cleaning up
		if session.Window != nil {
			err := session.Window.FocusMode(false)
			if err != nil {
				t.Logf("Warning: Error disabling focus mode: %v", err)
			}
		}

		fmt.Println("Cleaning up: Deleting the session...")
		err := agentBay.Delete(session)
		if err != nil {
			t.Logf("Warning: Error deleting session: %v", err)
		} else {
			t.Log("Session successfully deleted")
		}
	}()

	// Test FocusMode
	if session.Window != nil {
		// Enable focus mode
		fmt.Println("Enabling focus mode...")
		err := session.Window.FocusMode(true)
		if err != nil {
			t.Logf("Note: Enabling focus mode failed: %v", err)
		} else {
			t.Logf("Focus mode enabled successfully")
		}

		// Disable focus mode
		fmt.Println("Disabling focus mode...")
		err = session.Window.FocusMode(false)
		if err != nil {
			t.Logf("Note: Disabling focus mode failed: %v", err)
		} else {
			t.Logf("Focus mode disabled successfully")
		}
	} else {
		t.Logf("Note: Window interface is nil, skipping focus mode test")
	}
}
