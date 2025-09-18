# Troubleshooting Guide

This guide helps you quickly diagnose and resolve common issues encountered when using the AgentBay SDK.

## 🚨 Emergency Issue Quick Diagnosis

### Step 1: Basic Check
Run the following diagnostic code to quickly identify issues:

```python
import os
from agentbay import AgentBay

def quick_diagnosis():
    print("=== AgentBay Quick Diagnosis ===")

    # 1. Check API Key
    api_key = os.getenv('AGENTBAY_API_KEY')
    if not api_key:
        print("❌ AGENTBAY_API_KEY environment variable not set")
        return False
    else:
        print(f"✅ API key set (length: {len(api_key)})")

    # 2. Initialize Client
    try:
        agent_bay = AgentBay()
        print("✅ AgentBay client initialized successfully")
        print("ℹ️  Note: Creating AgentBay client does not establish a connection")
    except Exception as e:
        print(f"❌ Client initialization failed: {e}")
        return False

    # 3. Test Session Creation
    try:
        result = agent_bay.create()
        if not result.success:
            print(f"❌ Session creation failed: {result.error_message}")
            return False
        else:
            print("✅ Session created successfully")
            session = result.session
    except Exception as e:
        print(f"❌ Session creation exception: {e}")
        return False

    # 4. Test Basic Commands
    try:
        cmd_result = session.command.execute_command("echo 'Hello AgentBay'")
        if not cmd_result.success:
            print(f"❌ Command execution failed: {cmd_result.error_message}")
            return False
        else:
            print("✅ Command executed successfully")
            print(f"   Output: {cmd_result.output}")
    except Exception as e:
        print(f"❌ Command execution exception: {e}")
        return False

    print("🎉 All basic checks passed!")
    return True


# Run diagnosis
quick_diagnosis()
```

## 📋 Common Issues and Solutions

### 1. Authentication Issues

#### Problem: "API key not found" or "Invalid credentials"
**Cause**: Missing or incorrect API key configuration

**Solution**:
```bash
# Check if environment variable is set
echo $AGENTBAY_API_KEY

# Set API key (temporary)
export AGENTBAY_API_KEY=your_actual_api_key

# Or set it in your code
from agentbay import AgentBay
agent_bay = AgentBay(api_key="your_actual_api_key")
```

#### Problem: "Permission denied" or "Access forbidden"
**Cause**: API key lacks required permissions

**Solution**:
1. Verify your API key has the correct permissions in the AgentBay console
2. Contact your administrator to grant necessary permissions

### 2. Network and Connectivity Issues

#### Problem: "Connection timeout" or "Network error"
**Cause**: Network connectivity issues or firewall restrictions

**Solution**:
```python
# Test basic connectivity
import requests
try:
    response = requests.get("https://agentbay.aliyun.com/health", timeout=10)
    print(f"Connectivity test: {response.status_code}")
except Exception as e:
    print(f"Connectivity test failed: {e}")
```

#### Problem: "DNS resolution failed"
**Cause**: DNS configuration issues

**Solution**:
1. Check your DNS settings
2. Try using a different DNS server (e.g., 8.8.8.8)
3. Verify you can access other websites

### 3. Session Management Issues

#### Problem: "Session creation failed"
**Cause**: Resource limits or service availability issues

**Solution**:
```python
# Check your session quota
from agentbay import AgentBay
agent_bay = AgentBay()

# List existing sessions and clean up if needed
try:
    sessions = agent_bay.list()
    print(f"Current sessions: {len(sessions)}")

    # Clean up old sessions if needed
    for session in sessions[:3]:  # Clean up first 3 as example
        try:
            delete_result = agent_bay.delete(session)
            if delete_result.success:
                print(f"Deleted session: {session.session_id}")
            else:
                print(f"Failed to delete session {session.session_id}: {delete_result.error_message}")
        except Exception as e:
            print(f"Failed to delete session {session.session_id}: {e}")
except Exception as e:
    print(f"Failed to list sessions: {e}")
```

#### Problem: "Session not found" or "Session expired"
**Cause**: Session was terminated or timed out

**Solution**:
```python
# Implement session recreation logic
def get_or_create_session(agent_bay):
    try:
        # Try to create new session
        result = agent_bay.create()
        if result.success:
            return result.session
        else:
            print(f"Failed to create session: {result.error_message}")
            return None
    except Exception as e:
        print(f"Exception creating session: {e}")
        return None

# Usage
session = get_or_create_session(agent_bay)
```

### 4. File Operation Issues

#### Problem: "File not found" or "Permission denied"
**Cause**: Incorrect file paths or insufficient permissions

**Solution**:
```python
# Check if directory exists and is writable
import os

def check_file_access(session, path):
    try:
        # Check if directory exists
        dir_path = os.path.dirname(path)
        cmd_result = session.command.execute_command(f"mkdir -p {dir_path}")
        if not cmd_result.success:
            print(f"Failed to create directory: {cmd_result.error_message}")
            return False

        # Test write access
        test_content = "test"
        write_result = session.file_system.write_file(path, test_content)
        if not write_result.success:
            print(f"Write failed: {write_result.error_message}")
            return False

        # Clean up test file
        session.file_system.delete_file(path)
        return True
    except Exception as e:
        print(f"File access check failed: {e}")
        return False

# Usage
if check_file_access(session, "/tmp/test.txt"):
    print("File operations working correctly")
```

#### Problem: "File too large" or "Upload failed"
**Cause**: File size limits or network issues

**Solution**:
Instead of manually handling file chunking, use the SDK's built-in large file operations:

```python
# For reading large files, use read_large_file
def read_large_file_example(session, path):
    try:
        # read_large_file automatically handles chunking for large files
        result = session.file_system.read_large_file(path)
        if result.success:
            print(f"Successfully read large file: {len(result.content)} characters")
            return result.content
        else:
            print(f"Failed to read large file: {result.error_message}")
            return None
    except Exception as e:
        print(f"Error reading large file: {e}")
        return None

# For writing large files, use write_large_file
def write_large_file_example(session, path, content):
    try:
        # write_large_file automatically handles chunking for large files
        result = session.file_system.write_large_file(path, content)
        if result.success:
            print("Successfully wrote large file")
            return True
        else:
            print(f"Failed to write large file: {result.error_message}")
            return False
    except Exception as e:
        print(f"Error writing large file: {e}")
        return False

# Usage
large_content = "A" * (1024 * 1024 * 5)  # 5MB of data
if write_large_file_example(session, "/tmp/large_file.txt", large_content):
    content = read_large_file_example(session, "/tmp/large_file.txt")
    if content:
        print(f"Verified content length: {len(content)}")
```

### 5. Command Execution Issues

#### Problem: "Command not found" or "Executable not found"
**Cause**: Missing software or incorrect command syntax

**Solution**:
```python
# Check if command exists before executing
def check_command_exists(session, command):
    cmd_result = session.command.execute_command(f"which {command}")
    return cmd_result.success

# Install missing packages
def install_package(session, package_name):
    # For Ubuntu/Debian
    cmd_result = session.command.execute_command(f"apt-get update && apt-get install -y {package_name}")
    if not cmd_result.success:
        print(f"Failed to install {package_name}: {cmd_result.error_message}")
        return False
    return True

# Usage
if not check_command_exists(session, "curl"):
    print("Installing curl...")
    install_package(session, "curl")
```

#### Problem: "Command timeout" or "Process killed"
**Cause**: Long-running commands or resource constraints

**Solution**:
```python
# Use appropriate timeouts
# For quick commands, use shorter timeout
quick_cmd_result = session.command.execute_command("ls -la", timeout_ms=30000)

# For long-running commands, use longer timeout
long_cmd_result = session.command.execute_command("find / -name '*.log'", timeout_ms=300000)

# For very long operations, consider breaking them into steps
def process_large_dataset(session):
    # Step 1: Prepare data
    session.command.execute_command("mkdir -p /tmp/processing")

    # Step 2: Process in chunks
    for i in range(10):
        cmd_result = session.command.execute_command(
            f"process_chunk.sh {i}",
            timeout_ms=60000
        )
        if not cmd_result.success:
            print(f"Chunk {i} failed: {cmd_result.error_message}")
            # Decide whether to continue or abort
```

### 6. Agent Execution Issues
#### Problem: "tool by name flux_execute_task not found"
**Cause**: Currently only specific image_id and task can be used, only pre-release environment supports this tool

**Solution**: Use image_id as windows_latest:
```python
from agentbay import AgentBay
from agentbay.session_params import CreateSessionParams
# Create a session for Agent module usage
agent_bay = AgentBay(api_key=api_key)
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
# Execute a task using natural language
task_description = "your_task_description"
execution_result = agent_session.agent.execute_task(task_description, max_try_times=5)

if execution_result.success:
    print("Task completed successfully!")
    print(f"Task ID: {execution_result.task_id}")
    print(f"Task status: {execution_result.task_status}")
else:
    print(f"Task failed: {execution_result.error_message}")
agent_bay.delete(agent_session)
```

## 🔧 Advanced Debugging

### Enable Detailed Logging
```python
import logging
import os

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)
os.environ['AGENTBAY_DEBUG'] = 'true'

# Initialize with debug mode
agent_bay = AgentBay(debug=True)
```

### Capture and Analyze Error Details
```python
def detailed_error_analysis(result):
    if not result.success:
        print(f"Error Type: {type(result.error_message)}")
        print(f"Error Message: {result.error_message}")
        print(f"Error Code: {getattr(result, 'error_code', 'N/A')}")
        print(f"Request ID: {getattr(result, 'request_id', 'N/A')}")

        # Check if it's a network issue
        if "timeout" in str(result.error_message).lower():
            print("💡 This appears to be a network timeout issue")
        elif "permission" in str(result.error_message).lower():
            print("💡 This appears to be a permission issue")
        elif "not found" in str(result.error_message).lower():
            print("💡 This appears to be a resource not found issue")
```

## 📊 Performance Optimization

### Session Reuse
```python
# Reuse sessions for multiple operations instead of creating new ones
class SessionManager:
    def __init__(self):
        self.agent_bay = AgentBay()
        self.session = None

    def get_session(self):
        if not self.session:
            result = self.agent_bay.create()
            if result.success:
                self.session = result.session
        return self.session

    def cleanup(self):
        if self.session:
            self.agent_bay.delete(self.session)

# Usage
manager = SessionManager()
session = manager.get_session()
# Perform multiple operations with the same session
manager.cleanup()
```

### Batch Operations
```python
# Use batch operations when possible
def batch_file_operations(session, operations):
    results = []
    for op in operations:
        if op['type'] == 'write':
            result = session.file_system.write_file(op['path'], op['content'])
        elif op['type'] == 'read':
            result = session.file_system.read_file(op['path'])
        results.append(result)
    return results
```

## 📞 Getting Help

If you're still experiencing issues after trying these solutions:

1. **Review the [Documentation](../README.md)** for detailed information
2. **Search [GitHub Issues](https://github.com/aliyun/wuying-agentbay-sdk/issues)** for similar problems
3. **Create a new issue** with:
   - Detailed error messages
   - Code snippets that reproduce the issue
   - Environment information (SDK version, Python/Node.js/Go version, etc.)
   - Steps you've already tried

## 🎯 Quick Reference

| Issue | Quick Solution |
|-------|----------------|
| API Key Issues | `export AGENTBAY_API_KEY=your_key` |
| Session Creation Failed | Check quota and clean up old sessions |
| File Operations Failed | Verify paths and permissions |
| Command Timeout | Increase timeout or break into smaller steps |
| Network Issues | Test connectivity and check firewall settings |

Remember: Most issues can be resolved by checking your API key, network connectivity, and session management practices! 🚀
