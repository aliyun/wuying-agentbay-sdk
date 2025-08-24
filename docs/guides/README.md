# Feature Guides

Welcome to the AgentBay SDK Feature Guides! This provides complete functionality introduction and best practices for experienced developers.

## 🎯 Quick Navigation

### Core Features
- [Session Management](session-management.md) - Create, connect, and manage cloud sessions
- [File Operations](file-operations.md) - Upload, download, and manipulate files
- [Data Persistence](data-persistence.md) - Persistent data storage and synchronization
- [Automation](automation.md) - Command execution and workflow automation
- [Advanced Features](advanced-features.md) - Advanced capabilities and integrations

## 🚀 API Quick Reference

### Basic Operations
```python
# Create session
agent_bay = AgentBay()
session = agent_bay.create().session

# Execute command
result = session.command.execute("ls -la")

# File operations
session.filesystem.write("/path/file.txt", "content")
content = session.filesystem.read("/path/file.txt").data
```

### Persistent Storage
```python
# Create context
context = agent_bay.context.get("project-name", create=True).context

# Create session with context
context_sync = ContextSync.new(context.id, "/mnt/data", SyncPolicy.default())
session = agent_bay.create(CreateSessionParams(context_syncs=[context_sync])).session
```

### Code Execution
```python
# Python code
result = session.code.run_code("print('Hello World')", "python")

# JavaScript code
result = session.code.run_code("console.log('Hello')", "javascript")
```

### UI Automation
```python
# Click element
session.ui.click("button[type='submit']")

# Input text
session.ui.type("#username", "myuser")

# Wait for element
session.ui.wait_for_element(".loading", visible=False)
```

### Browser Automation
```python
# Navigate to page
session.browser.navigate("https://example.com")

# Take screenshot
screenshot = session.browser.screenshot()

# Execute JavaScript
result = session.browser.execute_script("return document.title")
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

## 🎯 Use Case Examples

### Web Scraping
```python
# Create session with browser
session = agent_bay.create().session

# Navigate and extract data
session.browser.navigate("https://example.com")
data = session.browser.execute_script("""
    return Array.from(document.querySelectorAll('.item')).map(el => el.textContent)
""")
```

### Data Processing
```python
# Upload data file
session.filesystem.upload_file("data.csv", "/tmp/data.csv")

# Process with Python
code = """
import pandas as pd
df = pd.read_csv('/tmp/data.csv')
result = df.groupby('category').sum()
result.to_csv('/tmp/result.csv')
"""
session.code.run_code(code, "python")

# Download result
session.filesystem.download_file("/tmp/result.csv", "result.csv")
```

### CI/CD Integration
```python
# Clone repository
session.command.execute("git clone https://github.com/user/repo.git")

# Run tests
result = session.command.execute("cd repo && npm test")

# Deploy if tests pass
if result.success:
    session.command.execute("cd repo && npm run deploy")
```

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