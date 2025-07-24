package command

import (
	"fmt"

	mcp "github.com/aliyun/wuying-agentbay-sdk/golang/api/client"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/models"
)

// CommandResult represents the result of a command execution
type CommandResult struct {
	models.ApiResponse // Embedded ApiResponse
	Output             string
}

// Command handles command execution operations in the AgentBay cloud environment.
type Command struct {
	Session interface {
		GetAPIKey() string
		GetClient() *mcp.Client
		GetSessionId() string
	}
}

// NewCommand creates a new Command instance
func NewCommand(session interface {
	GetAPIKey() string
	GetClient() *mcp.Client
	GetSessionId() string
}) *Command {
	return &Command{
		Session: session,
	}
}

// ExecuteCommand executes a command in the session environment.
func (c *Command) ExecuteCommand(command string, timeoutMs ...int) (*CommandResult, error) {
	// Set default timeout if not provided
	timeout := 1000
	if len(timeoutMs) > 0 && timeoutMs[0] > 0 {
		timeout = timeoutMs[0]
	}

	args := map[string]interface{}{
		"command":    command,
		"timeout_ms": timeout,
	}

	// Type assertion to access Session's CallMcpTool method
	if sessionWithCallTool, ok := c.Session.(interface {
		CallMcpTool(toolName string, args interface{}, defaultErrorMsg string) (interface{}, error)
	}); ok {
		result, err := sessionWithCallTool.CallMcpTool("execute_command", args, "Failed to execute command")
		if err != nil {
			return nil, err
		}

		// Type assertion to extract fields from result
		if callResult, ok := result.(interface {
			GetRequestID() string
			GetTextContent() string
		}); ok {
			return &CommandResult{
				ApiResponse: models.ApiResponse{
					RequestID: callResult.GetRequestID(),
				},
				Output: callResult.GetTextContent(),
			}, nil
		}
	}

	return nil, fmt.Errorf("session does not support CallMcpTool method")
}
