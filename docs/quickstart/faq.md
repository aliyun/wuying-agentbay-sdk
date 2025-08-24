# Frequently Asked Questions (FAQ)

This section collects the most common questions and answers that new users encounter. If your question isn't here, please check the [Troubleshooting Guide](troubleshooting.md) or submit a [GitHub Issue](https://github.com/aliyun/wuying-agentbay-sdk/issues).

## 🚀 Getting Started

### Q: What is AgentBay? How is it different from Docker?
**A:** AgentBay is a cloud execution environment service that allows you to run commands, code, and automation tasks in the cloud. Key differences from Docker:

| Feature | AgentBay | Docker |
|---------|----------|--------|
| Deployment | Cloud-hosted, ready to use | Requires local installation and configuration |
| Scalability | Auto-scaling | Manual resource management |
| Persistence | Built-in context system | Requires volume mounting configuration |
| Networking | Built-in network features | Requires network configuration |
| Use Case | Automation tasks, AI workflows | Application containerization |

### Q: Do I need to install any software?
**A:** No! AgentBay is completely cloud-based. You only need:
- Install the SDK package for your language (`pip install wuying-agentbay-sdk`)
- Get an API key
- Write code to call the API

### Q: Where can I get an API key?
**A:** 
1. Visit the [AgentBay Console](https://agentbay.console.aliyun.com/service-management)
2. Register or log in to your Alibaba Cloud account
3. Create an API key in the service management page
4. Set the key as an environment variable: `export AGENTBAY_API_KEY=your-key-here`

### Q: Which programming languages are supported?
**A:** Currently supported:
- **Python** - `pip install wuying-agentbay-sdk`
- **TypeScript/JavaScript** - `npm install wuying-agentbay-sdk`
- **Golang** - `go get github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay`

## 🔧 Usage

### Q: What is a session? Why do I need to create a session?
**A:** A session is an independent working environment in the cloud, similar to a virtual machine instance. Each session has:
- Independent file system
- Independent process space
- Independent network environment
- Optional persistent storage

You need to create a session first, then execute commands, run code, and perform other operations within the session.

### Q: Will sessions be automatically deleted? Will my data be lost?
**A:** 
- **Sessions themselves**: Will be automatically recycled after a period of inactivity
- **Session data**: Temporary data will be lost, but you can use the context system for persistence
- **Context data**: Will be preserved and can be accessed across different sessions

**Recommendation**: Use the context system to save important data.

### Q: How many sessions can I create? Are there limits?
**A:** 
- **Concurrent sessions**: Each account has a concurrent session limit (usually 10-50)
- **Daily creation**: There's a daily session creation limit
- **Resource usage**: Each session consumes computing resources

**Tip**: Reuse sessions when possible instead of creating new ones frequently.

### Q: Can I access the internet from sessions?
**A:** Yes! Sessions have internet access by default and can:
- Download files and packages
- Access APIs and web services
- Clone Git repositories
- Install software packages

## 📁 File Operations

### Q: How do I upload files to a session?
**A:** Multiple ways:
```python
# Method 1: Upload single file
session.filesystem.upload_file("local_file.txt", "/remote/path/file.txt")

# Method 2: Upload multiple files
session.filesystem.upload_files(["file1.txt", "file2.txt"], "/remote/dir/")

# Method 3: Write content directly
session.filesystem.write("/remote/path/file.txt", "file content")
```

### Q: How do I download files from a session?
**A:** 
```python
# Method 1: Download single file
session.filesystem.download_file("/remote/file.txt", "local_file.txt")

# Method 2: Read file content
content = session.filesystem.read("/remote/file.txt")
print(content.data)
```

### Q: What's the maximum file size I can upload?
**A:** 
- **Small files** (< 10MB): Use direct upload methods
- **Large files** (> 10MB): Automatically chunked, supports up to 5GB
- **Very large files**: Consider using OSS integration

### Q: Do files persist after session deletion?
**A:** 
- **Session files**: Deleted with the session
- **Context files**: Persist and can be accessed by new sessions
- **OSS files**: Persist independently

## 🔧 Command Execution

### Q: Can I run interactive commands?
**A:** AgentBay is designed for non-interactive commands. For interactive scenarios:
```python
# ❌ Won't work well
result = session.command.execute("python")  # Hangs waiting for input

# ✅ Better approach
result = session.command.execute("python script.py")
# or
result = session.code.run_code("print('Hello')", "python")
```

### Q: How do I handle long-running commands?
**A:** 
```python
# Set appropriate timeout
result = session.command.execute(
    "npm install",  # Long-running command
    timeout_ms=300000  # 5 minutes
)

# For very long tasks, consider breaking them down
commands = [
    "git clone https://github.com/user/repo.git",
    "cd repo",
    "npm install",
    "npm run build"
]
for cmd in commands:
    result = session.command.execute(cmd, timeout_ms=120000)
    if result.is_error:
        print(f"Command failed: {cmd}")
        break
```

### Q: Can I run commands in the background?
**A:** Currently, all commands run synchronously. For background-like behavior:
```python
# Start a service and continue
session.command.execute("nohup python server.py > server.log 2>&1 &")

# Check if it's running
result = session.command.execute("ps aux | grep python")
```

## 🐍 Python-Specific

### Q: How do I install Python packages?
**A:** 
```python
# Method 1: Using command execution
result = session.command.execute("pip install requests numpy")

# Method 2: Using code execution with installation
code = """
import subprocess
subprocess.run(['pip', 'install', 'requests'], check=True)
import requests
print(requests.__version__)
"""
result = session.code.run_code(code, "python")
```

### Q: How do I run Python scripts?
**A:** 
```python
# Method 1: Upload script and run
session.filesystem.upload_file("my_script.py", "/tmp/my_script.py")
result = session.command.execute("python /tmp/my_script.py")

# Method 2: Run code directly
code = """
def hello(name):
    return f"Hello, {name}!"

print(hello("AgentBay"))
"""
result = session.code.run_code(code, "python")
print(result.data.output)
```

### Q: How do I handle Python virtual environments?
**A:** 
```python
# Create and use virtual environment
commands = [
    "python -m venv /tmp/myenv",
    "source /tmp/myenv/bin/activate && pip install requests",
    "source /tmp/myenv/bin/activate && python my_script.py"
]

for cmd in commands:
    result = session.command.execute(cmd)
    if result.is_error:
        print(f"Failed: {cmd}")
        break
```

## 🌐 TypeScript/JavaScript

### Q: How do I run Node.js applications?
**A:** 
```typescript
// Install Node.js packages
await session.command.executeCommand("npm install express");

// Run Node.js script
const code = `
const express = require('express');
const app = express();
app.get('/', (req, res) => res.send('Hello AgentBay!'));
console.log('Server ready');
`;

const result = await session.code.runCode(code, "javascript");
```

### Q: How do I handle npm package installation?
**A:** 
```typescript
// Method 1: Direct npm install
await session.command.executeCommand("npm install lodash axios");

// Method 2: Using package.json
const packageJson = {
  "dependencies": {
    "lodash": "^4.17.21",
    "axios": "^0.24.0"
  }
};

await session.filesystem.write("/tmp/package.json", JSON.stringify(packageJson, null, 2));
await session.command.executeCommand("cd /tmp && npm install");
```

## 🐹 Golang

### Q: How do I run Go programs?
**A:** 
```go
// Upload Go source file
session.FileSystem.UploadFile("main.go", "/tmp/main.go")

// Run Go program
result, err := session.Command.ExecuteCommand("cd /tmp && go run main.go")
if err != nil {
    log.Printf("Error: %v", err)
}
fmt.Println(result.Output)
```

### Q: How do I handle Go modules?
**A:** 
```go
// Initialize Go module
session.Command.ExecuteCommand("cd /tmp && go mod init myapp")

// Add dependencies
session.Command.ExecuteCommand("cd /tmp && go get github.com/gin-gonic/gin")

// Run with dependencies
session.Command.ExecuteCommand("cd /tmp && go run main.go")
```

## 🔧 Troubleshooting

### Q: I'm getting "Session not found" errors
**A:** This usually means:
1. The session was automatically deleted due to inactivity
2. You're using an invalid session ID
3. Network connectivity issues

**Solution**: Create a new session and retry.

### Q: Commands are timing out
**A:** 
1. **Increase timeout**: Set a longer `timeout_ms` value
2. **Break down commands**: Split long operations into smaller steps
3. **Check command**: Ensure the command doesn't require interactive input

### Q: File upload/download is failing
**A:** 
1. **Check file paths**: Ensure paths are correct and accessible
2. **Check file size**: Large files may need special handling
3. **Check permissions**: Ensure you have read/write permissions

### Q: Getting authentication errors
**A:** 
1. **Check API key**: Ensure `AGENTBAY_API_KEY` is set correctly
2. **Check key validity**: API keys may expire or be revoked
3. **Check account status**: Ensure your account is active

## 💡 Best Practices

### Q: How should I structure my AgentBay applications?
**A:** 
```python
# Good structure
class AgentBayManager:
    def __init__(self):
        self.agent_bay = AgentBay()
        self.session = None
    
    def __enter__(self):
        self.session = self.agent_bay.create().session
        return self.session
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            self.agent_bay.delete(self.session)

# Usage
with AgentBayManager() as session:
    result = session.command.execute("echo 'Hello'")
    print(result.data.stdout)
```

### Q: How do I handle errors properly?
**A:** 
```python
try:
    result = session.command.execute("risky-command")
    if result.is_error:
        # Handle command-level errors
        print(f"Command failed: {result.error}")
    else:
        # Process successful result
        print(result.data.stdout)
except AgentBayError as e:
    # Handle SDK-level errors
    print(f"SDK error: {e}")
except Exception as e:
    # Handle unexpected errors
    print(f"Unexpected error: {e}")
```

### Q: When should I use context vs regular files?
**A:** 
- **Use context for**: Configuration files, user data, persistent state
- **Use regular files for**: Temporary files, processing data, logs

### Q: How do I optimize performance?
**A:** 
1. **Reuse sessions**: Don't create new sessions for each operation
2. **Batch operations**: Combine multiple commands when possible
3. **Use appropriate timeouts**: Don't set unnecessarily long timeouts
4. **Clean up resources**: Delete sessions when done

## 🆘 Getting More Help

If you still have questions:

1. **Check the documentation**: [Complete Documentation](../README.md)
2. **Browse examples**: Look at code examples in the repository
3. **Search issues**: Check existing [GitHub Issues](https://github.com/aliyun/wuying-agentbay-sdk/issues)
4. **Create an issue**: If you can't find an answer, create a new issue

Remember: The AgentBay community is here to help! 🚀 