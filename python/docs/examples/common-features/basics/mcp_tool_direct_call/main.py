"""
Example: List MCP Tools and Call a Tool

This example demonstrates:
1. Creating a session
2. Listing all available MCP tools
3. Calling a specific tool (shell command)
4. Cleaning up the session
"""

from agentbay import AgentBay
import json


def main():
    # Initialize AgentBay client
    print("Initializing AgentBay client...")
    agent_bay = AgentBay()

    # Create a session
    print("\n1. Creating session...")
    session_result = agent_bay.create()
    session = session_result.session
    print(f"✓ Session created successfully")
    print(f"  Session ID: {session.session_id}")
    print(f"  Request ID: {session_result.request_id}")

    try:
        # List all available MCP tools
        print("\n2. Listing available MCP tools...")
        tools_result = session.list_mcp_tools()
        print(f"✓ Found {len(tools_result.tools)} MCP tools")
        print(f"  Request ID: {tools_result.request_id}")

        # Display first 10 tools
        print("\n  Available tools (showing first 10):")
        for i, tool in enumerate(tools_result.tools[:10], 1):
            print(f"  {i}. {tool.name}")
            print(f"     Description: {tool.description}")
            print(f"     Server: {tool.server}")
            if tool.input_schema.get('required'):
                print(f"     Required params: {', '.join(tool.input_schema['required'])}")
            print()

        # Find and display the shell tool details
        print("\n3. Finding 'shell' tool details...")
        shell_tool = None
        for tool in tools_result.tools:
            if tool.name == "shell":
                shell_tool = tool
                break

        if shell_tool:
            print(f"✓ Found 'shell' tool")
            print(f"  Description: {shell_tool.description}")
            print(f"  Server: {shell_tool.server}")
            print(f"  Input Schema:")
            print(f"    {json.dumps(shell_tool.input_schema, indent=4)}")
        else:
            print("✗ 'shell' tool not found")
            return

        # Call the shell tool
        print("\n4. Calling 'shell' tool...")
        result = session.call_mcp_tool("shell", {
            "command": "echo 'Hello from MCP Tool!'",
            "timeout_ms": 1000
        })

        if result.success:
            print(f"✓ Tool call successful")
            print(f"  Request ID: {result.request_id}")
            print(f"  Output:")
            print(f"    {result.data}")
        else:
            print(f"✗ Tool call failed")
            print(f"  Error: {result.error_message}")
            print(f"  Request ID: {result.request_id}")

        # Call another command to demonstrate flexibility
        print("\n5. Calling 'shell' tool with different command...")
        result2 = session.call_mcp_tool("shell", {
            "command": "pwd",
            "timeout_ms": 1000
        })

        if result2.success:
            print(f"✓ Tool call successful")
            print(f"  Request ID: {result2.request_id}")
            print(f"  Current directory:")
            print(f"    {result2.data}")
        else:
            print(f"✗ Tool call failed")
            print(f"  Error: {result2.error_message}")

        # Demonstrate error handling
        print("\n6. Demonstrating error handling (invalid command)...")
        result3 = session.call_mcp_tool("shell", {
            "command": "this_command_does_not_exist_12345",
            "timeout_ms": 1000
        })

        if result3.success:
            print(f"✓ Command executed")
            print(f"  Output: {result3.data}")
        else:
            print(f"✓ Error handled correctly")
            print(f"  Request ID: {result3.request_id}")
            print(f"  Error message: {result3.error_message[:100]}...")

    finally:
        # Clean up - delete the session
        print("\n7. Cleaning up...")
        delete_result = agent_bay.delete(session)
        if delete_result.success:
            print(f"✓ Session deleted successfully")
            print(f"  Request ID: {delete_result.request_id}")
        else:
            print(f"✗ Failed to delete session")
            print(f"  Error: {delete_result.error_message}")

    print("\n" + "=" * 60)
    print("Example completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()

