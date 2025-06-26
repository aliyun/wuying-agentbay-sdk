# Golang SDK for Wuying AgentBay

This directory contains the Golang implementation of the Wuying AgentBay SDK.

## Version

**Current Version:** 0.3.0

## Authors

- **Organization:** Alibaba Group
- **Team:** Wuying AI Team
- **Email:** wuying-ai-team@aliyun.com
- **Website:** https://github.com/aliyun/wuying-agentbay-sdk

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

You can run the example file:

```bash
go run examples/basic_usage.go
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

	client, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		fmt.Printf("Error initializing AgentBay client: %v\n", err)
		os.Exit(1)
	}

	// Create a session
	session, err := client.Create()
	if err != nil {
		fmt.Printf("Error creating session: %v\n", err)
		os.Exit(1)
	}
	fmt.Printf("Session created with ID: %s\n", session.SessionID)

	// Execute a command
	result, err := session.Command.ExecuteCommand("ls -la")
	if err != nil {
		fmt.Printf("Error executing command: %v\n", err)
		os.Exit(1)
	}
	fmt.Printf("Command result: %s\n", result)

	// Run code
	pythonCode := `
print("Hello, World!")
print(1 + 1)
`
	codeResult, err := session.Command.RunCode(pythonCode, "python")
	if err != nil {
		fmt.Printf("Error running code: %v\n", err)
		os.Exit(1)
	}
	fmt.Printf("Code execution result: %s\n", codeResult)

	// Read a file
	content, err := session.FileSystem.ReadFile("/path/to/file.txt")
	if err != nil {
		fmt.Printf("Error reading file: %v\n", err)
		os.Exit(1)
	}
	fmt.Printf("File content: %s\n", content)

	// Clean up
	err = client.Delete(session)
	if err != nil {
		fmt.Printf("Error deleting session: %v\n", err)
		os.Exit(1)
	}
	fmt.Println("Session deleted successfully")
}
```

## Development

### Building the SDK

```bash
go build ./...
```

### Running Tests

```bash
go test ./...
```

For more detailed documentation, please refer to the main [README](../README.md) and [SDK Documentation](../docs/README.md) in the project root.
