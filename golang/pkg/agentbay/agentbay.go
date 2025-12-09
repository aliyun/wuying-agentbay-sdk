package agentbay

import (
	"encoding/json"
	"fmt"
	"os"
	"strings"
	"time"

	openapiutil "github.com/alibabacloud-go/darabonba-openapi/v2/utils"
	"github.com/alibabacloud-go/tea/tea"
	mcp "github.com/aliyun/wuying-agentbay-sdk/golang/api/client"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/models"
)

// Option is a function that sets optional parameters for AgentBay client.
type Option func(*AgentBayConfig)

// AgentBayConfig holds optional configuration for the AgentBay client.
type AgentBayConfig struct {
	cfg     *Config
	envFile string
}

// WithConfig returns an Option that sets the configuration for the AgentBay client.
func WithConfig(cfg *Config) Option {
	return func(c *AgentBayConfig) {
		c.cfg = cfg
	}
}

// WithEnvFile returns an Option that sets a custom .env file path for the AgentBay client.
func WithEnvFile(envFile string) Option {
	return func(c *AgentBayConfig) {
		c.envFile = envFile
	}
}

// AgentBay represents the main client for interacting with the AgentBay cloud runtime environment.
type AgentBay struct {
	APIKey         string
	Client         *mcp.Client
	Context        *ContextService
	MobileSimulate *MobileSimulateService
	config         Config
}

// NewAgentBay creates a new AgentBay client.
// If apiKey is empty, it will look for the AGENTBAY_API_KEY environment variable.
func NewAgentBay(apiKey string, opts ...Option) (*AgentBay, error) {
	if apiKey == "" {
		apiKey = os.Getenv("AGENTBAY_API_KEY")
		if apiKey == "" {
			return nil, fmt.Errorf("API key is required. Provide it as a parameter or set the AGENTBAY_API_KEY environment variable")
		}
	}

	// Apply options safely
	config_option := &AgentBayConfig{}
	if opts != nil {
		for _, opt := range opts {
			if opt != nil {
				opt(config_option)
			}
		}
	}

	// Load configuration using loadConfig function
	// This will load from environment variables, .env file (searched upward), or use defaults
	config := loadConfig(config_option.cfg, config_option.envFile)

	// Create API client
	apiConfig := &openapiutil.Config{
		RegionId:       tea.String(""),
		Endpoint:       tea.String(config.Endpoint),
		ReadTimeout:    tea.Int(config.TimeoutMs),
		ConnectTimeout: tea.Int(config.TimeoutMs),
	}

	client, err := mcp.NewClient(apiConfig)
	if err != nil {
		return nil, fmt.Errorf("create openapi client fails: %v", err)
	}

	// Create AgentBay instance
	agentBay := &AgentBay{
		APIKey:  apiKey,
		Client:  client,
		Context: nil, // Will be initialized after creation
		config:  config,
	}

	// Initialize context service
	agentBay.Context = &ContextService{AgentBay: agentBay}

	return agentBay, nil
}

// NewAgentBayWithDefaults creates a new AgentBay client using default configuration.
// This is a convenience function that allows calling NewAgentBay without a config parameter.
func NewAgentBayWithDefaults(apiKey string) (*AgentBay, error) {
	return NewAgentBay(apiKey, nil)
}

// Create creates a new session in the AgentBay cloud environment.
// If params is nil, default parameters will be used.
// Create creates a new AgentBay session with specified configuration.
//
// Parameters:
//   - params: Configuration parameters for the session (optional)
//   - Labels: Key-value pairs for session metadata
//   - ImageId: Custom image ID for the session environment
//   - IsVpc: Whether to create a VPC session
//   - PolicyId: Security policy ID
//   - ExtraConfigs: Additional configuration options
//
// Returns:
//   - *SessionResult: Result containing Session object and request ID
//   - error: Error if the operation fails
//
// Behavior:
//
// - Creates a new isolated cloud runtime environment
// - Waits for session to be ready before returning
// - For VPC sessions, includes VPC-specific configuration
//
// Example:
//
//	client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
//	result, _ := client.Create(nil)
//	defer result.Session.Delete()
func (a *AgentBay) Create(params *CreateSessionParams) (*SessionResult, error) {
	if params == nil {
		params = NewCreateSessionParams()
	}

	// Flag to indicate if we need to wait for mobile simulate
	needsMobileSim := false
	var mobileSimMode models.MobileSimulateMode
	var mobileSimPath string

	// Process mobile simulate configuration
	if params.ExtraConfigs != nil && params.ExtraConfigs.Mobile != nil && params.ExtraConfigs.Mobile.SimulateConfig != nil {
		// Check if simulated context id is provided
		mobileSimContextID := params.ExtraConfigs.Mobile.SimulateConfig.SimulatedContextID
		if mobileSimContextID != "" {
			mobileSimContextSync := &ContextSync{
				ContextID: mobileSimContextID,
				Path:      MobileInfoDefaultPath,
			}
			if params.ContextSync == nil {
				params.ContextSync = []*ContextSync{}
			}
			fmt.Printf("Adding context sync for mobile simulate: %+v\n", mobileSimContextSync)
			params.ContextSync = append(params.ContextSync, mobileSimContextSync)
		}

		// Check if we need to execute mobile simulate command
		if params.ExtraConfigs.Mobile.SimulateConfig.Simulate {
			mobileSimPath = params.ExtraConfigs.Mobile.SimulateConfig.SimulatePath
			if mobileSimPath != "" {
				needsMobileSim = true
				mobileSimMode = params.ExtraConfigs.Mobile.SimulateConfig.SimulateMode
			}
		}
	}

	createSessionRequest := &mcp.CreateMcpSessionRequest{
		Authorization: tea.String("Bearer " + a.APIKey),
	}

	// Add SDK stats for tracking
	isRelease := isReleaseVersion()
	framework := ""
	if params != nil {
		framework = params.Framework
	}
	sdkStatsJSON := fmt.Sprintf(`{"source":"sdk","sdk_language":"golang","sdk_version":"%s","is_release":%t,"framework":"%s"}`, Version, isRelease, framework)
	createSessionRequest.SdkStats = tea.String(sdkStatsJSON)

	// Add LoginRegionId if region_id is set
	if a.config.RegionID != "" {
		createSessionRequest.LoginRegionId = tea.String(a.config.RegionID)
	}

	// Add image_id if provided
	if params.ImageId != "" {
		createSessionRequest.ImageId = tea.String(params.ImageId)
	}

	// Add VPC resource if specified
	createSessionRequest.VpcResource = tea.Bool(params.IsVpc)

	// Add PolicyId if provided
	if params.PolicyId != "" {
		createSessionRequest.McpPolicyId = tea.String(params.PolicyId)
	}

	// Add labels if provided
	if len(params.Labels) > 0 {
		labelsJSON, err := params.GetLabelsJSON()
		if err != nil {
			return nil, fmt.Errorf("failed to marshal labels to JSON: %v", err)
		}
		createSessionRequest.Labels = tea.String(labelsJSON)
	}

	// Add extra configs if provided
	if params.ExtraConfigs != nil {
		extraConfigsJSON, err := params.GetExtraConfigsJSON()
		if err != nil {
			return nil, fmt.Errorf("failed to marshal extra configs to JSON: %v", err)
		}
		if extraConfigsJSON != "" {
			createSessionRequest.ExtraConfigs = tea.String(extraConfigsJSON)
		}
	}

	// Flag to indicate if we need to wait for context synchronization
	needsContextSync := false

	// Add context sync configurations if provided
	var persistenceDataList []*mcp.CreateMcpSessionRequestPersistenceDataList

	if len(params.ContextSync) > 0 {
		for _, contextSync := range params.ContextSync {
			persistenceItem := &mcp.CreateMcpSessionRequestPersistenceDataList{
				ContextId: tea.String(contextSync.ContextID),
				Path:      tea.String(contextSync.Path),
			}

			// Convert policy to JSON string if provided
			if contextSync.Policy != nil {
				policyJSON, err := json.Marshal(contextSync.Policy)
				if err != nil {
					return nil, fmt.Errorf("failed to marshal context sync policy to JSON: %v", err)
				}
				persistenceItem.Policy = tea.String(string(policyJSON))
			}

			persistenceDataList = append(persistenceDataList, persistenceItem)
		}
	}

	// Add mobile simulate context sync if needed
	if params.ExtraConfigs != nil && params.ExtraConfigs.Mobile != nil &&
		params.ExtraConfigs.Mobile.SimulateConfig != nil &&
		params.ExtraConfigs.Mobile.SimulateConfig.Simulate &&
		params.ExtraConfigs.Mobile.SimulateConfig.SimulatedContextID != "" {

		simContextID := params.ExtraConfigs.Mobile.SimulateConfig.SimulatedContextID
		fmt.Printf("ℹ️  Adding context sync for mobile simulate: &{ContextID:%s Path:%s Policy:<nil>}\n", simContextID, MobileInfoDefaultPath)

		// Check if already exists in persistenceDataList
		exists := false
		for _, item := range persistenceDataList {
			if tea.StringValue(item.ContextId) == simContextID {
				exists = true
				break
			}
		}

		if !exists {
			mobilePersistence := &mcp.CreateMcpSessionRequestPersistenceDataList{
				ContextId: tea.String(simContextID),
				Path:      tea.String(MobileInfoDefaultPath),
			}
			persistenceDataList = append(persistenceDataList, mobilePersistence)
		}
	}

	// Add browser recording persistence if enabled
	var recordContextID string
	if params.EnableBrowserReplay {
		// Generate random context name for browser recording
		recordContextName := fmt.Sprintf("browser-record-%d", time.Now().UnixNano())
		recordResult, err := a.Context.Get(recordContextName, true)
		if err == nil && recordResult.Success {
			recordContextID = recordResult.ContextID
			// Create browser recording persistence configuration
			recordPersistence := &mcp.CreateMcpSessionRequestPersistenceDataList{
				ContextId: tea.String(recordContextID),
				Path:      tea.String(BrowserRecordPath),
			}
			persistenceDataList = append(persistenceDataList, recordPersistence)
		}
	}

	if len(persistenceDataList) > 0 {
		createSessionRequest.PersistenceDataList = persistenceDataList
		needsContextSync = true
	}

	// Log API request with all set parameters
	requestParams := fmt.Sprintf("ImageId=%s, IsVpc=%t",
		tea.StringValue(createSessionRequest.ImageId),
		tea.BoolValue(createSessionRequest.VpcResource))

	// Add PolicyId if set
	if createSessionRequest.McpPolicyId != nil && *createSessionRequest.McpPolicyId != "" {
		requestParams += fmt.Sprintf(", PolicyId=%s", *createSessionRequest.McpPolicyId)
	}

	// Add Labels if set
	if createSessionRequest.Labels != nil && *createSessionRequest.Labels != "" {
		labelsStr := *createSessionRequest.Labels
		// Truncate long labels for readability
		if len(labelsStr) > 100 {
			labelsStr = labelsStr[:97] + "..."
		}
		requestParams += fmt.Sprintf(", Labels=%s", labelsStr)
	}

	// Add PersistenceDataList count if set
	if len(createSessionRequest.PersistenceDataList) > 0 {
		requestParams += fmt.Sprintf(", PersistenceDataList=%d items", len(createSessionRequest.PersistenceDataList))
	}

	// Add ExtraConfigs if set
	if createSessionRequest.ExtraConfigs != nil && *createSessionRequest.ExtraConfigs != "" {
		extraConfigsStr := *createSessionRequest.ExtraConfigs
		// Truncate long extra configs for readability
		if len(extraConfigsStr) > 100 {
			extraConfigsStr = extraConfigsStr[:97] + "..."
		}
		requestParams += fmt.Sprintf(", ExtraConfigs=%s", extraConfigsStr)
	}

	logAPICall("CreateMcpSession", requestParams)

	response, err := a.Client.CreateMcpSession(createSessionRequest)

	// Extract RequestID
	requestID := models.ExtractRequestID(response)

	// Log API response
	if err != nil {
		logOperationError("CreateMcpSession", err.Error(), true)
		return nil, err
	}

	// Check if the session creation was successful
	if response == nil || response.Body == nil || response.Body.Data == nil {
		return nil, fmt.Errorf("invalid response from CreateMcpSession")
	}

	// Check if there's an error message in the response
	if response.Body.Data.Success != nil && !*response.Body.Data.Success {
		errMsg := "session creation failed"
		if response.Body.Data.ErrMsg != nil {
			errMsg = *response.Body.Data.ErrMsg
		}
		responseJSON, _ := json.MarshalIndent(response.Body, "", "  ")
		logAPIResponseWithDetails("CreateMcpSession", requestID, false, nil, string(responseJSON))
		return nil, fmt.Errorf("%s", errMsg)
	}

	// Check if SessionId is present
	if response.Body.Data.SessionId == nil {
		return nil, fmt.Errorf("no session ID returned from CreateMcpSession")
	}

	// Create a new session object
	session := NewSession(a, *response.Body.Data.SessionId)
	session.ImageId = params.ImageId

	// Set VPC-related information from response
	session.IsVpcEnabled = params.IsVpc
	if response.Body.Data.NetworkInterfaceIp != nil {
		session.NetworkInterfaceIP = *response.Body.Data.NetworkInterfaceIp
	}
	if response.Body.Data.HttpPort != nil {
		session.HttpPortNumber = *response.Body.Data.HttpPort
	}
	if response.Body.Data.Token != nil {
		session.Token = *response.Body.Data.Token
	}

	// Set ResourceUrl
	if response.Body.Data.ResourceUrl != nil {
		session.ResourceUrl = *response.Body.Data.ResourceUrl
	}

	// Set browser recording state and context ID
	session.EnableBrowserReplay = params.EnableBrowserReplay
	session.RecordContextID = recordContextID

	// Log successful session creation
	keyFields := map[string]interface{}{
		"session_id":   session.SessionID,
		"resource_url": session.ResourceUrl,
		"is_vpc":       params.IsVpc,
	}
	responseJSON, _ := json.MarshalIndent(response.Body, "", "  ")
	logAPIResponseWithDetails("CreateMcpSession", requestID, true, keyFields, string(responseJSON))

	// Update browser replay context if enabled
	if params.EnableBrowserReplay && recordContextID != "" {
		a.updateBrowserReplayContext(response.Body.Data, recordContextID)
	}

	// Apply mobile configuration if provided
	if params.ExtraConfigs != nil && params.ExtraConfigs.Mobile != nil {
		if err := session.Mobile.Configure(params.ExtraConfigs.Mobile); err != nil {
			logOperationError("ApplyMobileConfiguration", err.Error(), false)
		}
	}

	// For VPC sessions, automatically fetch MCP tools information
	if params.IsVpc {
		toolsResult, err := session.ListMcpTools()
		if err != nil {
			logOperationError("FetchMCPTools", err.Error(), false)
		} else if len(toolsResult.Tools) > 0 {
			fmt.Printf("✅ Successfully fetched %d MCP tools for VPC session (RequestID: %s)\n",
				len(toolsResult.Tools), toolsResult.RequestID)
		}
	}

	// If we have persistence data, wait for context synchronization
	if needsContextSync {
		fmt.Println("Waiting for context synchronization to complete...")

		// Wait for context synchronization to complete
		const maxRetries = 150                        // Maximum number of retries
		const retryInterval = 1500 * time.Millisecond // 1.5 seconds between retries

		for retry := 0; retry < maxRetries; retry++ {
			// Get context status data
			infoResult, err := session.Context.Info()
			if err != nil {
				fmt.Printf("Error getting context info on attempt %d: %v\n", retry+1, err)
				time.Sleep(retryInterval)
				continue
			}

			// Check if all context items have status "Success" or "Failed"
			allCompleted := true
			hasFailure := false

			for _, item := range infoResult.ContextStatusData {
				fmt.Printf("Context %s status: %s, path: %s\n", item.ContextId, item.Status, item.Path)

				if item.Status != "Success" && item.Status != "Failed" {
					allCompleted = false
					break
				}

				if item.Status == "Failed" {
					hasFailure = true
					fmt.Printf("Context synchronization failed for %s: %s\n", item.ContextId, item.ErrorMessage)
				}
			}

			if allCompleted || len(infoResult.ContextStatusData) == 0 {
				if hasFailure {
					fmt.Println("Context synchronization completed with failures")
				} else {
					fmt.Println("Context synchronization completed successfully")
				}
				break
			}

			fmt.Printf("Waiting for context synchronization, attempt %d/%d\n", retry+1, maxRetries)
			time.Sleep(retryInterval)
		}
	}

	// If we need to do mobile simulate by command, wait for it
	if needsMobileSim && mobileSimPath != "" {
		a.waitForMobileSimulate(session, mobileSimPath, mobileSimMode)
	}

	// Return result with RequestID
	return &SessionResult{
		ApiResponse: models.ApiResponse{
			RequestID: requestID,
		},
		Session: session,
		Success: true,
	}, nil
}

// waitForMobileSimulate waits for mobile simulate command to complete.
func (a *AgentBay) waitForMobileSimulate(session *Session, mobileSimPath string, mobileSimMode models.MobileSimulateMode) error {
	fmt.Println("⏳ Mobile simulate: Waiting for completion")

	if session.Mobile == nil {
		fmt.Println("Mobile module not found in session, skipping mobile simulate")
		return nil
	}
	if session.Command == nil {
		fmt.Println("Command module not found in session, skipping mobile simulate")
		return nil
	}
	if mobileSimPath == "" {
		fmt.Println("Mobile simulate path is empty, skipping mobile simulate")
		return nil
	}

	// Run mobile simulate command
	startTime := time.Now()
	devInfoFilePath := mobileSimPath + "/" + MobileInfoFileName
	wyaApplyOption := ""

	switch mobileSimMode {
	case models.MobileSimulateModePropertiesOnly, "":
		wyaApplyOption = ""
	case models.MobileSimulateModeSensorsOnly:
		wyaApplyOption = " -sensors"
	case models.MobileSimulateModePackagesOnly:
		wyaApplyOption = " -packages"
	case models.MobileSimulateModeServicesOnly:
		wyaApplyOption = " -services"
	case models.MobileSimulateModeAll:
		wyaApplyOption = " -all"
	}

	command := fmt.Sprintf("chmod -R a+rwx %s; wya apply%s %s", mobileSimPath, wyaApplyOption, devInfoFilePath)
	fmt.Printf("⏳ Waiting for mobile simulate completion, command: %s\n", command)

	cmdResult, err := session.Command.ExecuteCommand(command)
	if err != nil {
		fmt.Printf("Failed to execute mobile simulate command: %v\n", err)
		return nil
	}

	duration := time.Since(startTime)
	fmt.Printf("✅ Mobile simulate completed with mode: %s, duration: %.2f seconds\n", mobileSimMode, duration.Seconds())
	fmt.Printf("   Output: %s\n", cmdResult.Output)

	return nil
}

// ListSessionParams contains parameters for listing sessions
type ListSessionParams struct {
	MaxResults int32             // Number of results per page
	NextToken  string            // Token for the next page
	Labels     map[string]string // Labels to filter by
}

// NewListSessionParams creates a new ListSessionParams with default values
func NewListSessionParams() *ListSessionParams {
	return &ListSessionParams{
		MaxResults: 10, // Default page size
		NextToken:  "",
		Labels:     make(map[string]string),
	}
}

// List returns paginated list of session IDs filtered by labels.
//
// Parameters:
//   - labels: Optional labels to filter sessions (can be nil for no filtering)
//   - page: Optional page number for pagination (starting from 1, nil or 0 for first page)
//   - limit: Optional maximum number of items per page (nil or 0 uses default of 10)
//
// Returns:
//   - *SessionListResult: Paginated list of session IDs that match the labels
//   - error: An error if the operation fails
//
// Example:
//
//	client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
//	result, _ := client.List(nil, nil, nil)
func (a *AgentBay) List(labels map[string]string, page *int, limit *int32) (*SessionListResult, error) {
	// Set default values
	if labels == nil {
		labels = make(map[string]string)
	}
	actualLimit := int32(10)
	if limit != nil && *limit > 0 {
		actualLimit = *limit
	}

	// Validate page number
	if page != nil && *page < 1 {
		return &SessionListResult{
			ApiResponse: models.ApiResponse{
				RequestID: "",
			},
			SessionIds: []string{},
			NextToken:  "",
			MaxResults: actualLimit,
			TotalCount: 0,
		}, fmt.Errorf("cannot reach page %d: Page number must be >= 1", *page)
	}

	// Convert labels to JSON
	labelsJSON, err := json.Marshal(labels)
	if err != nil {
		return nil, fmt.Errorf("failed to marshal labels to JSON: %v", err)
	}

	// Calculate next_token based on page number
	nextToken := ""
	if page != nil && *page > 1 {
		// We need to fetch pages 1 through page-1 to get the next_token
		currentPage := 1
		for currentPage < *page {
			// Make API call to get next_token
			listSessionRequest := &mcp.ListSessionRequest{
				Authorization: tea.String("Bearer " + a.APIKey),
				Labels:        tea.String(string(labelsJSON)),
				MaxResults:    tea.Int32(actualLimit),
			}
			if nextToken != "" {
				listSessionRequest.NextToken = tea.String(nextToken)
			}

			response, err := a.Client.ListSession(listSessionRequest)
			if err != nil {
				return &SessionListResult{
					ApiResponse: models.ApiResponse{
						RequestID: models.ExtractRequestID(response),
					},
					SessionIds: []string{},
					NextToken:  "",
					MaxResults: actualLimit,
					TotalCount: 0,
				}, fmt.Errorf("cannot reach page %d: %v", *page, err)
			}

			if response.Body == nil || response.Body.Success == nil || !*response.Body.Success {
				errorMsg := "Unknown error"
				if response.Body != nil && response.Body.Message != nil {
					errorMsg = *response.Body.Message
				} else if response.Body != nil && response.Body.Code != nil {
					errorMsg = *response.Body.Code
				}
				return &SessionListResult{
					ApiResponse: models.ApiResponse{
						RequestID: models.ExtractRequestID(response),
					},
					SessionIds: []string{},
					NextToken:  "",
					MaxResults: actualLimit,
					TotalCount: 0,
				}, fmt.Errorf("cannot reach page %d: %s", *page, errorMsg)
			}

			if response.Body.NextToken == nil || *response.Body.NextToken == "" {
				// No more pages available
				totalCount := int32(0)
				if response.Body.TotalCount != nil {
					totalCount = *response.Body.TotalCount
				}
				return &SessionListResult{
					ApiResponse: models.ApiResponse{
						RequestID: models.ExtractRequestID(response),
					},
					SessionIds: []string{},
					NextToken:  "",
					MaxResults: actualLimit,
					TotalCount: totalCount,
				}, fmt.Errorf("cannot reach page %d: No more pages available", *page)
			}
			nextToken = *response.Body.NextToken
			currentPage++
		}
	}

	// Make the actual request for the desired page
	listSessionRequest := &mcp.ListSessionRequest{
		Authorization: tea.String("Bearer " + a.APIKey),
		Labels:        tea.String(string(labelsJSON)),
		MaxResults:    tea.Int32(actualLimit),
	}
	if nextToken != "" {
		listSessionRequest.NextToken = tea.String(nextToken)
	}

	// Log API request
	requestParams := fmt.Sprintf("Labels=%s, MaxResults=%d", *listSessionRequest.Labels, *listSessionRequest.MaxResults)
	if listSessionRequest.NextToken != nil {
		requestParams += fmt.Sprintf(", NextToken=%s", *listSessionRequest.NextToken)
	}
	logAPICall("ListSession", requestParams)

	response, err := a.Client.ListSession(listSessionRequest)

	// Log API response
	if err != nil {
		logOperationError("ListSession", err.Error(), true)
		return nil, err
	}

	// Extract RequestID
	requestID := models.ExtractRequestID(response)

	if response != nil && response.Body != nil {
		fmt.Println("Response from ListSession:", response.Body)
	}

	// Check for errors in the response
	if response.Body == nil || response.Body.Success == nil || !*response.Body.Success {
		errorMsg := "Unknown error"
		if response.Body != nil && response.Body.Message != nil {
			errorMsg = *response.Body.Message
		} else if response.Body != nil && response.Body.Code != nil {
			errorMsg = *response.Body.Code
		}
		logOperationError("ListSession", fmt.Sprintf("failed to list sessions: %s", errorMsg), false)
		return &SessionListResult{
			ApiResponse: models.ApiResponse{
				RequestID: requestID,
			},
			SessionIds: []string{},
			NextToken:  "",
			MaxResults: actualLimit,
			TotalCount: 0,
		}, fmt.Errorf("failed to list sessions: %s", errorMsg)
	}

	var sessionIds []string
	var nextTokenResult string
	var maxResults int32 = actualLimit
	var totalCount int32

	if response.Body != nil {
		// Extract pagination information
		if response.Body.NextToken != nil {
			nextTokenResult = *response.Body.NextToken
		}
		if response.Body.MaxResults != nil {
			maxResults = *response.Body.MaxResults
		}
		if response.Body.TotalCount != nil {
			totalCount = *response.Body.TotalCount
		}

		// Extract session data
		if response.Body.Data != nil {
			for _, sessionData := range response.Body.Data {
				if sessionData.SessionId != nil {
					sessionIds = append(sessionIds, *sessionData.SessionId)
				}
			}
		}
	}

	// Log successful response
	keyFields := map[string]interface{}{
		"session_count": len(sessionIds),
		"total_count":   totalCount,
		"max_results":   maxResults,
		"has_next_page": nextTokenResult != "",
	}
	if nextTokenResult != "" {
		keyFields["next_token"] = nextTokenResult
	}
	responseJSON, _ := json.MarshalIndent(response.Body, "", "  ")
	logAPIResponseWithDetails("ListSession", requestID, true, keyFields, string(responseJSON))

	return &SessionListResult{
		ApiResponse: models.ApiResponse{
			RequestID: requestID,
		},
		SessionIds: sessionIds,
		NextToken:  nextTokenResult,
		MaxResults: maxResults,
		TotalCount: totalCount,
	}, nil
}

// Delete deletes a session from the AgentBay cloud environment.
//
// Parameters:
//   - session: The session to delete
//   - syncContext: Optional boolean to synchronize context data before deletion.
//     If true, uploads all context data to OSS. Defaults to false.
//
// Returns:
//   - *DeleteResult: Result containing success status and request ID
//   - error: Error if the operation fails
//
// Behavior:
//
// - If syncContext is true: Uploads all context data to OSS before deletion
// - If syncContext is false: Deletes immediately without sync
// - Continues with deletion even if context sync fails
// - Releases all associated resources
//
// Example:
//
//	client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
//	result, _ := client.Create(nil)
//	client.Delete(result.Session, true)
func (a *AgentBay) Delete(session *Session, syncContext ...bool) (*DeleteResult, error) {
	result, err := session.Delete(syncContext...)
	return result, err
}

// GetSessionResult represents the result of GetSession operation
type GetSessionResult struct {
	models.ApiResponse
	HttpStatusCode int32
	Code           string
	Success        bool
	Data           *GetSessionData
	ErrorMessage   string
}

// ContextInfo represents a context in the GetSession response
type ContextInfo struct {
	Name string
	ID   string
}

// GetSessionData represents the data returned by GetSession API
type GetSessionData struct {
	AppInstanceID      string
	ResourceID         string
	SessionID          string
	Success            bool
	HttpPort           string
	NetworkInterfaceIP string
	Token              string
	VpcResource        bool
	ResourceUrl        string
	Status             string
	Contexts           []ContextInfo
}

// GetSession retrieves session information by session ID
func (a *AgentBay) GetSession(sessionID string) (*GetSessionResult, error) {
	getSessionRequest := &mcp.GetSessionRequest{
		Authorization: tea.String("Bearer " + a.APIKey),
		SessionId:     tea.String(sessionID),
	}

	// Log API request
	requestParams := fmt.Sprintf("SessionId=%s", *getSessionRequest.SessionId)
	logAPICall("GetSession", requestParams)

	response, err := a.Client.GetSession(getSessionRequest)

	// Log API response
	if err != nil {
		// Check if this is an expected business error (e.g., session not found)
		errorStr := err.Error()
		if strings.Contains(errorStr, "InvalidMcpSession.NotFound") || strings.Contains(errorStr, "NotFound") {
			// This is an expected error - session doesn't exist
			// Use info level logging without stack trace, but with red color for visibility
			logInfoWithColor(fmt.Sprintf("Session not found: %s", sessionID))
			LogDebug(fmt.Sprintf("GetSession error details: %s", errorStr))
			return &GetSessionResult{
				ApiResponse: models.ApiResponse{
					RequestID: "",
				},
				HttpStatusCode: 400,
				Code:           "InvalidMcpSession.NotFound",
				Success:        false,
				ErrorMessage:   fmt.Sprintf("Session %s not found", sessionID),
			}, nil
		} else {
			// This is an unexpected error - log with stack trace
			logOperationError("GetSession", err.Error(), true)
			return nil, err
		}
	}

	// Extract RequestID
	requestID := models.ExtractRequestID(response)

	result := &GetSessionResult{
		ApiResponse: models.ApiResponse{
			RequestID: requestID,
		},
	}

	if response != nil && response.Body != nil {
		if response.Body.HttpStatusCode != nil {
			result.HttpStatusCode = *response.Body.HttpStatusCode
		}
		if response.Body.Code != nil {
			result.Code = *response.Body.Code
		}
		if response.Body.Success != nil {
			result.Success = *response.Body.Success
		}

		// Check for API-level errors
		if !result.Success && response.Body.Code != nil {
			code := tea.StringValue(response.Body.Code)
			message := tea.StringValue(response.Body.Message)
			if message == "" {
				message = "Unknown error"
			}
			result.ErrorMessage = fmt.Sprintf("[%s] %s", code, message)
			logOperationError("GetSession", result.ErrorMessage, false)
			return result, nil
		}

		if response.Body.Data != nil {
			data := &GetSessionData{}
			if response.Body.Data.GetAppInstanceId() != nil {
				data.AppInstanceID = *response.Body.Data.GetAppInstanceId()
			}
			if response.Body.Data.GetResourceId() != nil {
				data.ResourceID = *response.Body.Data.GetResourceId()
			}
			if response.Body.Data.GetSessionId() != nil {
				data.SessionID = *response.Body.Data.GetSessionId()
			}
			if response.Body.Data.GetSuccess() != nil {
				data.Success = *response.Body.Data.GetSuccess()
			}
			if response.Body.Data.GetHttpPort() != nil {
				data.HttpPort = *response.Body.Data.GetHttpPort()
			}
			if response.Body.Data.GetNetworkInterfaceIp() != nil {
				data.NetworkInterfaceIP = *response.Body.Data.GetNetworkInterfaceIp()
			}
			if response.Body.Data.GetToken() != nil {
				data.Token = *response.Body.Data.GetToken()
			}
			if response.Body.Data.GetVpcResource() != nil {
				data.VpcResource = *response.Body.Data.GetVpcResource()
			}
			if response.Body.Data.GetResourceUrl() != nil {
				data.ResourceUrl = *response.Body.Data.GetResourceUrl()
			}
			if response.Body.Data.GetStatus() != nil {
				data.Status = *response.Body.Data.GetStatus()
			}
			// Extract contexts list from response
			if response.Body.Data.GetContexts() != nil {
				contexts := []ContextInfo{}
				for _, ctx := range response.Body.Data.GetContexts() {
					if ctx != nil {
						contextInfo := ContextInfo{}
						if ctx.GetName() != nil {
							contextInfo.Name = *ctx.GetName()
						}
						if ctx.GetId() != nil {
							contextInfo.ID = *ctx.GetId()
						}
						if contextInfo.Name != "" || contextInfo.ID != "" {
							contexts = append(contexts, contextInfo)
						}
					}
				}
				data.Contexts = contexts
			}
			result.Data = data

			// Log successful response
			keyFields := map[string]interface{}{
				"session_id":   data.SessionID,
				"resource_url": data.ResourceUrl,
				"resource_id":  data.ResourceID,
				"app_instance": data.AppInstanceID,
				"vpc_resource": data.VpcResource,
			}
			if data.HttpPort != "" {
				keyFields["http_port"] = data.HttpPort
			}
			if data.NetworkInterfaceIP != "" {
				keyFields["network_interface_ip"] = data.NetworkInterfaceIP
			}
			responseJSON, _ := json.MarshalIndent(response.Body, "", "  ")
			logAPIResponseWithDetails("GetSession", requestID, true, keyFields, string(responseJSON))
		}

		result.ErrorMessage = ""
	}

	return result, nil
}

// Get retrieves a session by its ID.
// This method calls the GetSession API and returns a SessionResult containing the Session object and request ID.
//
// Parameters:
//   - sessionID: The ID of the session to retrieve
//
// Returns:
//   - *SessionResult: Result containing the Session instance, request ID, and success status
//   - error: An error if the operation fails
//
// Example:
//
//	client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
//	createResult, _ := client.Create(nil)
//	sessionID := createResult.Session.SessionID
//	result, _ := client.Get(sessionID)
//	defer result.Session.Delete()
func (a *AgentBay) Get(sessionID string) (*SessionResult, error) {
	if sessionID == "" {
		logOperationError("Get", "session_id is required", false)
		return &SessionResult{
			ApiResponse: models.ApiResponse{
				RequestID: "",
			},
			Success:      false,
			ErrorMessage: "session_id is required",
		}, nil
	}

	// Call GetSession API
	getResult, err := a.GetSession(sessionID)
	if err != nil {
		errorMsg := fmt.Sprintf("failed to get session %s: %v", sessionID, err)
		logOperationError("Get", errorMsg, true)
		return &SessionResult{
			ApiResponse: models.ApiResponse{
				RequestID: "",
			},
			Success:      false,
			ErrorMessage: errorMsg,
		}, nil
	}

	// Check if the API call was successful
	if !getResult.Success {
		errorMsg := "unknown error"
		if getResult.Data != nil && !getResult.Data.Success {
			errorMsg = "Session not found"
		}
		fullErrorMsg := fmt.Sprintf("failed to get session %s: %s", sessionID, errorMsg)
		logOperationError("Get", fullErrorMsg, false)
		return &SessionResult{
			ApiResponse: models.ApiResponse{
				RequestID: getResult.RequestID,
			},
			Success:      false,
			ErrorMessage: fullErrorMsg,
		}, nil
	}

	// Create the Session object
	session := NewSession(a, sessionID)

	// Set VPC-related information and ResourceUrl from GetSession response
	if getResult.Data != nil {
		session.IsVpcEnabled = getResult.Data.VpcResource
		session.NetworkInterfaceIP = getResult.Data.NetworkInterfaceIP
		session.HttpPortNumber = getResult.Data.HttpPort
		session.Token = getResult.Data.Token
		session.ResourceUrl = getResult.Data.ResourceUrl
	}

	// Extract file transfer context ID from contexts list
	if getResult.Data != nil && len(getResult.Data.Contexts) > 0 {
		contexts := getResult.Data.Contexts
		// Filter contexts with 'file-transfer-context-' prefix
		fileTransferContexts := []ContextInfo{}
		for _, ctx := range contexts {
			if strings.HasPrefix(ctx.Name, "file-transfer-context-") {
				fileTransferContexts = append(fileTransferContexts, ctx)
			}
		}

		if len(fileTransferContexts) == 0 {
			// No file transfer context found
			availableContexts := []string{}
			for _, ctx := range contexts {
				if ctx.Name != "" {
					availableContexts = append(availableContexts, ctx.Name)
				}
			}
			fmt.Printf("⚠️  No file-transfer-context- found in contexts list for session %s. Available contexts: %v\n",
				sessionID, availableContexts)
			session.FileTransferContextID = ""
		} else if len(fileTransferContexts) == 1 {
			// Exactly one file transfer context found
			contextID := fileTransferContexts[0].ID
			if contextID != "" {
				session.FileTransferContextID = contextID
				fmt.Printf("📁 Found file transfer context for recovered session: %s\n", contextID)
			} else {
				fmt.Printf("⚠️  File transfer context found but missing 'id' field: %+v\n", fileTransferContexts[0])
				session.FileTransferContextID = ""
			}
		} else {
			// Multiple file transfer contexts found
			contextNames := []string{}
			for _, ctx := range fileTransferContexts {
				if ctx.Name != "" {
					contextNames = append(contextNames, ctx.Name)
				}
			}
			fmt.Printf("⚠️  Multiple file-transfer-context- found in contexts list for session %s. Found %d contexts: %v. Not setting FileTransferContextID.\n",
				sessionID, len(fileTransferContexts), contextNames)
			session.FileTransferContextID = ""
		}
	} else {
		// No contexts list in response
		fmt.Printf("⚠️  No contexts list found in GetSession response for session %s. FileTransferContextID will remain empty.\n",
			sessionID)
		session.FileTransferContextID = ""
	}

	// Log successful retrieval
	keyFields := map[string]interface{}{
		"session_id":   sessionID,
		"resource_url": session.ResourceUrl,
	}
	if getResult.Data != nil {
		keyFields["vpc_enabled"] = getResult.Data.VpcResource
		if getResult.Data.ResourceID != "" {
			keyFields["resource_id"] = getResult.Data.ResourceID
		}
	}
	logAPIResponseWithDetails("Get", getResult.RequestID, true, keyFields, "")

	return &SessionResult{
		ApiResponse: models.ApiResponse{
			RequestID: getResult.RequestID,
		},
		Success: true,
		Session: session,
	}, nil
}

// Pause synchronously pauses a session, putting it into a dormant state to reduce resource usage and costs.
// Pause puts the session into a PAUSED state where computational resources are significantly reduced.
// The session state is preserved and can be resumed later to continue work.
//
// Parameters:
//   - session: The session to pause.
//   - timeout: Timeout in seconds to wait for the session to pause. Defaults to 600 seconds.
//   - pollInterval: Interval in seconds between status polls. Defaults to 2.0 seconds.
//
// Returns:
//   - *models.SessionPauseResult: Result containing success status, request ID, and error message if any.
//   - error: Error if the operation fails at the transport level
//
// Behavior:
//
// - Delegates to session's Pause method for actual implementation
// - Returns detailed result with success status and request tracking
//
// Exceptions:
//
// - Returns error result (not Go error) for API-level errors like invalid session ID
// - Returns error result for timeout conditions
// - Returns Go error for transport-level failures
//
// Example:
//
//	client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"))
//	result, _ := client.Create(nil)
//	defer result.Session.Delete()
//	pauseResult, _ := client.Pause(result.Session, 300, 2.0)
//	client.Resume(result.Session, 300, 2.0)
func (ab *AgentBay) Pause(session *Session, timeout int, pollInterval float64) (*models.SessionPauseResult, error) {
	// Use default values if not provided
	if timeout <= 0 {
		timeout = 600
	}
	if pollInterval <= 0 {
		pollInterval = 2.0
	}

	// Call session's Pause method with provided parameters
	return session.Pause(timeout, pollInterval)
}

// Resume synchronously resumes a session from a paused state to continue work.
// Resume restores the session from PAUSED state back to RUNNING state.
// All previous session state and data are preserved during resume operation.
//
// Parameters:
//   - session: The session to resume.
//   - timeout: Timeout in seconds to wait for the session to resume. Defaults to 600 seconds.
//   - pollInterval: Interval in seconds between status polls. Defaults to 2.0 seconds.
//
// Returns:
//   - *models.SessionResumeResult: Result containing success status, request ID, and error message if any.
//   - error: Error if the operation fails at the transport level
//
// Behavior:
//
// - Delegates to session's Resume method for actual implementation
// - Returns detailed result with success status and request tracking
//
// Exceptions:
//
// - Returns error result (not Go error) for API-level errors like invalid session ID
// - Returns error result for timeout conditions
// - Returns Go error for transport-level failures
//
// Example:
//
//	client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"))
//	result, _ := client.Create(nil)
//	defer result.Session.Delete()
//	client.Pause(result.Session, 300, 2.0)
//	resumeResult, _ := client.Resume(result.Session, 300, 2.0)
func (ab *AgentBay) Resume(session *Session, timeout int, pollInterval float64) (*models.SessionResumeResult, error) {
	// Use default values if not provided
	if timeout <= 0 {
		timeout = 600
	}
	if pollInterval <= 0 {
		pollInterval = 2.0
	}

	// Call session's Resume method with provided parameters
	return session.Resume(timeout, pollInterval)
}

// updateBrowserReplayContext updates browser replay context with AppInstanceId from response data.
// This method updates the context name to include the AppInstanceId for better tracking.
func (a *AgentBay) updateBrowserReplayContext(responseData *mcp.CreateMcpSessionResponseBodyData, recordContextID string) {
	// Check if recordContextID is provided
	if recordContextID == "" {
		return
	}

	// Extract AppInstanceId from response data
	if responseData == nil || responseData.AppInstanceId == nil || *responseData.AppInstanceId == "" {
		fmt.Printf("⚠️  AppInstanceId not found in response data, skipping browser replay context update\n")
		return
	}

	appInstanceID := *responseData.AppInstanceId

	// Create context name with prefix
	contextName := fmt.Sprintf("browserreplay-%s", appInstanceID)

	// Create Context object for update
	contextObj := &Context{
		ID:   recordContextID,
		Name: contextName,
	}

	// Call context.update interface
	fmt.Printf("Updating browser replay context: %s -> %s\n", contextName, recordContextID)
	updateResult, err := a.Context.Update(contextObj)

	if err != nil {
		fmt.Printf("❌ Error updating browser replay context: %v\n", err)
		// Continue execution even if context update fails
		return
	}

	_ = updateResult // Ignore result
}

// GetRegionID returns the region ID from config
func (a *AgentBay) GetRegionID() string {
	return a.config.RegionID
}
