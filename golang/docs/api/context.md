# Context API Reference

The Context API provides functionality for managing persistent storage contexts in the AgentBay cloud environment. Contexts allow you to persist data across sessions and reuse it in future sessions.

## Context Struct

The `Context` struct represents a persistent storage context in the AgentBay cloud environment.

### Properties

```go
ID  // The unique identifier of the context
Name  // The name of the context
State  // The current state of the context (e.g., "available", "in-use")
CreatedAt  // Date and time when the Context was created
LastUsedAt  // Date and time when the Context was last used
OsType  // The operating system type this context is bound to
```

## ContextService Struct

The `ContextService` struct provides methods for managing persistent contexts in the AgentBay cloud environment.

### List

Lists all available contexts.

```go
List() (*ContextListResult, error)
```

**Returns:**
- `*ContextListResult`: A result object containing the list of Context objects and RequestID.
- `error`: An error if the operation fails.

**Example:**
```go
package main

import (
	"fmt"
	"os"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

func main() {
	// Initialize the SDK
	client, err := agentbay.NewAgentBay("your_api_key", nil)
	if err != nil {
		fmt.Printf("Error initializing AgentBay client: %v\n", err)
		os.Exit(1)
	}

	// List all contexts
	result, err := client.Context.List()
	if err != nil {
		fmt.Printf("Error listing contexts: %v\n", err)
		os.Exit(1)
	}

	fmt.Printf("Found %d contexts:\n", len(result.Contexts))
	for _, context := range result.Contexts {
		fmt.Printf("Context ID: %s, Name: %s, State: %s\n", context.ID, context.Name, context.State)
	}
}
```

### Get

Gets a context by name. Optionally creates it if it doesn't exist.

```go
Get(name string, create bool) (*ContextResult, error)
```

**Parameters:**
- `name` (string): The name of the context to get.
- `create` (bool): Whether to create the context if it doesn't exist.

**Returns:**
- `*ContextResult`: A result object containing the Context object and RequestID.
- `error`: An error if the operation fails.

**Example:**
```go
package main

import (
	"fmt"
	"os"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

func main() {
	// Initialize the SDK
	client, err := agentbay.NewAgentBay("your_api_key", nil)
	if err != nil {
		fmt.Printf("Error initializing AgentBay client: %v\n", err)
		os.Exit(1)
	}

	// Get a context, creating it if it doesn't exist
	result, err := client.Context.Get("my-persistent-context", true)
	if err != nil {
		fmt.Printf("Error getting context: %v\n", err)
		os.Exit(1)
	}

	context := result.Context
	fmt.Printf("Context ID: %s, Name: %s, State: %s\n", context.ID, context.Name, context.State)
}
```

### Create

Creates a new context.

```go
Create(name string) (*ContextResult, error)
```

**Parameters:**
- `name` (string): The name of the context to create.

**Returns:**
- `*ContextResult`: A result object containing the created Context object and RequestID.
- `error`: An error if the operation fails.

**Example:**
```go
package main

import (
	"fmt"
	"os"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

func main() {
	// Initialize the SDK
	client, err := agentbay.NewAgentBay("your_api_key", nil)
	if err != nil {
		fmt.Printf("Error initializing AgentBay client: %v\n", err)
		os.Exit(1)
	}

	// Create a new context
	result, err := client.Context.Create("my-new-context")
	if err != nil {
		fmt.Printf("Error creating context: %v\n", err)
		os.Exit(1)
	}

	context := result.Context
	fmt.Printf("Created context with ID: %s, Name: %s\n", context.ID, context.Name)
}
```

### Update

Updates an existing context.

```go
Update(context *Context) (*OperationResult, error)
```

**Parameters:**
- `context` (*Context): The context object to update.

**Returns:**
- `*OperationResult`: A result object containing success status and RequestID.
- `error`: An error if the operation fails.

**Example:**
```go
package main

import (
	"fmt"
	"os"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

func main() {
	// Initialize the SDK
	client, err := agentbay.NewAgentBay("your_api_key", nil)
	if err != nil {
		fmt.Printf("Error initializing AgentBay client: %v\n", err)
		os.Exit(1)
	}

	// Get an existing context
	result, err := client.Context.Get("my-context", false)
	if err != nil {
		fmt.Printf("Error getting context: %v\n", err)
		os.Exit(1)
	}

	context := result.Context
	
	// Update the context name
	context.Name = "my-updated-context"
	
	// Save the changes
	updateResult, err := client.Context.Update(context)
	if err != nil {
		fmt.Printf("Error updating context: %v\n", err)
		os.Exit(1)
	}

	fmt.Println("Context updated successfully")
	fmt.Printf("Request ID: %s\n", updateResult.RequestID)
}
```

### Delete

Deletes a context.

```go
Delete(context *Context) (*OperationResult, error)
```

**Parameters:**
- `context` (*Context): The context object to delete.

**Returns:**
- `*OperationResult`: A result object containing success status and RequestID.
- `error`: An error if the operation fails.

**Example:**
```go
package main

import (
	"fmt"
	"os"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

func main() {
	// Initialize the SDK
	client, err := agentbay.NewAgentBay("your_api_key", nil)
	if err != nil {
		fmt.Printf("Error initializing AgentBay client: %v\n", err)
		os.Exit(1)
	}

	// Get an existing context
	result, err := client.Context.Get("my-context", false)
	if err != nil {
		fmt.Printf("Error getting context: %v\n", err)
		os.Exit(1)
	}

	context := result.Context
	
	// Delete the context
	deleteResult, err := client.Context.Delete(context)
	if err != nil {
		fmt.Printf("Error deleting context: %v\n", err)
		os.Exit(1)
	}

	fmt.Println("Context deleted successfully")
	fmt.Printf("Request ID: %s\n", deleteResult.RequestID)
}
```

## Related Resources

- [Session API Reference](session.md)
- [ContextManager API Reference](context-manager.md) 