package integration_test

import (
	"fmt"
	"strings"
	"testing"
	"time"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
	"github.com/aliyun/wuying-agentbay-sdk/golang/tests/pkg/agentbay/testutil"
)

// TestVpcSessionBasicTools tests the creation of a VPC-based session and basic tool functionality:
// 1. Create a session with IsVpc=true
// 2. Test Command tool functionality (without actually executing)
// 3. Test Code tool functionality (without actually executing)
// 4. Test FileSystem tool functionality (without actually executing)
// 5. Clean up the session
//
// Note: This test is designed to verify that VPC sessions can be created and tools are available,
// but does not actually execute commands/code/filesystem operations as they require specific VPC setup.
// The actual execution should be tested in the appropriate VPC environment.
func TestVpcSessionBasicTools(t *testing.T) {
	// Initialize AgentBay client
	apiKey := testutil.GetTestAPIKey(t)
	t.Logf("Using API key: %s", apiKey)

	agentBay, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		t.Fatalf("Error initializing AgentBay client: %v", err)
	}
	t.Logf("AgentBay client initialized successfully with region: %s", agentBay.RegionId)

	// Step 1: Create a VPC-based session
	t.Log("Step 1: Creating VPC-based session...")
	params := agentbay.NewCreateSessionParams().
		WithImageId("linux_latest").
		WithIsVpc(true).
		WithLabels(map[string]string{
			"test-type": "vpc-integration",
			"purpose":   "vpc-session-testing",
		})

	t.Logf("Session params: ImageId=%s, IsVpc=%v, Labels=%v",
		params.ImageId, params.IsVpc, params.Labels)

	sessionResult, err := agentBay.Create(params)
	if err != nil {
		t.Fatalf("Error creating VPC session: %v", err)
	}
	session := sessionResult.Session
	t.Logf("VPC session created successfully with ID: %s (RequestID: %s)",
		session.SessionID, sessionResult.RequestID)

	// Ensure cleanup of the session at the end of the test
	defer func() {
		t.Log("Cleaning up: Deleting the VPC session...")
		deleteResult, err := agentBay.Delete(session)
		if err != nil {
			t.Logf("Warning: Error deleting VPC session: %v", err)
		} else {
			t.Logf("VPC session successfully deleted (RequestID: %s)",
				deleteResult.RequestID)
		}
	}()

	// Verify session properties
	if session.SessionID == "" {
		t.Fatalf("Session ID is empty")
	}
	t.Logf("Session properties verified: ID=%s", session.SessionID)

	// Step 2: Test Command tool availability (without execution)
	t.Log("Step 2: Testing Command tool availability...")
	if session.Command != nil {
		t.Log("✓ Command tool is available in VPC session")

		// Note: We don't execute commands here as they require specific VPC setup
		// The actual command execution should be tested in the appropriate VPC environment
		t.Log("Note: Command execution skipped - requires specific VPC environment setup")
	} else {
		t.Log("⚠ Command tool is not available in VPC session")
	}

	// Step 3: Test Code tool availability (without execution)
	t.Log("Step 3: Testing Code tool availability...")
	if session.Code != nil {
		t.Log("✓ Code tool is available in VPC session")

		// Note: We don't execute code here as it requires specific VPC setup
		// The actual code execution should be tested in the appropriate VPC environment
		t.Log("Note: Code execution skipped - requires specific VPC environment setup")
	} else {
		t.Log("⚠ Code tool is not available in VPC session")
	}

	// Step 4: Test FileSystem tool availability (without execution)
	t.Log("Step 4: Testing FileSystem tool availability...")
	if session.FileSystem != nil {
		t.Log("✓ FileSystem tool is available in VPC session")

		// Note: We don't perform filesystem operations here as they require specific VPC setup
		// The actual filesystem operations should be tested in the appropriate VPC environment
		t.Log("Note: FileSystem operations skipped - requires specific VPC environment setup")
	} else {
		t.Log("⚠ FileSystem tool is not available in VPC session")
	}

	// Step 5: Verify session is still active
	t.Log("Step 5: Verifying session is still active...")
	listResult, err := agentBay.List()
	if err != nil {
		t.Logf("Warning: Error listing sessions: %v", err)
	} else {
		sessionFound := false
		for _, s := range listResult.Sessions {
			if s.SessionID == session.SessionID {
				sessionFound = true
				t.Logf("✓ VPC session is still active in session list")
				break
			}
		}
		if !sessionFound {
			t.Log("⚠ VPC session not found in session list")
		}
	}

	t.Log("VPC session integration test completed successfully")
}

// TestVpcSessionWithContextSync tests VPC session creation with context synchronization
func TestVpcSessionWithContextSync(t *testing.T) {
	// Initialize AgentBay client
	apiKey := testutil.GetTestAPIKey(t)
	t.Logf("Using API key: %s", apiKey)

	agentBay, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		t.Fatalf("Error initializing AgentBay client: %v", err)
	}
	t.Logf("AgentBay client initialized successfully with region: %s", agentBay.RegionId)

	// Step 1: Create a context for testing
	contextName := fmt.Sprintf("test-vpc-context-%d", time.Now().Unix())
	t.Logf("Creating context for VPC session test: %s", contextName)

	createResult, err := agentBay.Context.Create(contextName)
	if err != nil {
		t.Fatalf("Error creating context: %v", err)
	}

	// Get the created context
	getResult, err := agentBay.Context.Get(contextName, false)
	if err != nil {
		t.Fatalf("Error getting created context: %v", err)
	}

	context := contextFromResult(getResult)
	t.Logf("Context created successfully - ID: %s, Name: %s, State: %s (RequestID: %s)",
		context.ID, context.Name, context.State, createResult.RequestID)

	// Ensure cleanup of the context at the end of the test
	defer func() {
		t.Log("Cleaning up: Deleting the context...")
		deleteResult, err := agentBay.Context.Delete(context)
		if err != nil {
			t.Logf("Warning: Error deleting context: %v", err)
		} else {
			t.Logf("Context %s deleted successfully (RequestID: %s)",
				context.ID, deleteResult.RequestID)
		}
	}()

	// Step 2: Create a VPC session with context sync
	t.Log("Step 2: Creating VPC session with context sync...")
	params := agentbay.NewCreateSessionParams().
		WithImageId("linux_latest").
		WithIsVpc(true).
		WithLabels(map[string]string{
			"test-type": "vpc-context-sync",
			"purpose":   "vpc-context-sync-testing",
		}).
		AddContextSync(context.ID, "/workspace", agentbay.NewSyncPolicy())

	t.Logf("VPC session params: ImageId=%s, IsVpc=%v, ContextSync count=%d",
		params.ImageId, params.IsVpc, len(params.ContextSync))

	sessionResult, err := agentBay.Create(params)
	if err != nil {
		t.Fatalf("Error creating VPC session with context sync: %v", err)
	}
	session := sessionResult.Session
	t.Logf("VPC session with context sync created successfully with ID: %s (RequestID: %s)",
		session.SessionID, sessionResult.RequestID)

	// Ensure cleanup of the session at the end of the test
	defer func() {
		t.Log("Cleaning up: Deleting the VPC session...")
		deleteResult, err := agentBay.Delete(session)
		if err != nil {
			t.Logf("Warning: Error deleting VPC session: %v", err)
		} else {
			t.Logf("VPC session successfully deleted (RequestID: %s)",
				deleteResult.RequestID)
		}
	}()

	// Step 3: Verify context is in use
	t.Log("Step 3: Verifying context is in use...")
	getContextResult, err := agentBay.Context.Get(contextName, false)
	if err != nil {
		t.Logf("Warning: Error getting context after session creation: %v", err)
	} else {
		updatedContext := contextFromResult(getContextResult)
		t.Logf("Context state after VPC session creation: %s", updatedContext.State)
		if strings.Contains(strings.ToLower(updatedContext.State), "in-use") {
			t.Log("✓ Context is properly marked as in-use by VPC session")
		} else {
			t.Logf("⚠ Context state is not 'in-use': %s", updatedContext.State)
		}
	}

	// Step 4: Test tool availability in VPC session with context sync
	t.Log("Step 4: Testing tool availability in VPC session with context sync...")

	if session.Command != nil {
		t.Log("✓ Command tool is available in VPC session with context sync")
	} else {
		t.Log("⚠ Command tool is not available in VPC session with context sync")
	}

	if session.Code != nil {
		t.Log("✓ Code tool is available in VPC session with context sync")
	} else {
		t.Log("⚠ Code tool is not available in VPC session with context sync")
	}

	if session.FileSystem != nil {
		t.Log("✓ FileSystem tool is available in VPC session with context sync")
	} else {
		t.Log("⚠ FileSystem tool is not available in VPC session with context sync")
	}

	t.Log("VPC session with context sync integration test completed successfully")
}
