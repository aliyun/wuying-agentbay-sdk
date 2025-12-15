package integration

import (
	"fmt"
	"os"
	"strings"
	"testing"
	"time"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/browser"
	"github.com/playwright-community/playwright-go"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

// TestBrowserReplay_Integration tests browser session with browser recording enabled
func TestBrowserReplay_Integration(t *testing.T) {
	// Get API Key
	apiKey := os.Getenv("AGENTBAY_API_KEY")
	if apiKey == "" {
		t.Fatal("AGENTBAY_API_KEY environment variable is not set")
	}
	fmt.Printf("api_key = %s\n", apiKey)

	// Initialize AgentBay client
	agentBay, err := agentbay.NewAgentBay(apiKey, nil)
	require.NoError(t, err)
	require.NotNil(t, agentBay)

	// Create session with browser recording enabled
	fmt.Println("Creating a new session for browser recording testing...")
	params := agentbay.NewCreateSessionParams().
		WithImageId("browser_latest").
		WithEnableBrowserReplay(true) // Enable browser recording

	fmt.Println("Creating session with browser recording enabled...")
	sessionResult, err := agentBay.Create(params)
	require.NoError(t, err)
	require.NotNil(t, sessionResult)
	require.True(t, sessionResult.Success)
	require.NotNil(t, sessionResult.Session)

	session := sessionResult.Session
	fmt.Printf("Session created with ID: %s\n", session.SessionID)

	// Get session info
	infoResult, err := session.Info()
	require.NoError(t, err)
	require.NotNil(t, infoResult)

	fmt.Println("=== Session Info Details ===")
	if infoResult.Info != nil {
		info := infoResult.Info
		fmt.Printf("session_id: %s\n", info.SessionId)
		fmt.Printf("resource_url: %s\n", info.ResourceUrl)
		if info.AppId != "" {
			fmt.Printf("app_id: %s\n", info.AppId)
		}
		if info.AuthCode != "" {
			fmt.Printf("auth_code: %s\n", info.AuthCode)
		}
		if info.ConnectionProperties != "" {
			fmt.Printf("connection_properties: %s\n", info.ConnectionProperties)
		}
		if info.ResourceId != "" {
			fmt.Printf("resource_id: %s\n", info.ResourceId)
		}
		if info.ResourceType != "" {
			fmt.Printf("resource_type: %s\n", info.ResourceType)
		}
		if info.Ticket != "" {
			fmt.Printf("ticket: %s\n", info.Ticket)
		}
	} else {
		fmt.Printf("Failed to get session info: info is nil\n")
	}
	fmt.Println("=== End Session Info Details ===")

	// Verify EnableBrowserReplay is set
	assert.True(t, session.EnableBrowserReplay, "EnableBrowserReplay should be true")

	// Test browser operations with recording enabled
	t.Run("Browser record operations", func(t *testing.T) {
		browserInstance := session.Browser
		require.NotNil(t, browserInstance)

		// Initialize browser
		fmt.Println("Initializing browser for operations test...")
		browserOption := browser.NewBrowserOption()
		initResult, err := browserInstance.Initialize(browserOption)
		require.NoError(t, err)
		require.True(t, initResult, "Browser initialization should succeed")

		// Get endpoint URL
		endpointURL, err := browserInstance.GetEndpointURL()
		require.NoError(t, err)
		require.NotEmpty(t, endpointURL, "Browser endpoint URL should not be empty")
		fmt.Printf("Browser endpoint URL: %s\n", endpointURL)

		// Wait for browser to be ready
		time.Sleep(5 * time.Second)

		// Connect to browser using Playwright with retry logic
		fmt.Println("Connecting to browser via Playwright...")
		maxRetries := 3
		retryDelay := 2 * time.Second

		var playwrightBrowser playwright.Browser
		var pw *playwright.Playwright

		for attempt := 0; attempt < maxRetries; attempt++ {
			fmt.Printf("Attempting to connect (attempt %d/%d)...\n", attempt+1, maxRetries)

			// Start Playwright
			pw, err = playwright.Run()
			if err != nil {
				t.Fatalf("Failed to start Playwright: %v", err)
			}

			// Connect to browser with timeout
			playwrightBrowser, err = pw.Chromium.ConnectOverCDP(endpointURL)
			if err != nil {
				errorMsg := err.Error()
				fmt.Printf("Connection attempt %d failed: %s\n", attempt+1, errorMsg)

				// Check if it's a retryable error
				isRetryable := false
				retryableKeywords := []string{"ebadf", "connection", "timeout", "network", "websocket"}
				errorMsgLower := strings.ToLower(errorMsg)
				for _, keyword := range retryableKeywords {
					if strings.Contains(errorMsgLower, keyword) {
						isRetryable = true
						break
					}
				}

				if attempt < maxRetries-1 && isRetryable {
					fmt.Printf("Retrying in %v...\n", retryDelay)
					time.Sleep(retryDelay)
					retryDelay *= 2 // Exponential backoff
					_ = pw.Stop()   // Clean up before retry
					continue
				} else {
					_ = pw.Stop()
					t.Fatalf("Failed to connect after %d attempts: %v", attempt+1, err)
				}
			}

			// Connection successful
			fmt.Println("Browser connected successfully")
			break
		}

		// Ensure cleanup
		defer func() {
			if playwrightBrowser != nil {
				_ = playwrightBrowser.Close()
			}
			if pw != nil {
				_ = pw.Stop()
			}
		}()

		// Get the default context
		contexts := playwrightBrowser.Contexts()
		require.NotEmpty(t, contexts, "Should have at least one context")
		defaultContext := contexts[0]

		// Create a new page
		page, err := defaultContext.NewPage()
		require.NoError(t, err)
		fmt.Println("New page created")

		// Navigate to a test website
		fmt.Println("Navigating to Baidu...")
		_, err = page.Goto("http://www.baidu.com", playwright.PageGotoOptions{
			Timeout: playwright.Float(30000),
		})
		require.NoError(t, err)
		time.Sleep(3 * time.Second) // Wait for page to load

		// Get page title
		pageTitle, err := page.Title()
		require.NoError(t, err)
		fmt.Printf("page.title() = %s\n", pageTitle)
		assert.NotEmpty(t, pageTitle, "Page title should not be empty")

		// Perform some browser operations that will be recorded
		fmt.Println("Performing browser operations for recording...")

		// Take a screenshot
		screenshotPath := "/tmp/test_screenshot.png"
		_, err = page.Screenshot(playwright.PageScreenshotOptions{
			Path: playwright.String(screenshotPath),
		})
		if err == nil {
			fmt.Printf("Screenshot saved to %s\n", screenshotPath)
		} else {
			fmt.Printf("Screenshot failed (acceptable for recording test): %v\n", err)
		}

		// Try to interact with the page
		err = page.WaitForLoadState(playwright.PageWaitForLoadStateOptions{
			State:   playwright.LoadStateNetworkidle,
			Timeout: playwright.Float(10000),
		})
		if err == nil {
			// Try to find and interact with search input
			searchSelectors := []string{"#kw", "input[name='wd']", "input[type='text']"}
			var searchInput playwright.Locator

			for _, selector := range searchSelectors {
				searchInput = page.Locator(selector).First()
				if count, _ := searchInput.Count(); count > 0 {
					visible, _ := searchInput.IsVisible()
					if visible {
						fmt.Printf("Found search input with selector: %s\n", selector)
						break
					}
				}
			}

			if searchInput != nil {
				err = searchInput.Fill("AgentBay测试")
				if err == nil {
					fmt.Println("Filled search input")
					time.Sleep(1 * time.Second)

					// Try to find and click search button
					buttonSelectors := []string{"#su", "input[type='submit']", "button[type='submit']"}
					for _, btnSelector := range buttonSelectors {
						searchButton := page.Locator(btnSelector).First()
						if count, _ := searchButton.Count(); count > 0 {
							visible, _ := searchButton.IsVisible()
							if visible {
								err = searchButton.Click()
								if err == nil {
									fmt.Println("Clicked search button")
									time.Sleep(2 * time.Second)
									break
								}
							}
						}
					}
				}
			} else {
				fmt.Println("Search input not found, performing simple navigation instead")
				// Just scroll the page to demonstrate interaction
				_, _ = page.Evaluate("window.scrollTo(0, 500)")
				time.Sleep(1 * time.Second)
				_, _ = page.Evaluate("window.scrollTo(0, 0)")
			}
		} else {
			fmt.Printf("Page interaction failed, but that's okay for recording test: %v\n", err)
		}

		// Wait a bit more to ensure recording captures all operations
		time.Sleep(2 * time.Second)

		// Close the page
		err = page.Close()
		if err == nil {
			fmt.Println("Page closed")
		}

		fmt.Println("Browser operations completed successfully with recording")
	})

	// Note: In Go tests, we don't have a tearDown equivalent that waits for Ctrl+C
	// Instead, we'll use defer to clean up, but add a sleep to keep session alive for inspection
	fmt.Println("\nTest completed. Session will be kept alive for 10 seconds before deletion.")
	fmt.Println("You can inspect the session during this time.")
	time.Sleep(10 * time.Second)

	// Clean up session
	fmt.Println("Cleaning up: Deleting the session...")
	deleteResult, err := agentBay.Delete(session, false)
	if err != nil {
		t.Logf("Warning: Failed to delete session: %v", err)
	} else if deleteResult != nil {
		if deleteResult.Success {
			fmt.Println("Session deleted successfully")
		} else {
			fmt.Printf("Warning: Error deleting session: %s\n", deleteResult.ErrorMessage)
		}
	}
}
