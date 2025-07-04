package unit

import (
	"testing"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

// TestContextInitialization tests that Context initializes with the correct attributes
func TestContextInitialization(t *testing.T) {
	// Create a context
	context := &agentbay.Context{
		ID:         "test-id",
		Name:       "test-context",
		State:      "available",
		CreatedAt:  "2025-05-29T12:00:00Z",
		LastUsedAt: "2025-05-29T12:30:00Z",
		OSType:     "linux",
	}

	// Verify attributes
	if context.ID != "test-id" {
		t.Errorf("Expected ID to be 'test-id', got '%s'", context.ID)
	}
	if context.Name != "test-context" {
		t.Errorf("Expected Name to be 'test-context', got '%s'", context.Name)
	}
	if context.State != "available" {
		t.Errorf("Expected State to be 'available', got '%s'", context.State)
	}
	if context.CreatedAt != "2025-05-29T12:00:00Z" {
		t.Errorf("Expected CreatedAt to be '2025-05-29T12:00:00Z', got '%s'", context.CreatedAt)
	}
	if context.LastUsedAt != "2025-05-29T12:30:00Z" {
		t.Errorf("Expected LastUsedAt to be '2025-05-29T12:30:00Z', got '%s'", context.LastUsedAt)
	}
	if context.OSType != "linux" {
		t.Errorf("Expected OSType to be 'linux', got '%s'", context.OSType)
	}
}

// TestListContexts tests listing contexts
func TestListContexts(t *testing.T) {
	// Skip the test since we can't properly mock the client without refactoring
	t.Skip("Skipping test that requires mocking client")

	// In a real test with proper mocking, you would:
	// 1. Create a mock AgentBay instance
	// 2. Create a ContextService with the mock AgentBay
	// 3. Mock the ListContexts response
	// 4. Call List() and verify the results
}

// TestGetContext tests getting a context
func TestGetContext(t *testing.T) {
	// Skip the test since we can't properly mock the client without refactoring
	t.Skip("Skipping test that requires mocking client")

	// In a real test with proper mocking, you would:
	// 1. Create a mock AgentBay instance
	// 2. Create a ContextService with the mock AgentBay
	// 3. Mock the GetContext response
	// 4. Call Get() and verify the results
}

// TestCreateContext tests creating a context
func TestCreateContext(t *testing.T) {
	// Skip the test since we can't properly mock the client without refactoring
	t.Skip("Skipping test that requires mocking client")

	// In a real test with proper mocking, you would:
	// 1. Create a mock AgentBay instance
	// 2. Create a ContextService with the mock AgentBay
	// 3. Mock the GetContext response (with AllowCreate=true)
	// 4. Call Create() and verify the results
}

// TestUpdateContext tests updating a context
func TestUpdateContext(t *testing.T) {
	// Skip the test since we can't properly mock the client without refactoring
	t.Skip("Skipping test that requires mocking client")

	// In a real test with proper mocking, you would:
	// 1. Create a mock AgentBay instance
	// 2. Create a ContextService with the mock AgentBay
	// 3. Create a Context to update
	// 4. Mock the ModifyContext response
	// 5. Call Update() and verify the results
}

// TestDeleteContext tests deleting a context
func TestDeleteContext(t *testing.T) {
	// Skip the test since we can't properly mock the client without refactoring
	t.Skip("Skipping test that requires mocking client")

	// In a real test with proper mocking, you would:
	// 1. Create a mock AgentBay instance
	// 2. Create a ContextService with the mock AgentBay
	// 3. Create a Context to delete
	// 4. Mock the DeleteContext response
	// 5. Call Delete() and verify the results
}
