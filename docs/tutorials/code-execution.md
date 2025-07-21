# Code Execution Tutorial

AgentBay SDK allows you to run code in different languages in the cloud environment. This tutorial will guide you through running Python and JavaScript code.

## Code Execution Overview

In addition to executing shell commands, AgentBay also allows you to run code directly in the cloud environment. Currently, Python and JavaScript are supported. The code execution feature enables you to perform complex computations and automation tasks in the cloud environment without having to manually install dependencies or set up the environment.

## Running Python Code

The following example shows how to run Python code:

```python
from agentbay import AgentBay

# Initialize the SDK and create a session
agent_bay = AgentBay(api_key="your_api_key")
session_result = agent_bay.create()
session = session_result.session

# Prepare the Python code to execute
code = """
import random
import platform

# Get system information
system_info = {
    "platform": platform.platform(),
    "python_version": platform.python_version(),
    "processor": platform.processor()
}

# Generate random numbers
random_numbers = [random.randint(1, 100) for _ in range(5)]

# Print results
print(f"System info: {system_info}")
print(f"Random numbers: {random_numbers}")
"""

# Execute Python code
result = session.code.run_code(code, "python")
if result.success:
    print(f"Code execution result:\n{result.result}")
else:
    print(f"Code execution failed: {result.error_message}")

# Delete the session when done
agent_bay.delete(session)
```

```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

// Initialize the SDK
const agentBay = new AgentBay({ apiKey: 'your_api_key' });

async function executePythonCode() {
  try {
    // Create a session
    const createResponse = await agentBay.create();
    const session = createResponse.session;
    
    // Prepare the Python code to execute
    const code = `
import random
import platform

# Get system information
system_info = {
    "platform": platform.platform(),
    "python_version": platform.python_version(),
    "processor": platform.processor()
}

# Generate random numbers
random_numbers = [random.randint(1, 100) for _ in range(5)]

# Print results
print(f"System info: {system_info}")
print(f"Random numbers: {random_numbers}")
    `;
    
    // Execute Python code
    const result = await session.code.runCode(code, 'python');
    console.log(`Code execution result:\n${result.result}`);
    
    // Delete the session
    await agentBay.delete(session);
  } catch (error) {
    console.error('Error:', error);
  }
}

executePythonCode();
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

  // Prepare the Python code to execute
  code := `
import random
import platform

# Get system information
system_info = {
    "platform": platform.platform(),
    "python_version": platform.python_version(),
    "processor": platform.processor()
}

# Generate random numbers
random_numbers = [random.randint(1, 100) for _ in range(5)]

# Print results
print(f"System info: {system_info}")
print(f"Random numbers: {random_numbers}")
  `

  // Execute Python code
  codeResult, err := session.Code.RunCode(code, "python")
  if err != nil {
    fmt.Printf("Error executing code: %v\n", err)
    os.Exit(1)
  }
  fmt.Printf("Code execution result:\n%s\n", codeResult.Result)

  // Delete the session
  _, err = client.Delete(session)
  if err != nil {
    fmt.Printf("Error deleting session: %v\n", err)
    os.Exit(1)
  }
}
```

## Running JavaScript Code

The following example shows how to run JavaScript code:

```python
from agentbay import AgentBay

# Initialize the SDK and create a session
agent_bay = AgentBay(api_key="your_api_key")
session_result = agent_bay.create()
session = session_result.session

# Prepare the JavaScript code to execute
code = """
// Get current time
const now = new Date();
console.log(`Current time: ${now.toISOString()}`);

// Calculate values
const numbers = [1, 2, 3, 4, 5];
const sum = numbers.reduce((a, b) => a + b, 0);
const average = sum / numbers.length;

console.log(`Numbers: ${numbers}`);
console.log(`Sum: ${sum}`);
console.log(`Average: ${average}`);
"""

# Execute JavaScript code
result = session.code.run_code(code, "javascript")
if result.success:
    print(f"Code execution result:\n{result.result}")
else:
    print(f"Code execution failed: {result.error_message}")

# Delete the session when done
agent_bay.delete(session)
```

```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

// Initialize the SDK
const agentBay = new AgentBay({ apiKey: 'your_api_key' });

async function executeJavaScriptCode() {
  try {
    // Create a session
    const createResponse = await agentBay.create();
    const session = createResponse.session;
    
    // Prepare the JavaScript code to execute
    const code = `
      // Get current time
      const now = new Date();
      console.log(\`Current time: \${now.toISOString()}\`);
      
      // Calculate values
      const numbers = [1, 2, 3, 4, 5];
      const sum = numbers.reduce((a, b) => a + b, 0);
      const average = sum / numbers.length;
      
      console.log(\`Numbers: \${numbers}\`);
      console.log(\`Sum: \${sum}\`);
      console.log(\`Average: \${average}\`);
    `;
    
    // Execute JavaScript code
    const result = await session.code.runCode(code, 'javascript');
    console.log(`Code execution result:\n${result.result}`);
    
    // Delete the session
    await agentBay.delete(session);
  } catch (error) {
    console.error('Error:', error);
  }
}

executeJavaScriptCode();
```

## Setting Code Execution Timeout

For code that might take longer to run, you can set a timeout parameter:

```python
# Set a 300-second timeout for code execution
result = session.code.run_code(code, "python", timeout_s=300)
print(f"Code execution result:\n{result.result}")
```

## Best Practices

1. **Security**: Avoid executing untrusted code, especially from external sources.
2. **Error Handling**: Always check the return result of code executions and handle potential errors.
3. **Resource Management**: For compute-intensive or long-running code, consider setting appropriate timeout values.
4. **Cleanup**: After completing operations, make sure to delete sessions that are no longer needed to free up resources.
5. **Code Isolation**: When executing code, try to avoid modifying critical system files or operations that might damage the environment.
6. **Dependency Management**: Note that your code will run in a pre-configured environment, so ensure required libraries are available.

## Related Resources

- [API Reference: Command](../api-reference/command.md)
- [Command Execution Tutorial](command-execution.md): Learn how to execute shell commands 