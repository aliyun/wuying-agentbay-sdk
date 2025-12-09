package integration

import (
	"os"
	"testing"
	"time"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

// TestComputerAppsIntegration tests Computer application management functionality
// This test requires:
// 1. AGENTBAY_API_KEY environment variable
// 2. Real AgentBay session (windows_latest image preferred for app tests)
func TestComputerAppsIntegration(t *testing.T) {
	// Skip if no API key provided
	apiKey := os.Getenv("AGENTBAY_API_KEY")
	if apiKey == "" {
		t.Skip("Skipping integration test: AGENTBAY_API_KEY not set")
	}

	// Create AgentBay client
	agentBay, err := agentbay.NewAgentBay(apiKey)
	require.NoError(t, err, "Failed to create AgentBay client")

	// Create session with windows image for app testing (notepad is standard)
	sessionParams := &agentbay.CreateSessionParams{
		ImageId: "windows_latest",
	}

	t.Log("Creating session for app integration test...")
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

	t.Run("StartApp", func(t *testing.T) {
		t.Log("Testing StartApp (notepad.exe)...")
		result, err := session.Computer.StartApp("notepad.exe", "", "")

		assert.NoError(t, err, "StartApp should not return error")
		assert.NotNil(t, result, "Should return result")
		assert.NotEmpty(t, result.Processes, "Should return started processes")

		if len(result.Processes) > 0 {
			process := result.Processes[0]
			t.Logf("Started process: %s (PID: %d)", process.PName, process.PID)
			assert.Equal(t, "notepad.exe", process.PName)
			assert.Greater(t, process.PID, 0)
		}
	})

	t.Run("GetInstalledApps", func(t *testing.T) {
		t.Log("Testing GetInstalledApps...")
		result, err := session.Computer.GetInstalledApps(true, false, true)

		if err != nil {
			t.Logf("GetInstalledApps failed: %v", err)
			// Don't fail the test if it's just not supported in the environment or returns empty
		} else {
			assert.NotNil(t, result.Apps)
			t.Logf("Found %d installed apps", len(result.Apps))
			if len(result.Apps) > 0 {
				t.Logf("First app: %s (%s)", result.Apps[0].Name, result.Apps[0].StartCmd)
			}
		}
	})

	// Wait a bit for app to be fully running
	time.Sleep(2 * time.Second)

	t.Run("ListVisibleApps", func(t *testing.T) {
		t.Log("Testing ListVisibleApps with polling...")

		var foundNotepad bool
		// Poll for up to 10 seconds (5 attempts * 2 seconds)
		for i := 0; i < 5; i++ {
			result, err := session.Computer.ListVisibleApps()

			if err != nil {
				t.Logf("ListVisibleApps returned error: %v (attempt %d)", err, i+1)
			} else {
				assert.NotNil(t, result.Processes)

				// Log only if verbose or debugging
				// t.Logf("Found %d visible apps", len(result.Processes))

				foundNotepad = false
				for _, p := range result.Processes {
					if p.PName == "notepad.exe" {
						foundNotepad = true
						break
					}
				}

				if foundNotepad {
					t.Log("Confirmed notepad.exe is in visible apps list")
					break
				}
			}

			t.Logf("notepad.exe not yet visible, retrying... (attempt %d)", i+1)
			time.Sleep(2 * time.Second)
		}

		assert.True(t, foundNotepad, "notepad.exe should be in visible apps list after starting. Check if the app started correctly or if it takes too long to appear.")
	})

	t.Run("StopApp", func(t *testing.T) {
		t.Log("Testing StopAppByPName (notepad.exe)...")
		result := session.Computer.StopAppByPName("notepad.exe")

		if result.ErrorMessage != "" {
			t.Logf("StopAppByPName failed: %s", result.ErrorMessage)
			assert.Fail(t, "StopAppByPName failed")
		} else {
			assert.True(t, result.Success, "StopAppByPName should succeed")
			t.Log("Successfully stopped notepad.exe")
		}
	})

	t.Run("AppLifecycle", func(t *testing.T) {
		t.Log("Testing App Lifecycle (Find -> Start -> Verify -> Stop -> Verify)...")

		// 1. Get Installed Apps
		installedApps, err := session.Computer.GetInstalledApps(true, false, true)
		startCmd := "notepad.exe"

		if err == nil && len(installedApps.Apps) > 0 {
			for _, app := range installedApps.Apps {
				if app.Name == "Notepad" || app.StartCmd == "notepad.exe" {
					startCmd = app.StartCmd
					t.Logf("Found target app in installed list: %s (%s)", app.Name, app.StartCmd)
					break
				}
			}
		} else {
			t.Log("Warning: Could not get installed apps or list empty, using default 'notepad.exe'")
		}

		// 2. Start App
		t.Logf("Starting app with command: %s", startCmd)
		startResult, err := session.Computer.StartApp(startCmd, "", "")
		assert.NoError(t, err, "StartApp should succeed")
		require.NotNil(t, startResult, "StartApp should return result")
		require.NotEmpty(t, startResult.Processes, "StartApp should return processes")

		pid := startResult.Processes[0].PID
		t.Logf("Started app with PID: %d", pid)

		// 3. Verify with ListVisibleApps
		t.Log("Verifying app visibility (polling)...")

		foundInVisible := false
		for i := 0; i < 5; i++ {
			visibleApps, err := session.Computer.ListVisibleApps()
			if err != nil {
				t.Logf("ListVisibleApps error: %v", err)
			} else {
				for _, p := range visibleApps.Processes {
					if p.PID == pid {
						foundInVisible = true
						break
					}
				}
			}

			if foundInVisible {
				t.Log("App found in visible list")
				break
			}
			t.Logf("App PID %d not visible yet, waiting... (attempt %d)", pid, i+1)
			time.Sleep(2 * time.Second)
		}

		// Note: Sometimes apps might not be immediately "visible" depending on how OS reports it,
		// but for notepad it usually works. We'll log warning if not found but assert strictly for now.
		assert.True(t, foundInVisible, "Started app PID should be in visible apps list")

		// 4. Stop App by PID
		t.Logf("Stopping app with PID: %d", pid)
		stopResult := session.Computer.StopAppByPID(pid)
		assert.True(t, stopResult.Success, "StopAppByPID should succeed")

		// 5. Verify it's gone
		time.Sleep(2 * time.Second)
		visibleAppsAfter, err := session.Computer.ListVisibleApps()

		foundAfterStop := false
		if err == nil {
			for _, p := range visibleAppsAfter.Processes {
				if p.PID == pid {
					foundAfterStop = true
					break
				}
			}
		}
		assert.False(t, foundAfterStop, "App PID should NOT be in visible apps list after stopping")
	})
}
