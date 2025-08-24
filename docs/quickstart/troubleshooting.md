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
    
    # 2. Test Connection
    try:
        agent_bay = AgentBay()
        print("✅ AgentBay client initialized successfully")
    except Exception as e:
        print(f"❌ Client initialization failed: {e}")
        return False
    
    # 3. Test Session Creation
    try:
        result = agent_bay.create()
        if result.is_error:
            print(f"❌ Session creation failed: {result.error}")
            return False
        else:
            print("✅ Session created successfully")
            session = result.session
    except Exception as e:
        print(f"❌ Session creation exception: {e}")
        return False
    
    # 4. Test Basic Commands
    try:
        cmd_result = session.command.execute("echo 'Hello AgentBay'")
        if cmd_result.is_error:
            print(f"❌ Command execution failed: {cmd_result.error}")
            return False
        else:
            print("✅ Command executed successfully")
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
sessions_result = agent_bay.list()
if not sessions_result.is_error:
    sessions = sessions_result.sessions
    print(f"Current sessions: {len(sessions)}")
    
    # Clean up old sessions if needed
    for session_info in sessions[:3]:  # Clean up first 3 as example
        try:
            agent_bay.delete(session_info.session_id)
            print(f"Deleted session: {session_info.session_id}")
        except Exception as e:
            print(f"Failed to delete session {session_info.session_id}: {e}")
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
        if not result.is_error:
            return result.session
        else:
            print(f"Failed to create session: {result.error}")
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
        cmd_result = session.command.execute(f"mkdir -p {dir_path}")
        if cmd_result.is_error:
            print(f"Failed to create directory: {cmd_result.error}")
            return False
        
        # Test write access
        test_content = "test"
        write_result = session.file_system.write_file(path, test_content)
        if write_result.is_error:
            print(f"Write failed: {write_result.error}")
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
```python
# Handle large file uploads with chunking
def upload_large_file(session, local_path, remote_path, chunk_size=1024*1024):  # 1MB chunks
    try:
        with open(local_path, 'rb') as f:
            chunk_number = 0
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                
                # Write chunk to remote file (append mode would be needed)
                chunk_path = f"{remote_path}.part{chunk_number}"
                write_result = session.file_system.write_file(chunk_path, chunk)
                if write_result.is_error:
                    print(f"Failed to upload chunk {chunk_number}: {write_result.error}")
                    return False
                
                chunk_number += 1
            
            print(f"Uploaded {chunk_number} chunks successfully")
            return True
    except Exception as e:
        print(f"Large file upload failed: {e}")
        return False
```

### 5. Command Execution Issues

#### Problem: "Command not found" or "Executable not found"
**Cause**: Missing software or incorrect command syntax

**Solution**:
```python
# Check if command exists before executing
def check_command_exists(session, command):
    cmd_result = session.command.execute(f"which {command}")
    return not cmd_result.is_error

# Install missing packages
def install_package(session, package_name):
    # For Ubuntu/Debian
    cmd_result = session.command.execute(f"apt-get update && apt-get install -y {package_name}")
    if cmd_result.is_error:
        print(f"Failed to install {package_name}: {cmd_result.error}")
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
from agentbay import CommandOptions

# For quick commands, use shorter timeout
quick_cmd_result = session.command.execute("ls -la", CommandOptions(timeout=30))

# For long-running commands, use longer timeout
long_cmd_result = session.command.execute("find / -name '*.log'", CommandOptions(timeout=300))

# For very long operations, consider breaking them into steps
def process_large_dataset(session):
    # Step 1: Prepare data
    session.command.execute("mkdir -p /tmp/processing")
    
    # Step 2: Process in chunks
    for i in range(10):
        cmd_result = session.command.execute(
            f"process_chunk.sh {i}", 
            CommandOptions(timeout=60)
        )
        if cmd_result.is_error:
            print(f"Chunk {i} failed: {cmd_result.error}")
            # Decide whether to continue or abort
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
    if result.is_error:
        print(f"Error Type: {type(result.error)}")
        print(f"Error Message: {result.error}")
        print(f"Error Code: {getattr(result, 'error_code', 'N/A')}")
        print(f"Request ID: {getattr(result, 'request_id', 'N/A')}")
        
        # Check if it's a network issue
        if "timeout" in str(result.error).lower():
            print("💡 This appears to be a network timeout issue")
        elif "permission" in str(result.error).lower():
            print("💡 This appears to be a permission issue")
        elif "not found" in str(result.error).lower():
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
            if not result.is_error:
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

1. **Check the [FAQ](faq.md)** for common questions
2. **Review the [Documentation](../README.md)** for detailed information
3. **Search [GitHub Issues](https://github.com/aliyun/wuying-agentbay-sdk/issues)** for similar problems
4. **Create a new issue** with:
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