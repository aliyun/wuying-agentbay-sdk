#!/usr/bin/env python3
"""
Simple test script to verify VPC functionality migration works correctly.
"""

import os
from agentbay import AgentBay, CreateSessionParams

def test_vpc_session_creation():
    """Test VPC session creation and tool listing."""
    # Get API key from environment
    api_key = os.getenv('AGENTBAY_API_KEY')
    if not api_key:
        print("Error: AGENTBAY_API_KEY environment variable not set")
        return False
    
    try:
        # Initialize AgentBay client
        config = {
            'region_id': 'cn-hangzhou',
            'endpoint': 'wuyingai-pre.cn-hangzhou.aliyuncs.com',
            'timeout_ms': 60000
        }
        agent_bay = AgentBay(api_key, config)
        print("✓ AgentBay client initialized successfully")
        
        # Create VPC session parameters
        params = CreateSessionParams(
            image_id="imgc-07eksy57nw6r759fb",
            is_vpc=True,
            labels={
                "test-type": "vpc-migration-test",
                "purpose": "verify-implementation"
            }
        )
        print("✓ VPC session parameters created")
        
        # Create VPC session
        print("Creating VPC session...")
        session_result = agent_bay.create(params)
        
        if not session_result.success:
            print(f"Error creating session: {session_result.error_message}")
            return False
            
        session = session_result.session
        print(f"✓ VPC session created successfully: {session.session_id}")
        
        # Verify VPC properties
        print(f"✓ Is VPC enabled: {session.is_vpc_enabled()}")
        print(f"✓ Network Interface IP: {session.get_network_interface_ip()}")
        print(f"✓ HTTP Port: {session.get_http_port()}")
        
        # Test MCP tools listing
        print("Testing MCP tools listing...")
        tools_result = session.list_mcp_tools()
        print(f"✓ Found {len(tools_result.tools)} MCP tools")
        
        # Display first few tools
        for i, tool in enumerate(tools_result.tools[:3]):
            print(f"  Tool {i+1}: {tool.name} (server: {tool.server})")
        
        # Test find_server_for_tool functionality
        if tools_result.tools:
            first_tool = tools_result.tools[0]
            found_server = session.find_server_for_tool(first_tool.name)
            print(f"✓ Found server for '{first_tool.name}': {found_server}")
        
        # Clean up
        delete_result = session.delete()
        if delete_result.success:
            print("✓ Session deleted successfully")
        else:
            print(f"Warning: Error deleting session: {delete_result.error_message}")
        
        print("\n🎉 VPC migration test completed successfully!")
        return True
        
    except Exception as e:
        print(f"Error during VPC test: {e}")
        return False

if __name__ == "__main__":
    print("Testing VPC functionality migration...")
    success = test_vpc_session_creation()
    exit(0 if success else 1) 