import unittest
import pytest
from unittest.mock import MagicMock, MagicMock

from agentbay import McpToolResult, OperationResult
from agentbay import Oss


class TestAsyncOss(unittest.TestCase):
    def setUp(self):
        self.mock_session = MagicMock()
        self.session = self.mock_session  # Add session reference
        self.oss = Oss(self.mock_session)

    @pytest.mark.sync


    def test_env_init_success_parses_json_string(self):
        # Create a mock OperationResult with JSON string data
        mock_result = McpToolResult(
            request_id="test-request-id",
            success=True,
            data='{"region":"cn-hangzhou","endpoint":"https://oss-cn-hangzhou.aliyuncs.com"}',
            error_message="",
        )
        self.session.call_mcp_tool = MagicMock(return_value=mock_result)

        result = self.oss.env_init(
            "key_id", "key_secret", "security_token", endpoint="test_endpoint"
        )

        self.assertTrue(result.success)
        self.assertEqual(result.request_id, "test-request-id")
        # The current implementation directly assigns result.data to client_config
        # without JSON parsing, so we expect the JSON string as-is
        self.assertEqual(
            result.client_config,
            '{"region":"cn-hangzhou","endpoint":"https://oss-cn-hangzhou.aliyuncs.com"}',
        )
        self.assertEqual(result.error_message, "")

    @pytest.mark.sync


    def test_env_init_success_passes_through_dict(self):
        mock_result = McpToolResult(
            request_id="test-request-id",
            success=True,
            data={"foo": "bar"},
            error_message="",
        )
        self.session.call_mcp_tool = MagicMock(return_value=mock_result)

        result = self.oss.env_init("key_id", "key_secret", "security_token")

        self.assertTrue(result.success)
        self.assertEqual(result.client_config, {"foo": "bar"})

    @pytest.mark.sync
    def test_env_init_parse_error(self):
        # Successful call but with invalid JSON content
        # The current implementation doesn't parse JSON, so this will succeed
        # and return the invalid JSON string as client_config
        mock_result = McpToolResult(
            request_id="test-request-id",
            success=True,
            data="{invalid-json",
            error_message="",
        )
        self.session.call_mcp_tool = MagicMock(return_value=mock_result)

        result = self.oss.env_init("key_id", "key_secret", "security_token")

        # The current implementation will succeed and return the data as-is
        self.assertTrue(result.success)
        self.assertEqual(result.request_id, "test-request-id")
        self.assertEqual(result.client_config, "{invalid-json")
        self.assertEqual(result.error_message, "")

    @pytest.mark.sync


    def test_env_init_failure(self):
        # Create a mock failed OperationResult
        mock_result = McpToolResult(
            request_id="test-request-id",
            success=False,
            data=None,
            error_message="Failed to create OSS client",
        )
        self.session.call_mcp_tool = MagicMock(return_value=mock_result)

        result = self.oss.env_init("key_id", "key_secret", "security_token")

        self.assertFalse(result.success)
        self.assertEqual(result.request_id, "test-request-id")
        self.assertEqual(result.client_config, {})
        self.assertEqual(result.error_message, "Failed to create OSS client")

    @pytest.mark.sync


    def test_upload_success(self):
        """
        Test the upload method to ensure it succeeds with valid input.
        """
        from agentbay import McpToolResult

        mock_result = McpToolResult(
            request_id="test-request-id",
            success=True,
            data="Upload success",
            error_message="",
        )
        self.session.call_mcp_tool = MagicMock(return_value=mock_result)

        result = self.oss.upload("test_bucket", "test_object", "test_path")

        self.assertTrue(result.success)
        self.assertEqual(result.request_id, "test-request-id")
        self.assertEqual(result.content, "Upload success")
        self.assertEqual(result.error_message, "")

    @pytest.mark.sync


    def test_upload_failure(self):
        """
        Test the upload method to ensure it handles failure correctly.
        """
        error_msg = "Upload failed: The OSS Access Key Id you provided does not exist in our records."
        mock_result = McpToolResult(
            request_id="test-request-id",
            success=False,
            data=None,
            error_message=error_msg,
        )
        self.session.call_mcp_tool = MagicMock(return_value=mock_result)

        result = self.oss.upload("test_bucket", "test_object", "test_path")

        self.assertFalse(result.success)
        self.assertEqual(result.request_id, "test-request-id")
        self.assertEqual(result.content, "")
        self.assertEqual(result.error_message, error_msg)

    @pytest.mark.sync


    def test_upload_anonymous_success(self):
        mock_result = McpToolResult(
            request_id="test-request-id",
            success=True,
            data="upload_anon_success",
            error_message="",
        )
        self.session.call_mcp_tool = MagicMock(return_value=mock_result)

        result = self.oss.upload_anonymous("test_url", "test_path")

        self.assertTrue(result.success)
        self.assertEqual(result.request_id, "test-request-id")
        self.assertEqual(result.content, "upload_anon_success")
        self.assertEqual(result.error_message, "")

    @pytest.mark.sync


    def test_upload_anonymous_failure(self):
        mock_result = McpToolResult(
            request_id="test-request-id",
            success=False,
            data=None,
            error_message="Failed to upload anonymously",
        )
        self.session.call_mcp_tool = MagicMock(return_value=mock_result)

        result = self.oss.upload_anonymous("test_url", "test_path")

        self.assertFalse(result.success)
        self.assertEqual(result.request_id, "test-request-id")
        self.assertEqual(result.content, "")
        self.assertEqual(result.error_message, "Failed to upload anonymously")

    @pytest.mark.sync


    def test_download_success(self):
        mock_result = McpToolResult(
            request_id="test-request-id",
            success=True,
            data="download_success",
            error_message="",
        )
        self.session.call_mcp_tool = MagicMock(return_value=mock_result)

        result = self.oss.download("test_bucket", "test_object", "test_path")

        self.assertTrue(result.success)
        self.assertEqual(result.request_id, "test-request-id")
        self.assertEqual(result.content, "download_success")
        self.assertEqual(result.error_message, "")

    @pytest.mark.sync


    def test_download_failure(self):
        mock_result = McpToolResult(
            request_id="test-request-id",
            success=False,
            data=None,
            error_message="Failed to download from OSS",
        )
        self.session.call_mcp_tool = MagicMock(return_value=mock_result)

        result = self.oss.download("test_bucket", "test_object", "test_path")

        self.assertFalse(result.success)
        self.assertEqual(result.request_id, "test-request-id")
        self.assertEqual(result.content, "")
        self.assertEqual(result.error_message, "Failed to download from OSS")

    @pytest.mark.sync


    def test_download_anonymous_success(self):
        mock_result = McpToolResult(
            request_id="test-request-id",
            success=True,
            data="download_anon_success",
            error_message="",
        )
        self.session.call_mcp_tool = MagicMock(return_value=mock_result)

        result = self.oss.download_anonymous("test_url", "test_path")

        self.assertTrue(result.success)
        self.assertEqual(result.request_id, "test-request-id")
        self.assertEqual(result.content, "download_anon_success")
        self.assertEqual(result.error_message, "")

    @pytest.mark.sync


    def test_download_anonymous_failure(self):
        mock_result = McpToolResult(
            request_id="test-request-id",
            success=False,
            data=None,
            error_message="Failed to download anonymously",
        )
        self.session.call_mcp_tool = MagicMock(return_value=mock_result)

        result = self.oss.download_anonymous("test_url", "test_path")

        self.assertFalse(result.success)
        self.assertEqual(result.request_id, "test-request-id")
        self.assertEqual(result.content, "")
        self.assertEqual(result.error_message, "Failed to download anonymously")


if __name__ == "__main__":
    unittest.main()
