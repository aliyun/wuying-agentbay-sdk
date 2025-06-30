package agentbay_test

import (
	"encoding/json"
	"fmt"
	"math/rand"
	"testing"
	"time"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
	"github.com/aliyun/wuying-agentbay-sdk/golang/tests/pkg/agentbay/testutil"
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

func TestSession_SetGetLabels(t *testing.T) {
	// Initialize AgentBay client
	apiKey := testutil.GetTestAPIKey(t)
	agentBayClient, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		t.Fatalf("Error initializing AgentBay client: %v", err)
	}

	// Create a new session
	t.Log("Creating a new session for labels testing...")
	sessionResult, err := agentBayClient.Create(nil)
	if err != nil {
		t.Fatalf("Error creating session: %v", err)
	}

	session := sessionResult.Session
	t.Logf("Session created with ID: %s", session.SessionID)

	// Ensure cleanup of session
	defer func() {
		t.Log("Cleaning up session...")
		deleteResult, err := agentBayClient.Delete(session)
		if err != nil {
			t.Logf("Warning: Error deleting session: %v", err)
		} else {
			t.Logf("Session deleted (RequestID: %s)", deleteResult.RequestID)
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
	labelResult, err := session.SetLabels(string(labelsJSON))
	if err != nil {
		t.Fatalf("Error setting labels: %v", err)
	}
	t.Logf("Labels set successfully (RequestID: %s)", labelResult.RequestID)

	// Test 2: Get labels using GetLabels
	t.Log("Getting labels for the session...")
	getLabelResult, err := session.GetLabels()
	if err != nil {
		t.Fatalf("Error getting labels: %v", err)
	}
	t.Logf("Labels retrieved successfully (RequestID: %s)", getLabelResult.RequestID)

	// Parse the retrieved labels JSON
	var parsedLabels map[string]string
	err = json.Unmarshal([]byte(getLabelResult.Labels), &parsedLabels)
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

	params := agentbay.NewListSessionParams()
	params.Labels = singleLabelFilter
	sessionsResult, err := agentBayClient.ListByLabels(params)
	if err != nil {
		t.Fatalf("Error listing sessions by single label: %v", err)
	}
	t.Logf("Sessions listed by single label (RequestID: %s)", sessionsResult.RequestID)

	// Check if our session is in the results
	foundInSingleLabelResults := false
	for _, s := range sessionsResult.Sessions {
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

	params = agentbay.NewListSessionParams()
	params.Labels = multiLabelFilter
	sessionsResult, err = agentBayClient.ListByLabels(params)
	if err != nil {
		t.Fatalf("Error listing sessions by multiple labels: %v", err)
	}
	t.Logf("Sessions listed by multiple labels (RequestID: %s)", sessionsResult.RequestID)

	// Check if our session is in the results
	foundInMultiLabelResults := false
	for _, s := range sessionsResult.Sessions {
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

	params = agentbay.NewListSessionParams()
	params.Labels = nonMatchingFilter
	sessionsResult, err = agentBayClient.ListByLabels(params)
	if err != nil {
		t.Fatalf("Error listing sessions by non-matching label: %v", err)
	}
	t.Logf("Sessions listed by non-matching label (RequestID: %s)", sessionsResult.RequestID)

	// Check that our session is NOT in the results
	foundInNonMatchingResults := false
	for _, s := range sessionsResult.Sessions {
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
	updateResult, err := session.SetLabels(string(updatedLabelsJSON))
	if err != nil {
		t.Fatalf("Error updating labels: %v", err)
	}
	t.Logf("Labels updated successfully (RequestID: %s)", updateResult.RequestID)

	// Verify updated labels using GetLabels
	t.Log("Getting updated labels for the session...")
	retrievedUpdatedLabelsResult, err := session.GetLabels()
	if err != nil {
		t.Fatalf("Error getting updated labels: %v", err)
	}
	t.Logf("Updated labels retrieved successfully (RequestID: %s)", retrievedUpdatedLabelsResult.RequestID)

	// Parse the updated labels JSON
	var parsedUpdatedLabels map[string]string
	err = json.Unmarshal([]byte(retrievedUpdatedLabelsResult.Labels), &parsedUpdatedLabels)
	if err != nil {
		t.Fatalf("Error parsing updated labels JSON: %v", err)
	}

	// Verify that all expected updated labels are present with correct values
	for key, expectedValue := range updatedLabels {
		if actualValue, ok := parsedUpdatedLabels[key]; !ok {
			t.Errorf("Expected updated label '%s' not found", key)
		} else if actualValue != expectedValue {
			t.Errorf("Updated label '%s' value mismatch: expected '%s', got '%s'",
				key, expectedValue, actualValue)
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

	params = agentbay.NewListSessionParams()
	params.Labels = updatedEnvFilter
	updatedEnvResult, err := agentBayClient.ListByLabels(params)
	if err != nil {
		t.Fatalf("Error listing sessions by updated environment label: %v", err)
	}
	t.Logf("Sessions listed by updated environment (RequestID: %s)", updatedEnvResult.RequestID)

	foundWithUpdatedEnv := false
	for _, s := range updatedEnvResult.Sessions {
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

	params = agentbay.NewListSessionParams()
	params.Labels = oldEnvFilter
	oldEnvResult, err := agentBayClient.ListByLabels(params)
	if err != nil {
		t.Fatalf("Error listing sessions by old environment label: %v", err)
	}
	t.Logf("Sessions listed by old environment (RequestID: %s)", oldEnvResult.RequestID)

	foundWithOldEnv := false
	for _, s := range oldEnvResult.Sessions {
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

// TestListByUIDLabel tests querying sessions with a specific UID label
// and verifies pagination functionality
func TestListByUIDLabel(t *testing.T) {
	// Initialize AgentBay client
	apiKey := testutil.GetTestAPIKey(t)
	agentBayClient, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		t.Fatalf("Error initializing AgentBay client: %v", err)
	}

	// Define UID filter
	uidFilter := map[string]string{
		"test_group": "multi-session-test-1751262241385739000-4623",
	}

	// Test pagination by setting page size to 3 (expecting 6 total sessions)
	t.Log("Testing pagination with page size of 3...")

	// First page
	params := agentbay.NewListSessionParams()
	params.Labels = uidFilter
	params.MaxResults = 4 // Set page size to 4

	firstPageResult, err := agentBayClient.ListByLabels(params)
	if err != nil {
		t.Fatalf("Error listing first page of sessions: %v", err)
	}

	// Log the first page results
	t.Logf("First page - Sessions listed by UID label (RequestID: %s)", firstPageResult.RequestID)
	t.Logf("First page - Found %d sessions (MaxResults: %d, TotalCount: %d)",
		len(firstPageResult.Sessions), firstPageResult.MaxResults, firstPageResult.TotalCount)

	// Store session IDs from first page
	firstPageSessionIDs := make(map[string]bool)
	if len(firstPageResult.Sessions) > 0 {
		t.Log("First page - Sessions found:")
		for i, s := range firstPageResult.Sessions {
			t.Logf("  %d. Session ID: %s", i+1, s.SessionID)
			firstPageSessionIDs[s.SessionID] = true
		}
	} else {
		t.Log("First page - No sessions found with the specified UID label")
	}

	// Check if we have a next token for pagination
	if firstPageResult.NextToken == "" {
		t.Log("No NextToken returned, pagination not possible or not needed")
		return
	}

	// Second page
	t.Log("Fetching second page using NextToken...")
	secondPageParams := agentbay.NewListSessionParams()
	secondPageParams.Labels = uidFilter
	secondPageParams.MaxResults = 3
	secondPageParams.NextToken = firstPageResult.NextToken

	secondPageResult, err := agentBayClient.ListByLabels(secondPageParams)
	if err != nil {
		t.Fatalf("Error listing second page of sessions: %v", err)
	}

	// Log the second page results
	t.Logf("Second page - Sessions listed by UID label (RequestID: %s)", secondPageResult.RequestID)
	t.Logf("Second page - Found %d sessions", len(secondPageResult.Sessions))

	// Verify second page sessions are different from first page
	if len(secondPageResult.Sessions) > 0 {
		t.Log("Second page - Sessions found:")
		duplicateFound := false

		for i, s := range secondPageResult.Sessions {
			t.Logf("  %d. Session ID: %s", i+1, s.SessionID)

			// Check if this session was already in the first page
			if firstPageSessionIDs[s.SessionID] {
				duplicateFound = true
				t.Errorf("Session ID %s found in both first and second page", s.SessionID)
			}
		}

		if !duplicateFound {
			t.Log("Pagination verification successful: No duplicate sessions between pages")
		}
	} else {
		t.Log("Second page - No sessions found")
	}

	// Verify total count
	totalSessionsFound := len(firstPageResult.Sessions) + len(secondPageResult.Sessions)
	t.Logf("Total sessions found across both pages: %d", totalSessionsFound)

	if firstPageResult.TotalCount > 0 {
		if int(firstPageResult.TotalCount) != totalSessionsFound {
			t.Errorf("Note: TotalCount (%d) doesn't match actual sessions found (%d)",
				firstPageResult.TotalCount, totalSessionsFound)
		} else {
			t.Logf("TotalCount matches actual sessions found: %d", totalSessionsFound)
		}
	}
}

// TestListByLabels_OnlyUnreleasedSessions tests that ListByLabels only returns unreleased sessions
func TestListByLabels_OnlyUnreleasedSessions(t *testing.T) {
	// Initialize AgentBay client
	apiKey := testutil.GetTestAPIKey(t)
	agentBayClient, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		t.Fatalf("Error initializing AgentBay client: %v", err)
	}

	// Generate a unique identifier for this test run
	uniqueID := generateUniqueID()
	t.Logf("Using unique ID for test labels: %s", uniqueID)

	// Define a label to be used for all sessions in this test
	testLabel := map[string]string{
		"test_group": fmt.Sprintf("unreleased-session-test-%s", uniqueID),
	}

	// Convert label to JSON string
	labelJSON, err := json.Marshal(testLabel)
	if err != nil {
		t.Fatalf("Error marshaling label to JSON: %v", err)
	}

	// Number of sessions to create
	const totalSessionCount = 3
	const sessionsToReleaseCount = 1

	// Create multiple sessions with the same label
	var sessions []*agentbay.Session
	t.Logf("Creating %d sessions with the same label...", totalSessionCount)

	for i := 0; i < totalSessionCount; i++ {
		sessionResult, err := agentBayClient.Create(nil)
		if err != nil {
			t.Fatalf("Error creating session %d: %v", i+1, err)
		}

		session := sessionResult.Session
		t.Logf("Session %d created with ID: %s", i+1, session.SessionID)

		// Set the same label for each session
		labelResult, err := session.SetLabels(string(labelJSON))
		if err != nil {
			t.Fatalf("Error setting label for session %d: %v", i+1, err)
		}
		t.Logf("Label set successfully for session %d (RequestID: %s)", i+1, labelResult.RequestID)

		sessions = append(sessions, session)

		// Add a short delay between session creations to avoid rate limiting
		if i < totalSessionCount-1 {
			time.Sleep(2 * time.Second)
		}
	}

	// Store the IDs of all sessions for verification
	allSessionIDs := make(map[string]bool)
	for _, session := range sessions {
		allSessionIDs[session.SessionID] = true
	}

	// Release (delete) some of the sessions
	releasedSessionIDs := make(map[string]bool)
	t.Logf("Releasing %d out of %d sessions...", sessionsToReleaseCount, totalSessionCount)

	for i := 0; i < sessionsToReleaseCount; i++ {
		session := sessions[i]
		deleteResult, err := agentBayClient.Delete(session)
		if err != nil {
			t.Fatalf("Error releasing session %d: %v", i+1, err)
		}
		t.Logf("Session %d with ID %s released (RequestID: %s)", i+1, session.SessionID, deleteResult.RequestID)
		releasedSessionIDs[session.SessionID] = true
	}

	// Ensure cleanup of remaining sessions at the end of the test
	defer func() {
		t.Log("Cleaning up remaining sessions...")
		for i := sessionsToReleaseCount; i < totalSessionCount; i++ {
			session := sessions[i]
			deleteResult, err := agentBayClient.Delete(session)
			if err != nil {
				t.Logf("Warning: Error deleting session %d: %v", i+1, err)
			} else {
				t.Logf("Session %d deleted (RequestID: %s)", i+1, deleteResult.RequestID)
			}
		}
	}()

	// Use ListByLabels to get sessions with the test label
	t.Log("Listing sessions by label to verify only unreleased sessions are returned...")
	params := agentbay.NewListSessionParams()
	params.Labels = testLabel
	sessionsResult, err := agentBayClient.ListByLabels(params)
	if err != nil {
		t.Fatalf("Error listing sessions by label: %v", err)
	}
	t.Logf("Sessions listed by label (RequestID: %s)", sessionsResult.RequestID)

	// Verify that only unreleased sessions are returned
	t.Logf("Found %d sessions in the results", len(sessionsResult.Sessions))

	// Check each returned session
	for i, s := range sessionsResult.Sessions {
		t.Logf("Result session %d: ID=%s", i+1, s.SessionID)

		// Verify this session is one of our test sessions
		if !allSessionIDs[s.SessionID] {
			t.Logf("Note: Found a session not created in this test: %s", s.SessionID)
			continue
		}

		// Verify this session was not released
		if releasedSessionIDs[s.SessionID] {
			t.Errorf("Error: Released session with ID %s was returned by ListByLabels", s.SessionID)
		}
	}

	// Count how many of our unreleased sessions were found
	expectedUnreleasedCount := totalSessionCount - sessionsToReleaseCount
	foundUnreleasedCount := 0

	for _, s := range sessionsResult.Sessions {
		if allSessionIDs[s.SessionID] && !releasedSessionIDs[s.SessionID] {
			foundUnreleasedCount++
		}
	}

	// Verify that all unreleased sessions were found
	if foundUnreleasedCount != expectedUnreleasedCount {
		t.Errorf("Expected to find %d unreleased sessions, but found %d",
			expectedUnreleasedCount, foundUnreleasedCount)
	} else {
		t.Logf("Successfully found all %d unreleased sessions", expectedUnreleasedCount)
	}

	// Verify that no released sessions were found
	releasedSessionsFound := 0
	for _, s := range sessionsResult.Sessions {
		if releasedSessionIDs[s.SessionID] {
			releasedSessionsFound++
		}
	}

	if releasedSessionsFound > 0 {
		t.Errorf("Found %d released sessions in the results, expected 0", releasedSessionsFound)
	} else {
		t.Log("Verified that no released sessions were returned by ListByLabels")
	}

	fmt.Println("ListByLabels only returns unreleased sessions test completed successfully")
}
