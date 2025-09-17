# Complete Guide to Advanced Features

This guide integrates the advanced features of the AgentBay SDK, including VPC session configuration, Agent modules (AI tasks), browser automation, and integration extensions.

## 📋 Table of Contents

- [VPC Sessions](#vpc-sessions)
- [Session Access Links](#session-access-links)
- [Agent Modules](#agent-modules)
- [Browser Automation](#browser-automation)
- [Best Practices](#best-practices)

<a id="vpc-sessions"></a>
## 🔒 VPC Sessions

### VPC Session Overview

VPC (Virtual Private Cloud) sessions provide isolated network environments, suitable for scenarios requiring special network configurations or security requirements.

### Creating VPC Sessions

```python
from agentbay import AgentBay, CreateSessionParams

agent_bay = AgentBay(api_key=api_key)

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
agent_bay.delete(vpc_session)
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

<a id="session-access-links"></a>
## 🔗 Session Access Links

### Session Link Overview

The `get_link()` method provides access URLs for connecting to your session through different protocols and ports. This is essential for accessing web applications, development servers, and custom services running within your sessions.

**Important Port Range Restriction**: All port parameters must be integers in the range **[30100, 30199]**. Ports outside this range will result in validation errors.

### Basic Link Retrieval

```python
from agentbay import AgentBay
 # When get_link has no parameters, a special image_id needs to be specified, image_id should be browser_latest

# Initialize the SDK and create a session
session_params = CreateSessionParams(image_id="browser_latest")

session_result = agent_bay.create(session_params)

if session_result.success:
    session = session_result.session
    print(f"Session created with ID: {session.session_id}")

    # Get default session link (WebSocket connection) with exception handling
    try:
        link_result = session.get_link()


        if link_result.success:
            print(f"Default session link: {link_result.data}")
            print(f"Request ID: {link_result.request_id}")
            # Output: wss://gw-ap-southeast-1-ai-linux.wuyinggwintl.com:8008/websocket_ai/...
        else:
            print(f"Failed to get link: {link_result.error_message}")
    except Exception as e:
        print(f"Exception occurred while getting session link: {str(e)}")
else:
    print(f"Session creation failed: {session_result.error_message}")
agent_bay.delete(session)
```

### Port Range Validation

**Valid Port Range**: **[30100, 30199]**

All port parameters passed to `get_link()` must be integers within this range. Common ports like 80, 443, 8080, etc. are **not allowed** and will result in validation errors.

```python
from agentbay import AgentBay
from agentbay.exceptions import SessionError

agent_bay = AgentBay()
session = agent_bay.create().session

# ✅ Valid ports (within range [30100, 30199])
valid_ports = [30100, 30150, 30199]

for port in valid_ports:
    try:
        result = session.get_link(port=port)
        if result.success:
            print(f"✅ Port {port}: {result.data}")
    except SessionError as e:
        print(f"❌ Port {port}: {e}")

# ❌ Invalid ports (outside range [30100, 30199])
invalid_ports = [80, 443, 8080, 30099, 30200]

for port in invalid_ports:
    try:
        result = session.get_link(port=port)
        print(f"Unexpected success for invalid port {port}")
    except SessionError as e:
        print(f"✅ Expected error for port {port}: {e}")
        # Output: "Invalid port value: 8080. Port must be an integer in the range [30100, 30199]."
```

### Parameter Usage and Constraints

**Important**: The `get_link()` method has specific parameter requirements:

**Supported Protocol Types:**
- ✅ `"https"` - Returns HTTPS links for web access
- ✅ `"wss"` - Returns WebSocket Secure links for real-time communication
- ❌ `"http"`, `"ws"`, `"tcp"`, `"ftp"` - **NOT SUPPORTED**

**Valid Parameter Combinations:**
- **No parameters**: Returns default WebSocket Secure link (`wss://`)
- **Port only**: Specify port without protocol_type (returns `wss://` with port info) - **Port must be in range [30100, 30199]**
- **Both parameters**: Must specify both `protocol_type` and `port` together - **Port must be in range [30100, 30199]**
- **Protocol only**: ❌ **NOT ALLOWED** - Will cause "port is not valid: null" error

```python
from agentbay import AgentBay

agent_bay = AgentBay(api_key=api_key)
session_result = agent_bay.create()
session = session_result.session

# ✅ Valid: No parameters (default WebSocket Secure)
default_link = session.get_link()
print(f"Default: {default_link.data}")
# Output: wss://gw-ap-southeast-1-ai-linux.wuyinggwintl.com:8008/websocket_ai/...

# ✅ Valid: Port only (WebSocket Secure with port info) - using valid port
port_link = session.get_link(port=30150)  # Valid port in range [30100, 30199]
print(f"Port 30150: {port_link.data}")
# Output: wss://gw-ap-southeast-1-ai-linux.wuyinggwintl.com:8008/websocket_ai/...

# ✅ Valid: HTTPS with valid port
https_link = session.get_link(protocol_type="https", port=30199)  # Valid port
print(f"HTTPS: {https_link.data}")
# Output: https://gw-ap-southeast-1-ai-linux.wuyinggwintl.com:8008/request_ai/.../path/

# ✅ Valid: WebSocket Secure with valid port
wss_link = session.get_link(protocol_type="wss", port=30100)  # Valid port
print(f"WSS: {wss_link.data}")
# Output: wss://gw-ap-southeast-1-ai-linux.wuyinggwintl.com:8008/websocket_ai/...

# ❌ Invalid: Protocol without port (will raise SessionError)
try:
    invalid_link = session.get_link(protocol_type="https")
except SessionError as e:
    print(f"Error: {e}")  # "port is not valid: null"

# ❌ Invalid: Unsupported protocol (will raise SessionError)
try:
    invalid_link = session.get_link(protocol_type="http", port=30150)
except SessionError as e:
    print(f"Error: {e}")  # "No enum constant ProtocolTypeEnum.http"

# ❌ Invalid: Port outside valid range (will raise SessionError)
try:
    invalid_port_link = session.get_link(port=8080)  # Invalid port
except SessionError as e:
    print(f"Error: {e}")  # "Invalid port value: 8080. Port must be an integer in the range [30100, 30199]."
```

### Use Cases

Based on actual testing, here are the practical applications of `get_link()`:

#### WebSocket Connections for Real-Time Communication
```python
# Get WebSocket links for real-time applications
session = agent_bay.create().session

# Default WebSocket Secure connection
ws_link = session.get_link()
if ws_link.success:
    print(f"WebSocket URL: {ws_link.data}")
    # Use with WebSocket clients for real-time communication
    # Example: Browser automation, live data streaming

# WebSocket with specific port configuration
ws_port_link = session.get_link(port=8080)
if ws_port_link.success:
    # Port information is encoded in the WebSocket URL
    print(f"WebSocket (port 8080): {ws_port_link.data}")

agent_bay.delete(session)
```

#### HTTPS Access for Web Applications
```python
# Get WebSocket links for real-time applications
 session = agent_bay.create().session

# Linux sessions support HTTPS access
https_link = session.get_link(protocol_type="https", port=443)
if https_link.success:
    print(f"HTTPS Access: {https_link.data}")
    # Use for web-based applications running in the session

# HTTPS access on custom port
custom_https = session.get_link(protocol_type="https", port=8443)
if custom_https.success:
    print(f"Custom HTTPS: {custom_https.data}")
agent_bay.delete(session)
```

### Asynchronous Link Retrieval

For applications requiring asynchronous operations, use the `get_link_async()` method:

```python
import asyncio
from agentbay import AgentBay

async def get_multiple_links():
    agent_bay = AgentBay()
    session_result = agent_bay.create()
    session = session_result.session

    # Get multiple links asynchronously
    tasks = [
        session.get_link_async(),  # Default WebSocket
        session.get_link_async(protocol_type="https", port=443),  # HTTPS
        session.get_link_async(port=8080)  # WebSocket with port
    ]

    results = await asyncio.gather(*tasks, return_exceptions=True)

    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"Link {i+1} failed: {result}")
        elif result.success:
            print(f"Link {i+1}: {result.data}")
        else:
            print(f"Link {i+1} failed: {result.error_message}")

# Run the async example
asyncio.run(get_multiple_links())
```

### Understanding Link Types and Formats

Based on the parameters, `get_link()` returns different types of URLs:

#### 1. WebSocket Secure Links (Default and Port-only)
```python
# Default call returns WebSocket Secure URLs
ws_link = session.get_link()
# Format: wss://gw-ap-southeast-1-ai-linux.wuyinggwintl.com:8008/websocket_ai/{token}

# Port-only call also returns WebSocket Secure URLs
ws_port_link = session.get_link(port=8080)
# Format: wss://gw-ap-southeast-1-ai-linux.wuyinggwintl.com:8008/websocket_ai/{token}
# (Port information is encoded in the token)

# Explicit WebSocket Secure with port
wss_explicit = session.get_link(protocol_type="wss", port=443)
# Format: wss://gw-ap-southeast-1-ai-linux.wuyinggwintl.com:8008/websocket_ai/{token}
```

#### 2. HTTPS Links (Protocol + Port)
```python
# HTTPS protocol with port returns HTTPS URLs
https_link = session.get_link(protocol_type="https", port=443)
# Format: https://gw-ap-southeast-1-ai-linux.wuyinggwintl.com:8008/request_ai/{token}/path/
```

### Session Link Best Practices

1. **Parameter Validation**: Always validate parameters before calling
   ```python
   def safe_get_link(session, protocol_type=None, port=None):
       """Safely get session link with parameter validation."""
       if protocol_type is not None and port is None:
           raise ValueError("When protocol_type is specified, port must also be provided")

       try:
           return session.get_link(protocol_type=protocol_type, port=port)
       except Exception as e:
           print(f"Failed to get link: {e}")
           return None
   ```

2. **Protocol Selection**: Choose appropriate protocols based on your application needs
   - Use WebSocket Secure (`wss://`) for real-time communication and browser automation
   - Use HTTPS (`https://`) for web applications and REST APIs
   - **Note**: Only `"https"` and `"wss"` protocols are supported

3. **Port Management**:
   - Use standard ports when possible (80 for HTTP, 443 for HTTPS)
   - Document custom port usage for team collaboration
   - Avoid conflicts with system reserved ports (< 1024)

4. **Error Handling**:
   ```python
   def robust_get_link(session, protocol_type=None, port=None):
       """Get session link with comprehensive error handling."""
       try:
           result = session.get_link(protocol_type=protocol_type, port=port)

           if result.success:
               print(f"Link retrieved successfully: {result.data}")
               print(f"Request ID: {result.request_id}")
               return result.data
           else:
               print(f"API returned failure: {result.error_message}")
               return None

       except Exception as e:
           print(f"Exception occurred: {e}")
           return None
   ```

5. **Link Caching and Reuse**:
   ```python
   class SessionLinkManager:
       def __init__(self, session):
           self.session = session
           self.link_cache = {}

       def get_cached_link(self, protocol_type=None, port=None):
           """Get link with caching to avoid repeated API calls."""
           cache_key = f"{protocol_type}:{port}"

           if cache_key not in self.link_cache:
               result = self.session.get_link(protocol_type=protocol_type, port=port)
               if result.success:
                   self.link_cache[cache_key] = result.data
               else:
                   return None

           return self.link_cache[cache_key]
   ```

### Troubleshooting Session Links

#### Common Issues and Solutions

1. **"port is not valid: null" Error**:
   ```python
   # ❌ Wrong: Protocol without port
   # session.get_link(protocol_type="https")

   # ✅ Correct: Both protocol and port
   session.get_link(protocol_type="https", port=443)
   ```

2. **"No enum constant ProtocolTypeEnum" Error**:
   ```python
   # ❌ Wrong: Unsupported protocol
   # session.get_link(protocol_type="http", port=80)

   # ✅ Correct: Use supported protocols only
   session.get_link(protocol_type="https", port=443)  # or "wss"
   ```
3. **"no port specified, cdp default, but only BrowserUse image support cdp"Error**:
   ```python
   # ❌ Wrong: BrowserUse image does not support cdp
   session = agent_bay.create().session
   session.get_link()
   # ✅ Correct: Use supported image
   create_session_params = CreateSessionParams(image_id="browser_latest")
   session = agent_bay.create(create_session_params).session
   session.get_link()
   ```
4. **Link Not Accessible**:
   - Verify the service is running on the specified port within the session
   - Check if the session is still active using `session.info()`
   - Ensure firewall rules allow the specified port

5. **Connection Timeouts**:
   - Verify network connectivity to the gateway domain
   - Check if the session has been terminated
   - Review VPC and subnet configurations for VPC sessions

#### Debugging Helper Function
```python
def debug_session_links(session):
    """Debug session link generation and accessibility."""
    print(f"Debugging session: {session.session_id}")

    # Get session info first
    info_result = session.info()
    if info_result.success:
        info = info_result.data
        print(f"Session Type: {info. app_id}")
        print(f"Resource Type: {info.resource_type}")
        print(f"Resource URL: {info.resource_url[:100]}...")
    else:
        print(f"Failed to get session info: {info_result.error_message}")
        return

    # Test different link types (only supported protocols)
    test_cases = [
        ("Default WebSocket", None, None),
        ("WebSocket with port", None, 8080),
        ("HTTPS", "https", 443),
        ("WebSocket Secure", "wss", 443),
    ]

    for name, protocol, port in test_cases:
        try:
            if protocol is None and port is None:
                result = session.get_link()
            elif protocol is None:
                result = session.get_link(port=port)
            else:
                result = session.get_link(protocol_type=protocol, port=port)

            if result.success:
                print(f"✅ {name}: {result.data[:80]}...")
            else:
                print(f"❌ {name}: {result.error_message}")

        except Exception as e:
            print(f"❌ {name}: Exception - {e}")

# Usage
debug_session_links(session)
```

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
from agentbay.browser.browser import BrowserOption
session_params = CreateSessionParams(image_id="browser_latest")

session_result = agent_bay.create(session_params)
if session_result.success:
    session = session_result.session
    print(f"Session created with ID: {session.session_id}")

    # Initialize browser
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
agent_bay.delete(session)
```

### Browser Automation Implementation

Browser automation in AgentBay SDK is implemented using Playwright connected through the Chrome DevTools Protocol (CDP). After initializing the browser with `session.browser.initialize()`, you can use Playwright to perform advanced interactions:

```python
# Complete example of browser automation with Playwright
from agentbay.browser.browser import BrowserOption
# Complete example of browser automation with Playwright
import asyncio
from playwright.async_api import async_playwright

async def browser_automation_example():
    session_params = CreateSessionParams(image_id="browser_latest")
    session_result = agent_bay.create(session_params)
    session = session_result.session
    if session.browser.initialize(BrowserOption()):
        # After initializing the browser as shown in the basic example
        endpoint_url = session.browser.get_endpoint_url()

        async with async_playwright() as p:
            browser = await p.chromium.connect_over_cdp(endpoint_url)
            page = await browser.new_page()

            # Navigate to a webpage
            await page.goto("https://example.com")
            print("Page title:", await page.title())

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
        agent_bay.delete(session)

# Run the example
asyncio.run(browser_automation_example())
```

For a complete working example, see `examples/browser/visit_aliyun.py` in the SDK repository.

### Browser Automation Best Practices

1. **Element Waiting**: Always wait for elements to appear before interacting
2. **Error Handling**: Implement retry logic for flaky network conditions
3. **Resource Cleanup**: Close browser sessions to free resources
4. **Performance**: Use efficient selectors and minimize screenshot captures

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

## 🆘 Getting Help

If you encounter issues with advanced features:

1. Check the [Documentation](../README.md) for detailed information

2. Search [GitHub Issues](https://github.com/aliyun/wuying-agentbay-sdk/issues) for similar problems
3. Contact support with detailed error information and reproduction steps

Remember: Advanced features provide powerful capabilities but require careful planning and implementation. Start with simple use cases and gradually increase complexity! 🚀
