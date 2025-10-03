# Session Link Access

This guide shows you how to use `get_link()` to connect to your AgentBay cloud sessions.

> **⚠️ Important Notice**: The Session Link feature is currently in whitelist-only access. To request access to this feature, please send your application to agentbay_dev@alibabacloud.com. For product feedback or suggestions, please submit through the [Alibaba Cloud ticket system](https://smartservice.console.aliyun.com/service/list).

## 📋 Table of Contents

- [🎯 What is a Session Link?](#-what-is-a-session-link)
- [🚀 Three Main Use Cases](#-three-main-use-cases)
- [📋 Quick Selection Guide](#-quick-selection-guide)
- [💡 Complete Code Examples](#-complete-code-examples)
- [📖 Advanced Topics](#-advanced-topics)

---

## 🎯 What is a Session Link?

### Simple Explanation

When you create an AgentBay session, you're starting a virtual computer in the cloud. If you need to **directly connect** external tools (like Playwright, your local browser, or WebSocket clients) to services running inside the session, you'll need a **Session Link**.

Think of it this way:
- 🏠 **Session** = A house in the cloud running services
- 🔗 **Session Link** = The direct address to access those services
- 💻 **Your local tools** = Need this address to connect to services inside

Session Link provides the **direct network access URL** to services in your cloud session.

### What Can `get_link()` Do?

The `get_link()` method returns a URL that enables **direct connections** to services in your session:

1. ✅ **Control a cloud browser** with Playwright/Puppeteer (browser automation via CDP)
2. ✅ **Access web applications** running in your session (like dev servers on custom ports)
3. ✅ **Connect to custom services** in the cloud (like WebSocket servers, databases)

---

## 🚀 Three Main Use Cases

Based on what you want to do, `get_link()` has three main ways to use it:

### Use Case 1: Browser Automation 🤖

#### Your Need
I want to control a cloud browser with Playwright/Puppeteer for automation tasks.

#### Solution
Call `get_link()` **with no parameters**. It returns a browser control address (CDP endpoint).

#### Minimal Code

```python
from agentbay import AgentBay, CreateSessionParams

# 1. Create session (MUST use Browser Use image)
agent_bay = AgentBay(api_key="your_api_key")
session = agent_bay.create(
    CreateSessionParams(image_id="browser_latest")  # or other Browser Use images
).session

# 2. Get browser control address
link = session.get_link()
print(f"Browser address: {link.data}")
# Output: wss://gateway.../websocket_ai/...

# 3. Connect with Playwright
from playwright.async_api import async_playwright

async with async_playwright() as p:
    browser = await p.chromium.connect_over_cdp(link.data)
    page = await browser.new_page()
    await page.goto("https://example.com")
    # Now you can control the cloud browser!
```

#### Key Points
- ✅ MUST use Browser Use image (e.g., `browser_latest` or custom Browser Use images)
- ✅ No parameters needed (or use `protocol_type="wss"`)
- ✅ Returns a WebSocket URL starting with `wss://`

#### Who Is This For?
- Browser automation testing
- Web scraping with headless browsers
- RPA automation workflows

---

### Use Case 2: Access Web Applications 🌐

#### Your Need
I'm running a web service in the cloud session (like `npm run dev`) and want to access it from my local browser.

#### Solution
Call `get_link(protocol_type="https", port=port_number)` to get an HTTPS URL.

#### Minimal Code

```python
from agentbay import AgentBay

# 1. Create session (any image works)
agent_bay = AgentBay(api_key="your_api_key")
session = agent_bay.create().session

# 2. Start a web server in the cloud (port 30150)
session.file_system.write_file(
    "/tmp/index.html", 
    "<h1>Hello from Cloud!</h1>"
)
session.command.execute_command(
    "cd /tmp && python3 -m http.server 30150 &"
)

# 3. Get access URL
link = session.get_link(protocol_type="https", port=30150)
print(f"Web app URL: {link.data}")
# Output: https://gateway.../request_ai/.../path/

# 4. Open this URL in your browser to access the cloud web service!
```

#### Key Points
- ✅ MUST specify both `protocol_type="https"` and `port`
- ✅ Port number MUST be in **30100-30199** range
- ✅ Returns an HTTPS URL you can open in a browser

#### Who Is This For?
- Debugging frontend projects in the cloud (React/Vue dev servers)
- Viewing web apps running in the cloud

---

### Use Case 3: Connect to Custom Services 🔌

#### Your Need
I'm running a custom service in the cloud and want to connect to it from my local machine.

#### Solution
Call `get_link(port=port_number)` to get a WebSocket URL.

#### Minimal Code

```python
from agentbay import AgentBay

# 1. Create session
agent_bay = AgentBay(api_key="your_api_key")
session = agent_bay.create().session

# 2. Start a service in the cloud (port 30180)
session.command.execute_command(
    "python3 -m http.server 30180 &"
)

# 3. Get connection URL
link = session.get_link(port=30180)
print(f"Service URL: {link.data}")
# Output: wss://gateway.../websocket_ai/...

# 4. Connect from your local code
# (Use appropriate client based on your service type)
```

#### Key Points
- ✅ Only pass `port`, don't pass `protocol_type`
- ✅ Port number MUST be in **30100-30199** range
- ✅ Returns a WebSocket URL (wss://)

#### Who Is This For?
- Connecting to custom WebSocket services
- Accessing database services (via port forwarding)
- Debugging network services

---

## 📋 Quick Selection Guide

### Decision Tree

```
Question: What do you want to do?
    ↓
├─ A. Control a browser → [Use Case 1] No parameters
├─ B. Access a web page → [Continue to Question 2]
└─ C. Connect to other services → [Continue to Question 3]

Question 2: This web page is...
├─ Running in the cloud session → [Use Case 2] HTTPS + port
└─ External website → ⚠️  No need for get_link, access directly

Question 3: This service is...
├─ HTTP/HTTPS service → [Use Case 2] HTTPS + port
├─ WebSocket or other → [Use Case 3] Port only
└─ Other protocols → ⚠️  Only HTTPS and WSS are supported
```

### Quick Reference Table

| Your Need | How to Call | protocol_type | port | Image Required |
|-----------|------------|---------------|------|----------------|
| Browser automation (CDP) | `get_link()` | Don't pass | Don't pass | Browser Use image |
| Access web app | `get_link("https", 30150)` | `"https"` | 30100-30199 | Any |
| WebSocket service | `get_link(port=30150)` | Don't pass | 30100-30199 | Any |
| Custom HTTPS service | `get_link("https", 30150)` | `"https"` | 30100-30199 | Any |

### Common Mistakes

| You Write | What Happens | Correct Way |
|-----------|--------------|-------------|
| `get_link("https")` | ❌ Error: "port is not valid" | `get_link("https", 30150)` |
| `get_link(port=8080)` | ❌ Error: "Port must be in 30100-30199" | `get_link(port=30150)` |
| `get_link("http", 30150)` | ❌ Error: "http not supported" | `get_link("https", 30150)` |
| Non-Browser Use image + `get_link()` | ❌ Error: "only BrowserUse image support cdp" | Use Browser Use image (e.g., `browser_latest`) |

---

## 💡 Complete Code Examples

These are complete, tested examples you can copy and run directly.

### Example 1: Browser Automation Complete Flow

**Goal**: Control a cloud browser with Playwright and visit a website

```python
import asyncio
import os
from agentbay import AgentBay, CreateSessionParams
from playwright.async_api import async_playwright

async def browser_automation_example():
    """Complete browser automation example"""
    
    # 1. Initialize (get API key from environment variable)
    api_key = os.environ.get("AGENTBAY_API_KEY")
    if not api_key:
        print("❌ Error: AGENTBAY_API_KEY environment variable is not set")
        print("Please set it using: export AGENTBAY_API_KEY=your_api_key")
        return
    
    agent_bay = AgentBay(api_key=api_key)
    session = None
    
    try:
        # 2. Create Browser Use session
        print("Creating cloud browser session...")
        session_result = agent_bay.create(
            CreateSessionParams(image_id="browser_latest")
        )
        
        if not session_result.success:
            print(f"❌ Failed: {session_result.error_message}")
            return
        
        session = session_result.session
        print(f"✅ Session created: {session.session_id}")
        
        # 3. Get browser CDP address
        print("\nGetting browser control address...")
        link_result = session.get_link()
        
        if not link_result.success:
            print(f"❌ Failed: {link_result.error_message}")
            return
        
        cdp_url = link_result.data
        print(f"✅ CDP URL: {cdp_url[:60]}...")
        
        # 4. Connect with Playwright and control browser
        print("\nConnecting to browser...")
        async with async_playwright() as p:
            browser = await p.chromium.connect_over_cdp(cdp_url)
            print("✅ Connected to browser!")
            
            # Create new page
            page = await browser.new_page()
            
            # Visit Alibaba Cloud website
            print("\nVisiting https://www.aliyun.com ...")
            await page.goto("https://www.aliyun.com")
            title = await page.title()
            print(f"✅ Page title: {title}")
            
            # Close browser
            await browser.close()
            print("✅ Browser closed")
        
        print("\n🎉 SUCCESS: Browser automation completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # 5. Cleanup
        if session:
            print("\nCleaning up...")
            agent_bay.delete(session)
            print("✅ Session deleted")

if __name__ == "__main__":
    asyncio.run(browser_automation_example())
```

**Before Running**:
1. Install dependencies: `pip install agentbay playwright`
2. Install browser: `playwright install chromium`
3. Set your API key: `export AGENTBAY_API_KEY=your_api_key`

**Expected Output**:
```
Creating cloud browser session...
✅ Session created: session-abc123

Getting browser control address...
✅ CDP URL: wss://gateway.../websocket_ai/...

Connecting to browser...
✅ Connected to browser!

Visiting https://www.aliyun.com ...
✅ Page title: 阿里云-计算，为了无法计算的价值
✅ Browser closed

🎉 SUCCESS: Browser automation completed!

Cleaning up...
✅ Session deleted
```

---

### Example 2: Access Cloud Web Application

**Goal**: Start an HTTP server in the cloud and access it from local browser

```python
import time
import os
from agentbay import AgentBay

def web_app_access_example():
    """Complete web application access example"""
    
    # 1. Initialize (get API key from environment variable)
    api_key = os.environ.get("AGENTBAY_API_KEY")
    if not api_key:
        print("❌ Error: AGENTBAY_API_KEY environment variable is not set")
        print("Please set it using: export AGENTBAY_API_KEY=your_api_key")
        return
    
    agent_bay = AgentBay(api_key=api_key)
    session = None
    
    try:
        # 2. Create session (any image works)
        print("Creating session...")
        session = agent_bay.create().session
        print(f"✅ Session ID: {session.session_id}")
        
        # 3. Create a simple HTML file in the cloud
        print("\nCreating HTML file in cloud...")
        session.file_system.write_file(
            "/tmp/index.html",
            "<h1>Hello from AgentBay Cloud!</h1><p>Running on port 30150</p>"
        )
        print("✅ HTML file created")
        
        # 4. Start HTTP server on port 30150
        print("\nStarting HTTP server...")
        port = 30150
        session.command.execute_command(
            f"cd /tmp && nohup python3 -m http.server {port} > /dev/null 2>&1 &"
        )
        time.sleep(3)  # Wait for server to start
        print(f"✅ HTTP server started on port {port}")
        
        # 5. Get access URL
        print("\nGetting access URL...")
        link_result = session.get_link(protocol_type="https", port=port)
        
        if not link_result.success:
            print(f"❌ Failed: {link_result.error_message}")
            return
        
        web_url = link_result.data
        print(f"✅ Web URL: {web_url}")
        
        print("\n" + "=" * 70)
        print("🎉 SUCCESS: Web application is accessible!")
        print("=" * 70)
        print(f"\n👉 Open this URL in your browser:")
        print(f"   {web_url}")
        print(f"\nSession will stay alive for 30 seconds...")
        
        time.sleep(30)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # 6. Cleanup
        if session:
            print("\nCleaning up...")
            agent_bay.delete(session)
            print("✅ Session deleted")

if __name__ == "__main__":
    web_app_access_example()
```

**Key Points**:
- Port must be in 30100-30199 range
- Must pass both `protocol_type` and `port`
- Returned URL can be opened directly in browser

---

### Example 3: Custom Port Access

**Goal**: Demonstrate port parameter usage for custom services

```python
import time
import os
from agentbay import AgentBay

def custom_port_example():
    """Custom port access example"""
    
    # 1. Initialize (get API key from environment variable)
    api_key = os.environ.get("AGENTBAY_API_KEY")
    if not api_key:
        print("❌ Error: AGENTBAY_API_KEY environment variable is not set")
        print("Please set it using: export AGENTBAY_API_KEY=your_api_key")
        return
    
    agent_bay = AgentBay(api_key=api_key)
    session = None
    
    try:
        # 2. Create session
        print("Creating session...")
        session = agent_bay.create().session
        print(f"✅ Session ID: {session.session_id}")
        
        # 3. Start a service on custom port 30180
        print("\nStarting service on port 30180...")
        port = 30180
        session.command.execute_command(
            f"cd /tmp && nohup python3 -m http.server {port} > /dev/null 2>&1 &"
        )
        time.sleep(3)
        print(f"✅ Service started on port {port}")
        
        # 4. Get link with custom port
        print("\nGetting link with custom port...")
        link_result = session.get_link(port=port)
        
        if not link_result.success:
            print(f"❌ Failed: {link_result.error_message}")
            return
        
        service_url = link_result.data
        print(f"✅ Service URL: {service_url[:80]}...")
        print(f"✅ Protocol: {service_url.split('://')[0]}://")
        
        # Verify protocol
        if service_url.startswith("wss://"):
            print("✅ Confirmed: WebSocket Secure (wss://) URL")
        
        print("\n🎉 SUCCESS: Custom port link obtained!")
        print(f"\nKey findings:")
        print(f"  - Port: {port}")
        print(f"  - Protocol: wss://")
        print(f"  - Port range: 30100-30199")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # 5. Cleanup
        if session:
            print("\nCleaning up...")
            agent_bay.delete(session)
            print("✅ Session deleted")

if __name__ == "__main__":
    custom_port_example()
```

**Note**: These examples have been tested and verified with real AgentBay API calls.

---

## 📖 Advanced Topics

### Asynchronous Operations

For async applications, use `get_link_async()`:

```python
import asyncio
import os
from agentbay import AgentBay

async def get_multiple_links():
    api_key = os.environ.get("AGENTBAY_API_KEY")
    agent_bay = AgentBay(api_key=api_key)
    session = agent_bay.create().session
    
    try:
        # Get multiple links in parallel
        tasks = [
            session.get_link_async(),  # Default WebSocket
            session.get_link_async(protocol_type="https", port=30199),  # HTTPS
            session.get_link_async(port=30150)  # WebSocket with port
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                print(f"Link {i+1} failed: {result}")
            elif result.success:
                print(f"Link {i+1}: {result.data}")
    finally:
        agent_bay.delete(session)

if __name__ == "__main__":
    asyncio.run(get_multiple_links())
```

### Best Practices

#### 1. Parameter Validation

```python
def safe_get_link(session, protocol_type=None, port=None):
    """Safely get session link with validation"""
    if protocol_type is not None and port is None:
        raise ValueError("protocol_type requires port parameter")
    
    if port is not None and not (30100 <= port <= 30199):
        raise ValueError(f"Port {port} outside valid range [30100, 30199]")
    
    return session.get_link(protocol_type=protocol_type, port=port)
```

#### 2. Error Handling

```python
def robust_get_link(session, protocol_type=None, port=None):
    """Get link with comprehensive error handling"""
    try:
        result = session.get_link(protocol_type=protocol_type, port=port)
        
        if result.success:
            print(f"Link: {result.data}")
            print(f"Request ID: {result.request_id}")
            return result.data
        else:
            print(f"API error: {result.error_message}")
            return None
    
    except Exception as e:
        print(f"Exception: {e}")
        return None
```

#### 3. Link Caching

```python
class SessionLinkManager:
    """Cache links to avoid repeated API calls"""
    
    def __init__(self, session):
        self.session = session
        self.cache = {}
    
    def get_cached_link(self, protocol_type=None, port=None):
        key = f"{protocol_type}:{port}"
        
        if key not in self.cache:
            result = self.session.get_link(
                protocol_type=protocol_type, 
                port=port
            )
            if result.success:
                self.cache[key] = result.data
        
        return self.cache.get(key)
```

### Troubleshooting

#### Link Not Accessible

If the link is generated successfully but you cannot access it:

```python
# Check 1: Verify the service is running on the specified port
result = session.command.execute_command("netstat -tuln | grep 30150")
if result.success:
    print(f"Port status: {result.output}")
else:
    print("Service may not be running on the specified port")

# Check 2: Verify the session is still active
info_result = session.info()
if info_result.success:
    print(f"Session ID: {info_result.data.session_id}")
    print(f"Session status: Active")
else:
    print(f"Session may have been terminated: {info_result.error_message}")
```

#### Connection Timeouts

If connections to the link time out:

```python
# Check 1: Verify network connectivity to the gateway domain
# Extract domain from link for testing
link_result = session.get_link(protocol_type="https", port=30150)
if link_result.success:
    import urllib.parse
    parsed = urllib.parse.urlparse(link_result.data)
    print(f"Gateway domain: {parsed.netloc}")
    # Test connectivity: ping or curl the domain

# Check 2: Confirm the session hasn't been terminated
info_result = session.info()
if not info_result.success:
    print("Session may have been terminated")
    print("Create a new session and try again")

# Check 3: Review VPC and subnet configurations (for VPC sessions)
# If using VPC mode, ensure:
# - Security groups allow traffic on the specified port
# - Network ACLs permit inbound/outbound connections
# - Route tables are correctly configured
```

### Debugging Helper Function

When troubleshooting link issues, use this comprehensive debugging function.

**Note**: This is a helper function example, not a built-in SDK method. Copy the complete function code below into your script to use it.

#### How to Use

1. **Copy the entire function definition** from the code block below
2. **Paste it into your Python script** before calling it
3. **Call the function** with your session object: `debug_session_links(session)`

#### Function Code

```python
def debug_session_links(session):
    """Debug session link generation and accessibility."""
    print(f"Debugging session: {session.session_id}")
    print("=" * 70)
    
    # Step 1: Get session info
    print("\n[Step 1] Checking session status...")
    info_result = session.info()
    if info_result.success:
        info = info_result.data
        print(f"✅ Session ID: {info.session_id}")
        print(f"✅ Resource Type: {info.resource_type}")
        print(f"✅ Resource ID: {info.resource_id}")
        print(f"✅ Resource URL: {info.resource_url[:100]}...")
    else:
        print(f"❌ Failed to get session info: {info_result.error_message}")
        return
    
    # Step 2: Test different link types
    print("\n[Step 2] Testing different link configurations...")
    test_cases = [
        ("Default WebSocket", None, None),
        ("WebSocket with port 30150", None, 30150),
        ("HTTPS on port 30199", "https", 30199),
        ("WebSocket Secure on port 30199", "wss", 30199),
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
                url_preview = result.data[:80] + "..." if len(result.data) > 80 else result.data
                print(f"✅ {name}: {url_preview}")
            else:
                print(f"❌ {name}: {result.error_message}")
        
        except Exception as e:
            print(f"❌ {name}: Exception - {e}")
    
    print("\n" + "=" * 70)
    print("Debugging complete!")
```

#### Usage Example

After copying the function definition above, you can use it like this:

```python
import os
from agentbay import AgentBay

# (Paste the debug_session_links function definition here)

# Now use the function
api_key = os.environ.get("AGENTBAY_API_KEY")
agent_bay = AgentBay(api_key=api_key)
session = agent_bay.create().session

# Call the debugging function
debug_session_links(session)

# Cleanup
agent_bay.delete(session)
```

**Expected Output**:
```
Debugging session: session-abc123
======================================================================

[Step 1] Checking session status...
✅ Session ID: session-abc123
✅ Resource Type: container
✅ Resource ID: res-abc123
✅ Resource URL: wss://gateway.../websocket_ai/...

[Step 2] Testing different link configurations...
❌ Default WebSocket: no port specified, cdp default, but only BrowserUse image support cdp
✅ WebSocket with port 30150: wss://gateway.../websocket_ai/...
✅ HTTPS on port 30199: https://gateway.../request_ai/.../path/
✅ WebSocket Secure on port 30199: wss://gateway.../websocket_ai/...

======================================================================
Debugging complete!
```

### Link Format Details

#### WebSocket Secure (wss://)

```
wss://gw-cn-hangzhou-ai-linux.wuyinggw.com:8008/websocket_ai/{token}
 │    │                                        │     │              │
 │    └─ Gateway domain                        │     └─ Endpoint    └─ Auth token
 │                                             └─ Gateway port
 └─ Protocol (WebSocket Secure)
```

**Use**: Chrome DevTools Protocol (CDP) endpoint for browser automation, or WebSocket services with custom ports

#### HTTPS

```
https://gw-cn-hangzhou-ai-linux.wuyinggw.com:8008/request_ai/{token}/path/
 │     │                                        │     │           │        │
 │     └─ Gateway domain                        │     └─ Endpoint └─ Token └─ Path suffix
 │                                             └─ Gateway port
 └─ Protocol (HTTPS)
```

**Use**: HTTP/HTTPS access to web applications and services running in the session

---

## Related Resources

- [Session Management Guide](../basics/session-management.md)
- [Advanced Features Guide](README.md)

## Getting Help

If you encounter issues:

1. Check this documentation for solutions
2. Search [GitHub Issues](https://github.com/aliyun/wuying-agentbay-sdk/issues)
3. Contact support with detailed error information

Remember: Session Link Access is your gateway to cloud session connectivity! 🔗
