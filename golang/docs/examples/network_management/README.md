# Network Management Example

This example demonstrates how to use the network management functionality of the AgentBay SDK.

> **Note**: Network functionality is only available with custom images (imgc-xxxxx format) and when the advanced network option is selected.

## Features

- **Network Creation**: Create network environments
- **Network Query**: Query network status

## Running the Example

1. Install dependencies:
```bash
go mod tidy
```

2. Set API key:
```bash
export AGENTBAY_API_KEY=your_api_key_here
```

3. Run the example:
```bash
go run main.go
```

## Code Explanation

### Step 1: Network Creation

```go
// Create new network
result, err := agentBay.Network.CreateNetwork(nil)
if err != nil {
    log.Fatal(err)
}

if result.Success && result.NetworkInfo != nil {
    networkID := result.NetworkInfo.NetworkID
    fmt.Printf("Network ID: %s\n", networkID)
    fmt.Printf("Token: %s\n", result.NetworkInfo.NetworkToken)
}
```

### Step 2: Network Query

```go
// Query network status
result, err := agentBay.Network.DescribeNetwork(networkID)
if err != nil {
    log.Fatal(err)
}

if result.Success && result.NetworkInfo != nil {
    if result.NetworkInfo.Online != nil {
        fmt.Printf("Online: %v\n", *result.NetworkInfo.Online)
    }
}
```

### Step 3: Using Network in Session Creation

```go
// Create session with network functionality
sessionParams := agentbay.NewCreateSessionParams().
    WithImageId("imgc-12345678"). // Custom image required
    WithNetworkId(networkID).     // Use the created network
    WithLabels(map[string]string{"network": "enabled"})

sessionResult, err := agentBay.Create(sessionParams)
if err != nil {
    // Will fail with standard images like linux_latest
    fmt.Printf("Error: %v\n", err)
} else {
    fmt.Printf("Session created with network: %s\n", sessionResult.Session.SessionID)
}
```

## API Reference

### NetworkManager Struct

- `CreateNetwork(networkID *string) (*CreateNetworkResult, error)`: Create new network
- `DescribeNetwork(networkID string) (*DescribeNetworkResult, error)`: Query network status

## Important Notes

1. **API Key**: Ensure a valid AGENTBAY_API_KEY environment variable is set
2. **Image Requirements**: Must use custom image (imgc-xxxxx format) with advanced network option
