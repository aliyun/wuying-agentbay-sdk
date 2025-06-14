package filesystem

import (
	"encoding/json"
	"fmt"
	"strings"

	"github.com/alibabacloud-go/tea/tea"
	mcp "github.com/aliyun/wuying-agentbay-sdk/golang/api/client"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/command"
)

// FileSystem handles file operations in the AgentBay cloud environment.
type FileSystem struct {
	Session interface {
		GetAPIKey() string
		GetClient() *mcp.Client
		GetSessionId() string
	}
}

// NewFileSystem creates a new FileSystem object.
func NewFileSystem(session interface {
	GetAPIKey() string
	GetClient() *mcp.Client
	GetSessionId() string
}) *FileSystem {
	return &FileSystem{
		Session: session,
	}
}

// ReadFile reads the contents of a file in the cloud environment.
func (fs *FileSystem) ReadFile(path string) (string, error) {
	args := map[string]string{
		"path": path,
	}
	argsJSON, err := json.Marshal(args)
	if err != nil {
		return "", fmt.Errorf("failed to marshal args: %w", err)
	}

	callToolRequest := &mcp.CallMcpToolRequest{
		Authorization: tea.String("Bearer " + fs.Session.GetAPIKey()),
		SessionId:     tea.String(fs.Session.GetSessionId()),
		Name:          tea.String("read_file"),
		Args:          tea.String(string(argsJSON)),
	}

	// Log API request
	fmt.Println("API Call: CallMcpTool - read_file")
	fmt.Printf("Request: SessionId=%s, Args=%s\n", *callToolRequest.SessionId, *callToolRequest.Args)

	response, err := fs.Session.GetClient().CallMcpTool(callToolRequest)

	// Log API response
	if err != nil {
		fmt.Println("Error calling CallMcpTool - read_file:", err)
		return "", fmt.Errorf("failed to read file: %w", err)
	}
	if response != nil && response.Body != nil {
		fmt.Println("Response from CallMcpTool - read_file:", response.Body)
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

// WriteFile writes content to a file.
// API Parameters:
//
//	{
//	  "path": "file/path/to/write",
//	  "content": "Content to write to the file",
//	  "mode": "overwrite"  // Optional: "overwrite" (default) or "append"
//	}
func (fs *FileSystem) WriteFile(path, content string, mode string) (bool, error) {
	// Create a new Command object using the same session
	cmd := command.NewCommand(fs.Session)

	// If mode is not specified or invalid, default to "overwrite"
	if mode != "append" && mode != "overwrite" {
		mode = "overwrite"
	}

	// Determine the redirection operator based on the mode
	redirectOp := ">"
	if mode == "append" {
		redirectOp = ">>"
	}

	// Escape special characters in the content
	escapedContent := strings.Replace(content, "'", "'\\''", -1)

	// Construct the command to write content to file
	commandStr := fmt.Sprintf("echo -n '%s' %s '%s'", escapedContent, redirectOp, path)

	// Execute the command
	_, err := cmd.ExecuteCommand(commandStr)
	if err != nil {
		return false, fmt.Errorf("failed to write to file: %w", err)
	}

	return true, nil
}
