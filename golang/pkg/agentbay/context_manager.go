package agentbay

import (
	"encoding/json"
	"fmt"
	"time"

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
	Success           bool
	ContextStatusData []ContextStatusData // Parsed context status data
	ErrorMessage      string
}

// ContextSyncResult wraps context sync result and RequestID
type ContextSyncResult struct {
	models.ApiResponse
	Success      bool
	ErrorMessage string
}

// SyncCallback defines the callback function type for async sync operations
type SyncCallback func(success bool)

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
//
// Example:
//
//	client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
//	result, _ := client.Create(nil)
//	defer result.Session.Delete()
//	info, _ := result.Session.Context.Info()
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
	requestInfo := fmt.Sprintf("SessionId=%s", *request.SessionId)
	if request.ContextId != nil {
		requestInfo += fmt.Sprintf(", ContextId=%s", *request.ContextId)
	}
	if request.Path != nil {
		requestInfo += fmt.Sprintf(", Path=%s", *request.Path)
	}
	if request.TaskType != nil {
		requestInfo += fmt.Sprintf(", TaskType=%s", *request.TaskType)
	}
	logAPICall("GetContextInfo", requestInfo)

	response, err := cm.Session.GetClient().GetContextInfo(request)

	// Log API response
	if err != nil {
		logOperationError("GetContextInfo", err.Error(), true)
		return nil, fmt.Errorf("failed to get context info: %w", err)
	}

	// Extract RequestID
	requestID := models.ExtractRequestID(response)

	// Check for API-level errors
	if response != nil && response.Body != nil {
		if response.Body.Success != nil && !*response.Body.Success && response.Body.Code != nil {
			code := tea.StringValue(response.Body.Code)
			message := tea.StringValue(response.Body.Message)
			if message == "" {
				message = "Unknown error"
			}
			respJSON, _ := json.MarshalIndent(response.Body, "", "  ")
			logAPIResponseWithDetails("GetContextInfo", requestID, false, nil, string(respJSON))
			return &ContextInfoResult{
				ApiResponse: models.ApiResponse{
					RequestID: requestID,
				},
				Success:           false,
				ContextStatusData: []ContextStatusData{},
				ErrorMessage:      fmt.Sprintf("[%s] %s", code, message),
			}, nil
		}
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

	keyFields := map[string]interface{}{
		"session_id":    cm.Session.GetSessionId(),
		"context_count": len(contextStatusData),
	}
	if contextId != "" {
		keyFields["context_id"] = contextId
	}
	if path != "" {
		keyFields["path"] = path
	}
	if taskType != "" {
		keyFields["task_type"] = taskType
	}
	if response != nil && response.Body != nil {
		respJSON, _ := json.MarshalIndent(response.Body, "", "  ")
		logAPIResponseWithDetails("GetContextInfo", requestID, true, keyFields, string(respJSON))
	}

	return &ContextInfoResult{
		ApiResponse: models.ApiResponse{
			RequestID: requestID,
		},
		Success:           true,
		ContextStatusData: contextStatusData,
		ErrorMessage:      "",
	}, nil
}

// Sync synchronizes the context for the current session.
func (cm *ContextManager) Sync() (*ContextSyncResult, error) {
	return cm.SyncWithParams("", "", "")
}

// SyncWithCallback synchronizes the context with callback support (dual-mode).
// If callback is provided, it runs in background and calls callback when complete.
// If callback is nil, it waits for completion before returning.
//
// Example (Synchronous mode - waits for completion):
//
//	package main
//	import (
//		"fmt"
//		"os"
//		"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
//	)
//	func main() {
//		client, err := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
//		if err != nil {
//			fmt.Printf("Error: %v\n", err)
//			os.Exit(1)
//		}
//		result, err := client.Create(nil)
//		if err != nil {
//			fmt.Printf("Error: %v\n", err)
//			os.Exit(1)
//		}
//		session := result.Session
//
//		// Get or create a context
//		contextResult, err := client.Context.Get("my-context", true)
//		if err != nil {
//			fmt.Printf("Error: %v\n", err)
//			os.Exit(1)
//		}
//
//		// Synchronous mode: callback is nil, so it waits for completion
//		syncResult, err := session.Context.SyncWithCallback(
//			contextResult.ContextID,
//			"/mnt/persistent",
//			"upload",
//			nil,  // No callback - synchronous mode
//			10,   // maxRetries
//			1000, // retryInterval in milliseconds
//		)
//		if err != nil {
//			fmt.Printf("Error: %v\n", err)
//			os.Exit(1)
//		}
//		fmt.Printf("Sync completed - Success: %v\n", syncResult.Success)
//
//		// Output: No sync tasks found
//		// Output: Sync completed - Success: true
//
//		session.Delete()
//	}
//
// Example (Asynchronous mode - with callback):
//
//	package main
//	import (
//		"fmt"
//		"os"
//		"time"
//		"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
//	)
//	func main() {
//		client, err := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
//		if err != nil {
//			fmt.Printf("Error: %v\n", err)
//			os.Exit(1)
//		}
//		result, err := client.Create(nil)
//		if err != nil {
//			fmt.Printf("Error: %v\n", err)
//			os.Exit(1)
//		}
//		session := result.Session
//
//		// Get or create a context
//		contextResult, err := client.Context.Get("my-context", true)
//		if err != nil {
//			fmt.Printf("Error: %v\n", err)
//			os.Exit(1)
//		}
//
//		// Asynchronous mode: with callback, returns immediately
//		syncResult, err := session.Context.SyncWithCallback(
//			contextResult.ContextID,
//			"/mnt/persistent",
//			"upload",
//			func(success bool) {
//				if success {
//					fmt.Println("Context sync completed successfully")
//				} else {
//					fmt.Println("Context sync failed or timed out")
//				}
//			},
//			150,  // maxRetries
//			1500, // retryInterval in milliseconds
//		)
//		if err != nil {
//			fmt.Printf("Error: %v\n", err)
//			os.Exit(1)
//		}
//		fmt.Printf("Sync triggered - Success: %v\n", syncResult.Success)
//
//		// Wait for callback to complete
//		time.Sleep(5 * time.Second)
//
//		// Output: Sync triggered - Success: true
//		// Output: Context sync completed successfully
//
//		session.Delete()
//	}
func (cm *ContextManager) SyncWithCallback(contextId, path, mode string, callback SyncCallback, maxRetries int, retryInterval int) (*ContextSyncResult, error) {
	// First, trigger the sync operation
	syncResult, err := cm.SyncWithParams(contextId, path, mode)
	if err != nil {
		return nil, err
	}

	// If sync failed, return immediately
	if !syncResult.Success {
		return syncResult, nil
	}

	// If callback is provided, start polling in background (async mode)
	if callback != nil {
		go cm.pollForCompletion(callback, contextId, path, maxRetries, retryInterval)
		return syncResult, nil
	}

	// If no callback, wait for completion (sync mode)
	finalSuccess, err := cm.pollForCompletionSync(contextId, path, maxRetries, retryInterval)
	if err != nil {
		return nil, err
	}

	return &ContextSyncResult{
		ApiResponse: syncResult.ApiResponse,
		Success:     finalSuccess,
	}, nil
}

// SyncWithParams synchronizes the context for the current session with optional parameters.
//
// Example:
//
//	client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
//	result, _ := client.Create(nil)
//	defer result.Session.Delete()
//	session := result.Session
//	_, _ = session.Context.SyncWithCallback(
//		"project-data",
//		"/mnt/shared",
//		"upload",
//		func(success bool, message string) {
//			fmt.Printf("Sync callback -> success: %v message: %s\n", success, message)
//		},
//		20,
//		500,
//	)
func (cm *ContextManager) SyncWithParams(contextId, path, mode string) (*ContextSyncResult, error) {
	// Validate that contextId and path are provided together or both omitted
	hasContextId := contextId != ""
	hasPath := path != ""

	if hasContextId != hasPath {
		return nil, fmt.Errorf(
			"contextId and path must be provided together or both omitted. " +
				"If you want to sync a specific context, both contextId and path are required. " +
				"If you want to sync all contexts, omit both parameters.",
		)
	}

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
	// Set mode, default to "upload" if empty or not provided
	if mode == "" {
		mode = "upload"
	}
	request.Mode = tea.String(mode)

	// Log API request
	requestInfo := fmt.Sprintf("SessionId=%s", *request.SessionId)
	if request.ContextId != nil {
		requestInfo += fmt.Sprintf(", ContextId=%s", *request.ContextId)
	}
	if request.Path != nil {
		requestInfo += fmt.Sprintf(", Path=%s", *request.Path)
	}
	if request.Mode != nil {
		requestInfo += fmt.Sprintf(", Mode=%s", *request.Mode)
	}
	logAPICall("SyncContext", requestInfo)

	response, err := cm.Session.GetClient().SyncContext(request)

	// Log API response
	if err != nil {
		logOperationError("SyncContext", err.Error(), true)
		return nil, fmt.Errorf("failed to sync context: %w", err)
	}

	// Extract RequestID
	requestID := models.ExtractRequestID(response)

	// Check for API-level errors
	if response != nil && response.Body != nil {
		if response.Body.Success != nil && !*response.Body.Success && response.Body.Code != nil {
			code := tea.StringValue(response.Body.Code)
			message := tea.StringValue(response.Body.Message)
			if message == "" {
				message = "Unknown error"
			}
			respJSON, _ := json.MarshalIndent(response.Body, "", "  ")
			logAPIResponseWithDetails("SyncContext", requestID, false, nil, string(respJSON))
			return &ContextSyncResult{
				ApiResponse: models.ApiResponse{
					RequestID: requestID,
				},
				Success:      false,
				ErrorMessage: fmt.Sprintf("[%s] %s", code, message),
			}, nil
		}
	}

	var success bool
	if response.Body != nil {
		success = tea.BoolValue(response.Body.Success)
	}

	keyFields := map[string]interface{}{
		"session_id": cm.Session.GetSessionId(),
		"mode":       mode,
	}
	if contextId != "" {
		keyFields["context_id"] = contextId
	}
	if path != "" {
		keyFields["path"] = path
	}
	if response != nil && response.Body != nil {
		respJSON, _ := json.MarshalIndent(response.Body, "", "  ")
		logAPIResponseWithDetails("SyncContext", requestID, success, keyFields, string(respJSON))
	}

	return &ContextSyncResult{
		ApiResponse: models.ApiResponse{
			RequestID: requestID,
		},
		Success: success,
	}, nil
}

// pollForCompletion polls the info interface to check if sync is completed and calls callback.
func (cm *ContextManager) pollForCompletion(callback SyncCallback, contextId, path string, maxRetries, retryInterval int) {
	for retry := 0; retry < maxRetries; retry++ {
		// Get context status data
		infoResult, err := cm.InfoWithParams(contextId, path, "")
		if err != nil {
			fmt.Printf("Error checking context status on attempt %d: %v\n", retry+1, err)
			time.Sleep(time.Duration(retryInterval) * time.Millisecond)
			continue
		}

		// Check if all sync tasks are completed
		allCompleted := true
		hasFailure := false
		hasSyncTasks := false

		for _, item := range infoResult.ContextStatusData {
			// We only care about sync tasks (upload/download)
			if item.TaskType != "upload" && item.TaskType != "download" {
				continue
			}

			hasSyncTasks = true
			fmt.Printf("Sync task %s status: %s, path: %s\n", item.ContextId, item.Status, item.Path)

			if item.Status != "Success" && item.Status != "Failed" {
				allCompleted = false
				break
			}

			if item.Status == "Failed" {
				hasFailure = true
				fmt.Printf("Sync failed for context %s: %s\n", item.ContextId, item.ErrorMessage)
			}
		}

		if allCompleted || !hasSyncTasks {
			// All tasks completed or no sync tasks found
			if hasFailure {
				fmt.Println("Context sync completed with failures")
				callback(false)
			} else if hasSyncTasks {
				fmt.Println("Context sync completed successfully")
				callback(true)
			} else {
				fmt.Println("No sync tasks found")
				callback(true)
			}
			return // Exit the function immediately after calling callback
		}

		fmt.Printf("Waiting for context sync to complete, attempt %d/%d\n", retry+1, maxRetries)
		time.Sleep(time.Duration(retryInterval) * time.Millisecond)
	}

	// If we've exhausted all retries, call callback with failure
	fmt.Printf("Context sync polling timed out after %d attempts\n", maxRetries)
	callback(false)
}

// pollForCompletionSync is the synchronous version of polling for sync completion.
func (cm *ContextManager) pollForCompletionSync(contextId, path string, maxRetries, retryInterval int) (bool, error) {
	for retry := 0; retry < maxRetries; retry++ {
		// Get context status data
		infoResult, err := cm.InfoWithParams(contextId, path, "")
		if err != nil {
			fmt.Printf("Error checking context status on attempt %d: %v\n", retry+1, err)
			time.Sleep(time.Duration(retryInterval) * time.Millisecond)
			continue
		}

		// Check if all sync tasks are completed
		allCompleted := true
		hasFailure := false
		hasSyncTasks := false

		for _, item := range infoResult.ContextStatusData {
			// We only care about sync tasks (upload/download)
			if item.TaskType != "upload" && item.TaskType != "download" {
				continue
			}

			hasSyncTasks = true
			fmt.Printf("Sync task %s status: %s, path: %s\n", item.ContextId, item.Status, item.Path)

			if item.Status != "Success" && item.Status != "Failed" {
				allCompleted = false
				break
			}

			if item.Status == "Failed" {
				hasFailure = true
				fmt.Printf("Sync failed for context %s: %s\n", item.ContextId, item.ErrorMessage)
			}
		}

		if allCompleted || !hasSyncTasks {
			// All tasks completed or no sync tasks found
			if hasFailure {
				fmt.Println("Context sync completed with failures")
				return false, nil
			} else if hasSyncTasks {
				fmt.Println("Context sync completed successfully")
				return true, nil
			} else {
				fmt.Println("No sync tasks found")
				return true, nil
			}
		}

		fmt.Printf("Waiting for context sync to complete, attempt %d/%d\n", retry+1, maxRetries)
		time.Sleep(time.Duration(retryInterval) * time.Millisecond)
	}

	// If we've exhausted all retries, return failure
	fmt.Printf("Context sync polling timed out after %d attempts\n", maxRetries)
	return false, nil
}
