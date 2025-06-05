package integration_test

import (
	"fmt"
	"testing"
	"time"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

func TestWindow_WindowOperations(t *testing.T) {
	// Initialize AgentBay client
	apiKey := getTestAPIKey(t)
	agentBay, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		t.Fatalf("Error initializing AgentBay client: %v", err)
	}

	// Create a session
	fmt.Println("Creating a new session for window operations testing...")
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

	// Test window operations
	if session.Window != nil && session.Application != nil {
		// First, start Google Chrome
		fmt.Println("Starting Google Chrome application...")
		startCmd := "/usr/bin/google-chrome-stable"
		processes, err := session.Application.StartApp(startCmd, "")
		if err != nil {
			t.Logf("Note: Failed to start Google Chrome: %v", err)
			t.Logf("Continuing with existing windows...")
		} else {
			t.Logf("Google Chrome started successfully, returned %d processes", len(processes))

			// Give Chrome some time to initialize
			time.Sleep(3 * time.Second)

			// Clean up Chrome processes at the end
			defer func() {
				for _, process := range processes {
					if process.PID > 0 {
						fmt.Printf("Attempting to stop Chrome process (PID: %d)...\n", process.PID)
						stopErr := session.Application.StopAppByPID(process.PID)
						if stopErr != nil {
							t.Logf("Warning: Failed to stop Chrome process: %v", stopErr)
						} else {
							t.Logf("Successfully stopped Chrome process (PID: %d)", process.PID)
						}
					}
				}
			}()
		}

		// Get a list of root windows
		rootWindows, err := session.Window.ListRootWindows()
		if err != nil {
			t.Logf("Note: ListRootWindows failed: %v", err)
			return
		}

		if len(rootWindows) == 0 {
			t.Logf("No windows available for testing window operations")
			return
		}

		// Try to find a Chrome window for testing
		var windowID int
		var windowFound bool
		for _, window := range rootWindows {
			if window.PName == "chrome" {
				windowID = window.WindowID
				windowFound = true
				t.Logf("Found Chrome window with ID %d for testing window operations", windowID)
				break
			}
		}

		// If no Chrome window found, use the first window
		if !windowFound {
			windowID = rootWindows[0].WindowID
			t.Logf("No Chrome window found, using window with ID %d for testing window operations", windowID)
		}

		// Test RestoreWindow
		fmt.Printf("Restoring window with ID %d...\n", windowID)
		err = session.Window.RestoreWindow(windowID)
		if err != nil {
			t.Logf("Note: RestoreWindow failed: %v", err)
		} else {
			t.Logf("Window restored successfully")
		}
		// Wait for 3 seconds to allow user to see the result
		time.Sleep(3 * time.Second)

		// Test ResizeWindow
		fmt.Printf("Resizing window with ID %d to 800x600...\n", windowID)
		err = session.Window.ResizeWindow(windowID, 800, 600)
		if err != nil {
			t.Logf("Note: ResizeWindow failed: %v", err)
		} else {
			t.Logf("Window resized successfully")
		}
		// Wait for 3 seconds to allow user to see the result
		time.Sleep(3 * time.Second)

		// Test MinimizeWindow
		fmt.Printf("Minimizing window with ID %d...\n", windowID)
		err = session.Window.MinimizeWindow(windowID)
		if err != nil {
			t.Logf("Note: MinimizeWindow failed: %v", err)
		} else {
			t.Logf("Window minimized successfully")
		}
		// Wait for 3 seconds to allow user to see the result
		time.Sleep(3 * time.Second)

		// Test MaximizeWindow
		fmt.Printf("Maximizing window with ID %d...\n", windowID)
		err = session.Window.MaximizeWindow(windowID)
		if err != nil {
			t.Logf("Note: MaximizeWindow failed: %v", err)
		} else {
			t.Logf("Window maximized successfully")
		}
		// Wait for 3 seconds to allow user to see the result
		time.Sleep(3 * time.Second)

		// Start a terminal
		fmt.Println("Starting gnome-terminal...")
		terminalProcesses, err := session.Application.StartApp("/usr/bin/gnome-terminal", "")
		if err != nil {
			t.Logf("Note: Failed to start gnome-terminal: %v", err)
		} else {
			t.Logf("Terminal started successfully, returned %d processes", len(terminalProcesses))

			// Give terminal some time to initialize
			time.Sleep(3 * time.Second)

			// Clean up terminal processes at the end
			defer func() {
				for _, process := range terminalProcesses {
					if process.PID > 0 {
						fmt.Printf("Attempting to stop terminal process (PID: %d)...\n", process.PID)
						stopErr := session.Application.StopAppByPID(process.PID)
						if stopErr != nil {
							t.Logf("Warning: Failed to stop terminal process: %v", stopErr)
						} else {
							t.Logf("Successfully stopped terminal process (PID: %d)", process.PID)
						}
					}
				}
			}()
		}

		// Activate the Chrome window again
		fmt.Printf("Activating Chrome window with ID %d again...\n", windowID)
		err = session.Window.ActivateWindow(windowID)
		if err != nil {
			t.Logf("Note: ActivateWindow failed: %v", err)
		} else {
			t.Logf("Window activated successfully")
		}
		// Wait for 3 seconds to allow user to see the result
		time.Sleep(3 * time.Second)

		// Test FullscreenWindow
		fmt.Printf("Fullscreening window with ID %d...\n", windowID)
		err = session.Window.FullscreenWindow(windowID)
		if err != nil {
			t.Logf("Note: FullscreenWindow failed: %v", err)
		} else {
			t.Logf("Window fullscreened successfully")
		}
		// Wait for 3 seconds to allow user to see the result
		time.Sleep(3 * time.Second)

		// Test CloseWindow
		fmt.Printf("Closing window with ID %d...\n", windowID)
		err = session.Window.CloseWindow(windowID)
		if err != nil {
			t.Logf("Note: CloseWindow failed: %v", err)
		} else {
			t.Logf("Window closed successfully")
		}
		// Wait for 3 seconds to allow user to see the result
		time.Sleep(3 * time.Second)
	} else {
		t.Logf("Note: Window interface is nil, skipping window operations test")
	}
}
