package agentbay

import (
	"encoding/json"
	"fmt"
	"os"
	"strings"
	"sync"

	openapi "github.com/alibabacloud-go/darabonba-openapi/v2/client"
	"github.com/alibabacloud-go/tea/tea"
	mcp "github.com/aliyun/wuying-agentbay-sdk/golang/api/client"
)

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
func NewAgentBay(apiKey string) (*AgentBay, error) {
	if apiKey == "" {
		apiKey = os.Getenv("AGENTBAY_API_KEY")
		if apiKey == "" {
			return nil, fmt.Errorf("API key is required. Provide it as a parameter or set the AGENTBAY_API_KEY environment variable")
		}
	}

	// Load configuration
	config := LoadConfig()

	apiConfig := &openapi.Config{
		RegionId: tea.String(config.RegionID),
		Endpoint: tea.String(config.Endpoint),
	}
	apiConfig.ReadTimeout = tea.Int(config.TimeoutMs)
	apiConfig.ConnectTimeout = tea.Int(config.TimeoutMs)

	client, err := mcp.NewClient(apiConfig)
	if err != nil {
		return nil, fmt.Errorf("create openapi client fails")
	}

	agentBay := &AgentBay{
		APIKey:   apiKey,
		RegionId: config.RegionID,
		Client:   client,
	}

	// Initialize context service
	agentBay.Context = &ContextService{AgentBay: agentBay}

	return agentBay, nil
}

// Create creates a new session in the AgentBay cloud environment.
// If params is nil, default parameters will be used.
func (a *AgentBay) Create(params *CreateSessionParams) (*Session, error) {
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

	// Add labels if provided
	if len(params.Labels) > 0 {
		labelsJSON, err := params.GetLabelsJSON()
		if err != nil {
			return nil, fmt.Errorf("failed to marshal labels to JSON: %v", err)
		}
		createSessionRequest.Labels = tea.String(labelsJSON)
	}

	// Log API request
	fmt.Println("API Call: CreateMcpSession")
	fmt.Printf("Request: ")
	if createSessionRequest.ContextId != nil {
		fmt.Printf("ContextId=%s, ", *createSessionRequest.ContextId)
	}
	if createSessionRequest.Labels != nil {
		fmt.Printf("Labels=%s", *createSessionRequest.Labels)
	}
	fmt.Println()

	response, err := a.Client.CreateMcpSession(createSessionRequest)

	// Log API response
	if err != nil {
		fmt.Println("Error calling CreateMcpSession:", err)
		return nil, err
	}

	// Log only the response body
	if response != nil && response.Body != nil {
		// Convert response body to JSON for proper printing without escaped characters
		responseJSON, _ := json.MarshalIndent(response.Body, "", "  ")
		// Replace \u0026 with & for better readability
		jsonStr := strings.Replace(string(responseJSON), "\\u0026", "&", -1)
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
		return nil, fmt.Errorf(errMsg)
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
	return session, nil
}

// List lists all available sessions.
func (a *AgentBay) List() ([]Session, error) {
	var sessions []Session
	a.Sessions.Range(func(key, value interface{}) bool {
		if session, ok := value.(Session); ok {
			sessions = append(sessions, session)
		}
		return true
	})
	return sessions, nil
}

// ListByLabels lists sessions filtered by the provided labels.
// It returns sessions that match all the specified labels.
func (a *AgentBay) ListByLabels(labels map[string]string) ([]Session, error) {
	// Convert labels to JSON
	labelsJSON, err := json.Marshal(labels)
	if err != nil {
		return nil, fmt.Errorf("failed to marshal labels to JSON: %v", err)
	}

	listSessionRequest := &mcp.ListSessionRequest{
		Authorization: tea.String("Bearer " + a.APIKey),
		Labels:        tea.String(string(labelsJSON)),
	}

	// Log API request
	fmt.Println("API Call: ListSession")
	fmt.Printf("Request: Labels=%s\n", *listSessionRequest.Labels)

	response, err := a.Client.ListSession(listSessionRequest)

	// Log API response
	if err != nil {
		fmt.Println("Error calling ListSession:", err)
		return nil, err
	}
	if response != nil && response.Body != nil {
		fmt.Println("Response from ListSession:", response.Body)
	}

	var sessions []Session
	if response.Body != nil && response.Body.Data != nil {
		for _, sessionData := range response.Body.Data {
			if sessionData.SessionId != nil {
				session := NewSession(a, *sessionData.SessionId)
				sessions = append(sessions, *session)
				// Also store in the local cache
				a.Sessions.Store(*sessionData.SessionId, *session)
			}
		}
	}

	return sessions, nil
}

// Delete deletes a session by ID.
func (a *AgentBay) Delete(session *Session) error {
	err := session.Delete()
	if err == nil {
		a.Sessions.Delete(session.SessionID)
	}
	return err
}
