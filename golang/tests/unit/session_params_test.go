package unit

import (
	"encoding/json"
	"testing"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

// TestCreateSessionParamsDefaultInitialization tests that CreateSessionParams initializes with default values
func TestCreateSessionParamsDefaultInitialization(t *testing.T) {
	// Create default params
	params := agentbay.NewCreateSessionParams()

	// Verify default values
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

	if params.ImageId != "" {
		t.Errorf("Expected empty ImageId, got %s", params.ImageId)
	}
}

// TestCreateSessionParamsWithLabels tests that CreateSessionParams accepts custom labels
func TestCreateSessionParamsWithLabels(t *testing.T) {
	// Create labels
	labels := map[string]string{
		"username": "alice",
		"project":  "my-project",
	}

	// Create params with labels
	params := agentbay.NewCreateSessionParams().WithLabels(labels)

	// Verify labels were set
	if len(params.Labels) != 2 {
		t.Errorf("Expected 2 labels, got %d", len(params.Labels))
	}

	if params.Labels["username"] != "alice" {
		t.Errorf("Expected username=alice, got %s", params.Labels["username"])
	}

	if params.Labels["project"] != "my-project" {
		t.Errorf("Expected project=my-project, got %s", params.Labels["project"])
	}

	// Verify other fields are still default
	if params.ContextID != "" {
		t.Errorf("Expected empty ContextID, got %s", params.ContextID)
	}
}

// TestCreateSessionParamsWithContextID tests that CreateSessionParams accepts a context ID
func TestCreateSessionParamsWithContextID(t *testing.T) {
	// Create context ID
	contextID := "test-context-id"

	// Create params with context ID
	params := agentbay.NewCreateSessionParams().WithContextID(contextID)

	// Verify context ID was set
	if params.ContextID != contextID {
		t.Errorf("Expected ContextID=%s, got %s", contextID, params.ContextID)
	}

	// Verify other fields are still default
	if len(params.Labels) != 0 {
		t.Errorf("Expected empty Labels map, got %v", params.Labels)
	}
}

// TestCreateSessionParamsWithImageId tests that CreateSessionParams accepts an image ID
func TestCreateSessionParamsWithImageId(t *testing.T) {
	// Create image ID
	imageId := "test-image-id"

	// Create params with image ID
	params := agentbay.NewCreateSessionParams().WithImageId(imageId)

	// Verify image ID was set
	if params.ImageId != imageId {
		t.Errorf("Expected ImageId=%s, got %s", imageId, params.ImageId)
	}

	// Verify other fields are still default
	if len(params.Labels) != 0 {
		t.Errorf("Expected empty Labels map, got %v", params.Labels)
	}
	if params.ContextID != "" {
		t.Errorf("Expected empty ContextID, got %s", params.ContextID)
	}
}

// TestCreateSessionParamsWithAllParams tests that CreateSessionParams accepts all parameters
func TestCreateSessionParamsWithAllParams(t *testing.T) {
	// Create values
	labels := map[string]string{
		"username": "alice",
		"project":  "my-project",
	}
	contextID := "test-context-id"
	imageId := "test-image-id"

	// Create params with all values
	params := agentbay.NewCreateSessionParams().
		WithLabels(labels).
		WithContextID(contextID).
		WithImageId(imageId)

	// Verify all values were set
	if len(params.Labels) != 2 {
		t.Errorf("Expected 2 labels, got %d", len(params.Labels))
	}
	if params.Labels["username"] != "alice" {
		t.Errorf("Expected username=alice, got %s", params.Labels["username"])
	}
	if params.ContextID != contextID {
		t.Errorf("Expected ContextID=%s, got %s", contextID, params.ContextID)
	}
	if params.ImageId != imageId {
		t.Errorf("Expected ImageId=%s, got %s", imageId, params.ImageId)
	}
}

// TestCreateSessionParamsLabelsJsonConversion tests that labels can be converted to JSON
func TestCreateSessionParamsLabelsJsonConversion(t *testing.T) {
	// Create labels
	labels := map[string]string{
		"username": "alice",
		"project":  "my-project",
	}

	// Create params with labels
	params := agentbay.NewCreateSessionParams().WithLabels(labels)

	// Get labels as JSON
	labelsJSON, err := params.GetLabelsJSON()
	if err != nil {
		t.Fatalf("Error getting labels JSON: %v", err)
	}

	// Verify the JSON string by parsing it back
	var parsedLabels map[string]string
	err = json.Unmarshal([]byte(labelsJSON), &parsedLabels)
	if err != nil {
		t.Fatalf("Error parsing labels JSON: %v", err)
	}

	// Verify parsed labels match original labels
	if len(parsedLabels) != 2 {
		t.Errorf("Expected 2 labels, got %d", len(parsedLabels))
	}
	if parsedLabels["username"] != "alice" {
		t.Errorf("Expected username=alice, got %s", parsedLabels["username"])
	}
	if parsedLabels["project"] != "my-project" {
		t.Errorf("Expected project=my-project, got %s", parsedLabels["project"])
	}
}

// TestCreateSessionParamsEmptyLabelsJson tests that empty labels return an empty JSON string
func TestCreateSessionParamsEmptyLabelsJson(t *testing.T) {
	// Create params with no labels
	params := agentbay.NewCreateSessionParams()

	// Get labels as JSON
	labelsJSON, err := params.GetLabelsJSON()
	if err != nil {
		t.Fatalf("Error getting empty labels JSON: %v", err)
	}

	// Verify the JSON string is empty
	if labelsJSON != "" {
		t.Errorf("Expected empty JSON string for empty labels, got %s", labelsJSON)
	}
}
