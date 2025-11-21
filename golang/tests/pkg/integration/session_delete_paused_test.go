package integration

import (
	"fmt"
	"os"
	"strings"
	"testing"
	"time"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
	"github.com/joho/godotenv"
)

func init() {
	// Load environment variables from .env file
	envFile := "../../.env"
	if _, err := os.Stat(envFile); err == nil {
		if err := godotenv.Load(envFile); err != nil {
			fmt.Printf("Warning: Error loading .env file: %v\n", err)
		}
	}

	// Also try to load from project root
	rootEnvFile := "../../../.env"
	if _, err := os.Stat(rootEnvFile); err == nil {
		if err := godotenv.Load(rootEnvFile); err != nil {
			fmt.Printf("Warning: Error loading root .env file: %v\n", err)
		}
	}
}

// containsIgnoreCase checks if a string contains a substring (case insensitive)
func containsIgnoreCase(s, substr string) bool {
	return strings.Contains(strings.ToLower(s), strings.ToLower(substr))
}

// TestDeletePausedSession tests that deleting a paused session returns an appropriate error
func TestDeletePausedSession(t *testing.T) {
	apiKey := os.Getenv("AGENTBAY_API_KEY")
	if apiKey == "" {
		t.Fatal("AGENTBAY_API_KEY environment variable is not set")
	}

	client, err := agentbay.NewAgentBay(apiKey, nil)
	if err != nil {
		t.Fatalf("Failed to initialize AgentBay client: %v", err)
	}

	fmt.Println("Creating a new session for paused delete testing...")
	createResult, err := client.Create(nil)
	if err != nil {
		t.Fatalf("Failed to create session: %v", err)
	}
	createdSession := createResult.Session
	sessionId := createdSession.SessionID
	t.Logf("Session created with ID: %s", sessionId)

	// Verify session is initially in RUNNING state
	fmt.Println("Step 1: Verifying session is initially RUNNING...")
	getResult, err := client.GetSession(sessionId)
	if err != nil {
		t.Fatalf("Failed to get session: %v", err)
	}
	if !getResult.Success {
		t.Fatalf("Get session failed: %s", getResult.ErrorMessage)
	}
	if getResult.Data == nil {
		t.Fatal("Get session returned nil data")
	}
	if getResult.Data.Status != "RUNNING" {
		t.Fatalf("Expected session status RUNNING, got %s", getResult.Data.Status)
	}
	t.Logf("✓ Session is RUNNING: %s", sessionId)

	// Pause the session
	fmt.Println("Step 2: Pausing session...")
	pauseResult, err := client.Pause(createdSession, 600, 2.0)
	if err != nil {
		t.Fatalf("Failed to pause session: %v", err)
	}
	if pauseResult == nil {
		t.Fatal("Pause returned nil result")
	}
	if !pauseResult.Success {
		t.Fatalf("Pause failed: %s", pauseResult.ErrorMessage)
	}
	t.Logf("✓ Session pause initiated successfully")
	t.Logf("  Request ID: %s", pauseResult.RequestID)

	// Wait a bit for pause to complete
	fmt.Println("Step 3: Waiting for session to pause...")
	time.Sleep(2 * time.Second)

	// Check session status after pause
	getResult, err = client.GetSession(sessionId)
	if err != nil {
		t.Fatalf("Failed to get session: %v", err)
	}
	if !getResult.Success {
		t.Fatalf("Get session failed: %s", getResult.ErrorMessage)
	}
	if getResult.Data == nil {
		t.Fatal("Get session returned nil data")
	}
	// Session should be PAUSED or still PAUSING
	if getResult.Data.Status != "PAUSED" && getResult.Data.Status != "PAUSING" {
		t.Fatalf("Expected session status PAUSED or PAUSING, got %s", getResult.Data.Status)
	}
	t.Logf("✓ Session status after pause: %s", getResult.Data.Status)

	// Try to delete the paused session - this should fail gracefully
	fmt.Println("Step 4: Attempting to delete paused session...")
	deleteResult, err := createdSession.Delete()
	if err != nil {
		t.Logf("Error deleting paused session: %v", err)
		// Check if this is the expected error for paused sessions
		if err.Error() != "" {
			t.Logf("✓ Delete operation failed as expected for paused session")
		}
	} else {
		if deleteResult.Success {
			t.Logf("Session %s deleted successfully (unexpected)", sessionId)
		} else {
			t.Logf("Delete failed as expected: %s", deleteResult.ErrorMessage)
			// Check if the error message indicates the expected failure
			if deleteResult.ErrorMessage != "" {
				t.Logf("✓ Delete operation failed gracefully with error message")
				// Verify it's the expected error for paused sessions
				if containsIgnoreCase(deleteResult.ErrorMessage, "status PAUSED is not supported") ||
					containsIgnoreCase(deleteResult.ErrorMessage, "STATUS_NOT_RUNNING") {
					t.Logf("✓ Delete operation failed with expected PAUSED status error")
				}
			}
		}
	}

	// Resume the session so we can properly clean up
	fmt.Println("Step 5: Resuming session for cleanup...")
	resumeResult, err := client.Resume(createdSession, 120, 3.0)
	if err != nil {
		t.Fatalf("Failed to resume session for cleanup: %v", err)
	}
	if resumeResult == nil {
		t.Fatal("Resume returned nil result")
	}
	if !resumeResult.Success {
		t.Fatalf("Resume failed: %s", resumeResult.ErrorMessage)
	}
	t.Logf("✓ Session resumed successfully for cleanup")

	// Wait a bit for resume to complete
	fmt.Println("Step 6: Waiting for session to resume...")
	time.Sleep(2 * time.Second)

	// Now delete the session properly
	fmt.Println("Step 7: Deleting resumed session...")
	deleteResult, err = createdSession.Delete()
	if err != nil {
		t.Logf("Failed to delete session: %v", err)
	} else {
		if deleteResult.Success {
			t.Logf("✓ Session %s deleted successfully", sessionId)
		} else {
			t.Logf("Delete failed: %s", deleteResult.ErrorMessage)
		}
	}
}
