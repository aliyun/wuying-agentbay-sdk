# Browser Context Synchronization

This tutorial explains how to use AgentBay's Browser Context feature to persist browser data across sessions.

**Note**: BrowserContext is currently only available in Python and TypeScript SDKs. It is not supported in the Golang SDK.

## Overview

The Browser Context feature allows you to synchronize browser data (such as cookies, local storage, and other browser state) across multiple sessions. This is particularly useful for:

- Maintaining authentication state across sessions
- Preserving browser preferences and settings
- Ensuring consistent user experience in web applications

## Using Browser Context

### Creating a Session with Browser Context

When creating a session, you can specify a Browser Context configuration that defines how browser data should be synchronized.

#### Python

```python
from agentbay import AgentBay
from agentbay.session_params import CreateSessionParams, BrowserContext

# Initialize the SDK
agent_bay = AgentBay(api_key="your_api_key")

# Get or create a persistent context for browser data
context_result = agent_bay.context.get("my-browser-context", create=True)

if context_result.success:
    # Create a Browser Context configuration
    browser_context = BrowserContext(
        context_id=context_result.context.id,
        auto_upload=True  # Automatically upload browser data when session ends
    )
    
    # Create session parameters with the Browser Context
    params = CreateSessionParams()
    params.browser_context = browser_context
    
    # Create a session with Browser Context
    session_result = agent_bay.create(params)
    
    if session_result.success:
        session = session_result.session
        print(f"Session created with ID: {session.session_id} and Browser Context")
```

#### TypeScript

```typescript
import { AgentBay, BrowserContext } from 'wuying-agentbay-sdk';

// Initialize the SDK
const agentBay = new AgentBay({ apiKey: 'your_api_key' });

async function createSessionWithBrowserContext() {
  // Get or create a persistent context for browser data
  const contextResult = await agentBay.context.get('my-browser-context', true);
  
  if (contextResult.success) {
    // Create a Browser Context configuration
    const browserContext: BrowserContext = {
      contextId: contextResult.context.id,
      autoUpload: true  // Automatically upload browser data when session ends
    };
    
    // Create a session with Browser Context
    const sessionResult = await agentBay.create({
      browserContext: browserContext
    });
    
    if (sessionResult.success) {
      const session = sessionResult.session;
      console.log(`Session created with ID: ${session.sessionId} and Browser Context`);
    }
  }
}
```

## How Browser Context Works

Under the hood, when you create a session with a Browser Context, AgentBay automatically:

1. Creates a ContextSync configuration with the specified Browser Context ID
2. Mounts the browser data context to a predetermined path in the session
3. Sets up appropriate synchronization policies based on your AutoUpload setting

This allows for seamless browser data persistence without the need to manually configure complex synchronization settings.

## Browser Context vs. General Context Synchronization

While you can achieve similar results using general Context Synchronization, Browser Context provides a simplified interface specifically optimized for browser data. The main differences are:

| Feature | Browser Context | General Context Synchronization |
|---------|----------------|----------------------------------|
| Ease of use | Simplified API with fewer parameters | More complex with detailed configuration |
| Configuration | Only requires context ID and auto-upload setting | Requires path, policies, and other settings |
| Purpose | Specifically for browser data | General-purpose data persistence |
| Implementation | Automatically handled by the SDK | Manually configured by the developer |

## Complete Example: Cookie Persistence

Here's a comprehensive example demonstrating how to persist cookies across sessions:

### Python Example

```python
import asyncio
import time
from agentbay import AgentBay
from agentbay.session_params import CreateSessionParams, BrowserContext
from agentbay.browser.browser import BrowserOption
from playwright.async_api import async_playwright

async def demonstrate_cookie_persistence():
    # Initialize AgentBay
    agent_bay = AgentBay(api_key="your_api_key")
    
    # Create a persistent context
    context_result = agent_bay.context.get("cookie-demo", create=True)
    context = context_result.context
    
    # Create Browser Context configuration
    browser_context = BrowserContext(context.id, auto_upload=True)
    params = CreateSessionParams(
        image_id="imgc-wucyOiPmeV2Z753lq",
        browser_context=browser_context
    )
    
    # === FIRST SESSION ===
    print("Creating first session...")
    session1 = agent_bay.create(params).session
    
    # Initialize browser and set cookies
    await session1.browser.initialize_async(BrowserOption())
    endpoint_url = session1.browser.get_endpoint_url()
    
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(endpoint_url)
        context_p = browser.contexts[0]
        page = await context_p.new_page()
        
        # Navigate to website first (required for cookie domain)
        await page.goto("https://example.com")
        
        # Add test cookies
        test_cookies = [{
            "name": "user_preference",
            "value": "dark_mode",
            "domain": "example.com",
            "path": "/",
            "expires": int(time.time()) + 3600
        }]
        await context_p.add_cookies(test_cookies)
        print("Cookies set in first session")
        
        await browser.close()
    
    # Delete session with context synchronization (IMPORTANT!)
    print("Deleting first session with sync_context=True...")
    agent_bay.delete(session1, sync_context=True)
    
    # Wait for synchronization
    time.sleep(3)
    
    # === SECOND SESSION ===
    print("Creating second session...")
    session2 = agent_bay.create(params).session
    
    # Initialize browser and check cookies
    await session2.browser.initialize_async(BrowserOption())
    endpoint_url2 = session2.browser.get_endpoint_url()
    
    async with async_playwright() as p:
        browser2 = await p.chromium.connect_over_cdp(endpoint_url2)
        context2 = browser2.contexts[0]
        
        # Check if cookies persisted
        cookies = await context2.cookies()
        cookie_names = [c.get('name') for c in cookies]
        
        if 'user_preference' in cookie_names:
            print("✓ Cookies successfully persisted across sessions!")
        else:
            print("✗ Cookies not found in second session")
        
        await browser2.close()
    
    # Clean up
    agent_bay.delete(session2)
    agent_bay.context.delete(context)

# Run the example
asyncio.run(demonstrate_cookie_persistence())
```

### Key Points for Cookie Persistence

1. **Context Synchronization is Critical**: Always use `sync_context=True` when deleting sessions with browser data:
   ```python
   # Python
   agent_bay.delete(session, sync_context=True)
   ```
   ```typescript
   // TypeScript
   await agentBay.delete(session, true);
   ```

2. **Navigate Before Setting Cookies**: You must navigate to the target domain before setting cookies:
   ```python
   await page.goto("https://example.com")  # Required!
   await context.add_cookies(cookies)
   ```

3. **Wait for Synchronization**: Allow time for context sync to complete:
   ```python
   time.sleep(3)  # Wait after sync_context=True deletion
   ```

## Best Practices

- Use Browser Context when you need to persist browser state across sessions
- Set `autoUpload` to `true` if you want to automatically save browser data when the session ends
- **Always use `sync_context=True`** when deleting sessions with important browser data
- Use unique context IDs for different browser profiles or users
- Navigate to the target domain before setting cookies
- Allow time for context synchronization to complete
- For more advanced use cases or custom synchronization policies, consider using general Context Synchronization instead

## API Reference

### BrowserContext Structure

#### Python
```python
class BrowserContext:
    def __init__(self, context_id: str, auto_upload: bool = True):
        pass
```

| Field | Type | Description |
|-------|------|-------------|
| context_id | str | ID of the browser context to bind to the session |
| auto_upload | bool | Whether to automatically upload browser data when session ends |

#### TypeScript
```typescript
interface BrowserContext {
  contextId: string;
  autoUpload: boolean;
}
```

| Field | Type | Description |
|-------|------|-------------|
| contextId | string | ID of the browser context to bind to the session |
| autoUpload | boolean | Whether to automatically upload browser data when session ends |

### Session Parameter Methods

#### Python
- `CreateSessionParams.browser_context`: Set the browser context configuration

#### TypeScript
- `CreateSessionParams.browserContext`: Set the browser context configuration
- `CreateSessionParams.withBrowserContext(browserContext)`: Fluent method to set browser context
