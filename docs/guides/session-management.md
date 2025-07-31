# Session Management Documentation

This document provides comprehensive guidance on using the session management capabilities of the AgentBay SDK across all supported languages.

## Overview

Sessions are the fundamental unit of interaction with the AgentBay cloud environment. Each session represents an isolated environment where you can execute commands, manipulate files, run applications, and perform various operations in the cloud.

The session management system provides:
1. **Session Creation**: Create isolated environments with customizable parameters
2. **Session Lifecycle Management**: Manage the complete lifecycle of sessions
3. **Session Listing**: Retrieve and filter sessions based on various criteria
4. **Label Management**: Organize sessions using descriptive labels
5. **Context Synchronization**: Persist data across sessions using context synchronization

## Getting Started

### Prerequisites

To use session management, you need:
1. AgentBay SDK installed for your preferred language
2. Valid API key
3. Basic understanding of cloud computing concepts

### Creating a Session

Creating a session is the first step in using the AgentBay SDK:

```python
from agentbay import AgentBay

# Initialize the SDK
agent_bay = AgentBay(api_key="your_api_key")

# Create a session with default parameters
session_result = agent_bay.create()
if session_result.success:
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

## Creating Sessions with Custom Parameters

You can customize sessions by specifying parameters such as image ID and labels:

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

    // Create a session with custom parameters
    labels := map[string]string{
        "project":     "demo",
        "environment": "testing",
    }
    params := &agentbay.CreateSessionParams{
        ImageId: "linux_latest",
        Labels:  labels,
    }
    
    result, err := client.Create(params)
    if err != nil {
        fmt.Printf("Error creating session: %v\n", err)
        os.Exit(1)
    }
    
    session := result.Session
    fmt.Printf("Session created with ID: %s\n", session.SessionID)
}
```

## Session Context Synchronization

For data persistence across sessions, use context synchronization:

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

// Get or create a persistent context
async function createSessionWithContextSync() {
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

## Listing Sessions with Pagination

The session management system supports pagination for efficient handling of large numbers of sessions:

```python
from agentbay import AgentBay
from agentbay.session_params import ListSessionParams

# Initialize the SDK
agent_bay = AgentBay(api_key="your_api_key")

# List sessions by labels with pagination
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

    // List sessions by labels
    labels := map[string]string{
        "project": "demo",
    }
    params := &agentbay.ListSessionParams{
        MaxResults: 10,
        Labels:     labels,
    }
    
    result, err := client.ListByLabels(params)
    if err != nil {
        fmt.Printf("Error listing sessions: %v\n", err)
        os.Exit(1)
    }
    
    fmt.Printf("Found %d sessions\n", len(result.Sessions))
    for _, session := range result.Sessions {
        fmt.Printf("Session ID: %s\n", session.SessionID)
    }
    
    // Handle pagination
    if result.NextToken != "" {
        params.NextToken = result.NextToken
        nextPage, err := client.ListByLabels(params)
        if err != nil {
            fmt.Printf("Error listing next page: %v\n", err)
            os.Exit(1)
        }
        fmt.Printf("Next page has %d sessions\n", len(nextPage.Sessions))
    }
}
```

## Session Label Management

Labels help organize and categorize sessions for easier management:

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

When you're done with a session, delete it to free up resources:

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

### Deleting Sessions with Context Synchronization

To ensure all context changes are synchronized before deletion:

```python
from agentbay import AgentBay

# Initialize the SDK and create a session
agent_bay = AgentBay(api_key="your_api_key")
session_result = agent_bay.create()
session = session_result.session

# Perform operations on the session and make changes to synchronized contexts...

# Delete the session with context synchronization
delete_result = agent_bay.delete(session, sync_context=True)
# The delete() call will first trigger context.sync() to upload changes,
# then monitor all context operations until they complete (Success or Failed)
# or after maximum retry attempts (150 times with 2-second intervals)

if delete_result.success:
    print("Session deleted successfully with synchronized contexts")
else:
    # If any context operations failed, error messages will be printed automatically
    print(f"Failed to delete session: {delete_result.error_message}")
```

## Best Practices

1. **Resource Management**:
   - Always delete sessions that are no longer in use to avoid unnecessary resource consumption
   - Use session pooling for applications with high session turnover

2. **Using Labels**:
   - Add descriptive labels to sessions to make them easier to identify and manage
   - Use consistent labeling schemes across your organization

3. **Error Handling**:
   - Always check the `success` and `error_message` fields in the result objects
   - Implement retry logic for transient failures
   - Log request IDs for debugging purposes

4. **Session Reuse**:
   - If you need to perform multiple operations, try to complete them in the same session
   - Avoid creating short-lived sessions for single operations

5. **Context Synchronization**:
   - Use context synchronization for data persistence across sessions
   - Choose appropriate synchronization policies based on your use case
   - Monitor context synchronization status during session creation and deletion

6. **Performance Optimization**:
   - Use pagination when listing large numbers of sessions
   - Implement efficient filtering using labels
   - Minimize the number of synchronized contexts per session

## Limitations

1. **Session Limits**: There are limits on the number of concurrent sessions
2. **Resource Constraints**: Sessions have limits on CPU, memory, and storage
3. **Session Duration**: Sessions have maximum lifetime limits
4. **Network Dependencies**: Session operations require network connectivity

## Troubleshooting

### Common Issues

1. **Session Creation Failures**:
   - Verify your API key is valid
   - Check if you've reached session limits
   - Ensure the specified image ID is valid

2. **Context Synchronization Issues**:
   - Check network connectivity
   - Verify context IDs are valid
   - Review synchronization policy settings

3. **Pagination Problems**:
   - Ensure next tokens are properly handled
   - Check max results parameter is within allowed limits
   - Verify label filters are correctly specified

4. **Session Deletion Failures**:
   - Confirm the session exists and is active
   - Check for ongoing operations that might prevent deletion
   - Review context synchronization status

## API Reference

For detailed API documentation, see:
- [Python Session API](../api-reference/python/session.md)
- [TypeScript Session API](../api-reference/typescript/session.md)
- [Golang Session API](../api-reference/golang/session.md)
- [Python AgentBay API](../api-reference/python/agentbay.md)
- [TypeScript AgentBay API](../api-reference/typescript/agentbay.md)
- [Golang AgentBay API](../api-reference/golang/agentbay.md)