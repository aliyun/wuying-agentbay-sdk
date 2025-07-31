package agentbay

import (
	"fmt"

	"github.com/alibabacloud-go/tea/tea"
	mcp "github.com/aliyun/wuying-agentbay-sdk/golang/api/client"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/models"
)

// Context represents a persistent storage context in the AgentBay cloud environment.
type Context struct {
	// ID is the unique identifier of the context.
	ID string

	// Name is the name of the context.
	Name string

	// State is the current state of the context (e.g., "available", "in-use").
	State string

	// CreatedAt is the date and time when the Context was created.
	CreatedAt string

	// LastUsedAt is the date and time when the Context was last used.
	LastUsedAt string

	// OSType is the operating system type this context is bound to.
	OSType string
}

// ContextResult wraps context operation result and RequestID
type ContextResult struct {
	models.ApiResponse
	ContextID string
	Context   *Context
}

// ContextListResult wraps context list and RequestID
type ContextListResult struct {
	models.ApiResponse
	Contexts   []*Context
	NextToken  string
	MaxResults int32
	TotalCount int32
}

// ContextCreateResult wraps context creation result and RequestID
type ContextCreateResult struct {
	models.ApiResponse
	ContextID string
}

// ContextModifyResult wraps context modification result and RequestID
type ContextModifyResult struct {
	models.ApiResponse
	Success bool
}

// ContextDeleteResult wraps context deletion result and RequestID
type ContextDeleteResult struct {
	models.ApiResponse
	Success bool
}

// ContextService provides methods to manage persistent contexts in the AgentBay cloud environment.
type ContextService struct {
	// AgentBay is the AgentBay instance.
	AgentBay *AgentBay
}

// ContextListParams contains parameters for listing contexts
type ContextListParams struct {
	MaxResults int32  // Number of results per page
	NextToken  string // Token for the next page
}

// NewContextListParams creates a new ContextListParams with default values
func NewContextListParams() *ContextListParams {
	return &ContextListParams{
		MaxResults: 10, // Default page size
		NextToken:  "",
	}
}

// List lists all available contexts with pagination support.
func (cs *ContextService) List(params *ContextListParams) (*ContextListResult, error) {
	if params == nil {
		params = NewContextListParams()
	}

	request := &mcp.ListContextsRequest{
		Authorization: tea.String("Bearer " + cs.AgentBay.APIKey),
		MaxResults:    tea.Int32(params.MaxResults),
	}

	// Add NextToken if provided
	if params.NextToken != "" {
		request.NextToken = tea.String(params.NextToken)
	}

	// Log API request
	fmt.Println("API Call: ListContexts")
	fmt.Printf("Request: MaxResults=%d", *request.MaxResults)
	if request.NextToken != nil {
		fmt.Printf(", NextToken=%s", *request.NextToken)
	}
	fmt.Println()

	response, err := cs.AgentBay.Client.ListContexts(request)

	// Log API response
	if err != nil {
		fmt.Println("Error calling ListContexts:", err)
		return nil, fmt.Errorf("failed to list contexts: %v", err)
	}

	// Extract RequestID
	requestID := models.ExtractRequestID(response)

	if response != nil && response.Body != nil {
		fmt.Println("Response from ListContexts:", response.Body)
	}

	var contexts []*Context
	var nextToken string
	var maxResults int32
	var totalCount int32

	if response.Body != nil {
		// Extract pagination information
		if response.Body.NextToken != nil {
			nextToken = *response.Body.NextToken
		}
		// Set maxResults and totalCount from params or response
		maxResults = params.MaxResults
		if response.Body.TotalCount != nil {
			totalCount = *response.Body.TotalCount
		}

		// Extract context data
		if response.Body.Data != nil {
			for _, contextData := range response.Body.Data {
				context := &Context{
					ID:         tea.StringValue(contextData.Id),
					Name:       tea.StringValue(contextData.Name),
					State:      tea.StringValue(contextData.State),
					CreatedAt:  tea.StringValue(contextData.CreateTime),
					LastUsedAt: tea.StringValue(contextData.LastUsedTime),
					OSType:     tea.StringValue(contextData.OsType),
				}
				contexts = append(contexts, context)
			}
		}
	}

	return &ContextListResult{
		ApiResponse: models.ApiResponse{
			RequestID: requestID,
		},
		Contexts:   contexts,
		NextToken:  nextToken,
		MaxResults: maxResults,
		TotalCount: totalCount,
	}, nil
}

// Get gets a context by name. Optionally creates it if it doesn't exist.
func (cs *ContextService) Get(name string, create bool) (*ContextResult, error) {
	request := &mcp.GetContextRequest{
		Name:          tea.String(name),
		AllowCreate:   tea.Bool(create),
		Authorization: tea.String("Bearer " + cs.AgentBay.APIKey),
	}

	// Log API request
	fmt.Println("API Call: GetContext")
	fmt.Printf("Request: Name=%s, AllowCreate=%t\n", *request.Name, *request.AllowCreate)

	response, err := cs.AgentBay.Client.GetContext(request)

	// Log API response
	if err != nil {
		fmt.Println("Error calling GetContext:", err)
		return nil, fmt.Errorf("failed to get context %s: %v", name, err)
	}

	// Extract RequestID
	requestID := models.ExtractRequestID(response)

	if response != nil && response.Body != nil {
		fmt.Println("Response from GetContext:", response.Body)
	}

	if response.Body == nil || response.Body.Data == nil || response.Body.Data.Id == nil {
		return &ContextResult{
			ApiResponse: models.ApiResponse{
				RequestID: requestID,
			},
			ContextID: "",
			Context:   nil,
		}, nil
	}

	// Create context object
	context := &Context{
		ID:         tea.StringValue(response.Body.Data.Id),
		Name:       tea.StringValue(response.Body.Data.Name),
		State:      tea.StringValue(response.Body.Data.State),
		CreatedAt:  tea.StringValue(response.Body.Data.CreateTime),
		LastUsedAt: tea.StringValue(response.Body.Data.LastUsedTime),
		OSType:     tea.StringValue(response.Body.Data.OsType),
	}

	return &ContextResult{
		ApiResponse: models.ApiResponse{
			RequestID: requestID,
		},
		ContextID: tea.StringValue(response.Body.Data.Id),
		Context:   context,
	}, nil
}

// Create creates a new context with the given name.
func (cs *ContextService) Create(name string) (*ContextCreateResult, error) {
	result, err := cs.Get(name, true)
	if err != nil {
		return nil, err
	}

	if result == nil || result.ContextID == "" {
		return nil, fmt.Errorf("failed to create context: empty response")
	}

	return &ContextCreateResult{
		ApiResponse: models.ApiResponse{
			RequestID: result.RequestID,
		},
		ContextID: result.ContextID,
	}, nil
}

// Update updates the specified context.
// Returns a result with success status.
func (cs *ContextService) Update(context *Context) (*ContextModifyResult, error) {
	request := &mcp.ModifyContextRequest{
		Id:            tea.String(context.ID),
		Name:          tea.String(context.Name),
		Authorization: tea.String("Bearer " + cs.AgentBay.APIKey),
	}

	// Log API request
	fmt.Println("API Call: ModifyContext")
	fmt.Printf("Request: Id=%s, Name=%s\n", *request.Id, *request.Name)

	response, err := cs.AgentBay.Client.ModifyContext(request)

	// Log API response
	if err != nil {
		fmt.Println("Error calling ModifyContext:", err)
		return nil, fmt.Errorf("failed to update context %s: %v", context.ID, err)
	}

	// Extract RequestID
	requestID := models.ExtractRequestID(response)

	if response != nil && response.Body != nil {
		fmt.Println("Response from ModifyContext:", response.Body)
	}

	// Check if update was successful
	success := true
	if response != nil && response.Body != nil && response.Body.Success != nil {
		success = *response.Body.Success
	}

	return &ContextModifyResult{
		ApiResponse: models.ApiResponse{
			RequestID: requestID,
		},
		Success: success,
	}, nil
}

// Delete deletes the specified context.
func (cs *ContextService) Delete(context *Context) (*ContextDeleteResult, error) {
	request := &mcp.DeleteContextRequest{
		Id:            tea.String(context.ID),
		Authorization: tea.String("Bearer " + cs.AgentBay.APIKey),
	}

	// Log API request
	fmt.Println("API Call: DeleteContext")
	fmt.Printf("Request: Id=%s\n", *request.Id)

	response, err := cs.AgentBay.Client.DeleteContext(request)

	// Log API response
	if err != nil {
		fmt.Println("Error calling DeleteContext:", err)
		return nil, fmt.Errorf("failed to delete context %s: %v", context.ID, err)
	}

	// Extract RequestID
	requestID := models.ExtractRequestID(response)

	if response != nil && response.Body != nil {
		fmt.Println("Response from DeleteContext:", response.Body)
	}

	return &ContextDeleteResult{
		ApiResponse: models.ApiResponse{
			RequestID: requestID,
		},
		Success: true,
	}, nil
}
