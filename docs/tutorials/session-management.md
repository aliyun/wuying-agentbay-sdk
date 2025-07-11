# Session Management Tutorial

Sessions are the basic unit of interaction with the AgentBay cloud environment. Each session represents an isolated environment where you can execute commands, manipulate files, and run applications. This tutorial will cover how to create, manage, and delete sessions.

## Creating Sessions

Creating a session is the first step in using the AgentBay SDK. You can create a session with default parameters or customize the session attributes.

### Creating a Session with Default Parameters

```python
from agentbay import AgentBay

# Initialize the SDK
agent_bay = AgentBay(api_key="your_api_key")

# Create a session
session_result = agent_bay.create()
session = session_result.session

print(f"Session created with ID: {session.session_id}")
```

```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

// Initialize the SDK
const agentBay = new AgentBay({ apiKey: 'your_api_key' });

// Create a session
async function createSession() {
  const createResponse = await agentBay.create();
  const session = createResponse.session;
  console.log(`Session created with ID: ${session.sessionId}`);
  return session;
}
```

```go
package main

import (
	"fmt"
	"os"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

func main() {
  // Initialize the SDK
  client, err := agentbay.NewAgentBay("your_api_key")
  if err != nil {
    fmt.Printf("Error initializing AgentBay client: %v\n", err)
    os.Exit(1)
  }

  // Create a session
  result, err := client.Create(nil)
  if err != nil {
    fmt.Printf("Error creating session: %v\n", err)
    os.Exit(1)
  }

  session := result.Session
  fmt.Printf("Session created with ID: %s\n", session.SessionID)
}
```

### Creating a Session with Custom Parameters

You can customize a session by specifying parameters. Common parameters include:

- `image_id`: Specify the image to use for the session
- `labels`: Add labels to the session for easier management
- `context_id`: Associate a persistent context (DEPRECATED, use context synchronization instead)

```python
from agentbay import AgentBay
from agentbay.session_params import CreateSessionParams

# Initialize the SDK
agent_bay = AgentBay(api_key="your_api_key")

# Create a session with custom parameters
params = CreateSessionParams(
    image_id="linux_latest",
    labels={"project": "demo", "environment": "testing"}
)
session_result = agent_bay.create(params)
session = session_result.session

print(f"Session created with ID: {session.session_id}")
```

```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

// Initialize the SDK
const agentBay = new AgentBay({ apiKey: 'your_api_key' });

// Create a session with custom parameters
async function createCustomSession() {
  const createResponse = await agentBay.create({
    imageId: 'linux_latest',
    labels: { project: 'demo', environment: 'testing' }
  });
  
  const session = createResponse.session;
  console.log(`Session created with ID: ${session.sessionId}`);
  return session;
}
```

## Using Data Persistence with Context Synchronization

For long-term data persistence across sessions, use context synchronization. This feature allows you to mount persistent contexts at specific paths in your session with fine-grained control over synchronization policies.

### Creating a Session with Context Synchronization

```python
from agentbay import AgentBay
from agentbay.context_sync import ContextSync, SyncPolicy
from agentbay.session_params import CreateSessionParams

# Initialize the SDK
agent_bay = AgentBay(api_key="your_api_key")

# Get or create a persistent context
context_result = agent_bay.context.get("my-persistent-context", create=True)

if context_result.success:
    # Configure context synchronization
    context_sync = ContextSync.new(
        context_id=context_result.context.id,
        path="/mnt/data",  # Mount path in the session
        policy=SyncPolicy.default()
    )
    
    # Create a session with context synchronization
    params = CreateSessionParams(context_syncs=[context_sync])
    session_result = agent_bay.create(params)
    session = session_result.session
    
    print(f"Session created with ID: {session.session_id} and synchronized context at /mnt/data")
```

```typescript
import { AgentBay, ContextSync, SyncPolicy } from 'wuying-agentbay-sdk';

// Initialize the SDK
const agentBay = new AgentBay({ apiKey: 'your_api_key' });

async function createSessionWithContextSync() {
  // Get or create a persistent context
  const contextResult = await agentBay.context.get('my-persistent-context', true);
  
  if (contextResult.success) {
    // Configure context synchronization
    const contextSync = new ContextSync({
      contextId: contextResult.context.id,
      path: '/mnt/data',  // Mount path in the session
      policy: SyncPolicy.default()
    });
    
    // Create a session with context synchronization
    const sessionResult = await agentBay.create({
      contextSync: [contextSync]
    });
    
    const session = sessionResult.session;
    console.log(`Session created with ID: ${session.sessionId} and synchronized context at /mnt/data`);
    return session;
  }
}
```

```go
package main

import (
    "fmt"
    "github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

func main() {
    // Initialize the SDK
    client, _ := agentbay.NewAgentBay("your_api_key", nil)
    
    // Get or create a persistent context
    contextResult, _ := client.Context.Get("my-persistent-context", true)
    
    // Configure context synchronization
    policy := agentbay.NewSyncPolicy()
    contextSync := agentbay.NewContextSync(
        contextResult.Context.ID,
        "/mnt/data",  // Mount path in the session
        policy,
    )
    
    // Create a session with context synchronization
    params := agentbay.NewCreateSessionParams().
        AddContextSyncConfig(contextSync)
    
    sessionResult, _ := client.Create(params)
    session := sessionResult.Session
    
    fmt.Printf("Session created with ID: %s and synchronized context at /mnt/data\n", session.SessionID)
}
```

### Using Multiple Synchronized Contexts

You can synchronize multiple contexts with different mount paths and policies:

```python
from agentbay import AgentBay
from agentbay.context_sync import ContextSync, SyncPolicy
from agentbay.session_params import CreateSessionParams

# Initialize the SDK
agent_bay = AgentBay(api_key="your_api_key")

# Get or create persistent contexts
code_context = agent_bay.context.get("project-code", create=True).context
data_context = agent_bay.context.get("project-data", create=True).context

# Configure context synchronizations
code_sync = ContextSync.new(
    context_id=code_context.id,
    path="/app/code",
    policy=SyncPolicy.default()
)

data_sync = ContextSync.new(
    context_id=data_context.id,
    path="/app/data",
    policy=SyncPolicy.default()
)

# Create a session with multiple context synchronizations
params = CreateSessionParams(context_syncs=[code_sync, data_sync])
session_result = agent_bay.create(params)
```

## Listing Sessions

You can list all sessions or filter sessions by labels.

### Listing All Sessions

```python
from agentbay import AgentBay

# Initialize the SDK
agent_bay = AgentBay(api_key="your_api_key")

# List all sessions
sessions = agent_bay.list()
for session in sessions:
    print(f"Session ID: {session.session_id}")
```

### Listing Sessions by Labels

```python
from agentbay import AgentBay
from agentbay.session_params import ListSessionParams

# Initialize the SDK
agent_bay = AgentBay(api_key="your_api_key")

# List sessions by labels
params = ListSessionParams(
    labels={"project": "demo"},
    max_results=10
)
result = agent_bay.list_by_labels(params)

print(f"Found {len(result.sessions)} sessions")
for session in result.sessions:
    print(f"Session ID: {session.session_id}")

# Handle pagination
if result.next_token:
    params.next_token = result.next_token
    next_page = agent_bay.list_by_labels(params)
    print(f"Next page has {len(next_page.sessions)} sessions")
```

```typescript
import { AgentBay, ListSessionParams } from 'wuying-agentbay-sdk';

// Initialize the SDK
const agentBay = new AgentBay({ apiKey: 'your_api_key' });

// List sessions by labels
async function listSessionsByLabels() {
  const params: ListSessionParams = {
    labels: { project: 'demo' },
    maxResults: 10
  };
  
  const result = await agentBay.listByLabels(params);
  console.log(`Found ${result.sessions.length} sessions`);
  
  // Handle pagination
  if (result.nextToken) {
    const nextParams = {
      ...params,
      nextToken: result.nextToken
    };
    const nextPage = await agentBay.listByLabels(nextParams);
    console.log(`Next page has ${nextPage.sessions.length} sessions`);
  }
}
```

## Session Label Management

Labels can be used to categorize and organize sessions. You can set labels for a session and retrieve existing labels.

### Setting Session Labels

```python
from agentbay import AgentBay

# Initialize the SDK and create a session
agent_bay = AgentBay(api_key="your_api_key")
session_result = agent_bay.create()
session = session_result.session

# Set labels
labels = {"project": "demo", "environment": "testing"}
result = session.set_labels(labels)

if result.success:
    print("Labels set successfully")
else:
    print(f"Failed to set labels: {result.error_message}")
```

### Getting Session Labels

```python
from agentbay import AgentBay

# Initialize the SDK and create a session
agent_bay = AgentBay(api_key="your_api_key")
session_result = agent_bay.create()
session = session_result.session

# Get labels
result = session.get_labels()

if result.success:
    print("Session labels:")
    for key, value in result.data.items():
        print(f"  {key}: {value}")
else:
    print(f"Failed to get labels: {result.error_message}")
```

## Deleting Sessions

When you're done using a session, you should delete it to free up resources.

```python
from agentbay import AgentBay

# Initialize the SDK and create a session
agent_bay = AgentBay(api_key="your_api_key")
session_result = agent_bay.create()
session = session_result.session

# Perform operations on the session...

# Delete the session
delete_result = agent_bay.delete(session)
if delete_result.success:
    print("Session deleted successfully")
else:
    print(f"Failed to delete session: {delete_result.error_message}")
```

```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

// Initialize the SDK
const agentBay = new AgentBay({ apiKey: 'your_api_key' });

async function sessionLifecycle() {
  try {
    // Create a session
    const createResponse = await agentBay.create();
    const session = createResponse.session;
    
    // Perform operations on the session...
    
    // Delete the session
    const deleteResponse = await agentBay.delete(session);
    console.log('Session deleted successfully');
  } catch (error) {
    console.error('Error:', error);
  }
}
```

```go
package main

import (
	"fmt"
	"os"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

func main() {
  // Initialize the SDK
  client, err := agentbay.NewAgentBay("your_api_key")
  if err != nil {
    fmt.Printf("Error initializing AgentBay client: %v\n", err)
    os.Exit(1)
  }

  // Create a session
  result, err := client.Create(nil)
  if err != nil {
    fmt.Printf("Error creating session: %v\n", err)
    os.Exit(1)
  }

  session := result.Session
  
  // Perform operations on the session...
  
  // Delete the session
  _, err = client.Delete(session)
  if err != nil {
    fmt.Printf("Error deleting session: %v\n", err)
    os.Exit(1)
  }
  
  fmt.Println("Session deleted successfully")
}
```

## Best Practices

1. **Resource Management**: Always delete sessions that are no longer in use to avoid unnecessary resource consumption.
2. **Using Labels**: Add descriptive labels to sessions to make them easier to identify and manage.
3. **Error Handling**: Always check the `success` and `error_message` fields in the result objects to ensure operations completed successfully.
4. **Session Reuse**: If you need to perform multiple operations, try to complete them in the same session instead of creating a new session for each operation.

## Related Resources

- [API Reference: AgentBay](../api-reference/agentbay.md)
- [API Reference: Session](../api-reference/session.md)
- [Examples: Session Creation](../examples/python/session-creation) 