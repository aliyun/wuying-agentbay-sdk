# NetworkManager API Reference

The `NetworkManager` struct provides network management functionality, including creating networks and querying network details.

> **Important**: Network operations (CreateNetwork/DescribeNetwork) are **independent of sessions**. You can create and query networks without creating any sessions. Networks are only used when creating sessions with the `WithNetworkId()` parameter.

> **Note**: Using networks in sessions requires custom images (imgc-xxxxx format) and the advanced network option to be selected.

## Structs and Methods

### NetworkManager

Network manager struct that provides high-level interfaces for network-related operations.

#### Methods

##### CreateNetwork(networkID *string) (*CreateNetworkResult, error)

Create a new network or retrieve token for an existing network.

**Parameters:**
- `networkID` (*string): Existing network ID to retrieve token for. If nil, creates a new network with auto-generated ID.

**Returns:**
- `*CreateNetworkResult`: Result object containing network information and token
- `error`: Error if the operation fails

**Example:**
```go
package main

import (
    "fmt"
    "log"
    
    "github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

func main() {
    agentBay, err := agentbay.NewAgentBay("your-api-key")
    if err != nil {
        log.Fatal(err)
    }

    // Create new network
    result, err := agentBay.Network.CreateNetwork(nil)
    if err != nil {
        log.Fatal(err)
    }
    
    if result.Success && result.NetworkInfo != nil {
        networkID := result.NetworkInfo.NetworkID
        fmt.Printf("Network ID: %s\n", networkID)
        fmt.Printf("Network Token: %s\n", result.NetworkInfo.NetworkToken)
        
        // Step 2: Use network ID when creating session (optional)
        sessionParams := agentbay.NewCreateSessionParams().
            WithImageId("imgc-12345678"). // Custom image required
            WithNetworkId(networkID)
            
        sessionResult, err := agentBay.Create(sessionParams)
        if err != nil {
            log.Printf("Session creation failed: %v", err)
        } else {
            fmt.Printf("Session created with network: %s\n", sessionResult.Session.SessionID)
        }
    }
}
```

##### DescribeNetwork(networkID string) (*DescribeNetworkResult, error)

Query detailed information of the specified network.

**Parameters:**
- `networkID` (string): Network ID to query

**Returns:**
- `*DescribeNetworkResult`: Query result object
- `error`: Error if the operation fails

**Example:**
```go
// Query network details
result, err := agentBay.Network.DescribeNetwork("net-123456")
if err != nil {
    log.Fatal(err)
}

if result.Success && result.NetworkInfo != nil {
    fmt.Printf("Online: %v\n", *result.NetworkInfo.Online)
}
```

## Data Structs

### NetworkInfo

Network information struct containing detailed network information.

**Fields:**
- `NetworkID` (string): Network ID
- `NetworkToken` (string): Network token  
- `Online` (*bool): Online status (pointer to allow nil)

**Methods:**
- `NewNetworkInfoFromCreateResponse(data *CreateNetworkResponseBodyData) *NetworkInfo`: Create NetworkInfo from CreateNetwork response
- `NewNetworkInfoFromDescribeResponse(networkID string, data *DescribeNetworkResponseBodyData) *NetworkInfo`: Create NetworkInfo from DescribeNetwork response
- `ToMap() map[string]interface{}`: Convert to map
- `String() string`: String representation

### CreateNetworkResult

Result struct for create network operation.

**Fields:**
- `ApiResponse` (embedded): Contains RequestID
- `Success` (bool): Whether the operation was successful
- `NetworkInfo` (*NetworkInfo): Network information (when successful)
- `ErrorMessage` (string): Error message (when failed)

### DescribeNetworkResult

Result struct for describe network operation.

**Fields:**
- `ApiResponse` (embedded): Contains RequestID
- `Success` (bool): Whether the operation was successful
- `NetworkInfo` (*NetworkInfo): Network information (when successful)
- `ErrorMessage` (string): Error message (when failed)

## Error Handling

Network operations return errors through Go's standard error interface. It is recommended to use appropriate error handling:

```go
package main

import (
    "fmt"
    "log"
    
    "github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

func main() {
    agentBay, err := agentbay.NewAgentBay("your-api-key")
    if err != nil {
        log.Fatal(err)
    }
    
    result, err := agentBay.Network.CreateNetwork(nil)
    if err != nil {
        fmt.Printf("Network error: %v\n", err)
        return
    }
    
    if !result.Success {
        fmt.Printf("Operation failed: %s\n", result.ErrorMessage)
        return
    }
    
    fmt.Println("Network created successfully")
}
```

## Complete Example

```go
package main

import (
    "fmt"
    "log"
    
    "github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

func main() {
    fmt.Println("🚀 AgentBay Network Management Example")
    
    agentBay, err := agentbay.NewAgentBay("your-api-key")
    if err != nil {
        log.Fatal(err)
    }
    
    // 1. Create network
    fmt.Println("\n📡 Creating network...")
    createResult, err := agentBay.Network.CreateNetwork(nil)
    if err != nil {
        fmt.Printf("❌ Example execution failed: %v\n", err)
        return
    }
    
    if createResult.Success && createResult.NetworkInfo != nil {
        networkID := createResult.NetworkInfo.NetworkID
        fmt.Printf("✅ Network created successfully: %s\n", networkID)
        fmt.Printf("   Network token: %s\n", createResult.NetworkInfo.NetworkToken)
        
        // 2. Query network details
        fmt.Println("\n🔍 Querying network details...")
        describeResult, err := agentBay.Network.DescribeNetwork(networkID)
        if err != nil {
            fmt.Printf("❌ Failed to query network details: %v\n", err)
            return
        }
        
        if describeResult.Success && describeResult.NetworkInfo != nil {
            info := describeResult.NetworkInfo
            fmt.Println("✅ Network details:")
            fmt.Printf("   Network ID: %s\n", info.NetworkID)
            if info.Online != nil {
                fmt.Printf("   Online status: %s\n", map[bool]string{true: "Online", false: "Offline"}[*info.Online])
            } else {
                fmt.Println("   Online status: Unknown")
            }
        } else {
            fmt.Printf("❌ Failed to query network details: %s\n", describeResult.ErrorMessage)
        }
        
        // 3. Check network status
        fmt.Println("\n⏱️ Checking network status...")
        describeResult2, err := agentBay.Network.DescribeNetwork(networkID)
        if err != nil {
            fmt.Printf("Status check failed: %v\n", err)
            return
        }
        
        if describeResult2.Success && describeResult2.NetworkInfo != nil {
            if describeResult2.NetworkInfo.Online != nil {
                onlineStatus := *describeResult2.NetworkInfo.Online
                fmt.Printf("Network status: %s\n", map[bool]string{true: "Online", false: "Offline"}[onlineStatus])
                fmt.Printf("Network ready: %s\n", map[bool]string{true: "Yes", false: "No"}[onlineStatus])
            } else {
                fmt.Println("Network status: Unknown")
            }
        } else {
            fmt.Printf("Status check failed: %s\n", describeResult2.ErrorMessage)
        }
        
    } else {
        fmt.Printf("❌ Network creation failed: %s\n", createResult.ErrorMessage)
    }
}
```
