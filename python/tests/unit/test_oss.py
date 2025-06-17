import unittest
from unittest.mock import MagicMock
from agentbay.oss.oss import Oss
from agentbay.exceptions import OssError
import json

class TestOss(unittest.TestCase):
    def setUp(self):
        self.mock_session = MagicMock()
        self.oss = Oss(self.mock_session)

    def test_env_init_success(self):
        self.oss._call_mcp_tool = MagicMock(return_value="success")
        result = self.oss.env_init("key_id", "key_secret", endpoint="test_endpoint")
        self.assertEqual(result, "success")

    def test_env_init_failure(self):
        self.oss._call_mcp_tool = MagicMock(side_effect=OssError("Failed to create OSS client"))
        with self.assertRaises(OssError) as context:
            self.oss.env_init("key_id", "key_secret")
        self.assertIn("Failed to create OSS client", str(context.exception))

    def test_upload_success(self):
        """
        Test the upload method to ensure it succeeds with valid input.
        """
        self.oss._call_mcp_tool = MagicMock(return_value="Upload success")
        result = self.oss.upload("test_bucket", "test_object", "test_path")
        self.assertEqual(result, "Upload success")

    def test_upload_failure(self):
        """
        Test the upload method to ensure it raises OssError on failure.
        """
        # Mock _call_mcp_tool to return the error response
        self.oss._call_mcp_tool = MagicMock(side_effect=OssError("Upload failed: The OSS Access Key Id you provided does not exist in our records."))

        # Assert that OssError is raised with the correct message
        with self.assertRaises(OssError) as context:
            self.oss.upload("test_bucket", "test_object", "test_path")
        self.assertIn(
            "Upload failed: The OSS Access Key Id you provided does not exist in our records.",
            str(context.exception)
        )

    def test_upload_anonymous_success(self):
        self.oss._call_mcp_tool = MagicMock(return_value="upload_anon_success")
        result = self.oss.upload_anonymous("test_url", "test_path")
        self.assertEqual(result, "upload_anon_success")

    def test_upload_anonymous_failure(self):
        self.oss._call_mcp_tool = MagicMock(side_effect=OssError("Failed to upload anonymously"))
        with self.assertRaises(OssError) as context:
            self.oss.upload_anonymous("test_url", "test_path")
        self.assertIn("Failed to upload anonymously", str(context.exception))

    def test_download_success(self):
        self.oss._call_mcp_tool = MagicMock(return_value="download_success")
        result = self.oss.download("test_bucket", "test_object", "test_path")
        self.assertEqual(result, "download_success")

    def test_download_failure(self):
        self.oss._call_mcp_tool = MagicMock(side_effect=OssError("Failed to download from OSS"))
        with self.assertRaises(OssError) as context:
            self.oss.download("test_bucket", "test_object", "test_path")
        self.assertIn("Failed to download from OSS", str(context.exception))

    def test_download_anonymous_success(self):
        self.oss._call_mcp_tool = MagicMock(return_value="download_anon_success")
        result = self.oss.download_anonymous("test_url", "test_path")
        self.assertEqual(result, "download_anon_success")

    def test_download_anonymous_failure(self):
        self.oss._call_mcp_tool = MagicMock(side_effect=OssError("Failed to download anonymously"))
        with self.assertRaises(OssError) as context:
            self.oss.download_anonymous("test_url", "test_path")
        self.assertIn("Failed to download anonymously", str(context.exception))

    def test_call_mcp_tool_success(self):
        """
        Test _call_mcp_tool method with successful response.
        """
        # Mock the response from call_mcp_tool
        mock_response = MagicMock()
        mock_response.to_map.return_value = {
            "body": {
                "Data": {
                    "content": [
                        {
                            "text": "success",
                            "type": "text"
                        }
                    ],
                    "isError": False
                }
            }
        }
        self.mock_session.get_client().call_mcp_tool.return_value = mock_response

        # Call _call_mcp_tool
        result = self.oss._call_mcp_tool("test_tool", {"arg1": "value1"})
        self.assertEqual(result, "success")

        # Verify the call
        self.mock_session.get_client().call_mcp_tool.assert_called_once()
        call_args = self.mock_session.get_client().call_mcp_tool.call_args[0][0]
        self.assertEqual(call_args.name, "test_tool")
        self.assertEqual(json.loads(call_args.args), {"arg1": "value1"})

    def test_call_mcp_tool_failure(self):
        """
        Test _call_mcp_tool method with error response.
        """
        # Mock the response from call_mcp_tool
        mock_response = MagicMock()
        mock_response.to_map.return_value = {
            "body": {
                "Data": {
                    "content": [
                        {
                            "text": "Test error message",
                            "type": "text"
                        }
                    ],
                    "isError": True
                }
            }
        }
        self.mock_session.get_client().call_mcp_tool.return_value = mock_response

        # Assert that OssError is raised
        with self.assertRaises(OssError) as context:
            self.oss._call_mcp_tool("test_tool", {"arg1": "value1"})
        self.assertIn("Error in response: Test error message", str(context.exception))

    def test_call_mcp_tool_invalid_response(self):
        """
        Test _call_mcp_tool method with invalid response format.
        """
        # Mock the response from call_mcp_tool with invalid format
        mock_response = MagicMock()
        mock_response.to_map.return_value = {}  # Empty response
        self.mock_session.get_client().call_mcp_tool.return_value = mock_response

        # Assert that OssError is raised
        with self.assertRaises(OssError) as context:
            self.oss._call_mcp_tool("test_tool", {"arg1": "value1"})
        self.assertIn("Invalid response format", str(context.exception))

    def test_call_mcp_tool_api_error(self):
        """
        Test _call_mcp_tool method when API call fails.
        """
        # Mock the API call to raise an exception
        self.mock_session.get_client().call_mcp_tool.side_effect = Exception("API error")

        # Assert that OssError is raised
        with self.assertRaises(OssError) as context:
            self.oss._call_mcp_tool("test_tool", {"arg1": "value1"})
        self.assertIn("Failed to call MCP tool test_tool: API error", str(context.exception))

if __name__ == "__main__":
    unittest.main()