package main

import (
	"fmt"
	"log"
	"os"
	"time"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

func main() {
	// Get API key from environment variable
	apiKey := os.Getenv("AGENTBAY_API_KEY")
	if apiKey == "" {
		log.Fatal("AGENTBAY_API_KEY environment variable is not set")
	}

	// Initialize AgentBay client
	client, err := agentbay.NewAgentBay(apiKey, nil)
	if err != nil {
		log.Fatalf("Failed to initialize AgentBay client: %v", err)
	}

	// Create a session for demonstration
	fmt.Println("Creating a session...")
	createResult, err := client.Create(nil)
	if err != nil {
		log.Fatalf("Failed to create session: %v", err)
	}
	session := createResult.Session
	fmt.Printf("Created session with ID: %s\n", session.SessionID)

	// Ensure cleanup
	defer func() {
		fmt.Println("\nCleaning up...")
		deleteResult, err := session.Delete()
		if err != nil {
			log.Printf("Failed to delete session: %v", err)
		} else if deleteResult.Success {
			fmt.Printf("Session %s deleted successfully\n", session.SessionID)
		} else {
			fmt.Printf("Failed to delete session %s: %s\n", session.SessionID, deleteResult.ErrorMessage)
		}
	}()

	// Verify session is running
	fmt.Println("\n1. Verifying session is running...")
	getResult, err := client.GetSession(session.SessionID)
	if err != nil {
		log.Fatalf("Failed to get session status: %v", err)
	}
	if getResult.Success && getResult.Data != nil {
		fmt.Printf("Session status: %s\n", getResult.Data.Status)
	} else {
		log.Fatalf("Failed to get session status: %s", getResult.ErrorMessage)
	}

	// Perform some work on the session (e.g., execute a command)
	fmt.Println("\n2. Performing work on the session...")
	commandResult, err := session.Command.ExecuteCommand("echo 'Hello from AgentBay session'", 30000)
	if err != nil {
		log.Printf("Warning: Failed to execute command: %v", err)
	} else if commandResult.Output != "" {
		fmt.Printf("Command output: %s\n", commandResult.Output)
	} else {
		fmt.Println("Command executed successfully")
	}

	// Pause the session to save resources
	fmt.Println("\n3. Pausing the session...")
	pauseResult, err := client.Pause(session, 300, 2.0) // 5 minute timeout, 2 second poll interval
	if err != nil {
		log.Fatalf("Failed to pause session: %v", err)
	}
	if !pauseResult.Success {
		log.Fatalf("Failed to pause session: %s", pauseResult.ErrorMessage)
	}
	fmt.Printf("Session paused successfully (RequestID: %s)\n", pauseResult.RequestID)

	// Wait a moment to ensure pause is complete
	time.Sleep(2 * time.Second)

	// Verify session is paused
	fmt.Println("\n4. Verifying session is paused...")
	getResult, err = client.GetSession(session.SessionID)
	if err != nil {
		log.Fatalf("Failed to get session status: %v", err)
	}
	if getResult.Success && getResult.Data != nil {
		fmt.Printf("Session status: %s\n", getResult.Data.Status)
	} else {
		log.Fatalf("Failed to get session status: %s", getResult.ErrorMessage)
	}

	// Try to perform work on the paused session (should fail or wait until resumed)
	fmt.Println("\n5. Attempting work on paused session...")
	commandResult, err = session.Command.ExecuteCommand("echo 'This might not work on paused session'", 5000)
	if err != nil {
		fmt.Printf("Expected: Command failed on paused session: %v\n", err)
	} else if commandResult.Output != "" {
		fmt.Printf("Command output: %s\n", commandResult.Output)
	} else {
		fmt.Println("Command executed on paused session")
	}

	// Resume the session
	fmt.Println("\n6. Resuming the session...")
	resumeResult, err := client.Resume(session, 300, 2.0) // 5 minute timeout, 2 second poll interval
	if err != nil {
		log.Fatalf("Failed to resume session: %v", err)
	}
	if !resumeResult.Success {
		log.Fatalf("Failed to resume session: %s", resumeResult.ErrorMessage)
	}
	fmt.Printf("Session resumed successfully (RequestID: %s)\n", resumeResult.RequestID)

	// Wait a moment to ensure resume is complete
	time.Sleep(2 * time.Second)

	// Verify session is running again
	fmt.Println("\n7. Verifying session is running again...")
	getResult, err = client.GetSession(session.SessionID)
	if err != nil {
		log.Fatalf("Failed to get session status: %v", err)
	}
	if getResult.Success && getResult.Data != nil {
		fmt.Printf("Session status: %s\n", getResult.Data.Status)
	} else {
		log.Fatalf("Failed to get session status: %s", getResult.ErrorMessage)
	}

	// Perform work on the resumed session
	fmt.Println("\n8. Performing work on the resumed session...")
	commandResult, err = session.Command.ExecuteCommand("echo 'Hello from resumed session'", 30000)
	if err != nil {
		log.Printf("Warning: Failed to execute command: %v", err)
	} else if commandResult.Output != "" {
		fmt.Printf("Command output: %s\n", commandResult.Output)
	} else {
		fmt.Println("Command executed successfully")
	}

	fmt.Println("\nExample completed successfully!")
}
