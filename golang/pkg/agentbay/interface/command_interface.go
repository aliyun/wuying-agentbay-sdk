package interfaces

import (
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/command"
)

//go:generate mockgen -destination=../../../tests/pkg/unit/mock/mock_command.go -package=mock github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/interface CommandInterface

// CommandInterface defines the interface for command operations
type CommandInterface interface {
	// ExecuteCommand executes a command with optional timeout
	ExecuteCommand(command string, timeoutMs ...int) (*command.CommandResult, error)

	// RunCode executes code in the specified language with optional timeout
	RunCode(code string, language string, timeoutS ...int) (*command.CommandResult, error)
}
