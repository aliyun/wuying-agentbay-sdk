package command

import (
	"encoding/json"
	"fmt"

	mcp "github.com/aliyun/wuying-agentbay-sdk/golang/api/client"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/models"
)

// CommandResult represents the result of a command execution
type CommandResult struct {
	// Embed the basic API response structure
	models.ApiResponse
	// Success indicates whether the command execution was successful
	Success bool `json:"success"`
	// Output contains the command execution output (for backward compatibility, equals stdout if available, otherwise stderr)
	Output string `json:"output"`
	// ErrorMessage contains error message if the operation failed
	ErrorMessage string `json:"error_message,omitempty"`
	// ExitCode is the exit code of the command execution. Default is 0.
	ExitCode int `json:"exit_code"`
	// Stdout is the standard output from the command execution
	Stdout string `json:"stdout"`
	// Stderr is the standard error from the command execution
	Stderr string `json:"stderr"`
	// TraceID is the trace ID for error tracking. Only present when errorCode != 0. Used for quick problem localization.
	TraceID string `json:"trace_id,omitempty"`
}

// Command handles command execution operations in the AgentBay cloud environment.
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

// NewCommand creates a new Command instance
func NewCommand(session interface {
	GetAPIKey() string
	GetClient() *mcp.Client
	GetSessionId() string
	IsVpc() bool
	NetworkInterfaceIp() string
	HttpPort() string
	FindServerForTool(toolName string) string
	CallMcpTool(toolName string, args interface{}, autoGenSession ...bool) (*models.McpToolResult, error)
}) *Command {
	return &Command{
		Session: session,
	}
}

// ExecuteCommand executes a shell command in the session environment.
//
// This method maintains backward compatibility with the original signature.
// For advanced features like working directory and environment variables,
// use ExecuteCommandWithOptions instead.
//
// Parameters:
//   - command: The shell command to execute
//   - timeoutMs: Timeout in milliseconds (optional, defaults to 1000ms/1s).
//     Maximum allowed timeout is 50000ms (50s). If a larger value
//     is provided, it will be automatically limited to 50000ms
//
// Returns:
//   - *CommandResult: Result containing command output, exit code, stdout,
//     stderr, trace_id, and request ID
//   - error: Error if the operation fails
//
// Example:
//
// ==================== Option Definitions ====================

// commandOptions holds the configuration for command execution
type commandOptions struct {
	timeoutMs int
	cwd       string
	envs      map[string]string
}

// CommandOption is a function type for configuring ExecuteCommand options.
// This enables the Functional Options pattern for flexible and extensible API design.
type CommandOption func(*commandOptions)

// WithTimeoutMs sets the timeout for command execution in milliseconds.
// Maximum allowed timeout is 50000ms (50s). If a larger value is provided,
// it will be automatically limited to 50000ms.
//
// Example:
//
//	cmd.ExecuteCommand("ls -la", WithTimeoutMs(5000))
func WithTimeoutMs(timeoutMs int) CommandOption {
	return func(opts *commandOptions) {
		opts.timeoutMs = timeoutMs
	}
}

// WithCwd sets the working directory for command execution.
// If not set, the command runs in the default session directory.
//
// Example:
//
//	cmd.ExecuteCommand("pwd", WithCwd("/tmp"))
func WithCwd(cwd string) CommandOption {
	return func(opts *commandOptions) {
		opts.cwd = cwd
	}
}

// WithEnvs sets environment variables for command execution.
// These variables are set for the command execution only.
//
// Example:
//
//	cmd.ExecuteCommand("echo $VAR", WithEnvs(map[string]string{"VAR": "value"}))
func WithEnvs(envs map[string]string) CommandOption {
	return func(opts *commandOptions) {
		opts.envs = envs
	}
}

// ExecuteCommand executes a shell command in the session environment.
//
// This method supports both the legacy signature (command string, timeoutMs ...int)
// and the Functional Options pattern for flexible configuration.
//
// Legacy usage (backward compatible):
//   - cmd.ExecuteCommand("ls -la")
//   - cmd.ExecuteCommand("ls -la", 5000)
//
// Functional Options usage (recommended for new code):
//   - cmd.ExecuteCommand("ls -la", WithTimeoutMs(5000))
//   - cmd.ExecuteCommand("pwd", WithCwd("/tmp"), WithEnvs(map[string]string{"VAR": "value"}))
//
// Executes a shell command in the session environment with configurable timeout,
// working directory, and environment variables. The command runs with session
// user permissions in a Linux shell environment.
//
// Parameters:
//   - command: The shell command to execute
//   - options: Either an int (timeoutMs in milliseconds) for legacy usage, or
//     CommandOption functions for Functional Options pattern.
//     Maximum allowed timeout is 50000ms (50s). If a larger value is provided,
//     it will be automatically limited to 50000ms
//
// Returns:
//   - *CommandResult: Result containing command output, exit code, stdout,
//     stderr, trace_id, and request ID
//   - error: Error if the operation fails
//
// Example:
//
//	// Default usage
//	cmd.ExecuteCommand("ls")
//
//	// Legacy usage (backward compatible)
//	cmd.ExecuteCommand("ls", 5000)
//
//	// New style with Functional Options
//	cmd.ExecuteCommand("ls", WithTimeoutMs(5000))
//
//	// Combined options
//	cmd.ExecuteCommand("pwd",
//	    WithTimeoutMs(5000),
//	    WithCwd("/tmp"),
//	    WithEnvs(map[string]string{"FOO": "bar"}),
>>>>>>> f2ef8d07 (Update command interface documentation to match API documentation standards)
//	)
func (c *Command) ExecuteCommand(command string, options ...interface{}) (*CommandResult, error) {
	// Default configuration
	opts := &commandOptions{
		timeoutMs: 1000, // Default 1 second
		cwd:       "",
		envs:      nil,
	}

	// Handle both old and new styles
	for _, opt := range options {
		switch v := opt.(type) {
		case int: // Old: ExecuteCommand("ls", 5000)
			if v > 0 {
				opts.timeoutMs = v
			}
		case CommandOption: // New: ExecuteCommand("ls", WithTimeoutMs(5000))
			if v != nil {
				v(opts)
			}
		}
	}

	return c.executeCommandInternal(command, opts.timeoutMs, opts.cwd, opts.envs)
}

// executeCommandInternal is the internal implementation of command execution
func (c *Command) executeCommandInternal(
	command string,
	timeout int,
	cwd string,
	envs map[string]string,
) (*CommandResult, error) {
	// Limit timeout to maximum 50s (50000ms) as per SDK constraints
	const MAX_TIMEOUT_MS = 50000
	if timeout > MAX_TIMEOUT_MS {
		// Log warning (in production, you might want to use a proper logger)
		// fmt.Printf("Warning: Timeout %dms exceeds maximum allowed %dms. Limiting to %dms.\n", timeout, MAX_TIMEOUT_MS, MAX_TIMEOUT_MS)
		timeout = MAX_TIMEOUT_MS
	}

	// Build request arguments
	args := map[string]interface{}{
		"command":    command,
		"timeout_ms": timeout,
	}
	if cwd != "" {
		args["cwd"] = cwd
	}
	if len(envs) > 0 {
		args["envs"] = envs
	}

	// Use Session's CallMcpTool method
	result, err := c.Session.CallMcpTool("shell", args)
	if err != nil {
		return nil, fmt.Errorf("failed to execute command: %w", err)
	}

	if result.Success {
		// Try to parse the new JSON format response
		var dataJson map[string]interface{}
		if err := json.Unmarshal([]byte(result.Data), &dataJson); err != nil {
			// Fallback to old format if JSON parsing fails
			return &CommandResult{
				ApiResponse: models.ApiResponse{
					RequestID: result.RequestID,
				},
				Success: true,
				Output:  result.Data,
			}, nil
		}

		// Extract fields from new format
		stdout := ""
		if val, ok := dataJson["stdout"].(string); ok {
			stdout = val
		}
		stderr := ""
		if val, ok := dataJson["stderr"].(string); ok {
			stderr = val
		}
		errorCode := 0
		if val, ok := dataJson["errorCode"].(float64); ok {
			errorCode = int(val)
		}
		traceID := ""
		if val, ok := dataJson["traceId"].(string); ok {
			traceID = val
		}

		// Determine success based on errorCode (0 means success)
		success := errorCode == 0

		// For backward compatibility, output should be stdout if available, otherwise stderr
		output := stdout
		if output == "" {
			output = stderr
		}

		return &CommandResult{
			ApiResponse: models.ApiResponse{
				RequestID: result.RequestID,
			},
			Success:      success,
			Output:       output,
			ExitCode:     errorCode,
			Stdout:       stdout,
			Stderr:       stderr,
			TraceID:      traceID,
			ErrorMessage: result.ErrorMessage,
		}, nil
	} else {
		// Try to parse error message as JSON (in case backend returns JSON in error)
		var errorData map[string]interface{}
		if err := json.Unmarshal([]byte(result.ErrorMessage), &errorData); err == nil {
			// Successfully parsed JSON from error message
			stdout := ""
			if val, ok := errorData["stdout"].(string); ok {
				stdout = val
			}
			stderr := ""
			if val, ok := errorData["stderr"].(string); ok {
				stderr = val
			}
			errorCode := 0
			if val, ok := errorData["errorCode"].(float64); ok {
				errorCode = int(val)
			}
			traceID := ""
			if val, ok := errorData["traceId"].(string); ok {
				traceID = val
			}
			output := stdout
			if output == "" {
				output = stderr
			}

			return &CommandResult{
				ApiResponse: models.ApiResponse{
					RequestID: result.RequestID,
				},
				Success:      false,
				Output:       output,
				ExitCode:     errorCode,
				Stdout:       stdout,
				Stderr:       stderr,
				TraceID:      traceID,
				ErrorMessage: stderr,
			}, nil
		}

		// If parsing fails, return error
		return &CommandResult{
			ApiResponse: models.ApiResponse{
				RequestID: result.RequestID,
			},
			Success:      false,
			Output:       "",
			ErrorMessage: result.ErrorMessage,
		}, nil
	}
}
