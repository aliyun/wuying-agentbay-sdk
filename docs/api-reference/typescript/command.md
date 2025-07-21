# Command Class API Reference

The `Command` class provides methods for executing commands within a session in the AgentBay cloud environment.

## Methods

### executeCommand

Executes a shell command in the cloud environment.

```typescript
executeCommand(command: string, timeoutMs: number = 1000): Promise<CommandResult>
```

**Parameters:**
- `command` (string): The command to execute.
- `timeoutMs` (number, optional): The timeout for the command execution in milliseconds. Default is 1000ms.

**Returns:**
- `Promise<CommandResult>`: A promise that resolves to a result object containing the command output, success status, and request ID.

**CommandResult Interface:**
```typescript
interface CommandResult {
    requestId: string;      // Unique identifier for the API request
    success: boolean;       // Whether the operation was successful
    output: string;         // The command output
    errorMessage?: string;  // Error message if the operation failed
}
```

**Usage Example:**

```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

async function main() {
    // Initialize AgentBay with API key
    const apiKey = process.env.AGENTBAY_API_KEY!;
    const ab = new AgentBay({ apiKey });

    // Create a session
    const sessionResult = await ab.create();
    const session = sessionResult.session;

    try {
        // Execute a command
        const result = await session.command.executeCommand("ls -la");
        if (result.success) {
            console.log(`Command output:\n${result.output}`);
            console.log(`Request ID: ${result.requestId}`);
        } else {
            console.error(`Command execution failed: ${result.errorMessage}`);
        }

        // Execute a command with custom timeout
        const resultWithTimeout = await session.command.executeCommand(
            "sleep 2 && echo 'Done'", 
            5000
        );
        if (resultWithTimeout.success) {
            console.log(`Command output: ${resultWithTimeout.output}`);
        } else {
            console.error(`Command execution failed: ${resultWithTimeout.errorMessage}`);
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

main().catch(console.error);
```

## Related Resources

- [Session Class](session.md): The session class that provides access to the Command class.
- [Code Class](code.md): For executing Python and JavaScript code.
- [FileSystem Class](filesystem.md): Provides methods for file operations within a session.

