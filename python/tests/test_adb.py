import unittest
from unittest.mock import MagicMock, patch

from agentbay.adb import Adb  # Adjust based on actual module path
from agentbay.exceptions import AdbError


class DummySession:
    def __init__(self):
        self.api_key = "dummy_key"
        self.session_id = "dummy_session"
        self.client = MagicMock()

    def get_api_key(self):
        return self.api_key

    def get_session_id(self):
        return self.session_id

    def get_client(self):
        return self.client


class TestAdb(unittest.TestCase):
    def setUp(self):
        self.session = DummySession()
        self.adb = Adb(self.session)

    @patch("agentbay.adb.adb.CallMcpToolRequest")
    def test_execute_adb_command_success(self, MockCallMcpToolRequest):
        mock_response = MagicMock()
        mock_response.to_map.return_value = {
            "body": {"Data": {"content": [{"text": "rlt1"}, {"text": "rlt2"}]}}
        }
        self.session.client.call_mcp_tool.return_value = mock_response

        result = self.adb.shell("ls /sdcard")

        self.assertEqual(result, "rlt1\nrlt2")
        MockCallMcpToolRequest.assert_called_once()

    @patch("agentbay.adb.adb.CallMcpToolRequest")
    def test_execute_adb_command_get_false(self, MockCallMcpToolRequest):
        mock_response = MagicMock()
        mock_response.to_map.return_value = {
            "body": {
                "Data": {
                    "isError": True,
                    "content": [{"text": "some error message"}],
                }  # No content field
            }
        }
        self.session.client.call_mcp_tool.return_value = mock_response

        with self.assertRaises(AdbError) as context:
            self.adb.shell("ls /sdcard")

        self.assertIn("Failed to execute ADB shell", str(context.exception))

    @patch("agentbay.adb.adb.CallMcpToolRequest")
    def test_execute_adb_command_exception(self, MockCallMcpToolRequest):
        self.session.client.call_mcp_tool.side_effect = Exception(
            "adb connection failed"
        )

        # self.adb.shell("ls /sdcard")
        with self.assertRaises(AdbError) as context:
            self.adb.shell("ls /sdcard")

        self.assertIn("Failed to execute ADB shell command", str(context.exception))
        self.assertIn("adb connection failed", str(context.exception))


if __name__ == "__main__":
    unittest.main()
