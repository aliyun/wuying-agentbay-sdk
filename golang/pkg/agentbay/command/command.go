package command

import (
	"encoding/json"
	"fmt"

	"github.com/alibabacloud-go/tea/tea"
	mcp "github.com/aliyun/wuying-agentbay-sdk/golang/api/client"
)

// Command handles command execution operations in the AgentBay cloud environment.
type Command struct {
	Session interface {
		GetAPIKey() string
		GetClient() *mcp.Client
		GetSessionId() string
	}
}

// NewCommand creates a new Command object.
func NewCommand(session interface {
	GetAPIKey() string
	GetClient() *mcp.Client
	GetSessionId() string
}) *Command {
	return &Command{
		Session: session,
	}
}

// ExecuteCommand executes a command in the cloud environment.
func (c *Command) ExecuteCommand(command string) (string, error) {
	args := map[string]string{
		"command": command,
	}
	argsJSON, err := json.Marshal(args)
	if err != nil {
		return "", fmt.Errorf("failed to marshal args: %w", err)
	}

	callToolRequest := &mcp.CallMcpToolRequest{
		Authorization: tea.String("Bearer " + c.Session.GetAPIKey()),
		SessionId:     tea.String(c.Session.GetSessionId()),
		Name:          tea.String("execute_command"),
		Args:          tea.String(string(argsJSON)),
	}
	response, err := c.Session.GetClient().CallMcpTool(callToolRequest)
	if err != nil {
		return "", fmt.Errorf("failed to read file: %w", err)
	}

	// 将 interface{} 转换为 map
	data, ok := response.Body.Data.(map[string]interface{})
	if !ok {
		return "", fmt.Errorf("invalid response data format")
	}

	// 获取 content 字段并解析为数组
	contentArray, ok := data["content"].([]interface{})
	if !ok {
		return "", fmt.Errorf("content field not found or not an array")
	}

	var fullText string
	for _, item := range contentArray {
		// 断言每个元素是 map[string]interface{}
		contentItem, ok := item.(map[string]interface{})
		if !ok {
			continue
		}

		// 提取 text 字段
		text, ok := contentItem["text"].(string)
		if !ok {
			continue
		}

		fullText += text + "\n" // 拼接文本内容
	}
	return fullText, nil
}
