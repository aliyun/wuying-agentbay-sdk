package integration

import (
	"fmt"
	"io"
	"net/http"
	"os"
	"path/filepath"
	"strings"
	"testing"
	"time"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

// TestComputerWindowsIntegration tests Computer window management functionality
// This test requires:
// 1. AGENTBAY_API_KEY environment variable
// 2. Real AgentBay session (windows_latest image preferred for window tests)
func TestComputerWindowsIntegration(t *testing.T) {
	// Skip if no API key provided
	apiKey := os.Getenv("AGENTBAY_API_KEY")
	if apiKey == "" {
		t.Skip("Skipping integration test: AGENTBAY_API_KEY not set")
	}

	// Create AgentBay client
	agentBay, err := agentbay.NewAgentBay(apiKey)
	require.NoError(t, err, "Failed to create AgentBay client")

	// Create session with windows image for window testing
	sessionParams := &agentbay.CreateSessionParams{
		ImageId: "linux_latest",
	}

	t.Log("Creating session for window integration test...")
	sessionResult, err := agentBay.Create(sessionParams)
	require.NoError(t, err, "Failed to create session")
	require.NotNil(t, sessionResult.Session, "Session should be created")

	session := sessionResult.Session
	defer func() {
		// Cleanup: Delete session after test
		t.Log("Cleaning up: Deleting session...")
		deleteResult, _ := session.Delete()
		if deleteResult != nil && deleteResult.Success {
			t.Logf("Session %s deleted successfully", session.SessionID)
		}
	}()

	t.Logf("Created session: %s", session.SessionID)

	// Wait for session to be fully ready (desktop environment)
	time.Sleep(10 * time.Second)

	var calculatorWindowID int

		t.Run("StartCalculatorApp", func(t *testing.T) {
		t.Log("Testing StartApp - Finding Calculator in installed apps...")
		
		// First, get installed apps to find Calculator
		installedApps, err := session.Computer.GetInstalledApps(true, false, true)
		startCmd := "calc.exe" // Default fallback
		
		if err != nil {
			t.Logf("GetInstalledApps failed: %v, using default calc.exe", err)
		} else {
			assert.NotNil(t, installedApps.Apps)
			t.Logf("Found %d installed apps", len(installedApps.Apps))
			
			// Look for Calculator app
			for _, app := range installedApps.Apps {
				if strings.Contains(strings.ToLower(app.Name), "calculator") ||
					strings.Contains(strings.ToLower(app.Name), "计算器") {
					startCmd = app.StartCmd
					t.Logf("Found Calculator app: %s (%s)", app.Name, app.StartCmd)
					break
				}
			}
		}
		
		t.Logf("Starting Calculator with command: %s", startCmd)
		result, err := session.Computer.StartApp(startCmd, "", "")

		assert.NoError(t, err, "StartApp should not return error")
		assert.NotNil(t, result, "Should return result")
		assert.NotEmpty(t, result.Processes, "Should return started processes")

		if len(result.Processes) > 0 {
			process := result.Processes[0]
			t.Logf("Started Calculator process: %s (PID: %d)", process.PName, process.PID)
			assert.Contains(t, strings.ToLower(process.PName), "calc", "Process name should contain 'calc'")
			assert.Greater(t, process.PID, 0)
		}

		// Wait for app to be fully loaded
		time.Sleep(3 * time.Second)
	})

	t.Run("ListRootWindows", func(t *testing.T) {
		t.Log("Testing ListRootWindows...")
		result, err := session.Computer.ListRootWindows()

		assert.NoError(t, err, "ListRootWindows should not return error")
		assert.NotNil(t, result, "Should return result")
		assert.NotNil(t, result.Windows, "Should return windows list")

		// Find Calculator window
		var foundCalculator bool
		for _, window := range result.Windows {
			t.Logf("Found window: %s (ID: %d)", window.Title, window.WindowID)
			if strings.Contains(strings.ToLower(window.Title), "calculator") ||
				strings.Contains(strings.ToLower(window.Title), "计算器") {
				calculatorWindowID = window.WindowID
				foundCalculator = true
				t.Logf("Found Calculator window: %s (ID: %d)", window.Title, window.WindowID)
				break
			}
		}

		assert.True(t, foundCalculator, "Calculator window should be found in root windows list")
		assert.Greater(t, calculatorWindowID, 0, "Calculator window ID should be valid")
	})

	t.Run("ActivateWindow", func(t *testing.T) {
		t.Log("Testing ActivateWindow...")
		require.Greater(t, calculatorWindowID, 0, "Calculator window ID should be available")

		result, err := session.Computer.ActivateWindow(calculatorWindowID)
		assert.NoError(t, err, "ActivateWindow should not return error")
		assert.NotNil(t, result, "Should return result")
		assert.True(t, result.Success, "ActivateWindow should succeed")

		t.Logf("Successfully activated Calculator window (ID: %d)", calculatorWindowID)

		// Wait for activation to take effect
		time.Sleep(1 * time.Second)
	})

	t.Run("GetActiveWindowValidation", func(t *testing.T) {
		t.Log("Testing GetActiveWindow validation...")

		result, err := session.Computer.GetActiveWindow()
		assert.NoError(t, err, "GetActiveWindow should not return error")
		assert.NotNil(t, result, "Should return result")
		assert.NotNil(t, result.Window, "Should return active window")

		if result.Window != nil {
			t.Logf("Active window: %s (ID: %d)", result.Window.Title, result.Window.WindowID)
			// The active window should be Calculator (though title might vary by locale)
			assert.True(t, 
				strings.Contains(strings.ToLower(result.Window.Title), "calculator") ||
				strings.Contains(strings.ToLower(result.Window.Title), "计算器") ||
				result.Window.WindowID == calculatorWindowID,
				"Active window should be Calculator or match our Calculator window ID")
		}
	})

	t.Run("FocusMode", func(t *testing.T) {
		t.Log("Testing FocusMode...")

		// Enable focus mode
		result, err := session.Computer.FocusMode(true)
		assert.NoError(t, err, "FocusMode(true) should not return error")
		assert.NotNil(t, result, "Should return result")
		assert.True(t, result.Success, "FocusMode(true) should succeed")
		t.Log("Focus mode enabled successfully")

		// Wait a moment
		time.Sleep(1 * time.Second)

		// Disable focus mode
		result, err = session.Computer.FocusMode(false)
		assert.NoError(t, err, "FocusMode(false) should not return error")
		assert.NotNil(t, result, "Should return result")
		assert.True(t, result.Success, "FocusMode(false) should succeed")
		t.Log("Focus mode disabled successfully")
	})

	t.Run("MaximizeWindowAndScreenshot", func(t *testing.T) {
		t.Log("Testing MaximizeWindow and Screenshot...")
		require.Greater(t, calculatorWindowID, 0, "Calculator window ID should be available")

		// Maximize window
		result, err := session.Computer.MaximizeWindow(calculatorWindowID)
		assert.NoError(t, err, "MaximizeWindow should not return error")
		assert.NotNil(t, result, "Should return result")
		assert.True(t, result.Success, "MaximizeWindow should succeed")
		t.Log("Calculator window maximized successfully")

		// Wait for maximize to take effect
		time.Sleep(2 * time.Second)

		// Take screenshot
		screenshot := session.Computer.Screenshot()
		assert.NotNil(t, screenshot, "Screenshot should return result")
		if screenshot.ErrorMessage == "" && screenshot.Data != "" {
			err := saveScreenshotFromURL(screenshot.Data, "calculator_maximized.png")
			if err != nil {
				t.Logf("Warning: Failed to save maximized screenshot: %v", err)
			} else {
				t.Log("Maximized screenshot saved as calculator_maximized.png")
			}
		} else {
			t.Logf("Screenshot failed or returned empty data: %s", screenshot.ErrorMessage)
		}
	})

	t.Run("MinimizeWindowAndScreenshot", func(t *testing.T) {
		t.Log("Testing MinimizeWindow and Screenshot...")
		require.Greater(t, calculatorWindowID, 0, "Calculator window ID should be available")

		// Minimize window
		result, err := session.Computer.MinimizeWindow(calculatorWindowID)
		assert.NoError(t, err, "MinimizeWindow should not return error")
		assert.NotNil(t, result, "Should return result")
		assert.True(t, result.Success, "MinimizeWindow should succeed")
		t.Log("Calculator window minimized successfully")

		// Wait for minimize to take effect
		time.Sleep(2 * time.Second)

		// Take screenshot
		screenshot := session.Computer.Screenshot()
		assert.NotNil(t, screenshot, "Screenshot should return result")
		if screenshot.ErrorMessage == "" && screenshot.Data != "" {
			err := saveScreenshotFromURL(screenshot.Data, "calculator_minimized.png")
			if err != nil {
				t.Logf("Warning: Failed to save minimized screenshot: %v", err)
			} else {
				t.Log("Minimized screenshot saved as calculator_minimized.png")
			}
		} else {
			t.Logf("Screenshot failed or returned empty data: %s", screenshot.ErrorMessage)
		}
	})

	t.Run("RestoreWindowAndScreenshot", func(t *testing.T) {
		t.Log("Testing RestoreWindow and Screenshot...")
		require.Greater(t, calculatorWindowID, 0, "Calculator window ID should be available")

		// Restore window
		result, err := session.Computer.RestoreWindow(calculatorWindowID)
		assert.NoError(t, err, "RestoreWindow should not return error")
		assert.NotNil(t, result, "Should return result")
		assert.True(t, result.Success, "RestoreWindow should succeed")
		t.Log("Calculator window restored successfully")

		// Wait for restore to take effect
		time.Sleep(2 * time.Second)

		// Take screenshot
		screenshot := session.Computer.Screenshot()
		assert.NotNil(t, screenshot, "Screenshot should return result")
		if screenshot.ErrorMessage == "" && screenshot.Data != "" {
			err := saveScreenshotFromURL(screenshot.Data, "calculator_restored.png")
			if err != nil {
				t.Logf("Warning: Failed to save restored screenshot: %v", err)
			} else {
				t.Log("Restored screenshot saved as calculator_restored.png")
			}
		} else {
			t.Logf("Screenshot failed or returned empty data: %s", screenshot.ErrorMessage)
		}
	})

	t.Run("ResizeWindowAndScreenshot", func(t *testing.T) {
		t.Log("Testing ResizeWindow and Screenshot...")
		require.Greater(t, calculatorWindowID, 0, "Calculator window ID should be available")

		// Resize window to 600x400
		result, err := session.Computer.ResizeWindow(calculatorWindowID, 600, 400)
		assert.NoError(t, err, "ResizeWindow should not return error")
		assert.NotNil(t, result, "Should return result")
		assert.True(t, result.Success, "ResizeWindow should succeed")
		t.Log("Calculator window resized to 600x400 successfully")

		// Wait for resize to take effect
		time.Sleep(2 * time.Second)

		// Take screenshot
		screenshot := session.Computer.Screenshot()
		assert.NotNil(t, screenshot, "Screenshot should return result")
		if screenshot.ErrorMessage == "" && screenshot.Data != "" {
			err := saveScreenshotFromURL(screenshot.Data, "calculator_resized.png")
			if err != nil {
				t.Logf("Warning: Failed to save resized screenshot: %v", err)
			} else {
				t.Log("Resized screenshot saved as calculator_resized.png")
			}
		} else {
			t.Logf("Screenshot failed or returned empty data: %s", screenshot.ErrorMessage)
		}
	})

	t.Run("FullscreenWindowAndScreenshot", func(t *testing.T) {
		t.Log("Testing FullscreenWindow and Screenshot...")
		require.Greater(t, calculatorWindowID, 0, "Calculator window ID should be available")

		// Make window fullscreen
		result, err := session.Computer.FullscreenWindow(calculatorWindowID)
		assert.NoError(t, err, "FullscreenWindow should not return error")
		assert.NotNil(t, result, "Should return result")
		assert.True(t, result.Success, "FullscreenWindow should succeed")
		t.Log("Calculator window set to fullscreen successfully")

		// Wait for fullscreen to take effect
		time.Sleep(2 * time.Second)

		// Take screenshot
		screenshot := session.Computer.Screenshot()
		assert.NotNil(t, screenshot, "Screenshot should return result")
		if screenshot.ErrorMessage == "" && screenshot.Data != "" {
			err := saveScreenshotFromURL(screenshot.Data, "calculator_fullscreen.png")
			if err != nil {
				t.Logf("Warning: Failed to save fullscreen screenshot: %v", err)
			} else {
				t.Log("Fullscreen screenshot saved as calculator_fullscreen.png")
			}
		} else {
			t.Logf("Screenshot failed or returned empty data: %s", screenshot.ErrorMessage)
		}
	})

	// Final cleanup - close Calculator
	t.Run("CleanupCalculator", func(t *testing.T) {
		t.Log("Cleaning up: Closing Calculator...")
		if calculatorWindowID > 0 {
			result, err := session.Computer.CloseWindow(calculatorWindowID)
			if err != nil {
				t.Logf("Warning: Failed to close Calculator window: %v", err)
			} else if result.Success {
				t.Log("Calculator window closed successfully")
			} else {
				t.Logf("Warning: CloseWindow returned false")
			}
		}
	})
}

// saveScreenshotFromURL downloads screenshot from URL and saves as PNG file
func saveScreenshotFromURL(screenshotURL, filename string) error {
	// Get the project root directory (go up from tests/pkg/integration to golang root)
	currentDir, err := os.Getwd()
	if err != nil {
		return fmt.Errorf("failed to get current directory: %w", err)
	}
	
	// Navigate to golang root directory (up 3 levels from tests/pkg/integration)
	golangRoot := filepath.Join(currentDir, "..", "..", "..")
	screenshotDir := filepath.Join(golangRoot, "screenshots")
	
	// Create screenshots directory if it doesn't exist
	if err := os.MkdirAll(screenshotDir, 0755); err != nil {
		return fmt.Errorf("failed to create screenshots directory: %w", err)
	}

	fmt.Printf("DEBUG: Downloading screenshot from URL: %s\n", screenshotURL)

	// Download the screenshot from URL
	resp, err := http.Get(screenshotURL)
	if err != nil {
		return fmt.Errorf("failed to download screenshot from URL: %w", err)
	}
	defer resp.Body.Close()

	// Check HTTP status
	if resp.StatusCode != http.StatusOK {
		return fmt.Errorf("failed to download screenshot: HTTP %d", resp.StatusCode)
	}

	// Read the response body
	imageData, err := io.ReadAll(resp.Body)
	if err != nil {
		return fmt.Errorf("failed to read screenshot data: %w", err)
	}

	// Validate that we have some image data
	if len(imageData) == 0 {
		return fmt.Errorf("downloaded image data is empty")
	}

	fmt.Printf("DEBUG: Downloaded image data length: %d bytes\n", len(imageData))

	// Write to file
	filePath := filepath.Join(screenshotDir, filename)
	if err := os.WriteFile(filePath, imageData, 0644); err != nil {
		return fmt.Errorf("failed to write screenshot file: %w", err)
	}

	fmt.Printf("DEBUG: Successfully saved screenshot to %s\n", filePath)
	return nil
}
