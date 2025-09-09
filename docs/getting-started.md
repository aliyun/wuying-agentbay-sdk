# Getting Started with AgentBay SDK

The AgentBay SDK provides a comprehensive set of tools to interact with the AgentBay cloud environment, enabling you to create and manage cloud sessions, execute commands, manipulate files, and interact with UIs.

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

To use the AgentBay SDK, you need an API key. You can set the API key in two ways:

### 1. Set Environment Variable

**Linux/macOS:**
```bash
export AGENTBAY_API_KEY=your_api_key
```
**Windows (PowerShell):**
```powershell
$env:AGENTBAY_API_KEY="your-api-key-here"
```
**Windows (Command Prompt):**
```cmd
set AGENTBAY_API_KEY=your-api-key-here
```
#### Using Environment Variables
After setting environment variables, create the SDK client directly:

**Python:**
```python
from agentbay import AgentBay

# SDK will automatically read environment variable configuration
# API key can also be set via AGENTBAY_API_KEY environment variable
 api_key = os.getenv("AGENTBAY_API_KEY")
if not api_key:
    api_key = "akm-xxx"
    print("Warning: Using default API key.")
agent_bay = AgentBay(api_key=api_key)
```

**TypeScript:**
```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

// SDK will automatically read environment variable configuration
// API key can also be set via AGENTBAY_API_KEY environment variable
const apiKey = process.env.AGENTBAY_API_KEY
const agentBay = new AgentBay({apiKey});
```

**Golang:**
```go
package main

import (
    "testing"
    "github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

func main() {
    // SDK will automatically read environment variable configuration
    // API key can also be set via AGENTBAY_API_KEY environment variable
    testAPIKey := testutil.GetTestAPIKey(&testing.T{})
    client, err := agentbay.NewAgentBay(testAPIKey, nil)
    if err != nil {
        panic(err)
    }
}
```
### 2. Configuration File Method

Create a `.env` file in your project root directory:
```env
AGENTBAY_API_KEY=your-api-key-here
```
**Python:**
```python
# Python
from agentbay import AgentBay

# SDK will automatically load .env file
# No need to specify API key if it's in .env file
agent_bay = AgentBay()
```
**TypeScript:**
```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

// SDK will automatically load .env file
// No need to specify API key if it's in .env file
const agentBay = new AgentBay();
```
**Golang:**
```go
package main

import (
    "github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

func main() {
    // SDK will automatically load .env file
    // No need to specify API key if it's in .env file
    client, err := agentbay.NewAgentBay("")
    if err != nil {
        panic(err)
    }
}
```

For more details about authentication, see the [Authentication Guide](./guides/sdk-configuration.md).

## Basic Usage

### Create a Session

```python
# Python
from agentbay import AgentBay

agent_bay = AgentBay(api_key=api_key)
result = agent_bay.create()

if result.success:
    session = result.session
    print(f"Session created with ID: {session.session_id}")
```

```typescript
// TypeScript
import { AgentBay } from 'wuying-agentbay-sdk';

const agentBay = new AgentBay({apiKey});
const result = await agentBay.create();

if (result.success) {
    const session = result.session;
    console.log(`Session created with ID: ${session.sessionId}`);
}
```

```go
// Golang
package main

import (
    "fmt"
    "github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

func main() {
    client, err := agentbay.NewAgentBay("yourApiKey", nil)
    if err != nil {
        fmt.Printf("Error initializing client: %v\n", err)
        return
    }

    result, err := client.Create(nil)
    if err != nil {
        fmt.Printf("Error creating session: %v\n", err)
        return
    }

    fmt.Printf("Session created with ID: %s\n", result.Session.SessionID)
}
```

### Execute a Command

```python
# Python
command_result = session.command.execute_command("ls -la")
if command_result.success:
    print(f"Output: {command_result.output}")
```

```typescript
// TypeScript
const commandResult = await session.command.executeCommand('ls -la');
if (commandResult.success) {
    console.log(`Output: ${commandResult.output}`);
}
```

```go
// Golang
commandResult, err := session.Command.ExecuteCommand("ls -la")
if err != nil {
    fmt.Printf("Error executing command: %v\n", err)
    return
}

fmt.Printf("Output: %s\n", commandResult.Output)
```

### Working with Files

```python
# Python
# Write a file
write_result = session.file_system.write_file(
    path="/tmp/test.txt",
    content="Hello, World!"
)

# Read a file
read_result = session.file_system.read_file(path="/tmp/test.txt")
if read_result.success:
    print(f"File content: {read_result.content}")
```

```typescript
// TypeScript
// Write a file
const writeResult = await session.fileSystem.writeFile(
    '/tmp/test.txt',
    'Hello, World!'
);

// Read a file
const readResult = await session.fileSystem.readFile('/tmp/test.txt');
if (readResult.success) {
    console.log(`File content: ${readResult.content}`);
}
```

```go
// Golang
// Write a file
_, err = session.FileSystem.WriteFile(
    "/tmp/test.txt",
    "Hello, World!",
    "overwrite",
)
if err != nil {
    fmt.Printf("Error writing file: %v\n", err)
    return
}

// Read a file
readResult, err := session.FileSystem.ReadFile("/tmp/test.txt")
if err != nil {
    fmt.Printf("Error reading file: %v\n", err)
    return
}

fmt.Printf("File content: %s\n", string(readResult.Content))
```

### Using Persistent Contexts

```python
# Python
from agentbay import AgentBay
from agentbay.context_sync import ContextSync, SyncPolicy
from agentbay.session_params import CreateSessionParams

# Initialize the client
agent_bay = AgentBay(api_key=api_key)

# Get or create a context
context_result = agent_bay.context.get("my-persistent-context", create=True)

if context_result.success:
    context = context_result.context

    # Create a session with context synchronization
    context_sync = ContextSync.new(
        context_id=context.id,
        path="/tmp/data",  # Mount path in the session
        policy=SyncPolicy.default()
    )

    params = CreateSessionParams(context_syncs=[context_sync])
    session_result = agent_bay.create(params)
```

```typescript
// TypeScript
import { AgentBay, ContextSync, newSyncPolicy } from 'wuying-agentbay-sdk';

// Initialize the client
const agentBay = new AgentBay({apiKey});

// Get or create a context
const contextResult = await agentBay.context.get('my-persistent-context', true);

if (contextResult.success) {
    const context = contextResult.context;

    // Create a session with context synchronization
    const contextSync = new ContextSync({
        contextId: context.id,
        path: '/tmp/data',  // Mount path in the session
        policy: SyncPolicy.default()
    });

    const sessionResult = await agentBay.create({
        contextSync: [contextSync]
    });
}
```

```go
// Golang
package main

import (
    "fmt"
    "github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

func main() {
    // Initialize the client
    client, _ := agentbay.NewAgentBay("", nil)

    // Get or create a context
    contextResult, _ := client.Context.Get("my-persistent-context", true)

    // Create a session with context synchronization
    policy := agentbay.NewSyncPolicy()
    contextSync := agentbay.NewContextSync(
        contextResult.Context.ID,
        "/tmp/data",  // Mount path in the session
        policy,
    )

    params := agentbay.NewCreateSessionParams().
        AddContextSyncConfig(contextSync)

    sessionResult, _ := client.Create(params)
}
```

## Next Steps

Now that you know the basics of using the AgentBay SDK, you can explore more features:

### Tutorials

- [Golang Tutorial](../golang/docs/api/README.md)
- [Python Tutorial](../python/docs/api/README.md)
- [TypeScript Tutorial](../typescript/docs/api/README.md)
