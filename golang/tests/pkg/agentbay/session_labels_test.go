package agentbay_test

import (
	"encoding/json"
	"fmt"
	"math/rand"
	"testing"
	"time"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

// generateUniqueID creates a unique identifier for test labels
// to avoid conflicts with existing data in the database
func generateUniqueID() string {
	// Seed the random number generator to ensure different random numbers each time
	rand.Seed(time.Now().UnixNano())
	timestamp := time.Now().UnixNano()
	randomPart := rand.Intn(10000)
	return fmt.Sprintf("%d-%d", timestamp, randomPart)
}

// TestSession_SetGetLabels tests the functionality of setting and getting labels for a session
func TestSession_SetGetLabels(t *testing.T) {
	// Initialize AgentBay client
	apiKey := getTestAPIKey(t)
	agentBayClient, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		t.Fatalf("Error initializing AgentBay client: %v", err)
	}

	// Create a new session
	t.Log("Creating a new session for labels testing...")
	session, err := agentBayClient.Create(nil)
	if err != nil {
		t.Fatalf("Error creating session: %v", err)
	}
	t.Logf("Session created with ID: %s", session.SessionID)

	// Ensure cleanup of session
	defer func() {
		t.Log("Cleaning up session...")
		err := agentBayClient.Delete(session)
		if err != nil {
			t.Logf("Warning: Error deleting session: %v", err)
		}
	}()

	// Generate a unique identifier for this test run
	uniqueID := generateUniqueID()
	t.Logf("Using unique ID for test labels: %s", uniqueID)

	// Define test labels with unique values to avoid conflicts with existing data
	testLabels := map[string]string{
		"environment": fmt.Sprintf("testing-%s", uniqueID),
		"owner":       fmt.Sprintf("test-team-%s", uniqueID),
		"project":     fmt.Sprintf("labels-test-%s", uniqueID),
		"version":     "1.0.0",
	}

	// Convert labels to JSON string
	labelsJSON, err := json.Marshal(testLabels)
	if err != nil {
		t.Fatalf("Error marshaling labels to JSON: %v", err)
	}

	// Test 1: Set labels using SetLabels
	t.Log("Setting labels for the session...")
	err = session.SetLabels(string(labelsJSON))
	if err != nil {
		t.Fatalf("Error setting labels: %v", err)
	}

	// Test 2: Get labels using GetLabels
	t.Log("Getting labels for the session...")
	retrievedLabels, err := session.GetLabels()
	if err != nil {
		t.Fatalf("Error getting labels: %v", err)
	}

	// Parse the retrieved labels JSON
	var parsedLabels map[string]string
	err = json.Unmarshal([]byte(retrievedLabels), &parsedLabels)
	if err != nil {
		t.Fatalf("Error parsing retrieved labels JSON: %v", err)
	}

	// Verify that all expected labels are present with correct values
	for key, expectedValue := range testLabels {
		if actualValue, ok := parsedLabels[key]; !ok {
			t.Errorf("Expected label '%s' not found in retrieved labels", key)
		} else if actualValue != expectedValue {
			t.Errorf("Label '%s' value mismatch: expected '%s', got '%s'", key, expectedValue, actualValue)
		}
	}

	// Test 3: Verify labels using ListByLabels
	t.Log("Verifying labels using ListByLabels...")

	// Test with a single label (using the unique value)
	singleLabelFilter := map[string]string{
		"environment": testLabels["environment"],
	}

	sessions, err := agentBayClient.ListByLabels(singleLabelFilter)
	if err != nil {
		t.Fatalf("Error listing sessions by single label: %v", err)
	}

	// Check if our session is in the results
	foundInSingleLabelResults := false
	for _, s := range sessions {
		if s.SessionID == session.SessionID {
			foundInSingleLabelResults = true
			break
		}
	}

	if !foundInSingleLabelResults {
		t.Errorf("Session not found when filtering by single label")
	} else {
		t.Log("Session successfully found when filtering by single label")
	}

	// Test with multiple labels (using the unique values)
	multiLabelFilter := map[string]string{
		"environment": testLabels["environment"],
		"project":     testLabels["project"],
	}

	sessions, err = agentBayClient.ListByLabels(multiLabelFilter)
	if err != nil {
		t.Fatalf("Error listing sessions by multiple labels: %v", err)
	}

	// Check if our session is in the results
	foundInMultiLabelResults := false
	for _, s := range sessions {
		if s.SessionID == session.SessionID {
			foundInMultiLabelResults = true
			break
		}
	}

	if !foundInMultiLabelResults {
		t.Errorf("Session not found when filtering by multiple labels")
	} else {
		t.Log("Session successfully found when filtering by multiple labels")
	}

	// Test with non-matching label
	nonMatchingFilter := map[string]string{
		"environment": fmt.Sprintf("production-%s", uniqueID), // This doesn't match our session
	}

	sessions, err = agentBayClient.ListByLabels(nonMatchingFilter)
	if err != nil {
		t.Fatalf("Error listing sessions by non-matching label: %v", err)
	}

	// Check that our session is NOT in the results
	foundInNonMatchingResults := false
	for _, s := range sessions {
		if s.SessionID == session.SessionID {
			foundInNonMatchingResults = true
			break
		}
	}

	if foundInNonMatchingResults {
		t.Errorf("Session found when filtering by non-matching label")
	} else {
		t.Log("Session correctly not found when filtering by non-matching label")
	}

	// Test 4: Update labels (using the unique values)
	updatedLabels := map[string]string{
		"environment": fmt.Sprintf("staging-%s", uniqueID),
		"owner":       testLabels["owner"],
		"project":     fmt.Sprintf("labels-test-updated-%s", uniqueID),
		"status":      "active",
	}

	updatedLabelsJSON, err := json.Marshal(updatedLabels)
	if err != nil {
		t.Fatalf("Error marshaling updated labels to JSON: %v", err)
	}

	t.Log("Updating labels for the session...")
	err = session.SetLabels(string(updatedLabelsJSON))
	if err != nil {
		t.Fatalf("Error updating labels: %v", err)
	}

	// Verify updated labels using GetLabels
	t.Log("Getting updated labels for the session...")
	retrievedUpdatedLabels, err := session.GetLabels()
	if err != nil {
		t.Fatalf("Error getting updated labels: %v", err)
	}

	var parsedUpdatedLabels map[string]string
	err = json.Unmarshal([]byte(retrievedUpdatedLabels), &parsedUpdatedLabels)
	if err != nil {
		t.Fatalf("Error parsing retrieved updated labels JSON: %v", err)
	}

	// Verify that all expected updated labels are present with correct values
	for key, expectedValue := range updatedLabels {
		if actualValue, ok := parsedUpdatedLabels[key]; !ok {
			t.Errorf("Expected updated label '%s' not found in retrieved labels", key)
		} else if actualValue != expectedValue {
			t.Errorf("Updated label '%s' value mismatch: expected '%s', got '%s'", key, expectedValue, actualValue)
		}
	}

	// Verify that the old label that was removed is no longer present
	if _, ok := parsedUpdatedLabels["version"]; ok {
		t.Errorf("Removed label 'version' still present in updated labels")
	}

	// Verify updated labels using ListByLabels with the new environment value
	updatedEnvFilter := map[string]string{
		"environment": updatedLabels["environment"],
	}

	sessions, err = agentBayClient.ListByLabels(updatedEnvFilter)
	if err != nil {
		t.Fatalf("Error listing sessions by updated environment label: %v", err)
	}

	foundWithUpdatedEnv := false
	for _, s := range sessions {
		if s.SessionID == session.SessionID {
			foundWithUpdatedEnv = true
			break
		}
	}

	if !foundWithUpdatedEnv {
		t.Errorf("Session not found when filtering by updated environment label")
	} else {
		t.Log("Session successfully found when filtering by updated environment label")
	}

	// The session should no longer be found with the old environment value
	oldEnvFilter := map[string]string{
		"environment": testLabels["environment"],
	}

	sessions, err = agentBayClient.ListByLabels(oldEnvFilter)
	if err != nil {
		t.Fatalf("Error listing sessions by old environment label: %v", err)
	}

	foundWithOldEnv := false
	for _, s := range sessions {
		if s.SessionID == session.SessionID {
			foundWithOldEnv = true
			break
		}
	}

	if foundWithOldEnv {
		t.Errorf("Session found when filtering by old environment label")
	} else {
		t.Log("Session correctly not found when filtering by old environment label")
	}

	fmt.Println("Session labels test completed successfully")
}
