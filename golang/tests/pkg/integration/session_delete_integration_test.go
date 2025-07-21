package integration

import (
	"fmt"
	"os"
	"testing"
	"time"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

// TestSessionDeleteWithoutParams 测试不带参数Delete的集成测试
func TestSessionDeleteWithoutParams(t *testing.T) {
	// 获取API Key
	apiKey := os.Getenv("AGENTBAY_API_KEY")
	if apiKey == "" {
		t.Fatal("AGENTBAY_API_KEY environment variable is not set")
	}

	// 初始化AgentBay客户端
	client, err := agentbay.NewAgentBay(apiKey, nil)
	if err != nil {
		t.Fatalf("Failed to initialize AgentBay client: %v", err)
	}

	// 创建一个会话
	fmt.Println("Creating a new session for delete testing...")
	result, err := client.Create(nil)
	if err != nil {
		t.Fatalf("Failed to create session: %v", err)
	}
	session := result.Session
	t.Logf("Session created with ID: %s", session.SessionID)

	// 使用默认参数删除会话
	fmt.Println("Deleting session without parameters...")
	deleteResult, err := session.Delete()
	if err != nil {
		t.Fatalf("Failed to delete session: %v", err)
	}
	t.Logf("Session deleted (RequestID: %s)", deleteResult.RequestID)

	// 验证会话已被删除
	listResult, err := client.List()
	if err != nil {
		t.Fatalf("Failed to list sessions: %v", err)
	}

	for _, s := range listResult.Sessions {
		if s.SessionID == session.SessionID {
			t.Errorf("Session with ID %s still exists after deletion", session.SessionID)
		}
	}
}

// TestAgentBayDeleteWithSyncContext 测试AgentBay.Delete带syncContext参数的集成测试
func TestAgentBayDeleteWithSyncContext(t *testing.T) {
	// 获取API Key
	apiKey := os.Getenv("AGENTBAY_API_KEY")
	if apiKey == "" {
		t.Fatal("AGENTBAY_API_KEY environment variable is not set")
	}

	// 初始化AgentBay客户端
	client, err := agentbay.NewAgentBay(apiKey, nil)
	if err != nil {
		t.Fatalf("Failed to initialize AgentBay client: %v", err)
	}

	// 创建上下文
	contextName := "test-context-" + time.Now().Format("20060102150405")
	fmt.Println("Creating a new context...")
	createResult, err := client.Context.Create(contextName)
	if err != nil {
		t.Fatalf("Failed to create context: %v", err)
	}
	contextID := createResult.ContextID
	t.Logf("Context created with ID: %s", contextID)

	// 创建持久化配置
	persistenceData := []*agentbay.ContextSync{
		{
			ContextID: contextID,
			Path:      "/home/wuying/test",
		},
	}

	// 创建带上下文的会话
	params := agentbay.NewCreateSessionParams()
	params.ImageId = "linux_latest"
	params.ContextSync = persistenceData

	fmt.Println("Creating a new session with context...")
	result, err := client.Create(params)
	if err != nil {
		t.Fatalf("Failed to create session: %v", err)
	}
	session := result.Session
	t.Logf("Session created with ID: %s", session.SessionID)

	// 在会话中创建1GB大小的测试文件
	fmt.Println("Creating a 1GB test file for agentbay delete...")
	testCmd := "dd if=/dev/zero of=/home/wuying/test/testfile2.txt bs=1M count=1024"
	cmdResult, err := session.Command.ExecuteCommand(testCmd)
	if err != nil {
		t.Logf("Warning: Failed to create 1GB test file: %v", err)
	} else {
		t.Logf("Created 1GB test file: %s", cmdResult)
	}

	// 使用client.Delete带syncContext=true删除会话
	fmt.Println("Deleting session with AgentBay.Delete and syncContext=true...")
	deleteResult, err := client.Delete(session, true)
	if err != nil {
		t.Fatalf("Failed to delete session: %v", err)
	}
	t.Logf("Session deleted with client.Delete and syncContext=true (RequestID: %s)", deleteResult.RequestID)

	// 验证会话已被删除
	listResult, err := client.List()
	if err != nil {
		t.Fatalf("Failed to list sessions: %v", err)
	}

	for _, s := range listResult.Sessions {
		if s.SessionID == session.SessionID {
			t.Errorf("Session with ID %s still exists after deletion", session.SessionID)
		}
	}

	// 清理上下文
	// 创建Context对象用于删除
	getResult, err := client.Context.Get(contextName, false)
	if err == nil && getResult != nil && getResult.Context != nil {
		_, err = client.Context.Delete(getResult.Context)
		if err != nil {
			t.Logf("Warning: Failed to delete context: %v", err)
		} else {
			t.Logf("Context %s deleted", contextID)
		}
	}
}
