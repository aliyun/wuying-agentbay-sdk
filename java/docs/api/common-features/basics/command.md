# Command API Reference

## ⚡ Related Tutorial

- [Command Execution Guide](../../../../../docs/guides/common-features/basics/command-execution.md) - Learn how to execute commands in sessions

## Overview

The Command module provides methods for executing shell commands within a session in the AgentBay cloud environment. It supports synchronous command execution with configurable timeouts.

## CommandResult

```java
public class CommandResult extends ApiResponse
```

Result of command execution operations.

**Fields:**
- `success` (boolean): True if the operation succeeded
- `output` (String): The command output (stdout and stderr combined)  
- `requestId` (String): Unique identifier for this API request
- `errorMessage` (String): Error description (if success is false)
- `exitCode` (int): Command exit code

## Command

```java
public class Command extends BaseService
```

Handles command execution operations in the AgentBay cloud environment.

### executeCommand

```java
public CommandResult executeCommand(String command, int timeoutMs)
```

Execute a shell command in the cloud environment with a specified timeout.

**Parameters:**
- `command` (String): The shell command to execute
- `timeoutMs` (int): The timeout for the command execution in milliseconds. Defaults to 1000 (1 second).

**Returns:**
- `CommandResult`: Result object containing success status, command output, and error message if any.
  - `success` (boolean): True if the operation succeeded
  - `output` (String): The command output (stdout and stderr combined)
  - `requestId` (String): Unique identifier for this API request
  - `errorMessage` (String): Error description (if success is false)
  - `exitCode` (int): Command exit code

**Throws:**
- No checked exceptions (errors are returned in CommandResult)

**Example:**

```java
Session session = agentBay.create().getSession();
CommandResult result = session.getCommand().executeCommand("echo 'Hello, World!'", 1000);
System.out.println(result.getOutput());

// Long-running command with increased timeout
CommandResult longResult = session.getCommand().executeCommand("sleep 2 && echo 'Done'", 5000);
session.delete();
```

### execute

```java
public CommandResult execute(String command)
```

Execute a shell command with default timeout (1000ms).

**Parameters:**
- `command` (String): The shell command to execute

**Returns:**
- `CommandResult`: Result object containing execution results

**Example:**

```java
CommandResult result = session.getCommand().execute("ls -la");
if (result.isSuccess()) {
    System.out.println(result.getOutput());
}
```

## Best Practices

1. Always specify appropriate timeout values based on expected command duration
2. Handle command execution errors gracefully by checking `result.isSuccess()`
3. Use absolute paths when referencing files in commands
4. Be aware that commands run with session user permissions
5. Clean up temporary files created by commands
6. Check exit codes for command success/failure status

## Notes

- Commands are executed in a Linux shell environment
- Default timeout is 1 second (1000ms)
- Output includes both stdout and stderr
- Long-running commands may timeout if timeout_ms is too small
- Commands execute asynchronously on the server side

## Related Resources

- [Session API Reference](session.md)
- [FileSystem API Reference](filesystem.md)
- [Command Execution Example](../../../../agentbay/src/main/java/com/aliyun/agentbay/examples/FileSystemExample.java)

---

*Documentation for AgentBay Java SDK*

