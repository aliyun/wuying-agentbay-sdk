# Golang SDK for Wuying AgentBay

This directory contains the Golang implementation of the Wuying AgentBay SDK.

## Prerequisites

- Go 1.18 or later

## Installation

### For Development

Clone the repository and navigate to the Golang directory:

```bash
git clone https://github.com/aliyun/wuying-agentbay-sdk.git
cd wuying-agentbay-sdk/golang
```

### For Usage in Your Project

```bash
go get github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay
```

## Running Examples

You can find examples in the `docs/examples/golang` directory, including:

- Basic SDK usage
- Application window management
- Command execution
- Context management
- Context synchronization
- File system operations
- Session parameter configuration
- UI interaction

To run the examples:

```bash
go run docs/examples/golang/basic_usage/main.go
```

## Golang-Specific Usage

```go
package main

import (
	"fmt"
	"os"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

func main() {
	// Initialize with API key
	apiKey := os.Getenv("AGENTBAY_API_KEY")
	if apiKey == "" {
		apiKey = "your_api_key" // Replace with your actual API key
	}

	// Create client with configuration options
	client, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		fmt.Printf("Error initializing AgentBay client: %v\n", err)
		os.Exit(1)
	}

	// Create a session with parameters
	params := agentbay.NewCreateSessionParams()
	params.ImageId = "linux_latest"
	params.Labels = map[string]string{
		"purpose": "demo",
		"environment": "development",
	}
	
	session, err := client.Create(params)
	if err != nil {
		fmt.Printf("Error creating session: %v\n", err)
		os.Exit(1)
	}
	
	// Execute a command
	commandResult, err := session.Session.Command.ExecuteCommand("ls -la")
	if err != nil {
		fmt.Printf("Error executing command: %v\n", err)
		os.Exit(1)
	}
	
	// File system operations
	fileContent, err := session.Session.FileSystem.ReadFile("/etc/hosts")
	if err != nil {
		fmt.Printf("Error reading file: %v\n", err)
	}
	
	// Run code
	codeResult, err := session.Session.Code.RunCode("print('Hello, World!')", "python")
	if err != nil {
		fmt.Printf("Error running code: %v\n", err)
	}
	
	// Application management
	appsResult, err := session.Session.Application.GetInstalledApps(true, false, true)
	if err != nil {
		fmt.Printf("Error getting installed apps: %v\n", err)
	}
	
	// Window management
	windowsResult, err := session.Session.Window.ListRootWindows()
	if err != nil {
		fmt.Printf("Error listing windows: %v\n", err)
	}
	
	// UI operations
	screenshotResult, err := session.Session.UI.Screenshot()
	if err != nil {
		fmt.Printf("Error taking screenshot: %v\n", err)
	}
	
	// Context management
	contextsResult, err := client.Context.List()
	if err != nil {
		fmt.Printf("Error listing contexts: %v\n", err)
	}
	
	// Clean up
	err = client.Delete(session.Session)
	if err != nil {
		fmt.Printf("Error deleting session: %v\n", err)
	}
}
```

## Key Features

### Session Management

- Create sessions with optional parameters (ImageId, ContextID, Labels)
- List sessions with pagination and filtering by labels
- Delete sessions and clean up resources
- Manage session labels
- Get session information and links

### Command Execution

- Execute shell commands
- Run code in various languages
- Get command output and execution status

### File System Operations

- Read and write files
- List directory contents
- Create and delete files and directories
- Get file information

### UI Interaction

- Take screenshots
- Find UI elements by criteria
- Click on UI elements
- Send text input
- Perform swipe gestures
- Send key events (HOME, BACK, MENU, etc.)

### Application Management

- Get installed applications
- List running applications
- Start and stop applications
- Get application information

### Window Management

- List windows
- Get active window
- Focus, resize, and move windows
- Get window properties

### Context Management

- Create, list, and delete contexts
- Bind sessions to contexts
- Synchronize context data using policies
- Get context information

### OSS Integration

- Upload files to OSS
- Download files from OSS
- Initialize OSS environment

## Response Format

All API methods return responses that include:

- RequestID: A unique identifier for the request
- ApiResponse embedded structure that tracks success/failure
- Operation-specific data (varies by method)

## Development

### Building the SDK

```bash
go build ./...
```

### Running Tests

```bash
go test ./...
```

For more detailed documentation, refer to the [SDK Documentation](../docs/README.md).
