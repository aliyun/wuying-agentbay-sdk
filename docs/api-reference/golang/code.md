# Code Module - Go

The Code module handles code execution operations in the AgentBay cloud environment.

## Methods

### RunCode

Executes code in a specified programming language with a timeout.

```go
RunCode(code string, language string, timeoutS ...int) (*CodeResult, error)
```

**Parameters:**
- `code` (string): The code to execute.
- `language` (string): The programming language of the code. Must be either 'python' or 'javascript'.
- `timeoutS` (int, optional): The timeout for the code execution in seconds. Default is 300s.

**Returns:**
- `*CodeResult`: A result object containing the execution output and request ID.
- `error`: An error object if the operation fails.

**Usage Example:**

```go
package main

import (
    "fmt"
    agentbay "github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

func main() {
    // Initialize AgentBay and create session
    ab := agentbay.NewAgentBay()
    sessionParams := &agentbay.SessionParams{ResourceType: "linux"}
    sessionResult, err := ab.CreateSession(sessionParams)
    if err != nil {
        panic(err)
    }
    session := sessionResult.Session

    // Execute Python code
    pythonCode := `
print("Hello from Python!")
result = 2 + 3
print(f"Result: {result}")
`
    codeResult, err := session.Code.RunCode(pythonCode, "python")
    if err != nil {
        fmt.Printf("Error executing Python code: %v\n", err)
    } else {
        fmt.Printf("Python code output:\n%s\n", codeResult.Output)
        fmt.Printf("Request ID: %s\n", codeResult.RequestID)
    }

    // Execute JavaScript code
    jsCode := `
console.log("Hello from JavaScript!");
const result = 2 + 3;
console.log("Result:", result);
`
    jsResult, err := session.Code.RunCode(jsCode, "javascript", 30)
    if err != nil {
        fmt.Printf("Error executing JavaScript code: %v\n", err)
    } else {
        fmt.Printf("JavaScript code output:\n%s\n", jsResult.Output)
        fmt.Printf("Request ID: %s\n", jsResult.RequestID)
    }
}
```

## Error Handling

The RunCode method returns an error if:
- The specified language is not supported (only 'python' and 'javascript' are supported)
- The code execution fails in the cloud environment
- Network or API communication errors occur

## Types

### CodeResult

```go
type CodeResult struct {
    ApiResponse  // Embedded ApiResponse containing RequestID
    Output string // The execution output
}
``` 