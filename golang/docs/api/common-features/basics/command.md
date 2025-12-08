# Command API Reference

## ⚡ Related Tutorial

- [Command Execution Guide](../../../../../docs/guides/common-features/basics/command-execution.md) - Learn how to execute commands in sessions

## Overview

The Command module provides methods for executing shell commands within a session in the AgentBay cloud environment.
It supports both synchronous command execution with configurable timeouts.

Command templates for various AgentBay operations.

This module contains shell command templates used by different modules
to execute operations in remote environments.

Template naming convention:
- Use descriptive names that clearly indicate the operation
- Group templates by functionality (mobile, desktop, network, etc.)
- Use consistent parameter naming across similar templates

Parameter conventions:
- Use snake_case for parameter names
- Include descriptive parameter names (e.g., lock_switch, package_list)
- Document expected parameter types and values

## Type Command

```go
type Command struct {
	Session interface {
		GetAPIKey() string
		GetClient() *mcp.Client
		GetSessionId() string
		IsVpc() bool
		NetworkInterfaceIp() string
		HttpPort() string
		FindServerForTool(toolName string) string
		CallMcpTool(toolName string, args interface{}, autoGenSession ...bool) (*models.McpToolResult, error)
	}
}
```

Command handles command execution operations in the AgentBay cloud environment.

### Methods

### ExecuteCommand

```go
func (c *Command) ExecuteCommand(command string, timeoutMs ...int) (*CommandResult, error)
```

ExecuteCommand executes a shell command in the session environment.

This method maintains backward compatibility with the original signature. For advanced features like
working directory and environment variables, use ExecuteCommandWithOptions instead.

Parameters:
  - command: The shell command to execute
  - timeoutMs: Timeout in milliseconds (optional, defaults to 1000ms/1s). Maximum allowed timeout is
    50000ms (50s). If a larger value is provided, it will be automatically limited to 50000ms

Returns:
  - *CommandResult: Result containing command output, exit code, stdout, stderr, trace_id, and
    request ID
  - error: Error if the operation fails

**Example:**

```go
client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
result, _ := client.Create(nil)
defer result.Session.Delete()
cmdResult, _ := result.Session.Command.ExecuteCommand("ls -la")
cmdResult, _ := result.Session.Command.ExecuteCommand("ls -la", 5000)
```

### ExecuteCommandWithOptions

```go
func (c *Command) ExecuteCommandWithOptions(
	command string,
	timeoutMs int,
	cwd string,
	envs map[string]string,
) (*CommandResult, error)
```

ExecuteCommandWithOptions executes a shell command with advanced options.

Executes a shell command in the session environment with configurable timeout, working directory,
and environment variables. The command runs with session user permissions in a Linux shell
environment.

Parameters:
  - command: The shell command to execute
  - timeoutMs: Timeout in milliseconds (optional, defaults to 1000ms/1s). Maximum allowed timeout is
    50000ms (50s). If a larger value is provided, it will be automatically limited to 50000ms
  - cwd: The working directory for command execution. If empty, the command runs in the default
    session directory
  - envs: Environment variables as a map of key-value pairs. These variables are set for the command
    execution only

Returns:
  - *CommandResult: Result containing command output, exit code, stdout, stderr, trace_id, and
    request ID
  - error: Error if the operation fails

**Example:**

```go
client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
result, _ := client.Create(nil)
defer result.Session.Delete()
cmdResult, _ := result.Session.Command.ExecuteCommandWithOptions(
	"pwd",
	5000,
	"/tmp",
	map[string]string{"TEST_VAR": "test_value"},
)
```

### Related Functions

### NewCommand

```go
func NewCommand(session interface {
	GetAPIKey() string
	GetClient() *mcp.Client
	GetSessionId() string
	IsVpc() bool
	NetworkInterfaceIp() string
	HttpPort() string
	FindServerForTool(toolName string) string
	CallMcpTool(toolName string, args interface{}, autoGenSession ...bool) (*models.McpToolResult, error)
}) *Command
```

NewCommand creates a new Command instance

## Type CommandResult

```go
type CommandResult struct {
	// Embed the basic API response structure
	models.ApiResponse
	// Success indicates whether the command execution was successful
	Success	bool	`json:"success"`
	// Output contains the command execution output (for backward compatibility, equals stdout if available, otherwise stderr)
	Output	string	`json:"output"`
	// ErrorMessage contains error message if the operation failed
	ErrorMessage	string	`json:"error_message,omitempty"`
	// ExitCode is the exit code of the command execution. Default is 0.
	ExitCode	int	`json:"exit_code"`
	// Stdout is the standard output from the command execution
	Stdout	string	`json:"stdout"`
	// Stderr is the standard error from the command execution
	Stderr	string	`json:"stderr"`
	// TraceID is the trace ID for error tracking. Only present when errorCode != 0. Used for quick problem localization.
	TraceID	string	`json:"trace_id,omitempty"`
}
```

CommandResult represents the result of a command execution

## Functions

### GetMobileCommandTemplate

```go
func GetMobileCommandTemplate(templateName string) (string, bool)
```

GetMobileCommandTemplate returns a mobile command template by name

## Best Practices

1. Always specify appropriate timeout values based on expected command duration
2. Handle command execution errors gracefully
3. Use absolute paths when referencing files in commands
4. Be aware that commands run with session user permissions
5. Clean up temporary files created by commands

## Related Resources

- [Session API Reference](session.md)
- [FileSystem API Reference](filesystem.md)

---

*Documentation generated automatically from Go source code.*
