# Browser Proxy Configuration Guide

---

## Overview

Browser Proxy is a core feature of the AgentBay SDK that enables developers to route browser traffic through proxy servers. This functionality is essential for scenarios requiring IP rotation, geographical distribution, or network anonymization. The AgentBay SDK supports both custom proxy servers and integrated Wuying Proxy Service.

## Key Features

### 1. Custom Proxy Support
Configure your own proxy servers with full control over routing and authentication:
- **Protocol Support**: HTTP, HTTPS, and SOCKS proxies
- **Authentication**: Optional username and password authentication
- **Flexible Configuration**: Support for various proxy server configurations

### 2. Wuying Proxy Service
Leverage Alibaba Cloud's integrated proxy service with advanced management features:
- **Restricted Strategy**: Uses fixed proxy nodes for consistent IP addresses
- **Polling Strategy**: Rotates through a pool of proxy nodes for IP diversity
- **Managed Infrastructure**: No need to maintain your own proxy servers

## Proxy Types and Strategies

### Custom Proxy
Suitable for users who have their own proxy infrastructure or specific proxy requirements.

**Configuration Options:**
- `type`: Set to `"custom"`
- `server`: Proxy server address (required)
- `username`: Authentication username (optional)
- `password`: Authentication password (optional)

### Wuying Proxy
Provided by the Wuying Proxy Service integrated in AgentBay SDK

**Restricted Strategy:**
- Uses fixed proxy nodes
- Provides stable IP addresses
- The IP remains stable for the lifetime of the session.

**Polling Strategy:**
- Rotates through a pool of proxy nodes
- Provides IP diversity for each request
- Suitable for scenarios requiring frequent IP changes
- Configurable pool size via `pollsize` parameter

## Python Implementation

### Basic Usage

```python
import os
from agentbay import AgentBay
from agentbay import CreateSessionParams
from agentbay import BrowserOption, BrowserProxy
from playwright.sync_api import sync_playwright

def main():
    """Main function demonstrating browser proxy functionality."""
    # Get API key from environment variable
    api_key = os.getenv("AGENTBAY_API_KEY")
    if not api_key:
        print("Error: AGENTBAY_API_KEY environment variable not set")
        return

    print("Initializing AgentBay client...")
    agent_bay = AgentBay(api_key=api_key)

    print("Creating new session...")
    params = CreateSessionParams(
        image_id="browser_latest",  # Use latest browser image
    )
    session_result = agent_bay.create(params)

    if session_result.success:
        session = session_result.session
        print(f"Session created successfully, Session ID: {session.session_id}")

        # ==================== Proxy Configuration Examples ====================
        
        # Example 1: Custom Proxy Configuration
        # Suitable for users who have their own proxy servers
        # browser_proxy = BrowserProxy(
        #     proxy_type="custom",           # Proxy type: custom
        #     server="http://127.0.0.1:9090", # Proxy server address (required)
        #     username="username",           # Proxy username (optional)
        #     password="password"            # Proxy password (optional)
        # )

        # Example 2: Wuying Proxy - Polling Strategy
        # Rotates through proxy pool nodes, suitable for scenarios requiring frequent IP switching
        browser_proxy = BrowserProxy(
            proxy_type="wuying",    # Proxy type: wuying proxy
            strategy="polling",     # Strategy: polling
            pollsize=2             # Proxy pool size: 2 nodes
        )

        # Example 3: Wuying Proxy - Restricted Strategy
        # Uses fixed proxy nodes, suitable for scenarios requiring stable IP
        # browser_proxy = BrowserProxy(
        #     proxy_type="wuying",    # Proxy type: wuying proxy
        #     strategy="restricted"   # Strategy: restricted (fixed nodes)
        # )

        # Create browser options with proxy configuration, now only support one proxy
        browser_option = BrowserOption(
            proxies=[browser_proxy]
        )

        # Initialize browser instance
        if session.browser.initialize(browser_option):
            # Get browser CDP connection endpoint
            endpoint_url = session.browser.get_endpoint_url()
            print(f"Browser CDP endpoint: {endpoint_url}")

            # Use Playwright to connect to remote browser instance
            with sync_playwright() as p:
                browser = p.chromium.connect_over_cdp(endpoint_url)
                context = browser.contexts[0]  # Get default browser context
                page = context.new_page()  # Create new page

                # ==================== Verify Proxy IP ====================
                print("\n--- Starting proxy public IP check ---")
                page.goto("https://httpbin.org/ip")  # Visit IP checking service

                try:
                    # Parse JSON response from page content
                    response = page.evaluate("() => JSON.parse(document.body.textContent)")
                    public_ip = response.get("origin", "").strip()
                    print(f"Proxy public IP: {public_ip}")
                except Exception as e:
                    print(f"Failed to get proxy public IP: {e}")
                    public_ip = None
                print("--- Proxy IP check completed ---\n")
                
                # Wait 3 seconds to observe results
                page.wait_for_timeout(3000)
                browser.close()
        else:
            print("Browser initialization failed")

        # Clean up session resources
        print("Cleaning up session...")
        agent_bay.delete(session)
        print("Session cleanup completed")


if __name__ == "__main__":
    main()
```

## TypeScript Implementation

### Basic Usage

```typescript
import { AgentBay, CreateSessionParams } from 'wuying-agentbay-sdk';
import { BrowserOption, BrowserProxy } from 'wuying-agentbay-sdk';
import { chromium } from 'playwright';

interface IpResponse {
    origin: string;
}

async function proxyExample(): Promise<void> {
    // Initialize AgentBay client
    const apiKey = process.env.AGENTBAY_API_KEY;
    if (!apiKey) {
        console.log('Error: AGENTBAY_API_KEY environment variable not set');
        return;
    }

    try {
        const agentBay = new AgentBay({ apiKey });

        // Create a session
        const params: CreateSessionParams = {
            imageId: 'browser_latest',
        };
        const sessionResult = await agentBay.create(params);

        if (!sessionResult.success) {
            console.log('Failed to create session');
            return;
        }

        const session = sessionResult.session;
        console.log(`Session created with ID: ${session.sessionId}`);

        // Example 1: Custom Proxy Configuration
        // const browserProxy: BrowserProxy = {
        //     type: 'custom',
        //     server: 'http://127.0.0.1:9090',
        //     username: 'username',
        //     password: 'password',
        //     toMap: function() {
        //         return {
        //             type: this.type,
        //             server: this.server,
        //             username: this.username,
        //             password: this.password
        //         };
        //     }
        // };

        // Example 2: Wuying Proxy - Polling Strategy
        const browserProxy: BrowserProxy = {
            type: 'wuying',
            strategy: 'polling',
            pollsize: 2,
            toMap: function() {
                return {
                    type: this.type,
                    strategy: this.strategy,
                    pollsize: this.pollsize
                };
            }
        };

        // Example 3: Wuying Proxy - Restricted Strategy
        // const browserProxy: BrowserProxy = {
        //     type: 'wuying',
        //     strategy: 'restricted',
        //     toMap: function() {
        //         return {
        //             type: this.type,
        //             strategy: this.strategy
        //         };
        //     }
        // };

        // Create browser option with proxy configuration
        const browserOption: BrowserOption = {
            proxies: [browserProxy]
        };

        const initialized = await session.browser.initializeAsync(browserOption);
        if (initialized) {
            const endpointUrl = session.browser.getEndpointUrl();
            console.log('endpoint_url =', endpointUrl);

            const browser = await chromium.connectOverCDP(endpointUrl);
            const context = browser.contexts()[0];
            const page = await context.newPage();

            try {
                // Verify proxy IP
                console.log('\n--- Check proxy public IP start ---');
                await page.goto('https://httpbin.org/ip');

                const response = await page.evaluate((): IpResponse => {
                    return JSON.parse(document.body.textContent || '{}');
                });
                const publicIp = response.origin || '';
                console.log('proxy public IP:', publicIp);
                console.log('--- Check proxy public IP end ---');

                await page.waitForTimeout(3000);
            } finally {
                await browser.close();
            }
        }

        // Clean up session
        await agentBay.delete(session);
    } catch (error) {
        console.error('Error:', error);
    }
}

proxyExample().catch(console.error);
```

## Best Practices

### 1. Proxy Selection Strategy

**Custom Proxy Usage:**
- Use when you have existing proxy infrastructure
- Ideal for specific geographic requirements
- Provides full control over proxy configuration

```python
# ✅ Correct - Custom proxy with authentication
custom_proxy = BrowserProxy(
    proxy_type="custom",
    server="http://proxy.example.com:8080",
    username="your_username",
    password="your_password"
)
```

**Wuying Proxy Usage:**
- Use for managed proxy infrastructure
- Choose strategy based on your use case:
  - **Restricted**: For consistent IP requirements
  - **Polling**: For IP rotation needs

```python
# ✅ Correct - Wuying proxy with appropriate strategy
wuying_proxy = BrowserProxy(
    proxy_type="wuying",
    strategy="polling",
    pollsize=3  # Adjust based on your needs
)
```

### 2. Error Handling and Monitoring

```python
def robust_proxy_usage():
    try:
        # Initialize browser with proxy
        if session.browser.initialize(browser_option):
            endpoint_url = session.browser.get_endpoint_url()
            
            with sync_playwright() as p:
                browser = p.chromium.connect_over_cdp(endpoint_url)
                context = browser.contexts[0]
                page = context.new_page()
                
                # Verify proxy is working
                page.goto("https://httpbin.org/ip", timeout=30000)
                
                # Check if proxy is applied
                response = page.evaluate("() => JSON.parse(document.body.textContent)")
                proxy_ip = response.get("origin", "").strip()
                
                if not proxy_ip:
                    raise Exception("Failed to detect proxy IP")
                    
                print(f"Successfully using proxy IP: {proxy_ip}")
                
                browser.close()
        else:
            print("Browser initialization failed - check proxy configuration")
            
    except Exception as e:
        print(f"Proxy configuration error: {e}")
        # Implement fallback logic or retry mechanism
```

## Limitations
- **Single Proxy Support**: Although BrowserOption accepts an array in proxies, only the first proxy is currently applied per session.
- **Global Proxy Scope**: The proxy applies globally, meaning all browser requests will be routed through the proxy

## 📚 Related Guides

- [Browser Context](browser-context.md) - Browser context management for cookies and sessions
- [Browser Fingerprint](browser-fingerprint.md) - Simulate browser fingerprint for web automation
- [Browser Use Overview](../README.md) - Complete browser automation features
- [Session Management](../../common-features/basics/session-management.md) - Session lifecycle and configuration

## 🆘 Getting Help

- [GitHub Issues](https://github.com/aliyun/wuying-agentbay-sdk/issues)
- [Documentation Home](../../README.md)
