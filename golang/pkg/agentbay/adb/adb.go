package adb

import (
	"encoding/json"
	"fmt"

	"github.com/alibabacloud-go/tea/tea"
	mcp "github.com/aliyun/wuying-agentbay-sdk/golang/api/client"
)

// Adb handles ADB operations in the AgentBay mobile environment.
type Adb struct {
	Session interface {
		GetAPIKey() string
		GetClient() *mcp.Client
		GetSessionId() string
	}
}

// NewAdb creates a new Adb object.
func NewAdb(session interface {
	GetAPIKey() string
	GetClient() *mcp.Client
	GetSessionId() string
}) *Adb {
	return &Adb{
		Session: session,
	}
}

// Shell executes an ADB shell command in the mobile environment.
func (a *Adb) Shell(command string) (string, error) {
	args := map[string]string{
		"command": command,
	}
	argsJSON, err := json.Marshal(args)
	if err != nil {
		return "", fmt.Errorf("failed to marshal args: %w", err)
	}

	callToolRequest := &mcp.CallMcpToolRequest{
		Authorization: tea.String("Bearer " + a.Session.GetAPIKey()),
		SessionId:     tea.String(a.Session.GetSessionId()),
		Name:          tea.String("shell"),
		Args:          tea.String(string(argsJSON)),
	}
	response, err := a.Session.GetClient().CallMcpTool(callToolRequest)
	if err != nil {
		return "", fmt.Errorf("failed to execute adb shell command: %w", err)
	}

	// Convert interface{} to map
	data, ok := response.Body.Data.(map[string]interface{})
	if !ok {
		return "", fmt.Errorf("invalid response data format")
	}

	// Get content field and parse as array
	contentArray, ok := data["content"].([]interface{})
	if !ok {
		return "", fmt.Errorf("content field not found or not an array")
	}

	var fullText string
	for _, item := range contentArray {
		// Assert each element is map[string]interface{}
		contentItem, ok := item.(map[string]interface{})
		if !ok {
			continue
		}

		// Extract text field
		text, ok := contentItem["text"].(string)
		if !ok {
			continue
		}

		fullText += text + "\n" // Concatenate text content
	}
	return fullText, nil
}
