# VPC Session Management Documentation

This document provides comprehensive guidance on using VPC (Virtual Private Cloud) sessions with the AgentBay SDK across all supported languages.

## Overview

VPC sessions in AgentBay provide enhanced security and networking capabilities by running your cloud sessions within a private network environment. This feature is particularly useful for:

1. **Enhanced Security**: Isolating your sessions in a private network
2. **Custom Networking**: Configuring specific network policies and access controls
3. **Compliance**: Meeting regulatory requirements for data isolation
4. **Resource Access**: Securely accessing internal resources and services

VPC sessions have some limitations compared to standard sessions:
- Limited tool availability (only FileSystem and Command modules are available)
- Specialized system tools (get_resource, system_screenshot, release_resource)
- Browser tools availability (cdp, pageuse-mcp-server, playwright)

## Getting Started with VPC Sessions

### Prerequisites

To use VPC sessions, you need:
1. AgentBay SDK installed for your preferred language
2. Valid API key
3. Proper permissions for VPC session creation
4. Basic understanding of cloud networking concepts

### Creating a VPC Session

Creating a VPC session is similar to creating a standard session, but with the `is_vpc` parameter set to `true`:

```python
from agentbay import AgentBay
from agentbay.session_params import CreateSessionParams

# Initialize the SDK
agent_bay = AgentBay(api_key="your_api_key")

# Create a VPC session
params = CreateSessionParams(
    image_id="imgc-07eksy57nw6r759fb",  # Specific image ID for VPC sessions
    is_vpc=True,
    labels={"project": "vpc-demo", "environment": "testing"}
)
session_result = agent_bay.create(params)

if session_result.success:
    session = session_result.session
    print(f"VPC Session created with ID: {session.session_id}")
```

```typescript
import { AgentBay, CreateSessionParams } from 'wuying-agentbay-sdk';

// Initialize the SDK
const agentBay = new AgentBay({ apiKey: 'your_api_key' });

// Create a VPC session
async function createVpcSession() {
  const params = new CreateSessionParams()
    .withImageId('imgc-07eksy57nw6r759fb')
    .withIsVpc(true)
    .withLabels({ project: 'vpc-demo', environment: 'testing' });
  
  const sessionResult = await agentBay.create(params);
  
  if (sessionResult.success) {
    const session = sessionResult.session;
    console.log(`VPC Session created with ID: ${session.sessionId}`);
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

    // Create a VPC session
    params := agentbay.NewCreateSessionParams().
        WithImageId("imgc-07eksy57nw6r759fb").
        WithIsVpc(true).
        WithLabels(map[string]string{
            "project":     "vpc-demo",
            "environment": "testing",
        })

    sessionResult, err := client.Create(params)
    if err != nil {
        fmt.Printf("Error creating VPC session: %v\n", err)
        os.Exit(1)
    }

    session := sessionResult.Session
    fmt.Printf("VPC Session created with ID: %s\n", session.SessionID)
}
```

## Available Modules in VPC Sessions

VPC sessions have limited module availability compared to standard sessions:

### Available Modules:
1. **FileSystem**: File and directory operations
2. **Command**: Command execution
3. **System Tools**: 
   - `get_resource`: Resource information retrieval
   - `system_screenshot`: System-level screenshots
   - `release_resource`: Resource release operations
4. **Browser Tools**:
   - `cdp`: Chrome DevTools Protocol tools
   - `pageuse-mcp-server`: Page usage tools
   - `playwright`: Browser automation tools

### Unavailable Modules:
1. **Code**: Code execution module
2. **UI**: UI interaction module
3. **Window**: Window management module
4. **Application**: Application management module
5. **OSS**: Object Storage Service module

## Working with VPC Session Modules

### FileSystem Operations

VPC sessions support standard file system operations:

```python
# Write a file in VPC session
file_content = "Hello from VPC session!"
write_result = session.file_system.write_file("/tmp/vpc_test.txt", file_content)

if write_result.success:
    print("File written successfully")

# Read a file in VPC session
read_result = session.file_system.read_file("/tmp/vpc_test.txt")
if read_result.success:
    print(f"File content: {read_result.content}")
```

```typescript
// Write a file in VPC session
const fileContent = "Hello from VPC session!";
const writeResult = await session.fileSystem.writeFile("/tmp/vpc_test.txt", fileContent);

if (writeResult.success) {
    console.log("File written successfully");
}

// Read a file in VPC session
const readResult = await session.fileSystem.readFile("/tmp/vpc_test.txt");
if (readResult.success) {
    console.log(`File content: ${readResult.content}`);
}
```

```go
// Write a file in VPC session
fileContent := "Hello from VPC session!"
writeResult, err := session.FileSystem.WriteFile("/tmp/vpc_test.txt", fileContent)
if err != nil {
    fmt.Printf("Error writing file: %v\n", err)
} else if writeResult.Success {
    fmt.Println("File written successfully")
}

// Read a file in VPC session
readResult, err := session.FileSystem.ReadFile("/tmp/vpc_test.txt")
if err != nil {
    fmt.Printf("Error reading file: %v\n", err)
} else if readResult.Success {
    fmt.Printf("File content: %s\n", readResult.Content)
}
```

### Command Execution

VPC sessions support command execution:

```python
# Execute a command in VPC session
cmd_result = session.command.execute_command("whoami")
if cmd_result.success:
    print(f"Command output: {cmd_result.output}")
```

```typescript
// Execute a command in VPC session
const cmdResult = await session.command.executeCommand("whoami");
if (cmdResult.success) {
    console.log(`Command output: ${cmdResult.output}`);
}
```

```go
// Execute a command in VPC session
cmdResult, err := session.Command.ExecuteCommand("whoami")
if err != nil {
    fmt.Printf("Error executing command: %v\n", err)
} else if cmdResult.Success {
    fmt.Printf("Command output: %s\n", cmdResult.Output)
}
```

## VPC Session Context Synchronization

Context synchronization works the same way in VPC sessions as in standard sessions:

```python
from agentbay import AgentBay
from agentbay.context_sync import ContextSync, SyncPolicy
from agentbay.session_params import CreateSessionParams

# Initialize the SDK
agent_bay = AgentBay(api_key="your_api_key")

# Get or create a persistent context
context_result = agent_bay.context.get("my-vpc-context", create=True)

if context_result.success:
    # Configure context synchronization
    context_sync = ContextSync.new(
        context_id=context_result.context.id,
        path="/mnt/data",  # Mount path in the session
        policy=SyncPolicy.default()
    )
    
    # Create a VPC session with context synchronization
    params = CreateSessionParams(
        image_id="imgc-07eksy57nw6r759fb",
        is_vpc=True,
        context_syncs=[context_sync],
        labels={"project": "vpc-demo", "purpose": "data-processing"}
    )
    
    session_result = agent_bay.create(params)
    session = session_result.session
    
    print(f"VPC Session created with ID: {session.session_id} and synchronized context at /mnt/data")
```

## Best Practices for VPC Sessions

1. **Module Awareness**:
   - Be aware of the limited module availability in VPC sessions
   - Design your applications to work within these constraints
   - Use available system and browser tools when appropriate

2. **Security**:
   - Use VPC sessions for sensitive operations that require network isolation
   - Implement proper access controls and monitoring
   - Regularly review and audit VPC session usage

3. **Resource Management**:
   - Always delete VPC sessions when no longer needed
   - Use appropriate session timeouts to prevent resource waste
   - Monitor resource consumption in VPC environments

4. **Error Handling**:
   - Implement robust error handling for module unavailability
   - Check session creation results carefully
   - Log request IDs for debugging VPC session issues

5. **Performance Optimization**:
   - Use appropriate image IDs for VPC sessions
   - Minimize the number of synchronized contexts per VPC session
   - Optimize command execution and file operations

## Limitations and Considerations

1. **Module Limitations**: Only FileSystem and Command modules are available
2. **Tool Availability**: Some advanced tools are not available in VPC environments
3. **Image Requirements**: Specific image IDs may be required for VPC sessions
4. **Networking**: VPC sessions have different networking characteristics
5. **Performance**: VPC sessions may have different performance characteristics

## Troubleshooting VPC Sessions

### Common Issues

1. **Session Creation Failures**:
   - Verify your API key has VPC session permissions
   - Check if you've reached VPC session limits
   - Ensure the specified image ID is valid for VPC sessions
   - Verify VPC networking configuration

2. **Module Unavailability**:
   - Check that you're not trying to use unavailable modules
   - Verify session creation parameters include `is_vpc=true`
   - Review the available modules list for VPC sessions

3. **Context Synchronization Issues**:
   - Check network connectivity within the VPC environment
   - Verify context IDs are valid
   - Review synchronization policy settings

4. **Resource Access Problems**:
   - Verify VPC networking and security group configurations
   - Check resource permissions and access controls
   - Review VPC session networking documentation

## API Reference

For detailed API documentation, see:
- [Python Session API](../api-reference/python/session.md)
- [TypeScript Session API](../api-reference/typescript/session.md)
- [Golang Session API](../api-reference/golang/session.md)
- [Python AgentBay API](../api-reference/python/agentbay.md)
- [TypeScript AgentBay API](../api-reference/typescript/agentbay.md)
- [Golang AgentBay API](../api-reference/golang/agentbay.md)