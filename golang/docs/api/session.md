# Session Struct

The `Session` struct represents a session in the AgentBay cloud environment. It provides methods for managing file systems, executing commands, and more.

## Properties

```go
AgentBay  // The AgentBay client instance
SessionID  // The ID of this session
ImageId  // The image ID used when creating this session
IsVpcEnabled  // Whether this session uses VPC resources
NetworkInterfaceIP  // Network interface IP for VPC sessions
HttpPortNumber  // HTTP port for VPC sessions
FileSystem  // The FileSystem instance for this session
Command  // The Command instance for this session
Code  // The Code instance for this session
Oss  // The Oss instance for this session
UI  // The UI instance for this session
Application  // The ApplicationManager instance for this session
Window  // The WindowManager instance for this session
Agent  // The Agent instance for this session
Context  // The ContextManager instance for this session
McpTools  // MCP tools available for this session
```

**Accessor Methods:**
```go
IsVpc() bool  // Returns whether this session uses VPC resources
NetworkInterfaceIp() string  // Returns the network interface IP for VPC sessions
HttpPort() string  // Returns the HTTP port for VPC sessions
```

## Methods

### Delete

Deletes this session.

```go
Delete(syncContext ...bool) (*DeleteResult, error)
```

**Parameters:**
- `syncContext` (bool, optional): If true, the API will trigger a file upload via `Context.Sync()` before actually releasing the session. Default is false.

**Returns:**
- `*DeleteResult`: A result object containing success status and RequestID.
- `error`: An error if the session deletion fails.

**Behavior:**
- When `syncContext` is true, the API will first call `Context.Sync()` to trigger file upload.
- It will then check `Context.Info()` to retrieve ContextStatusData and monitor only upload task items' Status.
- The API waits until all upload tasks show either "Success" or "Failed" status, or until the maximum retry limit (150 times with 2-second intervals) is reached.
- Any "Failed" status upload tasks will have their error messages printed.
- The session deletion only proceeds after context sync status checking for upload tasks completes.

**Example:**
```go
package main

import (
	"fmt"
	"os"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

func main() {
	// Initialize the SDK
	client, err := agentbay.NewAgentBay("your_api_key", nil)
	if err != nil {
		fmt.Printf("Error initializing AgentBay client: %v\n", err)
		os.Exit(1)
	}

	// Create a session
	createResult, err := client.Create(nil)
	if err != nil {
		fmt.Printf("Error creating session: %v\n", err)
		os.Exit(1)
	}
	
	session := createResult.Session
	fmt.Printf("Session created with ID: %s\n", session.SessionID)
	
	// Use the session...
	
	// Delete the session with context synchronization
	deleteResult, err := session.Delete(true)
	if err != nil {
		fmt.Printf("Error deleting session: %v\n", err)
		os.Exit(1)
	}
	
	fmt.Println("Session deleted successfully with synchronized context")
	fmt.Printf("Request ID: %s\n", deleteResult.RequestID)
}
```

### SetLabels

Sets labels for this session.

```go
SetLabels(labels map[string]string) (*models.Response, error)
```

**Parameters:**
- `labels` (map[string]string): Key-value pairs representing the labels to set.

**Returns:**
- `*models.Response`: A response object containing RequestID and status information.
- `error`: An error if setting labels fails.

**Example:**
```go
// Set session labels
labels := map[string]string{
	"project":     "demo",
	"environment": "testing",
	"version":     "1.0.0",
}

response, err := session.SetLabels(labels)
if err != nil {
	fmt.Printf("Error setting labels: %v\n", err)
	os.Exit(1)
}

fmt.Println("Labels set successfully")
fmt.Printf("Request ID: %s\n", response.RequestID)
```

### GetLabels

Gets the labels for this session.

```go
GetLabels() (*LabelResult, error)
```

**Returns:**
- `*LabelResult`: A result object containing the labels data, request ID, and success status.
- `error`: An error if getting labels fails.

**Example:**
```go
// Get session labels
result, err := session.GetLabels()
if err != nil {
	fmt.Printf("Error getting labels: %v\n", err)
	os.Exit(1)
}

if result.Success {
	fmt.Println("Session labels:")
	// Parse the labels JSON string
	var labels map[string]string
	if err := json.Unmarshal([]byte(result.Labels), &labels); err == nil {
		for key, value := range labels {
			fmt.Printf("%s: %s\n", key, value)
		}
	}
} else {
	fmt.Printf("Failed to get labels: %s\n", result.ErrorMessage)
}
```

### Info

Gets information about this session.

```go
Info() (*SessionInfo, error)
```

**Returns:**
- `*SessionInfo`: An object containing information about the session.
- `error`: An error if getting session information fails.

**Example:**
```go
// Get session information
info, err := session.Info()
if err != nil {
	fmt.Printf("Error getting session info: %v\n", err)
	os.Exit(1)
}

fmt.Printf("Session ID: %s\n", info.SessionID)
fmt.Printf("Resource URL: %s\n", info.ResourceURL)
fmt.Printf("App ID: %s\n", info.AppID)
```

### GetLink

Gets a link for this session.

```go
GetLink(protocolType string, port int) (string, error)
```

**Parameters:**
- `protocolType` (string): The protocol type for the link. If empty, the default protocol will be used.
- `port` (int): The port for the link. If 0, the default port will be used.

**Returns:**
- `string`: The link for the session.
- `error`: An error if getting the link fails.

**Example:**
```go
// Get session link with default protocol and port
link, err := session.GetLink("", 0)
if err != nil {
	fmt.Printf("Error getting link: %v\n", err)
	os.Exit(1)
}

fmt.Printf("Session link: %s\n", link)

// Get link with specific protocol and port
customLink, err := session.GetLink("https", 8443)
if err != nil {
	fmt.Printf("Error getting custom link: %v\n", err)
	os.Exit(1)
}

fmt.Printf("Custom link: %s\n", customLink)
```

### ListMcpTools

Lists MCP tools available for this session.

```go
ListMcpTools() (*McpToolsResult, error)
```

**Returns:**
- `*McpToolsResult`: A result object containing the list of MCP tools and request ID.
- `error`: An error if listing MCP tools fails.

**Example:**
```go
// List MCP tools
toolsResult, err := session.ListMcpTools()
if err != nil {
	fmt.Printf("Error listing MCP tools: %v\n", err)
	os.Exit(1)
}

fmt.Printf("Found %d MCP tools\n", len(toolsResult.Tools))
for _, tool := range toolsResult.Tools {
	fmt.Printf("Tool: %s - %s\n", tool.Name, tool.Description)
}
```

## Related Resources

- [FileSystem API Reference](filesystem.md)
- [Command API Reference](command.md)
- [UI API Reference](ui.md)
- [Window API Reference](window.md)
- [OSS API Reference](oss.md)
- [Application API Reference](application.md)
- [Context API Reference](context-manager.md) 