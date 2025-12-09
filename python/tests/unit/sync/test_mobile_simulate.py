import json
import pytest
import unittest
from unittest.mock import MagicMock, MagicMock, patch

from agentbay import (
    MobileSimulateService,
    MobileSimulateUploadResult,
)
from agentbay import MobileSimulateConfig, MobileSimulateMode
from agentbay import Context
from agentbay import BWList, ContextSync, SyncPolicy


class TestMobileSimulateUploadResult(unittest.TestCase):
    def test_upload_result_success(self):
        result = MobileSimulateUploadResult(
            success=True, mobile_simulate_context_id="context-123"
        )
        self.assertTrue(result.success)
        self.assertEqual(result.mobile_simulate_context_id, "context-123")
        self.assertEqual(result.error_message, "")

    def test_upload_result_failure(self):
        result = MobileSimulateUploadResult(
            success=False, error_message="Upload failed"
        )
        self.assertFalse(result.success)
        self.assertEqual(result.mobile_simulate_context_id, "")
        self.assertEqual(result.error_message, "Upload failed")


class TestAsyncMobileSimulateService(unittest.TestCase):
    def setUp(self):
        self.agent_bay = MagicMock()
        self.agent_bay.context = MagicMock()
        self.mobile_simulate_service = MobileSimulateService(self.agent_bay)

    def test_initialization(self):
        """Test service initialization with default values"""
        self.assertIsNotNone(self.mobile_simulate_service.agent_bay)
        self.assertIsNotNone(self.mobile_simulate_service.context_service)
        self.assertFalse(self.mobile_simulate_service.simulate_enable)
        self.assertEqual(
            self.mobile_simulate_service.simulate_mode,
            MobileSimulateMode.PROPERTIES_ONLY,
        )
        self.assertIsNone(self.mobile_simulate_service.context_id)
        self.assertIsNone(self.mobile_simulate_service.context_sync)
        self.assertTrue(self.mobile_simulate_service.use_internal_context)

    def test_initialization_without_agent_bay(self):
        """Test initialization fails without agent_bay"""
        with self.assertRaises(ValueError) as context:
            MobileSimulateService(None)
        self.assertIn("agent_bay is required", str(context.exception))

    def test_initialization_without_context(self):
        """Test initialization fails without context service"""
        agent_bay = MagicMock()
        agent_bay.context = None
        with self.assertRaises(ValueError) as context:
            MobileSimulateService(agent_bay)
        self.assertIn("agent_bay.context is required", str(context.exception))

    def test_set_and_get_simulate_enable(self):
        """Test setting and getting simulate enable flag"""
        self.mobile_simulate_service.set_simulate_enable(True)
        self.assertTrue(self.mobile_simulate_service.get_simulate_enable())

        self.mobile_simulate_service.set_simulate_enable(False)
        self.assertFalse(self.mobile_simulate_service.get_simulate_enable())

    def test_set_and_get_simulate_mode(self):
        """Test setting and getting simulate mode"""
        self.mobile_simulate_service.set_simulate_mode(MobileSimulateMode.ALL)
        self.assertEqual(
            self.mobile_simulate_service.get_simulate_mode(), MobileSimulateMode.ALL
        )

        self.mobile_simulate_service.set_simulate_mode(MobileSimulateMode.SENSORS_ONLY)
        self.assertEqual(
            self.mobile_simulate_service.get_simulate_mode(),
            MobileSimulateMode.SENSORS_ONLY,
        )

    def test_set_and_get_simulate_context_id(self):
        """Test setting and getting simulate context id"""
        context_id = "test-context-123"
        self.mobile_simulate_service.set_simulate_context_id(context_id)
        self.assertEqual(
            self.mobile_simulate_service.get_simulate_context_id(), context_id
        )
        self.assertTrue(self.mobile_simulate_service.use_internal_context)

    def test_get_simulate_config_with_internal_context(self):
        """Test getting simulate config with internal context"""
        self.mobile_simulate_service.set_simulate_enable(True)
        self.mobile_simulate_service.set_simulate_mode(MobileSimulateMode.ALL)
        self.mobile_simulate_service.context_id = "internal-context-123"
        self.mobile_simulate_service.use_internal_context = True

        config = self.mobile_simulate_service.get_simulate_config()

        self.assertIsInstance(config, MobileSimulateConfig)
        self.assertTrue(config.simulate)
        self.assertEqual(config.simulate_mode, MobileSimulateMode.ALL)
        self.assertEqual(config.simulated_context_id, "internal-context-123")

    def test_get_simulate_config_with_external_context(self):
        """Test getting simulate config with external context"""
        self.mobile_simulate_service.set_simulate_enable(True)
        self.mobile_simulate_service.set_simulate_mode(
            MobileSimulateMode.PROPERTIES_ONLY
        )
        self.mobile_simulate_service.context_id = "external-context-123"
        self.mobile_simulate_service.use_internal_context = False

        config = self.mobile_simulate_service.get_simulate_config()

        self.assertIsInstance(config, MobileSimulateConfig)
        self.assertTrue(config.simulate)
        self.assertEqual(config.simulate_mode, MobileSimulateMode.PROPERTIES_ONLY)
        self.assertIsNone(config.simulated_context_id)

    @pytest.mark.sync


    def test_has_mobile_info_exists(self):
        """Test checking if mobile info exists in context"""
        context_sync = ContextSync(
            context_id="test-context",
            path="/data/data",
            policy=SyncPolicy(bw_list=BWList(white_lists=[])),
        )

        mock_list_result = MagicMock()
        mock_list_result.success = True
        mock_entry = MagicMock()
        mock_entry.file_name = "dev_info.json"
        mock_list_result.entries = [mock_entry]

        self.agent_bay.context.list_files = MagicMock(return_value=mock_list_result)

        result = self.mobile_simulate_service.has_mobile_info(context_sync)

        self.assertTrue(result)
        self.assertEqual(self.mobile_simulate_service.context_id, "test-context")
        self.assertFalse(self.mobile_simulate_service.use_internal_context)

    @pytest.mark.sync


    def test_has_mobile_info_not_exists(self):
        """Test checking when mobile info doesn't exist"""
        context_sync = ContextSync(
            context_id="test-context", path="/data/data", policy=SyncPolicy.default()
        )

        mock_list_result = MagicMock()
        mock_list_result.success = True
        mock_list_result.entries = []

        self.agent_bay.context.list_files = MagicMock(return_value=mock_list_result)

        result = self.mobile_simulate_service.has_mobile_info(context_sync)

        self.assertFalse(result)

    @pytest.mark.sync


    def test_has_mobile_info_list_failed(self):
        """Test handling list files failure"""
        context_sync = ContextSync(
            context_id="test-context", path="/data/data", policy=SyncPolicy.default()
        )

        mock_list_result = MagicMock()
        mock_list_result.success = False
        mock_list_result.error_message = "List failed"

        self.agent_bay.context.list_files = MagicMock(return_value=mock_list_result)

        result = self.mobile_simulate_service.has_mobile_info(context_sync)

        self.assertFalse(result)

    @pytest.mark.sync


    def test_has_mobile_info_invalid_context_sync(self):
        """Test validation when context_sync is None"""
        with self.assertRaises(ValueError) as context:
            self.mobile_simulate_service.has_mobile_info(None)
        self.assertIn("context_sync is required", str(context.exception))

    @pytest.mark.sync


    def test_has_mobile_info_missing_context_id(self):
        """Test validation when context_id is missing"""
        context_sync = ContextSync(
            context_id=None, path="/data/data", policy=SyncPolicy.default()
        )
        with self.assertRaises(ValueError) as context:
            self.mobile_simulate_service.has_mobile_info(context_sync)
        self.assertIn("context_sync.context_id is required", str(context.exception))

    @pytest.mark.sync


    def test_has_mobile_info_missing_path(self):
        """Test validation when path is missing"""
        context_sync = ContextSync(
            context_id="test-context", path=None, policy=SyncPolicy.default()
        )
        with self.assertRaises(ValueError) as context:
            self.mobile_simulate_service.has_mobile_info(context_sync)
        self.assertIn("context_sync.path is required", str(context.exception))

    @patch("httpx.Client")
    @pytest.mark.sync

    def test_upload_mobile_info_success_without_context(self, mock_client_cls):
        """Test uploading mobile info without providing context sync"""
        mobile_dev_info = json.dumps({"device": "test", "model": "test-model"})

        mock_context_result = MagicMock()
        mock_context_result.success = True
        mock_context = Context(id="new-context", name="test-context")
        mock_context_result.context = mock_context
        self.agent_bay.context.get = MagicMock(return_value=mock_context_result)

        mock_upload_url = MagicMock()
        mock_upload_url.success = True
        mock_upload_url.url = "https://test-upload-url.com"
        self.agent_bay.context.get_file_upload_url = MagicMock(
            return_value=mock_upload_url
        )

        mock_client = MagicMock()
        mock_client_cls.return_value.__enter__.return_value = mock_client
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_client.put.return_value = mock_response

        result = self.mobile_simulate_service.upload_mobile_info(mobile_dev_info)

        self.assertTrue(result.success)
        self.assertEqual(result.mobile_simulate_context_id, "new-context")
        self.assertTrue(self.mobile_simulate_service.use_internal_context)
        mock_client.put.assert_called_once_with(
            "https://test-upload-url.com", content=mobile_dev_info
        )

    @patch("httpx.Client")
    @pytest.mark.sync

    def test_upload_mobile_info_success_with_context(self, mock_client_cls):
        """Test uploading mobile info with existing context sync"""
        mobile_dev_info = json.dumps({"device": "test"})
        context_sync = ContextSync(
            context_id="existing-context",
            path="/data/data",
            policy=SyncPolicy(bw_list=BWList(white_lists=[])),
        )

        mock_upload_url = MagicMock()
        mock_upload_url.success = True
        mock_upload_url.url = "https://test-upload-url.com"
        self.agent_bay.context.get_file_upload_url = MagicMock(
            return_value=mock_upload_url
        )

        mock_client = MagicMock()
        mock_client_cls.return_value.__enter__.return_value = mock_client
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_client.put.return_value = mock_response

        result = self.mobile_simulate_service.upload_mobile_info(
            mobile_dev_info, context_sync
        )

        self.assertTrue(result.success)
        self.assertEqual(result.mobile_simulate_context_id, "existing-context")
        self.assertFalse(self.mobile_simulate_service.use_internal_context)

    @pytest.mark.sync


    def test_upload_mobile_info_invalid_json(self):
        """Test upload fails with invalid JSON"""
        with self.assertRaises(ValueError):
            self.mobile_simulate_service.upload_mobile_info("invalid json")

    @pytest.mark.sync


    def test_upload_mobile_info_empty_string(self):
        """Test upload fails with empty string"""
        with self.assertRaises(ValueError):
            self.mobile_simulate_service.upload_mobile_info("")

    @pytest.mark.sync


    def test_upload_mobile_info_context_creation_failed(self):
        """Test handling context creation failure"""
        mobile_dev_info = json.dumps({"device": "test"})

        mock_context_result = MagicMock()
        mock_context_result.success = False
        mock_context_result.error_message = "Failed to create context"
        self.agent_bay.context.get = MagicMock(return_value=mock_context_result)

        result = self.mobile_simulate_service.upload_mobile_info(mobile_dev_info)

        self.assertFalse(result.success)
        self.assertIn("Failed to create context for simulate", result.error_message)

    @pytest.mark.sync


    def test_upload_mobile_info_get_upload_url_failed(self):
        """Test handling get upload URL failure"""
        mobile_dev_info = json.dumps({"device": "test"})

        mock_context_result = MagicMock()
        mock_context_result.success = True
        mock_context = Context(id="new-context", name="test-context")
        mock_context_result.context = mock_context
        self.agent_bay.context.get = MagicMock(return_value=mock_context_result)

        mock_upload_url = MagicMock()
        mock_upload_url.success = False
        mock_upload_url.error_message = "Failed to get upload URL"
        self.agent_bay.context.get_file_upload_url = MagicMock(
            return_value=mock_upload_url
        )

        result = self.mobile_simulate_service.upload_mobile_info(mobile_dev_info)

        self.assertFalse(result.success)
        self.assertIn("Failed to get upload URL", result.error_message)

    @pytest.mark.sync


    def test_upload_mobile_info_with_context_missing_context_id(self):
        """Test validation when context_sync has no context_id"""
        mobile_dev_info = json.dumps({"device": "test"})
        context_sync = ContextSync(
            context_id=None, path="/data/data", policy=SyncPolicy.default()
        )

        with self.assertRaises(ValueError) as context:
            self.mobile_simulate_service.upload_mobile_info(
                mobile_dev_info, context_sync
            )
        self.assertIn("context_sync.context_id is required", str(context.exception))

    def test_update_context_internal(self):
        """Test updating context with internal mode"""
        self.mobile_simulate_service._update_context(True, "internal-ctx-123", None)

        self.assertTrue(self.mobile_simulate_service.use_internal_context)
        self.assertEqual(self.mobile_simulate_service.context_id, "internal-ctx-123")
        self.assertIsNone(self.mobile_simulate_service.context_sync)
        self.assertIsNotNone(self.mobile_simulate_service.mobile_dev_info_path)

    def test_update_context_external(self):
        """Test updating context with external mode"""
        context_sync = ContextSync(
            context_id="external-ctx-123",
            path="/data/data",
            policy=SyncPolicy(bw_list=BWList(white_lists=[])),
        )

        self.mobile_simulate_service._update_context(
            False, "external-ctx-123", context_sync
        )

        self.assertFalse(self.mobile_simulate_service.use_internal_context)
        self.assertEqual(self.mobile_simulate_service.context_id, "external-ctx-123")
        self.assertEqual(self.mobile_simulate_service.context_sync, context_sync)
        self.assertIsNotNone(self.mobile_simulate_service.mobile_dev_info_path)

    def test_update_context_external_without_context_sync(self):
        """Test updating external context without context_sync raises error"""
        with self.assertRaises(ValueError) as context:
            self.mobile_simulate_service._update_context(
                False, "external-ctx-123", None
            )
        self.assertIn("context_sync is required", str(context.exception))

    @pytest.mark.sync


    def test_create_context_for_simulate_success(self):
        """Test creating context for simulate"""
        mock_context_result = MagicMock()
        mock_context_result.success = True
        mock_context = Context(id="new-context-id", name="mobile_sim_test")
        mock_context_result.context = mock_context
        self.agent_bay.context.get = MagicMock(return_value=mock_context_result)

        result = self.mobile_simulate_service._create_context_for_simulate()

        self.assertIsNotNone(result)
        self.assertEqual(result.id, "new-context-id")

    @pytest.mark.sync


    def test_create_context_for_simulate_failed(self):
        """Test handling context creation failure"""
        mock_context_result = MagicMock()
        mock_context_result.success = False
        mock_context_result.error_message = "Failed to create context"
        self.agent_bay.context.get = MagicMock(return_value=mock_context_result)

        result = self.mobile_simulate_service._create_context_for_simulate()

        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
