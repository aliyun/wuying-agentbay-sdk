# Code Module - TypeScript

The Code module handles code execution operations in the AgentBay cloud environment.

## Methods

### runCode

Executes code in a specified programming language with a timeout.

```typescript
runCode(code: string, language: string, timeoutS: number = 300): Promise<CodeExecutionResult>
```

**Parameters:**
- `code` (string): The code to execute.
- `language` (string): The programming language of the code. Must be either 'python' or 'javascript'.
- `timeoutS` (number, optional): The timeout for the code execution in seconds. Default is 300s.

**Returns:**
- `Promise<CodeExecutionResult>`: A promise that resolves to a result object containing success status, execution result, error message if any, and request ID.

**Usage Example:**

```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

async function main() {
    // Initialize AgentBay with API key
    const apiKey = process.env.AGENTBAY_API_KEY!;
    const ab = new AgentBay({ apiKey });

    // Create a session
    const sessionResult = await ab.createSession({ resourceType: "linux" });
    const session = sessionResult.session;

    // Execute Python code
    const pythonCode = `
print("Hello from Python!")
result = 2 + 3
print(f"Result: {result}")
`;

    const codeResult = await session.code.runCode(pythonCode, "python");
    if (codeResult.success) {
        console.log(`Python code output:\n${codeResult.result}`);
        console.log(`Request ID: ${codeResult.requestId}`);
    } else {
        console.error(`Code execution failed: ${codeResult.errorMessage}`);
    }

    // Execute JavaScript code
    const jsCode = `
console.log("Hello from JavaScript!");
const result = 2 + 3;
console.log("Result:", result);
`;

    const jsResult = await session.code.runCode(jsCode, "javascript", 30);
    if (jsResult.success) {
        console.log(`JavaScript code output:\n${jsResult.result}`);
        console.log(`Request ID: ${jsResult.requestId}`);
    } else {
        console.error(`Code execution failed: ${jsResult.errorMessage}`);
    }
}

main().catch(console.error);
```

## Error Handling

The runCode method returns a CodeExecutionResult with `success: false` if:
- The specified language is not supported (only 'python' and 'javascript' are supported)
- The code execution fails in the cloud environment
- Network or API communication errors occur

In these cases, the `errorMessage` field will contain details about the failure.

## Types

### CodeExecutionResult

```typescript
interface CodeExecutionResult {
    requestId: string;      // Unique identifier for the API request
    success: boolean;       // Whether the operation was successful
    result: string;         // The execution result/output
    errorMessage?: string;  // Error message if the operation failed
}
``` 