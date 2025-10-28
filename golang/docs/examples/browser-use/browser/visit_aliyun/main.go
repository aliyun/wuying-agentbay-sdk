package main

import (
	"fmt"
	"log"
	"os"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/browser"
	"github.com/playwright-community/playwright-go"
)

func main() {
	// Get API key from environment variable
	apiKey := os.Getenv("AGENTBAY_API_KEY")
	if apiKey == "" {
		log.Fatal("AGENTBAY_API_KEY environment variable not set")
	}

	// Initialize AgentBay client
	agentBay := agentbay.NewAgentBay(apiKey)

	// Create a session with browser image
	params := &agentbay.CreateSessionParams{
		ImageId: "browser_latest",
	}

	fmt.Println("Creating session...")
	sessionResult, err := agentBay.Create(params)
	if err != nil {
		log.Fatalf("Failed to create session: %v", err)
	}
	if !sessionResult.Success {
		log.Fatalf("Failed to create session: %s", sessionResult.ErrorMessage)
	}

	session := sessionResult.Session
	fmt.Printf("Session created: %s\n", session.GetSessionID())
	defer func() {
		fmt.Println("Deleting session...")
		session.Delete()
	}()

	// Initialize browser with default options
	fmt.Println("Initializing browser...")
	option := browser.NewBrowserOption()

	ok, err := session.Browser.Initialize(option)
	if err != nil {
		log.Fatalf("Browser initialization failed: %v", err)
	}
	if !ok {
		log.Fatal("Browser initialization returned false")
	}

	// Get CDP endpoint URL
	endpointURL, err := session.Browser.GetEndpointURL()
	if err != nil {
		log.Fatalf("Failed to get endpoint URL: %v", err)
	}
	fmt.Printf("Browser CDP endpoint: %s\n", endpointURL)

	// Connect Playwright over CDP
	fmt.Println("Starting Playwright...")
	pw, err := playwright.Run()
	if err != nil {
		log.Fatalf("Failed to start Playwright: %v", err)
	}
	defer pw.Stop()

	fmt.Println("Connecting to browser over CDP...")
	browserInstance, err := pw.Chromium.ConnectOverCDP(endpointURL)
	if err != nil {
		log.Fatalf("Failed to connect over CDP: %v", err)
	}
	defer browserInstance.Close()

	// Get existing browser context
	contexts := browserInstance.Contexts()
	if len(contexts) == 0 {
		log.Fatal("No browser contexts available")
	}
	context := contexts[0]

	// Create a new page
	page, err := context.NewPage()
	if err != nil {
		log.Fatalf("Failed to create new page: %v", err)
	}

	// Navigate to Aliyun
	fmt.Println("Navigating to https://www.aliyun.com...")
	_, err = page.Goto("https://www.aliyun.com")
	if err != nil {
		log.Fatalf("Failed to navigate: %v", err)
	}

	// Get and print page title
	title, err := page.Title()
	if err != nil {
		log.Fatalf("Failed to get title: %v", err)
	}
	fmt.Printf("Page title: %s\n", title)

	// Take a screenshot (optional)
	fmt.Println("Taking screenshot...")
	_, err = page.Screenshot(playwright.PageScreenshotOptions{
		Path: playwright.String("aliyun_screenshot.png"),
	})
	if err != nil {
		log.Printf("Warning: Failed to take screenshot: %v", err)
	} else {
		fmt.Println("Screenshot saved to aliyun_screenshot.png")
	}

	fmt.Println("Browser automation completed successfully!")
}

