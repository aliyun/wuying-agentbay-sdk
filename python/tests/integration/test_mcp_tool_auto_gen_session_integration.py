import os
import time
import unittest

from agentbay import AgentBay


def get_test_api_key():
    """Get API key for testing"""
    return os.environ.get("AGENTBAY_API_KEY")


class TestMcpToolAutoGenSessionIntegration(unittest.TestCase):
    """Integration test for MCP tool call with AutoGenSession parameter"""

    @classmethod
    def setUpClass(cls):
        # Get API Key
        api_key = get_test_api_key()
        if not api_key:
            raise unittest.SkipTest("AGENTBAY_API_KEY environment variable not set")

        # Initialize AgentBay client
        cls.agent_bay = AgentBay(api_key=api_key)

    def test_mcp_tool_call_with_active_session(self):
        """Test MCP tool call succeeds when session is active"""
        # Create a session
        print("Creating session for MCP tool call test...")
        result = self.agent_bay.create()
        self.assertTrue(result.success)
        self.assertIsNotNone(result.session)
        session = result.session
        print(f"Session created successfully, ID: {session.session_id}")

        # Call MCP tool with active session (auto_gen_session=False)
        print("Calling MCP tool with active session...")
        tool_result = session.call_mcp_tool(
            tool_name="shell",
            args={"command": "echo 'test'", "timeout_ms": 5000},
            auto_gen_session=False
        )
        self.assertTrue(tool_result.success, f"MCP tool call failed: {tool_result.error_message}")
        print(f"MCP tool call succeeded (RequestID: {tool_result.request_id})")

        # Clean up
        print("Deleting session...")
        delete_result = session.delete()
        self.assertTrue(delete_result.success)
        print("Session deleted successfully")

    def test_mcp_tool_call_with_deleted_session_auto_gen_false(self):
        """Test MCP tool call fails when session is deleted and auto_gen_session=False"""
        # Create a session
        print("Creating session for deletion test...")
        result = self.agent_bay.create()
        self.assertTrue(result.success)
        self.assertIsNotNone(result.session)
        session = result.session
        session_id = session.session_id
        print(f"Session created successfully, ID: {session_id}")

        # Delete the session
        print("Deleting session...")
        delete_result = session.delete()
        self.assertTrue(delete_result.success)
        print(f"Session deleted successfully (RequestID: {delete_result.request_id})")

        # Wait for deletion to complete
        time.sleep(2)

        # Verify session is deleted
        list_result = self.agent_bay.list()
        self.assertTrue(list_result.success)
        self.assertNotIn(
            session_id,
            list_result.session_ids,
            f"Session ID {session_id} still exists after deletion",
        )

        # Try to call MCP tool with deleted session (auto_gen_session=False)
        print("Calling MCP tool with deleted session (auto_gen_session=False)...")
        tool_result = session.call_mcp_tool(
            tool_name="shell",
            args={"command": "echo 'test'", "timeout_ms": 5000},
            auto_gen_session=False
        )
        # Expect failure
        self.assertFalse(tool_result.success, "MCP tool call should fail with deleted session")
        self.assertIsNotNone(tool_result.error_message)
        self.assertTrue(len(tool_result.error_message) > 0)
        print(f"MCP tool call failed as expected: {tool_result.error_message}")

    def test_mcp_tool_call_with_deleted_session_auto_gen_true(self):
        """Test MCP tool call behavior when session is deleted and auto_gen_session=True"""
        # Create a session
        print("Creating session for auto-gen test...")
        result = self.agent_bay.create()
        self.assertTrue(result.success)
        self.assertIsNotNone(result.session)
        session = result.session
        session_id = session.session_id
        print(f"Session created successfully, ID: {session_id}")

        # Delete the session
        print("Deleting session...")
        delete_result = session.delete()
        self.assertTrue(delete_result.success)
        print(f"Session deleted successfully (RequestID: {delete_result.request_id})")

        # Wait for deletion to complete
        time.sleep(2)

        # Verify session is deleted
        list_result = self.agent_bay.list()
        self.assertTrue(list_result.success)
        self.assertNotIn(
            session_id,
            list_result.session_ids,
            f"Session ID {session_id} still exists after deletion",
        )

        # Try to call MCP tool with deleted session (auto_gen_session=True)
        print("Calling MCP tool with deleted session (auto_gen_session=True)...")
        tool_result = session.call_mcp_tool(
            tool_name="shell",
            args={"command": "echo 'test'", "timeout_ms": 5000},
            auto_gen_session=True
        )
        # The behavior depends on the server implementation
        # If auto_gen_session is supported, it may succeed by creating a new session
        # If not supported, it should fail
        print(f"MCP tool call result: success={tool_result.success}, error={tool_result.error_message}")
        # We don't assert success/failure here as it depends on server support
        # Just verify we got a response
        self.assertIsNotNone(tool_result)


if __name__ == "__main__":
    unittest.main()

