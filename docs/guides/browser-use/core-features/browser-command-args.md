# Browser Command-Line Arguments Configuration Guide

---

## Overview

Browser Command-Line Arguments is a core feature of the AgentBay SDK that enables developers to customize browser launch parameters and control browser behavior. This functionality allows you to pass custom Chrome/Chromium command-line arguments to fine-tune browser settings, disable specific features, or enable experimental functionality for your automation needs.

## Key Features

### 1. Custom Command-Line Arguments
Configure Chrome/Chromium with specific command-line arguments.

### 2. Default Navigation URL
Set a default URL that the browser navigates to upon initialization.

## Configuration Of BrowserOption

### Command-Line Arguments (`cmdArgs`)
An array of Chrome/Chromium command-line arguments to customize browser behavior.

**Common Examples:**
- `--disable-features=PrivacySandboxSettings4` - Disable privacy sandbox
- `--disable-extensions-http-throttling` - Disable HTTP request throttling for extensions
- `--disable-background-timer-throttling` - Disable background timer throttling to prevent performance issues
- `--password-store=basic` - Use basic password storage instead of system keychain

### Default Navigate URL (`defaultNavigateUrl`)
The URL that the browser automatically navigates to after initialization. For Browser Initialize operations, it's **highly recommended** to use Chrome internal pages (e.g., `chrome://version/`, `chrome://settings/`) or extension pages instead of internet URLs. Navigating to internet pages during initialization may cause timeout of browser launch.


## Python Implementation

```python
import os
import time

from agentbay import AgentBay
from agentbay import CreateSessionParams
from agentbay import BrowserOption
from playwright.sync_api import sync_playwright

def main():
    # Get API key from environment variable
    api_key = os.getenv("AGENTBAY_API_KEY")
    if not api_key:
        print("Error: AGENTBAY_API_KEY environment variable not set")
        return

    # Initialize AgentBay client
    print("Initializing AgentBay client...")
    agent_bay = AgentBay(api_key=api_key)

    # Create a session
    print("Creating a new session...")
    params = CreateSessionParams(
        image_id="linux_latest"
    )
    session_result = agent_bay.create(params)

    if session_result.success:
        session = session_result.session
        print(f"Session created with ID: {session.session_id}")

        # Create browser option with custom command arguments and default navigate URL
        browser_option = BrowserOption(
            cmd_args=["--disable-features=PrivacySandboxSettings4"],
            default_navigate_url="chrome://version/",
        )

        print("Browser configuration:")
        print("- Command arguments:", browser_option.cmd_args)
        print("- Default navigate URL:", browser_option.default_navigate_url)

        if session.browser.initialize(browser_option):
            print("Browser initialized successfully")
            
            # Get browser endpoint URL
            endpoint_url = session.browser.get_endpoint_url()
            print(f"endpoint_url = {endpoint_url}")

            # Use Playwright to connect and validate
            with sync_playwright() as p:
                browser = p.chromium.connect_over_cdp(endpoint_url)
                context = browser.contexts[0]
                page = context.pages[0]

                try:
                    # Check if browser navigated to default URL
                    print("\n--- Check Default Navigation ---")
                    time.sleep(2)  # Wait for navigation
                    current_url = page.url
                    print(f"Current URL: {current_url}")
                    
                    if "chrome://version/" in current_url:
                        print("✓ Browser successfully navigated to default URL")
                    else:
                        print("✗ Browser did not navigate to default URL")

                    # Test command arguments effect by checking Chrome version page
                    if "chrome://version/" in current_url:
                        print("\n--- Check Chrome Version Info ---")
                        version_info = page.evaluate("""
                            () => {
                                const versionElement = document.querySelector('#version');
                                const commandLineElement = document.querySelector('#command_line');
                                return {
                                    version: versionElement ? versionElement.textContent : 'Not found',
                                    commandLine: commandLineElement ? commandLineElement.textContent : 'Not found'
                                };
                            }
                        """)
                        
                        print(f"Chrome Version: {version_info['version']}")
                        print(f"Command Line: {version_info['commandLine']}")
                        
                        if "--disable-features=PrivacySandboxSettings4" in version_info['commandLine']:
                            print("✓ Custom command argument found in browser")
                        else:
                            print("✗ Custom command argument not found in browser")

                    time.sleep(3)
                finally:
                    browser.close()
                    session.browser.destroy()
        else:
            print("Failed to initialize browser")

        # Clean up session
        agent_bay.delete(session)
    else:
        print("Failed to create session", session_result.error_message)

if __name__ == "__main__":
    main()
```

## Go Implementation

```go
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

	// Defer session cleanup
	defer func() {
		fmt.Println("Cleaning up session...")
		if _, err := session.Delete(); err != nil {
			log.Printf("Warning: Error deleting session: %v", err)
		} else {
			fmt.Println("Session deleted successfully")
		}
	}()

	// Create browser option with custom command arguments and default navigate URL
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

	// Wait for some time to allow user interaction
	fmt.Println("Waiting for 20 seconds...")
	time.Sleep(20 * time.Second)

	// Destroy browser
	fmt.Println("Destroying browser...")
	err = session.Browser.Destroy()
	if err != nil {
		log.Fatalf("Failed to destroy browser: %v", err)
	}
	fmt.Println("Browser destroyed successfully")

	fmt.Println("\n=== Browser Command Arguments Example Completed ===")
}
```

## TypeScript Implementation

```typescript
import { AgentBay, CreateSessionParams } from 'wuying-agentbay-sdk';
import { BrowserOption } from 'wuying-agentbay-sdk';
import { chromium } from 'playwright';

async function main(): Promise<void> {
    // Get API key from environment variable
    const apiKey = process.env.AGENTBAY_API_KEY;
    if (!apiKey) {
        console.log('Error: AGENTBAY_API_KEY environment variable not set');
        return;
    }

    try {
        // Initialize AgentBay client
        console.log('Initializing AgentBay client...');
        const agentBay = new AgentBay({ apiKey });

        // Create a session
        console.log('Creating a new session...');
        const params: CreateSessionParams = {
            imageId: 'linux_latest',
        };
        const sessionResult = await agentBay.create(params);

        if (!sessionResult.success) {
            console.log('Failed to create session');
            return;
        }

        const session = sessionResult.session;
        console.log(`Session created with ID: ${session.sessionId}`);

        // Create browser option with custom command arguments and default navigate URL
        const browserOption: BrowserOption = {
            cmdArgs: ['--disable-features=PrivacySandboxSettings4'],
            defaultNavigateUrl: 'chrome://version/',
        };

        console.log('Browser configuration:');
        console.log('- Command arguments:', browserOption.cmdArgs);
        console.log('- Default navigate URL:', browserOption.defaultNavigateUrl);

        const initialized = await session.browser.initializeAsync(browserOption);
        if (initialized) {
            const endpointUrl = await session.browser.getEndpointUrl();
            console.log('endpoint_url =', endpointUrl);

            const browser = await chromium.connectOverCDP(endpointUrl);
            const context = browser.contexts()[0];
            const page = context.pages()[0];

            try {
                // Check if browser navigated to default URL
                console.log('\n--- Check Default Navigation ---');
                await page.waitForTimeout(2000); // Wait for navigation
                const currentUrl = page.url();
                console.log('Current URL:', currentUrl);
                
                if (currentUrl.includes('chrome://version/')) {
                    console.log('✓ Browser successfully navigated to default URL');
                } else {
                    console.log('✗ Browser did not navigate to default URL');
                }

                // Test command arguments effect by checking Chrome version page
                if (currentUrl.includes('chrome://version/')) {
                    console.log('\n--- Check Chrome Version Info ---');
                    const versionInfo = await page.evaluate(() => {
                        const versionElement = document.querySelector('#version');
                        const commandLineElement = document.querySelector('#command_line');
                        return {
                            version: versionElement ? versionElement.textContent : 'Not found',
                            commandLine: commandLineElement ? commandLineElement.textContent : 'Not found'
                        };
                    });
                    
                    console.log('Chrome Version:', versionInfo.version);
                    console.log('Command Line:', versionInfo.commandLine);
                    
                    if (versionInfo.commandLine.includes('--disable-features=PrivacySandboxSettings4')) {
                        console.log('✓ Custom command argument found in browser');
                    } else {
                        console.log('✗ Custom command argument not found in browser');
                    }
                }

                await page.waitForTimeout(3000);
            } finally {
                await browser.close();
            }
            await session.browser.destroy();
        }

        // Clean up session
        await agentBay.delete(session);
    } catch (error) {
        console.error('Error:', error);
    }
}

main().catch(console.error);
```


## Limitations

- **Chrome/Chromium Only**: Command arguments are specific to Chrome/Chromium browsers
- **Platform Differences**: Some arguments may behave differently across operating systems
- **Version Compatibility**: Certain arguments may not be available in all Chrome versions
- **Security Restrictions**: Some arguments may be restricted in certain environments

## 📚 Related Guides

- [Browser Proxy Configuration](browser-proxies.md) - Configure proxy settings for browser sessions
- [Browser Context](browser-context.md) - Browser context management for cookies and sessions
- [Browser Fingerprint](browser-fingerprint.md) - Simulate browser fingerprint feature
- [Browser Use Overview](../README.md) - Complete browser automation features
- [Session Management](../../common-features/basics/session-management.md) - Session lifecycle and configuration

## 🆘 Getting Help

- [GitHub Issues](https://github.com/aliyun/wuying-agentbay-sdk/issues)
- [Documentation Home](../../README.md)
