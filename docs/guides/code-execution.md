# Code Execution Documentation

This document provides comprehensive guidance on using the code execution capabilities of the AgentBay SDK across all supported languages.

## Overview

The code execution feature allows developers to run code in different programming languages directly in the AgentBay cloud environment. This eliminates the need to set up local development environments and provides access to powerful cloud computing resources.

Currently, the SDK supports executing code in two languages:
- Python
- JavaScript

## Getting Started

### Prerequisites

To use code execution, you need:
1. AgentBay SDK installed for your preferred language
2. Valid API key
3. Active session in the AgentBay cloud environment

### Creating a Session for Code Execution

Before executing code, you need to create a session:

```python
from agentbay import AgentBay

# Initialize the SDK
agent_bay = AgentBay(api_key="your_api_key")

# Create a session
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
  const sessionResult = await agentBay.create();
  if (sessionResult.success) {
    const session = sessionResult.session;
    console.log(`Session created with ID: ${session.sessionId}`);
    return session;
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
    fmt.Printf("Session created with ID: %s\n", session.SessionID)
}
```

## Running Python Code

### Basic Python Code Execution

```python
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
```

### Python Code with Custom Timeout

```python
# Set a 60-second timeout for code execution
result = session.code.run_code(code, "python", timeout_s=60)
if result.success:
    print(f"Code execution result:\n{result.result}")
else:
    print(f"Code execution failed: {result.error_message}")
```

## Running JavaScript Code

### Basic JavaScript Code Execution

```python
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
```

### JavaScript Code with Custom Timeout

```python
# Set a 45-second timeout for code execution
result = session.code.run_code(code, "javascript", timeout_s=45)
if result.success:
    print(f"Code execution result:\n{result.result}")
else:
    print(f"Code execution failed: {result.error_message}")
```

## TypeScript Examples

### Running Python Code

```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

async function executePythonCode() {
  // Initialize the SDK
  const agentBay = new AgentBay({ apiKey: 'your_api_key' });
  
  try {
    // Create a session
    const sessionResult = await agentBay.create();
    const session = sessionResult.session;
    
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
    if (result.success) {
        console.log(`Code execution result:\n${result.result}`);
    } else {
        console.error(`Code execution failed: ${result.errorMessage}`);
    }
    
    // Clean up
    await agentBay.delete(session);
  } catch (error) {
    console.error('Error:', error);
  }
}

executePythonCode();
```

### Running JavaScript Code

```typescript
async function executeJavaScriptCode() {
  // Initialize the SDK
  const agentBay = new AgentBay({ apiKey: 'your_api_key' });
  
  try {
    // Create a session
    const sessionResult = await agentBay.create();
    const session = sessionResult.session;
    
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
    if (result.success) {
        console.log(`Code execution result:\n${result.result}`);
    } else {
        console.error(`Code execution failed: ${result.errorMessage}`);
    }
    
    // Clean up
    await agentBay.delete(session);
  } catch (error) {
    console.error('Error:', error);
  }
}

executeJavaScriptCode();
```

## Golang Examples

### Running Python Code

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
    
    fmt.Printf("Code execution result:\n%s\n", codeResult.Output)
    fmt.Printf("Request ID: %s\n", codeResult.RequestID)

    // Clean up
    _, err = client.Delete(session)
    if err != nil {
        fmt.Printf("Error deleting session: %v\n", err)
        os.Exit(1)
    }
}
```

### Running JavaScript Code

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

    // Prepare the JavaScript code to execute
    code := `
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
    `

    // Execute JavaScript code with custom timeout
    codeResult, err := session.Code.RunCode(code, "javascript", 30)
    if err != nil {
        fmt.Printf("Error executing code: %v\n", err)
        os.Exit(1)
    }
    
    fmt.Printf("Code execution result:\n%s\n", codeResult.Output)
    fmt.Printf("Request ID: %s\n", codeResult.RequestID)

    // Clean up
    _, err = client.Delete(session)
    if err != nil {
        fmt.Printf("Error deleting session: %v\n", err)
        os.Exit(1)
    }
}
```

## Error Handling

### Python Error Handling

```python
try:
    result = session.code.run_code(code, "python")
    if result.success:
        print(f"Code execution result:\n{result.result}")
    else:
        print(f"Code execution failed: {result.error_message}")
        print(f"Request ID: {result.request_id}")  # Useful for debugging
except Exception as e:
    print(f"Unexpected error: {e}")
```

### TypeScript Error Handling

```typescript
try {
    const result = await session.code.runCode(code, 'python');
    if (result.success) {
        console.log(`Code execution result:\n${result.result}`);
    } else {
        console.error(`Code execution failed: ${result.errorMessage}`);
        console.error(`Request ID: ${result.requestId}`);  // Useful for debugging
    }
} catch (error) {
    console.error('Unexpected error:', error);
}
```

### Golang Error Handling

```go
codeResult, err := session.Code.RunCode(code, "python")
if err != nil {
    fmt.Printf("Error executing code: %v\n", err)
    return
}

if codeResult.Output != "" {
    fmt.Printf("Code execution result:\n%s\n", codeResult.Output)
} else {
    fmt.Printf("Code execution completed with no output\n")
}
fmt.Printf("Request ID: %s\n", codeResult.RequestID)  // Useful for debugging
```

## Best Practices

1. **Security**: 
   - Avoid executing untrusted code, especially from external sources
   - Validate and sanitize any user-provided code before execution
   - Use the principle of least privilege when designing your applications

2. **Error Handling**:
   - Always check the return result of code executions
   - Handle potential errors gracefully
   - Log request IDs for debugging purposes

3. **Resource Management**:
   - For compute-intensive or long-running code, consider setting appropriate timeout values
   - Delete sessions that are no longer needed to free up resources
   - Monitor resource usage to optimize costs

4. **Code Isolation**:
   - When executing code, try to avoid modifying critical system files
   - Use separate sessions for different types of operations
   - Design your code to be stateless when possible

5. **Dependency Management**:
   - Note that your code will run in a pre-configured environment
   - Ensure required libraries are available in the cloud environment
   - Test your code in the cloud environment before production use

6. **Performance Optimization**:
   - Batch multiple operations in a single code execution when possible
   - Minimize data transfer between your application and the cloud environment
   - Use appropriate session configurations for your workload

## Limitations

1. **Supported Languages**: Only Python and JavaScript are currently supported
2. **Execution Time**: Maximum execution time is limited (default 300 seconds)
3. **Resource Constraints**: Memory and CPU resources are limited per session
4. **Network Access**: Code execution environment has controlled network access
5. **File System**: Limited file system access with session-based isolation

## Troubleshooting

### Common Issues

1. **Language Not Supported Error**:
   - Ensure you're using either "python" or "javascript" as the language parameter
   - Check for typos in the language name

2. **Timeout Errors**:
   - Increase the timeout value for long-running operations
   - Optimize your code for better performance
   - Break complex operations into smaller chunks

3. **Execution Failures**:
   - Check the error message for specific details
   - Verify syntax errors in your code
   - Ensure all required dependencies are available

4. **Network Issues**:
   - Check your internet connection
   - Verify the AgentBay service status
   - Retry the operation after a short delay

## API Reference

For detailed API documentation, see:
- [Python Code API](../api-reference/python/code.md)
- [TypeScript Code API](../api-reference/typescript/code.md)
- [Golang Code API](../api-reference/golang/code.md)