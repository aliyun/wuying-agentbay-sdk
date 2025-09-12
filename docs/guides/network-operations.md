# Network Operations Guide

This guide provides comprehensive guidance on using network management capabilities in the AgentBay Go SDK, including network creation, status monitoring, and lifecycle management.

> **Important**: Network functionality is only available with custom images (imgc-xxxxx format) and when the advanced network option is selected during session creation.

## 📋 Table of Contents

- [Network Operations Guide](#network-operations-guide)
  - [📋 Table of Contents](#-table-of-contents)
  - [🎯 Core Concepts](#-core-concepts)
    - [What is Network Management?](#what-is-network-management)
    - [Complete Network Workflow](#complete-network-workflow)
      - [1. Network Creation](#1-network-creation)
      - [2. Local Client Setup](#2-local-client-setup)
      - [3. Session Creation](#3-session-creation)
      - [4. Tool Execution](#4-tool-execution)
      - [5. Session Release](#5-session-release)
      - [6. Network Status Query](#6-network-status-query)
    - [Key Components](#key-components)
      - [Network ID (NetworkId)](#network-id-networkid)
      - [Network Token (NetworkToken)](#network-token-networktoken)
      - [Online Status](#online-status)
  - [📚 API Quick Reference](#-api-quick-reference)
    - [Session Integration](#session-integration)
  - [📡 Network Creation](#-network-creation)
    - [Basic Network Creation](#basic-network-creation)
  - [📊 Network Status Monitoring](#-network-status-monitoring)
    - [Basic Status Query](#basic-status-query)
  - [🔗 Session Integration](#-session-integration)
    - [Creating Sessions with Specific Networks](#creating-sessions-with-specific-networks)
    - [Complete End-to-End Example](#complete-end-to-end-example)
  - [📝 Summary](#-summary)

<a id="core-concepts"></a>
## 🎯 Core Concepts

### What is Network Management?

AgentBay's network management functionality provides a complete network redirection solution for cloud computing environments. The complete workflow includes:

- **Network Creation**: Create or retrieve advanced office networks with redirection capabilities
- **Local Client Setup**: Use network tokens to establish local redirection services
- **Session Integration**: Create cloud sessions that can access local services through network redirection
- **Tool Execution**: Execute MCP tools in cloud sessions with local network access
- **Lifecycle Management**: Manage the complete network and session lifecycle

### Complete Network Workflow

The network functionality follows a comprehensive workflow that enables cloud sessions to access local services through network redirection:

#### 1. Network Creation
```go
// Create or retrieve advanced office network
result, err := agentBay.Network.CreateNetwork(nil) // or with specific networkId
// Returns: networkId, token
```
- **Purpose**: Create or retrieve user's advanced office network ID
- **Result**: Network resources are created/retrieved, returning networkId and token
- **Note**: Success doesn't depend on actual network creation status

#### 2. Local Client Setup
```bash
# Use token to start local redirection service
./rick-cli -m bind -t <network-token>
./rick-cli
```
- **Purpose**: Establish local redirection service using the network token
- **Result**: Local client is ready to receive redirected network traffic

#### 3. Session Creation
```go
// Create session with network redirection
params := agentbay.NewCreateSessionParams().
    WithImageId("imgc-12345678").  // Custom image required
    WithNetworkId(networkId)       // Specify network for redirection

sessionResult, err := agentBay.Create(params)
```
- **Purpose**: Create cloud session with network redirection capabilities
- **Network Update**: Updates network configuration with session IP list
- **Error Handling**: If redirection network fails, session creation will error with specific message

#### 4. Tool Execution
```go
// Execute MCP tools with local network access
result, err := session.CallMcpTool("tool-name", args)
```
- **Purpose**: Execute tools in cloud session with access to local services
- **Network Access**: Tools can access local services through network redirection
- **Error Handling**: If redirection network fails, tool calls will error with exception

#### 5. Session Release
```go
// Release session and update network configuration
deleteResult, err := agentBay.Delete(session)
```
- **Purpose**: Clean up session resources
- **Network Update**: Updates network configuration to remove session IP from list

#### 6. Network Status Query
```go
// Query network status and configuration
result, err := agentBay.Network.DescribeNetwork(networkId)
```
- **Purpose**: Check network status and configuration
- **Information**: Returns network online status and other details

### Key Components

#### Network ID (NetworkId)
- **Definition**: Unique identifier for a network instance
- **Format**: String typically starting with "net-"
- **Usage**: Required for all network operations after creation

#### Network Token (NetworkToken)
- **Definition**: Security credential for network access
- **Format**: Encrypted token string
- **Purpose**: Used for secure network authentication

#### Online Status
- **Type**: Boolean value
- **Meaning**: Indicates whether the network is ready for use
- **Usage**: Check before using network for operations

<a id="api-quick-reference"></a>
## 📚 API Quick Reference

```go
package main

import (
    "fmt"
    "log"
    
    "github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
    "github.com/alibabacloud-go/tea/tea"
)

func main() {
    // Initialize client
    agentBay, err := agentbay.NewAgentBay("your-api-key")
    if err != nil {
        log.Fatal(err)
    }

    // Create new network (auto-generated ID)
    createResult, err := agentBay.Network.CreateNetwork(nil)
    if err == nil && createResult.Success && createResult.NetworkInfo != nil {
        networkID := createResult.NetworkInfo.NetworkID
        networkToken := createResult.NetworkInfo.NetworkToken
        fmt.Printf("Network ID: %s, Token: %s\n", networkID, networkToken)
    }

    // Retrieve token for existing network
    tokenResult, err := agentBay.Network.CreateNetwork(tea.String("net-existing-123456"))
    if err == nil && tokenResult.Success && tokenResult.NetworkInfo != nil {
        token := tokenResult.NetworkInfo.NetworkToken
        fmt.Printf("Token: %s\n", token)
    }

    // Query network status
    describeResult, err := agentBay.Network.DescribeNetwork(networkID)
    if err == nil && describeResult.Success && describeResult.NetworkInfo != nil {
        if describeResult.NetworkInfo.Online != nil {
            onlineStatus := *describeResult.NetworkInfo.Online
            fmt.Printf("Online: %v\n", onlineStatus)
        }
    }
}
```

### Session Integration
```go
import "github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"

// Create session with specific network
// Requirements: Custom image (imgc-xxxxx) + Advanced network option
params := agentbay.NewCreateSessionParams().
    WithImageId("imgc-12345678").  // Must use custom image with advanced network option
    WithNetworkId(networkID).      // Existing network ID
    WithLabels(map[string]string{  // Optional labels
        "network": "enabled",
        "project": "demo",
    })

sessionResult, err := agentBay.Create(params)
if err != nil {
    // Expected error with standard images: "NetworkId not supported"
    log.Printf("Session creation failed: %v", err)
} else if sessionResult.Session != nil {
    fmt.Printf("✅ Session created with network: %s\n", sessionResult.Session.SessionID)
}
```

<a id="network-creation"></a>
## 📡 Network Creation

### Basic Network Creation

```go
package main

import (
    "fmt"
    "log"
    
    "github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

func main() {
    // Initialize AgentBay client
    agentBay, err := agentbay.NewAgentBay("")
    if err != nil {
        log.Fatal(err)
    }

    // Create network
    createResult, err := agentBay.Network.CreateNetwork(nil)
    if err != nil {
        log.Fatal(err)
    }

    if createResult.Success && createResult.NetworkInfo != nil {
        networkInfo := createResult.NetworkInfo
        fmt.Printf("Network ID: %s\n", networkInfo.NetworkID)
        fmt.Printf("Network Token: %s\n", networkInfo.NetworkToken)
    } else {
        fmt.Printf("Network creation failed: %s\n", createResult.ErrorMessage)
    }
}
```

<a id="network-status-monitoring"></a>
## 📊 Network Status Monitoring

### Basic Status Query

Query network details and status:

```go
// Query network status
describeResult, err := agentBay.Network.DescribeNetwork("net-123456")
if err != nil {
    log.Fatal(err)
}

if describeResult.Success && describeResult.NetworkInfo != nil {
    networkInfo := describeResult.NetworkInfo
    fmt.Printf("Network ID: %s\n", networkInfo.NetworkID)
    if networkInfo.Online != nil {
        fmt.Printf("Online: %v\n", *networkInfo.Online)
    } else {
        fmt.Println("Online: Unknown")
    }
} else {
    fmt.Printf("Query failed: %s\n", describeResult.ErrorMessage)
}
```

<a id="session-integration"></a>
## 🔗 Session Integration

### Creating Sessions with Specific Networks

Associate a network with a new session:

```go
import (
    "fmt"
    "log"
    
    "github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

func createSessionWithNetwork(agentBay *agentbay.AgentBay, networkID string) *agentbay.Session {
    // Create a session using a specific network
    params := agentbay.NewCreateSessionParams().
        WithImageId("imgc-12345678").  // Custom image required
        WithNetworkId(networkID).      // Network ID from previous creation
        WithLabels(map[string]string{
            "network": "enabled",
            "environment": "production",
        })
    
    sessionResult, err := agentBay.Create(params)
    if err != nil {
        fmt.Printf("Session creation error: %v\n", err)
        return nil
    }
    
    if sessionResult != nil && sessionResult.Session != nil {
        return sessionResult.Session
    } else {
        fmt.Printf("Session creation failed or returned nil result\n")
        return nil
    }
}

// Usage
session := createSessionWithNetwork(agentBay, "net-123456")
```

### Complete End-to-End Example

Here's a complete example following the proper workflow from network creation to tool execution:

```go
package main

import (
    "fmt"
    "log"
    "os"
    
    "github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

func main() {
    fmt.Println("🚀 Complete Network Redirection Workflow")
    fmt.Println("========================================")
    
    // Initialize AgentBay client
    agentBay, err := agentbay.NewAgentBay("")
    if err != nil {
        log.Fatalf("Failed to create AgentBay client: %v", err)
    }
    
    // Step 1: Create Network
    fmt.Println("\n📡 Step 1: Creating advanced office network...")
    networkResult, err := agentBay.Network.CreateNetwork(nil)
    if err != nil {
        log.Fatalf("Failed to create network: %v", err)
    }
    
    if !networkResult.Success || networkResult.NetworkInfo == nil {
        log.Fatalf("Network creation failed: %s", networkResult.ErrorMessage)
    }
    
    networkID := networkResult.NetworkInfo.NetworkID
    networkToken := networkResult.NetworkInfo.NetworkToken
    fmt.Printf("✅ Advanced office network ready!\n")
    fmt.Printf("   Network ID: %s\n", networkID)
    fmt.Printf("   Network Token: %s\n", networkToken)
    fmt.Printf("   Note: Network creation success doesn't depend on actual network status\n")
    
    // Step 2: Setup Local Redirection
    fmt.Println("\n🔧 Step 2: Setting up local redirection service...")
    fmt.Printf("   Run these commands on your local client:\n")
    fmt.Printf("   $ ./rick-cli -m bind -t %s\n", networkToken)
    fmt.Printf("   $ ./rick-cli\n")
    fmt.Printf("   ✅ Local redirection service should now be running\n")
    
    // Step 3: Create Session with Network
    fmt.Println("\n🔗 Step 3: Creating session with network redirection...")
    fmt.Println("   This will update network configuration with session IP list")
    
    sessionParams := agentbay.NewCreateSessionParams().
        WithImageId("imgc-12345678").  // Custom image required for network functionality
        WithNetworkId(networkID).      // Enable network redirection
        WithLabels(map[string]string{
            "workflow": "network-redirection",
            "network": "enabled",
        })
    
    sessionResult, err := agentBay.Create(sessionParams)
    if err != nil {
        fmt.Printf("⚠️  Session creation failed (expected with test image): %v\n", err)
        fmt.Println("\n💡 In production:")
        fmt.Println("   - Use a real custom image ID (imgc-xxxxxxxxx)")
        fmt.Println("   - Ensure advanced network option is enabled for the image")
        fmt.Println("   - If redirection network fails, session creation will error")
        return
    }
    
    if sessionResult != nil && sessionResult.Session != nil {
        session := sessionResult.Session
        fmt.Printf("✅ Session created with network redirection!\n")
        fmt.Printf("   Session ID: %s\n", session.SessionID)
        fmt.Printf("   Network configuration updated with session IP\n")
        
        // Step 4: Execute Tools with Local Network Access
        fmt.Println("\n🛠️  Step 4: Executing MCP tools with local network access...")
        fmt.Printf("   Tools in this session can now access local services\n")
        fmt.Printf("   Example: session.CallMcpTool(\"local-service-tool\", args)\n")
        fmt.Printf("   Note: If redirection network fails, tool calls will error\n")
        
        // Step 5: Query Network Status
        fmt.Println("\n🔍 Step 5: Querying network status...")
        statusResult, err := agentBay.Network.DescribeNetwork(networkID)
        if err != nil {
            fmt.Printf("⚠️  Network status query failed: %v\n", err)
        } else if statusResult.Success && statusResult.NetworkInfo != nil {
            if statusResult.NetworkInfo.Online != nil {
                status := map[bool]string{true: "🟢 Online", false: "🔴 Offline"}[*statusResult.NetworkInfo.Online]
                fmt.Printf("✅ Network status: %s\n", status)
            } else {
                fmt.Printf("⚪ Network status: Unknown\n")
            }
        } else {
            fmt.Printf("⚠️  Network status unavailable: %s\n", statusResult.ErrorMessage)
        }
        
        // Step 6: Release Session
        fmt.Println("\n🧹 Step 6: Releasing session...")
        fmt.Printf("   This will update network configuration to remove session IP\n")
        
        deleteResult, err := agentBay.Delete(session)
        if err != nil {
            fmt.Printf("⚠️  Warning: Failed to delete session: %v\n", err)
        } else {
            fmt.Printf("✅ Session released successfully (Request ID: %s)\n", deleteResult.RequestID)
            fmt.Printf("   Network configuration updated\n")
        }
    }
    
    fmt.Println("\n🎉 Complete network redirection workflow finished!")
    fmt.Println("\n📋 Workflow Summary:")
    fmt.Printf("   1. ✅ Network created: %s\n", networkID)
    fmt.Printf("   2. ✅ Token obtained: %s\n", networkToken)
    fmt.Printf("   3. 🔧 Local redirection: Ready to setup with Rick plugin\n")
    fmt.Printf("   4. 🔗 Session integration: Ready for custom images\n")
    fmt.Printf("   5. 🛠️  Tool execution: Ready for local service access\n")
    fmt.Printf("   6. 🧹 Cleanup: Network configuration managed automatically\n")
}
```

## 📝 Summary

This guide covers the basic network operations available in AgentBay Go SDK:

- **Network Creation**: Use `agentBay.Network.CreateNetwork(nil)` to create new networks
- **Status Query**: Use `agentBay.Network.DescribeNetwork(networkID)` to check network status
- **Session Integration**: Pass `networkId` when creating sessions to associate networks
- **Rick Plugin Integration**: Use network tokens with the Rick plugin to enable network redirection from cloud sessions to local client environment

**Use Case**: The network functionality is particularly powerful when combined with the Rick plugin, enabling hybrid development workflows where cloud compute resources can seamlessly access local development services through secure network redirection.

For more details, refer to the API documentation.