package main

import (
	"fmt"
	"os"
	"strings"

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

	// Create a new session with default parameters
	fmt.Println("\nCreating a new session...")
	session, err := agentBay.Create(nil)
	if err != nil {
		fmt.Printf("\nError creating session: %v\n", err)
		os.Exit(1)
	}
	fmt.Printf("\nSession created with ID: %s\n", session.SessionID)

	// List Sessions
	fmt.Println("\nList sessions...")
	sessions, err := agentBay.List()
	if err != nil {
		fmt.Printf("\nError list sessions: %v\n", err)
		os.Exit(1)
	}
	// Extract SessionID list and join as string
	var sessionIDs []string
	for _, session := range sessions {
		sessionIDs = append(sessionIDs, session.SessionID)
	}
	sessionIDsStr := strings.Join(sessionIDs, ", ")
	fmt.Printf("\nList sessions: %s\n", sessionIDsStr)

	// Execute command
	fmt.Println("\nExecute command...")
	response, err := session.Command.ExecuteCommand("ls")
	if err != nil {
		fmt.Printf("Error execute command: %v\n", err)
		os.Exit(1)
	}
	fmt.Println("Execute command result: " + response)

	// Read a file
	fmt.Println("\nReading a file...")
	content, err := session.FileSystem.ReadFile("/etc/hosts")
	if err != nil {
		fmt.Printf("Error reading file: %v\n", err)
	} else {
		fmt.Printf("File content: %s\n", content)
	}

	// Execute ADB shell command (for mobile environments)
	fmt.Println("\nExecute ADB shell command...")
	adbResponse, err := session.Adb.Shell("ls /sdcard")
	if err != nil {
		fmt.Printf("Error execute ADB shell command: %v\n", err)
		os.Exit(1)
	}
	fmt.Println("ADB shell command result: " + adbResponse)

	// Delete the session
	fmt.Println("\nDeleting the session...")
	err = agentBay.Delete(session)
	if err != nil {
		fmt.Printf("Error deleting session: %v\n", err)
		os.Exit(1)
	}
	fmt.Println("Session deleted successfully")

	// List Sessions
	fmt.Println("\nList sessions...")
	sessions, err = agentBay.List()
	if err != nil {
		fmt.Printf("\nError list sessions: %v\n", err)
		os.Exit(1)
	}
	// Extract SessionID list and join as string
	sessionIDs = []string{}
	for _, session := range sessions {
		sessionIDs = append(sessionIDs, session.SessionID)
	}
	sessionIDsStr = strings.Join(sessionIDs, ", ")
	fmt.Printf("\nList sessions: %s\n", sessionIDsStr)
}
