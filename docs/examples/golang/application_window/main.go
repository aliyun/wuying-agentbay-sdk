package main

import (
	"fmt"
	"os"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

func main() {
	// Get API key from environment variable or use a default value for testing
	apiKey := os.Getenv("AGENTBAY_API_KEY")
	if apiKey == "" {
		apiKey = "akm-xxx" // Replace with your actual API key for testing
		fmt.Println("Warning: Using default API key. Set AGENTBAY_API_KEY environment variable for production use.")
	}

	// Initialize the AgentBay client
	agentBay, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		fmt.Printf("Error initializing AgentBay client: %v\n", err)
		os.Exit(1)
	}

	// Create a new session with default parameters
	fmt.Println("\nCreating a new session...")
	params := agentbay.NewCreateSessionParams().WithImageId("linux_latest")
	sessionResult, err := agentBay.Create(params)
	if err != nil {
		fmt.Printf("\nError creating session: %v\n", err)
		os.Exit(1)
	}
	session := sessionResult.Session
	fmt.Printf("\nSession created with ID: %s\n", session.SessionID)

	// Application Management Examples
	fmt.Println("\n=== Application Management Examples ===")

	// Get installed applications
	fmt.Println("\nGetting installed applications...")
	appsResult, err := session.Application.GetInstalledApps(true, false, true)
	if err != nil {
		fmt.Printf("Error getting installed apps: %v\n", err)
	} else {
		fmt.Printf("Found %d installed applications\n", len(appsResult.Applications))
		// Print the first 3 apps or fewer if less than 3 are available
		count := min(len(appsResult.Applications), 3)
		for i := 0; i < count; i++ {
			fmt.Printf("App %d: %s\n", i+1, appsResult.Applications[i].Name)
		}
	}

	// List visible applications
	fmt.Println("\nListing visible applications...")
	visibleAppsResult, err := session.Application.ListVisibleApps()
	if err != nil {
		fmt.Printf("Error listing visible apps: %v\n", err)
	} else {
		fmt.Printf("Found %d visible applications\n", len(visibleAppsResult.Processes))
		// Print the first 3 apps or fewer if less than 3 are available
		count := min(len(visibleAppsResult.Processes), 3)
		for i := 0; i < count; i++ {
			fmt.Printf("Process %d: %s (PID: %d)\n", i+1, visibleAppsResult.Processes[i].PName, visibleAppsResult.Processes[i].PID)
		}
	}

	// Window Management Examples
	fmt.Println("\n=== Window Management Examples ===")

	// List root windows
	fmt.Println("\nListing root windows...")
	rootWindowsResult, err := session.Window.ListRootWindows()
	if err != nil {
		fmt.Printf("Error listing root windows: %v\n", err)
	} else {
		fmt.Printf("Found %d root windows\n", len(rootWindowsResult.Windows))
		// Print the first 3 windows or fewer if less than 3 are available
		count := min(len(rootWindowsResult.Windows), 3)
		for i := 0; i < count; i++ {
			fmt.Printf("Window %d: %s (ID: %d)\n", i+1, rootWindowsResult.Windows[i].Title, rootWindowsResult.Windows[i].WindowID)
		}
	}

	// Get active window
	fmt.Println("\nGetting active window...")
	activeWindowResult, err := session.Window.GetActiveWindow()
	if err != nil {
		fmt.Printf("Error getting active window: %v\n", err)
	} else if activeWindowResult != nil && activeWindowResult.Window != nil {
		fmt.Printf("Active window: %s (ID: %d, Process: %s, PID: %d)\n",
			activeWindowResult.Window.Title, activeWindowResult.Window.WindowID, activeWindowResult.Window.PName, activeWindowResult.Window.PID)
	} else {
		fmt.Println("No active window found")
	}

	// Window operations
	var windowID int
	if rootWindowsResult != nil && len(rootWindowsResult.Windows) > 0 {
		windowID = rootWindowsResult.Windows[0].WindowID

		// Activate window
		fmt.Printf("\nActivating window with ID %d...\n", windowID)
		activateResult, err := session.Window.ActivateWindow(windowID)
		if err != nil {
			fmt.Printf("Error activating window: %v\n", err)
		} else {
			fmt.Printf("Window activated successfully (RequestID: %s)\n", activateResult.RequestID)
		}

		// Maximize window
		fmt.Printf("\nMaximizing window with ID %d...\n", windowID)
		maximizeResult, err := session.Window.MaximizeWindow(windowID)
		if err != nil {
			fmt.Printf("Error maximizing window: %v\n", err)
		} else {
			fmt.Printf("Window maximized successfully (RequestID: %s)\n", maximizeResult.RequestID)
		}

		// Minimize window
		fmt.Printf("\nMinimizing window with ID %d...\n", windowID)
		minimizeResult, err := session.Window.MinimizeWindow(windowID)
		if err != nil {
			fmt.Printf("Error minimizing window: %v\n", err)
		} else {
			fmt.Printf("Window minimized successfully (RequestID: %s)\n", minimizeResult.RequestID)
		}

		// Restore window
		fmt.Printf("\nRestoring window with ID %d...\n", windowID)
		restoreResult, err := session.Window.RestoreWindow(windowID)
		if err != nil {
			fmt.Printf("Error restoring window: %v\n", err)
		} else {
			fmt.Printf("Window restored successfully (RequestID: %s)\n", restoreResult.RequestID)
		}

		// Resize window
		fmt.Printf("\nResizing window with ID %d to 800x600...\n", windowID)
		resizeResult, err := session.Window.ResizeWindow(windowID, 800, 600)
		if err != nil {
			fmt.Printf("Error resizing window: %v\n", err)
		} else {
			fmt.Printf("Window resized successfully (RequestID: %s)\n", resizeResult.RequestID)
		}
	}

	// Focus mode
	// Enable focus mode
	fmt.Println("\nEnabling focus mode...")
	focusEnableResult, err := session.Window.FocusMode(true)
	if err != nil {
		fmt.Printf("Error enabling focus mode: %v\n", err)
	} else {
		fmt.Printf("Focus mode enabled successfully (RequestID: %s)\n", focusEnableResult.RequestID)
	}

	// Disable focus mode
	fmt.Println("\nDisabling focus mode...")
	focusDisableResult, err := session.Window.FocusMode(false)
	if err != nil {
		fmt.Printf("Error disabling focus mode: %v\n", err)
	} else {
		fmt.Printf("Focus mode disabled successfully (RequestID: %s)\n", focusDisableResult.RequestID)
	}

	// Delete the session
	fmt.Println("\nDeleting the session...")
	deleteResult, err := session.Delete()
	if err != nil {
		fmt.Printf("Error deleting session: %v\n", err)
		os.Exit(1)
	}
	fmt.Printf("Session deleted successfully (RequestID: %s)\n", deleteResult.RequestID)
}

// min returns the smaller of x or y.
func min(x, y int) int {
	if x < y {
		return x
	}
	return y
}
