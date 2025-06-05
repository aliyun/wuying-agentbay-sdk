package agentbay_test

import (
	"fmt"
	"testing"
	"time"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

// TestContext_GetNonExistentContext tests attempting to get a context that doesn't exist
func TestContext_GetNonExistentContext(t *testing.T) {
	// Initialize AgentBay client
	apiKey := getTestAPIKey(t)
	agentBay, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		t.Fatalf("Error initializing AgentBay client: %v", err)
	}

	// Try to get a non-existent context with AllowCreate=false
	nonExistentName := fmt.Sprintf("non-existent-context-%d", time.Now().Unix())
	t.Logf("Attempting to get non-existent context: %s with AllowCreate=false", nonExistentName)

	context, err := agentBay.Context.Get(nonExistentName, false)

	// We expect either an error or a nil context since the context doesn't exist
	// and we're not allowing creation
	if err == nil && context != nil && context.ID != "" {
		// If we somehow got a context, make sure to clean it up
		t.Errorf("Unexpectedly got a context when requesting a non-existent one with AllowCreate=false: %+v", context)

		// Clean up the unexpected context
		cleanupErr := agentBay.Context.Delete(context)
		if cleanupErr != nil {
			t.Logf("Warning: Error cleaning up unexpected context: %v", cleanupErr)
		}
	} else {
		// This is the expected outcome - either an error or nil context
		t.Logf("As expected, failed to get non-existent context or got nil: err=%v, context=%+v", err, context)
	}
}

// TestContext_Create tests creating a new context
func TestContext_Create(t *testing.T) {
	// Initialize AgentBay client
	apiKey := getTestAPIKey(t)
	agentBay, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		t.Fatalf("Error initializing AgentBay client: %v", err)
	}

	// Create a new context
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

	// Clean up
	err = agentBay.Context.Delete(context)
	if err != nil {
		t.Logf("Warning: Error deleting context: %v", err)
	}
}

// TestContext_Get tests retrieving a context by name
func TestContext_Get(t *testing.T) {
	// Initialize AgentBay client
	apiKey := getTestAPIKey(t)
	agentBay, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		t.Fatalf("Error initializing AgentBay client: %v", err)
	}

	// First create a context
	contextName := "test-context-" + fmt.Sprintf("%d", time.Now().Unix())
	context, err := agentBay.Context.Create(contextName)
	if err != nil {
		t.Fatalf("Error creating context: %v", err)
	}
	originalContextID := context.ID

	// Ensure cleanup of the context after test
	defer func() {
		err := agentBay.Context.Delete(context)
		if err != nil {
			t.Logf("Warning: Error deleting context: %v", err)
		}
	}()

	// Get the context we just created
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
}

// TestContext_List tests listing all contexts
func TestContext_List(t *testing.T) {
	// Initialize AgentBay client
	apiKey := getTestAPIKey(t)
	agentBay, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		t.Fatalf("Error initializing AgentBay client: %v", err)
	}

	// Get initial list of contexts
	initialContexts, err := agentBay.Context.List()
	if err != nil {
		t.Fatalf("Error listing contexts: %v", err)
	}
	t.Logf("Found %d contexts initially", len(initialContexts))

	// Create a new context
	contextName := "test-context-" + fmt.Sprintf("%d", time.Now().Unix())
	context, err := agentBay.Context.Create(contextName)
	if err != nil {
		t.Fatalf("Error creating context: %v", err)
	}
	originalContextID := context.ID

	// Ensure cleanup of the context after test
	defer func() {
		err := agentBay.Context.Delete(context)
		if err != nil {
			t.Logf("Warning: Error deleting context: %v", err)
		}
	}()

	// List contexts again and verify our new context is in the list
	allContexts, err := agentBay.Context.List()
	if err != nil {
		t.Fatalf("Error listing contexts: %v", err)
	}

	// Verify the list contains our new context
	var foundInList bool
	for _, c := range allContexts {
		if c.ID == originalContextID {
			foundInList = true
			if c.Name != contextName {
				t.Errorf("Expected context name in list to be '%s', got '%s'", contextName, c.Name)
			}
			break
		}
	}
	if !foundInList {
		t.Errorf("New context with ID '%s' not found in context list", originalContextID)
	}

	// Verify the list contains at least one more context than the initial list
	if len(allContexts) <= len(initialContexts) {
		t.Errorf("Expected context list to grow, but it didn't: initial=%d, current=%d",
			len(initialContexts), len(allContexts))
	}
	t.Logf("Successfully listed contexts, found our context in the list")
}

// TestContext_Update tests updating a context's name
func TestContext_Update(t *testing.T) {
	// Initialize AgentBay client
	apiKey := getTestAPIKey(t)
	agentBay, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		t.Fatalf("Error initializing AgentBay client: %v", err)
	}

	// First create a context
	contextName := "test-context-" + fmt.Sprintf("%d", time.Now().Unix())
	context, err := agentBay.Context.Create(contextName)
	if err != nil {
		t.Fatalf("Error creating context: %v", err)
	}
	originalContextID := context.ID

	// Ensure cleanup of the context after test
	defer func() {
		err := agentBay.Context.Delete(context)
		if err != nil {
			t.Logf("Warning: Error deleting context: %v", err)
		}
	}()

	// Update the context
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

	// Verify the update by getting the context again
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
}

// TestContext_Delete tests deleting a context
func TestContext_Delete(t *testing.T) {
	// Initialize AgentBay client
	apiKey := getTestAPIKey(t)
	agentBay, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		t.Fatalf("Error initializing AgentBay client: %v", err)
	}

	// First create a context
	contextName := "test-context-" + fmt.Sprintf("%d", time.Now().Unix())
	context, err := agentBay.Context.Create(contextName)
	if err != nil {
		t.Fatalf("Error creating context: %v", err)
	}
	originalContextID := context.ID

	// Delete the context
	err = agentBay.Context.Delete(context)
	if err != nil {
		t.Fatalf("Error deleting context: %v", err)
	}
	t.Log("Context successfully deleted")

	// Verify the context is actually deleted
	deletedContext, err := agentBay.Context.Get(contextName, false)
	if err == nil && deletedContext != nil && deletedContext.ID == originalContextID {
		t.Errorf("Context still exists after deletion")

		// Clean up if it still exists
		cleanupErr := agentBay.Context.Delete(deletedContext)
		if cleanupErr != nil {
			t.Logf("Warning: Error cleaning up context: %v", cleanupErr)
		}
	}
}
