# Golang API Reference

This section provides detailed API reference documentation for the Golang version of the AgentBay SDK.

## Core Structures

- [AgentBay](agentbay.md) - The main entry point of the SDK, used to create sessions and manage global configuration
- [Session](session.md) - Represents a session in the AgentBay cloud environment, providing interfaces to access various features

## Functional Components

- [Agent](agent.md) - Provides AI-powered capabilities for executing tasks using natural language descriptions
- [FileSystem](filesystem.md) - Provides file system operations such as uploading, downloading, and managing files
- [Command](command.md) - Provides functionality to execute shell commands in a session
- [Code](code.md) - Handles code execution operations in Python and JavaScript languages
- [Application](application.md) - Manages application operations and state
- [Window](window.md) - Manages window and view operations
- [UI](ui.md) - Provides user interface interaction functionality
- [OSS](oss.md) - Provides Object Storage Service (OSS) integration

## Context Management

- [Context](context.md) - Manages context data in a session
- [ContextManager](context-manager.md) - Provides context management functionality

## Examples

Check out the [Golang Examples](../../examples/golang/) for code samples and use cases.

## Installation

Install the Golang version of the AgentBay SDK using go get:

```bash
go get github.com/aliyun/wuying-agentbay-sdk/golang
```

## Quick Start

```go
package main

import (
	"fmt"
	"os"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

func main() {
	// Initialize the SDK with default configuration
	client, err := agentbay.NewAgentBay("your_api_key")
	if err != nil {
		fmt.Printf("Error initializing AgentBay client: %v\n", err)
		os.Exit(1)
	}

	// Or with custom configuration
	config := &agentbay.Config{
		RegionID:  "us-west-1",
		Endpoint:  "https://agentbay.example.com",
		TimeoutMs: 30000,
	}
	clientWithConfig, err := agentbay.NewAgentBay("your_api_key", agentbay.WithConfig(config))
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
	
	// Use the file system
	fs := session.FileSystem
	
	// Execute commands
	cmd := session.Command
	
	// Delete the session when done
	deleteResult, err := session.Delete()
	if err != nil {
		fmt.Printf("Error deleting session: %v\n", err)
		os.Exit(1)
	}
	
	fmt.Println("Session deleted successfully")
}
``` 