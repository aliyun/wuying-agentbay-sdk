# Feature Guides

Welcome to the AgentBay SDK Feature Guides! This provides complete functionality introduction and best practices for experienced developers.

## 🎯 Quick Navigation

### Core Features
- [Session Management](session-management.md) - Create, connect, and manage cloud sessions
- [File Operations](file-operations.md) - Upload, download, and manipulate files
- [Data Persistence](data-persistence.md) - Persistent data storage and synchronization
- [Network Operations](network-operations.md) - Network creation, management, and monitoring
- [Automation](automation.md) - Command execution and workflow automation
- [Application & Window Operations](application-window-operations.md) - Application management and window control
- [Browser Extensions](browser-extensions.md) - Browser extension management and testing
- [Advanced Features](advanced-features.md) - Advanced capabilities and integrations

### Configuration
- [SDK Configuration](sdk-configuration.md) - Complete SDK configuration guide including API keys, regions, endpoints, and timeouts

## 🚀 API Quick Reference

### Basic Operations
```python
# Create session
agent_bay = AgentBay(api_key=api_kay)
# Create session
result = agent_bay.create()
if result.success:
    session = result.session
else:
    print(f"Failed to create session: {result.error_message}")

# Execute command
result = session.command.execute_command("ls -la")

# File operations
write_result = session.file_system.write_file("/tmp/file.txt", "content")
if write_result.success:
    read_result = session.file_system.read_file("/tmp/file.txt")
    if read_result.success:
        content = read_result.content
        print(f"File content: {content}")
agent_bay.delete(session)
```

### Persistent Storage
```python
# Create context
context_result = agent_bay.context.get("project-name", create=True)
if context_result.success:
    context = context_result.context
else:
    print(f"Failed to get context: {context_result.request_id}")

# Create session with context
context_sync = ContextSync.new(context.id, "/tmp/data", SyncPolicy.default())
params = CreateSessionParams(context_syncs=[context_sync])
session_result = agent_bay.create(params)
if session_result.success:
    session = session_result.session
    print(f"Session created successfully, ID: {session.session_id}")
    agent_bay.delete(session)
else:
    print(f"Failed to create session: {session_result.error_message}")
```

### Code Execution
```python
# Create session
result = agent_bay.create()
if result.success:
    session = result.session
else:
    print(f"Failed to create session: {result.error_message}")
# Python code execution using command
python_code = """
print('Hello World from Python!')
import sys
print('Python version:', sys.version)
"""

# Write code to a file and execute it
write_result = session.file_system.write_file("/tmp/script.py", python_code)
if write_result.success:
    result = session.command.execute_command("python3 /tmp/script.py")
    if result.success:
        print("Python output:", result.output)
    else:
        print(f"Python execution failed: {result.error_message}")
else:
    print(f"Failed to write Python script: {write_result.error_message}")

# JavaScript code execution using command
js_code = """
console.log('Hello World from JavaScript!');
console.log('Node.js version:', process.version);
"""

# Write code to a file and execute it
write_result = session.file_system.write_file("/tmp/script.js", js_code)
if write_result.success:
    result = session.command.execute_command("node /tmp/script.js")
    if result.success:
        print("JavaScript output:", result.output)
    else:
        print(f"JavaScript execution failed: {result.error_message}")
else:
    print(f"Failed to write JavaScript script: {write_result.error_message}")
#release session
agent_bay.delete(session)
```

### UI Automation
```python
 # Create session
params = CreateSessionParams(image_id="mobile_latest")
result = agent_bay.create(params)
if result.success:
    session = result.session
else:
    print(f"Failed to create session: {result.error_message}")
# Get clickable UI elements
elements_result = session.ui.get_clickable_ui_elements(timeout_ms=5000)
if elements_result.success:
    print(f"Found {len(elements_result.elements)} clickable elements")
    for element in elements_result.elements:
        print(f"  - {element.get('text', '')} ({element.get('className', '')})")
else:
    print(f"Failed to get clickable UI elements: {elements_result.error_message}")

# Click at specific coordinates
click_result = session.ui.click(x=100, y=200, button="left")
if click_result.success:
    print("Click successful")
else:
    print(f"Click failed: {click_result.error_message}")

# Input text
input_result = session.ui.input_text("myuser")
if input_result.success:
    print("Text input successful")
else:
    print(f"Text input failed: {input_result.error_message}")

# Send key events (e.g., HOME key)
from agentbay.ui.ui import KeyCode
key_result = session.ui.send_key(KeyCode.HOME)
if key_result.success:
    print("Key event sent successfully")
else:
    print(f"Key event failed: {key_result.error_message}")

# Swipe gesture
swipe_result = session.ui.swipe(start_x=100, start_y=200, end_x=300, end_y=400, duration_ms=500)
if swipe_result.success:
    print("Swipe gesture performed successfully")
else:
    print(f"Swipe gesture failed: {swipe_result.error_message}")

# Take screenshot
screenshot_result = session.ui.screenshot()
if screenshot_result.success:
    print(f"Screenshot saved to: {screenshot_result.data}")
else:
    print(f"Screenshot failed: {screenshot_result.error_message}")
# release session
agent_bay.delete(session)
```

### Browser Automation
```python
# Initialize browser with options
from agentbay.browser.browser import BrowserOption
option = BrowserOption(
    use_stealth=True,
    viewport={"width": 1920, "height": 1080}
)

# Initialize browser
init_result = session.browser.initialize(option)
if init_result:
    print("Browser initialized successfully")
else:
    print("Failed to initialize browser")
    exit(1)

# Get browser endpoint URL for Playwright connection
try:
    endpoint_url = session.browser.get_endpoint_url()
    print(f"Browser endpoint URL: {endpoint_url}")
except Exception as e:
    print(f"Failed to get browser endpoint URL: {e}")
    exit(1)

# Connect to browser using Playwright
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(endpoint_url)
    page = browser.new_page()

    # Navigate to page
    page.goto("https://example.com")
    print("Navigation successful")

    # Take screenshot
    screenshot = page.screenshot()
    with open("screenshot.png", "wb") as f:
        f.write(screenshot)
    print("Screenshot saved to screenshot.png")

    # Execute JavaScript
    title = page.evaluate("() => document.title")
    print("Page title:", title)

    # Close browser
    browser.close()
```

## 📚 Detailed Guides

### 🔧 Session Management
Learn how to effectively manage cloud sessions:
- Creating and configuring sessions
- Session lifecycle management
- Resource optimization
- Multi-session coordination

[Read Session Management Guide →](session-management.md)

### 📁 File Operations
Master file handling in cloud environments:
- Upload and download strategies
- Large file handling
- Batch operations
- Permission management

[Read File Operations Guide →](file-operations.md)

### 💾 Data Persistence
Understand data persistence patterns:
- Context system overview
- Sync strategies and policies
- Cross-session data sharing
- Version control and backup

[Read Data Persistence Guide →](data-persistence.md)

### 🤖 Automation
Automate complex workflows:
- Command execution patterns
- Code execution environments
- UI automation techniques
- Workflow orchestration

[Read Automation Guide →](automation.md)

### ⚡ Advanced Features
Explore advanced capabilities:
- VPC sessions
- Agent modules
- Browser automation
- Integration patterns

[Read Advanced Features Guide →](advanced-features.md)


## 🔍 Troubleshooting

### Common Issues
- **Session timeouts**: Increase timeout values or implement retry logic
- **File upload failures**: Check file size limits and network connectivity
- **Command failures**: Verify command syntax and environment setup

### Performance Tips
- Reuse sessions for multiple operations
- Use batch operations when possible
- Implement proper error handling
- Monitor resource usage

## 📖 Additional Resources

- [API Reference](../api-reference.md) - Complete API documentation
- [Best Practices](../quickstart/best-practices.md) - Recommended patterns
- [FAQ](../quickstart/faq.md) - Frequently asked questions
- [Examples](../../examples/) - Working code examples

## 🆘 Getting Help

- [GitHub Issues](https://github.com/aliyun/wuying-agentbay-sdk/issues)
- [Community Discussions](https://github.com/aliyun/wuying-agentbay-sdk/discussions)
- [Documentation](../README.md)

Happy coding with AgentBay! 🚀
