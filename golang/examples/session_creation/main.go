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
	session, err := agentBay.Create(nil)
	if err != nil {
		fmt.Printf("\nError creating session: %v\n", err)
		os.Exit(1)
	}
	fmt.Printf("\nSession created with ID: %s\n", session.SessionID)

	// List all sessions
	fmt.Println("\nListing all sessions...")
	sessions, err := agentBay.List()
	if err != nil {
		fmt.Printf("\nError listing sessions: %v\n", err)
		os.Exit(1)
	}

	// Extract SessionID list and join as string
	var sessionIDs []string
	for _, s := range sessions {
		sessionIDs = append(sessionIDs, s.SessionID)
	}
	sessionIDsStr := strings.Join(sessionIDs, ", ")
	fmt.Printf("\nAvailable sessions: %s\n", sessionIDsStr)

	// Create multiple sessions to demonstrate listing
	fmt.Println("\nCreating additional sessions...")
	var additionalSessions []*agentbay.Session
	for i := 0; i < 2; i++ {
		additionalSession, err := agentBay.Create(nil)
		if err != nil {
			fmt.Printf("\nError creating additional session: %v\n", err)
			continue
		}
		fmt.Printf("Additional session created with ID: %s\n", additionalSession.SessionID)

		// Store the session for later cleanup
		additionalSessions = append(additionalSessions, additionalSession)
	}

	// List sessions again to show the new sessions
	fmt.Println("\nListing all sessions after creating additional ones...")
	updatedSessions, err := agentBay.List()
	if err != nil {
		fmt.Printf("\nError listing sessions: %v\n", err)
	} else {
		var updatedSessionIDs []string
		for _, s := range updatedSessions {
			updatedSessionIDs = append(updatedSessionIDs, s.SessionID)
		}
		updatedSessionIDsStr := strings.Join(updatedSessionIDs, ", ")
		fmt.Printf("\nUpdated list of sessions: %s\n", updatedSessionIDsStr)
	}

	// Clean up all sessions
	fmt.Println("\nCleaning up sessions...")
	// First delete the initial session
	err = agentBay.Delete(session)
	if err != nil {
		fmt.Printf("Error deleting session %s: %v\n", session.SessionID, err)
	} else {
		fmt.Printf("Session %s deleted successfully\n", session.SessionID)
	}

	// Then delete the additional sessions
	for _, s := range additionalSessions {
		err = agentBay.Delete(s)
		if err != nil {
			fmt.Printf("Error deleting session %s: %v\n", s.SessionID, err)
		} else {
			fmt.Printf("Session %s deleted successfully\n", s.SessionID)
		}
	}

	// List sessions one more time to confirm deletion
	fmt.Println("\nListing sessions after cleanup...")
	finalSessions, err := agentBay.List()
	if err != nil {
		fmt.Printf("\nError listing sessions: %v\n", err)
	} else {
		if len(finalSessions) == 0 {
			fmt.Println("All sessions have been deleted successfully.")
		} else {
			var finalSessionIDs []string
			for _, s := range finalSessions {
				finalSessionIDs = append(finalSessionIDs, s.SessionID)
			}
			finalSessionIDsStr := strings.Join(finalSessionIDs, ", ")
			fmt.Printf("\nRemaining sessions: %s\n", finalSessionIDsStr)
		}
	}
}
