package agentbay_test

import (
	"encoding/json"
	"testing"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

func TestCreateSessionParams(t *testing.T) {
	// Test default initialization
	params := agentbay.NewCreateSessionParams()
	if params == nil {
		t.Fatal("Expected non-nil CreateSessionParams")
	}
	if params.Labels == nil {
		t.Error("Expected non-nil Labels map")
	}
	if len(params.Labels) != 0 {
		t.Errorf("Expected empty Labels map, got %v", params.Labels)
	}
	if params.ContextID != "" {
		t.Errorf("Expected empty ContextID, got %s", params.ContextID)
	}

	// Test WithLabels
	labels := map[string]string{
		"username": "alice",
		"project":  "my-project",
	}
	params = agentbay.NewCreateSessionParams().WithLabels(labels)
	if len(params.Labels) != 2 {
		t.Errorf("Expected 2 labels, got %d", len(params.Labels))
	}
	if params.Labels["username"] != "alice" {
		t.Errorf("Expected username=alice, got %s", params.Labels["username"])
	}
	if params.Labels["project"] != "my-project" {
		t.Errorf("Expected project=my-project, got %s", params.Labels["project"])
	}

	// Test WithContextID
	contextID := "test-context-id"
	params = agentbay.NewCreateSessionParams().WithContextID(contextID)
	if params.ContextID != contextID {
		t.Errorf("Expected ContextID=%s, got %s", contextID, params.ContextID)
	}

	// Test chaining
	params = agentbay.NewCreateSessionParams().
		WithLabels(labels).
		WithContextID(contextID)
	if len(params.Labels) != 2 {
		t.Errorf("Expected 2 labels, got %d", len(params.Labels))
	}
	if params.ContextID != contextID {
		t.Errorf("Expected ContextID=%s, got %s", contextID, params.ContextID)
	}

	// Test GetLabelsJSON
	params = agentbay.NewCreateSessionParams().WithLabels(labels)
	labelsJSON, err := params.GetLabelsJSON()
	if err != nil {
		t.Fatalf("Error getting labels JSON: %v", err)
	}

	// Verify the JSON string
	var parsedLabels map[string]string
	err = json.Unmarshal([]byte(labelsJSON), &parsedLabels)
	if err != nil {
		t.Fatalf("Error parsing labels JSON: %v", err)
	}
	if parsedLabels["username"] != "alice" {
		t.Errorf("Expected username=alice in JSON, got %s", parsedLabels["username"])
	}
	if parsedLabels["project"] != "my-project" {
		t.Errorf("Expected project=my-project in JSON, got %s", parsedLabels["project"])
	}

	// Test GetLabelsJSON with empty labels
	params = agentbay.NewCreateSessionParams()
	labelsJSON, err = params.GetLabelsJSON()
	if err != nil {
		t.Fatalf("Error getting empty labels JSON: %v", err)
	}
	if labelsJSON != "" {
		t.Errorf("Expected empty JSON string for empty labels, got %s", labelsJSON)
	}
}
