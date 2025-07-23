package agentbay

import (
	"encoding/json"
	"fmt"
	"os"
	"strings"
	"sync"
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
	cfg *Config
}

// WithConfig returns an Option that sets the configuration for the AgentBay client.
func WithConfig(cfg *Config) Option {
	return func(c *AgentBayConfig) {
		c.cfg = cfg
	}
}

// AgentBay represents the main client for interacting with the AgentBay cloud runtime environment.
type AgentBay struct {
	APIKey   string
	RegionId string
	Client   *mcp.Client
	Sessions sync.Map
	Context  *ContextService
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

	// Load configuration using LoadConfig function
	// This will load from environment variables, .env file, or use defaults
	config := LoadConfig(config_option.cfg)

	// Create API client
	apiConfig := &openapiutil.Config{
		RegionId:       tea.String(config.RegionID),
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
		APIKey:   apiKey,
		RegionId: config.RegionID,
		Client:   client,
		Context:  nil, // Will be initialized after creation
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
func (a *AgentBay) Create(params *CreateSessionParams) (*SessionResult, error) {
	if params == nil {
		params = NewCreateSessionParams()
	}

	createSessionRequest := &mcp.CreateMcpSessionRequest{
		Authorization: tea.String("Bearer " + a.APIKey),
	}

	// Add context_id if provided
	if params.ContextID != "" {
		createSessionRequest.ContextId = tea.String(params.ContextID)
	}

	// Add image_id if provided
	if params.ImageId != "" {
		createSessionRequest.ImageId = tea.String(params.ImageId)
	}

	// Add labels if provided
	if len(params.Labels) > 0 {
		labelsJSON, err := params.GetLabelsJSON()
		if err != nil {
			return nil, fmt.Errorf("failed to marshal labels to JSON: %v", err)
		}
		createSessionRequest.Labels = tea.String(labelsJSON)
	}

	// Flag to indicate if we need to wait for context synchronization
	hasPersistenceData := false

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

	if len(persistenceDataList) > 0 {
		createSessionRequest.PersistenceDataList = persistenceDataList
		hasPersistenceData = true
	}

	// Log API request
	fmt.Println("API Call: CreateMcpSession")
	fmt.Printf("Request: ")
	if createSessionRequest.ContextId != nil {
		fmt.Printf("ContextId=%s, ", *createSessionRequest.ContextId)
	}
	if createSessionRequest.ImageId != nil {
		fmt.Printf("ImageId=%s, ", *createSessionRequest.ImageId)
	}
	if createSessionRequest.Labels != nil {
		fmt.Printf("Labels=%s, ", *createSessionRequest.Labels)
	}
	if len(createSessionRequest.PersistenceDataList) > 0 {
		fmt.Printf("PersistenceDataList=%d items, ", len(createSessionRequest.PersistenceDataList))
		for i, pd := range createSessionRequest.PersistenceDataList {
			fmt.Printf("Item%d[ContextId=%s, Path=%s", i, tea.StringValue(pd.ContextId), tea.StringValue(pd.Path))
			if pd.Policy != nil {
				fmt.Printf(", Policy=%s", tea.StringValue(pd.Policy))
			}
			fmt.Printf("], ")
		}
	}
	fmt.Println()

	response, err := a.Client.CreateMcpSession(createSessionRequest)

	// Log API response
	if err != nil {
		fmt.Println("Error calling CreateMcpSession:", err)
		return nil, err
	}

	// Extract RequestID
	requestID := models.ExtractRequestID(response)

	// Log only the response body
	if response != nil && response.Body != nil {
		// Convert response body to JSON for proper printing without escaped characters
		responseJSON, _ := json.MarshalIndent(response.Body, "", "  ")
		// Replace \u0026 with & for better readability
		jsonStr := strings.ReplaceAll(string(responseJSON), "\\u0026", "&")
		fmt.Println("Response from CreateMcpSession:")
		fmt.Println(jsonStr)
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
		return nil, fmt.Errorf("%s", errMsg)
	}

	// Check if SessionId is present
	if response.Body.Data.SessionId == nil {
		return nil, fmt.Errorf("no session ID returned from CreateMcpSession")
	}

	// ResourceUrl is optional in CreateMcpSession response

	// Create a new Session using the NewSession function from session.go
	session := NewSession(a, *response.Body.Data.SessionId)

	// Set the ResourceUrl field from the response data if present
	if response.Body.Data.ResourceUrl != nil {
		session.ResourceUrl = *response.Body.Data.ResourceUrl
	}

	a.Sessions.Store(session.SessionID, *session)

	// If we have persistence data, wait for context synchronization
	if hasPersistenceData {
		fmt.Println("Waiting for context synchronization to complete...")

		// Wait for context synchronization to complete
		const maxRetries = 150  // Maximum number of retries
		const retryInterval = 2 // Seconds to wait between retries

		for retry := 0; retry < maxRetries; retry++ {
			// Get context status data
			infoResult, err := session.Context.Info()
			if err != nil {
				fmt.Printf("Error getting context info on attempt %d: %v\n", retry+1, err)
				time.Sleep(time.Duration(retryInterval) * time.Second)
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
			time.Sleep(time.Duration(retryInterval) * time.Second)
		}
	}

	// Return result with RequestID
	return &SessionResult{
		ApiResponse: models.ApiResponse{
			RequestID: requestID,
		},
		Session: session,
	}, nil
}

// List lists all available sessions.
func (a *AgentBay) List() (*SessionListResult, error) {
	var sessions []Session
	a.Sessions.Range(func(key, value interface{}) bool {
		if session, ok := value.(Session); ok {
			sessions = append(sessions, session)
		}
		return true
	})

	// No actual API call here, so RequestID is empty
	return &SessionListResult{
		ApiResponse: models.ApiResponse{
			RequestID: "",
		},
		Sessions: sessions,
	}, nil
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

// ListByLabels lists sessions filtered by the provided labels with pagination support.
// It returns sessions that match all the specified labels.
func (a *AgentBay) ListByLabels(params *ListSessionParams) (*SessionListResult, error) {
	if params == nil {
		params = NewListSessionParams()
	}

	// Convert labels to JSON
	labelsJSON, err := json.Marshal(params.Labels)
	if err != nil {
		return nil, fmt.Errorf("failed to marshal labels to JSON: %v", err)
	}

	listSessionRequest := &mcp.ListSessionRequest{
		Authorization: tea.String("Bearer " + a.APIKey),
		Labels:        tea.String(string(labelsJSON)),
		MaxResults:    tea.Int32(params.MaxResults),
	}

	// Add NextToken if provided
	if params.NextToken != "" {
		listSessionRequest.NextToken = tea.String(params.NextToken)
	}

	// Log API request
	fmt.Println("API Call: ListSession")
	fmt.Printf("Request: Labels=%s, MaxResults=%d", *listSessionRequest.Labels, *listSessionRequest.MaxResults)
	if listSessionRequest.NextToken != nil {
		fmt.Printf(", NextToken=%s", *listSessionRequest.NextToken)
	}
	fmt.Println()

	response, err := a.Client.ListSession(listSessionRequest)

	// Log API response
	if err != nil {
		fmt.Println("Error calling ListSession:", err)
		return nil, err
	}

	// Extract RequestID
	requestID := models.ExtractRequestID(response)

	if response != nil && response.Body != nil {
		fmt.Println("Response from ListSession:", response.Body)
	}

	var sessions []Session
	var nextToken string
	var maxResults int32
	var totalCount int32

	if response.Body != nil {
		// Extract pagination information
		if response.Body.NextToken != nil {
			nextToken = *response.Body.NextToken
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
					session := NewSession(a, *sessionData.SessionId)
					sessions = append(sessions, *session)
					// Also store in the local cache
					a.Sessions.Store(*sessionData.SessionId, *session)
				}
			}
		}
	}

	return &SessionListResult{
		ApiResponse: models.ApiResponse{
			RequestID: requestID,
		},
		Sessions:   sessions,
		NextToken:  nextToken,
		MaxResults: maxResults,
		TotalCount: totalCount,
	}, nil
}

// Delete deletes a session by ID.
func (a *AgentBay) Delete(session *Session, syncContext ...bool) (*DeleteResult, error) {
	result, err := session.Delete(syncContext...)
	if err == nil {
		a.Sessions.Delete(session.SessionID)
	}
	return result, err
}
