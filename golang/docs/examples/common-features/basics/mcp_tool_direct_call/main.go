/*
Example: List MCP Tools and Call a Tool

This example demonstrates:
1. Creating a session
2. Listing all available MCP tools
3. Calling a specific tool (shell command)
4. Cleaning up the session
*/

package main

import (
	"encoding/json"
	"fmt"
	"strings"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

func main() {
	// Initialize AgentBay client
	fmt.Println("Initializing AgentBay client...")
	client, err := agentbay.NewAgentBay("", nil)
	if err != nil {
		fmt.Printf("Failed to initialize AgentBay client: %v\n", err)
		return
	}

	// Create a session
	fmt.Println("\n1. Creating session...")
	sessionResult, err := client.Create(nil)
	if err != nil {
		fmt.Printf("Failed to create session: %v\n", err)
		return
	}
	session := sessionResult.Session
	fmt.Println("✓ Session created successfully")
	fmt.Printf("  Session ID: %s\n", session.GetSessionId())
	fmt.Printf("  Request ID: %s\n", sessionResult.RequestID)

	// Ensure cleanup
	defer func() {
		fmt.Println("\n7. Cleaning up...")
		deleteResult, err := client.Delete(session, false)
		if err != nil {
			fmt.Printf("✗ Failed to delete session: %v\n", err)
			return
		}
		if deleteResult.Success {
			fmt.Println("✓ Session deleted successfully")
			fmt.Printf("  Request ID: %s\n", deleteResult.RequestID)
		} else {
			fmt.Println("✗ Failed to delete session")
			fmt.Printf("  Error: %s\n", deleteResult.ErrorMessage)
		}
	}()

	// List all available MCP tools
	fmt.Println("\n2. Listing available MCP tools...")
	toolsResult, err := session.ListMcpTools()
	if err != nil {
		fmt.Printf("Failed to list MCP tools: %v\n", err)
		return
	}
	fmt.Printf("✓ Found %d MCP tools\n", len(toolsResult.Tools))
	fmt.Printf("  Request ID: %s\n", toolsResult.RequestID)

	// Display first 10 tools
	fmt.Println("\n  Available tools (showing first 10):")
	maxTools := 10
	if len(toolsResult.Tools) < maxTools {
		maxTools = len(toolsResult.Tools)
	}
	for i := 0; i < maxTools; i++ {
		tool := toolsResult.Tools[i]
		fmt.Printf("  %d. %s\n", i+1, tool.Name)
		fmt.Printf("     Description: %s\n", tool.Description)
		fmt.Printf("     Server: %s\n", tool.Server)
		if required, ok := tool.InputSchema["required"].([]interface{}); ok && len(required) > 0 {
			reqParams := make([]string, len(required))
			for j, r := range required {
				reqParams[j] = fmt.Sprint(r)
			}
			fmt.Printf("     Required params: %s\n", strings.Join(reqParams, ", "))
		}
		fmt.Println()
	}

	// Find and display the shell tool details
	fmt.Println("\n3. Finding 'shell' tool details...")
	var shellTool *agentbay.McpTool
	for i := range toolsResult.Tools {
		if toolsResult.Tools[i].Name == "shell" {
			shellTool = &toolsResult.Tools[i]
			break
		}
	}

	if shellTool != nil {
		fmt.Println("✓ Found 'shell' tool")
		fmt.Printf("  Description: %s\n", shellTool.Description)
		fmt.Printf("  Server: %s\n", shellTool.Server)
		fmt.Println("  Input Schema:")
		schemaJSON, _ := json.MarshalIndent(shellTool.InputSchema, "    ", "  ")
		fmt.Printf("    %s\n", string(schemaJSON))
	} else {
		fmt.Println("✗ 'shell' tool not found")
		return
	}

	// Call the shell tool
	fmt.Println("\n4. Calling 'shell' tool...")
	result, err := session.CallMcpTool("shell", map[string]interface{}{
		"command":    "echo 'Hello from MCP Tool!'",
		"timeout_ms": 1000,
	})
	if err != nil {
		fmt.Printf("Failed to call tool: %v\n", err)
		return
	}

	if result.Success {
		fmt.Println("✓ Tool call successful")
		fmt.Printf("  Request ID: %s\n", result.RequestID)
		fmt.Println("  Output:")
		fmt.Printf("    %s\n", result.Data)
	} else {
		fmt.Println("✗ Tool call failed")
		fmt.Printf("  Error: %s\n", result.ErrorMessage)
		fmt.Printf("  Request ID: %s\n", result.RequestID)
	}

	// Call another command to demonstrate flexibility
	fmt.Println("\n5. Calling 'shell' tool with different command...")
	result2, err := session.CallMcpTool("shell", map[string]interface{}{
		"command":    "pwd",
		"timeout_ms": 1000,
	})
	if err != nil {
		fmt.Printf("Failed to call tool: %v\n", err)
		return
	}

	if result2.Success {
		fmt.Println("✓ Tool call successful")
		fmt.Printf("  Request ID: %s\n", result2.RequestID)
		fmt.Println("  Current directory:")
		fmt.Printf("    %s\n", result2.Data)
	} else {
		fmt.Println("✗ Tool call failed")
		fmt.Printf("  Error: %s\n", result2.ErrorMessage)
	}

	// Demonstrate error handling
	fmt.Println("\n6. Demonstrating error handling (invalid command)...")
	result3, err := session.CallMcpTool("shell", map[string]interface{}{
		"command":    "this_command_does_not_exist_12345",
		"timeout_ms": 1000,
	})
	if err != nil {
		fmt.Printf("Failed to call tool: %v\n", err)
		return
	}

	if result3.Success {
		fmt.Println("✓ Command executed")
		fmt.Printf("  Output: %s\n", result3.Data)
	} else {
		fmt.Println("✓ Error handled correctly")
		fmt.Printf("  Request ID: %s\n", result3.RequestID)
		errorMsg := result3.ErrorMessage
		if len(errorMsg) > 100 {
			errorMsg = errorMsg[:100] + "..."
		}
		fmt.Printf("  Error message: %s\n", errorMsg)
	}

	fmt.Println("\n" + strings.Repeat("=", 60))
	fmt.Println("Example completed successfully!")
	fmt.Println(strings.Repeat("=", 60))
}
