package agentbay_test

import (
	"fmt"
	"testing"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

func TestAdb_Shell(t *testing.T) {
	// Initialize AgentBay client
	apiKey := getTestAPIKey(t)
	agentBay, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		t.Fatalf("Error initializing AgentBay client: %v", err)
	}

	// Create a session
	fmt.Println("Creating a new session for ADB testing...")
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

	// Test Adb shell command execution
	if session.Adb != nil {
		fmt.Println("Executing ADB shell command...")
		response, err := session.Adb.Shell("ls /sdcard")
		if err != nil {
			t.Logf("Note: ADB shell execution failed: %v", err)
		} else {
			t.Logf("ADB shell execution result: %s", response)
			// Check if response contains "tool not found"
			if containsToolNotFound(response) {
				t.Errorf("Adb.Shell returned 'tool not found'")
			}
		}

		// Add more ADB-related tests
		fmt.Println("Executing ADB shell command to check device properties...")
		propResponse, err := session.Adb.Shell("getprop")
		if err != nil {
			t.Logf("Note: ADB getprop execution failed: %v", err)
		} else {
			t.Logf("ADB getprop execution result length: %d bytes", len(propResponse))
			// Check if response contains "tool not found"
			if containsToolNotFound(propResponse) {
				t.Errorf("Adb.Shell returned 'tool not found'")
			}
		}
	} else {
		t.Logf("Note: Adb interface is nil, skipping ADB test")
	}
}
