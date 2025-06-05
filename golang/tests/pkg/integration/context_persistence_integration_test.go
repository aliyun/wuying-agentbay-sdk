package integration_test

import (
	"fmt"
	"os"
	"strings"
	"testing"
	"time"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

// Helper function to check if a string contains "tool not found"
func containsToolNotFound(s string) bool {
	return strings.Contains(strings.ToLower(s), "tool not found")
}

// Get API key for testing
func getTestAPIKey(t *testing.T) string {
	apiKey := os.Getenv("AGENTBAY_API_KEY")
	if apiKey == "" {
		apiKey = "akm-xxx" // Replace with your test API key
		t.Logf("Warning: Using default API key. Set AGENTBAY_API_KEY environment variable for testing.")
	}
	return apiKey
}

// TestContextPersistence tests the persistence of files across sessions with the same context ID
// and the isolation of files between different contexts.
func TestContextPersistence(t *testing.T) {
	// Initialize AgentBay client
	apiKey := getTestAPIKey(t)
	t.Logf("Using API key: %s", apiKey)

	agentBay, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		t.Fatalf("Error initializing AgentBay client: %v", err)
	}
	t.Logf("AgentBay client initialized successfully with region: %s", agentBay.RegionId)

	// Step 1: Create a new context
	contextName := fmt.Sprintf("test-context-%d", time.Now().Unix())
	t.Logf("Creating new context with name: %s", contextName)

	// List existing contexts before creation
	existingContexts, err := agentBay.Context.List()
	if err != nil {
		t.Logf("Warning: Failed to list existing contexts: %v", err)
	} else {
		t.Logf("Found %d existing contexts before creation", len(existingContexts))
		for i, ctx := range existingContexts {
			t.Logf("Existing context %d: ID=%s, Name=%s, State=%s, OSType=%s",
				i+1, ctx.ID, ctx.Name, ctx.State, ctx.OSType)
		}
	}

	context, err := agentBay.Context.Create(contextName)
	if err != nil {
		t.Fatalf("Error creating context: %v", err)
	}
	t.Logf("Context created successfully - ID: %s, Name: %s, State: %s, OSType: %s",
		context.ID, context.Name, context.State, context.OSType)

	// Create a unique filename for testing in the home directory
	testFilePath := fmt.Sprintf("~/test-file-%d.txt", time.Now().Unix())
	testFileContent := "This is a test file for context persistence"

	// Step 2: Create a session with the context ID
	t.Log("Creating first session with context ID...")
	params := agentbay.NewCreateSessionParams().WithContextID(context.ID)
	t.Logf("Session params: ContextID=%s", params.ContextID)

	// List active sessions before creation
	activeSessions, err := agentBay.List()
	if err != nil {
		t.Logf("Warning: Failed to list active sessions: %v", err)
	} else {
		t.Logf("Found %d active sessions before creation", len(activeSessions))
		for i, sess := range activeSessions {
			t.Logf("Active session %d: ID=%s", i+1, sess.SessionID)
		}
	}

	session1, err := agentBay.Create(params)
	if err != nil {
		t.Fatalf("Error creating session with context ID: %v", err)
	}
	t.Logf("Session created with ID: %s, AgentBay client region: %s",
		session1.SessionID, session1.AgentBay.RegionId)

	// Step 3: Use Execute command to create a file
	t.Logf("Creating test file at %s...", testFilePath)
	createFileCmd := fmt.Sprintf("echo '%s' > %s", testFileContent, testFilePath)
	t.Logf("Executing command: %s", createFileCmd)

	// First check if the file already exists (it shouldn't)
	checkCmd := fmt.Sprintf("ls -la %s 2>&1 || echo 'File does not exist'", testFilePath)
	checkOutput, err := session1.Command.ExecuteCommand(checkCmd)
	if err != nil {
		t.Logf("Warning: Pre-check command failed: %v", err)
	}
	t.Logf("Pre-check output: %s", checkOutput)

	// Now create the file
	output, err := session1.Command.ExecuteCommand(createFileCmd)
	if err != nil {
		t.Logf("Warning: Command execution failed: %v", err)
		if containsToolNotFound(output) {
			t.Skip("Skipping test as execute_command tool is not available")
		}
	}
	t.Logf("File creation output: %s", output)

	// Verify the file was created
	verifyCmd := fmt.Sprintf("cat %s", testFilePath)
	t.Logf("Verifying file with command: %s", verifyCmd)
	output, err = session1.Command.ExecuteCommand(verifyCmd)
	if err != nil {
		t.Fatalf("Error verifying file creation: %v", err)
	}

	// Also check file attributes
	lsCmd := fmt.Sprintf("ls -la %s", testFilePath)
	lsOutput, lsErr := session1.Command.ExecuteCommand(lsCmd)
	if lsErr != nil {
		t.Logf("Warning: Could not get file attributes: %v", lsErr)
	} else {
		t.Logf("File attributes: %s", lsOutput)
	}

	if !strings.Contains(output, testFileContent) {
		t.Fatalf("File content verification failed. Expected to contain '%s', got: '%s'", testFileContent, output)
	}
	t.Logf("File created and verified successfully with content: %s", output)

	// Step 4: Release the session
	t.Log("Releasing first session...")
	err = session1.Delete()
	if err != nil {
		t.Fatalf("Error releasing session: %v", err)
	}

	// Add a 20-second delay to ensure the session is fully released
	t.Log("Waiting for 20 seconds before creating the second session...")
	time.Sleep(20 * time.Second)

	// Step 5: Create another session with the same context ID
	t.Log("Creating second session with the same context ID...")
	params = agentbay.NewCreateSessionParams().WithContextID(context.ID)
	t.Logf("Second session params: ContextID=%s", params.ContextID)

	// List active sessions before creating second session
	activeSessions, err = agentBay.List()
	if err != nil {
		t.Logf("Warning: Failed to list active sessions before second session creation: %v", err)
	} else {
		t.Logf("Found %d active sessions before second session creation", len(activeSessions))
		for i, sess := range activeSessions {
			t.Logf("Active session %d: ID=%s", i+1, sess.SessionID)
		}
	}

	// Check context state before creating second session
	contextBefore, err := agentBay.Context.Get(contextName, false)
	if err != nil {
		t.Logf("Warning: Failed to get context before second session creation: %v", err)
	} else if contextBefore != nil {
		t.Logf("Context state before second session: ID=%s, Name=%s, State=%s, OSType=%s",
			contextBefore.ID, contextBefore.Name, contextBefore.State, contextBefore.OSType)
	}

	session2, err := agentBay.Create(params)
	if err != nil {
		t.Logf("Error creating second session with context ID: %v", err)
		t.Logf("This may be due to resource limits or the context being in use.")

		// Try to clean up the context before failing
		t.Log("Attempting to clean up context before failing...")
		cleanupErr := agentBay.Context.Delete(context)
		if cleanupErr != nil {
			t.Logf("Warning: Failed to clean up context: %v", cleanupErr)
		} else {
			t.Logf("Successfully cleaned up context %s", context.ID)
		}

		t.Fatalf("Failed to create second session with context ID: %v", err)
	}
	t.Logf("Second session created with ID: %s, AgentBay client region: %s",
		session2.SessionID, session2.AgentBay.RegionId)

	// Step 6: Check if the file still exists (expected: yes)
	t.Logf("Checking if file %s still exists in the second session...", testFilePath)
	output, err = session2.Command.ExecuteCommand(verifyCmd)
	if err != nil {
		t.Fatalf("Error checking file existence in second session: %v", err)
	}
	if !strings.Contains(output, testFileContent) {
		t.Fatalf("File persistence test failed. Expected file to exist with content '%s', got: '%s'", testFileContent, output)
	}
	t.Logf("File persistence verified: file exists in the second session")

	// Step 7: Release the second session
	t.Log("Releasing second session...")
	err = session2.Delete()
	if err != nil {
		t.Fatalf("Error releasing second session: %v", err)
	}

	// Step 8: Create a session without a context ID
	t.Log("Creating third session without context ID...")

	// List active sessions before creating third session
	activeSessions, err = agentBay.List()
	if err != nil {
		t.Logf("Warning: Failed to list active sessions before third session creation: %v", err)
	} else {
		t.Logf("Found %d active sessions before third session creation", len(activeSessions))
		for i, sess := range activeSessions {
			t.Logf("Active session %d: ID=%s", i+1, sess.SessionID)
		}
	}

	// Create session with no context ID
	t.Logf("Creating session with no context ID (should be a fresh environment)")
	session3, err := agentBay.Create(nil)
	if err != nil {
		t.Logf("Error creating session without context ID: %v", err)
		t.Logf("This may be due to resource limits.")

		// Try to clean up the context before failing
		t.Log("Attempting to clean up context before failing...")
		cleanupErr := agentBay.Context.Delete(context)
		if cleanupErr != nil {
			t.Logf("Warning: Failed to clean up context: %v", cleanupErr)
		} else {
			t.Logf("Successfully cleaned up context %s", context.ID)
		}

		t.Fatalf("Failed to create third session without context ID: %v", err)
	}
	t.Logf("Third session created with ID: %s, AgentBay client region: %s",
		session3.SessionID, session3.AgentBay.RegionId)

	// Step 9: Check if the file exists (expected: no)
	t.Logf("Checking if file %s exists in the third session (should not exist)...", testFilePath)

	// First check with ls command
	lsCmd = fmt.Sprintf("ls -la %s 2>&1 || echo 'File does not exist'", testFilePath)
	lsOutput, lsErr = session3.Command.ExecuteCommand(lsCmd)
	if lsErr != nil {
		t.Logf("Warning: ls command failed in third session: %v", lsErr)
	} else {
		t.Logf("ls command output in third session: %s", lsOutput)
	}

	// Then try to read the file content
	t.Logf("Attempting to read file content with command: %s", verifyCmd)
	output, err = session3.Command.ExecuteCommand(verifyCmd)
	if err != nil {
		// Error is expected as the file should not exist
		t.Logf("Expected error when checking non-existent file: %v", err)
	} else {
		// If no error, check if the output indicates the file doesn't exist
		if strings.Contains(output, "No such file") ||
			strings.Contains(output, "not found") ||
			strings.Contains(output, "File does not exist") ||
			strings.TrimSpace(output) == "" {
			t.Logf("File isolation verified: file does not exist in the third session")
		} else if strings.Contains(output, testFileContent) {
			t.Logf("UNEXPECTED: File exists in the third session with content: '%s'", output)
			t.Fatalf("File isolation test failed. File unexpectedly exists in the third session with content: '%s'", output)
		} else {
			t.Logf("Unexpected output when checking file: '%s'", output)
		}
	}

	// Step 10: Release the third session and delete the context
	t.Log("Releasing third session...")

	// List active sessions before cleanup
	activeSessions, err = agentBay.List()
	if err != nil {
		t.Logf("Warning: Failed to list active sessions before cleanup: %v", err)
	} else {
		t.Logf("Found %d active sessions before cleanup", len(activeSessions))
		for i, sess := range activeSessions {
			t.Logf("Active session %d: ID=%s", i+1, sess.SessionID)
		}
	}

	// Release the third session
	err = session3.Delete()
	if err != nil {
		t.Logf("Error releasing third session: %v", err)
		t.Logf("Continuing with context deletion anyway...")
	} else {
		t.Logf("Third session released successfully")
	}

	// List contexts before deletion
	existingContexts, err = agentBay.Context.List()
	if err != nil {
		t.Logf("Warning: Failed to list contexts before deletion: %v", err)
	} else {
		t.Logf("Found %d contexts before deletion", len(existingContexts))
		for i, ctx := range existingContexts {
			t.Logf("Context %d: ID=%s, Name=%s, State=%s, OSType=%s",
				i+1, ctx.ID, ctx.Name, ctx.State, ctx.OSType)
		}
	}

	t.Log("Deleting context...")
	err = agentBay.Context.Delete(context)
	if err != nil {
		t.Fatalf("Error deleting context: %v", err)
	}
	t.Logf("Context %s deleted successfully", context.ID)

	// Verify context deletion
	existingContexts, err = agentBay.Context.List()
	if err != nil {
		t.Logf("Warning: Failed to list contexts after deletion: %v", err)
	} else {
		t.Logf("Found %d contexts after deletion", len(existingContexts))

		// Check if our context is still in the list
		contextFound := false
		for _, ctx := range existingContexts {
			if ctx.ID == context.ID {
				contextFound = true
				t.Logf("WARNING: Context %s still exists after deletion", context.ID)
				break
			}
		}

		if !contextFound {
			t.Logf("Context deletion verified: context %s no longer exists", context.ID)
		}
	}

	t.Logf("Test completed successfully")
}
