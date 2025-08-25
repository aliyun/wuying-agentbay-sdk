# Complete Guide to Advanced Features

This guide integrates the advanced features of the AgentBay SDK, including VPC session configuration, Agent modules (AI tasks), browser automation, and integration extensions.

## 📋 Table of Contents

- [VPC Sessions](#vpc-sessions)
- [Agent Modules](#agent-modules)
- [Browser Automation](#browser-automation)
- [Integration and Extensions](#integration-and-extensions)
- [Best Practices](#best-practices)

<a id="vpc-sessions"></a>
## 🔒 VPC Sessions

### VPC Session Overview

VPC (Virtual Private Cloud) sessions provide isolated network environments, suitable for scenarios requiring special network configurations or security requirements.

### Creating VPC Sessions

```python
from agentbay import AgentBay, CreateSessionParams

agent_bay = AgentBay()

# Create VPC session parameters
vpc_params = CreateSessionParams(
    is_vpc=True,
    labels={"environment": "production", "type": "vpc"}
)

# Create VPC session
result = agent_bay.create(vpc_params)
if result.success:
    vpc_session = result.session
    print(f"VPC session created successfully: {vpc_session.session_id}")
else:
    print(f"VPC session creation failed: {result.error_message}")
```

### VPC Session Creation

VPC sessions are created by setting the `is_vpc` parameter to `True` in the `CreateSessionParams`. The actual VPC configuration (VPC ID, subnet ID, security groups, etc.) is managed by the AgentBay platform and does not need to be specified in the SDK.

### VPC Session Benefits

1. **Network Isolation**: Complete network isolation for security-sensitive applications
2. **Custom Network Configuration**: Flexible network topology and routing rules
3. **Resource Access Control**: Fine-grained control over resource access
4. **Compliance**: Meets enterprise security and compliance requirements

### VPC Session Limitations

1. **Regional Restrictions**: VPC sessions are region-specific
2. **Resource Quotas**: Subject to VPC and subnet resource quotas
3. **Network Complexity**: Requires understanding of cloud networking concepts

<a id="agent-modules"></a>
## 🤖 Agent Modules

### Agent Module Overview

Agent modules are specialized AI task execution units that can perform complex operations including:
- Web scraping and data extraction
- Automated testing and QA
- Code generation and review
- Natural language processing
- Image and video analysis

### Creating Agent Sessions

```python
from agentbay import AgentBay, CreateSessionParams

agent_bay = AgentBay()

# Create a session for Agent module usage
agent_params = CreateSessionParams(
    image_id="windows_latest",
    labels={"project": "ai-agent", "type": "web-scraper"}
)

result = agent_bay.create(agent_params)
if result.success:
    agent_session = result.session
    print(f"Session created with ID: {agent_session.session_id}")
else:
    print(f"Session creation failed: {result.error_message}")
```

### Agent Capabilities

#### Task Execution
```python
# Execute a task using natural language
task_description = "Calculate the square root of 144"
execution_result = agent_session.agent.execute_task(task_description, max_try_times=5)

if execution_result.success:
    print("Task completed successfully!")
    print(f"Task ID: {execution_result.task_id}")
    print(f"Task status: {execution_result.task_status}")
else:
    print(f"Task failed: {execution_result.error_message}")
```

### Agent Module Best Practices

1. **Capability Selection**: Only enable required capabilities to optimize performance
2. **Resource Management**: Monitor token usage and set appropriate limits
3. **Error Handling**: Implement robust error handling for AI-generated content
4. **Security**: Validate and sanitize AI-generated code before execution

<a id="browser-automation"></a>
## 🌐 Browser Automation

### Browser Automation Overview

Browser automation enables programmatic control of web browsers for tasks such as:
- Web scraping and data collection
- Automated testing
- User interaction simulation
- Screenshot capture
- PDF generation

### Basic Browser Operations

```python
from agentbay import AgentBay

agent_bay = AgentBay()
session_result = agent_bay.create()
if session_result.success:
    session = session_result.session
    print(f"Session created with ID: {session.session_id}")

    # Initialize browser
    from agentbay.browser.browser import BrowserOption
    if session.browser.initialize(BrowserOption()):
        print("Browser initialized successfully")
        endpoint_url = session.browser.get_endpoint_url()
        print(f"Browser endpoint URL: {endpoint_url}")
        
        # Note: Actual browser automation is done using Playwright
        # See examples/browser/visit_aliyun.py for a complete example
    else:
        print("Failed to initialize browser")
else:
    print(f"Session creation failed: {session_result.error_message}")
```

### Browser Automation Implementation

Browser automation in AgentBay SDK is implemented using Playwright connected through the Chrome DevTools Protocol (CDP). After initializing the browser with `session.browser.initialize()`, you can use Playwright to perform advanced interactions:

```python
# Complete example of browser automation with Playwright
import asyncio
from playwright.async_api import async_playwright

async def browser_automation_example():
    # After initializing the browser as shown in the basic example
    endpoint_url = session.browser.get_endpoint_url()
    
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(endpoint_url)
        page = await browser.new_page()
        
        # Navigate to a webpage
        await page.goto("https://example.com")
        print("Page title:", await page.title())·
        
        # Fill form fields
        await page.fill("#username", "myuser")
        await page.fill("#password", "mypassword")
        
        # Click buttons
        await page.click("#login-button")
        
        # Wait for navigation
        await page.wait_for_url("https://example.com/dashboard")
        
        # Execute custom JavaScript
        dimensions = await page.evaluate("""() => {
            return {
                width: window.innerWidth,
                height: window.innerHeight,
                userAgent: navigator.userAgent
            };
        }""")
        print(f"Browser dimensions: {dimensions['width']}x{dimensions['height']}")
        
        # Take screenshot
        await page.screenshot(path="screenshot.png")
        
        await browser.close()

# Run the example
asyncio.run(browser_automation_example())
```

For a complete working example, see `examples/browser/visit_aliyun.py` in the SDK repository.

### Browser Automation Best Practices

1. **Element Waiting**: Always wait for elements to appear before interacting
2. **Error Handling**: Implement retry logic for flaky network conditions
3. **Resource Cleanup**: Close browser sessions to free resources
4. **Performance**: Use efficient selectors and minimize screenshot captures

<a id="integration-and-extensions"></a>
## 🔌 Integration and Extensions

### Custom Integration Framework

The AgentBay SDK can be integrated with custom systems and third-party services. While the SDK doesn't provide built-in event listeners or middleware, you can implement these patterns in your application code:

#### Custom Event Handling
```python
# Python example of custom event handling
class SessionEventManager:
    def __init__(self):
        self.listeners = {
            "session_created": [],
            "session_destroyed": []
        }
    
    def on(self, event, callback):
        if event in self.listeners:
            self.listeners[event].append(callback)
    
    def emit(self, event, *args):
        if event in self.listeners:
            for callback in self.listeners[event]:
                callback(*args)

# Usage
event_manager = SessionEventManager()

def on_session_created(session):
    print(f"Session created: {session.session_id}")
    # Custom initialization logic

def on_session_destroyed(session_id):
    print(f"Session destroyed: {session_id}")
    # Cleanup logic

event_manager.on("session_created", on_session_created)
event_manager.on("session_destroyed", on_session_destroyed)

# Emit events in your application code
# event_manager.emit("session_created", session)
# event_manager.emit("session_destroyed", session_id)
```

### Third-Party Service Integration

#### Database Integration
```python
# Python example with database integration
import sqlite3

def save_session_data(session, db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id TEXT PRIMARY KEY,
            created_at TIMESTAMP,
            status TEXT
        )
    """)
    
    cursor.execute("""
        INSERT OR REPLACE INTO sessions (id, created_at, status)
        VALUES (?, ?, ?)
    """, (session.session_id, session.created_at, session.status))
    
    conn.commit()
    conn.close()
```

#### CI/CD Pipeline Integration
```yaml
# GitHub Actions example
name: AgentBay Integration Test
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    - name: Install dependencies
      run: |
        pip install wuying-agentbay-sdk
    - name: Run integration test
      run: |
        python test_agentbay.py
      env:
        AGENTBAY_API_KEY: ${{ secrets.AGENTBAY_API_KEY }}
```

<a id="best-practices"></a>
## 🏆 Best Practices

### Performance Optimization

1. **Session Reuse**: Reuse sessions for multiple operations
2. **Batch Operations**: Group related operations together
3. **Connection Pooling**: Use connection pooling for high-frequency operations
4. **Caching**: Implement caching for frequently accessed data

### Security Considerations

1. **API Key Management**: Use environment variables or secure vaults
2. **Network Security**: Implement proper firewall rules and VPC configurations
3. **Data Encryption**: Encrypt sensitive data in transit and at rest
4. **Access Control**: Implement role-based access control (RBAC)

### Error Handling and Monitoring

1. **Comprehensive Logging**: Implement detailed logging for debugging
2. **Retry Logic**: Implement exponential backoff for transient failures
3. **Health Checks**: Regular health checks for critical services
4. **Alerting**: Set up alerts for critical failures and performance issues

### Resource Management

1. **Session Lifecycle**: Properly clean up sessions when done
2. **Memory Management**: Monitor and optimize memory usage
3. **Quota Management**: Monitor resource quotas and limits
4. **Cost Optimization**: Optimize resource usage to minimize costs

## 📚 Related Resources

- [Session Management Guide](session-management.md)
- [Data Persistence Guide](data-persistence.md)
- [API Reference](../api-reference.md)
- [Example Code](../../examples/)

## 🆘 Getting Help

If you encounter issues with advanced features:

1. Check the [Documentation](../README.md) for detailed information
2. Review [Example Code](../../examples/) for implementation patterns
3. Search [GitHub Issues](https://github.com/aliyun/wuying-agentbay-sdk/issues) for similar problems
4. Contact support with detailed error information and reproduction steps

Remember: Advanced features provide powerful capabilities but require careful planning and implementation. Start with simple use cases and gradually increase complexity! 🚀