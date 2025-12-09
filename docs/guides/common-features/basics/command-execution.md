# Command Execution Guide

This guide covers command execution capabilities in AgentBay SDK. The command module allows you to execute shell commands and system operations in cloud sessions.

> **💡 Async API Support**: This guide uses synchronous API by default. For async/await syntax and concurrent execution patterns, see:
> - [Async-Specific Patterns](#async-specific-patterns) - Concurrent command execution

## 📋 Table of Contents

- [Overview](#overview)
- [Basic Command Execution](#basic-command-execution)
- [Command with Timeout](#command-with-timeout)
- [Working with Command Output](#working-with-command-output)
- [Advanced Patterns](#advanced-patterns)
  - [Working Directory (cwd)](#working-directory-cwd)
  - [Environment Variables (envs)](#environment-variables-envs)
  - [Combining cwd and envs](#combining-cwd-and-envs)
  - [Command Chaining](#command-chaining-legacy-pattern)
- [Async-Specific Patterns](#async-specific-patterns)
- [Choosing Sync vs Async](#choosing-sync-vs-async)

<a id="overview"></a>
## 🎯 Overview

The `session.command` module provides programmatic access to execute shell commands in cloud sessions. This is useful for:

- **System Operations** - Run shell commands, manage processes
- **Environment Setup** - Install packages, configure environments
- **File Processing** - Use command-line tools for file operations
- **Automation** - Automate complex workflows

### Command Module Features

- ✅ Synchronous and asynchronous command execution
- ✅ Timeout support (maximum 50 seconds)
- ✅ Working directory (cwd) configuration
- ✅ Environment variables (envs) support
- ✅ Detailed output capture (stdout, stderr)
- ✅ Exit code and trace ID handling
- ✅ Backward compatible output field

<a id="basic-command-execution"></a>
## 💻 Basic Command Execution

### Simple Commands

```python
from agentbay import AgentBay

agent_bay = AgentBay(api_key="your-api-key")
result = agent_bay.create()

if result.success:
    session = result.session

    cmd_result = session.command.execute_command("ls -la /tmp")
    if cmd_result.success:
        print("Output:", cmd_result.output)
    else:
        print("Command failed:", cmd_result.error_message)

    agent_bay.delete(session)
else:
    print("Failed to create session:", result.error_message)

# Output example:
# Output: total 140
# drwxrwxrwt 21 root   root    4096 Oct  2 14:57 .
# drwxr-xr-x 19 root   root    4096 Oct  2 14:20 ..
# -rw-------  1 root   root       0 Oct  2 14:20 example.lock
# srwxr-xr-x  1 root   root       0 Oct  2 14:20 service.sock
# ...
```

### Sequential Command Execution

Execute multiple commands one after another:

```python
from agentbay import AgentBay

agent_bay = AgentBay()
session = agent_bay.create().session

commands = [
    "echo 'Hello from cloud'",
    "pwd",
    "whoami",
    "uname -a"
]

for cmd in commands:
    result = session.command.execute_command(cmd)
    if result.success:
        print(f"{cmd} -> {result.output.strip()}")
    else:
        print(f"{cmd} failed: {result.error_message}")

agent_bay.delete(session)

# Output example:
# echo 'Hello from cloud' -> Hello from cloud
# pwd -> /home/user
# whoami -> user
# uname -a -> Linux hostname 5.15.0-125-generic #135-Ubuntu SMP x86_64 x86_64 x86_64 GNU/Linux
```

<a id="command-with-timeout"></a>
## ⏱️ Command with Timeout

### Setting Execution Timeout

Control how long a command can run before timing out:

```python
from agentbay import AgentBay

agent_bay = AgentBay()
session = agent_bay.create().session

# Command completes within timeout
result = session.command.execute_command("sleep 3", timeout_ms=5000)
if result.success:
    print("Command completed within timeout")
else:
    print("Command timed out or failed:", result.error_message)

# Command exceeds timeout
result = session.command.execute_command("sleep 10", timeout_ms=2000)
if result.success:
    print("Command completed")
else:
    print("Command timed out:", result.error_message)

agent_bay.delete(session)

# Output example:
# Command completed within timeout
# Command timed out: Error in response: Execution failed. Error code:-1 Error message: [timeout]
```

### Timeout Limits

- **Default timeout**: 60 seconds (60000ms) for Python SDK
- **Maximum timeout**: 50 seconds (50000ms) - SDK automatically limits larger values
- If you specify a timeout greater than 50 seconds, the SDK will automatically cap it to 50 seconds and log a warning

```python
from agentbay import AgentBay

agent_bay = AgentBay()
session = agent_bay.create().session

# Timeout will be automatically limited to 50000ms (50s)
result = session.command.execute_command("sleep 1", timeout_ms=60000)
# Warning: Timeout 60000ms exceeds maximum allowed 50000ms. Limiting to 50000ms.

agent_bay.delete(session)
```

<a id="working-with-command-output"></a>
## 📤 Working with Command Output

### Understanding Command Result Fields

The `execute_command` method returns a `CommandResult` object with the following fields:

- **`output`** - Combined stdout and stderr (for backward compatibility: `output = stdout + stderr`)
- **`stdout`** - Standard output from the command
- **`stderr`** - Standard error from the command
- **`exit_code`** - Command exit code (0 for success)
- **`success`** - Boolean indicating if command succeeded (based on exit_code)
- **`trace_id`** - Trace ID for error tracking (only present when exit_code != 0)
- **`request_id`** - Unique identifier for the API request
- **`error_message`** - Error description if execution failed

### Capturing and Processing Output

```python
from agentbay import AgentBay

agent_bay = AgentBay()
session = agent_bay.create().session

result = session.command.execute_command("df -h")
if result.success:
    print("Full output (stdout + stderr):")
    print(result.output)
    
    print("\nStandard output:")
    print(result.stdout)
    
    print("\nStandard error:")
    print(result.stderr)
    
    print(f"\nExit code: {result.exit_code}")
    
    lines = result.stdout.strip().split('\n')
    print(f"Found {len(lines)} filesystems")
else:
    print("Command failed:", result.error_message)
    print(f"Exit code: {result.exit_code}")
    if result.trace_id:
        print(f"Trace ID: {result.trace_id}")

agent_bay.delete(session)

# Output example:
# Full output (stdout + stderr):
# Filesystem      Size  Used Avail Use% Mounted on
# tmpfs           756M  2.9M  753M   1% /run
# /dev/vda3        99G   23G   72G  24% /
# ...
# 
# Standard output:
# Filesystem      Size  Used Avail Use% Mounted on
# ...
# 
# Standard error:
# 
# Exit code: 0
# Found 8 filesystems
```

### Separating stdout and stderr

```python
from agentbay import AgentBay

agent_bay = AgentBay()
session = agent_bay.create().session

# Command that produces both stdout and stderr
result = session.command.execute_command("echo 'Hello' && echo 'Error' >&2")
if result.success:
    print(f"stdout: {repr(result.stdout)}")  # 'Hello\n'
    print(f"stderr: {repr(result.stderr)}")   # 'Error\n'
    print(f"output: {repr(result.output)}")   # 'Hello\nError\n' (stdout + stderr)
    print(f"output == stdout + stderr: {result.output == result.stdout + result.stderr}")  # True

agent_bay.delete(session)
```

<a id="advanced-patterns"></a>
## 🔧 Advanced Patterns

### Working Directory (cwd)

Execute commands in a specific directory:

```python
from agentbay import AgentBay

agent_bay = AgentBay()
session = agent_bay.create().session

# Execute command in /tmp directory
result = session.command.execute_command(
    "pwd",
    cwd="/tmp"
)
if result.success:
    print(f"Current directory: {result.stdout.strip()}")  # /tmp

agent_bay.delete(session)
```

### Environment Variables (envs)

Set environment variables for command execution:

```python
from agentbay import AgentBay

agent_bay = AgentBay()
session = agent_bay.create().session

# Execute command with custom environment variables
result = session.command.execute_command(
    "echo $API_KEY && echo $MODE",
    envs={
        "API_KEY": "secret123",
        "MODE": "production"
    }
)
if result.success:
    print("Output:", result.stdout)
    # Output: secret123
    #         production

agent_bay.delete(session)
```

> **⚠️ Type Requirements**: The `envs` parameter requires all keys and values to be strings. If any key or value is not a string type, the SDK will raise a `ValueError` (Python) or `Error` (TypeScript) before executing the command. In Go, the type system enforces `map[string]string` at compile time.
>
> **Valid examples:**
> ```python
> envs={"API_KEY": "secret123", "MODE": "production"}  # ✅ All strings
> ```
>
> **Invalid examples (will raise error):**
> ```python
> envs={"API_KEY": 123}  # ❌ Value is int, not string
> envs={"DEBUG": True}   # ❌ Value is bool, not string
> envs={123: "value"}    # ❌ Key is int, not string
> ```

### Combining cwd and envs

Use both working directory and environment variables:

```python
from agentbay import AgentBay

agent_bay = AgentBay()
session = agent_bay.create().session

# Execute command in specific directory with environment variables
result = session.command.execute_command(
    "pwd && echo $TEST_VAR",
    cwd="/tmp",
    envs={"TEST_VAR": "test_value"}
)
if result.success:
    print("Output:", result.stdout)
    # Output: /tmp
    #         test_value

agent_bay.delete(session)
```

### Command Chaining (Legacy Pattern)

> **Note**: While command chaining still works, it's recommended to use `cwd` and `envs` parameters instead for better clarity and security.

Execute multiple commands in a single shell invocation:

```python
from agentbay import AgentBay

agent_bay = AgentBay()
session = agent_bay.create().session

# Old pattern (still supported)
result = session.command.execute_command(
    "mkdir -p /tmp/test && cd /tmp/test && echo 'Hello' > file.txt && cat file.txt"
)
if result.success:
    print("Output:", result.output)

# Recommended pattern (using cwd)
result = session.command.execute_command(
    "echo 'Hello' > file.txt && cat file.txt",
    cwd="/tmp/test"
)
if result.success:
    print("Output:", result.output)

agent_bay.delete(session)

# Output example:
# Output: Hello
```

<a id="async-specific-patterns"></a>
## ⚡ Async-Specific Patterns

The async API provides powerful patterns for concurrent command execution, delivering **4-6x performance improvements** when running multiple independent commands.

> **Note**: These patterns require the asynchronous API (`from agentbay import AsyncAgentBay`)

### Concurrent Command Execution

Execute multiple commands simultaneously for dramatic performance gains:

```python
import asyncio
from agentbay import AsyncAgentBay

async def main():
    agent_bay = AsyncAgentBay()
    session = (await agent_bay.create()).session

    # Execute multiple commands concurrently
    commands = [
        "sleep 2 && echo 'Command 1 done'",
        "sleep 2 && echo 'Command 2 done'",
        "sleep 2 && echo 'Command 3 done'"
    ]

    # This takes ~2 seconds instead of ~6 seconds (3x faster!)
    results = await asyncio.gather(*[
        session.command.execute_command(cmd)
        for cmd in commands
    ])

    for i, result in enumerate(results, 1):
        if result.success:
            print(f"Command {i}: {result.output.strip()}")

    await agent_bay.delete(session)

asyncio.run(main())

# Output (all commands complete in ~2 seconds):
# Command 1: Command 1 done
# Command 2: Command 2 done
# Command 3: Command 3 done
```

**Performance**: Sequential execution would take 6 seconds, concurrent execution takes only 2 seconds.

### Async Timeout with asyncio.wait_for

Use asyncio's native timeout functionality for fine-grained control:

```python
import asyncio
from agentbay import AsyncAgentBay

async def main():
    agent_bay = AsyncAgentBay()
    session = (await agent_bay.create()).session

    try:
        # Use asyncio.wait_for for timeout
        result = await asyncio.wait_for(
            session.command.execute_command("sleep 10"),
            timeout=5.0  # 5 seconds
        )
        print("Command completed:", result.output)
    except asyncio.TimeoutError:
        print("Command timed out after 5 seconds")
    finally:
        await agent_bay.delete(session)

asyncio.run(main())
```

### Parallel Processing Pattern

Process multiple files or tasks concurrently:

```python
import asyncio
from agentbay import AsyncAgentBay

async def process_file(session, filename):
    """Process a single file"""
    cmd = f"wc -l /tmp/{filename}"
    result = await session.command.execute_command(cmd)
    if result.success:
        return f"{filename}: {result.output.strip()}"
    return f"{filename}: failed"

async def main():
    agent_bay = AsyncAgentBay()
    session = (await agent_bay.create()).session

    # Create test files
    for i in range(5):
        await session.command.execute_command(
            f"seq 1 {(i+1)*10} > /tmp/file{i}.txt"
        )

    # Process all files concurrently
    files = [f"file{i}.txt" for i in range(5)]
    results = await asyncio.gather(*[
        process_file(session, f)
        for f in files
    ])

    for result in results:
        print(result)

    await agent_bay.delete(session)

asyncio.run(main())

# Output:
# file0.txt: 10 /tmp/file0.txt
# file1.txt: 20 /tmp/file1.txt
# file2.txt: 30 /tmp/file2.txt
# file3.txt: 40 /tmp/file3.txt
# file4.txt: 50 /tmp/file4.txt
```

<a id="choosing-sync-vs-async"></a>
## 🔄 Choosing Sync vs Async

### Use Sync API When:

- ✅ Writing simple scripts or CLI tools
- ✅ Commands must execute sequentially
- ✅ Learning AgentBay for the first time
- ✅ Code simplicity is more important than performance

### Use Async API When:

- ✅ Building web applications (FastAPI, Django async)
- ✅ Need to execute multiple commands concurrently
- ✅ Working with I/O-bound operations
- ✅ Performance and scalability are critical

### Performance Comparison

**Sequential Execution (5 commands, 1 second each)**:
- Sync API: ~5 seconds
- Async API (sequential with for loop): ~5 seconds
- Async API (concurrent with asyncio.gather): ~1 second ⚡ **5x faster!**

**Recommendation**: For command execution, async API shines when you need to run multiple commands concurrently. For single commands or sequential workflows, both APIs perform similarly - use sync for simplicity.

## 📚 Related Documentation

- [Code Execution (CodeSpace)](../../codespace/code-execution.md) - Python, JavaScript code execution
- [File Operations](file-operations.md) - File handling and management
- [Session Management](session-management.md) - Session lifecycle

## 🆘 Getting Help

- [GitHub Issues](https://github.com/aliyun/wuying-agentbay-sdk/issues)
- [Documentation Home](../README.md)

Happy automating with AgentBay! 🚀
