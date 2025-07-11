# Session Struct

The `Session` struct represents a session in the AgentBay cloud environment. It provides methods for managing file systems, executing commands, and more.

## Properties

```go
SessionID  // The ID of this session
ResourceURL  // The URL of the resource associated with this session
FileSystem  // The FileSystem instance for this session
Command  // The Command instance for this session
Oss  // The Oss instance for this session
Application  // The ApplicationManager instance for this session
Window  // The WindowManager instance for this session
UI  // The UI instance for this session
Context  // The ContextManager instance for this session
```

## Methods

### Delete

Deletes this session.

```go
Delete() (*DeleteResult, error)
```

**Returns:**
- `*DeleteResult`: A result object containing success status and RequestID.
- `error`: An error if the session deletion fails.

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
	
	// Delete the session when done
	deleteResult, err := session.Delete()
	if err != nil {
		fmt.Printf("Error deleting session: %v\n", err)
		os.Exit(1)
	}
	
	fmt.Println("Session deleted successfully")
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
GetLabels() (map[string]string, error)
```

**Returns:**
- `map[string]string`: The labels for the session.
- `error`: An error if getting labels fails.

**Example:**
```go
// Get session labels
labels, err := session.GetLabels()
if err != nil {
	fmt.Printf("Error getting labels: %v\n", err)
	os.Exit(1)
}

fmt.Println("Session labels:")
for key, value := range labels {
	fmt.Printf("%s: %s\n", key, value)
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

## Related Resources

- [FileSystem API Reference](filesystem.md)
- [Command API Reference](command.md)
- [UI API Reference](ui.md)
- [Window API Reference](window.md)
- [OSS API Reference](oss.md)
- [Application API Reference](application.md)
- [Context API Reference](context-manager.md) 