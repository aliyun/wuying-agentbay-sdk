package agentbay

import (
	"fmt"

	"github.com/alibabacloud-go/tea/tea"
	mcp "github.com/aliyun/wuying-agentbay-sdk/golang/api/client"
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

// ContextService provides methods to manage persistent contexts in the AgentBay cloud environment.
type ContextService struct {
	// AgentBay is the AgentBay instance.
	AgentBay *AgentBay
}

// List lists all available contexts.
func (cs *ContextService) List() ([]Context, error) {
	request := &mcp.ListContextsRequest{
		Authorization: tea.String("Bearer " + cs.AgentBay.APIKey),
	}

	// Log API request
	fmt.Println("API Call: ListContexts")
	fmt.Println("Request: (no parameters)")

	response, err := cs.AgentBay.Client.ListContexts(request)

	// Log API response
	if err != nil {
		fmt.Println("Error calling ListContexts:", err)
		return nil, fmt.Errorf("failed to list contexts: %v", err)
	}
	if response != nil && response.Body != nil {
		fmt.Println("Response from ListContexts:", response.Body)
	}

	var contexts []Context
	if response.Body != nil && response.Body.Data != nil {
		for _, contextData := range response.Body.Data {
			context := Context{
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

	return contexts, nil
}

// Get gets a context by name. Optionally creates it if it doesn't exist.
func (cs *ContextService) Get(name string, create bool) (*Context, error) {
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
	if response != nil && response.Body != nil {
		fmt.Println("Response from GetContext:", response.Body)
	}

	if response.Body == nil || response.Body.Data == nil || response.Body.Data.Id == nil {
		return nil, nil
	}

	// Create a context object directly from the response data
	context := &Context{
		ID:         tea.StringValue(response.Body.Data.Id),
		Name:       tea.StringValue(response.Body.Data.Name),
		State:      tea.StringValue(response.Body.Data.State),
		CreatedAt:  tea.StringValue(response.Body.Data.CreateTime),
		LastUsedAt: tea.StringValue(response.Body.Data.LastUsedTime),
		OSType:     tea.StringValue(response.Body.Data.OsType),
	}

	// If the name is empty (which shouldn't happen), use the provided name
	if context.Name == "" {
		context.Name = name
	}

	return context, nil
}

// Create creates a new context with the given name.
func (cs *ContextService) Create(name string) (*Context, error) {
	return cs.Get(name, true)
}

// Update updates the specified context.
// Returns true if the update was successful, false otherwise.
func (cs *ContextService) Update(context *Context) (bool, error) {
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
		return false, fmt.Errorf("failed to update context %s: %v", context.ID, err)
	}
	if response != nil && response.Body != nil {
		fmt.Println("Response from ModifyContext:", response.Body)
	}

	// Check if the update was successful
	if response != nil && response.Body != nil && response.Body.Success != nil {
		return *response.Body.Success, nil
	}

	// If we can't determine success from the response, assume it was successful
	// since there was no error
	return true, nil
}

// Delete deletes the specified context.
func (cs *ContextService) Delete(context *Context) error {
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
		return fmt.Errorf("failed to delete context %s: %v", context.ID, err)
	}
	if response != nil && response.Body != nil {
		fmt.Println("Response from DeleteContext:", response.Body)
	}

	return nil
}
