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

agent_bay = AgentBay(api_key=api_key)
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

### 4. Use Environment Variables for Configuration
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

### 5. Handle Errors Gracefully
```python
from agentbay import AgentBay, AgentBayError

try:
    agent_bay = AgentBay(api_key=api_key)
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
from agentbay import AgentBay
agent_bay = AgentBay(api_key=api_key)
# ✅ Good practice
session = agent_bay.create().session
# Write file
result = session.file_system.write_file("/path/to/file", "content")
if result.success:
    print("File written successfully")
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
else:
    print("Failed to write file")

# ❌ Bad practice
content = session.file_system.read_file("/path/to/file")  # May fail
print(content.content)
```

### 7. Use Appropriate Methods for File Size
```python
from agentbay import AgentBay
agent_bay = AgentBay(api_key=api_key)
session = agent_bay.create().session

#large_content >50KB
large_content = "large_content" * 51000 # 51KB of 'large_content'

# ✅ For large files (≥ 50KB) or when you need chunked reading
result = session.file_system.write_file("/path/to/file",large_content, mode="overwrite")
if result.success:
    print("Large file written successfully")
    result = session.file_system.read_file("/path/to/file")
    if result.success:
        print(f"Large file read successfully: {len(result.content)} characters")
    else:
        print(f"Failed to read large file: {result.error_message}")
else :
    print("Failed to write large file")
# ✅ For multiple files
files = ["file1.txt", "file2.txt", "file3.txt"]
for file_path in files:
    result = session.file_system.write_file(file_path, "content")
    if result.success:
        print(f"{file_path} written successfully")
        content = session.file_system.read_file(file_path)
        if not content.success:
            print(f"Failed to read {file_path}: {content.error_message}")
            break
        print(f"{file_path} read successfully: {content.content}")
agent_bay.delete(session)
```

**Note on File Size Thresholds:**
- Use `read_file()` for any file size (automatic chunked transfer for large files)
- Use `write_file()` for any content size (automatic chunked transfer for large content)

### 8. Handle File Paths Correctly
```python
import os
# ✅ Good practice - Use os.path.join
base_dir = '/tmp'
filename = 'example.txt'

# Construct the path
file_path = os.path.join(base_dir, filename).replace("\\", "/")
print(file_path)

# ✅ Check paths before operations
# Note: In cloud environments, local file operations should be handled carefully
# For demonstration purposes, we show the pattern but in practice you would
# either upload existing files or create them programmatically

agent_bay = AgentBay()
session = agent_bay.create().session
try:
    result = session.file_system.search_files(base_dir, filename)
    print(f"Search result success: {result.success}")  # Debug info
    print(f"Matches count: {len(result.matches)}")  # Debug info
    print(f"Matches: {result.matches}")
    if result.success and result.matches:
        # File exists in remote workspace
        print("File found in remote workspace")
        for match in result.matches:
            print(match)

        result = session.file_system.read_file(file_path)
        if result.success:
            print("File read successfully")
            print(result.content)
    else:
        # Example of creating and uploading a file (more appropriate for cloud environments)
        content = "Example file content"
        result = session.file_system.write_file(file_path, content,mode="overwrite")

        if not result.success:
            print(f"Failed to create file: {result.error_message}")
        else:
            print("File created successfully in remote workspace")
            result = session.file_system.read_file(file_path)
            if result.success:
                print("File read successfully")

except Exception as e:
    print(f"Exception: {e}")
agent_bay.delete(session)
```

### 9. Set Appropriate Timeouts
```python
from agentbay import AgentBay
agent_bay = AgentBay(api_key=api_key)
session = agent_bay.create().session
# ✅ For quick commands
result = session.command.execute_command("ls -a",timeout_ms=1000)  # 1 second timeout
if result.success:
    print("Command executed successfully")
    print(result.output)

# ✅ For long-running commands
result = session.command.execute_command("npm install",timeout_ms=60000)  # Let system handle timeouts
if result.success:
    print("Command executed successfully")
    print(result.output)
# ✅ For potentially infinite commands
result = session.command.execute_command("tail -f /var/log/app.log", timeout_ms=None)  # Let system handle timeouts
if result.success:
    print("Command executed successfully")
    print(result.output)
agent_bay.delete(session)
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
agent_bay.delete(session)
```

### 11. Use Proper Shell Escaping
**Note**: In particular, `shlex.quote` is primarily used to ensure that special characters within strings (such as spaces, quotes, and other characters with special meanings) are interpreted correctly. This helps prevent command injection attacks or other unintended behaviors.
```python
import shlex
agent_bay = AgentBay(api_key=api_key)
session = agent_bay.create().session
# ✅ Good practice - Escape shell arguments
filename = "file with spaces.txt"
escaped_filename = shlex.quote(filename)
result = session.command.execute_command(f"cat {escaped_filename}")
if result.success:
    print("File read successfully")
    print(result.output)
else:
    print(f"Failed to read file: {result.error_message}")
agent_bay.delete(session)

# ❌ Bad practice - Direct string interpolation
result = session.command.execute_command(f"cat {filename}")  # Will fail
```

## 🏷️ Session Management Best Practices

### 12. Use Labels for Session Organization
```python
from agentbay.session_params import CreateSessionParams

# ✅ Create sessions with meaningful labels (recommended approach)
params = CreateSessionParams(labels={
    'project': 'web-scraper',
    'environment': 'development',
    'owner': 'john.doe'
})
agent_bay = AgentBay()
result = agent_bay.create(params)
session = result.session

if(result.success):
    print("Session created successfully")
    print(f"Session ID: {session.session_id}")
    # ✅ Find sessions by labels
    result = agent_bay.list_by_labels({'project': 'web-scraper'})
    if result.success:
        sessions = result.sessions
        for session in sessions:
            print(f"Session ID: {session.session_id}")
agent_bay.delete(session)
```

**Note**: While you can pass labels directly as a dictionary to the `create()` method, using `CreateSessionParams` is the recommended approach for better type safety and clarity.

### 13. Clean Up Sessions When Done
```python
# ✅ Good practice - Clean up after use
try:
    session = agent_bay.create().session
    # Do work...
    result = session.command.execute_command("ls -a")
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
from agentbay import AgentBay
agent_bay = AgentBay(api_key=api_key)
session = agent_bay.create().session
# ✅ Check session info periodically
result = session.info()
if hasattr(result, 'success') and result.success:
    print("Session is active and responding")
    # You can also access detailed session information
    session_info = getattr(result, 'data', None)
    if session_info:
        print(f"Session ID: {getattr(session_info, 'session_id', 'N/A')}")
    else:
        print("Session info not available")
else:
    print("Session is not active or not responding")
agent_bay.delete(session)
```

## 🔄 Context and Data Persistence

### 15. Use Context for Data Persistence
```python
from agentbay import AgentBay
from agentbay.session_params import CreateSessionParams
from agentbay.context_sync import ContextSync, SyncPolicy

# ✅ Create a context for data persistence across sessions
agent_bay = AgentBay(api_key=api_key)

# Create a named context for persistence
context_name = "my-persistent-context"
context_result = agent_bay.context.create(context_name)
if context_result.success:
    context_id = context_result.context_id
    print(f"Context created with ID: {context_id}")

# ✅ Save important data to context in first session
# Create context sync configuration
context_sync = ContextSync.new(
    context_id,
    '/tmp/shared_data',
    SyncPolicy.default()
)

# Create session with context sync
session_params = CreateSessionParams()
session_params.context_syncs = [context_sync]

session_result = agent_bay.create(session_params)
if session_result.success:
    session1 = session_result.session

    # Create and save data in the context
    session1.command.execute_command("mkdir -p /tmp/shared_data")
    session1.command.execute_command("echo '{\"theme\": \"dark\", \"language\": \"en\", \"version\": \"1.0\"}' > /tmp/shared_data/user_preferences.json")

    # Session cleanup with automatic context sync
    agent_bay.delete(session1, sync_context=True)

# ✅ Retrieve data in another session using the same context
# Create a new session with the same context
context_sync2 = ContextSync.new(
    context_id,
    '/tmp/shared_data',
    SyncPolicy.default()
)

session_params2 = CreateSessionParams()
session_params2.context_syncs = [context_sync2]

session_result2 = agent_bay.create(session_params2)
if session_result2.success:
    session2 = session_result2.session

    # Retrieve the data that was saved in the first session
    result = session2.command.execute_command("cat /tmp/shared_data/user_preferences.json")
    if hasattr(result, 'success') and result.success:
        preferences = getattr(result, 'output', result)
        print(f"Retrieved preferences: {preferences.strip()}")

    # Clean up
    agent_bay.delete(session2, sync_context=True)
print("Context deleted",context_id)
# Clean up context when no longer needed
agent_bay.context.delete(context_result.context)
```

## 🚨 Common Pitfalls to Avoid

### 16. Don't Ignore Error Handling
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
agent_bay.delete(session)
```

### 17. Don't Create Too Many Sessions
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

## 📊 Performance Tips

### 18. Batch Operations When Possible
```python
# ✅ Batch commands
commands = [
    "mkdir -p ~/data",
    "cd ~",
    "git clone https://github.com/user/repo.git"
]
session = agent_bay.create().session
try:
    for cmd in commands:
        result = session.command.execute_command(cmd)
        if hasattr(result, 'success') and not result.success:
            print(f"Command failed: {getattr(result, 'error_message', 'Unknown error')}")
            break
        else:
            print(f"Command executed successfully")

finally:
    agent_bay.delete(session)
```

### 19. Reuse Sessions
```python
# ✅ Reuse sessions for multiple operations
session = agent_bay.create().session
try:
    append_list = []

    # Perform multiple operations with the same session
    result1 = session.command.execute_command("ls")
    result2 = session.command.execute_command("pwd")
    result3 = session.command.execute_command("whoami")
    append_list.extend([{"success": result1.success, "output": result1.output},
                        {"success": result2.success, "output": result2.output},
                        {"success": result3.success, "output": result3.output}])
    if all(item['success'] for item in append_list):
        print("All commands executed successfully")
        # Print each output individually
        for item in append_list:
            print(item["output"])

finally:
    agent_bay.delete(session)
```

### 20. Monitor and Optimize
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

### 21. Never Hardcode Credentials
```python
# ❌ Never do this
api_key = "sk-1234567890abcdef"

# ✅ Use environment variables
import os
api_key = os.getenv('AGENTBAY_API_KEY')
```

Following these best practices will help you build more reliable, secure, and maintainable applications with AgentBay SDK.
