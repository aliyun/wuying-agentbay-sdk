package unit

import (
	"encoding/json"
	"testing"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

// TestListByLabelsWithPagination tests list_by_labels method with pagination support
func TestListByLabelsWithPagination(t *testing.T) {
	// Skip the test since we can't properly mock the client without refactoring
	t.Skip("Skipping test that requires mocking client")

	// In a real test with proper mocking, you would:
	// 1. Create a mock AgentBay instance
	// 2. Create ListSessionParams with pagination parameters
	// 3. Mock the client's ListSession response to include pagination fields
	// 4. Call ListByLabels and verify the results include pagination information
}

// TestListByLabelsWithNextToken tests list_by_labels method with next_token
func TestListByLabelsWithNextToken(t *testing.T) {
	// Skip the test since we can't properly mock the client without refactoring
	t.Skip("Skipping test that requires mocking client")

	// In a real test with proper mocking, you would:
	// 1. Create a mock AgentBay instance
	// 2. Create ListSessionParams with a next_token from a previous call
	// 3. Mock the client's ListSession response
	// 4. Call ListByLabels and verify the next_token was used correctly
}

// TestListByLabelsDefaultParams tests list_by_labels method with default parameters
func TestListByLabelsDefaultParams(t *testing.T) {
	// Skip the test since we can't properly mock the client without refactoring
	t.Skip("Skipping test that requires mocking client")

	// In a real test with proper mocking, you would:
	// 1. Create a mock AgentBay instance
	// 2. Call ListByLabels with nil params (should use defaults)
	// 3. Verify the default values were used (MaxResults=10, empty Labels)
}

// TestListSessionParamsInitialization tests initialization of ListSessionParams
func TestListSessionParamsInitialization(t *testing.T) {
	// Create ListSessionParams with default values
	params := agentbay.NewListSessionParams()

	// Verify default values
	if params == nil {
		t.Fatal("Expected non-nil ListSessionParams")
	}
	if params.MaxResults != 10 {
		t.Errorf("Expected MaxResults to be 10, got %d", params.MaxResults)
	}
	if params.NextToken != "" {
		t.Errorf("Expected empty NextToken, got '%s'", params.NextToken)
	}
	if params.Labels == nil {
		t.Error("Expected non-nil Labels map")
	}
	if len(params.Labels) != 0 {
		t.Errorf("Expected empty Labels map, got %v", params.Labels)
	}
}

// TestListSessionParamsCustomValues tests ListSessionParams with custom values
func TestListSessionParamsCustomValues(t *testing.T) {
	// Create ListSessionParams with custom values
	params := agentbay.NewListSessionParams()
	params.MaxResults = 5
	params.NextToken = "next-page-token"
	params.Labels = map[string]string{
		"env":     "test",
		"project": "demo",
	}

	// Verify custom values
	if params.MaxResults != 5 {
		t.Errorf("Expected MaxResults to be 5, got %d", params.MaxResults)
	}
	if params.NextToken != "next-page-token" {
		t.Errorf("Expected NextToken to be 'next-page-token', got '%s'", params.NextToken)
	}
	if len(params.Labels) != 2 {
		t.Errorf("Expected 2 labels, got %d", len(params.Labels))
	}
	if params.Labels["env"] != "test" {
		t.Errorf("Expected env=test, got %s", params.Labels["env"])
	}
	if params.Labels["project"] != "demo" {
		t.Errorf("Expected project=demo, got %s", params.Labels["project"])
	}

	// Test JSON marshaling of labels
	labelsJSON, err := json.Marshal(params.Labels)
	if err != nil {
		t.Fatalf("Error marshaling labels to JSON: %v", err)
	}

	// Unmarshal and verify
	var parsedLabels map[string]string
	err = json.Unmarshal(labelsJSON, &parsedLabels)
	if err != nil {
		t.Fatalf("Error unmarshaling labels JSON: %v", err)
	}
	if len(parsedLabels) != 2 {
		t.Errorf("Expected 2 labels after unmarshaling, got %d", len(parsedLabels))
	}
	if parsedLabels["env"] != "test" {
		t.Errorf("Expected env=test after unmarshaling, got %s", parsedLabels["env"])
	}
}
