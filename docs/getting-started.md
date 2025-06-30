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
from agentbay import AgentBay

# Initialize the AgentBay client
api_key = "your_api_key_here"
agent_bay = AgentBay(api_key=api_key)

try:
    # Create a new session
    session_result = agent_bay.create()
    if session_result.success:
        session = session_result.session
        print(f"Session created with ID: {session.session_id}")

        # Execute a command
        result = session.command.execute_command("ls -la")
        if result.success:
            print(f"Command result: {result.data}")
        else:
            print(f"Command failed: {result.error_message}")

        # Read a file
        file_result = session.filesystem.read_file("/etc/hosts")
        if file_result.success:
            print(f"File content: {file_result.data}")
        else:
            print(f"File read failed: {file_result.error_message}")

        # Execute code
        code_result = session.command.run_code('print("Hello, World!")', "python")
        if code_result.success:
            print(f"Code execution result: {code_result.data}")
        else:
            print(f"Code execution failed: {code_result.error_message}")

        # Delete the session
        delete_result = session.delete()
        if delete_result.success:
            print("Session deleted successfully")
        else:
            print(f"Session deletion failed: {delete_result.error_message}")
    else:
        print(f"Failed to create session: {session_result.error_message}")
except Exception as e:
    print(f"An error occurred: {e}")
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
    log(`Session created with ID: ${session.sessionId}`);

    // Execute a command
    const result = await session.command.executeCommand('ls -la');
    log('Command result:', result);

    // Read a file
    const content = await session.filesystem.readFile('/etc/hosts');
    log(`File content: ${content}`);

    // Execute code
    const codeResult = await session.command.runCode('console.log("Hello, World!");', 'javascript');
    log(`Code execution result: ${codeResult}`);

    // Delete the session
    await agentBay.delete(session);
    log('Session deleted successfully');
  } catch (error) {
    logError('Error:', error);
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
	session, err := client.Create(nil)
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

    // Execute code
    codeResult, err := session.Command.RunCode(`print("Hello, World!")`, "python")
    if err != nil {
        fmt.Printf("Error executing code: %v\n", err)
        os.Exit(1)
    }
    fmt.Printf("Code execution result: %s\n", codeResult)

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
