# Browser Context Guide

Browser Context is a core feature of the AgentBay SDK that enables persistent browser state management across multiple sessions. It allows you to maintain cookies, cache, local storage, and other browser data between sessions, significantly reducing anti-bot friction and speeding up web page navigation.

## Overview

A Browser Context represents a persistent browser environment that stores browser state such as:
- Cookies
- Cache
- Local storage
- Session storage
- Browser preferences
- Installed extensions (when used with Extension Management)

## Key Benefits

1. **Reduced Anti-Bot Friction**: By maintaining browser state, websites recognize your sessions as returning users rather than new visitors
2. **Faster Page Loads**: Cached resources and cookies reduce page load times
3. **Session Continuity**: Continue where you left off across multiple sessions
4. **Consistent User Experience**: Maintain user preferences and settings

## Python Implementation

### Basic Usage

```python
import os
from agentbay import AgentBay
from agentbay import CreateSessionParams, BrowserContext

# Get API key from environment
api_key = os.environ.get("AGENTBAY_API_KEY")
if not api_key:
    print("Error: AGENTBAY_API_KEY environment variable not set")
    return

# Initialize AgentBay client
agent_bay = AgentBay(api_key)

# Create or get a persistent context
context_result = agent_bay.context.get("my-browser-context", create=True)

if not context_result.success or not context_result.context:
    print(f"Failed to create context: {context_result.error_message}")
    return

context = context_result.context
print(f"Context created with ID: {context.id}")

# Create browser session with context
browser_context = BrowserContext(context.id, auto_upload=True)

params = CreateSessionParams(
    image_id="browser_latest",
    browser_context=browser_context
)

session_result = agent_bay.create(params)

if not session_result.success or not session_result.session:
    print(f"Failed to create session: {session_result.error_message}")
    return

session = session_result.session
print(f"Session created with ID: {session.session_id}")
```

### Cookie Persistence Example

```python
import os
import time
from agentbay import AgentBay
from agentbay import CreateSessionParams, BrowserContext
from agentbay import BrowserOption
from playwright.sync_api import sync_playwright

# Get API key from environment
api_key = os.environ.get("AGENTBAY_API_KEY")
if not api_key:
    print("Error: AGENTBAY_API_KEY environment variable not set")
    return

# Initialize AgentBay client
agent_bay = AgentBay(api_key)
print("AgentBay client initialized")

# Create a unique context name
context_name = f"browser-cookie-demo-{int(time.time())}"

# Step 1: Create or get a persistent context
print(f"Creating context '{context_name}'...")
context_result = agent_bay.context.get(context_name, create=True)

if not context_result.success or not context_result.context:
    print(f"Failed to create context: {context_result.error_message}")
    return

context = context_result.context
print(f"Context created with ID: {context.id}")

# Step 2: Create first session with Browser Context
print("Creating first session with Browser Context...")
browser_context = BrowserContext(context.id, auto_upload=True)
params = CreateSessionParams(
    image_id="browser_latest",
    browser_context=browser_context
)

session_result = agent_bay.create(params)
if not session_result.success or not session_result.session:
    print(f"Failed to create first session: {session_result.error_message}")
    return

session1 = session_result.session
print(f"First session created with ID: {session1.session_id}")

# Test data
test_url = "https://www.aliyun.com"
test_domain = "aliyun.com"

# Define test cookies
test_cookies = [
    {
        "name": "demo_cookie_1",
        "value": "demo_value_1",
        "domain": test_domain,
        "path": "/",
        "httpOnly": False,
        "secure": False,
        "expires": int(time.time()) + 3600  # 1 hour from now
    },
    {
        "name": "demo_cookie_2",
        "value": "demo_value_2",
        "domain": test_domain,
        "path": "/",
        "httpOnly": False,
        "secure": False,
        "expires": int(time.time()) + 3600
    }
]

# Step 3: Initialize browser and set cookies
print("Initializing browser and setting test cookies...")
init_success = session1.browser.initialize(BrowserOption())
if not init_success:
    print("Failed to initialize browser")
    return

print("Browser initialized successfully")

# Get endpoint URL
endpoint_url = session1.browser.get_endpoint_url()
if not endpoint_url:
    print("Failed to get browser endpoint URL")
    return

print(f"Browser endpoint URL: {endpoint_url}")

# Connect with Playwright and set cookies
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(endpoint_url)
    cdp_session = browser.new_browser_cdp_session()
    context_p = browser.contexts[0] if browser.contexts else browser.new_context()
    page = context_p.new_page()
    
    # Navigate to test URL first (required before setting cookies)
    page.goto(test_url)
    print(f"Navigated to {test_url}")
    page.wait_for_timeout(2000)
    
    # Add test cookies
    context_p.add_cookies(test_cookies)  # type: ignore
    print(f"Added {len(test_cookies)} test cookies")
    
    # Verify cookies were set
    cookies = context_p.cookies()
    cookie_dict = {cookie.get('name', ''): cookie.get('value', '') for cookie in cookies}
    print(f"Total cookies in first session: {len(cookies)}")
    
    # Check our test cookies
    for test_cookie in test_cookies:
        cookie_name = test_cookie["name"]
        if cookie_name in cookie_dict:
            print(f"✓ Test cookie '{cookie_name}' set successfully: {cookie_dict[cookie_name]}")
        else:
            print(f"✗ Test cookie '{cookie_name}' not found")
    
    cdp_session.send('Browser.close')
    
    # Wait for browser to save cookies to file
    print("Waiting for browser to save cookies to file...")
    time.sleep(2)
    
    browser.close()
    print("First session browser operations completed")

# Step 4: Delete first session with context synchronization
print("Deleting first session with context synchronization...")
delete_result = agent_bay.delete(session1, sync_context=True)

if not delete_result.success:
    print(f"Failed to delete first session: {delete_result.error_message}")
    return

print(f"First session deleted successfully (RequestID: {delete_result.request_id})")

# Wait for context sync to complete
print("Waiting for context synchronization to complete...")
time.sleep(3)

# Step 5: Create second session with same Browser Context
print("Creating second session with same Browser Context...")
session_result2 = agent_bay.create(params)

if not session_result2.success or not session_result2.session:
    print(f"Failed to create second session: {session_result2.error_message}")
    return

session2 = session_result2.session
print(f"Second session created with ID: {session2.session_id}")

# Step 6: Verify cookie persistence
print("Verifying cookie persistence in second session...")

# Initialize browser in second session
init_success2 = session2.browser.initialize(BrowserOption())
if not init_success2:
    print("Failed to initialize browser in second session")
    return

print("Second session browser initialized successfully")

# Get endpoint URL for second session
endpoint_url2 = session2.browser.get_endpoint_url()
if not endpoint_url2:
    print("Failed to get browser endpoint URL for second session")
    return

print(f"Second session browser endpoint URL: {endpoint_url2}")

# Check cookies in second session
with sync_playwright() as p:
    browser2 = p.chromium.connect_over_cdp(endpoint_url2)
    context2 = browser2.contexts[0] if browser2.contexts else browser2.new_context()
    
    # Read cookies directly from context (without opening any page)
    cookies2 = context2.cookies()
    cookie_dict2 = {cookie.get('name', ''): cookie.get('value', '') for cookie in cookies2}
    
    print(f"Total cookies in second session: {len(cookies2)}")
    
    # Check if our test cookies persisted
    expected_cookie_names = {"demo_cookie_1", "demo_cookie_2"}
    found_cookie_names = set(cookie_dict2.keys())
    
    print("Checking test cookie persistence...")
    missing_cookies = expected_cookie_names - found_cookie_names
    
    if missing_cookies:
        print(f"✗ Missing test cookies: {missing_cookies}")
        print("Cookie persistence test FAILED")
    else:
        # Verify cookie values
        all_values_match = True
        for test_cookie in test_cookies:
            cookie_name = test_cookie["name"]
            expected_value = test_cookie["value"]
            actual_value = cookie_dict2.get(cookie_name, "")
            
            if expected_value == actual_value:
                print(f"✓ Cookie '{cookie_name}' persisted correctly: {actual_value}")
            else:
                print(f"✗ Cookie '{cookie_name}' value mismatch. Expected: {expected_value}, Actual: {actual_value}")
                all_values_match = False
        
        if all_values_match:
            print("🎉 Cookie persistence test PASSED! All cookies persisted correctly across sessions.")
        else:
            print("Cookie persistence test FAILED due to value mismatches")
    
    browser2.close()
    print("Second session browser operations completed")

# Step 7: Clean up second session
print("Cleaning up second session...")
delete_result2 = agent_bay.delete(session2)

if delete_result2.success:
    print(f"Second session deleted successfully (RequestID: {delete_result2.request_id})")
else:
    print(f"Failed to delete second session: {delete_result2.error_message}")

# Clean up context
agent_bay.context.delete(context)
print(f"Context '{context_name}' deleted")
```

## TypeScript Implementation

### Basic Usage

```typescript
import { AgentBay, CreateSessionParams, BrowserContext } from 'wuying-agentbay-sdk';

// Initialize AgentBay client
const agentBay = new AgentBay({ apiKey: "your_api_key" });

// Create or get a persistent context
const contextResult = await agentBay.context.get("my-browser-context", true);
const context = contextResult.context;

// Create browser session with context
const browserContext: BrowserContext = {
    contextId: context.id,
    autoUpload: true
};

const params = new CreateSessionParams()
    .withImageId("browser-image-id")
    .withBrowserContext(browserContext);

const sessionResult = await agentBay.create(params);
const session = sessionResult.session;
```

### Cookie Persistence Example

```typescript
import { AgentBay, CreateSessionParams, BrowserContext, BrowserOption } from 'wuying-agentbay-sdk';
import { chromium } from 'playwright';

// Initialize AgentBay
const agentBay = new AgentBay({ apiKey: "your_api_key" });

// Create persistent context
const contextResult = await agentBay.context.get("cookie-demo-context", true);
const context = contextResult.context;

// First session - set cookies
const browserContext: BrowserContext = {
    contextId: context.id,
    autoUpload: true
};

const params = new CreateSessionParams()
    .withImageId("browser-image-id")
    .withBrowserContext(browserContext);

const session1 = (await agentBay.create(params)).session;

// Set cookies in first session
await session1.browser.initializeAsync(new BrowserOption());
const endpointUrl = session1.browser.getEndpointUrl();

const browser = await chromium.connectOverCDP(endpointUrl);
const contextP = browser.contexts()[0] || await browser.newContext();
const page = await contextP.newPage();

// Navigate and set cookies
await page.goto("https://example.com");
await contextP.addCookies([
    {
        name: "session_cookie",
        value: "session_value",
        domain: "example.com",
        path: "/",
    }
]);

await browser.close();

// Delete first session with context sync
await agentBay.delete(session1, true);

// Second session - verify cookies persist
const session2 = (await agentBay.create(params)).session;

// Check cookies in second session
await session2.browser.initializeAsync(new BrowserOption());
const endpointUrl2 = session2.browser.getEndpointUrl();

const browser2 = await chromium.connectOverCDP(endpointUrl2);
const contextP2 = browser2.contexts()[0] || await browser2.newContext();

// Verify cookies persist
const cookies = await contextP2.cookies();
console.log(`Persisted cookies: ${JSON.stringify(cookies)}`);

await browser2.close();
```

## Best Practices

1. **Use Descriptive Context Names**: Name your contexts based on their purpose (e.g., "ecommerce-scraping", "social-media-automation")
2. **Enable Auto Upload**: Set `auto_upload=True` to automatically synchronize browser data when sessions end
3. **Clean Up Resources**: Delete sessions when done to free up cloud resources
4. **Handle Errors Gracefully**: Implement proper error handling for context operations
5. **Reuse Contexts**: Reuse the same context across multiple sessions for continuity

## Advanced Features

### Context Synchronization Policies

You can customize how browser data is synchronized:

```python
from agentbay import SyncPolicy

# Create custom sync policy
policy = SyncPolicy(
    upload=True,
    extract=True,
    white_list=["/cookies.json", "/storage/"],
    black_list=["/cache/large_files/"]
)

# Use with context sync
context_sync = ContextSync.new(
    context_id=context.id,
    path="/browser-data",
    policy=policy
)
```

### Multiple Contexts

You can use multiple contexts for different purposes:

```python
# Create separate contexts for different websites
ecommerce_result = agent_bay.context.get("ecommerce-site", create=True)
if ecommerce_result.success and ecommerce_result.context:
    ecommerce_context = ecommerce_result.context
    print(f"E-commerce context created: {ecommerce_context.id}")

social_result = agent_bay.context.get("social-media", create=True)
if social_result.success and social_result.context:
    social_context = social_result.context
    print(f"Social media context created: {social_context.id}")

# Use different contexts for different sessions
ecommerce_session_params = CreateSessionParams(
    image_id="browser_latest",
    browser_context=BrowserContext(ecommerce_context.id, auto_upload=True)
)

social_session_params = CreateSessionParams(
    image_id="browser_latest",
    browser_context=BrowserContext(social_context.id, auto_upload=True)
)
```

## Error Handling

Common errors and how to handle them:

```python
try:
    # Create context with error checking
    context_result = agent_bay.context.get("my-context", create=True)
    if not context_result.success or not context_result.context:
        print(f"Failed to create context: {context_result.error_message}")
        return
    
    context = context_result.context
    
    # Create session with error checking
    browser_context = BrowserContext(context.id, auto_upload=True)
    params = CreateSessionParams(
        image_id="browser_latest",
        browser_context=browser_context
    )
    
    session_result = agent_bay.create(params)
    if not session_result.success or not session_result.session:
        print(f"Failed to create session: {session_result.error_message}")
        return
    
    session = session_result.session
    
    # Initialize browser with error checking
    init_success = session.browser.initialize(BrowserOption())
    if not init_success:
        print("Failed to initialize browser")
        return
    
    # Get endpoint URL with error checking
    endpoint_url = session.browser.get_endpoint_url()
    if not endpoint_url:
        print("Failed to get browser endpoint URL")
        return
    
    # Your browser operations here...
    
    # Clean up with error checking
    delete_result = agent_bay.delete(session, sync_context=True)
    if not delete_result.success:
        print(f"Failed to delete session: {delete_result.error_message}")
        
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Clean up context
    try:
        if context:
            agent_bay.context.delete(context)
            print("Context deleted")
    except Exception as e:
        print(f"Warning: Failed to delete context: {e}")
```

## 📚 Related Guides

- [Extension Management](extension.md) - Browser extension integration
- [Data Persistence](../../common-features/basics/data-persistence.md) - Broader context management
- [Session Management](../../common-features/basics/session-management.md) - Session lifecycle and configuration
- [Browser Use Overview](../README.md) - Complete browser automation features

## 🆘 Getting Help

- [GitHub Issues](https://github.com/aliyun/wuying-agentbay-sdk/issues)
- [Documentation Home](../../README.md)