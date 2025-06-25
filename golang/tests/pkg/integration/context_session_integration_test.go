package integration_test

import (
	"fmt"
	"testing"
	"time"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
	"github.com/aliyun/wuying-agentbay-sdk/golang/tests/pkg/agentbay/testutil"
)

// TestContextSessionManagement tests the context and session management functionality:
// 1. Create a context_id
// 2. Use this context_id to create a session (expect success)
// 3. Get the context list and verify that the context_id's status is "in-use"
// 4. Try to create another session with the same context_id (expect failure)
// 5. Release the first session
// 6. Get the context list and verify that the context_id's status is "available"
// 7. Create another session with the same context_id (expect success)
// 8. Clean up by releasing the session and deleting the context
func TestContextSessionManagement(t *testing.T) {
	// Initialize AgentBay client
	apiKey := testutil.GetTestAPIKey(t)
	t.Logf("Using API key: %s", apiKey)

	agentBay, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		t.Fatalf("Error initializing AgentBay client: %v", err)
	}
	t.Logf("AgentBay client initialized successfully with region: %s", agentBay.RegionId)

	// Step 1: Create a new context
	contextName := fmt.Sprintf("test-context-%d", time.Now().Unix())
	t.Logf("Creating new context with name: %s", contextName)

	createResult, err := agentBay.Context.Create(contextName)
	if err != nil {
		t.Fatalf("Error creating context: %v", err)
	}

	// Get the created context to get its full details
	getResult, err := agentBay.Context.Get(contextName, false)
	if err != nil {
		t.Fatalf("Error getting created context: %v", err)
	}

	context := contextFromResult(getResult)
	t.Logf("Context created successfully - ID: %s, Name: %s, State: %s, OSType: %s (RequestID: %s)",
		context.ID, context.Name, context.State, context.OSType, createResult.RequestID)

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

	// Step 2: Create a session with the context ID (expect success)
	t.Log("Step 2: Creating first session with context ID...")
	params := agentbay.NewCreateSessionParams().WithContextID(context.ID)
	t.Logf("Session params: ContextID=%s", params.ContextID)

	sessionResult, err := agentBay.Create(params)
	if err != nil {
		t.Fatalf("Error creating session with context ID: %v", err)
	}
	session1 := sessionResult.Session
	t.Logf("Session created successfully with ID: %s (RequestID: %s)",
		session1.SessionID, sessionResult.RequestID)

	// Ensure cleanup of the session if it's not released during the test
	defer func() {
		// Check if the session still exists before trying to delete it
		listResult, listErr := agentBay.List()
		if listErr != nil {
			t.Logf("Warning: Error listing sessions: %v", listErr)
			return
		}

		sessionExists := false
		for _, s := range listResult.Sessions {
			if s.SessionID == session1.SessionID {
				sessionExists = true
				break
			}
		}

		if sessionExists {
			t.Log("Cleaning up: Deleting the first session...")
			deleteResult, err := agentBay.Delete(session1)
			if err != nil {
				t.Logf("Warning: Error deleting first session: %v", err)
			} else {
				t.Logf("First session successfully deleted (RequestID: %s)",
					deleteResult.RequestID)
			}
		}
	}()

	// Step 3: Get the context directly and verify that its status is "in-use"
	t.Log("Step 3: Checking context status after session creation...")

	// Wait a moment for the system to update the context status
	time.Sleep(2 * time.Second)

	updatedGetResult, err := agentBay.Context.Get(contextName, false)
	if err != nil {
		t.Fatalf("Error getting context: %v", err)
	}
	if updatedGetResult == nil {
		t.Fatalf("Context not found after session creation")
	}

	updatedContext := contextFromResult(updatedGetResult)
	t.Logf("Retrieved context - ID: %s, Name: %s, State: %s (RequestID: %s)",
		updatedContext.ID, updatedContext.Name, updatedContext.State, updatedGetResult.RequestID)

	if updatedContext.State != "in-use" {
		t.Errorf("Expected context state to be 'in-use', got '%s'", updatedContext.State)
	} else {
		t.Logf("Context state is correctly set to 'in-use'")
	}

	// Step 4: Try to create another session with the same context_id (expect failure)
	t.Log("Step 4: Attempting to create a second session with the same context ID...")
	session2Result, err := agentBay.Create(params)
	if err == nil {
		// If somehow it succeeds (which shouldn't happen), make sure to clean it up
		session2 := session2Result.Session
		t.Logf("WARNING: Unexpectedly succeeded in creating second session with ID: %s (RequestID: %s)",
			session2.SessionID, session2Result.RequestID)
		t.Log("Cleaning up the unexpected second session...")
		deleteResult, cleanupErr := agentBay.Delete(session2)
		if cleanupErr != nil {
			t.Logf("Warning: Error cleaning up unexpected second session: %v", cleanupErr)
		} else {
			t.Logf("Unexpected second session deleted (RequestID: %s)", deleteResult.RequestID)
		}
		t.Errorf("Expected error when creating second session with same context ID, but got success")
	} else {
		t.Logf("As expected, failed to create second session with same context ID: %v", err)
	}

	// Step 5: Release the first session
	t.Log("Step 5: Releasing the first session...")
	deleteResult, err := agentBay.Delete(session1)
	if err != nil {
		t.Fatalf("Error releasing first session: %v", err)
	}
	t.Logf("First session released successfully (RequestID: %s)", deleteResult.RequestID)

	// Wait for the system to update the context status
	t.Log("Waiting for context status to update...")
	time.Sleep(3 * time.Second)

	// Step 6: Get the context directly and verify that its status is "available"
	t.Log("Step 6: Checking context status after session release...")

	updatedGetResult, err = agentBay.Context.Get(contextName, false)
	if err != nil {
		t.Fatalf("Error getting context: %v", err)
	}
	if updatedGetResult == nil {
		t.Fatalf("Context not found after session release")
	}

	updatedContext = contextFromResult(updatedGetResult)
	t.Logf("Retrieved context - ID: %s, Name: %s, State: %s (RequestID: %s)",
		updatedContext.ID, updatedContext.Name, updatedContext.State, updatedGetResult.RequestID)

	if updatedContext.State != "available" {
		t.Errorf("Expected context state to be 'available', got '%s'", updatedContext.State)
	} else {
		t.Logf("Context state is correctly set to 'available'")
	}

	// Step 7: Create another session with the same context_id (expect success)
	t.Log("Step 7: Creating a new session with the same context ID...")

	// Add retry mechanism for handling temporary unavailability
	var session3Result *agentbay.SessionResult
	maxRetries := 5
	retryDelay := 5 * time.Second
	var lastErr error

	for i := 0; i < maxRetries; i++ {
		session3Result, err = agentBay.Create(params)
		if err == nil {
			t.Logf("New session created successfully with ID: %s (RequestID: %s)",
				session3Result.Session.SessionID, session3Result.RequestID)
			break
		}

		lastErr = err
		t.Logf("Attempt %d: Failed to create session: %v", i+1, err)

		if i < maxRetries-1 {
			t.Logf("Waiting %s before retrying...", retryDelay)
			time.Sleep(retryDelay)
		}
	}

	if session3Result == nil {
		t.Fatalf("Error creating new session with same context ID after %d attempts: %v", maxRetries, lastErr)
	}

	session3 := session3Result.Session

	// Step 8: Clean up by releasing the session
	t.Log("Step 8: Cleaning up - releasing the third session...")
	deleteResult, err = agentBay.Delete(session3)
	if err != nil {
		t.Fatalf("Error releasing third session: %v", err)
	}
	t.Logf("Third session released successfully (RequestID: %s)", deleteResult.RequestID)

	// Context will be deleted by the defer function at the beginning
	t.Log("Test completed successfully")
}

// Create a context from the context result
func contextFromResult(result *agentbay.ContextResult) *agentbay.Context {
	if result == nil || result.Data == nil {
		return nil
	}

	return &agentbay.Context{
		ID:         result.ContextID,
		Name:       result.Data["name"].(string),
		State:      result.Data["state"].(string),
		CreatedAt:  result.Data["created_at"].(string),
		LastUsedAt: result.Data["last_used_at"].(string),
		OSType:     result.Data["os_type"].(string),
	}
}

// TestContextLifecycle tests the complete lifecycle of a context:
// 1. List initial contexts
// 2. Create a new context
// 3. List contexts and verify the new context is there
// 4. Get the context by name
// 5. Delete the context
// 6. List contexts and verify the context is gone
func TestContextLifecycle(t *testing.T) {
	// Initialize AgentBay client
	apiKey := testutil.GetTestAPIKey(t)
	t.Logf("Using API key: %s", apiKey)

	agentBay, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		t.Fatalf("Error initializing AgentBay client: %v", err)
	}
	t.Logf("AgentBay client initialized successfully with region: %s", agentBay.RegionId)

	// Step 1: List initial contexts
	t.Log("Step 1: Listing initial contexts...")
	initialContextsResult, err := agentBay.Context.List()
	if err != nil {
		t.Fatalf("Error listing contexts: %v", err)
	}

	initialContexts := initialContextsResult.Contexts
	t.Logf("Found %d initial contexts (RequestID: %s)",
		len(initialContexts), initialContextsResult.RequestID)
	for i, ctx := range initialContexts {
		t.Logf("Context %d: ID=%s, Name=%s, State=%s",
			i+1, ctx["id"], ctx["name"], ctx["state"])
	}

	// Step 2: Create a new context
	contextName := fmt.Sprintf("test-lifecycle-%d", time.Now().Unix())
	t.Logf("Step 2: Creating new context with name: %s", contextName)

	createResult, err := agentBay.Context.Create(contextName)
	if err != nil {
		t.Fatalf("Error creating context: %v", err)
	}

	// Get the created context to get its full details
	getResult, err := agentBay.Context.Get(contextName, false)
	if err != nil {
		t.Fatalf("Error getting created context: %v", err)
	}

	context := contextFromResult(getResult)
	t.Logf("Context created successfully - ID: %s, Name: %s (RequestID: %s)",
		context.ID, context.Name, createResult.RequestID)

	// Step 3: List contexts and verify the new context is there
	t.Log("Step 3: Listing contexts after creation...")
	updatedContextsResult, err := agentBay.Context.List()
	if err != nil {
		t.Fatalf("Error listing contexts: %v", err)
	}

	updatedContexts := updatedContextsResult.Contexts
	t.Logf("Found %d contexts after creation (RequestID: %s)",
		len(updatedContexts), updatedContextsResult.RequestID)

	// Check if our context is in the list
	contextFound := false
	for _, ctx := range updatedContexts {
		if ctx["name"] == contextName {
			contextFound = true
			t.Logf("Found our context in the list: ID=%s, Name=%s, State=%s",
				ctx["id"], ctx["name"], ctx["state"])
			break
		}
	}

	if !contextFound {
		t.Errorf("Created context not found in the list")
	}

	// Step 4: Get the context by name
	t.Log("Step 4: Getting the context by name...")
	getContextResult, err := agentBay.Context.Get(contextName, false)
	if err != nil {
		t.Fatalf("Error getting context: %v", err)
	}

	retrievedContext := contextFromResult(getContextResult)
	if retrievedContext == nil {
		t.Fatalf("Context not found by name")
	}

	t.Logf("Retrieved context - ID: %s, Name: %s, State: %s (RequestID: %s)",
		retrievedContext.ID, retrievedContext.Name, retrievedContext.State, getContextResult.RequestID)

	// Step 5: Delete the context
	t.Log("Step 5: Deleting the context...")
	deleteResult, err := agentBay.Context.Delete(context)
	if err != nil {
		t.Fatalf("Error deleting context: %v", err)
	}
	t.Logf("Context deleted successfully (RequestID: %s)", deleteResult.RequestID)

	// Step 6: List contexts and verify the context is gone
	t.Log("Step 6: Listing contexts after deletion...")
	finalContextsResult, err := agentBay.Context.List()
	if err != nil {
		t.Fatalf("Error listing contexts: %v", err)
	}

	finalContexts := finalContextsResult.Contexts
	t.Logf("Found %d contexts after deletion (RequestID: %s)",
		len(finalContexts), finalContextsResult.RequestID)

	// Check if our context is still in the list (it shouldn't be)
	contextFound = false
	for _, ctx := range finalContexts {
		if ctx["name"] == contextName {
			contextFound = true
			t.Logf("WARNING: Context still exists after deletion: ID=%s, Name=%s",
				ctx["id"], ctx["name"])
			break
		}
	}

	if contextFound {
		t.Errorf("Context still exists after deletion")
	} else {
		t.Logf("Context deletion verified: context no longer exists")
	}
}
