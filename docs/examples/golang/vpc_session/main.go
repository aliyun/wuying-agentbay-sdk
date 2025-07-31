package main

import (
	"fmt"
	"os"
	"time"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

// Basic example of creating and using a VPC session.
// This example demonstrates:
// - Creating a VPC session with specific parameters
// - Using FileSystem operations in a VPC session
// - Using Command execution in a VPC session
// - Proper session cleanup

func main() {
	// Get API key from environment variable
	apiKey := os.Getenv("AGENTBAY_API_KEY")
	if apiKey == "" {
		fmt.Println("Error: AGENTBAY_API_KEY environment variable not set")
		return
	}

	// Initialize AgentBay client
	fmt.Println("Initializing AgentBay client...")
	client, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		fmt.Printf("Error initializing AgentBay client: %v\n", err)
		return
	}

	// Create a VPC session
	fmt.Println("Creating a VPC session...")
	labels := map[string]string{
		"test-type": "vpc-basic-example",
		"purpose":   "demonstration",
		"timestamp": fmt.Sprintf("%d", time.Now().Unix()),
	}
	
	params := agentbay.NewCreateSessionParams().
		WithImageId("imgc-07eksy57nw6r759fb").
		WithIsVpc(true).
		WithLabels(labels)

	sessionResult, err := client.Create(params)
	if err != nil {
		fmt.Printf("Error creating VPC session: %v\n", err)
		return
	}
	
	if !sessionResult.Success {
		fmt.Printf("Failed to create VPC session: %s\n", sessionResult.ErrorMessage)
		return
	}

	session := sessionResult.Session
	fmt.Printf("VPC session created successfully with ID: %s\n", session.SessionID)
	
	// Ensure cleanup
	defer func() {
		fmt.Println("\n--- Cleaning up ---")
		deleteResult, err := client.Delete(session)
		if err != nil {
			fmt.Printf("Error deleting VPC session: %v\n", err)
		} else if deleteResult.Success {
			fmt.Println("✓ VPC session deleted successfully")
		} else {
			fmt.Printf("⚠ Failed to delete VPC session: %s\n", deleteResult.ErrorMessage)
		}
	}()

	// Test FileSystem operations
	fmt.Println("\n--- Testing FileSystem operations ---")
	testFilePath := "/tmp/vpc_example_test.txt"
	testContent := fmt.Sprintf("Hello from VPC session! Created at %s", time.Now().Format(time.RFC3339))

	// Write file
	writeResult, err := session.FileSystem.WriteFile(testFilePath, testContent)
	if err != nil {
		fmt.Printf("Error writing file: %v\n", err)
	} else if writeResult.Success {
		fmt.Println("✓ File written successfully")
	} else {
		fmt.Printf("⚠ File write failed: %s\n", writeResult.ErrorMessage)
	}

	// Read file
	readResult, err := session.FileSystem.ReadFile(testFilePath)
	if err != nil {
		fmt.Printf("Error reading file: %v\n", err)
	} else if readResult.Success {
		fmt.Printf("✓ File read successfully. Content: %s\n", readResult.Content)
	} else {
		fmt.Printf("⚠ File read failed: %s\n", readResult.ErrorMessage)
	}

	// Test Command operations
	fmt.Println("\n--- Testing Command operations ---")

	// Get current user
	cmdResult, err := session.Command.ExecuteCommand("whoami")
	if err != nil {
		fmt.Printf("Error executing command: %v\n", err)
	} else if cmdResult.Success {
		fmt.Printf("✓ Current user: %s\n", cmdResult.Output)
	} else {
		fmt.Printf("⚠ Command execution failed: %s\n", cmdResult.ErrorMessage)
	}

	// List directory contents
	lsResult, err := session.Command.ExecuteCommand("ls -la /tmp")
	if err != nil {
		fmt.Printf("Error executing command: %v\n", err)
	} else if lsResult.Success {
		fmt.Println("✓ Directory listing successful")
		fmt.Printf("  Output:\n%s\n", lsResult.Output)
	} else {
		fmt.Printf("⚠ Directory listing failed: %s\n", lsResult.ErrorMessage)
	}
}