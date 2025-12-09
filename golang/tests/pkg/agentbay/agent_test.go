package agentbay_test

import (
	"os"
	"strconv"
	"testing"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
	"github.com/aliyun/wuying-agentbay-sdk/golang/tests/pkg/agentbay/testutil"
)

func TestComputerAgent_ExecuteTask(t *testing.T) {
	// Create session parameters with Windows image for agent tasks
	params := agentbay.NewCreateSessionParams().WithImageId("windows_latest")

	// Setup session with cleanup
	session, cleanup := testutil.SetupAndCleanup(t, params)
	defer cleanup()

	// Test Agent task execution
	if session.Agent != nil {
		task := "create a folder named 'agentbay' in C:\\Windows\\Temp"

		// Get timeout from environment or use default
		maxTryTimesStr := os.Getenv("AGENT_TASK_TIMEOUT")
		maxTryTimes := 300 // default value
		if maxTryTimesStr != "" {
			if parsed, err := strconv.Atoi(maxTryTimesStr); err == nil {
				maxTryTimes = parsed
			}
		} else {
			t.Log("We will wait for 300 * 3 seconds to finish.")
		}

		t.Logf("Executing agent task: %s", task)
		result := session.Agent.Computer.ExecuteTask(task, maxTryTimes)

		t.Logf("Computer Agent task result with RequestID %s: Success=%v, TaskID=%s, Status=%s",
			result.RequestID, result.Success, result.TaskID, result.TaskStatus)

		if !result.Success {
			t.Errorf("Computer Agent task execution failed: %s", result.ErrorMessage)
		} else {
			t.Logf("Computer Agent task executed successfully with result:%s", result.TaskResult)

			if result.RequestID == "" {
				t.Errorf("Agent.Computer.ExecuteTask did not return RequestID")
			}

			if result.TaskID == "" {
				t.Errorf("Agent.Computer.ExecuteTask did not return TaskID")
			}
		}
	} else {
		t.Log("Note: Agent interface is nil, skipping agent test")
	}
}

func TestBrowserAgent_ExecuteTask(t *testing.T) {
	// Create session parameters with Windows image for agent tasks
	params := agentbay.NewCreateSessionParams().WithImageId("linux_latest")

	// Setup session with cleanup
	session, cleanup := testutil.SetupAndCleanup(t, params)
	defer cleanup()

	// Test Agent task execution
	if session.Agent != nil {
		task := "Navigate to baidu.com and Query the date when Alibaba listed in the U.S"

		// Get timeout from environment or use default
		maxTryTimesStr := os.Getenv("AGENT_TASK_TIMEOUT")
		maxTryTimes := 300 // default value
		if maxTryTimesStr != "" {
			if parsed, err := strconv.Atoi(maxTryTimesStr); err == nil {
				maxTryTimes = parsed
			}
		} else {
			t.Log("We will wait for 300 * 3 seconds to finish.")
		}

		t.Logf("Executing agent task: %s", task)
		result := session.Agent.Browser.ExecuteTask(task, maxTryTimes)

		t.Logf("Browser Agent task result with RequestID %s: Success=%v, TaskID=%s, Status=%s",
			result.RequestID, result.Success, result.TaskID, result.TaskStatus)

		if !result.Success {
			t.Errorf("Browser Agent task execution failed: %s", result.ErrorMessage)
		} else {
			t.Logf("Browser Agent task executed successfully with result:%s", result.TaskResult)

			if result.RequestID == "" {
				t.Errorf("Agent.Browser.ExecuteTask did not return RequestID")
			}

			if result.TaskID == "" {
				t.Errorf("Agent.Browser.ExecuteTask did not return TaskID")
			}
		}
	} else {
		t.Log("Note: Agent interface is nil, skipping agent test")
	}
}
