package main

import (
	"fmt"
	"os"
	"strings"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

// This example demonstrates how to create, list, and delete sessions
// using the Wuying AgentBay SDK.

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

	// Create a new session with default parameters
	fmt.Println("\nCreating a new session...")
	sessionResult, err := agentBay.Create(nil)
	if err != nil {
		fmt.Printf("\nError creating session: %v\n", err)
		os.Exit(1)
	}
	session := sessionResult.Session
	fmt.Printf("\nSession created with ID: %s (RequestID: %s)\n", session.SessionID, sessionResult.RequestID)

	// List all sessions
	fmt.Println("\nListing all sessions...")
	sessionsResult, err := agentBay.List()
	if err != nil {
		fmt.Printf("\nError listing sessions: %v\n", err)
		os.Exit(1)
	}

	// Extract SessionID list and join as string
	var sessionIDs []string
	for _, s := range sessionsResult.Sessions {
		sessionIDs = append(sessionIDs, s.SessionID)
	}
	sessionIDsStr := strings.Join(sessionIDs, ", ")
	fmt.Printf("\nAvailable sessions: %s (RequestID: %s)\n", sessionIDsStr, sessionsResult.RequestID)

	// Create multiple sessions to demonstrate listing
	fmt.Println("\nCreating additional sessions...")
	var additionalSessions []*agentbay.Session
	for i := 0; i < 2; i++ {
		additionalSessionResult, err := agentBay.Create(nil)
		if err != nil {
			fmt.Printf("\nError creating additional session: %v\n", err)
			continue
		}
		additionalSession := additionalSessionResult.Session
		fmt.Printf("Additional session created with ID: %s (RequestID: %s)\n", additionalSession.SessionID, additionalSessionResult.RequestID)

		// Store the session for later cleanup
		additionalSessions = append(additionalSessions, additionalSession)
	}

	// List sessions again to show the new sessions
	fmt.Println("\nListing all sessions after creating additional ones...")
	updatedSessionsResult, err := agentBay.List()
	if err != nil {
		fmt.Printf("\nError listing sessions: %v\n", err)
	} else {
		var updatedSessionIDs []string
		for _, s := range updatedSessionsResult.Sessions {
			updatedSessionIDs = append(updatedSessionIDs, s.SessionID)
		}
		updatedSessionIDsStr := strings.Join(updatedSessionIDs, ", ")
		fmt.Printf("\nUpdated list of sessions: %s (RequestID: %s)\n", updatedSessionIDsStr, updatedSessionsResult.RequestID)
	}

	// Clean up all sessions
	fmt.Println("\nCleaning up sessions...")
	// First delete the initial session
	deleteResult, err := session.Delete()
	if err != nil {
		fmt.Printf("Error deleting session %s: %v\n", session.SessionID, err)
	} else {
		fmt.Printf("Session %s deleted successfully (RequestID: %s)\n", session.SessionID, deleteResult.RequestID)
	}

	// Then delete the additional sessions
	for _, s := range additionalSessions {
		deleteResult, err := s.Delete()
		if err != nil {
			fmt.Printf("Error deleting session %s: %v\n", s.SessionID, err)
		} else {
			fmt.Printf("Session %s deleted successfully (RequestID: %s)\n", s.SessionID, deleteResult.RequestID)
		}
	}

	// List sessions one more time to confirm deletion
	fmt.Println("\nListing sessions after cleanup...")
	finalSessionsResult, err := agentBay.List()
	if err != nil {
		fmt.Printf("\nError listing sessions: %v\n", err)
	} else {
		if len(finalSessionsResult.Sessions) == 0 {
			fmt.Printf("All sessions have been deleted successfully. (RequestID: %s)\n", finalSessionsResult.RequestID)
		} else {
			var finalSessionIDs []string
			for _, s := range finalSessionsResult.Sessions {
				finalSessionIDs = append(finalSessionIDs, s.SessionID)
			}
			finalSessionIDsStr := strings.Join(finalSessionIDs, ", ")
			fmt.Printf("\nRemaining sessions: %s (RequestID: %s)\n", finalSessionIDsStr, finalSessionsResult.RequestID)
		}
	}
}
