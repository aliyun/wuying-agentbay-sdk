//go:build ignore
// +build ignore

/**
 * Example demonstrating Browser Launch with Custom Command Arguments and
 * go to Default Navigation URL with AgentBay SDK.
 *
 * This example shows how to configure browser with custom command arguments
 * and go to default navigation URL:
 * - Create AIBrowser session with custom command arguments and go to default navigation URL
 * - Use playwright to connect to AIBrowser instance through CDP protocol
 * - Verify the browser navigated to the default URL
 * - Test custom command arguments effects
 */

package main

import (
	"fmt"
	"log"
	"os"
	"time"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/browser"
)

func main() {
	// Get API key from environment variable
	apiKey := os.Getenv("AGENTBAY_API_KEY")
	if apiKey == "" {
		log.Fatal("AGENTBAY_API_KEY environment variable is required")
	}

	// Initialize AgentBay client
	fmt.Println("Initializing AgentBay client...")
	agentBay, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		log.Fatalf("Error initializing AgentBay client: %v", err)
	}

	// Create session parameters
	fmt.Println("Creating a new session...")
	params := agentbay.NewCreateSessionParams().WithImageId("linux_latest")

	// Create a new session
	sessionResult, err := agentBay.Create(params)
	if err != nil {
		log.Fatalf("Error creating session: %v", err)
	}

	session := sessionResult.Session
	fmt.Printf("Session created with ID: %s\n", session.SessionID)
	fmt.Printf("Resource URL: %s\n", session.ResourceUrl)

	// Defer session cleanup
	defer func() {
		fmt.Println("Cleaning up session...")
		if _, err := session.Delete(); err != nil {
			log.Printf("Warning: Error deleting session: %v", err)
		} else {
			fmt.Println("Session deleted successfully")
		}
	}()

	// Create browser option with user defined cmd args and default navigate url
	browserOption := browser.NewBrowserOption()
	browserOption.CmdArgs = []string{"--disable-features=PrivacySandboxSettings4"}
	defaultUrl := "chrome://version/"
	browserOption.DefaultNavigateUrl = &defaultUrl

	fmt.Println("Browser configuration:")
	fmt.Printf("- Command arguments: %v\n", browserOption.CmdArgs)
	if browserOption.DefaultNavigateUrl != nil {
		fmt.Printf("- Default navigate URL: %s\n", *browserOption.DefaultNavigateUrl)
	}

	// Initialize browser
	fmt.Println("Initializing browser...")
	success, err := session.Browser.Initialize(browserOption)
	if err != nil {
		log.Fatalf("Failed to initialize browser: %v", err)
	}

	if success {
		fmt.Println("Browser initialized successfully")
	} else {
		log.Fatal("Browser initialization failed")
	}

	// Wait for some time to do user interaction
	fmt.Println("Waiting for 20 seconds...")
	time.Sleep(20 * time.Second)

	// Destroy browser
	fmt.Println("Destroying browser...")
	err = session.Browser.Destroy()
	if err != nil {
		log.Fatalf("Failed to destroy browser: %v", err)
	}
	fmt.Println("Browser destroyed successfully")

	fmt.Println("\n=== Browser Default Navigation Example Completed ===")
}
