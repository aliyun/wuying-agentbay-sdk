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
android_params = CreateSessionParams(image_id="mobile_latest")
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
└── ...           # Other Windows directories
```

#### Android Images
```
/
├── data/         # Application data
├── system/       # System files
├── storage/      # Storage directory
└── ...           # Other Android directories
```

### File Operations
File operations vary depending on the operating system image:

#### Linux/Android
```python
# Write file
session.filesystem.write_file("/tmp/hello.txt", "Hello World")

# Read file
content = session.filesystem.read_file("/tmp/hello.txt")
print(content.content)  # Hello World

# List directory
files = session.filesystem.list_directory("/tmp")
for file in files.entries:
    print(file.name)
```

#### Windows
```python
# Write file
session.filesystem.write_file("C:\\Users\\hello.txt", "Hello World")

# Read file
content = session.filesystem.read_file("C:\\Users\\hello.txt")
print(content.content)  # Hello World

# List directory
files = session.filesystem.list_directory("C:\\Users")
for file in files.entries:
    print(file.name)
```

## ⚡ Command Execution

### Linux/Android Commands
```python
# Basic commands
result = session.command.execute_command("ls -la")
result = session.command.execute_command("pwd")
result = session.command.execute_command("whoami")

# Install packages
result = session.command.execute_command("apt-get update")
result = session.command.execute_command("apt-get install -y python3-pip")

# Run Python
result = session.command.execute_command("python3 -c 'print(\"Hello from Python\")'")
```

### Windows Commands
```python
# Basic commands
result = session.command.execute_command("dir")
result = session.command.execute_command("cd")
result = session.command.execute_command("whoami")

# PowerShell commands
result = session.command.execute_command("powershell -Command \"Get-Process | Select-Object -First 5\"")
result = session.command.execute_command("powershell -Command \"Get-Location\"")
result = session.command.execute_command("powershell -Command \"Get-Date\"")

# Run programs
result = session.command.execute_command("python --version")
```

### Android Commands
```python
# Android-specific commands
result = session.command.execute_command("am start -n com.android.settings/.Settings")
result = session.command.execute_command("input tap 500 500")
result = session.command.execute_command("screencap /tmp/screenshot.png")

# Package management
result = session.command.execute_command("pm list packages")
result = session.command.execute_command("pm install /tmp/app.apk")
```

## 🔄 Data Persistence

### Temporary Data
- Stored in session file system
- **Lost when session ends**
- Suitable for: temporary processing, cache files

```python
# Temporary data - will be lost
# For Linux/Android:
session.filesystem.write_file("/tmp/temp_data.txt", "temporary content")
# For Windows:
session.filesystem.write_file("C:\\Users\\temp_data.txt", "temporary content")
```

### Persistent Data (Context)
- Stored in AgentBay's persistent storage
- **Preserved across sessions**
- Suitable for: configuration files, user data, project files

```python
from agentbay import ContextSync, SyncPolicy

# Create persistent context
context = agent_bay.context.get("my-project", create=True).context

# Create context sync (sync_policy is optional)
context_sync = ContextSync.new(context.id, "/tmp/data")

# Create session with persistent data
from agentbay import CreateSessionParams
params = CreateSessionParams(context_syncs=[context_sync])
session = agent_bay.create(params).session

# Data written to /tmp/data will persist
session.filesystem.write_file("/tmp/data/config.json", '{"setting": "value"}')
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
for session_info in sessions.sessions:
    print(f"Session: {session_info.session_id}")
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