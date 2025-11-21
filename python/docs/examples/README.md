# Python SDK Examples

This directory contains Python examples demonstrating various features and capabilities of the AgentBay SDK.

## 📁 Directory Structure

The examples are organized by feature categories:

```
examples/
├── basic_usage.py                 # Quick start single-file example
├── common-features/               # Features available across all environments
│   ├── basics/                    # Essential features
│   │   ├── session_creation/      # Session lifecycle management
│   │   ├── session_pause_resume/  # Session pause and resume operations
│   │   ├── file_system/           # File operations
│   │   ├── filesystem_example/    # Practical filesystem use cases
│   │   ├── context_management/    # Context creation and management
│   │   ├── data_persistence/      # Data persistence across sessions
│   │   ├── label_management/      # Session organization with labels
│   │   ├── list_sessions/         # Session listing and filtering
│   │   └── get/                   # Session retrieval
│   └── advanced/                  # Advanced features
│       ├── agent_module/          # AI-powered automation
│       ├── oss_management/        # Object Storage Service integration
│       ├── vpc_session/           # Secure isolated network environments
│       └── screenshot_download/   # Screenshot capture and download
├── browser-use/                   # Browser automation (browser_latest)
│   ├── browser/                   # Browser automation examples
│   └── extension/                 # Browser extension management
├── computer-use/                  # Windows desktop automation (windows_latest)
│   └── computer/                  # Application and window management
├── mobile-use/                    # Mobile UI automation (mobile_latest)
│   ├── mobile_system/             # Mobile automation examples
│   └── mobile_get_adb_url_example.py  # ADB URL retrieval
└── codespace/                     # Code execution (code_latest)
    └── code_execution_example.py  # Python/JavaScript code execution
```

## 🚀 Quick Start

### Single-File Example

The fastest way to get started:

```bash
# Set your API key
export AGENTBAY_API_KEY=your_api_key_here

# Run the quick start example
python basic_usage.py
```

This example demonstrates:
- Initializing the AgentBay client
- Creating sessions
- Basic operations (commands, file operations)
- Session cleanup

## 📚 Feature Categories

### [Common Features](common-features/)

Features available across all environment types (browser, computer, mobile, codespace).

**Basics:**
- **Session Management**: Create, configure, and manage cloud sessions
- **File Operations**: Read, write, and manage files in cloud environments
- **Context Management**: Persistent data storage across sessions
- **Data Persistence**: Cross-session data sharing and synchronization
- **Label Management**: Organize and filter sessions with labels

**Advanced:**
- **Agent Module**: AI-powered task automation with natural language
- **OSS Integration**: Object Storage Service for file management
- **VPC Sessions**: Secure isolated network environments
- **Screenshot Download**: Capture and download screenshots

### [Browser Use](browser-use/)

Cloud-based browser automation with Playwright integration.

**Key Features:**
- Cookie and session persistence
- Stealth mode to avoid detection
- CAPTCHA handling capabilities
- Browser extension support
- AI-powered automation
- Proxy configuration

**Use Cases:**
- Web scraping and data extraction
- Automated testing
- Form filling and submission
- Game automation
- E-commerce automation

### [Computer Use](computer-use/)

Windows desktop automation for application control and window management.

**Key Features:**
- Application management (start, stop, list)
- Window operations (maximize, minimize, resize, close)
- Focus management
- Desktop UI automation
- Process monitoring

**Use Cases:**
- Desktop application testing
- Automated workflows
- Application monitoring
- UI automation

### [Mobile Use](mobile-use/)

Android mobile UI automation for app testing and gesture-based interactions.

**Key Features:**
- UI element detection and interaction
- Touch gestures (tap, swipe, scroll)
- Text input and key events
- Screenshot capture
- Mobile application management
- ADB integration

**Use Cases:**
- Mobile app testing
- UI automation
- Gesture-based interactions
- Screenshot verification

### [CodeSpace](codespace/)

Cloud-based development environment for code execution and scripting.

**Key Features:**
- Python code execution
- JavaScript/Node.js code execution
- Shell command execution
- File system operations
- Package management (pip, npm)

**Use Cases:**
- Automated testing
- Code validation
- Data processing
- CI/CD integration
- Educational tools

## 📋 Prerequisites

### Basic Requirements

- Python 3.8 or later
- AgentBay SDK: `pip install wuying-agentbay-sdk`
- Valid `AGENTBAY_API_KEY` environment variable

### Additional Requirements by Category

**Browser Use:**
```bash
pip install playwright
playwright install chromium
```

**All Others:**
No additional requirements beyond the basic SDK.

## 🎯 Running Examples

### Option 1: Using Installed Package (Recommended)

1. Install the SDK:
```bash
pip install wuying-agentbay-sdk
```

2. For browser examples, install Playwright:
```bash
playwright install chromium
```

3. Set your API key:
```bash
export AGENTBAY_API_KEY=your_api_key_here
```

4. Run any example:
```bash
python basic_usage.py
python common-features/basics/session_creation/main.py
python browser-use/browser/browser_stealth.py
python codespace/code_execution_example.py
```

### Option 2: Development from Source

1. Install dependencies:
```bash
cd python
poetry install
```

2. For browser examples, install Playwright:
```bash
poetry run playwright install chromium
```

3. Set your API key:
```bash
export AGENTBAY_API_KEY=your_api_key_here
```

4. Run examples with poetry:
```bash
poetry run python docs/examples/basic_usage.py
poetry run python docs/examples/common-features/basics/session_creation/main.py
```

## 💡 Common Patterns

### Basic Session Creation

```python
from agentbay import AgentBay
from agentbay.session_params import CreateSessionParams

# Initialize client
agent_bay = AgentBay(api_key="your_api_key")

# Create session
params = CreateSessionParams(image_id="linux_latest")
result = agent_bay.create(params)

if result.success:
    session = result.session
    # Use session...
    
    # Cleanup
    agent_bay.delete(session)
```

### File Operations

```python
# Write file
result = session.file_system.write_file("/tmp/test.txt", "content")

# Read file
result = session.file_system.read_file("/tmp/test.txt")
if result.success:
    print(result.content)
```

### Command Execution

```python
result = session.command.execute_command("ls -la")
if result.success:
    print(result.output)
```

### Browser Automation

```python
import asyncio
from agentbay.browser.browser import BrowserOption
from playwright.async_api import async_playwright

async def automate():
    # Initialize browser
    option = BrowserOption()
    await session.browser.initialize_async(option)
    
    # Connect Playwright
    endpoint_url = session.browser.get_endpoint_url()
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(endpoint_url)
        context = browser.contexts[0]
        page = await context.new_page()
        
        # Automate...
        await page.goto("https://example.com")
        
        await browser.close()

asyncio.run(automate())
```

### Code Execution

```python
# Python code
python_code = """
print("Hello from Python!")
"""
result = session.code.run_code(python_code, "python")

# JavaScript code
js_code = """
console.log("Hello from JavaScript!");
"""
result = session.code.run_code(js_code, "javascript")
```

## 🎓 Learning Path

### For Beginners

1. Start with [basic_usage.py](basic_usage.py)
2. Explore [Common Features - Basics](common-features/basics/)
3. Try environment-specific examples based on your use case

### For Experienced Developers

1. Review [Common Features](common-features/) for SDK capabilities
2. Jump to your specific environment:
   - [Browser Use](browser-use/) for web automation
   - [Computer Use](computer-use/) for desktop automation
   - [Mobile Use](mobile-use/) for mobile automation
   - [CodeSpace](codespace/) for code execution
3. Explore [Advanced Features](common-features/advanced/) for integrations

## 📖 Best Practices

1. **Always Clean Up**: Delete sessions when done to free resources
2. **Error Handling**: Check `result.success` before using data
3. **Use Labels**: Organize sessions with meaningful labels
4. **Context Sync**: Use context synchronization for data persistence
5. **Resource Limits**: Be aware of concurrent session limits
6. **Proper Cleanup**: Close connections and delete sessions properly
7. **API Key Security**: Never commit API keys to version control

## 🔍 Example Index

### By Use Case

**Web Automation:**
- Browser stealth mode: `browser-use/browser/browser_stealth.py`
- Cookie persistence: `browser-use/browser/browser_context_cookie_persistence.py`
- AI-powered automation: `browser-use/browser/search_agentbay_doc_by_agent.py`

**Desktop Automation:**
- Application management: `computer-use/computer/windows_app_management_example.py`

**Mobile Automation:**
- Mobile UI automation: `mobile-use/mobile_system/main.py`
- ADB integration: `mobile-use/mobile_get_adb_url_example.py`

**Code Execution:**
- Python/JavaScript execution: `codespace/code_execution_example.py`

**Data Management:**
- File operations: `common-features/basics/file_system/main.py`
- Context management: `common-features/basics/context_management/main.py`
- Data persistence: `common-features/basics/data_persistence/main.py`

**Session Management:**
- Session pause and resume: `common-features/basics/session_pause_resume/main.py`

**Advanced Features:**
- AI Agent: `common-features/advanced/agent_module/main.py`
- OSS integration: `common-features/advanced/oss_management/main.py`
- VPC sessions: `common-features/advanced/vpc_session/main.py`

## 🆘 Troubleshooting

### Resource Creation Delay

If you see "The system is creating resources" message:
- Wait 90 seconds and retry
- This is normal for resource initialization
- Consider using session pooling for production

### API Key Issues

Ensure your API key is properly set:
```bash
export AGENTBAY_API_KEY=your_api_key_here
# Verify
echo $AGENTBAY_API_KEY
```

### Import Errors

If you get import errors:
```bash
# Ensure SDK is installed
pip install wuying-agentbay-sdk

# Or for development
cd python
poetry install
```

### Browser Examples Not Working

For browser examples:
```bash
# Install Playwright
pip install playwright
playwright install chromium
```

## 📚 Related Documentation

- [Python SDK Documentation](../../)
- [API Reference](../api/)
- [Quick Start Guide](../../../docs/quickstart/README.md)
- [Feature Guides](../../../docs/guides/README.md)
- [Common Features Guide](../../../docs/guides/common-features/README.md)
- [Browser Use Guide](../../../docs/guides/browser-use/README.md)
- [Computer Use Guide](../../../docs/guides/computer-use/README.md)
- [Mobile Use Guide](../../../docs/guides/mobile-use/README.md)
- [CodeSpace Guide](../../../docs/guides/codespace/README.md)

## 🤝 Getting Help

- [GitHub Issues](https://github.com/aliyun/wuying-agentbay-sdk/issues)
- [Documentation](../../../docs/README.md)

---

💡 **Tip**: Start with `basic_usage.py` for a quick overview, then explore category-specific examples based on your needs.

