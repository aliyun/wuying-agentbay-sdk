# ContextManager API Reference

The `ContextManager` class provides functionality for managing contexts within a session. It enables you to interact with the contexts that are synchronized to the session, including reading and writing data, and managing file operations.

## Properties

### Python

```python
session  # The Session instance that this ContextManager belongs to
```

### TypeScript

```typescript
session  # The Session instance that this ContextManager belongs to
```

### Golang

```go
Session  # The Session instance that this ContextManager belongs to
```

## Methods

### sync_context / syncContext / SyncContext

Synchronizes a context with the session.

#### Python

```python
sync_context(context_id: str, path: str, policy: Optional[SyncPolicy] = None) -> OperationResult
```

**Parameters:**
- `context_id` (str): The ID of the context to synchronize.
- `path` (str): The path where the context should be mounted.
- `policy` (SyncPolicy, optional): The synchronization policy. If None, default policy is used.

**Returns:**
- `OperationResult`: A result object containing success status, request ID, and error message if any.

**Example:**
```python
from agentbay import AgentBay
from agentbay.context_sync import SyncPolicy

# Initialize the SDK
agent_bay = AgentBay(api_key="your_api_key")

# Create a session
result = agent_bay.create()
if result.success:
    session = result.session
    
    # Get or create a context
    context_result = agent_bay.context.get("my-context", create=True)
    if context_result.success:
        # Synchronize the context with the session
        sync_result = session.context.sync_context(
            context_id=context_result.context.id,
            path="/mnt/persistent",
            policy=SyncPolicy.default()
        )
        
        if sync_result.success:
            print(f"Context synchronized successfully, request ID: {sync_result.request_id}")
        else:
            print(f"Failed to synchronize context: {sync_result.error_message}")
    else:
        print(f"Failed to get context: {context_result.error_message}")
else:
    print(f"Failed to create session: {result.error_message}")
```

#### TypeScript

```typescript
syncContext(contextId: string, path: string, policy?: SyncPolicy): Promise<OperationResult>
```

**Parameters:**
- `contextId` (string): The ID of the context to synchronize.
- `path` (string): The path where the context should be mounted.
- `policy` (SyncPolicy, optional): The synchronization policy. If not provided, default policy is used.

**Returns:**
- `Promise<OperationResult>`: A promise that resolves to a result object containing success status, request ID, and error message if any.

**Example:**
```typescript
import { AgentBay } from 'wuying-agentbay-sdk';
import { SyncPolicy } from 'wuying-agentbay-sdk/context-sync';

// Initialize the SDK
const agentBay = new AgentBay({ apiKey: 'your_api_key' });

// Create a session and synchronize a context
async function syncContextInSession() {
  try {
    // Create a session
    const result = await agentBay.create();
    if (result.success) {
      const session = result.session;
      
      // Get or create a context
      const contextResult = await agentBay.context.get('my-context', true);
      if (contextResult.success) {
        // Synchronize the context with the session
        const syncResult = await session.context.syncContext(
          contextResult.context.id,
          '/mnt/persistent',
          SyncPolicy.default()
        );
        
        if (syncResult.success) {
          console.log(`Context synchronized successfully, request ID: ${syncResult.requestId}`);
        } else {
          console.log(`Failed to synchronize context: ${syncResult.errorMessage}`);
        }
      } else {
        console.log(`Failed to get context: ${contextResult.errorMessage}`);
      }
    } else {
      console.log(`Failed to create session: ${result.errorMessage}`);
    }
  } catch (error) {
    console.error('Error:', error);
  }
}

syncContextInSession();
```

#### Golang

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

### get_info / getInfo / GetInfo

Gets information about a context that is synchronized to the session.

#### Python

```python
get_info(path: str) -> OperationResult
```

**Parameters:**
- `path` (str): The path where the context is mounted.

**Returns:**
- `OperationResult`: A result object containing the context information as data, success status, request ID, and error message if any.

**Example:**
```python
from agentbay import AgentBay

# Initialize the SDK
agent_bay = AgentBay(api_key="your_api_key")

# Create a session with a synchronized context
# ... (assume context is synchronized to '/mnt/persistent')

# Get information about the synchronized context
info_result = session.context.get_info("/mnt/persistent")
if info_result.success:
    context_info = info_result.data
    print(f"Context Information:")
    print(f"  Context ID: {context_info.context_id}")
    print(f"  Path: {context_info.path}")
    print(f"  State: {context_info.state}")
    print(f"Request ID: {info_result.request_id}")
else:
    print(f"Failed to get context info: {info_result.error_message}")
```

#### TypeScript

```typescript
getInfo(path: string): Promise<OperationResult>
```

**Parameters:**
- `path` (string): The path where the context is mounted.

**Returns:**
- `Promise<OperationResult>`: A promise that resolves to a result object containing the context information as data, success status, request ID, and error message if any.

**Example:**
```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

// Initialize the SDK
const agentBay = new AgentBay({ apiKey: 'your_api_key' });

// Create a session with a synchronized context
// ... (assume context is synchronized to '/mnt/persistent')

// Get information about the synchronized context
async function getContextInfo() {
  try {
    const infoResult = await session.context.getInfo('/mnt/persistent');
    if (infoResult.success) {
      const contextInfo = infoResult.data;
      console.log('Context Information:');
      console.log(`  Context ID: ${contextInfo.contextId}`);
      console.log(`  Path: ${contextInfo.path}`);
      console.log(`  State: ${contextInfo.state}`);
      console.log(`Request ID: ${infoResult.requestId}`);
    } else {
      console.log(`Failed to get context info: ${infoResult.errorMessage}`);
    }
  } catch (error) {
    console.error('Error:', error);
  }
}

getContextInfo();
```

#### Golang

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

### delete_context / deleteContext / DeleteContext

Deletes a context that is synchronized to the session.

#### Python

```python
delete_context(path: str) -> OperationResult
```

**Parameters:**
- `path` (str): The path where the context is mounted.

**Returns:**
- `OperationResult`: A result object containing success status, request ID, and error message if any.

**Example:**
```python
from agentbay import AgentBay

# Initialize the SDK
agent_bay = AgentBay(api_key="your_api_key")

# Create a session with a synchronized context
# ... (assume context is synchronized to '/mnt/persistent')

# Delete the synchronized context
delete_result = session.context.delete_context("/mnt/persistent")
if delete_result.success:
    print(f"Context deleted successfully, request ID: {delete_result.request_id}")
else:
    print(f"Failed to delete context: {delete_result.error_message}")
```

#### TypeScript

```typescript
deleteContext(path: string): Promise<OperationResult>
```

**Parameters:**
- `path` (string): The path where the context is mounted.

**Returns:**
- `Promise<OperationResult>`: A promise that resolves to a result object containing success status, request ID, and error message if any.

**Example:**
```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

// Initialize the SDK
const agentBay = new AgentBay({ apiKey: 'your_api_key' });

// Create a session with a synchronized context
// ... (assume context is synchronized to '/mnt/persistent')

// Delete the synchronized context
async function deleteContext() {
  try {
    const deleteResult = await session.context.deleteContext('/mnt/persistent');
    if (deleteResult.success) {
      console.log(`Context deleted successfully, request ID: ${deleteResult.requestId}`);
    } else {
      console.log(`Failed to delete context: ${deleteResult.errorMessage}`);
    }
  } catch (error) {
    console.error('Error:', error);
  }
}

deleteContext();
```

#### Golang

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

### list / List

Lists all contexts that are synchronized to the session.

#### Python

```python
list() -> OperationResult
```

**Returns:**
- `OperationResult`: A result object containing the list of synchronized contexts as data, success status, request ID, and error message if any.

**Example:**
```python
from agentbay import AgentBay

# Initialize the SDK
agent_bay = AgentBay(api_key="your_api_key")

# Create a session with synchronized contexts
# ...

# List all synchronized contexts
list_result = session.context.list()
if list_result.success:
    contexts = list_result.data
    print(f"Found {len(contexts)} synchronized contexts:")
    for context in contexts:
        print(f"  Context ID: {context.context_id}, Path: {context.path}, State: {context.state}")
    print(f"Request ID: {list_result.request_id}")
else:
    print(f"Failed to list contexts: {list_result.error_message}")
```

#### TypeScript

```typescript
list(): Promise<OperationResult>
```

**Returns:**
- `Promise<OperationResult>`: A promise that resolves to a result object containing the list of synchronized contexts as data, success status, request ID, and error message if any.

**Example:**
```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

// Initialize the SDK
const agentBay = new AgentBay({ apiKey: 'your_api_key' });

// Create a session with synchronized contexts
// ...

// List all synchronized contexts
async function listSynchronizedContexts() {
  try {
    const listResult = await session.context.list();
    if (listResult.success) {
      const contexts = listResult.data;
      console.log(`Found ${contexts.length} synchronized contexts:`);
      contexts.forEach(context => {
        console.log(`  Context ID: ${context.contextId}, Path: ${context.path}, State: ${context.state}`);
      });
      console.log(`Request ID: ${listResult.requestId}`);
    } else {
      console.log(`Failed to list contexts: ${listResult.errorMessage}`);
    }
  } catch (error) {
    console.error('Error:', error);
  }
}

listSynchronizedContexts();
```

#### Golang

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