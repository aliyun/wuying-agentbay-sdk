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
	session, err := agentBay.Create(nil)
	if err != nil {
		fmt.Printf("\nError creating session: %v\n", err)
		os.Exit(1)
	}
	fmt.Printf("\nSession created with ID: %s\n", session.SessionID)

	// Application Management Examples
	fmt.Println("\n=== Application Management Examples ===")

	// Get installed applications
	fmt.Println("\nGetting installed applications...")
	apps, err := session.Application.GetInstalledApps(true, false, true)
	if err != nil {
		fmt.Printf("Error getting installed apps: %v\n", err)
	} else {
		fmt.Printf("Found %d installed applications\n", len(apps))
		// Print the first 3 apps or fewer if less than 3 are available
		count := min(len(apps), 3)
		for i := 0; i < count; i++ {
			fmt.Printf("App %d: %s\n", i+1, apps[i].Name)
		}
	}

	// List visible applications
	fmt.Println("\nListing visible applications...")
	visibleApps, err := session.Application.ListVisibleApps()
	if err != nil {
		fmt.Printf("Error listing visible apps: %v\n", err)
	} else {
		fmt.Printf("Found %d visible applications\n", len(visibleApps))
		// Print the first 3 apps or fewer if less than 3 are available
		count := min(len(visibleApps), 3)
		for i := 0; i < count; i++ {
			fmt.Printf("Process %d: %s (PID: %d)\n", i+1, visibleApps[i].PName, visibleApps[i].PID)
		}
	}

	// Window Management Examples
	fmt.Println("\n=== Window Management Examples ===")

	// List root windows
	fmt.Println("\nListing root windows...")
	rootWindows, err := session.Window.ListRootWindows()
	if err != nil {
		fmt.Printf("Error listing root windows: %v\n", err)
	} else {
		fmt.Printf("Found %d root windows\n", len(rootWindows))
		// Print the first 3 windows or fewer if less than 3 are available
		count := min(len(rootWindows), 3)
		for i := 0; i < count; i++ {
			fmt.Printf("Window %d: %s (ID: %d)\n", i+1, rootWindows[i].Title, rootWindows[i].WindowID)
		}
	}

	// Get active window
	fmt.Println("\nGetting active window...")
	activeWindow, err := session.Window.GetActiveWindow()
	if err != nil {
		fmt.Printf("Error getting active window: %v\n", err)
	} else {
		fmt.Printf("Active window: %s (ID: %d, Process: %s, PID: %d)\n",
			activeWindow.Title, activeWindow.WindowID, activeWindow.PName, activeWindow.PID)
	}

	// Window operations
	if len(rootWindows) > 0 {
		windowID := rootWindows[0].WindowID

		// Activate window
		fmt.Printf("\nActivating window with ID %d...\n", windowID)
		if err := session.Window.ActivateWindow(windowID); err != nil {
			fmt.Printf("Error activating window: %v\n", err)
		} else {
			fmt.Println("Window activated successfully")
		}

		// Maximize window
		fmt.Printf("\nMaximizing window with ID %d...\n", windowID)
		if err := session.Window.MaximizeWindow(windowID); err != nil {
			fmt.Printf("Error maximizing window: %v\n", err)
		} else {
			fmt.Println("Window maximized successfully")
		}

		// Minimize window
		fmt.Printf("\nMinimizing window with ID %d...\n", windowID)
		if err := session.Window.MinimizeWindow(windowID); err != nil {
			fmt.Printf("Error minimizing window: %v\n", err)
		} else {
			fmt.Println("Window minimized successfully")
		}

		// Restore window
		fmt.Printf("\nRestoring window with ID %d...\n", windowID)
		if err := session.Window.RestoreWindow(windowID); err != nil {
			fmt.Printf("Error restoring window: %v\n", err)
		} else {
			fmt.Println("Window restored successfully")
		}

		// Resize window
		fmt.Printf("\nResizing window with ID %d to 800x600...\n", windowID)
		if err := session.Window.ResizeWindow(windowID, 800, 600); err != nil {
			fmt.Printf("Error resizing window: %v\n", err)
		} else {
			fmt.Println("Window resized successfully")
		}
	}

	// Focus mode
	// Enable focus mode
	fmt.Println("\nEnabling focus mode...")
	if err := session.Window.FocusMode(true); err != nil {
		fmt.Printf("Error enabling focus mode: %v\n", err)
	} else {
		fmt.Println("Focus mode enabled successfully")
	}

	// Disable focus mode
	fmt.Println("\nDisabling focus mode...")
	if err := session.Window.FocusMode(false); err != nil {
		fmt.Printf("Error disabling focus mode: %v\n", err)
	} else {
		fmt.Println("Focus mode disabled successfully")
	}

	// Delete the session
	fmt.Println("\nDeleting the session...")
	err = agentBay.Delete(session)
	if err != nil {
		fmt.Printf("Error deleting session: %v\n", err)
		os.Exit(1)
	}
	fmt.Println("Session deleted successfully")
}

// min returns the smaller of x or y.
func min(x, y int) int {
	if x < y {
		return x
	}
	return y
}
