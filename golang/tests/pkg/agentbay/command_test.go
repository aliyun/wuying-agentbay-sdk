package agentbay_test

import (
	"fmt"
	"strings"
	"testing"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

func TestCommand_ExecuteCommand(t *testing.T) {
	// Initialize AgentBay client
	apiKey := getTestAPIKey(t)
	agentBay, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		t.Fatalf("Error initializing AgentBay client: %v", err)
	}

	// Create a session
	fmt.Println("Creating a new session for command testing...")
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

	// Test Command execution
	if session.Command != nil {
		// Test with echo command (works on all platforms)
		fmt.Println("Executing echo command...")
		testString := "AgentBay SDK Test"
		echoCmd := fmt.Sprintf("echo '%s'", testString)

		response, err := session.Command.ExecuteCommand(echoCmd)
		if err != nil {
			t.Logf("Note: Echo command failed: %v", err)
		} else {
			t.Logf("Echo command result: %s", response)

			// Check if response contains "tool not found"
			if containsToolNotFound(response) {
				t.Errorf("Command.ExecuteCommand returned 'tool not found'")
			}

			// Verify the response contains the test string
			if !strings.Contains(response, testString) {
				t.Errorf("Echo command verification failed: expected '%s' in response, got '%s'", testString, response)
			} else {
				t.Logf("Echo command verified successfully")
			}
		}
	} else {
		t.Logf("Note: Command interface is nil, skipping command test")
	}
}
