# Call For User

The Call For User feature handles scenarios where browser automation encounters situations that require human intervention. This includes authentication challenges, complex verification processes, or security measures that cannot be automatically resolved by the system.

> **Use Cases:** This feature is triggered when the browser encounters user information requests, authentication challenges, or other scenarios that require manual human interaction to proceed.

## When Call For User is Triggered

The system automatically triggers a "wuying-call-for-user" message when it encounters:

- **Authentication challenges** that cannot be automatically resolved
- **Complex verification processes** that need user input
- **Security measures** that require manual verification
- **User information requests** that need human intervention
- **Situations** where automated solutions are insufficient

## Event Monitoring

Monitor Call For User events through console messages to implement custom handling logic:

```python
def handle_console(msg):
    print(f"🔍 Received console message: {msg.text}")
    
    # Parse JSON message
    try:
        message_data = json.loads(msg.text)
        message_type = message_data.get('type', '')
        print(f"📋 Parsed message type: {message_type}")
    except (json.JSONDecodeError, AttributeError):
        # If not JSON, treat as plain text
        message_type = msg.text
        print(f"📋 Plain text message: {message_type}")

    if message_type == "wuying-call-for-user":
        print("📞 Received wuying-call-for-user message")
        print(f"session resource url is {info.resource_url}")
        # Open browser for user interaction
        import webbrowser
        print("🌐 Opening browser with session resource URL...")
        webbrowser.open(info.resource_url)
        # Wait for user to complete interaction
        print("⏳ Starting 20 second wait for user interaction...")
        time.sleep(20)

page.on("console", handle_console)
```

## Handling User Intervention

When a Call For User event is triggered, the recommended flow is:

1. **Parse the console message** to identify the message type (JSON or plain text)
2. **Detect the "wuying-call-for-user" message** from the parsed message type
3. **Open the session resource URL** in a browser for user interaction
4. **Allow the user to interact** with the browser to complete the required action
5. **Wait for completion** (typically 20-30 seconds using `time.sleep()`)
6. **Continue with automation** flow after user completes the interaction

## Complete Example

Here's a complete example demonstrating the Call For User feature:

```python
import os
import time
import json
from agentbay import AgentBay, CreateSessionParams, BrowserOption
from playwright.sync_api import sync_playwright

# Get API key from environment variable
api_key = os.getenv("AGENTBAY_API_KEY")
agent_bay = AgentBay(api_key=api_key)

# Create a session
params = CreateSessionParams(
    image_id="browser_latest",
)
session_result = agent_bay.create(params)

if session_result.success:
    session = session_result.session
    print(f"Session created with ID: {session.session_id}")
    
    if session.browser.initialize(BrowserOption()):
        print("Browser initialized successfully")
        endpoint_url = session.browser.get_endpoint_url()
        
        # Get session info to access resource URL
        result = session.info()
        info = result.data
        print(f"session resource url is {info.resource_url}")

        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp(endpoint_url)
            context = browser.contexts[0]
            page = context.new_page()
            
            # Navigate to target site
            page.goto("https://www.jd.com/")

            # Listen for console messages
            def handle_console(msg):
                print(f"🔍 Received console message: {msg.text}")
                
                # Parse JSON message
                try:
                    message_data = json.loads(msg.text)
                    message_type = message_data.get('type', '')
                    print(f"📋 Parsed message type: {message_type}")
                except (json.JSONDecodeError, AttributeError):
                    # If not JSON, treat as plain text
                    message_type = msg.text
                    print(f"📋 Plain text message: {message_type}")

                if message_type == "wuying-call-for-user":
                    print("📞 Received wuying-call-for-user message")
                    print(f"session resource url is {info.resource_url}")
                    import webbrowser
                    print("🌐 Opening browser with session resource URL...")
                    webbrowser.open(info.resource_url)
                    print("⏳ Starting 20 second wait for user interaction...")
                    time.sleep(20)

            page.on("console", handle_console)

            # Trigger login action that may require user intervention
            time.sleep(5)
            page.click('.link-login')
            time.sleep(25)
            
            print("Test completed")
            browser.close()
```

## Usage Tips

- **Monitor console events** using `page.on("console", handle_console)` to detect when user intervention is needed
- **Parse both JSON and plain text** messages to handle different message formats
- **Use `webbrowser.open()`** to open the session resource URL in the user's default browser
- **Implement proper waiting** mechanisms using `time.sleep(20)` (20-30 seconds) for user interaction
- **Provide clear feedback** with print statements to inform users about what action is required
- **Plan for user interaction time** in your automation workflows
- **Connect via CDP protocol** using Playwright's `connect_over_cdp()` method for browser control


## 📚 Related Guides

- [CAPTCHA Resolution](captcha.md) - Automatic CAPTCHA handling
- [Session Management](../../common-features/basics/session-management.md) - Session lifecycle and configuration
- [Browser Use Overview](../README.md) - Complete browser automation features

## 🆘 Getting Help

- [GitHub Issues](https://github.com/aliyun/wuying-agentbay-sdk/issues)
- [Documentation Home](../../README.md)
