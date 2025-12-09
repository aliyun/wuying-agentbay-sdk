"""
Unit tests for Mobile module.
Following TDD principles - tests first, then implementation.
"""

from unittest.mock import MagicMock, Mock, patch

import pytest

from agentbay import AgentBayError
from agentbay import BoolResult, OperationResult
from agentbay import AppOperationResult, ProcessListResult
from agentbay import Mobile


class TestMobile:
    """Test cases for Mobile module."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_session = Mock()
        self.mock_session.call_mcp_tool = MagicMock()
        # Setup agent_bay.client mock for get_adb_url
        self.mock_session.agent_bay = Mock()
        self.mock_session.agent_bay.client = Mock()
        self.mock_session.agent_bay.client.get_adb_link = MagicMock()
        self.session = self.mock_session  # Add session reference for tests
        self.mobile = Mobile(self.mock_session)

    @pytest.mark.sync


    def test_mobile_initialization(self):
        """Test Mobile module initialization."""
        assert self.mobile.session == self.mock_session

    # Touch Operations Tests
    @pytest.mark.sync

    def test_tap_success(self):
        """Test successful tap."""
        # Arrange
        mock_result = Mock()
        mock_result.success = True
        mock_result.request_id = "test-123"
        mock_result.error_message = ""

        self.session.call_mcp_tool = MagicMock(return_value=mock_result)

        # Act
        result = self.mobile.tap(100, 200)

        # Assert
        assert isinstance(result, BoolResult)
        assert result.success is True
        assert result.data is True
        self.session.call_mcp_tool.assert_called_once_with("tap", {"x": 100, "y": 200})

    @pytest.mark.sync


    def test_swipe_success(self):
        """Test successful swipe."""
        # Arrange
        mock_result = Mock()
        mock_result.success = True
        mock_result.request_id = "test-123"

        self.session.call_mcp_tool = MagicMock(return_value=mock_result)

        # Act
        result = self.mobile.swipe(100, 100, 200, 200)

        # Assert
        assert isinstance(result, BoolResult)
        assert result.success is True
        self.session.call_mcp_tool.assert_called_once_with(
            "swipe",
            {
                "start_x": 100,
                "start_y": 100,
                "end_x": 200,
                "end_y": 200,
                "duration_ms": 300,
            },
        )

    @pytest.mark.sync


    def test_swipe_with_duration(self):
        """Test swipe with custom duration."""
        # Arrange
        mock_result = Mock()
        mock_result.success = True
        mock_result.request_id = "test-123"

        self.session.call_mcp_tool = MagicMock(return_value=mock_result)

        # Act
        result = self.mobile.swipe(100, 100, 200, 200, duration_ms=500)

        # Assert
        self.session.call_mcp_tool.assert_called_once_with(
            "swipe",
            {
                "start_x": 100,
                "start_y": 100,
                "end_x": 200,
                "end_y": 200,
                "duration_ms": 500,
            },
        )

    @pytest.mark.sync


    def test_input_text_success(self):
        """Test successful text input."""
        # Arrange
        mock_result = Mock()
        mock_result.success = True
        mock_result.request_id = "test-123"

        self.session.call_mcp_tool = MagicMock(return_value=mock_result)

        # Act
        result = self.mobile.input_text("Hello Mobile")

        # Assert
        assert isinstance(result, BoolResult)
        assert result.success is True
        self.session.call_mcp_tool.assert_called_once_with(
            "input_text", {"text": "Hello Mobile"}
        )

    @pytest.mark.sync


    def test_send_key_success(self):
        """Test successful key send."""
        # Arrange
        mock_result = Mock()
        mock_result.success = True
        mock_result.request_id = "test-123"

        self.session.call_mcp_tool = MagicMock(return_value=mock_result)

        # Act
        result = self.mobile.send_key(4)  # BACK key

        # Assert
        assert isinstance(result, BoolResult)
        assert result.success is True
        self.session.call_mcp_tool.assert_called_once_with("send_key", {"key": 4})

    # UI Elements Tests
    @pytest.mark.sync

    def test_get_clickable_ui_elements_success(self):
        """Test successful clickable UI elements retrieval."""
        # Arrange
        mock_result = Mock()
        mock_result.success = True
        mock_result.request_id = "test-123"
        mock_result.data = '[{"id": "button1", "text": "Click me"}]'  # JSON string

        self.session.call_mcp_tool = MagicMock(return_value=mock_result)

        # Act
        result = self.mobile.get_clickable_ui_elements()

        # Assert
        assert result.success is True
        assert len(result.elements) == 1
        assert result.elements[0]["id"] == "button1"
        self.session.call_mcp_tool.assert_called_once_with(
            "get_clickable_ui_elements", {"timeout_ms": 2000}
        )

    @pytest.mark.sync


    def test_get_clickable_ui_elements_with_timeout(self):
        """Test clickable UI elements with custom timeout."""
        # Arrange
        mock_result = Mock()
        mock_result.success = True
        mock_result.request_id = "test-123"
        mock_result.data = "[]"  # JSON string

        self.session.call_mcp_tool = MagicMock(return_value=mock_result)

        # Act
        result = self.mobile.get_clickable_ui_elements(timeout_ms=5000)

        # Assert
        self.session.call_mcp_tool.assert_called_once_with(
            "get_clickable_ui_elements", {"timeout_ms": 5000}
        )

    @pytest.mark.sync


    def test_get_all_ui_elements_success(self):
        """Test successful all UI elements retrieval."""
        # Arrange
        mock_result = Mock()
        mock_result.success = True
        mock_result.request_id = "test-123"
        # Mock data with proper UI element structure including children
        mock_result.data = '[{"bounds": "[0,0][100,100]", "className": "Button", "text": "Click me", "type": "button", "resourceId": "btn1", "index": 0, "isParent": true, "children": [{"bounds": "[10,10][90,90]", "className": "Text", "text": "Label", "type": "text", "resourceId": "txt1", "index": 0, "isParent": false}]}, {"bounds": "[0,100][100,200]", "className": "TextView", "text": "Hello", "type": "text", "resourceId": "txt2", "index": 1, "isParent": false}]'

        self.session.call_mcp_tool = MagicMock(return_value=mock_result)

        # Act
        result = self.mobile.get_all_ui_elements()

        # Assert
        assert result.success is True
        assert len(result.elements) == 2
        # Verify first element structure and fields
        assert result.elements[0]["bounds"] == "[0,0][100,100]"
        assert result.elements[0]["className"] == "Button"
        assert result.elements[0]["text"] == "Click me"
        assert result.elements[0]["resourceId"] == "btn1"
        # Verify children are parsed
        assert len(result.elements[0]["children"]) == 1
        assert result.elements[0]["children"][0]["text"] == "Label"
        # Verify second element
        assert result.elements[1]["text"] == "Hello"
        assert result.elements[1]["children"] == []
        self.session.call_mcp_tool.assert_called_once_with(
            "get_all_ui_elements", {"timeout_ms": 2000}
        )

    # Application Management Tests
    @pytest.mark.sync

    def test_get_installed_apps_success(self):
        """Test successful installed apps retrieval."""
        # Arrange - Mock the _call_mcp_tool method
        mock_result = Mock()
        mock_result.success = True
        mock_result.data = '[{"name": "Calculator", "package_name": "com.calculator"}]'
        mock_result.request_id = "test-123"

        self.session.call_mcp_tool = MagicMock(return_value=mock_result)

        # Act
        result = self.mobile.get_installed_apps(
            start_menu=False, desktop=True, ignore_system_apps=True
        )

        # Assert
        assert result.success is True
        assert len(result.data) == 1
        self.session.call_mcp_tool.assert_called_once_with(
            "get_installed_apps",
            {"start_menu": False, "desktop": True, "ignore_system_apps": True},
        )

    @pytest.mark.sync


    def test_get_installed_apps_with_options(self):
        """Test installed apps with custom options."""
        # Arrange - Mock the _call_mcp_tool method
        mock_result = Mock()
        mock_result.success = True
        mock_result.data = "[]"
        mock_result.request_id = "test-123"

        self.session.call_mcp_tool = MagicMock(return_value=mock_result)

        # Act
        result = self.mobile.get_installed_apps(
            start_menu=True, desktop=False, ignore_system_apps=False
        )

        # Assert
        self.session.call_mcp_tool.assert_called_once_with(
            "get_installed_apps",
            {"start_menu": True, "desktop": False, "ignore_system_apps": False},
        )

    @pytest.mark.sync


    def test_start_app_success(self):
        """Test successful app start."""
        # Arrange
        mock_result = Mock()
        mock_result.success = True
        mock_result.data = '[{"pid": 1234, "name": "calculator"}]'
        mock_result.request_id = "test-123"

        self.session.call_mcp_tool = MagicMock(return_value=mock_result)

        # Act
        result = self.mobile.start_app("com.android.calculator2")

        # Assert
        assert isinstance(result, ProcessListResult)
        assert result.success is True
        self.session.call_mcp_tool.assert_called_once_with(
            "start_app", {"start_cmd": "com.android.calculator2"}
        )

    @pytest.mark.sync


    def test_start_app_with_activity(self):
        """Test app start with specific activity."""
        # Arrange
        mock_result = Mock()
        mock_result.success = True
        mock_result.data = '[{"pid": 1234, "name": "settings"}]'
        mock_result.request_id = "test-123"

        self.session.call_mcp_tool = MagicMock(return_value=mock_result)

        # Act
        result = self.mobile.start_app(
            "com.android.settings", activity=".MainActivity"
        )

        # Assert
        self.session.call_mcp_tool.assert_called_once_with(
            "start_app",
            {"start_cmd": "com.android.settings", "activity": ".MainActivity"},
        )

    @pytest.mark.sync


    def test_stop_app_by_cmd_success(self):
        """Test successful app stop by command."""
        # Arrange - Mock the _call_mcp_tool method
        mock_result = Mock()
        mock_result.success = True
        mock_result.request_id = "test-123"
        mock_result.error_message = ""

        self.session.call_mcp_tool = MagicMock(return_value=mock_result)

        # Act
        result = self.mobile.stop_app_by_cmd("com.android.calculator2")

        # Assert
        assert isinstance(result, AppOperationResult)
        assert result.success is True
        self.session.call_mcp_tool.assert_called_once_with(
            "stop_app_by_cmd", {"stop_cmd": "com.android.calculator2"}
        )

    # Screenshot Tests
    @pytest.mark.sync

    def test_screenshot_success(self):
        """Test successful screenshot."""
        # Arrange
        mock_result = Mock()
        mock_result.success = True
        mock_result.request_id = "test-123"
        mock_result.data = "/path/to/mobile_screenshot.png"

        self.session.call_mcp_tool = MagicMock(return_value=mock_result)

        # Act
        result = self.mobile.screenshot()

        # Assert
        assert isinstance(result, OperationResult)
        assert result.success is True
        assert result.data == "/path/to/mobile_screenshot.png"
        self.session.call_mcp_tool.assert_called_once_with("system_screenshot", {})

    # ADB URL Tests
    @pytest.mark.sync

    def test_get_adb_url_success_with_valid_mobile_env(self):
        """Test get_adb_url returns AdbUrlResult with valid adbkey_pub in mobile environment."""
        # Arrange
        self.mock_session.image_id = "mobile_latest"

        # Mock get_adb_link response
        mock_response = Mock()
        mock_response.body = Mock()
        mock_response.body.success = True
        mock_response.body.request_id = "adb-request-123"
        mock_response.body.data = Mock()
        mock_response.body.data.url = "adb connect 47.99.76.99:54848"

        self.mobile.session.agent_bay.client.get_adb_link = MagicMock(
            return_value=mock_response
        )

        # Act
        adbkey_pub = "test_adb_key..."
        result = self.mobile.get_adb_url(adbkey_pub)

        # Assert
        from agentbay import AdbUrlResult

        assert isinstance(result, AdbUrlResult)
        assert result.success is True
        assert result.request_id == "adb-request-123"
        assert result.data == "adb connect 47.99.76.99:54848"

    @pytest.mark.sync


    def test_get_adb_url_fails_on_non_mobile_env(self):
        """Test get_adb_url fails when session is not mobile environment."""
        # Arrange
        self.mock_session.image_id = "browser_latest"

        # Mock get_adb_link to return error response
        from agentbay import AdbUrlResult

        mock_response = Mock()
        mock_response.body = Mock()
        mock_response.body.success = False
        mock_response.body.request_id = "adb-request-error"
        mock_response.body.message = (
            "ImageTypeNotMatched: Expected: MobileUse, Actual: BrowserUse"
        )
        mock_response.body.data = None

        self.mobile.session.agent_bay.client.get_adb_link = MagicMock(
            return_value=mock_response
        )

        # Act
        adbkey_pub = "test_adb_key..."
        result = self.mobile.get_adb_url(adbkey_pub)

        # Assert - Should return AdbUrlResult with success=False
        assert isinstance(result, AdbUrlResult)
        assert result.success is False
        assert (
            "imagetypenotmatched" in result.error_message.lower()
            or "failed" in result.error_message.lower()
        )

    @pytest.mark.sync


    def test_get_adb_url_calls_get_link_with_correct_params(self):
        """Test get_adb_url calls client.get_adb_link with correct parameters."""
        # Arrange
        self.mock_session.image_id = "mobile_latest"

        mock_response = Mock()
        mock_response.body = Mock()
        mock_response.body.success = True
        mock_response.body.request_id = "adb-request-456"
        mock_response.body.data = Mock()
        mock_response.body.data.url = "adb connect 192.168.1.1:5555"

        self.mobile.session.agent_bay.client.get_adb_link = MagicMock(
            return_value=mock_response
        )

        # Act
        adbkey_pub = "test_key_123"
        result = self.mobile.get_adb_url(adbkey_pub)

        # Assert
        self.mobile.session.agent_bay.client.get_adb_link.assert_called_once()
        call_args = self.mobile.session.agent_bay.client.get_adb_link.call_args

        # Verify the request object
        request = call_args[0][0]
        assert request.authorization == f"Bearer {self.mock_session.agent_bay.api_key}"
        assert request.session_id == self.mock_session.session_id

        # Verify options contains adbkey_pub
        import json

        options_dict = json.loads(request.option)
        assert options_dict["adbkey_pub"] == adbkey_pub

    @pytest.mark.sync


    def test_get_adb_url_returns_correct_structure(self):
        """Test get_adb_url returns AdbUrlResult with all required fields."""
        # Arrange
        self.mock_session.image_id = "mobile_latest"
        mock_result = Mock()
        mock_result.success = True
        mock_result.request_id = "adb-req-789"
        mock_result.data = "adb connect 10.0.0.1:5555"

        self.mobile.session.get_link = Mock(return_value=mock_result)

        # Act
        result = self.mobile.get_adb_url("key_xyz")

        # Assert - verify result structure
        from agentbay import AdbUrlResult

        assert isinstance(result, AdbUrlResult)
        assert hasattr(result, "success")
        assert hasattr(result, "request_id")
        assert hasattr(result, "data")
        assert hasattr(result, "error_message")

    # Error Handling Tests
    @pytest.mark.sync

    def test_tap_mcp_failure(self):
        """Test tap when MCP tool fails."""
        # Arrange
        mock_result = Mock()
        mock_result.success = False
        mock_result.request_id = "test-123"
        mock_result.error_message = "MCP tool failed"

        self.session.call_mcp_tool = MagicMock(return_value=mock_result)

        # Act
        result = self.mobile.tap(100, 200)

        # Assert
        assert isinstance(result, BoolResult)
        assert result.success is False
        assert result.error_message == "MCP tool failed"

    @pytest.mark.sync


    def test_tap_exception(self):
        """Test tap when exception occurs."""
        # Arrange
        self.session.call_mcp_tool = MagicMock(side_effect=Exception("Network error"))

        # Act
        result = self.mobile.tap(100, 200)

        # Assert
        assert isinstance(result, BoolResult)
        assert result.success is False
        assert "Failed to tap" in result.error_message

    @pytest.mark.sync


    def test_get_clickable_ui_elements_exception(self):
        """Test UI elements retrieval when exception occurs."""
        # Arrange
        self.session.call_mcp_tool = Mock(side_effect=Exception("Network error"))

        # Act
        result = self.mobile.get_clickable_ui_elements()

        # Assert
        assert result.success is False
        assert "Failed to get clickable UI elements" in result.error_message
