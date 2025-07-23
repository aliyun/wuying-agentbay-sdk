# AgentBay Class API Reference

The `AgentBay` class is the main entry point for interacting with the AgentBay cloud environment. It provides methods for creating, retrieving, listing, and deleting sessions.

## Constructor

### NewAgentBay

```go
func NewAgentBay(apiKey string, cfg *Config) (*AgentBay, error)
```

**Parameters:**
- `apiKey` (string): The API key for authentication. If empty, the SDK will look for the `AGENTBAY_API_KEY` environment variable.
- `cfg` (*Config, optional): Configuration object containing region_id, endpoint, and timeout_ms. If not provided, default configuration is used.

**Returns:**
- `*AgentBay`: A new AgentBay instance.
- `error`: An error if initialization fails.

**Raises:**
- `error`: If no API key is provided and `AGENTBAY_API_KEY` environment variable is not set.

## Properties

### Context

The `Context` field provides access to a `ContextService` instance for managing persistent contexts. See the [Context API Reference](context.md) for more details.

## Methods


Creates a new session in the AgentBay cloud environment.


```go
Create(params *CreateSessionParams) (*SessionResult, error)
```

**Parameters:**
- `params` (*CreateSessionParams, optional): Parameters for session creation. If nil, default parameters will be used.

**Returns:**
- `*SessionResult`: A result object containing the new Session instance and RequestID.
- `error`: An error if the session creation fails.

**Behavior:**
- When `params` includes valid `PersistenceDataList`, after creating the session, the API will check `session.Context.Info()` to retrieve ContextStatusData.
- It will continuously monitor all data items' Status in ContextStatusData until all items show either "Success" or "Failed" status, or until the maximum retry limit (150 times with 2-second intervals) is reached.
- Any "Failed" status items will have their error messages printed.
- The Create operation only returns after context status checking completes.

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

	// Create a session with default parameters
	defaultResult, err := client.Create(nil)
	if err != nil {
		fmt.Printf("Error creating session: %v\n", err)
		os.Exit(1)
	}
	fmt.Printf("Created session with ID: %s\n", defaultResult.Session.SessionID)

	// Create a session with custom parameters
	labels := map[string]string{
		"project":     "demo",
		"environment": "testing",
	}
	params := &agentbay.CreateSessionParams{
		ImageId:   "linux_latest",
		Labels:    labels,
		ContextID: "your_context_id", // DEPRECATED: Use ContextSync instead
	}
	customResult, err := client.Create(params)
	if err != nil {
		fmt.Printf("Error creating custom session: %v\n", err)
		os.Exit(1)
	}
	fmt.Printf("Created custom session with ID: %s\n", customResult.Session.SessionID)

	// RECOMMENDED: Create a session with context synchronization
	policy := agentbay.SyncPolicy{
		UploadPolicy: &agentbay.UploadPolicy{
			AutoUpload:     true,
			UploadStrategy: agentbay.UploadBeforeResourceRelease,
			Period:         15,  // 15 minutes
		},
		DownloadPolicy: &agentbay.DownloadPolicy{
			AutoDownload:     true,
			DownloadStrategy: agentbay.DownloadAsync,
		},
	}
	contextSync := &agentbay.ContextSync{
		ContextID: "your_context_id",
		Path:      "/mnt/persistent",
		Policy:    &policy,
	}
	syncParams := &agentbay.CreateSessionParams{
		ImageId:      "linux_latest",
		ContextSync: []*agentbay.ContextSync{contextSync},
	}
	syncResult, err := client.Create(syncParams)
	if err != nil {
		fmt.Printf("Error creating session with context sync: %v\n", err)
		os.Exit(1)
	}
	fmt.Printf("Created session with context sync: %s\n", syncResult.Session.SessionID)
}
```


Lists all available sessions cached in the current client instance.


```go
List() (*SessionListResult, error)
```

**Returns:**
- `*SessionListResult`: A result object containing an array of Session instances and RequestID.
- `error`: An error if the session listing fails.

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

	// List all sessions
	result, err := client.List()
	if err != nil {
		fmt.Printf("Error listing sessions: %v\n", err)
		os.Exit(1)
	}

	fmt.Printf("Found %d sessions:\n", len(result.Sessions))
	for _, session := range result.Sessions {
		fmt.Printf("Session ID: %s\n", session.SessionID)
	}
}
```


Lists sessions filtered by the provided labels. It returns sessions that match all the specified labels. This method supports pagination to handle large result sets efficiently.


```go
ListByLabels(params *ListSessionParams) (*SessionListResult, error)
```

**Parameters:**
- `params` (*ListSessionParams, optional): Parameters for filtering sessions by labels. If nil, all sessions will be returned.

**Returns:**
- `*SessionListResult`: A result object containing the filtered sessions, pagination information, and RequestID.
- `error`: An error if the session listing fails.

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

	// Create pagination parameters
	labels := map[string]string{
		"environment": "production",
		"project":     "demo",
	}
	params := &agentbay.ListSessionParams{
		MaxResults: 10,
		NextToken:  "",
		Labels:     labels,
	}

	// Get the first page of results
	result, err := client.ListByLabels(params)
	if err != nil {
		fmt.Printf("Error listing sessions by labels: %v\n", err)
		os.Exit(1)
	}

	// Process the results
	fmt.Printf("Found %d sessions:\n", len(result.Sessions))
	for _, session := range result.Sessions {
		fmt.Printf("Session ID: %s\n", session.SessionID)
	}

	// Print pagination information
	fmt.Printf("Total count: %d\n", result.TotalCount)
	fmt.Printf("Max results per page: %d\n", result.MaxResults)
	fmt.Printf("Next token: %s\n", result.NextToken)

	// If there is a next page, retrieve it
	if result.NextToken != "" {
		params.NextToken = result.NextToken
		nextPageResult, err := client.ListByLabels(params)
		if err != nil {
			fmt.Printf("Error retrieving next page: %v\n", err)
			os.Exit(1)
		}
		// Process the next page...
	}
}
```


Deletes a session from the AgentBay cloud environment.


```go
Delete(session *Session, syncContext ...bool) (*DeleteResult, error)
```

**Parameters:**
- `session` (*Session): The session to delete.
- `syncContext` (bool, optional): If true, the API will trigger a file upload via `session.Context.Sync()` before actually releasing the session. Default is false.

**Returns:**
- `*DeleteResult`: A result object containing success status and RequestID.
- `error`: An error if the session deletion fails.

**Behavior:**
- When `syncContext` is true, the API will first call `session.Context.Sync()` to trigger file upload.
- It will then check `session.Context.Info()` to retrieve ContextStatusData and monitor all data items' Status.
- The API waits until all items show either "Success" or "Failed" status, or until the maximum retry limit (150 times with 2-second intervals) is reached.
- Any "Failed" status items will have their error messages printed.
- The session deletion only proceeds after context sync status checking completes.

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
	fmt.Printf("Created session with ID: %s\n", session.SessionID)
	
	// Use the session for operations...
	
	// Delete the session with context synchronization
	deleteResult, err := client.Delete(session, true)
	if err != nil {
		fmt.Printf("Error deleting session: %v\n", err)
		os.Exit(1)
	}
	
	fmt.Println("Session deleted successfully with synchronized context")
	fmt.Printf("Request ID: %s\n", deleteResult.RequestID)
}
```