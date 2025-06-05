package main

import (
	"fmt"
	"os"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

func main() {
	// Initialize the AgentBay client
	// You can provide the API key as a parameter or set the AGENTBAY_API_KEY environment variable
	apiKey := os.Getenv("AGENTBAY_API_KEY")
	if apiKey == "" {
		apiKey = "akm-xxx" // Replace with your actual API key
	}

	agentBay, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		fmt.Printf("Error initializing AgentBay: %v\n", err)
		return
	}

	// Example 1: List all contexts
	fmt.Println("\nExample 1: Listing all contexts...")
	contexts, err := agentBay.Context.List()
	if err != nil {
		fmt.Printf("Error listing contexts: %v\n", err)
	} else {
		fmt.Printf("Found %d contexts:\n", len(contexts))
		for _, context := range contexts {
			fmt.Printf("- %s (%s): state=%s, os=%s\n", context.Name, context.ID, context.State, context.OSType)
		}
	}

	// Example 2: Get a context (create if it doesn't exist)
	fmt.Println("\nExample 2: Getting a context (creating if it doesn't exist)...")
	contextName := "my-test-context"
	context, err := agentBay.Context.Get(contextName, true)
	if err != nil {
		fmt.Printf("Error getting context: %v\n", err)
		return
	}
	if context != nil {
		fmt.Printf("Got context: %s (%s)\n", context.Name, context.ID)
	} else {
		fmt.Println("Context not found and could not be created")
		return
	}

	// Example 3: Create a session with the context
	fmt.Println("\nExample 3: Creating a session with the context...")
	params := agentbay.NewCreateSessionParams().
		WithContextID(context.ID).
		WithLabels(map[string]string{
			"username": "alice",
			"project":  "my-project",
		})

	session, err := agentBay.Create(params)
	if err != nil {
		fmt.Printf("Error creating session: %v\n", err)
		return
	}
	fmt.Printf("Session created with ID: %s\n", session.SessionID)

	// Example 4: Update the context
	fmt.Println("\nExample 4: Updating the context...")
	context.Name = "renamed-test-context"
	success, err := agentBay.Context.Update(context)
	if err != nil {
		fmt.Printf("Error updating context: %v\n", err)
	} else if !success {
		fmt.Println("Context update was not successful")
	} else {
		fmt.Printf("Context updated successfully to: %s\n", context.Name)
	}

	// Clean up
	fmt.Println("\nCleaning up...")

	// Delete the session
	err = agentBay.Delete(session)
	if err != nil {
		fmt.Printf("Error deleting session: %v\n", err)
	} else {
		fmt.Println("Session deleted successfully")
	}

	// Delete the context
	fmt.Println("Deleting the context...")
	err = agentBay.Context.Delete(context)
	if err != nil {
		fmt.Printf("Error deleting context: %v\n", err)
	} else {
		fmt.Println("Context deleted successfully")
	}
}
