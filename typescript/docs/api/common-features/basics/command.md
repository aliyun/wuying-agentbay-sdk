# Class: Command

## ⚡ Related Tutorial

- [Command Execution Guide](../../../../../docs/guides/common-features/basics/command-execution.md) - Learn how to execute commands in sessions

## Overview

The Command module provides methods for executing shell commands within a session in the AgentBay cloud environment.
It supports both synchronous command execution with configurable timeouts.

Handles command execution operations in the AgentBay cloud environment.

## Table of contents


### Methods

- [executeCommand](#executecommand)

## Methods

### executeCommand

▸ **executeCommand**(`command`, `timeoutMs?`, `cwd?`, `envs?`): `Promise`\<`CommandResult`\>

Execute a shell command with optional working directory and environment variables.

Executes a shell command in the session environment with configurable timeout,
working directory, and environment variables. The command runs with session
user permissions in a Linux shell environment.

#### Parameters

| Name | Type | Default value | Description |
| :------ | :------ | :------ | :------ |
| `command` | `string` | `undefined` | The shell command to execute |
| `timeoutMs` | `number` | `1000` | Timeout in milliseconds (default: 1000ms/1s). Maximum allowed timeout is 50000ms (50s). If a larger value is provided, it will be automatically limited to 50000ms |
| `cwd?` | `string` | `undefined` | The working directory for command execution. If not specified, the command runs in the default session directory |
| `envs?` | `Record`\<`string`, `string`\> | `undefined` | Environment variables as a dictionary of key-value pairs. These variables are set for the command execution only |

#### Returns

`Promise`\<`CommandResult`\>

Promise resolving to CommandResult containing:
         - success: Whether the command executed successfully (exitCode === 0)
         - output: Command output for backward compatibility (stdout + stderr)
         - exitCode: The exit code of the command execution (0 for success)
         - stdout: Standard output from the command execution
         - stderr: Standard error from the command execution
         - traceId: Trace ID for error tracking (only present when exitCode !== 0)
         - requestId: Unique identifier for this API request
         - errorMessage: Error description if execution failed

**`Example`**

```typescript
const agentBay = new AgentBay({ apiKey: 'your_api_key' });
const result = await agentBay.create();
if (result.success) {
  const cmdResult = await result.session.command.executeCommand('echo "Hello"', 5000);
  console.log('Command output:', cmdResult.output);
  console.log('Exit code:', cmdResult.exitCode);
  console.log('Stdout:', cmdResult.stdout);
  await result.session.delete();
}
```

**`Example`**

```typescript
const agentBay = new AgentBay({ apiKey: 'your_api_key' });
const result = await agentBay.create();
if (result.success) {
  const cmdResult = await result.session.command.executeCommand(
    'pwd',
    5000,
    '/tmp',
    { TEST_VAR: 'test_value' }
  );
  console.log('Working directory:', cmdResult.stdout);
  await result.session.delete();
}
```

## Best Practices

1. Always specify appropriate timeout values based on expected command duration
2. Handle command execution errors gracefully
3. Use absolute paths when referencing files in commands
4. Be aware that commands run with session user permissions
5. Clean up temporary files created by commands


## Related Resources

- [Session API Reference](session.md)
- [FileSystem API Reference](filesystem.md)

