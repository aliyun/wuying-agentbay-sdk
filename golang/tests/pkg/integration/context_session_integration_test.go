package integration_test

import (
	"fmt"
	"testing"
	"time"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
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

	context, err := agentBay.Context.Create(contextName)
	if err != nil {
		t.Fatalf("Error creating context: %v", err)
	}
	t.Logf("Context created successfully - ID: %s, Name: %s, State: %s, OSType: %s",
		context.ID, context.Name, context.State, context.OSType)

	// Ensure cleanup of the context at the end of the test
	defer func() {
		t.Log("Cleaning up: Deleting the context...")
		err := agentBay.Context.Delete(context)
		if err != nil {
			t.Logf("Warning: Error deleting context: %v", err)
		} else {
			t.Logf("Context %s deleted successfully", context.ID)
		}
	}()

	// Step 2: Create a session with the context ID (expect success)
	t.Log("Step 2: Creating first session with context ID...")
	params := agentbay.NewCreateSessionParams().WithContextID(context.ID)
	t.Logf("Session params: ContextID=%s", params.ContextID)

	session1, err := agentBay.Create(params)
	if err != nil {
		t.Fatalf("Error creating session with context ID: %v", err)
	}
	t.Logf("Session created successfully with ID: %s", session1.SessionID)

	// Ensure cleanup of the session if it's not released during the test
	defer func() {
		// Check if the session still exists before trying to delete it
		sessions, listErr := agentBay.List()
		if listErr != nil {
			t.Logf("Warning: Error listing sessions: %v", listErr)
			return
		}

		sessionExists := false
		for _, s := range sessions {
			if s.SessionID == session1.SessionID {
				sessionExists = true
				break
			}
		}

		if sessionExists {
			t.Log("Cleaning up: Deleting the first session...")
			err := session1.Delete()
			if err != nil {
				t.Logf("Warning: Error deleting first session: %v", err)
			} else {
				t.Log("First session successfully deleted")
			}
		}
	}()

	// Step 3: Get the context directly and verify that its status is "in-use"
	t.Log("Step 3: Checking context status after session creation...")

	// Wait a moment for the system to update the context status
	time.Sleep(2 * time.Second)

	updatedContext, err := agentBay.Context.Get(contextName, false)
	if err != nil {
		t.Fatalf("Error getting context: %v", err)
	}
	if updatedContext == nil {
		t.Fatalf("Context not found after session creation")
	}

	t.Logf("Retrieved context - ID: %s, Name: %s, State: %s", updatedContext.ID, updatedContext.Name, updatedContext.State)

	if updatedContext.State != "in-use" {
		t.Errorf("Expected context state to be 'in-use', got '%s'", updatedContext.State)
	} else {
		t.Logf("Context state is correctly set to 'in-use'")
	}

	// Step 4: Try to create another session with the same context_id (expect failure)
	t.Log("Step 4: Attempting to create a second session with the same context ID...")
	session2, err := agentBay.Create(params)
	if err == nil {
		// If somehow it succeeds (which shouldn't happen), make sure to clean it up
		t.Logf("WARNING: Unexpectedly succeeded in creating second session with ID: %s", session2.SessionID)
		t.Log("Cleaning up the unexpected second session...")
		cleanupErr := session2.Delete()
		if cleanupErr != nil {
			t.Logf("Warning: Error cleaning up unexpected second session: %v", cleanupErr)
		}
		t.Errorf("Expected error when creating second session with same context ID, but got success")
	} else {
		t.Logf("As expected, failed to create second session with same context ID: %v", err)
	}

	// Step 5: Release the first session
	t.Log("Step 5: Releasing the first session...")
	err = session1.Delete()
	if err != nil {
		t.Fatalf("Error releasing first session: %v", err)
	}
	t.Log("First session released successfully")

	// Wait for the system to update the context status
	t.Log("Waiting for context status to update...")
	time.Sleep(3 * time.Second)

	// Step 6: Get the context directly and verify that its status is "available"
	t.Log("Step 6: Checking context status after session release...")

	updatedContext, err = agentBay.Context.Get(contextName, false)
	if err != nil {
		t.Fatalf("Error getting context: %v", err)
	}
	if updatedContext == nil {
		t.Fatalf("Context not found after session release")
	}

	t.Logf("Retrieved context - ID: %s, Name: %s, State: %s", updatedContext.ID, updatedContext.Name, updatedContext.State)

	if updatedContext.State != "available" {
		t.Errorf("Expected context state to be 'available', got '%s'", updatedContext.State)
	} else {
		t.Logf("Context state is correctly set to 'available'")
	}

	// Step 7: Create another session with the same context_id (expect success)
	t.Log("Step 7: Creating a new session with the same context ID...")
	session3, err := agentBay.Create(params)
	if err != nil {
		t.Fatalf("Error creating new session with same context ID: %v", err)
	}
	t.Logf("New session created successfully with ID: %s", session3.SessionID)

	// Step 8: Clean up by releasing the session
	t.Log("Step 8: Cleaning up - releasing the third session...")
	err = session3.Delete()
	if err != nil {
		t.Fatalf("Error releasing third session: %v", err)
	}
	t.Log("Third session released successfully")

	// Context will be deleted by the defer function at the beginning
	t.Log("Test completed successfully")
}

// TestContextLifecycle tests the complete lifecycle of a context:
// 1. List initial contexts for comparison
// 2. Create a new context
// 3. Get the context by name
// 4. List contexts and verify the new context is in the list
// 5. Create a session with the context
// 6. Update the context name
// 7. Verify the update by getting the context again
// 8. List contexts again to verify the update is visible
// 9. Clean up by releasing the session and deleting the context
func TestContextLifecycle(t *testing.T) {
	// Initialize AgentBay client
	apiKey := getTestAPIKey(t)
	agentBay, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		t.Fatalf("Error initializing AgentBay client: %v", err)
	}

	// Get initial list of contexts for comparison later
	t.Log("Getting initial list of contexts...")
	initialContexts, err := agentBay.Context.List()
	if err != nil {
		t.Fatalf("Error listing initial contexts: %v", err)
	}
	t.Logf("Found %d contexts initially", len(initialContexts))

	// Store initial context IDs for comparison
	initialContextIDs := make(map[string]bool)
	for _, ctx := range initialContexts {
		initialContextIDs[ctx.ID] = true
		t.Logf("Initial context: %s (%s)", ctx.Name, ctx.ID)
	}

	// Step 1: Create a new context
	t.Log("Step 1: Creating a new context...")
	contextName := "test-context-" + fmt.Sprintf("%d", time.Now().Unix())
	context, err := agentBay.Context.Create(contextName)
	if err != nil {
		t.Fatalf("Error creating context: %v", err)
	}
	if context == nil {
		t.Fatalf("Context not created")
	}
	t.Logf("Created context: %s (%s)", context.Name, context.ID)

	// Verify the created context has the expected name
	if context.Name != contextName {
		t.Errorf("Expected context name to be '%s', got '%s'", contextName, context.Name)
	}
	if context.ID == "" {
		t.Errorf("Expected non-empty context ID")
	}

	// Store the original context ID for later verification
	originalContextID := context.ID

	// Ensure cleanup of the context after test
	defer func() {
		t.Log("Cleaning up: Deleting the context...")
		err := agentBay.Context.Delete(context)
		if err != nil {
			t.Logf("Warning: Error deleting context: %v", err)
		} else {
			t.Log("Context successfully deleted")

			// Verify the context is actually deleted
			deletedContext, err := agentBay.Context.Get(contextName, false)
			if err == nil && deletedContext != nil && deletedContext.ID == originalContextID {
				t.Errorf("Context still exists after deletion")
			}
		}
	}()

	// Step 2: Get the context we just created
	t.Log("Step 2: Getting the context we just created...")
	retrievedContext, err := agentBay.Context.Get(contextName, false)
	if err != nil {
		t.Fatalf("Error getting context: %v", err)
	}
	if retrievedContext == nil {
		t.Fatalf("Context not found")
	}

	// Verify the retrieved context matches what we created
	if retrievedContext.Name != contextName {
		t.Errorf("Expected retrieved context name to be '%s', got '%s'", contextName, retrievedContext.Name)
	}
	if retrievedContext.ID != originalContextID {
		t.Errorf("Expected retrieved context ID to be '%s', got '%s'", originalContextID, retrievedContext.ID)
	}
	t.Logf("Successfully retrieved context: %s (%s)", retrievedContext.Name, retrievedContext.ID)

	// Step 3: List contexts and verify our new context is in the list
	t.Log("Step 3: Listing all contexts...")
	allContexts, err := agentBay.Context.List()
	if err != nil {
		t.Fatalf("Error listing contexts: %v", err)
	}

	// Verify the list contains our new context
	var foundInInitialList bool
	for _, c := range allContexts {
		if c.ID == originalContextID {
			foundInInitialList = true
			if c.Name != contextName {
				t.Errorf("Expected context name in list to be '%s', got '%s'", contextName, c.Name)
			}
			break
		}
	}
	if !foundInInitialList {
		t.Errorf("New context with ID '%s' not found in context list", originalContextID)
	}

	// Verify the list contains at least one more context than the initial list
	if len(allContexts) <= len(initialContexts) {
		t.Errorf("Expected context list to grow, but it didn't: initial=%d, current=%d",
			len(initialContexts), len(allContexts))
	}
	t.Logf("Successfully listed contexts, found our context in the list")

	// Step 4: Create a session with the context
	t.Log("Step 4: Creating a session with the context...")
	params := agentbay.NewCreateSessionParams().
		WithContextID(context.ID).
		WithLabels(map[string]string{
			"username": "test-user",
			"project":  "test-project",
		})

	session, err := agentBay.Create(params)
	if err != nil {
		t.Fatalf("Error creating session: %v", err)
	}
	t.Logf("Session created with ID: %s", session.SessionID)

	// Ensure cleanup of the session after test
	defer func() {
		t.Log("Cleaning up: Deleting the session...")
		err := agentBay.Delete(session)
		if err != nil {
			t.Logf("Warning: Error deleting session: %v", err)
		} else {
			t.Log("Session successfully deleted")
		}
	}()

	// Step 5: Update the context
	t.Log("Step 5: Updating the context...")
	updatedName := "updated-" + contextName
	context.Name = updatedName
	success, err := agentBay.Context.Update(context)
	if err != nil {
		t.Fatalf("Error updating context: %v", err)
	}
	if !success {
		t.Fatalf("Context update reported as unsuccessful")
	}
	t.Logf("Context update reported as successful")

	// Step 6: Verify the update by getting the context again
	t.Log("Step 6: Verifying the update by getting the context again...")
	retrievedUpdatedContext, err := agentBay.Context.Get(updatedName, false)
	if err != nil {
		t.Fatalf("Error getting updated context: %v", err)
	}
	if retrievedUpdatedContext == nil {
		t.Fatalf("Updated context not found")
	}

	// Verify the retrieved context has the updated name
	if retrievedUpdatedContext.Name != updatedName {
		t.Errorf("Expected retrieved context name to be '%s', got '%s'", updatedName, retrievedUpdatedContext.Name)
	}
	if retrievedUpdatedContext.ID != originalContextID {
		t.Errorf("Expected retrieved context ID to be '%s', got '%s'", originalContextID, retrievedUpdatedContext.ID)
	}

	// Step 7: List contexts again to verify the update is visible in the list
	t.Log("Step 7: Listing contexts again to verify the update...")
	updatedContexts, err := agentBay.Context.List()
	if err != nil {
		t.Fatalf("Error listing contexts after update: %v", err)
	}

	// Find the updated context in the list
	var foundInUpdatedList bool
	for _, c := range updatedContexts {
		if c.ID == originalContextID {
			foundInUpdatedList = true
			if c.Name != updatedName {
				t.Errorf("Expected context name in list to be '%s', got '%s'", updatedName, c.Name)
			}
			break
		}
	}
	if !foundInUpdatedList {
		t.Errorf("Updated context with ID '%s' not found in context list", originalContextID)
	}

	t.Log("Test completed successfully")
}
