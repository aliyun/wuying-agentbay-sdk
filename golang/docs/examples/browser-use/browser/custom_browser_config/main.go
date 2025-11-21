//go:build ignore
// +build ignore

package main

import (
	"fmt"
	"log"
	"os"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/browser"
	"github.com/playwright-community/playwright-go"
)

const CUSTOM_UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"

func main() {
	apiKey := os.Getenv("AGENTBAY_API_KEY")
	if apiKey == "" {
		log.Fatal("AGENTBAY_API_KEY environment variable not set")
	}

	// First, authenticate
	agentBay, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		log.Fatalf("Failed to create AgentBay client: %v", err)
	}

	// Then, provision a browser-ready session
	params := &agentbay.CreateSessionParams{
		ImageId: "browser_latest",
	}

	fmt.Println("Creating session...")
	result, err := agentBay.Create(params)
	if err != nil || !result.Success {
		log.Fatalf("Failed to create session: %v", err)
	}

	session := result.Session
	fmt.Printf("Session created: %s\n", session.GetSessionID())
	defer func() {
		fmt.Println("Deleting session...")
		session.Delete()
	}()

	// After that, define how the browser should look and feel
	fmt.Println("Initializing browser with custom configuration...")
	option := browser.NewBrowserOption()

	// Present ourselves with a custom identity
	customUA := CUSTOM_UA
	option.UserAgent = &customUA

	// Stand on a stage sized like a common laptop
	option.Viewport = &browser.BrowserViewport{
		Width:  1366,
		Height: 768,
	}

	// Optionally set screen dimensions (usually same as viewport)
	option.Screen = &browser.BrowserScreen{
		Width:  1366,
		Height: 768,
	}

	// Optionally choose browser type (chrome or chromium)
	// chromeType := "chrome"
	// option.BrowserType = &chromeType

	ok, err := session.Browser.Initialize(option)
	if err != nil || !ok {
		log.Fatalf("Browser initialization failed: %v", err)
	}

	// Now, discover the CDP doorway
	endpointURL, err := session.Browser.GetEndpointURL()
	if err != nil {
		log.Fatalf("Failed to get endpoint URL: %v", err)
	}

	// Step through and take control
	fmt.Println("Connecting to browser over CDP...")
	pw, err := playwright.Run()
	if err != nil {
		log.Fatalf("Failed to start Playwright: %v", err)
	}
	defer pw.Stop()

	browserInstance, err := pw.Chromium.ConnectOverCDP(endpointURL)
	if err != nil {
		log.Fatalf("Failed to connect over CDP: %v", err)
	}
	defer browserInstance.Close()

	context := browserInstance.Contexts()[0]
	page, err := context.NewPage()
	if err != nil {
		log.Fatalf("Failed to create page: %v", err)
	}

	// Navigate to a site that shows our user agent
	fmt.Println("Navigating to user agent detection site...")
	_, err = page.Goto("https://www.whatismybrowser.com/detect/what-is-my-user-agent")
	if err != nil {
		log.Fatalf("Failed to navigate: %v", err)
	}

	// Verify our new voice and our new stage
	fmt.Println("\nVerifying browser configuration:")

	ua, err := page.Evaluate("navigator.userAgent")
	if err != nil {
		log.Fatalf("Failed to get user agent: %v", err)
	}
	fmt.Printf("Effective UA: %v\n", ua)

	w, err := page.Evaluate("window.innerWidth")
	if err != nil {
		log.Fatalf("Failed to get window width: %v", err)
	}

	h, err := page.Evaluate("window.innerHeight")
	if err != nil {
		log.Fatalf("Failed to get window height: %v", err)
	}
	fmt.Printf("Viewport: %v x %v\n", w, h)

	// Get screen dimensions
	screenWidth, err := page.Evaluate("window.screen.width")
	if err != nil {
		log.Fatalf("Failed to get screen width: %v", err)
	}

	screenHeight, err := page.Evaluate("window.screen.height")
	if err != nil {
		log.Fatalf("Failed to get screen height: %v", err)
	}
	fmt.Printf("Screen: %v x %v\n", screenWidth, screenHeight)

	fmt.Println("\nBrowser configuration verified successfully!")
}
