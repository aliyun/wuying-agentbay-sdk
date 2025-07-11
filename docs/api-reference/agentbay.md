# AgentBay Class API Reference

The `AgentBay` class is the main entry point for interacting with the AgentBay cloud environment. It provides methods for creating, retrieving, listing, and deleting sessions.

## Constructor

### Python

```python
AgentBay(api_key=None, cfg=None)
```

**Parameters:**
- `api_key` (str, optional): The API key for authentication. If not provided, the SDK will look for the `AGENTBAY_API_KEY` environment variable.
- `cfg` (Config, optional): Configuration object containing region_id, endpoint, and timeout_ms. If not provided, default configuration is used.

**Raises:**
- `ValueError`: If no API key is provided and `AGENTBAY_API_KEY` environment variable is not set.

### TypeScript

```typescript
new AgentBay({
  apiKey?: string;
  config?: Config;
})
```

**Parameters:**
- `apiKey` (string, optional): The API key for authentication. If not provided, the SDK will look for the `AGENTBAY_API_KEY` environment variable.
- `config` (Config, optional): Configuration object containing regionId, endpoint, and timeoutMs. If not provided, default configuration is used.

### Golang

```go
NewAgentBay(apiKey string, config *Config) (*AgentBay, error)
```

**Parameters:**
- `apiKey` (string): The API key for authentication. If empty, the SDK will look for the `AGENTBAY_API_KEY` environment variable.
- `config` (*Config, optional): Configuration struct containing RegionId, Endpoint, and TimeoutMs. If nil, default configuration is used.

**Returns:**
- `*AgentBay`: A pointer to the AgentBay instance.
- `error`: An error if the initialization fails.

## Properties

### Python

```python
context
```
A `ContextService` instance for managing persistent contexts. See the [Context API Reference](context.md) for more details.

### TypeScript

```typescript
context
```
A `ContextService` instance for managing persistent contexts. See the [Context API Reference](context.md) for more details.

### Golang

```go
Context
```
A `ContextService` instance for managing persistent contexts. See the [Context API Reference](context.md) for more details.

## Methods

### create / Create

Creates a new session in the AgentBay cloud environment.

#### Python

```python
create(params: Optional[CreateSessionParams] = None) -> SessionResult
```

**Parameters:**
- `params` (CreateSessionParams, optional): Parameters for session creation. If None, default parameters will be used.

**Returns:**
- `SessionResult`: A result object containing the new Session instance, success status, request ID, and error message if any.

**Raises:**
- `AgentBayError`: If the session creation fails due to API errors or other issues.

**Example:**
```python
from agentbay import AgentBay
from agentbay.session_params import CreateSessionParams
from agentbay.context_sync import ContextSync, SyncPolicy

# Initialize the SDK
agent_bay = AgentBay(api_key="your_api_key")

# Create a session with default parameters
default_result = agent_bay.create()
if default_result.success:
    default_session = default_result.session
    print(f"Created session with ID: {default_session.session_id}")

# Create a session with custom parameters
params = CreateSessionParams(
    image_id="linux_latest",
    labels={"project": "demo", "environment": "testing"},
    context_id="your_context_id"  # DEPRECATED: Use context_syncs instead
)
custom_result = agent_bay.create(params)
if custom_result.success:
    custom_session = custom_result.session
    print(f"Created custom session with ID: {custom_session.session_id}")

# RECOMMENDED: Create a session with context synchronization
context_sync = ContextSync.new(
    context_id="your_context_id",
    path="/mnt/persistent",
    policy=SyncPolicy.default()
)
sync_params = CreateSessionParams(
    image_id="linux_latest",
    context_syncs=[context_sync]
)
sync_result = agent_bay.create(sync_params)
if sync_result.success:
    sync_session = sync_result.session
    print(f"Created session with context sync: {sync_session.session_id}")
```

#### TypeScript

```typescript
create(params?: CreateSessionParams): Promise<SessionResult>
```

**Parameters:**
- `params` (CreateSessionParams, optional): Parameters for session creation.

**Returns:**
- `Promise<SessionResult>`: A promise that resolves to a result object containing the new Session instance, success status, request ID, and error message if any.

**Throws:**
- `Error`: If the session creation fails.

**Example:**
```typescript
import { AgentBay, CreateSessionParams } from 'wuying-agentbay-sdk';
import { ContextSync, SyncPolicy } from 'wuying-agentbay-sdk/context-sync';

// Initialize the SDK
const agentBay = new AgentBay({ apiKey: 'your_api_key' });

// Create a session with default parameters
async function createDefaultSession() {
  const result = await agentBay.create();
  if (result.success) {
    console.log(`Created session with ID: ${result.session.sessionId}`);
    return result.session;
  }
  throw new Error(`Failed to create session: ${result.errorMessage}`);
}

// Create a session with custom parameters
async function createCustomSession() {
  const params: CreateSessionParams = {
    imageId: 'linux_latest',
    labels: { project: 'demo', environment: 'testing' },
    contextId: 'your_context_id'  // DEPRECATED: Use contextSync instead
  };
  
  const result = await agentBay.create(params);
  if (result.success) {
    console.log(`Created custom session with ID: ${result.session.sessionId}`);
    return result.session;
  }
  throw new Error(`Failed to create session: ${result.errorMessage}`);
}

// RECOMMENDED: Create a session with context synchronization
async function createSessionWithSync() {
  const contextSync = new ContextSync({
    contextId: 'your_context_id',
    path: '/mnt/persistent',
    policy: SyncPolicy.default()
  });
  
  const params: CreateSessionParams = {
    imageId: 'linux_latest',
    contextSync: [contextSync]
  };
  
  const result = await agentBay.create(params);
  if (result.success) {
    console.log(`Created session with context sync: ${result.session.sessionId}`);
    return result.session;
  }
  throw new Error(`Failed to create session: ${result.errorMessage}`);
}
```

#### Golang

```go
Create(params *CreateSessionParams) (*SessionResult, error)
```

**Parameters:**
- `params` (*CreateSessionParams, optional): Parameters for session creation. If nil, default parameters will be used.

**Returns:**
- `*SessionResult`: A result object containing the new Session instance and RequestID.
- `error`: An error if the session creation fails.

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
			Period:         30,
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

### list / List

Lists all available sessions cached in the current client instance.

#### Python

```python
list() -> List[Session]
```

**Returns:**
- `List[Session]`: A list of Session instances currently cached in the client.

**Raises:**
- `AgentBayError`: If the session listing fails.

**Example:**
```python
from agentbay import AgentBay

# Initialize the SDK
agent_bay = AgentBay(api_key="your_api_key")

# List all sessions
sessions = agent_bay.list()
print(f"Found {len(sessions)} sessions:")
for session in sessions:
    print(f"Session ID: {session.session_id}")
```

#### TypeScript

```typescript
list(): Promise<Session[]>
```

**Returns:**
- `Promise<Session[]>`: A promise that resolves to an array of Session instances.

**Throws:**
- `Error`: If the session listing fails.

**Example:**
```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

// Initialize the SDK
const agentBay = new AgentBay({ apiKey: 'your_api_key' });

// List all sessions
async function listSessions() {
  const sessions = await agentBay.list();
  console.log(`Found ${sessions.length} sessions:`);
  sessions.forEach(session => {
    console.log(`Session ID: ${session.sessionId}`);
  });
}

listSessions();
```

#### Golang

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

### list_by_labels / listByLabels / ListByLabels

Lists sessions filtered by the provided labels. It returns sessions that match all the specified labels. This method supports pagination to handle large result sets efficiently.

#### Python

```python
list_by_labels(params: Optional[Union[ListSessionParams, Dict[str, str]]] = None) -> SessionListResult
```

**Parameters:**
- `params` (ListSessionParams or Dict[str, str], optional): Parameters for filtering sessions by labels. If a dictionary is provided, it will be treated as labels. If None, all sessions will be returned.

**Returns:**
- `SessionListResult`: A result object containing the filtered sessions, pagination information, and request ID.

**Raises:**
- `AgentBayError`: If the session listing fails.

**Example:**
```python
from agentbay import AgentBay
from agentbay.session_params import ListSessionParams

# Initialize the SDK
agent_bay = AgentBay(api_key="your_api_key")

# Create pagination parameters
params = ListSessionParams(
    max_results=10,  # Maximum results per page
    next_token="",   # Token for the next page, empty for the first page
    labels={"environment": "production", "project": "demo"}  # Filter labels
)

# Get the first page of results
result = agent_bay.list_by_labels(params)

# Process the results
if result.success:
    # Print the current page sessions
    for session in result.sessions:
        print(f"Session ID: {session.session_id}")

    # Print pagination information
    print(f"Total count: {result.total_count}")
    print(f"Max results per page: {result.max_results}")
    print(f"Next token: {result.next_token}")

    # If there is a next page, retrieve it
    if result.next_token:
        params.next_token = result.next_token
        next_page_result = agent_bay.list_by_labels(params)
        # Process the next page...
```

#### TypeScript

```typescript
listByLabels(params?: ListSessionParams | Record<string, string>): Promise<SessionListResult>
```

**Parameters:**
- `params` (ListSessionParams | Record<string, string>, optional): Parameters for filtering sessions by labels. If a dictionary is provided, it will be treated as labels. If not provided, all sessions will be returned.

**Returns:**
- `Promise<SessionListResult>`: A promise that resolves to a result object containing the filtered sessions, pagination information, and request ID.

**Throws:**
- `Error`: If the session listing fails.

**Example:**
```typescript
import { AgentBay, ListSessionParams } from 'wuying-agentbay-sdk';

// Initialize the SDK
const agentBay = new AgentBay({ apiKey: 'your_api_key' });

// List sessions by labels with pagination
async function listSessionsByLabels() {
  // Create pagination parameters
  const params: ListSessionParams = {
    maxResults: 10,  // Maximum results per page
    nextToken: '',   // Token for the next page, empty for the first page
    labels: { environment: 'production', project: 'demo' }  // Filter labels
  };
  
  // Get the first page of results
  const result = await agentBay.listByLabels(params);
  
  // Process the results
  if (result.success) {
    // Print the current page sessions
    console.log(`Found ${result.sessions.length} sessions:`);
    result.sessions.forEach(session => {
      console.log(`Session ID: ${session.sessionId}`);
    });
    
    // Print pagination information
    console.log(`Total count: ${result.totalCount}`);
    console.log(`Max results per page: ${result.maxResults}`);
    console.log(`Next token: ${result.nextToken}`);
    
    // If there is a next page, retrieve it
    if (result.nextToken) {
      const nextParams = {
        ...params,
        nextToken: result.nextToken
      };
      const nextPageResult = await agentBay.listByLabels(nextParams);
      // Process the next page...
    }
  }
}

listSessionsByLabels();
```

#### Golang

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

### delete / Delete

Deletes a session from the AgentBay cloud environment.

#### Python

```python
delete(session: Session) -> DeleteResult
```

**Parameters:**
- `session` (Session): The session to delete.

**Returns:**
- `DeleteResult`: A result object containing success status, request ID, and error message if any.

**Raises:**
- `AgentBayError`: If the session deletion fails.

**Example:**
```python
from agentbay import AgentBay

# Initialize the SDK
agent_bay = AgentBay(api_key="your_api_key")

# Create a session
result = agent_bay.create()
if result.success:
    session = result.session
    print(f"Created session with ID: {session.session_id}")
    
    # Use the session for operations...
    
    # Delete the session when done
    delete_result = agent_bay.delete(session)
    if delete_result.success:
        print("Session deleted successfully")
    else:
        print(f"Failed to delete session: {delete_result.error_message}")
```

#### TypeScript

```typescript
delete(session: Session): Promise<DeleteResult>
```

**Parameters:**
- `session` (Session): The session to delete.

**Returns:**
- `Promise<DeleteResult>`: A promise that resolves to a result object containing success status, request ID, and error message if any.

**Throws:**
- `Error`: If the session deletion fails.

**Example:**
```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

// Initialize the SDK
const agentBay = new AgentBay({ apiKey: 'your_api_key' });

// Create and delete a session
async function createAndDeleteSession() {
  try {
    // Create a session
    const createResult = await agentBay.create();
    if (createResult.success) {
      const session = createResult.session;
      console.log(`Created session with ID: ${session.sessionId}`);
      
      // Use the session for operations...
      
      // Delete the session when done
      const deleteResult = await agentBay.delete(session);
      if (deleteResult.success) {
        console.log('Session deleted successfully');
      } else {
        console.log(`Failed to delete session: ${deleteResult.errorMessage}`);
      }
    }
  } catch (error) {
    console.error('Error:', error);
  }
}

createAndDeleteSession();
```

#### Golang

```go
Delete(session *Session) (*DeleteResult, error)
```

**Parameters:**
- `session` (*Session): The session to delete.

**Returns:**
- `*DeleteResult`: A result object containing success status and RequestID.
- `error`: An error if the session deletion fails.

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
	
	// Delete the session when done
	deleteResult, err := client.Delete(session)
	if err != nil {
		fmt.Printf("Error deleting session: %v\n", err)
		os.Exit(1)
	}
	
	fmt.Println("Session deleted successfully")
	fmt.Printf("Request ID: %s\n", deleteResult.RequestID)
}
```
