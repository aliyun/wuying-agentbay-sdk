# Browser Automation Documentation

This document provides comprehensive guidance on using the browser automation capabilities of the AgentBay SDK, available in Python and TypeScript implementations, now enhanced with Agent integration.

## Overview

Browser automation in AgentBay SDK allows developers to automate web interactions in cloud environments. The implementation provides both traditional browser automation and AI-assisted operations for more intelligent web interactions, including integration with the Agent module for natural language task execution.

## Getting Started

### Prerequisites

To use browser automation, you need:
1. AgentBay SDK installed
2. Valid API key
3. For Playwright integration: Playwright library installed

### Creating a Browser Session

```python
from agentbay import AgentBay
from agentbay.session_params import CreateSessionParams

# Initialize the SDK
agent_bay = AgentBay(api_key="your_api_key")

# Create a session with browser image
params = CreateSessionParams(
    image_id="browser_latest",  # Specify the browser image
)
session_result = agent_bay.create(params)

if session_result.success:
    session = session_result.session
    print(f"Session created with ID: {session.session_id}")
```

```typescript
import { AgentBay, CreateSessionParams } from 'wuying-agentbay-sdk';

// Initialize the SDK
const agentBay = new AgentBay({ apiKey: 'your_api_key' });

// Create a session with browser image
async function createBrowserSession() {
  const params: CreateSessionParams = {
    imageId: "browser_latest",
  };
  const sessionResult = await agentBay.create(params);
  
  if (sessionResult.success) {
    const session = sessionResult.session;
    console.log(`Session created with ID: ${session.sessionId}`);
    return session;
  }
}
```

## Browser Initialization

After creating a session, initialize the browser:

```python
from agentbay.browser.browser import BrowserOption

# Initialize browser
if await session.browser.initialize_async(BrowserOption()):
    print("Browser initialized successfully")
    endpoint_url = session.browser.get_endpoint_url()
    print("Browser endpoint URL:", endpoint_url)
```

```typescript
import { BrowserOption } from 'wuying-agentbay-sdk';

// Initialize browser with default options
const initialized = await session.browser.initializeAsync(new BrowserOption());
if (initialized) {
  console.log("Browser initialized successfully");
  const endpointUrl = await session.browser.getEndpointUrl();
  console.log("Browser endpoint URL:", endpointUrl);
}
```

## Playwright Integration

The SDK integrates seamlessly with Playwright for advanced browser automation:

```python
from playwright.async_api import async_playwright

async with async_playwright() as p:
    # Connect to the browser
    browser = await p.chromium.connect_over_cdp(endpoint_url)
    
    # Create a new page
    page = await browser.new_page()
    
    # Navigate to a website
    await page.goto("https://www.example.com")
    print("Page title:", await page.title())
    
    # Perform actions
    await page.click("text=More information...")
    
    # Close the browser
    await browser.close()
```

## AI-Assisted Browser Operations

The SDK provides AI-powered browser operations for more intelligent automation.

### Act Operation

Perform actions based on natural language instructions:

```typescript
// Perform an action
const actOptions: ActOptions = {
  action: "Click the 'Sign In' button",
  timeoutMS: 5000
};

const actResult = await session.browser.agent.act(page, actOptions);
console.log("Action result:", {
  success: actResult.success,
  message: actResult.message,
  action: actResult.action
});
```

### Observe Operation

Identify elements on a page based on descriptions:

```typescript
// Observe elements on the page
const observeOptions: ObserveOptions = {
  instruction: "Find all links and buttons on the page",
  returnActions: 5
};

const [observeSuccess, observations] = await session.browser.agent.observe(page, observeOptions);
console.log("Observe success:", observeSuccess);
console.log("Number of observations:", observations.length);

observations.forEach((obs, index) => {
  console.log(`Observation ${index + 1}:`, {
    selector: obs.selector,
    description: obs.description,
    method: obs.method
  });
});
```

### Extract Operation

Extract structured data from web pages:

```typescript
// Define a schema for extraction
class PageInfo {
  title: string = "";
  url: string = "";
}

// Extract structured data
const extractOptions: ExtractOptions<PageInfo> = {
  instruction: "Extract the page title and URL",
  schema: PageInfo
};

const [extractSuccess, extractedData] = await session.browser.agent.extract(page, extractOptions);
console.log("Extract success:", extractSuccess);
console.log("Extracted data count:", extractedData.length);

extractedData.forEach((data, index) => {
  console.log(`Extracted item ${index + 1}:`, {
    title: data.title,
    url: data.url
  });
});
```

## Agent Module Integration

The Agent module can be used alongside browser automation for enhanced capabilities:

### Executing Browser-Related Tasks

Execute complex tasks that involve browser interactions using natural language:

```python
# Execute a task using the Agent module in a browser session
task_description = "Navigate to wikipedia.org, search for 'Artificial Intelligence', and summarize the first paragraph"
execution_result = session.agent.execute_task(task_description, max_try_times=15)

if execution_result.success:
    print(f"Task completed with status: {execution_result.task_status}")
    print(f"Task ID: {execution_result.task_id}")
else:
    print(f"Task failed: {execution_result.error_message}")
```

```typescript
// Execute a task using the Agent module in a browser session
async function executeBrowserTask() {
  const taskDescription = "Navigate to wikipedia.org, search for 'Artificial Intelligence', and summarize the first paragraph";
  const executionResult = await session.agent.executeTask(taskDescription, 15);

  if (executionResult.success) {
    console.log(`Task completed with status: ${executionResult.taskStatus}`);
    console.log(`Task ID: ${executionResult.taskId}`);
  } else {
    console.log(`Task failed: ${executionResult.errorMessage}`);
  }
}
```

### Monitoring Browser Tasks

Monitor the status of browser-related tasks:

```python
# Get the status of a browser task
task_id = "browser_task_12345"
status_result = session.agent.get_task_status(task_id)

if status_result.success:
    print(f"Task output: {status_result.output}")
else:
    print(f"Failed to get task status: {status_result.error_message}")
```

### Terminating Browser Tasks

Terminate long-running browser tasks when needed:

```python
# Terminate a browser task
task_id = "browser_task_12345"
terminate_result = session.agent.terminate_task(task_id)

if terminate_result.success:
    print(f"Task terminated with status: {terminate_result.task_status}")
else:
    print(f"Failed to terminate task: {terminate_result.error_message}")
```

## Browser Context Synchronization

Browser contexts allow persistence of browser data across sessions:

```python
from agentbay.context_sync import ContextSync, SyncPolicy

# Get or create a persistent context for browser data
context_result = agent_bay.context.get("my-browser-context", create=True)

if context_result.success:
    # Create a Browser Context configuration
    browser_context = BrowserContext(
        context_id=context_result.context.id,
        auto_upload=True  # Automatically upload browser data when session ends
    )
    
    # Create session parameters with the Browser Context
    params = CreateSessionParams(
        image_id="imgc-wucyOiPmeV2Z753lq",  # Browser image ID required for browser sessions
    )
    params.browser_context = browser_context
    
    # Create a session with Browser Context
    session_result = agent_bay.create(params)
    
    if session_result.success:
        session = session_result.session
        
        # Initialize browser with default options
        await session.browser.initialize_async(BrowserOption())
        
        # ... perform browser operations ...
        
        # Clean up session with context synchronization
        agent_bay.delete(session, sync_context=True)
```

```typescript
// Get or create a persistent context for browser data
const contextResult = await agentBay.context.get('my-browser-context', true);

if (contextResult.success) {
  // Create a Browser Context configuration
  const browserContext: BrowserContext = {
    contextId: contextResult.context.id,
    autoUpload: true  // Automatically upload browser data when session ends
  };
  
  // Create session parameters with the Browser Context
  const params = new CreateSessionParams()
    .withImageId("imgc-wucyOiPmeV2Z753lq");  // Browser image ID required for browser sessions
  params.browserContext = browserContext;
  
  // Create a session with Browser Context
  const sessionResult = await agentBay.create(params);
  
  if (sessionResult.success) {
    const session = sessionResult.session;
    
    // Initialize browser with default options
    await session.browser.initializeAsync(new BrowserOption());
    
    // ... perform browser operations ...
    
    // Clean up session with context synchronization
    await agentBay.delete(session, true);  // syncContext = true
  }
}
```

## Best Practices

1. **Resource Management**: Always close browser connections and delete sessions when done
2. **Error Handling**: Implement proper error handling for network and browser operations
3. **Timeouts**: Set appropriate timeouts for browser operations
4. **Context Persistence**: Use browser contexts for maintaining state across sessions
5. **AI Operations**: Use AI-assisted operations for complex or dynamic web interactions
6. **Agent Integration**: Use the Agent module for complex multi-step browser tasks
7. **Task Monitoring**: Monitor long-running Agent tasks and terminate when necessary

## Common Use Cases

1. **Web Scraping**: Extract data from websites with dynamic content
2. **Automated Testing**: Test web applications in cloud environments
3. **User Simulation**: Simulate user interactions for analytics
4. **Content Management**: Automate content updates on web platforms
5. **Data Entry**: Automate form filling and data submission
6. **Intelligent Web Interactions**: Use Agent module for complex web tasks described in natural language

## Troubleshooting

### Connection Issues
- Verify the endpoint URL is correct
- Check network connectivity
- Ensure the session is active

### Browser Initialization Failures
- Confirm the browser image is valid
- Check resource availability
- Verify browser options configuration

### AI Operation Failures
- Ensure clear and specific instructions
- Check that elements exist on the page
- Verify the page has fully loaded

### Agent Task Issues
- Use clear and specific task descriptions
- Increase max_try_times for complex tasks
- Check task status regularly for long-running operations

## API Reference

For detailed API documentation, see:
- [Python Browser API](../api-reference/python/browser.md)
- [TypeScript Browser API](../api-reference/typescript/browser.md)
- [Python Agent API](../api-reference/python/agent.md)
- [TypeScript Agent API](../api-reference/typescript/agent.md)