# Context API Reference

The Context API provides functionality for managing persistent storage contexts in the AgentBay cloud environment. Contexts allow you to persist data across sessions and reuse it in future sessions.

## Context Class

The `Context` class represents a persistent storage context in the AgentBay cloud environment.

### Properties

#### Python

```python
id  # The unique identifier of the context
name  # The name of the context
state  # The current state of the context (e.g., "available", "in-use")
created_at  # Date and time when the Context was created
last_used_at  # Date and time when the Context was last used
os_type  # The operating system type this context is bound to
```

#### TypeScript

```typescript
id  // The unique identifier of the context
name  // The name of the context
state  // The current state of the context (e.g., "available", "in-use")
createdAt  // Date and time when the Context was created
lastUsedAt  // Date and time when the Context was last used
osType  // The operating system type this context is bound to
```

#### Golang

```go
ID  // The unique identifier of the context
Name  // The name of the context
State  // The current state of the context (e.g., "available", "in-use")
CreatedAt  // Date and time when the Context was created
LastUsedAt  // Date and time when the Context was last used
OsType  // The operating system type this context is bound to
```

## ContextService Class

The `ContextService` class provides methods for managing persistent contexts in the AgentBay cloud environment.

### Methods

#### list / List

Lists all available contexts.

##### Python

```python
list() -> ContextListResult
```

**Returns:**
- `ContextListResult`: A result object containing the list of Context objects and request ID.

**Example:**
```python
from agentbay import AgentBay

# Initialize the SDK
agent_bay = AgentBay(api_key="your_api_key")

# List all contexts
result = agent_bay.context.list()
if result.success:
    print(f"Found {len(result.contexts)} contexts:")
    for context in result.contexts:
        print(f"Context ID: {context.id}, Name: {context.name}, State: {context.state}")
else:
    print("Failed to list contexts")
```

##### TypeScript

```typescript
list(): Promise<ContextListResult>
```

**Returns:**
- `Promise<ContextListResult>`: A promise that resolves to a result object containing the list of Context objects and request ID.

**Example:**
```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

// Initialize the SDK
const agentBay = new AgentBay({ apiKey: 'your_api_key' });

// List all contexts
async function listContexts() {
  try {
    const result = await agentBay.context.list();
    if (result.success) {
      console.log(`Found ${result.contexts.length} contexts:`);
      result.contexts.forEach(context => {
        console.log(`Context ID: ${context.id}, Name: ${context.name}, State: ${context.state}`);
      });
    } else {
      console.log('Failed to list contexts');
    }
  } catch (error) {
    console.error('Error:', error);
  }
}

listContexts();
```

##### Golang

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

#### get / Get

Gets a context by name. Optionally creates it if it doesn't exist.

##### Python

```python
get(name: str, create: bool = False) -> ContextResult
```

**Parameters:**
- `name` (str): The name of the context to get.
- `create` (bool, optional): Whether to create the context if it doesn't exist. Defaults to False.

**Returns:**
- `ContextResult`: A result object containing the Context object and request ID.

**Example:**
```python
from agentbay import AgentBay

# Initialize the SDK
agent_bay = AgentBay(api_key="your_api_key")

# Get a context, creating it if it doesn't exist
result = agent_bay.context.get("my-persistent-context", create=True)
if result.success:
    context = result.context
    print(f"Context ID: {context.id}, Name: {context.name}, State: {context.state}")
else:
    print(f"Failed to get context: {result.error_message}")
```

##### TypeScript

```typescript
get(name: string, create?: boolean): Promise<ContextResult>
```

**Parameters:**
- `name` (string): The name of the context to get.
- `create` (boolean, optional): Whether to create the context if it doesn't exist. Defaults to false.

**Returns:**
- `Promise<ContextResult>`: A promise that resolves to a result object containing the Context object and request ID.

**Example:**
```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

// Initialize the SDK
const agentBay = new AgentBay({ apiKey: 'your_api_key' });

// Get a context, creating it if it doesn't exist
async function getOrCreateContext() {
  try {
    const result = await agentBay.context.get('my-persistent-context', true);
    if (result.success) {
      const context = result.context;
      console.log(`Context ID: ${context.id}, Name: ${context.name}, State: ${context.state}`);
    } else {
      console.log(`Failed to get context: ${result.errorMessage}`);
    }
  } catch (error) {
    console.error('Error:', error);
  }
}

getOrCreateContext();
```

##### Golang

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

#### create / Create

Creates a new context.

##### Python

```python
create(name: str) -> ContextResult
```

**Parameters:**
- `name` (str): The name of the context to create.

**Returns:**
- `ContextResult`: A result object containing the created Context object and request ID.

**Example:**
```python
from agentbay import AgentBay

# Initialize the SDK
agent_bay = AgentBay(api_key="your_api_key")

# Create a new context
result = agent_bay.context.create("my-new-context")
if result.success:
    context = result.context
    print(f"Created context with ID: {context.id}, Name: {context.name}")
else:
    print(f"Failed to create context: {result.error_message}")
```

##### TypeScript

```typescript
create(name: string): Promise<ContextResult>
```

**Parameters:**
- `name` (string): The name of the context to create.

**Returns:**
- `Promise<ContextResult>`: A promise that resolves to a result object containing the created Context object and request ID.

**Example:**
```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

// Initialize the SDK
const agentBay = new AgentBay({ apiKey: 'your_api_key' });

// Create a new context
async function createContext() {
  try {
    const result = await agentBay.context.create('my-new-context');
    if (result.success) {
      const context = result.context;
      console.log(`Created context with ID: ${context.id}, Name: ${context.name}`);
    } else {
      console.log(`Failed to create context: ${result.errorMessage}`);
    }
  } catch (error) {
    console.error('Error:', error);
  }
}

createContext();
```

##### Golang

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

#### update / Update

Updates an existing context.

##### Python

```python
update(context: Context) -> OperationResult
```

**Parameters:**
- `context` (Context): The context object to update.

**Returns:**
- `OperationResult`: A result object containing success status, request ID, and error message if any.

**Example:**
```python
from agentbay import AgentBay

# Initialize the SDK
agent_bay = AgentBay(api_key="your_api_key")

# Get an existing context
result = agent_bay.context.get("my-context")
if result.success:
    context = result.context
    
    # Update the context name
    context.name = "my-updated-context"
    
    # Save the changes
    update_result = agent_bay.context.update(context)
    if update_result.success:
        print(f"Context updated successfully, request ID: {update_result.request_id}")
    else:
        print(f"Failed to update context: {update_result.error_message}")
else:
    print(f"Failed to get context: {result.error_message}")
```

##### TypeScript

```typescript
update(context: Context): Promise<OperationResult>
```

**Parameters:**
- `context` (Context): The context object to update.

**Returns:**
- `Promise<OperationResult>`: A promise that resolves to a result object containing success status, request ID, and error message if any.

**Example:**
```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

// Initialize the SDK
const agentBay = new AgentBay({ apiKey: 'your_api_key' });

// Update an existing context
async function updateContext() {
  try {
    // Get an existing context
    const result = await agentBay.context.get('my-context');
    if (result.success) {
      const context = result.context;
      
      // Update the context name
      context.name = 'my-updated-context';
      
      // Save the changes
      const updateResult = await agentBay.context.update(context);
      if (updateResult.success) {
        console.log(`Context updated successfully, request ID: ${updateResult.requestId}`);
      } else {
        console.log(`Failed to update context: ${updateResult.errorMessage}`);
      }
    } else {
      console.log(`Failed to get context: ${result.errorMessage}`);
    }
  } catch (error) {
    console.error('Error:', error);
  }
}

updateContext();
```

##### Golang

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

#### delete / Delete

Deletes a context.

##### Python

```python
delete(context: Context) -> OperationResult
```

**Parameters:**
- `context` (Context): The context object to delete.

**Returns:**
- `OperationResult`: A result object containing success status, request ID, and error message if any.

**Example:**
```python
from agentbay import AgentBay

# Initialize the SDK
agent_bay = AgentBay(api_key="your_api_key")

# Get an existing context
result = agent_bay.context.get("my-context")
if result.success:
    context = result.context
    
    # Delete the context
    delete_result = agent_bay.context.delete(context)
    if delete_result.success:
        print(f"Context deleted successfully, request ID: {delete_result.request_id}")
    else:
        print(f"Failed to delete context: {delete_result.error_message}")
else:
    print(f"Failed to get context: {result.error_message}")
```

##### TypeScript

```typescript
delete(context: Context): Promise<OperationResult>
```

**Parameters:**
- `context` (Context): The context object to delete.

**Returns:**
- `Promise<OperationResult>`: A promise that resolves to a result object containing success status, request ID, and error message if any.

**Example:**
```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

// Initialize the SDK
const agentBay = new AgentBay({ apiKey: 'your_api_key' });

// Delete an existing context
async function deleteContext() {
  try {
    // Get an existing context
    const result = await agentBay.context.get('my-context');
    if (result.success) {
      const context = result.context;
      
      // Delete the context
      const deleteResult = await agentBay.context.delete(context);
      if (deleteResult.success) {
        console.log(`Context deleted successfully, request ID: ${deleteResult.requestId}`);
      } else {
        console.log(`Failed to delete context: ${deleteResult.errorMessage}`);
      }
    } else {
      console.log(`Failed to get context: ${result.errorMessage}`);
    }
  } catch (error) {
    console.error('Error:', error);
  }
}

deleteContext();
```

##### Golang

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

## ContextSync Class

The `ContextSync` class defines the configuration for synchronizing a context with a session. It is used in the `CreateSessionParams` to specify which contexts should be mounted in the session and how they should be synchronized.

### Properties

#### Python

```python
context_id  # The ID of the context to synchronize
path  # The path where the context should be mounted
policy  # The synchronization policy (optional)
```

#### TypeScript

```typescript
contextId  # The ID of the context to synchronize
path  # The path where the context should be mounted
policy  # The synchronization policy (optional)
```

#### Golang

```go
ContextID  # The ID of the context to synchronize
Path  # The path where the context should be mounted
Policy  # The synchronization policy (optional)
```

### Constructor

#### Python

```python
ContextSync(context_id: str, path: str, policy: Optional[SyncPolicy] = None)
```

**Parameters:**
- `context_id` (str): The ID of the context to synchronize.
- `path` (str): The path where the context should be mounted.
- `policy` (SyncPolicy, optional): The synchronization policy. If None, default policy is used.

**Example:**
```python
from agentbay import AgentBay
from agentbay.context_sync import ContextSync, SyncPolicy
from agentbay.session_params import CreateSessionParams

# Initialize the SDK
agent_bay = AgentBay(api_key="your_api_key")

# Get or create a context
context_result = agent_bay.context.get("my-context", create=True)
if context_result.success:
    # Create a context sync configuration
    context_sync = ContextSync(
        context_id=context_result.context.id,
        path="/mnt/persistent",
        policy=SyncPolicy.default()
    )
    
    # Create a session with context synchronization
    params = CreateSessionParams(
        context_syncs=[context_sync]
    )
    
    session_result = agent_bay.create(params)
    if session_result.success:
        print(f"Created session with ID: {session_result.session.session_id}")
    else:
        print(f"Failed to create session: {session_result.error_message}")
else:
    print(f"Failed to get context: {context_result.error_message}")
```

#### TypeScript

```typescript
new ContextSync(options: {
  contextId: string;
  path: string;
  policy?: SyncPolicy;
})
```

**Parameters:**
- `options` (object): An object containing:
  - `contextId` (string): The ID of the context to synchronize.
  - `path` (string): The path where the context should be mounted.
  - `policy` (SyncPolicy, optional): The synchronization policy. If not provided, default policy is used.

**Example:**
```typescript
import { AgentBay, CreateSessionParams } from 'wuying-agentbay-sdk';
import { ContextSync, SyncPolicy } from 'wuying-agentbay-sdk/context-sync';

// Initialize the SDK
const agentBay = new AgentBay({ apiKey: 'your_api_key' });

// Get or create a context and create a session with context synchronization
async function createSessionWithContextSync() {
  try {
    // Get or create a context
    const contextResult = await agentBay.context.get('my-context', true);
    if (contextResult.success) {
      // Create a context sync configuration
      const contextSync = new ContextSync({
        contextId: contextResult.context.id,
        path: '/mnt/persistent',
        policy: SyncPolicy.default()
      });
      
      // Create a session with context synchronization
      const params: CreateSessionParams = {
        contextSyncs: [contextSync]
      };
      
      const sessionResult = await agentBay.create(params);
      if (sessionResult.success) {
        console.log(`Created session with ID: ${sessionResult.session.sessionId}`);
      } else {
        console.log(`Failed to create session: ${sessionResult.errorMessage}`);
      }
    } else {
      console.log(`Failed to get context: ${contextResult.errorMessage}`);
    }
  } catch (error) {
    console.error('Error:', error);
  }
}

createSessionWithContextSync();
```

#### Golang

```go
NewContextSync(contextID string, path string, policy *SyncPolicy) *ContextSync
```

**Parameters:**
- `contextID` (string): The ID of the context to synchronize.
- `path` (string): The path where the context should be mounted.
- `policy` (*SyncPolicy, optional): The synchronization policy. If nil, default policy is used.

**Returns:**
- `*ContextSync`: A pointer to the new ContextSync instance.

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

	// Get or create a context
	contextResult, err := client.Context.Get("my-context", true)
	if err != nil {
		fmt.Printf("Error getting context: %v\n", err)
		os.Exit(1)
	}

	// Create a sync policy
	policy := agentbay.NewSyncPolicy()
	
	// Create a context sync configuration
	contextSync := agentbay.NewContextSync(
		contextResult.Context.ID,
		"/mnt/persistent",
		policy,
	)
	
	// Create a session with context synchronization
	params := &agentbay.CreateSessionParams{
		ContextSyncs: []*agentbay.ContextSync{contextSync},
	}
	
	sessionResult, err := client.Create(params)
	if err != nil {
		fmt.Printf("Error creating session: %v\n", err)
		os.Exit(1)
	}
	
	fmt.Printf("Created session with ID: %s\n", sessionResult.Session.SessionID)
}
```

## SyncPolicy Class

The `SyncPolicy` class defines the synchronization policy for context synchronization.

### Properties

#### Python

```python
upload_policy  # The upload policy
download_policy  # The download policy
delete_policy  # The delete policy
bw_list  # The black and white list
sync_paths  # The paths to synchronize
```

#### TypeScript

```typescript
uploadPolicy  # The upload policy
downloadPolicy  # The download policy
deletePolicy  # The delete policy
bwList  # The black and white list
syncPaths  # The paths to synchronize
```

#### Golang

```go
UploadPolicy  # The upload policy
DownloadPolicy  # The download policy
DeletePolicy  # The delete policy
BWList  # The black and white list
SyncPaths  # The paths to synchronize
```

### Class Methods

#### default / Default

Creates a new sync policy with default values.

##### Python

```python
@classmethod
default(cls) -> SyncPolicy
```

**Returns:**
- `SyncPolicy`: A new sync policy with default values.

**Example:**
```python
from agentbay.context_sync import SyncPolicy

# Create a sync policy with default values
policy = SyncPolicy.default()
```

##### TypeScript

```typescript
static default(): SyncPolicy
```

**Returns:**
- `SyncPolicy`: A new sync policy with default values.

**Example:**
```typescript
import { SyncPolicy } from 'wuying-agentbay-sdk/context-sync';

// Create a sync policy with default values
const policy = SyncPolicy.default();
```

##### Golang

```go
NewSyncPolicy() *SyncPolicy
```

**Returns:**
- `*SyncPolicy`: A pointer to a new SyncPolicy instance with default values.

**Example:**
```go
import "github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"

// Create a sync policy with default values
policy := agentbay.NewSyncPolicy()
``` 