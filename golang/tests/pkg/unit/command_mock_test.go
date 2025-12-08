package agentbay_test

import (
	"encoding/json"
	"testing"

	mcp "github.com/aliyun/wuying-agentbay-sdk/golang/api/client"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/command"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/models"
	"github.com/aliyun/wuying-agentbay-sdk/golang/tests/pkg/unit/mock"
	"github.com/golang/mock/gomock"
	"github.com/stretchr/testify/assert"
)

// CommandTestMockSession is a simple mock implementation of the Session interface for testing implementation logic
type CommandTestMockSession struct {
	callMcpToolFunc func(toolName string, args interface{}, autoGenSession ...bool) (*models.McpToolResult, error)
}

func (m *CommandTestMockSession) GetAPIKey() string {
	return "test-api-key"
}

func (m *CommandTestMockSession) GetClient() *mcp.Client {
	return nil
}

func (m *CommandTestMockSession) GetSessionId() string {
	return "test-session-id"
}

func (m *CommandTestMockSession) IsVpc() bool {
	return false
}

func (m *CommandTestMockSession) NetworkInterfaceIp() string {
	return ""
}

func (m *CommandTestMockSession) HttpPort() string {
	return ""
}

func (m *CommandTestMockSession) FindServerForTool(toolName string) string {
	return ""
}

func (m *CommandTestMockSession) CallMcpTool(toolName string, args interface{}, autoGenSession ...bool) (*models.McpToolResult, error) {
	if m.callMcpToolFunc != nil {
		return m.callMcpToolFunc(toolName, args, autoGenSession...)
	}
	return nil, nil
}

func TestCommand_ExecuteCommand_WithMockClient(t *testing.T) {
	ctrl := gomock.NewController(t)
	defer ctrl.Finish()

	// Create mock Command
	mockCmd := mock.NewMockCommandInterface(ctrl)

	// Set expected behavior
	expectedResult := &command.CommandResult{
		Success:  true,
		Output:   "Command executed successfully",
		ExitCode: 0,
		Stdout:   "Command executed successfully",
		Stderr:   "",
	}
	mockCmd.EXPECT().ExecuteCommand("ls -la").Return(expectedResult, nil)

	// Test ExecuteCommand method call
	result, err := mockCmd.ExecuteCommand("ls -la")

	// Verify call success
	assert.NoError(t, err)
	assert.NotNil(t, result)
	assert.Equal(t, "Command executed successfully", result.Output)
}

func TestCommand_ExecuteCommandWithTimeout_WithMockClient(t *testing.T) {
	ctrl := gomock.NewController(t)
	defer ctrl.Finish()

	// Create mock Command
	mockCmd := mock.NewMockCommandInterface(ctrl)

	// Set expected behavior
	expectedResult := &command.CommandResult{
		Success:  true,
		Output:   "Command executed with timeout",
		ExitCode: 0,
		Stdout:   "Command executed with timeout",
		Stderr:   "",
	}
	mockCmd.EXPECT().ExecuteCommand("ls -la", 5000).Return(expectedResult, nil)

	// Test ExecuteCommand with timeout method call
	result, err := mockCmd.ExecuteCommand("ls -la", 5000)

	// Verify call success
	assert.NoError(t, err)
	assert.NotNil(t, result)
	assert.Equal(t, "Command executed with timeout", result.Output)
}

func TestCommand_Error_WithMockClient(t *testing.T) {
	ctrl := gomock.NewController(t)
	defer ctrl.Finish()

	// Create mock Command
	mockCmd := mock.NewMockCommandInterface(ctrl)

	// Set expected behavior - return error
	mockCmd.EXPECT().ExecuteCommand("invalid_command").Return(nil, assert.AnError)

	// Test error case
	result, err := mockCmd.ExecuteCommand("invalid_command")

	// Verify error handling
	assert.Error(t, err)
	assert.Nil(t, result)
}

func TestCommand_NewReturnFormat_WithMockClient(t *testing.T) {
	ctrl := gomock.NewController(t)
	defer ctrl.Finish()

	// Create mock Command
	mockCmd := mock.NewMockCommandInterface(ctrl)

	// Set expected behavior with new return format
	expectedResult := &command.CommandResult{
		Success:      true,
		Output:       "output text",
		ExitCode:     0,
		Stdout:       "output text",
		Stderr:       "error text",
		TraceID:      "",
		ErrorMessage: "",
	}
	mockCmd.EXPECT().ExecuteCommand("ls -la").Return(expectedResult, nil)

	// Test ExecuteCommand method call
	result, err := mockCmd.ExecuteCommand("ls -la")

	// Verify call success
	assert.NoError(t, err)
	assert.NotNil(t, result)
	assert.Equal(t, "output text", result.Output)
	assert.Equal(t, 0, result.ExitCode)
	assert.Equal(t, "output text", result.Stdout)
	assert.Equal(t, "error text", result.Stderr)
	assert.Equal(t, "", result.TraceID)
}

func TestCommand_NewReturnFormatError_WithMockClient(t *testing.T) {
	ctrl := gomock.NewController(t)
	defer ctrl.Finish()

	// Create mock Command
	mockCmd := mock.NewMockCommandInterface(ctrl)

	// Set expected behavior with error format
	expectedResult := &command.CommandResult{
		Success:      false,
		Output:       "command not found",
		ExitCode:     127,
		Stdout:       "",
		Stderr:       "command not found",
		TraceID:      "trace-123",
		ErrorMessage: "command not found",
	}
	mockCmd.EXPECT().ExecuteCommand("invalid_command").Return(expectedResult, nil)

	// Test ExecuteCommand method call
	result, err := mockCmd.ExecuteCommand("invalid_command")

	// Verify call success
	assert.NoError(t, err)
	assert.NotNil(t, result)
	assert.Equal(t, false, result.Success)
	assert.Equal(t, 127, result.ExitCode)
	assert.Equal(t, "", result.Stdout)
	assert.Equal(t, "command not found", result.Stderr)
	assert.Equal(t, "trace-123", result.TraceID)
}

// ============================================================================
// Implementation Tests - Testing Command implementation logic directly
// ============================================================================

func TestCommand_Implementation_NewJsonFormat(t *testing.T) {
	// Test new JSON format response parsing
	jsonData := map[string]interface{}{
		"stdout":    "output text",
		"stderr":    "error text",
		"errorCode": 0,
		"traceId":   "",
	}
	jsonBytes, _ := json.Marshal(jsonData)

	mockResult := &models.McpToolResult{
		Success:      true,
		Data:         string(jsonBytes),
		ErrorMessage: "",
		RequestID:    "request-123",
	}

	mockSession := &CommandTestMockSession{
		callMcpToolFunc: func(toolName string, args interface{}, autoGenSession ...bool) (*models.McpToolResult, error) {
			assert.Equal(t, "shell", toolName)
			return mockResult, nil
		},
	}
	cmd := command.NewCommand(mockSession)

	result, err := cmd.ExecuteCommand("ls -la")

	assert.NoError(t, err)
	assert.NotNil(t, result)
	assert.Equal(t, "request-123", result.RequestID)
	assert.True(t, result.Success)
	assert.Equal(t, 0, result.ExitCode)
	assert.Equal(t, "output text", result.Stdout)
	assert.Equal(t, "error text", result.Stderr)
	assert.Equal(t, "output text", result.Output)
	assert.Equal(t, "", result.TraceID)
}

func TestCommand_Implementation_NewJsonFormatError(t *testing.T) {
	// Test new JSON format response with error parsing
	jsonData := map[string]interface{}{
		"stdout":    "",
		"stderr":    "command not found",
		"errorCode": 127,
		"traceId":   "trace-123",
	}
	jsonBytes, _ := json.Marshal(jsonData)

	mockResult := &models.McpToolResult{
		Success:      true,
		Data:         string(jsonBytes),
		ErrorMessage: "",
		RequestID:    "request-123",
	}

	mockSession := &CommandTestMockSession{
		callMcpToolFunc: func(toolName string, args interface{}, autoGenSession ...bool) (*models.McpToolResult, error) {
			assert.Equal(t, "shell", toolName)
			return mockResult, nil
		},
	}
	cmd := command.NewCommand(mockSession)

	result, err := cmd.ExecuteCommand("invalid_command")

	assert.NoError(t, err)
	assert.NotNil(t, result)
	assert.Equal(t, "request-123", result.RequestID)
	assert.False(t, result.Success)
	assert.Equal(t, 127, result.ExitCode)
	assert.Equal(t, "", result.Stdout)
	assert.Equal(t, "command not found", result.Stderr)
	assert.Equal(t, "command not found", result.Output)
	assert.Equal(t, "trace-123", result.TraceID)
}

func TestCommand_Implementation_CwdAndEnvs(t *testing.T) {
	// Test cwd and envs parameters
	mockResult := &models.McpToolResult{
		Success:      true,
		Data:         "test output",
		ErrorMessage: "",
		RequestID:    "request-123",
	}

	var capturedArgs interface{}
	mockSession := &CommandTestMockSession{
		callMcpToolFunc: func(toolName string, args interface{}, autoGenSession ...bool) (*models.McpToolResult, error) {
			assert.Equal(t, "shell", toolName)
			capturedArgs = args
			return mockResult, nil
		},
	}
	cmd := command.NewCommand(mockSession)

	result, err := cmd.ExecuteCommandWithOptions("pwd", 5000, "/tmp", map[string]string{"TEST_VAR": "test_value"})

	assert.NoError(t, err)
	assert.NotNil(t, result)
	assert.True(t, result.Success)

	// Verify arguments
	argsMap := capturedArgs.(map[string]interface{})
	assert.Equal(t, "pwd", argsMap["command"])
	assert.Equal(t, 5000, argsMap["timeout_ms"])
	assert.Equal(t, "/tmp", argsMap["cwd"])
	envs := argsMap["envs"].(map[string]interface{})
	assert.Equal(t, "test_value", envs["TEST_VAR"])
}

func TestCommand_Implementation_TimeoutLimit(t *testing.T) {
	// Test timeout limit enforcement (50s maximum)
	mockResult := &models.McpToolResult{
		Success:      true,
		Data:         "test output",
		ErrorMessage: "",
		RequestID:    "request-123",
	}

	// Test with timeout exceeding 50s (50000ms) - should be limited to 50s
	var capturedTimeout1 interface{}
	mockSession1 := &CommandTestMockSession{
		callMcpToolFunc: func(toolName string, args interface{}, autoGenSession ...bool) (*models.McpToolResult, error) {
			capturedTimeout1 = args.(map[string]interface{})["timeout_ms"]
			return mockResult, nil
		},
	}
	cmd1 := command.NewCommand(mockSession1)
	result1, err1 := cmd1.ExecuteCommand("ls -la", 60000)
	assert.NoError(t, err1)
	assert.NotNil(t, result1)
	assert.Equal(t, 50000, capturedTimeout1) // Should be limited to 50s

	// Test with timeout exactly at limit
	var capturedTimeout2 interface{}
	mockSession2 := &CommandTestMockSession{
		callMcpToolFunc: func(toolName string, args interface{}, autoGenSession ...bool) (*models.McpToolResult, error) {
			capturedTimeout2 = args.(map[string]interface{})["timeout_ms"]
			return mockResult, nil
		},
	}
	cmd2 := command.NewCommand(mockSession2)
	result2, err2 := cmd2.ExecuteCommand("ls -la", 50000)
	assert.NoError(t, err2)
	assert.NotNil(t, result2)
	assert.Equal(t, 50000, capturedTimeout2) // Should remain 50s

	// Test with timeout below limit
	var capturedTimeout3 interface{}
	mockSession3 := &CommandTestMockSession{
		callMcpToolFunc: func(toolName string, args interface{}, autoGenSession ...bool) (*models.McpToolResult, error) {
			capturedTimeout3 = args.(map[string]interface{})["timeout_ms"]
			return mockResult, nil
		},
	}
	cmd3 := command.NewCommand(mockSession3)
	result3, err3 := cmd3.ExecuteCommand("ls -la", 30000)
	assert.NoError(t, err3)
	assert.NotNil(t, result3)
	assert.Equal(t, 30000, capturedTimeout3) // Should remain unchanged
}
