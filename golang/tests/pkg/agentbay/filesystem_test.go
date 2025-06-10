package agentbay_test

import (
	"fmt"
	"strings"
	"testing"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

func TestFileSystem_ReadFile(t *testing.T) {
	// Initialize AgentBay client
	apiKey := getTestAPIKey(t)
	agentBay, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		t.Fatalf("Error initializing AgentBay client: %v", err)
	}

	// Create a session
	fmt.Println("Creating a new session for filesystem testing...")
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

	// Test FileSystem read operations
	if session.FileSystem != nil {
		fmt.Println("Reading file...")
		content, err := session.FileSystem.ReadFile("/etc/hosts")
		t.Logf("ReadFile result: content='%s', err=%v", content, err)
		if err != nil {
			t.Logf("Note: File read failed: %v", err)
		} else {
			t.Logf("File read successful, content length: %d bytes", len(content))
			// Check if response contains "tool not found"
			if containsToolNotFound(content) {
				t.Errorf("FileSystem.ReadFile returned 'tool not found'")
			}
		}
	} else {
		t.Logf("Note: FileSystem interface is nil, skipping file test")
	}
}

func TestFileSystem_WriteFile(t *testing.T) {
	// Initialize AgentBay client
	apiKey := getTestAPIKey(t)
	agentBay, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		t.Fatalf("Error initializing AgentBay client: %v", err)
	}

	// Create a session
	fmt.Println("Creating a new session for filesystem write testing...")
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

	// Test FileSystem write operations
	if session.FileSystem != nil && session.Command != nil {
		// Test case 1: Write file with overwrite mode
		testFilePath := "/tmp/test_write_file.txt"
		testContent := "Hello, this is a test content for overwrite mode."

		fmt.Println("Writing file with overwrite mode...")
		success, err := session.FileSystem.WriteFile(testFilePath, testContent, "overwrite")
		t.Logf("WriteFile (overwrite) result: success=%v, err=%v", success, err)
		if err != nil {
			t.Errorf("FileSystem.WriteFile (overwrite) failed: %v", err)
		} else if !success {
			t.Errorf("FileSystem.WriteFile (overwrite) returned false")
		}

		// Verify the content was written correctly
		fmt.Println("Reading file to verify overwrite content...")
		readContent, err := session.FileSystem.ReadFile(testFilePath)
		if err != nil {
			t.Errorf("Error reading file after write (overwrite): %v", err)
		} else {
			// Trim any trailing newlines for comparison
			readContent = strings.TrimSpace(readContent)
			if readContent != testContent {
				t.Errorf("File content mismatch after overwrite. Expected: %s, Got: %s", testContent, readContent)
			} else {
				t.Log("File content verified after overwrite")
			}
		}

		// Test case 2: Write file with append mode
		appendContent := "\nThis is additional content for append mode."
		fmt.Println("Writing file with append mode...")
		success, err = session.FileSystem.WriteFile(testFilePath, appendContent, "append")
		t.Logf("WriteFile (append) result: success=%v, err=%v", success, err)
		if err != nil {
			t.Errorf("FileSystem.WriteFile (append) failed: %v", err)
		} else if !success {
			t.Errorf("FileSystem.WriteFile (append) returned false")
		}

		// Verify the content was appended correctly
		fmt.Println("Reading file to verify appended content...")
		readContent, err = session.FileSystem.ReadFile(testFilePath)
		if err != nil {
			t.Errorf("Error reading file after write (append): %v", err)
		} else {
			// Trim any trailing newlines for comparison
			readContent = strings.TrimSpace(readContent)
			expectedContent := testContent + appendContent
			if readContent != expectedContent {
				t.Errorf("File content mismatch after append. Expected: %s, Got: %s", expectedContent, readContent)
			} else {
				t.Log("File content verified after append")
			}
		}

		// Test case 3: Write file with empty mode (should default to overwrite)
		defaultContent := "This content tests the default mode (should be overwrite)."
		fmt.Println("Writing file with empty mode (should default to overwrite)...")
		success, err = session.FileSystem.WriteFile(testFilePath, defaultContent, "")
		t.Logf("WriteFile (empty mode) result: success=%v, err=%v", success, err)
		if err != nil {
			t.Errorf("FileSystem.WriteFile (empty mode) failed: %v", err)
		} else if !success {
			t.Errorf("FileSystem.WriteFile (empty mode) returned false")
		}

		// Verify the content was overwritten correctly
		fmt.Println("Reading file to verify default mode content...")
		readContent, err = session.FileSystem.ReadFile(testFilePath)
		if err != nil {
			t.Errorf("Error reading file after write (empty mode): %v", err)
		} else {
			// Trim any trailing newlines for comparison
			readContent = strings.TrimSpace(readContent)
			if readContent != defaultContent {
				t.Errorf("File content mismatch after empty mode write. Expected: %s, Got: %s", defaultContent, readContent)
			} else {
				t.Log("File content verified after empty mode write (correctly defaulted to overwrite)")
			}
		}

		// Clean up the test file using ExecuteCommand
		fmt.Println("Cleaning up test file...")
		_, err = session.Command.ExecuteCommand("rm " + testFilePath)
		if err != nil {
			t.Logf("Warning: Error cleaning up test file: %v", err)
		}
	} else {
		if session.FileSystem == nil {
			t.Logf("Note: FileSystem interface is nil, skipping file write test")
		}
		if session.Command == nil {
			t.Logf("Note: Command interface is nil, skipping file write test")
		}
	}
}
