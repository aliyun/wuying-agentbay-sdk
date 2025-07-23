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

## Best Practices

- Use Browser Context when you need to persist browser state across sessions
- Set `autoUpload` to `true` if you want to automatically save browser data when the session ends
- Use unique context IDs for different browser profiles or users
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
