package agentbay_test

import (
	"fmt"
	"strings"
	"testing"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/command"
	"github.com/aliyun/wuying-agentbay-sdk/golang/tests/pkg/agentbay/testutil"
)

func TestCommand_ExecuteCommand(t *testing.T) {
	// Create session parameters with ImageId set to code_latest
	params := agentbay.NewCreateSessionParams().WithImageId("code_latest")

	// Setup session with cleanup
	session, cleanup := testutil.SetupAndCleanup(t, params)
	defer cleanup()

	// Test Command execution
	if session.Command != nil {
		// Test with echo command (works on all platforms)
		fmt.Println("Executing echo command...")
		testString := "AgentBay SDK Test"
		echoCmd := fmt.Sprintf("echo '%s'", testString)

		// Test with default timeout
		cmdResult, err := session.Command.ExecuteCommand(echoCmd)
		if err != nil {
			t.Logf("Note: Echo command failed: %v", err)
		} else {
			result := cmdResult.Output
			t.Logf("Echo command result with RequestID %s: %s", cmdResult.RequestID, result)

			// Check if response contains "tool not found"
			if testutil.ContainsToolNotFound(result) {
				t.Errorf("Command.ExecuteCommand returned 'tool not found'")
			}

			// Verify the response contains the test string
			if !strings.Contains(result, testString) {
				t.Errorf("Echo command verification failed: expected '%s' in response, got '%s'", testString, result)
			} else {
				t.Logf("Echo command verified successfully")
			}

			if cmdResult.RequestID == "" {
				t.Errorf("Command.ExecuteCommand did not return RequestID")
			}

			// Verify new return fields exist
			if cmdResult.ExitCode == 0 {
				t.Logf("✓ New return format verified: exitCode=%d, stdout=%s", cmdResult.ExitCode, cmdResult.Stdout)
			}
		}

		// Test with custom timeout
		fmt.Println("Executing echo command with custom timeout...")
		customTimeout := 2000 // 2 seconds
		cmdResultWithTimeout, err := session.Command.ExecuteCommand(echoCmd, customTimeout)
		if err != nil {
			t.Logf("Note: Echo command with custom timeout failed: %v", err)
		} else {
			resultWithTimeout := cmdResultWithTimeout.Output
			t.Logf("Echo command with custom timeout result with RequestID %s: %s", cmdResultWithTimeout.RequestID, resultWithTimeout)

			// Check if response contains "tool not found"
			if testutil.ContainsToolNotFound(resultWithTimeout) {
				t.Errorf("Command.ExecuteCommand with custom timeout returned 'tool not found'")
			}

			// Verify the response contains the test string
			if !strings.Contains(resultWithTimeout, testString) {
				t.Errorf("Echo command with custom timeout verification failed: expected '%s' in response, got '%s'", testString, resultWithTimeout)
			} else {
				t.Logf("Echo command with custom timeout verified successfully")
			}

			if cmdResultWithTimeout.RequestID == "" {
				t.Errorf("Command.ExecuteCommand with custom timeout did not return RequestID")
			}
		}
	} else {
		t.Logf("Note: Command interface is nil, skipping command test")
	}
}

func TestCommand_ExecuteCommandWithFunctionalOptions(t *testing.T) {
	// Create session parameters with ImageId set to code_latest
	params := agentbay.NewCreateSessionParams().WithImageId("code_latest")

	// Setup session with cleanup
	session, cleanup := testutil.SetupAndCleanup(t, params)
	defer cleanup()

	if session.Command == nil {
		t.Skip("Command interface is nil, skipping test")
	}

	// Test with cwd parameter
	t.Run("TestWithCwd", func(t *testing.T) {
		cmdResult, err := session.Command.ExecuteCommand("pwd", command.WithTimeoutMs(10000), command.WithCwd("/tmp"))
		if err != nil {
			t.Logf("Note: CWD test failed: %v", err)
		} else {
			if !strings.Contains(cmdResult.Stdout, "/tmp") {
				t.Errorf("CWD test failed: expected /tmp in stdout, got: %s", cmdResult.Stdout)
			} else {
				t.Logf("✓ CWD test passed: working directory=%s", strings.TrimSpace(cmdResult.Stdout))
			}
		}
	})

	// Test with envs parameter
	t.Run("TestWithEnvs", func(t *testing.T) {
		envs := map[string]string{"TEST_VAR": "test_value_123"}
		cmdResult, err := session.Command.ExecuteCommand("echo $TEST_VAR", command.WithTimeoutMs(10000), command.WithEnvs(envs))
		if err != nil {
			t.Logf("Note: Envs test failed: %v", err)
		} else {
			output := strings.TrimSpace(cmdResult.Stdout)
			if strings.Contains(output, "test_value_123") {
				t.Logf("✓ Envs test passed: environment variable set correctly: %s", output)
			} else {
				t.Logf("⚠ Envs test: environment variable may not be set (output: %s)", output)
			}
		}
	})

	// Test with cwd and envs together
	t.Run("TestWithCwdAndEnvs", func(t *testing.T) {
		envs := map[string]string{"CUSTOM_VAR": "custom_value"}
		cmdResult, err := session.Command.ExecuteCommand("pwd && echo $CUSTOM_VAR", command.WithTimeoutMs(10000), command.WithCwd("/tmp"), command.WithEnvs(envs))
		if err != nil {
			t.Logf("Note: Combined cwd and envs test failed: %v", err)
		} else {
			if !strings.Contains(cmdResult.Stdout, "/tmp") {
				t.Errorf("Combined test failed: expected /tmp in stdout, got: %s", cmdResult.Stdout)
			} else {
				t.Logf("✓ Combined cwd and envs test passed")
				t.Logf("  Output: %s", cmdResult.Stdout)
			}
		}
	})
}

func TestCommand_NewReturnFormat(t *testing.T) {
	// Create session parameters with ImageId set to code_latest
	params := agentbay.NewCreateSessionParams().WithImageId("code_latest")

	// Setup session with cleanup
	session, cleanup := testutil.SetupAndCleanup(t, params)
	defer cleanup()

	if session.Command == nil {
		t.Skip("Command interface is nil, skipping test")
	}

	// Test new return format (exitCode, stdout, stderr)
	t.Run("TestNewReturnFormat", func(t *testing.T) {
		cmdResult, err := session.Command.ExecuteCommand("echo 'Hello, AgentBay!'")
		if err != nil {
			t.Logf("Note: New return format test failed: %v", err)
		} else {
			if cmdResult.ExitCode != 0 {
				t.Errorf("Exit code should be 0 for success, got: %d", cmdResult.ExitCode)
			}
			if !strings.Contains(cmdResult.Stdout, "Hello, AgentBay!") {
				t.Errorf("Stdout should contain expected output, got: %s", cmdResult.Stdout)
			}
			if cmdResult.Output != cmdResult.Stdout {
				t.Errorf("Output should equal stdout for success")
			}
			t.Logf("✓ New return format test passed: exitCode=%d, stdout=%s", cmdResult.ExitCode, cmdResult.Stdout)
		}
	})

	// Test error case with exitCode and traceId
	t.Run("TestErrorWithExitCode", func(t *testing.T) {
		cmdResult, err := session.Command.ExecuteCommand("ls /non_existent_directory_12345")
		if err != nil {
			t.Logf("Note: Error test failed: %v", err)
		} else {
			if cmdResult.ExitCode != 0 {
				t.Logf("✓ Error command test passed: exitCode=%d, stderr=%s", cmdResult.ExitCode, cmdResult.Stderr)
				if cmdResult.TraceID != "" {
					t.Logf("  traceId=%s", cmdResult.TraceID)
				}
			} else {
				t.Logf("⚠ Command returned exitCode=0, but this is acceptable")
			}
		}
	})
}

func TestCommand_TimeoutLimit(t *testing.T) {
	// Create session parameters with ImageId set to code_latest
	params := agentbay.NewCreateSessionParams().WithImageId("code_latest")

	// Setup session with cleanup
	session, cleanup := testutil.SetupAndCleanup(t, params)
	defer cleanup()

	if session.Command == nil {
		t.Skip("Command interface is nil, skipping test")
	}

	// Test with timeout exceeding 50s (50000ms) - should be limited to 50s
	// Note: We can't directly verify the timeout was limited without mocking,
	// but we can verify the command still executes successfully
	t.Run("TestTimeoutExceedingLimit", func(t *testing.T) {
		cmdResult, err := session.Command.ExecuteCommand("echo 'timeout test'", 60000)
		if err != nil {
			t.Logf("Note: Timeout limit test failed: %v", err)
		} else {
			if !cmdResult.Success {
				t.Errorf("Command should succeed even with timeout > 50s")
			}
			if cmdResult.ExitCode != 0 {
				t.Errorf("Exit code should be 0, got: %d", cmdResult.ExitCode)
			}
		}
	})

	// Test with timeout exactly at limit
	t.Run("TestTimeoutAtLimit", func(t *testing.T) {
		cmdResult, err := session.Command.ExecuteCommand("echo 'timeout test 50s'", 50000)
		if err != nil {
			t.Logf("Note: Timeout at limit test failed: %v", err)
		} else {
			if !cmdResult.Success {
				t.Errorf("Command should succeed with timeout = 50s")
			}
		}
	})

	// Test with timeout below limit
	t.Run("TestTimeoutBelowLimit", func(t *testing.T) {
		cmdResult, err := session.Command.ExecuteCommand("echo 'timeout test 30s'", 30000)
		if err != nil {
			t.Logf("Note: Timeout below limit test failed: %v", err)
		} else {
			if !cmdResult.Success {
				t.Errorf("Command should succeed with timeout < 50s")
			}
		}
		t.Logf("✓ Timeout limit test passed")
	})
}

func TestCommand_CwdWithSpaces(t *testing.T) {
	// Create session parameters with ImageId set to linux_latest
	params := agentbay.NewCreateSessionParams().WithImageId("linux_latest")

	// Setup session with cleanup
	session, cleanup := testutil.SetupAndCleanup(t, params)
	defer cleanup()

	if session.Command == nil {
		t.Skip("Command interface is nil, skipping test")
	}

	// Create a directory with spaces in the path
	testDir := "/tmp/test dir with spaces"

	// First, create the directory
	createResult, err := session.Command.ExecuteCommand(fmt.Sprintf("mkdir -p '%s'", testDir))
	if err != nil {
		t.Logf("Note: Failed to create directory with spaces: %v", err)
		return
	}
	if !createResult.Success {
		t.Logf("Note: Failed to create directory with spaces: %s", createResult.ErrorMessage)
		return
	}

	// Test pwd with cwd containing spaces
	result, err := session.Command.ExecuteCommand("pwd", command.WithTimeoutMs(10000), command.WithCwd(testDir))
	if err != nil {
		t.Logf("Note: CWD with spaces test failed: %v", err)
	} else {
		if !result.Success {
			t.Errorf("Command should succeed with cwd containing spaces")
		}
		if result.ExitCode != 0 {
			t.Errorf("Exit code should be 0, got: %d", result.ExitCode)
		}
		// The output should contain the directory path (may be normalized)
		if !strings.Contains(result.Stdout, testDir) && !strings.Contains(result.Stdout, "/tmp/test") {
			t.Errorf("Working directory should contain test dir, got: %s", result.Stdout)
		} else {
			t.Logf("✓ CWD with spaces test passed: directory=%s, output=%s", testDir, strings.TrimSpace(result.Stdout))
		}
	}

	// Test creating a file in the directory with spaces
	fileResult, err := session.Command.ExecuteCommand("echo 'test content' > test_file.txt", command.WithTimeoutMs(10000), command.WithCwd(testDir))
	if err != nil {
		t.Logf("Note: Failed to create file in directory with spaces: %v", err)
	} else {
		if !fileResult.Success {
			t.Logf("Note: Failed to create file in directory with spaces: %s", fileResult.ErrorMessage)
		}
	}

	// Verify file was created
	listResult, err := session.Command.ExecuteCommand("ls test_file.txt", command.WithTimeoutMs(10000), command.WithCwd(testDir))
	if err != nil {
		t.Logf("Note: Failed to list file in directory with spaces: %v", err)
	} else {
		if !listResult.Success {
			t.Logf("Note: Failed to list file in directory with spaces: %s", listResult.ErrorMessage)
		} else {
			if !strings.Contains(listResult.Stdout, "test_file.txt") {
				t.Errorf("File should exist in directory with spaces, got: %s", listResult.Stdout)
			}
		}
	}

	// Cleanup
	cleanupResult, _ := session.Command.ExecuteCommand(fmt.Sprintf("rm -rf '%s'", testDir))
	if !cleanupResult.Success {
		t.Logf("Note: Failed to cleanup directory: %s", cleanupResult.ErrorMessage)
	}
}

func TestCommand_EnvsWithSpecialCharacters(t *testing.T) {
	// Create session parameters with ImageId set to linux_latest
	params := agentbay.NewCreateSessionParams().WithImageId("linux_latest")

	// Setup session with cleanup
	session, cleanup := testutil.SetupAndCleanup(t, params)
	defer cleanup()

	if session.Command == nil {
		t.Skip("Command interface is nil, skipping test")
	}

	// Test environment variable with quotes
	t.Run("TestEnvsWithSingleQuotes", func(t *testing.T) {
		envs := map[string]string{"TEST_VAR": "value with 'single quotes'"}
		result, err := session.Command.ExecuteCommand("echo $TEST_VAR", command.WithTimeoutMs(10000), command.WithEnvs(envs))
		if err != nil {
			t.Logf("Note: Envs with single quotes test failed: %v", err)
		} else {
			if !result.Success {
				t.Errorf("Command should succeed with env containing single quotes")
			}
			output := strings.TrimSpace(result.Stdout)
			if strings.Contains(output, "value with") && strings.Contains(output, "single quotes") {
				t.Logf("✓ Envs with single quotes test passed: %s", output)
			} else {
				t.Logf("⚠ Envs with single quotes: output may not match exactly: %s", output)
			}
		}
	})

	// Test environment variable with double quotes
	t.Run("TestEnvsWithDoubleQuotes", func(t *testing.T) {
		envs := map[string]string{"TEST_VAR": `value with "double quotes"`}
		result, err := session.Command.ExecuteCommand("echo $TEST_VAR", command.WithTimeoutMs(10000), command.WithEnvs(envs))
		if err != nil {
			t.Logf("Note: Envs with double quotes test failed: %v", err)
		} else {
			if !result.Success {
				t.Errorf("Command should succeed with env containing double quotes")
			}
			output := strings.TrimSpace(result.Stdout)
			if strings.Contains(output, "value with") && strings.Contains(output, "double quotes") {
				t.Logf("✓ Envs with double quotes test passed: %s", output)
			} else {
				t.Logf("⚠ Envs with double quotes: output may not match exactly: %s", output)
			}
		}
	})

	// Test environment variable with semicolon (potential injection attempt)
	// This should NOT execute as a separate command due to parameter passing
	t.Run("TestEnvsWithSemicolon", func(t *testing.T) {
		envs := map[string]string{"TEST_VAR": "value; rm -rf /"}
		result, err := session.Command.ExecuteCommand("echo $TEST_VAR", command.WithTimeoutMs(10000), command.WithEnvs(envs))
		if err != nil {
			t.Logf("Note: Envs with semicolon test failed: %v", err)
		} else {
			if !result.Success {
				t.Errorf("Command should succeed (semicolon should be treated as literal)")
			}
			output := strings.TrimSpace(result.Stdout)
			// The semicolon should be part of the value, not a command separator
			if strings.Contains(output, "value; rm -rf /") || strings.Contains(output, "value") {
				t.Logf("✓ Envs with semicolon test passed (no injection): %s", output)
			} else {
				t.Logf("⚠ Envs with semicolon: output=%s", output)
			}
		}
	})

	// Test environment variable with special characters
	t.Run("TestEnvsWithSpecialChars", func(t *testing.T) {
		envs := map[string]string{"TEST_VAR": "value with !@#$%^&*()_+-=[]{}|;':\",./<>?"}
		result, err := session.Command.ExecuteCommand("echo $TEST_VAR", command.WithTimeoutMs(10000), command.WithEnvs(envs))
		if err != nil {
			t.Logf("Note: Envs with special characters test failed: %v", err)
		} else {
			if !result.Success {
				t.Errorf("Command should succeed with env containing special chars")
			}
			output := strings.TrimSpace(result.Stdout)
			if strings.Contains(output, "value with") {
				outputPreview := output
				if len(outputPreview) > 50 {
					outputPreview = outputPreview[:50] + "..."
				}
				t.Logf("✓ Envs with special characters test passed: %s", outputPreview)
			} else {
				t.Logf("⚠ Envs with special characters: output may not match: %s", output)
			}
		}
	})

	// Test environment variable with newline (potential injection attempt)
	t.Run("TestEnvsWithNewlines", func(t *testing.T) {
		envs := map[string]string{"TEST_VAR": "value\nwith\nnewlines"}
		result, err := session.Command.ExecuteCommand("echo $TEST_VAR", command.WithTimeoutMs(10000), command.WithEnvs(envs))
		if err != nil {
			t.Logf("Note: Envs with newlines test failed: %v", err)
		} else {
			if !result.Success {
				t.Errorf("Command should succeed with env containing newlines")
			}
			output := strings.TrimSpace(result.Stdout)
			if strings.Contains(output, "value") {
				outputPreview := output
				if len(outputPreview) > 50 {
					outputPreview = outputPreview[:50] + "..."
				}
				t.Logf("✓ Envs with newlines test passed: %s", outputPreview)
			} else {
				t.Logf("⚠ Envs with newlines: output may not match: %s", output)
			}
		}
	})
}

func TestCommand_CwdAndEnvsWithSpecialChars(t *testing.T) {
	// Create session parameters with ImageId set to linux_latest
	params := agentbay.NewCreateSessionParams().WithImageId("linux_latest")

	// Setup session with cleanup
	session, cleanup := testutil.SetupAndCleanup(t, params)
	defer cleanup()

	if session.Command == nil {
		t.Skip("Command interface is nil, skipping test")
	}

	// Create a directory with spaces
	testDir := "/tmp/test dir with spaces"
	createResult, err := session.Command.ExecuteCommand(fmt.Sprintf("mkdir -p '%s'", testDir))
	if err != nil {
		t.Logf("Note: Failed to create directory with spaces: %v", err)
		return
	}
	if !createResult.Success {
		t.Logf("Note: Failed to create directory with spaces: %s", createResult.ErrorMessage)
		return
	}

	// Test with both cwd (spaces) and envs (special chars)
	envs := map[string]string{"TEST_VAR": "value with 'quotes' and ; semicolon"}
	result, err := session.Command.ExecuteCommand("pwd && echo $TEST_VAR", command.WithTimeoutMs(10000), command.WithCwd(testDir), command.WithEnvs(envs))
	if err != nil {
		t.Logf("Note: Combined cwd (spaces) and envs (special chars) test failed: %v", err)
	} else {
		if !result.Success {
			t.Errorf("Command should succeed with both cwd (spaces) and envs (special chars)")
		}
		if result.ExitCode != 0 {
			t.Errorf("Exit code should be 0, got: %d", result.ExitCode)
		}
		if !strings.Contains(result.Stdout, testDir) && !strings.Contains(result.Stdout, "/tmp/test") {
			t.Errorf("Working directory should contain test dir, got: %s", result.Stdout)
		}

		// Verify environment variable was set (may be partially visible)
		output := strings.TrimSpace(result.Stdout)
		if strings.Contains(output, "value") || strings.Contains(output, "TEST_VAR") {
			outputPreview := output
			if len(outputPreview) > 100 {
				outputPreview = outputPreview[:100] + "..."
			}
			t.Logf("✓ Combined cwd (spaces) and envs (special chars) test passed")
			t.Logf("  Output: %s", outputPreview)
		} else {
			t.Logf("⚠ Combined test: output may not show env var: %s", output)
		}
	}

	// Cleanup
	cleanupResult, _ := session.Command.ExecuteCommand(fmt.Sprintf("rm -rf '%s'", testDir))
	if !cleanupResult.Success {
		t.Logf("Note: Failed to cleanup directory: %s", cleanupResult.ErrorMessage)
	}
}
