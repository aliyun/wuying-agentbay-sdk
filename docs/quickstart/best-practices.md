# Best Practices and Common Patterns

This guide provides best practices and common patterns for AgentBay SDK to help new users avoid common pitfalls and write more reliable code.

## 🎯 Core Principles

### 1. Always Check Operation Results
```python
# ✅ Good practice
result = session.command.execute("ls -la")
if result.is_error:
    print(f"Command execution failed: {result.error}")
    return
print(result.data.stdout)

# ❌ Bad practice
result = session.command.execute("ls -la")
print(result.data.stdout)  # May cause errors
```

### 2. Properly Manage Session Lifecycle
```python
# ✅ Good practice - Using context manager
from agentbay import AgentBay

agent_bay = AgentBay()
try:
    session = agent_bay.create().session
    # Perform operations
    result = session.command.execute("echo 'Hello'")
    print(result.data.stdout)
finally:
    # Clean up resources (if needed)
    pass

# ✅ Better practice - Batch operations
session = agent_bay.create().session
commands = ["ls -la", "pwd", "whoami"]
for cmd in commands:
    result = session.command.execute(cmd)
    if not result.is_error:
        print(f"{cmd}: {result.data.stdout}")
```

### 3. Use Environment Variables for Configuration
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
    result = session.command.execute("some-command")
    
    if result.is_error:
        print(f"Command failed: {result.error}")
    else:
        print(f"Success: {result.data.stdout}")
        
except AgentBayError as e:
    print(f"AgentBay error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## 📁 File Operations Best Practices

### 1. Check File Existence Before Operations
```python
# ✅ Good practice
if session.filesystem.exists("/path/to/file"):
    content = session.filesystem.read("/path/to/file")
    print(content.data)
else:
    print("File does not exist")

# ❌ Bad practice
content = session.filesystem.read("/path/to/file")  # May fail
```

### 2. Use Appropriate Methods for File Size
```python
# ✅ For small files (< 1MB)
content = session.filesystem.read("small_file.txt")

# ✅ For large files
session.filesystem.upload_file("large_file.zip", "/remote/path/")

# ✅ For multiple files
files = ["file1.txt", "file2.txt", "file3.txt"]
session.filesystem.upload_files(files, "/remote/directory/")
```

### 3. Handle File Paths Correctly
```python
import os

# ✅ Good practice - Use os.path.join
local_path = os.path.join("data", "input.txt")
remote_path = "/workspace/input.txt"

# ✅ Check paths before operations
if os.path.exists(local_path):
    session.filesystem.upload_file(local_path, remote_path)
```

## 🔧 Command Execution Best Practices

### 1. Set Appropriate Timeouts
```python
# ✅ For quick commands
result = session.command.execute("ls", timeout_ms=1000)

# ✅ For long-running commands
result = session.command.execute("npm install", timeout_ms=300000)  # 5 minutes

# ✅ For potentially infinite commands
result = session.command.execute("tail -f /var/log/app.log", timeout_ms=60000)
```

### 2. Handle Command Output Properly
```python
result = session.command.execute("find /home -name '*.py'")

if result.is_error:
    print(f"Command failed: {result.error}")
elif result.data.stdout:
    files = result.data.stdout.strip().split('\n')
    print(f"Found {len(files)} Python files")
    for file in files[:10]:  # Show first 10
        print(f"  {file}")
else:
    print("No Python files found")
```

### 3. Use Proper Shell Escaping
```python
import shlex

# ✅ Good practice - Escape shell arguments
filename = "file with spaces.txt"
escaped_filename = shlex.quote(filename)
result = session.command.execute(f"cat {escaped_filename}")

# ❌ Bad practice - Direct string interpolation
result = session.command.execute(f"cat {filename}")  # Will fail
```

## 🏷️ Session Management Best Practices

### 1. Use Labels for Session Organization
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

### 2. Clean Up Sessions When Done
```python
# ✅ Good practice - Clean up after use
try:
    session = agent_bay.create().session
    # Do work...
    result = session.command.execute("python script.py")
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
    result = session.command.execute("echo 'Hello'")
    print(result.data.stdout)
```

### 3. Monitor Session Resources
```python
# ✅ Check session info periodically
info = session.info()
if info.success:
    print(f"Session ID: {info.data.session_id}")
    print(f"Status: {info.data.status}")
```

## 🔄 Context and Data Persistence

### 1. Use Context for Data Persistence
```python
# ✅ Save important data to context
session.context.save_data("user_preferences", {
    "theme": "dark",
    "language": "en"
})

# ✅ Retrieve data in another session
preferences = session.context.get_data("user_preferences")
```

### 2. Sync Context When Needed
```python
# ✅ Sync context before important operations
session.context.sync()

# ✅ Use context sync policies
from agentbay import SyncPolicy

session = agent_bay.create({
    'context_sync': [{
        'policy': SyncPolicy.AUTO,
        'interval': 300  # 5 minutes
    }]
}).session
```

## 🚨 Common Pitfalls to Avoid

### 1. Don't Ignore Error Handling
```python
# ❌ Bad - Ignoring errors
result = session.command.execute("risky-command")
print(result.data.stdout)  # May crash

# ✅ Good - Proper error handling
result = session.command.execute("risky-command")
if result.is_error:
    print(f"Error: {result.error}")
    # Handle error appropriately
else:
    print(result.data.stdout)
```

### 2. Don't Create Too Many Sessions
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

### 3. Don't Hardcode Paths and Values
```python
# ❌ Bad - Hardcoded values
result = session.command.execute("cd /home/user/project && python main.py")

# ✅ Good - Use variables and configuration
project_dir = os.getenv('PROJECT_DIR', '/workspace/project')
python_script = os.getenv('PYTHON_SCRIPT', 'main.py')
result = session.command.execute(f"cd {project_dir} && python {python_script}")
```

## 📊 Performance Tips

### 1. Batch Operations When Possible
```python
# ✅ Batch file operations
files_to_upload = ["file1.txt", "file2.txt", "file3.txt"]
session.filesystem.upload_files(files_to_upload, "/remote/dir/")

# ✅ Batch commands
commands = [
    "mkdir -p /workspace/data",
    "cd /workspace",
    "git clone https://github.com/user/repo.git"
]
for cmd in commands:
    result = session.command.execute(cmd)
    if result.is_error:
        break
```

### 2. Use Appropriate Timeouts
```python
# ✅ Short timeout for quick operations
result = session.command.execute("ls", timeout_ms=1000)

# ✅ Longer timeout for complex operations
result = session.command.execute("npm install", timeout_ms=300000)
```

### 3. Monitor and Optimize
```python
import time

# ✅ Measure operation time
start_time = time.time()
result = session.command.execute("heavy-computation")
end_time = time.time()

print(f"Operation took {end_time - start_time:.2f} seconds")
```

## 🔐 Security Best Practices

### 1. Never Hardcode Credentials
```python
# ❌ Never do this
api_key = "sk-1234567890abcdef"

# ✅ Use environment variables
import os
api_key = os.getenv('AGENTBAY_API_KEY')
```

### 2. Validate Input Data
```python
import re

def safe_filename(filename):
    # Remove potentially dangerous characters
    return re.sub(r'[^\w\-_\.]', '_', filename)

# ✅ Use validated filenames
user_filename = input("Enter filename: ")
safe_name = safe_filename(user_filename)
session.filesystem.upload_file(local_file, f"/workspace/{safe_name}")
```

### 3. Be Careful with Command Injection
```python
import shlex

# ✅ Safe command construction
user_input = "file with spaces.txt"
safe_input = shlex.quote(user_input)
result = session.command.execute(f"cat {safe_input}")

# ❌ Dangerous - Direct interpolation
result = session.command.execute(f"cat {user_input}")  # Vulnerable!
```

Following these best practices will help you build more reliable, secure, and maintainable applications with AgentBay SDK. 