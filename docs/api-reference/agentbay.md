# AgentBay Class API Reference

The `AgentBay` class is the main entry point for interacting with the AgentBay cloud environment. It provides methods for creating, retrieving, listing, and deleting sessions.

## Constructor

### Python

```python
AgentBay(api_key=None)
```

**Parameters:**
- `api_key` (str, optional): The API key for authentication. If not provided, the SDK will look for the `AGENTBAY_API_KEY` environment variable.

### TypeScript

```typescript
new AgentBay({
  apiKey?: string;
})
```

**Parameters:**
- `apiKey` (string, optional): The API key for authentication. If not provided, the SDK will look for the `AGENTBAY_API_KEY` environment variable.

### Golang

```go
NewAgentBay(apiKey string) (*AgentBay, error)
```

**Parameters:**
- `apiKey` (string): The API key for authentication. If empty, the SDK will look for the `AGENTBAY_API_KEY` environment variable.

**Returns:**
- `*AgentBay`: A pointer to the AgentBay instance.
- `error`: An error if the initialization fails.

## Methods

### create / Create

Creates a new session in the AgentBay cloud environment.

#### Python

```python
create() -> Session
```

**Returns:**
- `Session`: A new Session instance.

**Raises:**
- `AgentBayError`: If the session creation fails.

#### TypeScript

```typescript
create(): Promise<Session>
```

**Returns:**
- `Promise<Session>`: A promise that resolves to a new Session instance.

**Throws:**
- `Error`: If the session creation fails.

#### Golang

```go
Create(params *CreateSessionParams) (*Session, error)
```

**Parameters:**
- `params` (*CreateSessionParams, optional): Parameters for session creation. If nil, default parameters will be used.

**Returns:**
- `*Session`: A pointer to the new Session instance.
- `error`: An error if the session creation fails.

### list / List

Lists all available sessions.

#### Python

```python
list() -> List[Dict[str, Any]]
```

**Returns:**
- `List[Dict[str, Any]]`: A list of dictionaries containing session information.

**Raises:**
- `AgentBayError`: If the session listing fails.

#### TypeScript

```typescript
list(): Promise<Session[]>
```

**Returns:**
- `Promise<Session[]>`: A promise that resolves to an array of Session instances.

**Throws:**
- `Error`: If the session listing fails.

#### Golang

```go
List() ([]Session, error)
```

**Returns:**
- `[]Session`: An array of Session instances.
- `error`: An error if the session listing fails.

### list_by_labels / listByLabels / ListByLabels

Lists sessions filtered by the provided labels. It returns sessions that match all the specified labels.

#### Python

```python
list_by_labels(labels: Dict[str, str]) -> List[Session]
```

**Parameters:**
- `labels` (Dict[str, str]): A dictionary of labels to filter sessions by.

**Returns:**
- `List[Session]`: A list of Session instances that match the specified labels.

**Raises:**
- `AgentBayError`: If the session listing fails.

#### TypeScript

```typescript
listByLabels(labels: Record<string, string>): Promise<Session[]>
```

**Parameters:**
- `labels` (Record<string, string>): An object of labels to filter sessions by.

**Returns:**
- `Promise<Session[]>`: A promise that resolves to an array of Session instances that match the specified labels.

**Throws:**
- `Error`: If the session listing fails.

#### Golang

```go
ListByLabels(labels map[string]string) ([]Session, error)
```

**Parameters:**
- `labels` (map[string]string): A map of labels to filter sessions by.

**Returns:**
- `[]Session`: An array of Session instances that match the specified labels.
- `error`: An error if the session listing fails.

### delete / Delete

Deletes a session by ID.

#### Python

```python
delete(session_id: str) -> bool
```

**Parameters:**
- `session_id` (str): The ID of the session to delete.

**Returns:**
- `bool`: True if the session was deleted successfully, False otherwise.

**Raises:**
- `AgentBayError`: If the session deletion fails.

#### TypeScript

```typescript
delete(sessionId: string): Promise<boolean>
```

**Parameters:**
- `sessionId` (string): The ID of the session to delete.

**Returns:**
- `Promise<boolean>`: A promise that resolves to true if the session was deleted successfully, false otherwise.

**Throws:**
- `Error`: If the session deletion fails.

#### Golang

```go
Delete(session *Session) error
```

**Parameters:**
- `session` (*Session): The session to delete.

**Returns:**
- `error`: An error if the session deletion fails.

## Context Service

The AgentBay class also provides access to the Context service, which allows you to manage persistent contexts.

### Python

```python
# Access the Context service
context = agent_bay.context.get("my-context", create_if_not_exists=True)
```

### TypeScript

```typescript
// Access the Context service
const context = await agentBay.context.get("my-context", true);
```

### Golang

```go
// Access the Context service
context, err := agentBay.Context.Get("my-context", true)
```

For more information on the Context service, see the [Contexts](../concepts/contexts.md) documentation.

## Usage Examples

### Python

```python
from wuying_agentbay import AgentBay
from wuying_agentbay.exceptions import AgentBayError
from wuying_agentbay.session_params import CreateSessionParams

def main():
    # Initialize with API key
    api_key = "your_api_key"  # Or use os.environ.get("AGENTBAY_API_KEY")
    
    try:
        agent_bay = AgentBay(api_key=api_key)
        
        # Create a session with labels
        params = CreateSessionParams()
        params.labels = {
            "purpose": "demo",
            "environment": "development"
        }
        session = agent_bay.create(params)
        print(f"Session created with ID: {session.session_id}")
        
        # List all sessions
        all_sessions = agent_bay.list()
        print(f"Found {len(all_sessions)} sessions")
        
        # List sessions by labels
        filtered_sessions = agent_bay.list_by_labels({
            "purpose": "demo"
        })
        print(f"Found {len(filtered_sessions)} matching sessions")
        
        # Delete the session
        agent_bay.delete(session)
        print("Session deleted successfully")
        
    except AgentBayError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
```

### TypeScript

```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

async function main() {
  try {
    // Initialize with API key
    const agentBay = new AgentBay({ apiKey: 'your_api_key' });
    
    // Create a session with labels
    const session = await agentBay.create({
      labels: {
        purpose: 'demo',
        environment: 'development'
      }
    });
    console.log(`Session created with ID: ${session.sessionId}`);
    
    // List all sessions
    const allSessions = agentBay.list();
    console.log(`Found ${allSessions.length} sessions`);
    
    // List sessions by labels
    const filteredSessions = await agentBay.listByLabels({
      purpose: 'demo'
    });
    console.log(`Found ${filteredSessions.length} matching sessions`);
    
    // Delete the session
    await agentBay.delete(session.sessionId);
    console.log('Session deleted successfully');
  } catch (error) {
    console.error('Error:', error);
  }
}

main();
```

### Golang

```go
package main

import (
	"fmt"
	"os"
	
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

func main() {
	// Initialize with API key
	apiKey := os.Getenv("AGENTBAY_API_KEY")
	if apiKey == "" {
		apiKey = "your_api_key" // Replace with your actual API key
	}
	
	client, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		fmt.Printf("Error initializing AgentBay client: %v\n", err)
		os.Exit(1)
	}
	
	// Create a session with labels
	params := agentbay.NewCreateSessionParams().
		WithLabels(map[string]string{
			"purpose":     "demo",
			"environment": "development",
		})
	session, err := client.Create(params)
	if err != nil {
		fmt.Printf("Error creating session: %v\n", err)
		os.Exit(1)
	}
	fmt.Printf("Session created with ID: %s\n", session.SessionID)
	
	// List all sessions
	sessions, err := client.List()
	if err != nil {
		fmt.Printf("Error listing sessions: %v\n", err)
		os.Exit(1)
	}
	fmt.Printf("Found %d sessions\n", len(sessions))
	
	// List sessions by labels
	filteredSessions, err := client.ListByLabels(map[string]string{
		"purpose": "demo",
	})
	if err != nil {
		fmt.Printf("Error listing sessions by labels: %v\n", err)
		os.Exit(1)
	}
	fmt.Printf("Found %d matching sessions\n", len(filteredSessions))
	
	// Delete the session
	err = client.Delete(session)
	if err != nil {
		fmt.Printf("Error deleting session: %v\n", err)
		os.Exit(1)
	}
	fmt.Println("Session deleted successfully")
}
```
