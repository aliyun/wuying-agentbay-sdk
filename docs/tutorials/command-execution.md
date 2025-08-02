# Command Execution Tutorial

AgentBay SDK allows you to execute various commands in the cloud environment. This tutorial will guide you through executing shell commands.

## Command Execution

With AgentBay, you can execute shell commands in the cloud environment, just like you would in a local terminal. This is useful for file operations, installing packages, and other system administration tasks.

### Executing Basic Commands

The following example shows how to execute a simple echo command:

```python
from agentbay import AgentBay

# Initialize the SDK and create a session
agent_bay = AgentBay(api_key="your_api_key")
session_result = agent_bay.create()
session = session_result.session

# Execute an echo command
result = session.command.execute_command("echo 'Hello, AgentBay!'")
if result.success:
    print(f"Command output: {result.output}")
else:
    print(f"Command execution failed: {result.error_message}")

# Delete the session when done
agent_bay.delete(session)
```

```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

// Initialize the SDK
const agentBay = new AgentBay({ apiKey: 'your_api_key' });

async function executeBasicCommand() {
  try {
    // Create a session
    const createResponse = await agentBay.create();
    const session = createResponse.session;
    
    // Execute an echo command
    const result = await session.command.executeCommand("echo 'Hello, AgentBay!'");
    console.log(`Command output: ${result.output}`);
    
    // Delete the session
    await agentBay.delete(session);
  } catch (error) {
    console.error('Error:', error);
  }
}

executeBasicCommand();
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

  // Execute an echo command
  cmdResult, err := session.Command.ExecuteCommand("echo 'Hello, AgentBay!'")
  if err != nil {
    fmt.Printf("Error executing command: %v\n", err)
    os.Exit(1)
  }
  fmt.Printf("Command output: %s\n", cmdResult.Output)

  // Delete the session
  _, err = client.Delete(session)
  if err != nil {
    fmt.Printf("Error deleting session: %v\n", err)
    os.Exit(1)
  }
}
```

### Executing Complex Commands

You can also execute more complex commands, such as installing packages, creating files, or running scripts.

```python
from agentbay import AgentBay

# Initialize the SDK and create a session
agent_bay = AgentBay(api_key="your_api_key")
session_result = agent_bay.create()
session = session_result.session

# Execute multiple commands
commands = [
    "mkdir -p test_dir",
    "cd test_dir",
    "echo 'Test content' > test.txt",
    "cat test.txt",
    "ls -la"
]

for cmd in commands:
    print(f"Executing command: {cmd}")
    result = session.command.execute_command(cmd)
    if result.success:
        print(f"Output: {result.output}")
    else:
        print(f"Failed: {result.error_message}")
        break

# Delete the session when done
agent_bay.delete(session)
```

### Setting Command Timeout

For commands that might take longer to run, you can set a timeout parameter:

```python
# Execute a command that might take longer, with a 5-second timeout
result = session.command.execute_command("sleep 2 && echo 'Done'", timeout_ms=5000)
print(f"Command output: {result.output}")
```

## Best Practices

1. **Security**: Avoid executing untrusted commands, especially those from external sources.
2. **Error Handling**: Always check the return result of command executions and handle potential errors.
3. **Resource Management**: When executing long-running commands, consider setting appropriate timeout values.
4. **Cleanup**: After completing operations, make sure to delete sessions that are no longer needed to free up resources.
5. **Command Environment**: Be aware of the working directory and environment variables, as they may affect command behavior.

## Related Resources

- [API Reference: Command (Python)](../api-reference/python/command.md)
- [API Reference: Command (TypeScript)](../api-reference/typescript/command.md)
- [API Reference: Command (Golang)](../api-reference/golang/command.md)
- [Examples: Command Execution](../examples/python/command-example)
- [Code Execution Tutorial](code-execution.md): Learn how to run Python and JavaScript code 