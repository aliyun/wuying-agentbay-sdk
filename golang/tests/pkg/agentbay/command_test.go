package agentbay_test

import (
	"fmt"
	"strings"
	"testing"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
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

func TestCommand_RunCode(t *testing.T) {
	// Create session parameters with ImageId set to code_latest
	params := agentbay.NewCreateSessionParams().WithImageId("code_latest")

	// Setup session with cleanup
	session, cleanup := testutil.SetupAndCleanup(t, params)
	defer cleanup()

	// Test RunCode execution
	if session.Command != nil {
		// Test with Python code
		fmt.Println("Executing Python code...")
		pythonCode := `
print("Hello, world!")
x = 1 + 1
print(x)
`
		// Test with default timeout
		cmdResult, err := session.Command.RunCode(pythonCode, "python")
		if err != nil {
			t.Logf("Note: Python code execution failed: %v", err)
		} else {
			result := cmdResult.Output
			t.Logf("Python code execution result with RequestID %s: %s", cmdResult.RequestID, result)

			// Check if response contains "tool not found"
			if testutil.ContainsToolNotFound(result) {
				t.Errorf("Command.RunCode returned 'tool not found'")
			}

			// Verify the response contains expected output
			if !strings.Contains(result, "Hello, world!") || !strings.Contains(result, "2") {
				t.Errorf("Python code verification failed: expected 'Hello, world!' and '2' in response, got '%s'", result)
			} else {
				t.Logf("Python code execution verified successfully")
			}

			if cmdResult.RequestID == "" {
				t.Errorf("Command.RunCode did not return RequestID")
			}
		}

		// Test with JavaScript code and custom timeout
		fmt.Println("Executing JavaScript code with custom timeout...")
		jsCode := `
console.log("Hello, world!");
const x = 1 + 1;
console.log(x);
`
		customTimeout := 600 // 10 minutes
		cmdResultJs, err := session.Command.RunCode(jsCode, "javascript", customTimeout)
		if err != nil {
			t.Logf("Note: JavaScript code execution with custom timeout failed: %v", err)
		} else {
			resultJs := cmdResultJs.Output
			t.Logf("JavaScript code execution result with RequestID %s: %s", cmdResultJs.RequestID, resultJs)

			// Check if response contains "tool not found"
			if testutil.ContainsToolNotFound(resultJs) {
				t.Errorf("Command.RunCode with custom timeout returned 'tool not found'")
			}

			// Verify the response contains expected output
			if !strings.Contains(resultJs, "Hello, world!") || !strings.Contains(resultJs, "2") {
				t.Errorf("JavaScript code verification failed: expected 'Hello, world!' and '2' in response, got '%s'", resultJs)
			} else {
				t.Logf("JavaScript code execution verified successfully")
			}

			if cmdResultJs.RequestID == "" {
				t.Errorf("Command.RunCode with custom timeout did not return RequestID")
			}
		}

		// Test with invalid language
		fmt.Println("Testing with invalid language...")
		_, err = session.Command.RunCode("print('test')", "invalid_language")
		if err == nil {
			t.Errorf("Expected error for invalid language, but got nil")
		} else {
			t.Logf("Correctly received error for invalid language: %v", err)
		}
	} else {
		t.Logf("Note: Command interface is nil, skipping run_code test")
	}
}
