# Network Redirection Example

This example demonstrates how to use AgentBay's network redirection functionality to route cloud session traffic through your local network IP, preventing account suspensions caused by cloud IP reputation issues.

## 🎯 Problem Solved
Cloud-based AI operations often trigger account suspensions because services detect and block requests from cloud data center IPs. This example shows how to route all traffic through your trusted local IP address.

> **Note**: Network functionality is only available with custom images (imgc-xxxxx format) and when the advanced network option is selected.

## Features

- **Network Redirection Setup**: Create network redirection infrastructure
- **Local IP Routing**: Route cloud traffic through your local network
- **Status Monitoring**: Query network redirection status
- **Session Integration**: Create sessions that appear to originate from your local IP

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

### Step 1: Network Redirection Setup

```go
// Create network redirection infrastructure
result, err := agentBay.Network.CreateNetwork(nil)
if err != nil {
    log.Fatal(err)
}

if result.Success && result.NetworkInfo != nil {
    networkID := result.NetworkInfo.NetworkID
    networkToken := result.NetworkInfo.NetworkToken
    fmt.Printf("Network ID: %s\n", networkID)
    fmt.Printf("Token: %s (use with Rick Plugin)\n", networkToken)
}
```

### Step 2: Local Redirection Setup

```bash
# Use network token with Rick Plugin to establish redirection
./rick-cli -m bind -t <network-token>
./rick-cli
```

### Step 3: Network Status Query (After Rick Plugin Setup)

```go
// Query network redirection status - will show Online after Rick Plugin starts
result, err := agentBay.Network.DescribeNetwork(networkID)
if err != nil {
    log.Fatal(err)
}

if result.Success && result.NetworkInfo != nil {
    if result.NetworkInfo.Online != nil {
        fmt.Printf("Online: %v\n", *result.NetworkInfo.Online)
        // Network shows as Online only when Rick Plugin is running
    }
}
```

### Step 4: Session Creation with Network Redirection

```go
// Create session that routes traffic through your local IP
sessionParams := agentbay.NewCreateSessionParams().
    WithImageId("imgc-12345678"). // Custom image required
    WithNetworkId(networkID).     // Enable network redirection
    WithLabels(map[string]string{
        "purpose": "ip-reputation-protection",
        "network": "redirection-enabled",
    })

sessionResult, err := agentBay.Create(sessionParams)
if err != nil {
    // Expected with test images - will work with real custom images
    fmt.Printf("Error: %v\n", err)
} else {
    fmt.Printf("Session created with network redirection: %s\n", sessionResult.Session.SessionID)
    // All operations in this session will appear to come from your local IP
}
```

## API Reference

### NetworkManager Struct

- `CreateNetwork(networkID *string) (*CreateNetworkResult, error)`: Create network redirection infrastructure
- `DescribeNetwork(networkID string) (*DescribeNetworkResult, error)`: Query network redirection status

## Benefits

- ✅ **Prevent Account Suspensions**: Avoid blocks from cloud IP reputation issues
- ✅ **Consistent IP Identity**: All AI operations appear from your trusted local IP
- ✅ **Transparent Integration**: No application code changes required
- ✅ **Enhanced Reliability**: Reduce service interruptions and rate limiting

## Important Notes

1. **API Key**: Ensure a valid AGENTBAY_API_KEY environment variable is set
2. **Image Requirements**: Must use custom image (imgc-xxxxx format) with advanced network option
3. **Rick Plugin**: Required for establishing local redirection tunnel
4. **Use Cases**: Ideal for AI automation, web scraping, account management scenarios
