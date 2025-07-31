# VPC Session Management Tutorial

This tutorial provides step-by-step instructions for working with VPC (Virtual Private Cloud) sessions in the AgentBay SDK. VPC sessions offer enhanced security and networking capabilities by running your cloud sessions within a private network environment.

## Overview

VPC sessions in AgentBay provide several benefits:
1. **Enhanced Security**: Isolated network environment for sensitive operations
2. **Custom Networking**: Ability to configure specific network policies
3. **Compliance**: Meeting regulatory requirements for data isolation
4. **Resource Access**: Secure access to internal resources and services

This tutorial will cover:
- Creating VPC sessions
- Working with available modules in VPC sessions
- Context synchronization in VPC environments
- Best practices for VPC session management

## Prerequisites

Before starting this tutorial, ensure you have:
1. AgentBay SDK installed for your preferred language
2. Valid API key with VPC session permissions
3. Basic understanding of cloud computing concepts
4. Familiarity with the AgentBay SDK fundamentals

## Step 1: Creating a Basic VPC Session

Let's start by creating a simple VPC session. The key difference from a standard session is setting the `is_vpc` parameter to `true`.

### Python

```python
from agentbay import AgentBay
from agentbay.session_params import CreateSessionParams

# Initialize the SDK
agent_bay = AgentBay(api_key="your_api_key")

# Create a VPC session
params = CreateSessionParams(
    image_id="imgc-07eksy57nw6r759fb",  # Specific image ID for VPC sessions
    is_vpc=True,
    labels={"tutorial": "vpc-basic", "step": "1"}
)

session_result = agent_bay.create(params)
if session_result.success:
    session = session_result.session
    print(f"VPC Session created with ID: {session.session_id}")
```

### TypeScript

```typescript
import { AgentBay, CreateSessionParams } from 'wuying-agentbay-sdk';

// Initialize the SDK
const agentBay = new AgentBay({ apiKey: 'your_api_key' });

// Create a VPC session
const params = new CreateSessionParams()
  .withImageId('imgc-07eksy57nw6r759fb')
  .withIsVpc(true)
  .withLabels({ tutorial: 'vpc-basic', step: '1' });

const sessionResult = await agentBay.create(params);
if (sessionResult.success) {
    const session = sessionResult.session;
    console.log(`VPC Session created with ID: ${session.sessionId}`);
}
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
            "tutorial": "vpc-basic",
            "step":     "1",
        })

    sessionResult, err := client.Create(params)
    if err != nil {
        fmt.Printf("Error creating VPC session: %v\n", err)
        os.Exit(1)
    }

    if sessionResult.Success {
        session := sessionResult.Session
        fmt.Printf("VPC Session created with ID: %s\n", session.SessionID)
    }
}
```

## Step 2: Working with VPC Session Modules

VPC sessions have limited module availability compared to standard sessions. The available modules are:
1. **FileSystem**: File and directory operations
2. **Command**: Command execution
3. **System Tools**: Specialized system-level tools
4. **Browser Tools**: Browser automation capabilities

Let's explore working with these modules:

### FileSystem Operations

```python
# Write a file in VPC session
file_content = "Hello from VPC session!"
write_result = session.file_system.write_file("/tmp/vpc_tutorial.txt", file_content)

if write_result.success:
    print("File written successfully")

# Read a file in VPC session
read_result = session.file_system.read_file("/tmp/vpc_tutorial.txt")
if read_result.success:
    print(f"File content: {read_result.content}")
```

### Command Execution

```python
# Execute a command in VPC session
cmd_result = session.command.execute_command("ls -la /tmp")
if cmd_result.success:
    print(f"Directory listing:\n{cmd_result.output}")
```

## Step 3: Context Synchronization in VPC Sessions

Context synchronization works the same way in VPC sessions as in standard sessions. Let's create a VPC session with context synchronization:

### Python

```python
from agentbay.context_sync import ContextSync, SyncPolicy

# Get or create a persistent context
context_result = agent_bay.context.get("vpc-tutorial-context", create=True)

if context_result.success:
    # Configure context synchronization
    context_sync = ContextSync.new(
        context_id=context_result.context.id,
        path="/mnt/vpc-data",
        policy=SyncPolicy.default()
    )
    
    # Create a VPC session with context synchronization
    params = CreateSessionParams(
        image_id="imgc-07eksy57nw6r759fb",
        is_vpc=True,
        context_syncs=[context_sync],
        labels={"tutorial": "vpc-context", "step": "3"}
    )
    
    session_result = agent_bay.create(params)
    session = session_result.session
    
    # Write data to the synchronized context
    data_content = "Data persisted in VPC session"
    write_result = session.file_system.write_file("/mnt/vpc-data/tutorial_data.txt", data_content)
    
    # The data will be synchronized when the session is deleted
    agent_bay.delete(session, sync_context=True)
```

## Step 4: Working with System Tools

VPC sessions provide access to specialized system tools that are not available in standard sessions:

```python
# These tools are automatically available in VPC sessions
# System screenshot
# Resource information retrieval
# Resource release operations

# Note: Direct access to these tools is typically handled by the SDK
# You would use them through the available modules like Command
cmd_result = session.command.execute_command("system_screenshot")
if cmd_result.success:
    print("System screenshot captured")
```

## Step 5: Browser Automation in VPC Sessions

VPC sessions also support browser automation tools:

```python
# Browser tools are available in VPC sessions
# This includes cdp, pageuse-mcp-server, and playwright tools

# Note: Browser automation in VPC sessions requires specific setup
# and may have different capabilities than standard browser sessions
```

## Best Practices

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

## Common Use Cases

1. **Secure Data Processing**: Processing sensitive data in an isolated environment
2. **Compliance Operations**: Meeting regulatory requirements for data isolation
3. **Internal Resource Access**: Securely accessing internal services and databases
4. **Network Testing**: Testing applications in controlled network environments
5. **Penetration Testing**: Security testing in isolated environments

## Troubleshooting

### Session Creation Failures

If you encounter issues creating VPC sessions:

1. Verify your API key has VPC session permissions
2. Check if you've reached VPC session limits
3. Ensure the specified image ID is valid for VPC sessions
4. Verify VPC networking configuration

### Module Unavailability

If you're trying to use unavailable modules:

1. Check that you're not trying to use unavailable modules
2. Verify session creation parameters include `is_vpc=true`
3. Review the available modules list for VPC sessions

### Context Synchronization Issues

For context synchronization problems:

1. Check network connectivity within the VPC environment
2. Verify context IDs are valid
3. Review synchronization policy settings

## Next Steps

1. Experiment with different VPC session configurations
2. Implement more sophisticated error handling and retry mechanisms
3. Add logging and monitoring for production use
4. Explore integration with other AgentBay session capabilities
5. Build applications that leverage the security benefits of VPC sessions

This tutorial demonstrated how to create and work with VPC sessions using the AgentBay SDK. By leveraging VPC sessions, you can enhance the security and networking capabilities of your cloud-based applications while maintaining the flexibility and power of the AgentBay platform.