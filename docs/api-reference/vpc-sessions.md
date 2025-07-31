# VPC Session API Reference

This document provides detailed API reference documentation for VPC (Virtual Private Cloud) session functionality in the AgentBay SDK across all supported languages.

## Overview

VPC sessions in AgentBay provide enhanced security and networking capabilities by running your cloud sessions within a private network environment. This feature is particularly useful for sensitive operations that require network isolation.

## Python VPC Session API

### Session Class Extensions

The `Session` class in Python has been extended with VPC-specific functionality:

#### is_vpc_enabled()

```python
def is_vpc_enabled(self) -> bool
```

Return whether this session uses VPC resources.

**Returns:**
- `bool`: True if the session is a VPC session, False otherwise.

#### get_network_interface_ip()

```python
def get_network_interface_ip(self) -> str
```

Return the network interface IP for VPC sessions.

**Returns:**
- `str`: The network interface IP address for VPC sessions.

#### get_http_port()

```python
def get_http_port(self) -> str
```

Return the HTTP port for VPC sessions.

**Returns:**
- `str`: The HTTP port for VPC sessions.

### VPC Session Creation

To create a VPC session in Python, use the `is_vpc` parameter in `CreateSessionParams`:

```python
from agentbay import AgentBay
from agentbay.session_params import CreateSessionParams

# Initialize the SDK
agent_bay = AgentBay(api_key="your_api_key")

# Create a VPC session
params = CreateSessionParams(
    image_id="imgc-07eksy57nw6r759fb",
    is_vpc=True,
    labels={"environment": "vpc-test"}
)

session_result = agent_bay.create(params)
if session_result.success:
    session = session_result.session
    print(f"VPC Session created: {session.is_vpc_enabled()}")  # True
```

## TypeScript VPC Session API

### Session Class Extensions

The `Session` class in TypeScript has been extended with VPC-specific functionality:

#### isVpcEnabled()

```typescript
isVpcEnabled(): boolean
```

Return whether this session uses VPC resources.

**Returns:**
- `boolean`: True if the session is a VPC session, False otherwise.

#### getNetworkInterfaceIp()

```typescript
getNetworkInterfaceIp(): string
```

Return the network interface IP for VPC sessions.

**Returns:**
- `string`: The network interface IP address for VPC sessions.

#### getHttpPort()

```typescript
getHttpPort(): string
```

Return the HTTP port for VPC sessions.

**Returns:**
- `string`: The HTTP port for VPC sessions.

### VPC Session Creation

To create a VPC session in TypeScript, use the `withIsVpc` method in `CreateSessionParams`:

```typescript
import { AgentBay, CreateSessionParams } from 'wuying-agentbay-sdk';

// Initialize the SDK
const agentBay = new AgentBay({ apiKey: 'your_api_key' });

// Create a VPC session
const params = new CreateSessionParams()
  .withImageId('imgc-07eksy57nw6r759fb')
  .withIsVpc(true)
  .withLabels({ environment: 'vpc-test' });

const sessionResult = await agentBay.create(params);
if (sessionResult.success) {
    const session = sessionResult.session;
    console.log(`VPC Session created: ${session.isVpcEnabled()}`);  // true
}
```

## Golang VPC Session API

### Session Struct Extensions

The `Session` struct in Golang has been extended with VPC-specific functionality:

#### IsVpc()

```go
func (s *Session) IsVpc() bool
```

Return whether this session uses VPC resources.

**Returns:**
- `bool`: True if the session is a VPC session, False otherwise.

#### NetworkInterfaceIp()

```go
func (s *Session) NetworkInterfaceIp() string
```

Return the network interface IP for VPC sessions.

**Returns:**
- `string`: The network interface IP address for VPC sessions.

#### HttpPort()

```go
func (s *Session) HttpPort() string
```

Return the HTTP port for VPC sessions.

**Returns:**
- `string`: The HTTP port for VPC sessions.

### VPC Session Creation

To create a VPC session in Golang, use the `WithIsVpc` method in `CreateSessionParams`:

```go
package main

import (
    "fmt"
    "github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

func main() {
    // Initialize the SDK
    client, err := agentbay.NewAgentBay("your_api_key")
    if err != nil {
        fmt.Printf("Error: %v\n", err)
        return
    }

    // Create a VPC session
    params := agentbay.NewCreateSessionParams().
        WithImageId("imgc-07eksy57nw6r759fb").
        WithIsVpc(true).
        WithLabels(map[string]string{"environment": "vpc-test"})

    sessionResult, err := client.Create(params)
    if err != nil {
        fmt.Printf("Error: %v\n", err)
        return
    }

    if sessionResult.Success {
        session := sessionResult.Session
        fmt.Printf("VPC Session created: %v\n", session.IsVpc())  // true
    }
}
```

## CreateSessionParams Extensions

All three language implementations have been extended to support VPC session creation:

### Python

```python
class CreateSessionParams:
    def __init__(
        self,
        # ... other parameters ...
        is_vpc: Optional[bool] = None,
    ):
        # ... other initialization ...
        self.is_vpc = is_vpc if is_vpc is not None else False

# Usage:
params = CreateSessionParams(is_vpc=True)
```

### TypeScript

```typescript
class CreateSessionParams {
    public isVpc: boolean;
    
    constructor() {
        // ... other initialization ...
        this.isVpc = false;
    }
    
    withIsVpc(isVpc: boolean): CreateSessionParams {
        this.isVpc = isVpc;
        return this;
    }
}

// Usage:
const params = new CreateSessionParams().withIsVpc(true);
```

### Golang

```go
type CreateSessionParams struct {
    // ... other fields ...
    IsVpc bool
}

func NewCreateSessionParams() *CreateSessionParams {
    return &CreateSessionParams{
        // ... other initialization ...
        IsVpc: false,
    }
}

func (p *CreateSessionParams) WithIsVpc(isVpc bool) *CreateSessionParams {
    p.IsVpc = isVpc
    return p
}

// Usage:
params := NewCreateSessionParams().WithIsVpc(true)
```

## VPC Session Capabilities

VPC sessions have different capabilities compared to standard sessions:

### Available Modules
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

### Unavailable Modules
1. **Code**: Code execution module
2. **UI**: UI interaction module
3. **Window**: Window management module
4. **Application**: Application management module
5. **OSS**: Object Storage Service module

## Best Practices

1. **Module Awareness**: Always check if a module is available in VPC sessions before using it
2. **Error Handling**: Implement proper error handling for VPC-specific operations
3. **Resource Management**: Clean up VPC sessions properly to avoid resource waste
4. **Security**: Use VPC sessions for sensitive operations that require network isolation
5. **Networking**: Ensure proper VPC networking configuration for optimal performance

## Limitations

1. **Module Limitations**: Only a subset of modules are available in VPC sessions
2. **Image Requirements**: Specific image IDs may be required for VPC sessions
3. **Networking**: VPC sessions have different networking characteristics
4. **Performance**: VPC sessions may have different performance characteristics

## Troubleshooting

### Common Issues

1. **Session Creation Failures**:
   - Verify your API key has VPC session permissions
   - Check if you've reached VPC session limits
   - Ensure the specified image ID is valid for VPC sessions

2. **Module Unavailability**:
   - Check that you're not trying to use unavailable modules
   - Verify session creation parameters include `is_vpc=true`

3. **Networking Problems**:
   - Verify VPC networking and security group configurations
   - Check resource permissions and access controls