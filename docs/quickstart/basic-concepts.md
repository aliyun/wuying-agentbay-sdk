# Core Concepts

Before we start programming, let's understand several core concepts of AgentBay.

## 🌐 What is AgentBay?

AgentBay is a cloud computing environment. You can think of it as:
- A remote virtual machine (supporting Linux, Windows, Android)
- Can be created and destroyed at any time
- Has a complete file system and command-line environment
- Supports running various programs and scripts

### Supported Image Types
- **Linux Images**: Ubuntu and other Linux distributions, suitable for development, deployment, data processing
- **Windows Images**: Windows Server, suitable for .NET development, Windows application testing
- **Android Images**: Android system, suitable for mobile app testing, automation

## 🔗 Session

### Concept
A session is a connection between you and the cloud environment, similar to:
- SSH connection to a remote server
- Opening a terminal window
- Starting a Docker container

### Features
```python
# Create session (default Linux image)
session = agent_bay.create().session

# Create session with specific operating system
from agentbay.session_params import CreateSessionParams

# Linux image
linux_params = CreateSessionParams(image_id="linux_latest")
linux_session = agent_bay.create(linux_params).session

# Windows image
windows_params = CreateSessionParams(image_id="windows_latest")
windows_session = agent_bay.create(windows_params).session

# Android image
android_params = CreateSessionParams(image_id="android_latest")
android_session = agent_bay.create(android_params).session

# Sessions have independent:
# - File system (varies by image type)
# - Process space (can run programs)
# - Network environment (can access internet)
```

### Lifecycle
```
Create Session → Use Session → Session Timeout/Active Close
      ↓             ↓              ↓
  Allocate      Execute         Release
  Resources     Operations      Resources
```

## 📁 File System

### Directory Structure
The file system structure depends on the cloud image type you choose:

#### Linux Images
```
/
├── tmp/          # Temporary files (cleared after session ends)
├── home/         # User directory
├── mnt/          # Mount points (for persistent data)
├── etc/          # System configuration
├── var/          # Variable data
└── ...           # Other standard Linux directories
```

#### Windows Images
```
C:\
├── Users\        # User directory
├── Windows\      # System files
├── Program Files\ # Program files
├── temp\         # Temporary files
└── ...           # Other Windows directories
```

#### Android Images
```
/
├── data/         # Application data
├── system/       # System files
├── storage/      # Storage directory
├── tmp/          # Temporary files
└── ...           # Other Android directories
```

### File Operations
File operations vary depending on the operating system image:

#### Linux/Android
```python
# Write file
session.filesystem.write("/tmp/hello.txt", "Hello World")

# Read file
content = session.filesystem.read("/tmp/hello.txt")
print(content.data)  # Hello World

# List directory
files = session.filesystem.list("/tmp")
for file in files.data:
    print(file.name)
```

#### Windows
```python
# Write file
session.filesystem.write("C:\\temp\\hello.txt", "Hello World")

# Read file
content = session.filesystem.read("C:\\temp\\hello.txt")
print(content.data)  # Hello World

# List directory
files = session.filesystem.list("C:\\temp")
for file in files.data:
    print(file.name)
```

## ⚡ Command Execution

### Linux/Android Commands
```python
# Basic commands
result = session.command.execute("ls -la")
result = session.command.execute("pwd")
result = session.command.execute("whoami")

# Install packages
result = session.command.execute("apt-get update")
result = session.command.execute("apt-get install -y python3-pip")

# Run Python
result = session.command.execute("python3 -c 'print(\"Hello from Python\")'")
```

### Windows Commands
```python
# Basic commands
result = session.command.execute("dir")
result = session.command.execute("cd")
result = session.command.execute("whoami")

# PowerShell commands
result = session.command.execute("powershell Get-Process")
result = session.command.execute("powershell Get-Location")

# Run programs
result = session.command.execute("python --version")
```

### Android Commands
```python
# Android-specific commands
result = session.command.execute("am start -n com.android.settings/.Settings")
result = session.command.execute("input tap 500 500")
result = session.command.execute("screencap /tmp/screenshot.png")

# Package management
result = session.command.execute("pm list packages")
result = session.command.execute("pm install /tmp/app.apk")
```

## 🔄 Data Persistence

### Temporary Data
- Stored in session file system
- **Lost when session ends**
- Suitable for: temporary processing, cache files

```python
# Temporary data - will be lost
session.filesystem.write("/tmp/temp_data.txt", "temporary content")
```

### Persistent Data (Context)
- Stored in AgentBay's persistent storage
- **Preserved across sessions**
- Suitable for: configuration files, user data, project files

```python
from agentbay import ContextSync, SyncPolicy

# Create persistent context
context = agent_bay.context.get("my-project", create=True).context

# Configure sync policy
sync_policy = SyncPolicy.default()
context_sync = ContextSync.new(context.id, "/mnt/data", sync_policy)

# Create session with persistent data
from agentbay import CreateSessionParams
params = CreateSessionParams(context_syncs=[context_sync])
session = agent_bay.create(params).session

# Data written to /mnt/data will persist
session.filesystem.write("/mnt/data/config.json", '{"setting": "value"}')
```

## 🏷️ Labels and Organization

### Session Labels
Use labels to organize and find sessions:

```python
# Create session with labels
params = CreateSessionParams(
    labels={
        "project": "web-scraper",
        "environment": "development",
        "owner": "john.doe"
    }
)
session = agent_bay.create(params).session

# Find sessions by labels
sessions = agent_bay.list_by_labels({"project": "web-scraper"})
for session_info in sessions.data:
    print(f"Session: {session_info.session_id}")
```

## 🌍 Network Access

### Internet Access
All sessions have internet access by default:

```python
# Download files
session.command.execute("wget https://example.com/file.txt")

# Use curl
session.command.execute("curl -s https://api.github.com/users/octocat")

# Python requests
code = """
import requests
response = requests.get('https://httpbin.org/json')
print(response.json())
"""
session.code.run_code(code, "python")
```

### Port Access
For applications that start services:

```python
# Start a web server
session.command.execute("python3 -m http.server 8000 &")

# Get access link
link_result = session.get_link("http", 8000)
if link_result.success:
    print(f"Access your server at: {link_result.data}")
```

## 🔐 Security Model

### Isolation
- Each session is completely isolated
- Cannot access other users' sessions
- Cannot access local files on your machine

### Data Security
- All data transmission uses HTTPS encryption
- Context data is encrypted at rest
- Temporary data is automatically cleaned up

### Best Practices
```python
# ✅ Good - Use environment variables
import os
api_key = os.getenv('AGENTBAY_API_KEY')

# ❌ Bad - Hardcode sensitive data
api_key = "your-secret-key"  # Never do this!
```

## 🚀 Next Steps

Now that you understand the core concepts:

1. **Try the examples**: Each concept has working code examples
2. **Create your first session**: Follow the [First Session Guide](first-session.md)
3. **Learn best practices**: Check out [Best Practices](best-practices.md)
4. **Explore advanced features**: Browse the [Feature Guides](../guides/README.md)

Remember: AgentBay gives you the power of cloud computing with the simplicity of local development! 