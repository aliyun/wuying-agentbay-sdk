# Getting Started with Wuying AgentBay SDK

This guide will help you get started with the Wuying AgentBay SDK, including installation, authentication, and basic usage.

## Installation

### Python

```bash
pip install wuying-agentbay-sdk
```

### TypeScript

```bash
npm install wuying-agentbay-sdk
```

### Golang

```bash
go get github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay
```

## Authentication

Authentication is done using an API key, which can be provided in several ways:

1. As a parameter when initializing the SDK
2. Through environment variables (`AGENTBAY_API_KEY`)

For more details on authentication, see the [Authentication Guide](guides/authentication.md).

## Basic Usage

### Python

```python
from wuying_agentbay import AgentBay

# Initialize the AgentBay client
api_key = "your_api_key_here"
agent_bay = AgentBay(api_key=api_key)

# Create a new session
session = agent_bay.create()
print(f"Session created with ID: {session.session_id}")

# Execute a command
result = session.command.execute_command("ls -la")
print(f"Command result: {result}")

# Read a file
content = session.filesystem.read_file("/etc/hosts")
print(f"File content: {content}")

# Delete the session
agent_bay.delete(session.session_id)
print("Session deleted successfully")
```

### TypeScript

```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

async function main() {
  // Initialize the AgentBay client
  const apiKey = 'your_api_key_here';
  const agentBay = new AgentBay({ apiKey });

  try {
    // Create a new session
    const session = await agentBay.create();
    console.log(`Session created with ID: ${session.sessionId}`);

    // Execute a command
    const result = await session.command.execute_command('ls -la');
    console.log('Command result:', result);

    // Read a file
    const content = await session.filesystem.read_file('/etc/hosts');
    console.log(`File content: ${content}`);

    // Delete the session
    await agentBay.delete(session);
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
	// Initialize the AgentBay client
	apiKey := "your_api_key_here"
	client, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		fmt.Printf("Error initializing AgentBay client: %v\n", err)
		os.Exit(1)
	}

	// Create a new session
	session, err := client.Create()
	if err != nil {
		fmt.Printf("Error creating session: %v\n", err)
		os.Exit(1)
	}
	fmt.Printf("Session created with ID: %s\n", session.SessionID)

    // Execute a command
    result, err := session.Command.ExecuteCommand("ls -la")
    if err != nil {
        fmt.Printf("Error executing command: %v\n", err)
        os.Exit(1)
    }
    fmt.Printf("Command result: %v\n", result)

    // Read a file
    content, err := session.FileSystem.ReadFile("/etc/hosts")
    if err != nil {
        fmt.Printf("Error reading file: %v\n", err)
        os.Exit(1)
    }
    fmt.Printf("File content: %s\n", content)

	// Delete the session
	err = client.Delete(session)
	if err != nil {
		fmt.Printf("Error deleting session: %v\n", err)
		os.Exit(1)
	}
	fmt.Println("Session deleted successfully")
}
```

## Next Steps

Now that you've learned the basics of using the Wuying AgentBay SDK, you can explore more advanced features:

- [Sessions](concepts/sessions.md): Learn more about sessions in the AgentBay cloud environment.
- [Contexts](concepts/contexts.md): Learn about persistent storage contexts.
- [Applications](concepts/applications.md): Learn about managing applications and windows.
- [API Reference](api-reference/agentbay.md): Explore the complete API reference.
