# ContextManager API Reference

The `ContextManager` class provides functionality for managing contexts within a session. It enables you to interact with the contexts that are synchronized to the session, including reading and writing data, and managing file operations.

## Overview

The `ContextManager` is accessed through a session instance and provides functionality for managing contexts within that session.

## Methods


Synchronizes a context with the session.


```go
SyncContext(contextID string, path string, policy *SyncPolicy) (*OperationResult, error)
```

**Parameters:**
- `contextID` (string): The ID of the context to synchronize.
- `path` (string): The path where the context should be mounted.
- `policy` (*SyncPolicy, optional): The synchronization policy. If nil, default policy is used.

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

	// Create a session
	createResult, err := client.Create(nil)
	if err != nil {
		fmt.Printf("Error creating session: %v\n", err)
		os.Exit(1)
	}
	
	session := createResult.Session
	
	// Get or create a context
	contextResult, err := client.Context.Get("my-context", true)
	if err != nil {
		fmt.Printf("Error getting context: %v\n", err)
		os.Exit(1)
	}
	
	// Create a sync policy
	policy := agentbay.NewSyncPolicy()
	
	// Synchronize the context with the session
	syncResult, err := session.Context.SyncContext(
		contextResult.Context.ID,
		"/mnt/persistent",
		policy,
	)
	if err != nil {
		fmt.Printf("Error synchronizing context: %v\n", err)
		os.Exit(1)
	}
	
	fmt.Println("Context synchronized successfully")
	fmt.Printf("Request ID: %s\n", syncResult.RequestID)
}
```


Gets information about a context that is synchronized to the session.


```go
GetInfo(path string) (*OperationResult, error)
```

**Parameters:**
- `path` (string): The path where the context is mounted.

**Returns:**
- `*OperationResult`: A result object containing the context information as data, success status, and RequestID.
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

	// Create a session with a synchronized context
	// ... (assume context is synchronized to '/mnt/persistent')
	
	// Get information about the synchronized context
	infoResult, err := session.Context.GetInfo("/mnt/persistent")
	if err != nil {
		fmt.Printf("Error getting context info: %v\n", err)
		os.Exit(1)
	}
	
	// The data is returned as an interface{}, convert it to ContextInfo
	contextInfo, ok := infoResult.Data.(*agentbay.ContextInfo)
	if !ok {
		fmt.Println("Error: Context info data is not in expected format")
		os.Exit(1)
	}
	
	fmt.Println("Context Information:")
	fmt.Printf("  Context ID: %s\n", contextInfo.ContextID)
	fmt.Printf("  Path: %s\n", contextInfo.Path)
	fmt.Printf("  State: %s\n", contextInfo.State)
	fmt.Printf("Request ID: %s\n", infoResult.RequestID)
}
```


Deletes a context that is synchronized to the session.


```go
DeleteContext(path string) (*OperationResult, error)
```

**Parameters:**
- `path` (string): The path where the context is mounted.

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

	// Create a session with a synchronized context
	// ... (assume context is synchronized to '/mnt/persistent')
	
	// Delete the synchronized context
	deleteResult, err := session.Context.DeleteContext("/mnt/persistent")
	if err != nil {
		fmt.Printf("Error deleting context: %v\n", err)
		os.Exit(1)
	}
	
	fmt.Println("Context deleted successfully")
	fmt.Printf("Request ID: %s\n", deleteResult.RequestID)
}
```


Lists all contexts that are synchronized to the session.


```go
List() (*OperationResult, error)
```

**Returns:**
- `*OperationResult`: A result object containing the list of synchronized contexts as data, success status, and RequestID.
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

	// Create a session with synchronized contexts
	// ...
	
	// List all synchronized contexts
	listResult, err := session.Context.List()
	if err != nil {
		fmt.Printf("Error listing contexts: %v\n", err)
		os.Exit(1)
	}
	
	// The data is returned as an interface{}, convert it to []ContextInfo
	contexts, ok := listResult.Data.([]agentbay.ContextInfo)
	if !ok {
		fmt.Println("Error: Contexts data is not in expected format")
		os.Exit(1)
	}
	
	fmt.Printf("Found %d synchronized contexts:\n", len(contexts))
	for _, context := range contexts {
		fmt.Printf("  Context ID: %s, Path: %s, State: %s\n", context.ContextID, context.Path, context.State)
	}
	fmt.Printf("Request ID: %s\n", listResult.RequestID)
}
``` 