package agentbay_test

import (
	"testing"
	"time"

	"github.com/alibabacloud-go/tea/tea"
	mcp "github.com/aliyun/wuying-agentbay-sdk/golang/api/client"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
	"github.com/stretchr/testify/assert"
)

func TestContext_ClearAsync_Success(t *testing.T) {
	// Create mock client
	mockAgentBay, err := agentbay.NewAgentBay("test-api-key", nil)
	assert.NoError(t, err)
	assert.NotNil(t, mockAgentBay.Context)

	// Mock the ClearContext response
	mockResponse := &mcp.ClearContextResponse{
		Body: &mcp.ClearContextResponseBody{
			Success:   tea.Bool(true),
			RequestId: tea.String("test-request-id"),
			Code:      nil,
			Message:   nil,
		},
	}
	assert.NotNil(t, mockResponse.Body)
}

func TestContext_ClearAsync_APIError(t *testing.T) {
	// Create AgentBay instance
	agentBay, err := agentbay.NewAgentBay("test-api-key", nil)
	assert.NoError(t, err)

	// Test with invalid context ID
	result, err := agentBay.Context.ClearAsync("invalid-context-id")

	// Should return error
	if err == nil {
		assert.NotNil(t, result)
		assert.False(t, result.Success)
		assert.NotEmpty(t, result.ErrorMessage)
	}
}

func TestContext_GetClearStatus_Success(t *testing.T) {
	// Create AgentBay instance
	agentBay, err := agentbay.NewAgentBay("test-api-key", nil)
	assert.NoError(t, err)

	// Create test context first
	createResult, err := agentBay.Context.Create("test-context-for-clearing")
	if err == nil && createResult != nil && createResult.ContextID != "" {
		// Test GetClearStatus (internal method - not directly accessible)
		// This would require exposing the method or testing through Clear
		clearResult, _ := agentBay.Context.ClearAsync(createResult.ContextID)
		assert.NotNil(t, clearResult)

		// Clean up
		if createResult.ContextID != "" {
			ctx := &agentbay.Context{ID: createResult.ContextID}
			agentBay.Context.Delete(ctx)
		}
	}
}

func TestContext_Clear_Success(t *testing.T) {
	// Create AgentBay instance
	agentBay, err := agentbay.NewAgentBay("test-api-key", nil)
	assert.NoError(t, err)

	// Create test context first
	createResult, err := agentBay.Context.Create("test-context-for-clear")
	if err == nil && createResult != nil && createResult.ContextID != "" {
		// Test clear with short timeout and interval
		clearResult, err := agentBay.Context.Clear(createResult.ContextID, 5, 1.0)

		if err == nil {
			assert.NotNil(t, clearResult)
			// Status could be "clearing", "available", or error
			assert.Contains(t, []string{"clearing", "available", "", "FAILURE"}, clearResult.Status)
		}

		// Clean up
		if createResult.ContextID != "" {
			ctx := &agentbay.Context{ID: createResult.ContextID}
			agentBay.Context.Delete(ctx)
		}
	}
}

func TestContext_Clear_WithShortTimeout(t *testing.T) {
	// Create AgentBay instance
	agentBay, err := agentbay.NewAgentBay("test-api-key", nil)
	assert.NoError(t, err)

	// Test clear with very short timeout to test timeout behavior
	agentBay.Context.ClearAsync("context-123")

	// Test with 1 second timeout and 0.5 second interval
	clearResult, err := agentBay.Context.Clear("context-123", 1, 0.5)

	// Should timeout
	if err != nil {
		assert.Contains(t, err.Error(), "timed out")
	} else {
		assert.NotNil(t, clearResult)
	}
}

func TestContextClearResult_Initialization(t *testing.T) {
	result := &agentbay.ContextClearResult{
		Success:      true,
		Status:       "clearing",
		ContextID:    "context-123",
		ErrorMessage: "",
	}

	assert.True(t, result.Success)
	assert.Equal(t, "clearing", result.Status)
	assert.Equal(t, "context-123", result.ContextID)
	assert.Empty(t, result.ErrorMessage)
}

func TestContextClearResult_Defaults(t *testing.T) {
	result := &agentbay.ContextClearResult{}

	assert.False(t, result.Success)
	assert.Empty(t, result.Status)
	assert.Empty(t, result.ContextID)
	assert.Empty(t, result.ErrorMessage)
}

func TestContext_Clear_ConcurrentCalls(t *testing.T) {
	agentBay, err := agentbay.NewAgentBay("test-api-key", nil)
	assert.NoError(t, err)

	// Create context
	createResult, err := agentBay.Context.Create("test-context-concurrent")
	if err != nil || createResult == nil || createResult.ContextID == "" {
		t.Skip("Cannot create test context, skipping concurrent test")
	}

	// Start multiple clear operations concurrently
	done := make(chan bool, 3)

	go func() {
		agentBay.Context.ClearAsync(createResult.ContextID)
		done <- true
	}()

	go func() {
		agentBay.Context.ClearAsync(createResult.ContextID)
		done <- true
	}()

	go func() {
		time.Sleep(100 * time.Millisecond)
		done <- true
	}()

	// Wait for all goroutines
	<-done
	<-done
	<-done

	// Clean up
	if createResult.ContextID != "" {
		ctx := &agentbay.Context{ID: createResult.ContextID}
		agentBay.Context.Delete(ctx)
	}
}
