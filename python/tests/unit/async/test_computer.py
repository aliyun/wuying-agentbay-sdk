"""
Unit tests for Computer module.
Following TDD principles - tests first, then implementation.
"""

from unittest.mock import AsyncMock, Mock, patch

import pytest

from agentbay import AgentBayError
from agentbay import BoolResult, OperationResult
from agentbay import AsyncComputer, MouseButton, ScrollDirection


class TestComputer:
    """Test cases for Computer module."""

    def setup_method(self):
        """Set up test fixtures."""
        self.session = Mock()
        self.session.call_mcp_tool = AsyncMock()
        self.computer = AsyncComputer(self.session)

    @pytest.mark.asyncio


    async def test_computer_initialization(self):
        """Test Computer module initialization."""
        assert self.computer.session == self.session

    # Mouse Operations Tests
    @pytest.mark.asyncio

    async def test_click_mouse_success(self):
        """Test successful mouse click."""
        # Arrange
        mock_result = Mock()
        mock_result.success = True
        mock_result.request_id = "test-123"
        mock_result.error_message = ""

        self.session.call_mcp_tool = AsyncMock(return_value=mock_result)

        # Act
        result = await self.computer.click_mouse(100, 200)

        # Assert
        assert isinstance(result, BoolResult)
        assert result.success is True
        assert result.data is True
        self.session.call_mcp_tool.assert_called_once_with(
            "click_mouse", {"x": 100, "y": 200, "button": "left"}
        )

    @pytest.mark.asyncio


    async def test_click_mouse_with_button(self):
        """Test mouse click with specific button."""
        # Arrange
        mock_result = Mock()
        mock_result.success = True
        mock_result.request_id = "test-123"

        self.session.call_mcp_tool = AsyncMock(return_value=mock_result)

        # Act
        result = await self.computer.click_mouse(100, 200, button="right")

        # Assert
        self.session.call_mcp_tool.assert_called_once_with(
            "click_mouse", {"x": 100, "y": 200, "button": "right"}
        )

    @pytest.mark.asyncio


    async def test_click_mouse_invalid_button(self):
        """Test mouse click with invalid button."""
        # Act & Assert
        with pytest.raises(ValueError, match="Invalid button"):
            await self.computer.click_mouse(100, 200, button="invalid")

    @pytest.mark.asyncio


    async def test_click_mouse_with_enum(self):
        """Test mouse click with MouseButton enum."""
        # Arrange
        mock_result = Mock()
        mock_result.success = True
        mock_result.request_id = "test-123"

        self.session.call_mcp_tool = AsyncMock(return_value=mock_result)

        # Act
        result = await self.computer.click_mouse(100, 200, button=MouseButton.RIGHT)

        # Assert
        assert result.success is True
        self.session.call_mcp_tool.assert_called_once_with(
            "click_mouse", {"x": 100, "y": 200, "button": "right"}
        )

    @pytest.mark.asyncio


    async def test_click_mouse_with_double_left_enum(self):
        """Test mouse click with MouseButton.DOUBLE_LEFT enum."""
        # Arrange
        mock_result = Mock()
        mock_result.success = True
        mock_result.request_id = "test-123"

        self.session.call_mcp_tool = AsyncMock(return_value=mock_result)

        # Act
        result = await self.computer.click_mouse(
            100, 200, button=MouseButton.DOUBLE_LEFT
        )

        # Assert
        self.session.call_mcp_tool.assert_called_once_with(
            "click_mouse", {"x": 100, "y": 200, "button": "double_left"}
        )

    @pytest.mark.asyncio


    async def test_move_mouse_success(self):
        """Test successful mouse move."""
        # Arrange
        mock_result = Mock()
        mock_result.success = True
        mock_result.request_id = "test-123"

        self.session.call_mcp_tool = AsyncMock(return_value=mock_result)

        # Act
        result = await self.computer.move_mouse(150, 250)

        # Assert
        assert isinstance(result, BoolResult)
        assert result.success is True
        self.session.call_mcp_tool.assert_called_once_with(
            "move_mouse", {"x": 150, "y": 250}
        )

    @pytest.mark.asyncio


    async def test_drag_mouse_success(self):
        """Test successful mouse drag."""
        # Arrange
        mock_result = Mock()
        mock_result.success = True
        mock_result.request_id = "test-123"

        self.session.call_mcp_tool = AsyncMock(return_value=mock_result)

        # Act
        result = await self.computer.drag_mouse(100, 100, 200, 200)

        # Assert
        assert isinstance(result, BoolResult)
        assert result.success is True
        self.session.call_mcp_tool.assert_called_once_with(
            "drag_mouse",
            {"from_x": 100, "from_y": 100, "to_x": 200, "to_y": 200, "button": "left"},
        )

    @pytest.mark.asyncio


    async def test_scroll_success(self):
        """Test successful scroll."""
        # Arrange
        mock_result = Mock()
        mock_result.success = True
        mock_result.request_id = "test-123"

        self.session.call_mcp_tool = AsyncMock(return_value=mock_result)

        # Act
        result = await self.computer.scroll(300, 300)

        # Assert
        assert isinstance(result, BoolResult)
        assert result.success is True
        self.session.call_mcp_tool.assert_called_once_with(
            "scroll", {"x": 300, "y": 300, "direction": "up", "amount": 1}
        )

    @pytest.mark.asyncio


    async def test_scroll_with_params(self):
        """Test scroll with custom parameters."""
        # Arrange
        mock_result = Mock()
        mock_result.success = True
        mock_result.request_id = "test-123"

        self.session.call_mcp_tool = AsyncMock(return_value=mock_result)

        # Act
        result = await self.computer.scroll(300, 300, direction="down", amount=3)

        # Assert
        self.session.call_mcp_tool.assert_called_once_with(
            "scroll", {"x": 300, "y": 300, "direction": "down", "amount": 3}
        )

    @pytest.mark.asyncio


    async def test_get_cursor_position_success(self):
        """Test successful cursor position retrieval."""
        # Arrange
        mock_result = Mock()
        mock_result.success = True
        mock_result.request_id = "test-123"
        mock_result.data = {"x": 150, "y": 250}

        self.session.call_mcp_tool = AsyncMock(return_value=mock_result)

        # Act
        result = await self.computer.get_cursor_position()

        # Assert
        assert isinstance(result, OperationResult)
        assert result.success is True
        assert result.data == {"x": 150, "y": 250}
        self.session.call_mcp_tool.assert_called_once_with("get_cursor_position", {})

    # Keyboard Operations Tests
    @pytest.mark.asyncio

    async def test_input_text_success(self):
        """Test successful text input."""
        # Arrange
        mock_result = Mock()
        mock_result.success = True
        mock_result.request_id = "test-123"

        self.session.call_mcp_tool = AsyncMock(return_value=mock_result)

        # Act
        result = await self.computer.input_text("Hello World")

        # Assert
        assert isinstance(result, BoolResult)
        assert result.success is True
        self.session.call_mcp_tool.assert_called_once_with(
            "input_text", {"text": "Hello World"}
        )

    @pytest.mark.asyncio


    async def test_press_keys_success(self):
        """Test successful key press."""
        # Arrange
        mock_result = Mock()
        mock_result.success = True
        mock_result.request_id = "test-123"

        self.session.call_mcp_tool = AsyncMock(return_value=mock_result)

        # Act
        result = await self.computer.press_keys(["Ctrl", "a"])

        # Assert
        assert isinstance(result, BoolResult)
        assert result.success is True
        self.session.call_mcp_tool.assert_called_once_with(
            "press_keys", {"keys": ["Ctrl", "a"], "hold": False}
        )

    @pytest.mark.asyncio


    async def test_press_keys_with_hold(self):
        """Test key press with hold."""
        # Arrange
        mock_result = Mock()
        mock_result.success = True
        mock_result.request_id = "test-123"

        self.session.call_mcp_tool = AsyncMock(return_value=mock_result)

        # Act
        result = await self.computer.press_keys(["Shift"], hold=True)

        # Assert
        self.session.call_mcp_tool.assert_called_once_with(
            "press_keys", {"keys": ["Shift"], "hold": True}
        )

    @pytest.mark.asyncio


    async def test_release_keys_success(self):
        """Test successful key release."""
        # Arrange
        mock_result = Mock()
        mock_result.success = True
        mock_result.request_id = "test-123"

        self.session.call_mcp_tool = AsyncMock(return_value=mock_result)

        # Act
        result = await self.computer.release_keys(["Shift"])

        # Assert
        assert isinstance(result, BoolResult)
        assert result.success is True
        self.session.call_mcp_tool.assert_called_once_with(
            "release_keys", {"keys": ["Shift"]}
        )

    # Screen Operations Tests
    @pytest.mark.asyncio

    async def test_get_screen_size_success(self):
        """Test successful screen size retrieval."""
        # Arrange
        mock_result = Mock()
        mock_result.success = True
        mock_result.request_id = "test-123"
        # Session.call_mcp_tool returns McpToolResult.data as string (content[0].text),
        # for structured results it is usually a JSON string.
        mock_result.data = '{"width": 1920, "height": 1080, "dpiScalingFactor": 1.0}'

        self.session.call_mcp_tool = AsyncMock(return_value=mock_result)

        # Act
        result = await self.computer.get_screen_size()

        # Assert
        assert isinstance(result, OperationResult)
        assert result.success is True
        assert isinstance(result.data, dict)
        assert result.data["width"] == 1920
        assert result.data["height"] == 1080
        self.session.call_mcp_tool.assert_called_once_with("get_screen_size", {})

    @pytest.mark.asyncio


    async def test_screenshot_success(self):
        """Test successful screenshot."""
        # Arrange
        mock_result = Mock()
        mock_result.success = True
        mock_result.request_id = "test-123"
        mock_result.data = "/path/to/screenshot.png"

        self.session.call_mcp_tool = AsyncMock(return_value=mock_result)

        # Act
        result = await self.computer.screenshot()

        # Assert
        assert isinstance(result, OperationResult)
        assert result.success is True
        assert result.data == "/path/to/screenshot.png"
        self.session.call_mcp_tool.assert_called_once_with("system_screenshot", {})

    # Error Handling Tests
    @pytest.mark.asyncio

    async def test_click_mouse_mcp_failure(self):
        """Test mouse click when MCP tool fails."""
        # Arrange
        mock_result = Mock()
        mock_result.success = False
        mock_result.request_id = "test-123"
        mock_result.error_message = "MCP tool failed"

        self.session.call_mcp_tool = AsyncMock(return_value=mock_result)

        # Act
        result = await self.computer.click_mouse(100, 200)

        # Assert
        assert isinstance(result, BoolResult)
        assert result.success is False
        assert result.error_message == "MCP tool failed"

    @pytest.mark.asyncio


    async def test_click_mouse_exception(self):
        """Test mouse click when exception occurs."""
        # Arrange
        self.session.call_mcp_tool = AsyncMock(side_effect=Exception("Network error"))

        # Act
        result = await self.computer.click_mouse(100, 200)

        # Assert
        assert isinstance(result, BoolResult)
        assert result.success is False
        assert "Failed to click mouse" in result.error_message

    @pytest.mark.asyncio


    async def test_invalid_scroll_direction(self):
        """Test scroll with invalid direction."""
        # Act & Assert
        with pytest.raises(ValueError, match="Invalid direction"):
            await self.computer.scroll(100, 100, direction="invalid")

    @pytest.mark.asyncio


    async def test_scroll_with_enum(self):
        """Test scroll with ScrollDirection enum."""
        # Arrange
        mock_result = Mock()
        mock_result.success = True
        mock_result.request_id = "test-123"

        self.session.call_mcp_tool = AsyncMock(return_value=mock_result)

        # Act
        result = await self.computer.scroll(
            300, 300, direction=ScrollDirection.DOWN, amount=5
        )

        # Assert
        assert result.success is True
        self.session.call_mcp_tool.assert_called_once_with(
            "scroll", {"x": 300, "y": 300, "direction": "down", "amount": 5}
        )

    @pytest.mark.asyncio


    async def test_drag_mouse_with_enum(self):
        """Test drag mouse with MouseButton enum."""
        # Arrange
        mock_result = Mock()
        mock_result.success = True
        mock_result.request_id = "test-123"

        self.session.call_mcp_tool = AsyncMock(return_value=mock_result)

        # Act
        result = await self.computer.drag_mouse(
            100, 100, 200, 200, button=MouseButton.MIDDLE
        )

        # Assert
        assert result.success is True
        self.session.call_mcp_tool.assert_called_once_with(
            "drag_mouse",
            {
                "from_x": 100,
                "from_y": 100,
                "to_x": 200,
                "to_y": 200,
                "button": "middle",
            },
        )

    # Application Management Operations Tests
    @pytest.mark.asyncio

    async def test_list_visible_apps_success(self):
        """Test list_visible_apps success."""
        self.session.call_mcp_tool.return_value = Mock(
            success=True,
            request_id="test-request-id",
            data='[{"pname":"Calculator","pid":1234}]',
        )

        result = await self.computer.list_visible_apps()

        assert result.success is True
        assert len(result.data) == 1
        assert result.data[0].pname == "Calculator"
        self.session.call_mcp_tool.assert_called_once_with("list_visible_apps", {})

    @pytest.mark.asyncio


    async def test_get_installed_apps_success(self):
        """Test get_installed_apps success."""
        self.session.call_mcp_tool.return_value = Mock(
            success=True,
            request_id="test-request-id",
            data='[{"name":"Notepad","start_cmd":"notepad.exe"},{"name":"Calculator","start_cmd":"calc.exe"}]',
        )

        result = await self.computer.get_installed_apps()

        assert result.success is True
        assert len(result.data) == 2
        assert result.data[0].name == "Notepad"
        assert result.data[1].name == "Calculator"

    @pytest.mark.asyncio


    async def test_start_app_success(self):
        """Test start_app success."""
        self.session.call_mcp_tool.return_value = Mock(
            success=True,
            request_id="test-request-id",
            data='[{"pname":"notepad","pid":1234}]',
        )

        result = await self.computer.start_app("notepad.exe")

        assert result.success is True
        assert len(result.data) == 1
        assert result.data[0].pname == "notepad"
        assert result.data[0].pid == 1234

    @pytest.mark.asyncio


    async def test_start_app_with_working_directory(self):
        """Test start_app with working directory."""
        self.session.call_mcp_tool.return_value = Mock(
            success=True, request_id="test-request-id", data="[]"
        )

        result = await self.computer.start_app("notepad.exe", "/home/user/documents")

        assert result.success is True

    @pytest.mark.asyncio


    async def test_stop_app_by_pname_success(self):
        """Test stop_app_by_pname success."""
        self.session.call_mcp_tool.return_value = Mock(
            success=True, request_id="test-request-id"
        )

        result = await self.computer.stop_app_by_pname("notepad")

        assert result.success is True

    @pytest.mark.asyncio


    async def test_stop_app_by_pid_success(self):
        """Test stop_app_by_pid success."""
        self.session.call_mcp_tool.return_value = Mock(
            success=True, request_id="test-request-id"
        )

        result = await self.computer.stop_app_by_pid(1234)

        assert result.success is True

    @pytest.mark.asyncio


    async def test_stop_app_by_cmd_success(self):
        """Test stop_app_by_cmd success."""
        self.session.call_mcp_tool.return_value = Mock(
            success=True, request_id="test-request-id"
        )

        result = await self.computer.stop_app_by_cmd("pkill notepad")

        assert result.success is True

    @pytest.mark.asyncio


    async def test_application_management_methods_exist(self):
        """Test that all application management methods exist on Computer class."""
        # Assert
        assert hasattr(self.computer, "get_installed_apps")
        assert hasattr(self.computer, "start_app")
        assert hasattr(self.computer, "stop_app_by_pname")
        assert hasattr(self.computer, "stop_app_by_pid")
        assert hasattr(self.computer, "stop_app_by_cmd")
        assert hasattr(self.computer, "list_visible_apps")

        # Verify they are callable
        assert callable(self.computer.get_installed_apps)
        assert callable(self.computer.start_app)
        assert callable(self.computer.stop_app_by_pname)
        assert callable(self.computer.stop_app_by_pid)
        assert callable(self.computer.stop_app_by_cmd)
        assert callable(self.computer.list_visible_apps)
