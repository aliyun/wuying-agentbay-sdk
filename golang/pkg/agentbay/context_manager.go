package agentbay

import (
	"encoding/json"
	"fmt"

	"github.com/alibabacloud-go/tea/tea"
	mcp "github.com/aliyun/wuying-agentbay-sdk/golang/api/client"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/models"
)

// ContextStatusData represents the parsed context status data
type ContextStatusData struct {
	ContextId    string `json:"contextId"`
	Path         string `json:"path"`
	ErrorMessage string `json:"errorMessage"`
	Status       string `json:"status"`
	StartTime    int64  `json:"startTime"`
	FinishTime   int64  `json:"finishTime"`
	TaskType     string `json:"taskType"`
}

// ContextStatusItem represents an item in the context status response
type ContextStatusItem struct {
	Type string `json:"type"`
	Data string `json:"data"`
}

// ContextInfoResult wraps context info result and RequestID
type ContextInfoResult struct {
	models.ApiResponse
	ContextStatusData []ContextStatusData // Parsed context status data
}

// ContextSyncResult wraps context sync result and RequestID
type ContextSyncResult struct {
	models.ApiResponse
	Success bool
}

// ContextManager handles context operations for a specific session.
type ContextManager struct {
	Session interface {
		GetAPIKey() string
		GetClient() *mcp.Client
		GetSessionId() string
	}
}

// NewContextManager creates a new ContextManager object.
func NewContextManager(session interface {
	GetAPIKey() string
	GetClient() *mcp.Client
	GetSessionId() string
}) *ContextManager {
	return &ContextManager{
		Session: session,
	}
}

// Info retrieves context information for the current session.
func (cm *ContextManager) Info() (*ContextInfoResult, error) {
	return cm.InfoWithParams("", "", "")
}

// InfoWithParams retrieves context information for the current session with optional parameters.
func (cm *ContextManager) InfoWithParams(contextId, path, taskType string) (*ContextInfoResult, error) {
	request := &mcp.GetContextInfoRequest{
		Authorization: tea.String("Bearer " + cm.Session.GetAPIKey()),
		SessionId:     tea.String(cm.Session.GetSessionId()),
	}

	// Set optional parameters if provided
	if contextId != "" {
		request.ContextId = tea.String(contextId)
	}
	if path != "" {
		request.Path = tea.String(path)
	}
	if taskType != "" {
		request.TaskType = tea.String(taskType)
	}

	// Log API request
	fmt.Println("API Call: GetContextInfo")
	fmt.Printf("Request: SessionId=%s", *request.SessionId)
	if request.ContextId != nil {
		fmt.Printf(", ContextId=%s", *request.ContextId)
	}
	if request.Path != nil {
		fmt.Printf(", Path=%s", *request.Path)
	}
	if request.TaskType != nil {
		fmt.Printf(", TaskType=%s", *request.TaskType)
	}
	fmt.Println()

	response, err := cm.Session.GetClient().GetContextInfo(request)

	// Log API response
	if err != nil {
		fmt.Println("Error calling GetContextInfo:", err)
		return nil, fmt.Errorf("failed to get context info: %w", err)
	}

	// Extract RequestID
	requestID := models.ExtractRequestID(response)

	if response != nil && response.Body != nil {
		fmt.Println("Response from GetContextInfo:", response.Body)
	}

	// Parse the context status data
	var contextStatusData []ContextStatusData
	if response.Body != nil && response.Body.Data != nil {
		contextStatus := tea.StringValue(response.Body.Data.ContextStatus)
		if contextStatus != "" {
			// First, parse the outer array
			var statusItems []ContextStatusItem
			if err := json.Unmarshal([]byte(contextStatus), &statusItems); err != nil {
				fmt.Println("Error parsing context status:", err)
			} else {
				// Process each item in the array
				for _, item := range statusItems {
					if item.Type == "data" {
						// Parse the inner data string
						var dataItems []ContextStatusData
						if err := json.Unmarshal([]byte(item.Data), &dataItems); err != nil {
							fmt.Println("Error parsing context status data:", err)
						} else {
							contextStatusData = append(contextStatusData, dataItems...)
						}
					}
				}
			}
		}
	}

	return &ContextInfoResult{
		ApiResponse: models.ApiResponse{
			RequestID: requestID,
		},
		ContextStatusData: contextStatusData,
	}, nil
}

// Sync synchronizes the context for the current session.
func (cm *ContextManager) Sync() (*ContextSyncResult, error) {
	return cm.SyncWithParams("", "", "")
}

// SyncWithParams synchronizes the context for the current session with optional parameters.
func (cm *ContextManager) SyncWithParams(contextId, path, mode string) (*ContextSyncResult, error) {
	request := &mcp.SyncContextRequest{
		Authorization: tea.String("Bearer " + cm.Session.GetAPIKey()),
		SessionId:     tea.String(cm.Session.GetSessionId()),
	}

	// Set optional parameters if provided
	if contextId != "" {
		request.ContextId = tea.String(contextId)
	}
	if path != "" {
		request.Path = tea.String(path)
	}
	if mode != "" {
		request.Mode = tea.String(mode)
	}

	// Log API request
	fmt.Println("API Call: SyncContext")
	fmt.Printf("Request: SessionId=%s", *request.SessionId)
	if request.ContextId != nil {
		fmt.Printf(", ContextId=%s", *request.ContextId)
	}
	if request.Path != nil {
		fmt.Printf(", Path=%s", *request.Path)
	}
	if request.Mode != nil {
		fmt.Printf(", Mode=%s", *request.Mode)
	}
	fmt.Println()

	response, err := cm.Session.GetClient().SyncContext(request)

	// Log API response
	if err != nil {
		fmt.Println("Error calling SyncContext:", err)
		return nil, fmt.Errorf("failed to sync context: %w", err)
	}

	// Extract RequestID
	requestID := models.ExtractRequestID(response)

	if response != nil && response.Body != nil {
		fmt.Println("Response from SyncContext:", response.Body)
	}

	var success bool
	if response.Body != nil {
		success = tea.BoolValue(response.Body.Success)
	}

	return &ContextSyncResult{
		ApiResponse: models.ApiResponse{
			RequestID: requestID,
		},
		Success: success,
	}, nil
}
