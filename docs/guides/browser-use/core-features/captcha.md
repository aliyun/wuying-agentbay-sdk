# CAPTCHA Resolution

CAPTCHA challenges are common obstacles in web automation that can disrupt your workflow. AIBrowser includes an intelligent CAPTCHA resolution system that automatically handles these verification challenges, ensuring your automation tasks proceed smoothly.

> **Version Information:** CAPTCHA resolution is available starting from version 0.7.0. Currently, the system only supports automatic resolution of slider-type CAPTCHAs. Support for text-based CAPTCHAs will be added in future releases.

## Automatic CAPTCHA Resolution

The system works by:
- Detecting CAPTCHA challenges as they appear on web pages
- Processing the challenge using advanced recognition algorithms
- Completing the verification process transparently
- Resolution typically completes within 30 seconds for most CAPTCHA types
- Feature is opt-in and disabled by default for performance optimization

## Configuration

Enable CAPTCHA resolution by setting the appropriate flag during browser initialization:

```python
from agentbay import AgentBay, CreateSessionParams, BrowserOption
from playwright.sync_api import sync_playwright

# Initialize AgentBay client
agent_bay = AgentBay(api_key="your_api_key")

# Create a session
params = CreateSessionParams(
    image_id="browser_latest",
)
session_result = agent_bay.create(params)

if session_result.success:
    session = session_result.session
    
    # Enable CAPTCHA resolution
    browser_option = BrowserOption(
        use_stealth=True,
        solve_captchas=True,
    )
    
    # Initialize browser with CAPTCHA resolution enabled
    if session.browser.initialize(browser_option):
        print("Browser initialized successfully")
        endpoint_url = session.browser.get_endpoint_url()
        
        # Connect with Playwright
        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp(endpoint_url)
            context = browser.contexts[0]
            page = context.new_page()
            
            # Your automation code here
            page.goto("https://example.com")
```

## Event Monitoring

Track CAPTCHA resolution progress through console events. This allows you to implement custom logic while the system handles the verification:

```python
import time

def handle_console(msg):
    if msg.text == "wuying-captcha-solving-started":
        print("🎯 CAPTCHA solving started")
    elif msg.text == "wuying-captcha-solving-finished":
        print("✅ CAPTCHA solving finished")

# Register console event listener
page.on("console", handle_console)

# Trigger action that may encounter CAPTCHA
page.click("#submit_button")

# Wait for CAPTCHA resolution
time.sleep(30)  # Allow time for CAPTCHA processing
```

## Complete Example

Here's a complete example demonstrating CAPTCHA resolution with event monitoring:

```python
import os
import time
from agentbay import AgentBay, CreateSessionParams, BrowserOption
from playwright.sync_api import sync_playwright

# Initialize AgentBay client
api_key = os.getenv("AGENTBAY_API_KEY")
agent_bay = AgentBay(api_key=api_key)

# Create session
params = CreateSessionParams(image_id="browser_latest")
session_result = agent_bay.create(params)

if session_result.success:
    session = session_result.session
    
    # Enable CAPTCHA resolution
    browser_option = BrowserOption(
        use_stealth=True,
        solve_captchas=True,
    )
    
    if session.browser.initialize(browser_option):
        endpoint_url = session.browser.get_endpoint_url()
        
        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp(endpoint_url)
            context = browser.contexts[0]
            page = context.new_page()
            
            # Set up console event listener
            def handle_console(msg):
                if msg.text == "wuying-captcha-solving-started":
                    print("🎯 CAPTCHA processing started")
                elif msg.text == "wuying-captcha-solving-finished":
                    print("✅ CAPTCHA processing finished")
            
            page.on("console", handle_console)
            
            # Navigate and interact with page
            page.goto("https://example.com/login")
            page.fill("#username", "user@example.com")
            page.click("#submit")
            
            # Wait for CAPTCHA resolution if needed
            time.sleep(30)
            
            browser.close()
```

## Usage Tips

- Plan for up to 30 seconds processing time per CAPTCHA
- Implement event listeners to track resolution status
- Disable the feature if manual CAPTCHA handling is preferred for your use case

## 📚 Related Guides

- [Browser Fingerprint](browser-fingerprint.md) - Simulate browser fingerprint for web automation
- [Call For User](call-for-user.md) - Human intervention for unsolvable challenges
- [Browser Use Overview](../README.md) - Complete browser automation features
- [Session Management](../../common-features/basics/session-management.md) - Session lifecycle and configuration

## 🆘 Getting Help

- [GitHub Issues](https://github.com/aliyun/wuying-agentbay-sdk/issues)
- [Documentation Home](../../README.md)
