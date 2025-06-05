package main

import (
	"fmt"
	"os"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

func main() {
	// Get API key from environment variable or use a default value for testing
	apiKey := os.Getenv("AGENTBAY_API_KEY")
	if apiKey == "" {
		apiKey = "akm-xxx" // Replace with your actual API key for testing
		fmt.Println("Warning: Using default API key. Set AGENTBAY_API_KEY environment variable for production use.")
	}

	// Initialize the AgentBay client
	agentBay, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		fmt.Printf("Error initializing AgentBay client: %v\n", err)
		os.Exit(1)
	}

	// Example 1: Create a session with custom labels
	fmt.Println("\nExample 1: Creating a session with custom labels...")

	// Create parameters with labels
	params := agentbay.NewCreateSessionParams().
		WithLabels(map[string]string{
			"username": "alice",
			"project":  "my-project",
		})

	session, err := agentBay.Create(params)
	if err != nil {
		fmt.Printf("\nError creating session: %v\n", err)
		os.Exit(1)
	}
	fmt.Printf("\nSession created with ID: %s and labels: username=alice, project=my-project\n", session.SessionID)

	// Example 2: List sessions by labels
	fmt.Println("\nExample 2: Listing sessions by labels...")

	// Query sessions with the "project" label set to "my-project"
	sessionsByLabel, err := agentBay.ListByLabels(map[string]string{
		"project": "my-project",
	})
	if err != nil {
		fmt.Printf("\nError listing sessions by labels: %v\n", err)
		os.Exit(1)
	}

	fmt.Printf("\nFound %d sessions with project=my-project:\n", len(sessionsByLabel))
	for i, s := range sessionsByLabel {
		fmt.Printf("  %d. Session ID: %s\n", i+1, s.SessionID)
	}

	// Clean up
	fmt.Println("\nCleaning up sessions...")

	err = agentBay.Delete(session)
	if err != nil {
		fmt.Printf("Error deleting session: %v\n", err)
	}

	fmt.Println("Session deleted successfully")
}
