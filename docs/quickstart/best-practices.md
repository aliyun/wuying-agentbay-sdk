# Best Practices and Common Patterns

This guide provides best practices and common patterns for AgentBay SDK to help new users avoid common pitfalls and write more reliable code.

## 🎯 Core Principles

### 1. Always Check Operation Results
```python
# ✅ Good practice
result = session.command.execute_command("ls -la")
if hasattr(result, 'success') and not result.success:
    print(f"Command execution failed: {getattr(result, 'error_message', 'Unknown error')}")
    return
print(getattr(result, 'output', result))

# ❌ Bad practice
result = session.command.execute_command("ls -la")
print(getattr(result, 'output', result))  # May cause errors if command failed
```

### 2. Handle Resource Limits
Note: API keys have resource limits. Check for quota errors and handle them appropriately:
```python
# ✅ Good practice
try:
    session = agent_bay.create().session
except Exception as e:
    if "resource exceed limit" in str(e):
        print("Resource limit exceeded. Please wait or upgrade your plan.")
    else:
        raise e
```

### 3. Properly Manage Session Lifecycle
```python
# ✅ Good practice - Using context manager
from agentbay import AgentBay

agent_bay = AgentBay()
try:
    session = agent_bay.create().session
    # Perform operations
    result = session.command.execute_command("echo 'Hello'")
    print(getattr(result, 'stdout', result))
finally:
    # Clean up resources
    agent_bay.delete(session)

# ✅ Better practice - Batch operations
session = agent_bay.create().session
commands = ["ls -la", "pwd", "whoami"]
try:
    for cmd in commands:
        result = session.command.execute_command(cmd)
        if hasattr(result, 'success') and not result.success:
            print(f"{cmd} failed: {getattr(result, 'error_message', 'Unknown error')}")
        else:
            print(f"{cmd}: {getattr(result, 'output', result)}")
finally:
    # Always clean up
    agent_bay.delete(session)
```

### 5. Use Environment Variables for Configuration
```python
import os
from agentbay import AgentBay

# ✅ Good practice
api_key = os.getenv('AGENTBAY_API_KEY')
if not api_key:
    raise ValueError("AGENTBAY_API_KEY environment variable not set")

agent_bay = AgentBay(api_key=api_key)

# ❌ Bad practice - Hardcoded keys
agent_bay = AgentBay(api_key="sk-1234567890abcdef")  # Never do this!
```

### 4. Handle Errors Gracefully
```python
from agentbay import AgentBay, AgentBayError

try:
    agent_bay = AgentBay()
    session = agent_bay.create().session
    result = session.command.execute_command("some-command")
    
    if hasattr(result, 'success') and not result.success:
        print(f"Command failed: {getattr(result, 'error_message', 'Unknown error')}")
    else:
        print(f"Success: {getattr(result, 'output', result)}")
        
except AgentBayError as e:
    print(f"AgentBay error: {e}")
except Exception as e:
    if "resource exceed limit" in str(e):
        print("Resource limit exceeded. Please wait or upgrade your plan.")
    else:
        print(f"Unexpected error: {e}")
finally:
    # Always clean up
    if 'session' in locals():
        agent_bay.delete(session)
```

## 📁 File Operations Best Practices

### 6. Check File Existence Before Operations
```python
# ✅ Good practice
file_info = session.file_system.get_file_info("/path/to/file")
if file_info.success and file_info.file_info:
    # File exists, read it
    content = session.file_system.read_file("/path/to/file")
    if content.success:
        print(content.content)
    else:
        print(f"Failed to read file: {content.error_message}")
else:
    print("File does not exist")

# ❌ Bad practice
content = session.file_system.read_file("/path/to/file")  # May fail
print(content.content)
```

### 7. Use Appropriate Methods for File Size
```python
# ✅ For small files (< 50KB)
content = session.file_system.read_file("small_file.txt")
if content.success:
    print(content.content)

# ✅ For large files (≥ 50KB) or when you need chunked reading
result = session.file_system.read_large_file("large_file.zip")
if result.success:
    print(f"Large file read successfully: {len(result.content)} characters")
else:
    print(f"Failed to read large file: {result.error_message}")

# ✅ For multiple files
files = ["file1.txt", "file2.txt", "file3.txt"]
for file_path in files:
    content = session.file_system.read_file(file_path)
    if not content.success:
        print(f"Failed to read {file_path}: {content.error_message}")
        break
```

**Note on File Size Thresholds:**
- The `read_file()` method is suitable for small files (less than 50KB) 
- The `read_large_file()` method is recommended for larger files or when you need chunked reading to handle API size limitations
- `read_large_file()` automatically splits the read operation into multiple requests with a default chunk size of 50KB
- For files near the threshold, either method can be used, but `read_large_file()` provides better handling of API limitations

### 8. Handle File Paths Correctly
```python
import os

# ✅ Good practice - Use os.path.join
local_path = os.path.join("data", "input.txt")
remote_path = "/workspace/input.txt"

# ✅ Check paths before operations
# Note: In cloud environments, local file operations should be handled carefully
# For demonstration purposes, we show the pattern but in practice you would
# either upload existing files or create them programmatically
print(f"Local path: {local_path}")
print(f"Remote path: {remote_path}")

# Example of creating and uploading a file (more appropriate for cloud environments)
content = "Example file content"
result = session.file_system.write_file(remote_path, content)
if not result.success:
    print(f"Failed to create file: {result.error_message}")
else:
    print("File created successfully in remote workspace")

## 🔧 Command Execution Best Practices

### 9. Set Appropriate Timeouts
```python
# ✅ For quick commands
result = session.command.execute_command("ls")

# ✅ For long-running commands
result = session.command.execute_command("npm install")  # Let system handle timeouts

# ✅ For potentially infinite commands
result = session.command.execute_command("tail -f /var/log/app.log")
```

### 10. Handle Command Output Properly
```python
result = session.command.execute_command("find /home -name '*.py'")

if hasattr(result, 'success') and not result.success:
    print(f"Command failed: {getattr(result, 'error_message', result)}")
elif getattr(result, 'output', None):
    output = getattr(result, 'output', '')
    files = output.strip().split('\n')
    print(f"Found {len(files)} Python files")
    for file in files[:10]:  # Show first 10
        print(f"  {file}")
else:
    print("No Python files found")
```

### 11. Use Proper Shell Escaping
```python
import shlex

# ✅ Good practice - Escape shell arguments
filename = "file with spaces.txt"
escaped_filename = shlex.quote(filename)
result = session.command.execute_command(f"cat {escaped_filename}")

# ❌ Bad practice - Direct string interpolation
result = session.command.execute_command(f"cat {filename}")  # Will fail
```

## 🏷️ Session Management Best Practices

### 12. Use Labels for Session Organization
```python
# ✅ Create sessions with meaningful labels
session = agent_bay.create({
    'labels': {
        'project': 'web-scraper',
        'environment': 'development',
        'owner': 'john.doe'
    }
}).session

# ✅ Find sessions by labels
sessions = agent_bay.list_by_labels({'project': 'web-scraper'})
```

### 13. Clean Up Sessions When Done
```python
# ✅ Good practice - Clean up after use
try:
    session = agent_bay.create().session
    # Do work...
    result = session.command.execute_command("python script.py")
finally:
    # Always clean up
    agent_bay.delete(session)

# ✅ Better practice - Use session context
from contextlib import contextmanager

@contextmanager
def agentbay_session():
    agent_bay = AgentBay()
    session = agent_bay.create().session
    try:
        yield session
    finally:
        agent_bay.delete(session)

# Usage
with agentbay_session() as session:
    result = session.command.execute_command("echo 'Hello'")
    if hasattr(result, 'success') and not result.success:
        print(f"Command failed: {getattr(result, 'error_message', 'Unknown error')}")
    else:
        print(getattr(result, 'output', result))
```

### 14. Monitor Session Resources
```python
# ✅ Check session info periodically
result = session.info()
if hasattr(result, 'success') and result.success:
    print("Session is active and responding")
    # You can also access detailed session information
    session_info = getattr(result, 'data', None)
    if session_info:
        print(f"Session ID: {getattr(session_info, 'session_id', 'N/A')}")
```

## 🔄 Context and Data Persistence

### 15. Use Context for Data Persistence
```python
# ✅ Save important data to context
# Note: Direct context methods may vary, use file-based persistence as alternative
session.command.execute_command("mkdir -p /workspace/context")
session.command.execute_command("echo '{\"theme\": \"dark\", \"language\": \"en\"}' > /workspace/context/user_preferences.json")

# ✅ Retrieve data in another session
result = session.command.execute_command("cat /workspace/context/user_preferences.json")
preferences = getattr(result, 'stdout', result)
```

### 16. Sync Context When Needed
```python
# ✅ Sync context before important operations
result = session.context.sync()
if hasattr(result, 'success') and result.success:
    print("Context sync initiated successfully")
else:
    print(f"Failed to sync context: {getattr(result, 'error_message', 'Unknown error')}")

# ✅ Use file-based persistence as alternative to context
session.command.execute_command("cp -r /workspace/data /persistent/data")
```
```

## 🚨 Common Pitfalls to Avoid

### 17. Don't Ignore Error Handling
```python
# ❌ Bad - Ignoring errors
result = session.command.execute_command("risky-command")
print(getattr(result, 'stdout', result))  # May crash

# ✅ Good - Proper error handling
result = session.command.execute_command("risky-command")
if hasattr(result, 'success') and not result.success:
    print(f"Error: {getattr(result, 'error_message', 'Unknown error')}")
    # Handle error appropriately
else:
    print(getattr(result, 'output', result))
```

### 18. Don't Create Too Many Sessions
```python
# ❌ Bad - Creating sessions in loops
for task in tasks:
    session = agent_bay.create().session  # Expensive!
    process_task(session, task)
    agent_bay.delete(session)

# ✅ Good - Reuse sessions
session = agent_bay.create().session
try:
    for task in tasks:
        process_task(session, task)
finally:
    agent_bay.delete(session)
```

### 19. Don't Hardcode Paths and Values
```python
# ❌ Bad - Hardcoded values
result = session.command.execute_command("cd /home/user/project && python main.py")

# ✅ Good - Use variables and configuration
project_dir = os.getenv('PROJECT_DIR', '/workspace/project')
python_script = os.getenv('PYTHON_SCRIPT', 'main.py')
result = session.command.execute_command(f"cd {project_dir} && python {python_script}")
```

## 📊 Performance Tips

### 20. Batch Operations When Possible
```python
# ✅ Batch commands
commands = [
    "mkdir -p /workspace/data",
    "cd /workspace",
    "git clone https://github.com/user/repo.git"
]
session = agent_bay.create().session
try:
    for cmd in commands:
        result = session.command.execute_command(cmd)
        if hasattr(result, 'success') and not result.success:
            print(f"Command failed: {getattr(result, 'error_message', 'Unknown error')}")
            break
finally:
    agent_bay.delete(session)
```

### 21. Reuse Sessions
```python
# ✅ Reuse sessions for multiple operations
session = agent_bay.create().session
try:
    # Perform multiple operations with the same session
    result1 = session.command.execute_command("ls")
    result2 = session.command.execute_command("pwd")
    result3 = session.command.execute_command("whoami")
finally:
    agent_bay.delete(session)
```

### 22. Monitor and Optimize
```python
import time

# ✅ Measure operation time
session = agent_bay.create().session
try:
    start_time = time.time()
    result = session.command.execute_command("heavy-computation")
    end_time = time.time()
    
    print(f"Operation took {end_time - start_time:.2f} seconds")
finally:
    agent_bay.delete(session)
```

## 🔐 Security Best Practices

### 23. Never Hardcode Credentials
```python
# ❌ Never do this
api_key = "sk-1234567890abcdef"

# ✅ Use environment variables
import os
api_key = os.getenv('AGENTBAY_API_KEY')
```

### 24. Validate Input Data
```python
import re

def safe_filename(filename):
    # Remove potentially dangerous characters
    return re.sub(r'[^\w\-_\.]', '_', filename)

# ✅ Use validated filenames
user_filename = input("Enter filename: ")
safe_name = safe_filename(user_filename)
# Use command execution for file operations
session.command.execute_command(f"cp {local_file} /workspace/{safe_name}")
```

### 25. Be Careful with Command Injection
```python
import shlex

# ✅ Safe command construction
user_input = "file with spaces.txt"
safe_input = shlex.quote(user_input)
result = session.command.execute_command(f"cat {safe_input}")

# ❌ Dangerous - Direct interpolation
result = session.command.execute_command(f"cat {user_input}")  # Vulnerable!
```

Following these best practices will help you build more reliable, secure, and maintainable applications with AgentBay SDK. 