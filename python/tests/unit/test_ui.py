import unittest
from unittest.mock import MagicMock
from agentbay.ui.ui import UI, KeyCode
from agentbay.exceptions import AgentBayError
from agentbay.model import OperationResult


class TestUIApi(unittest.TestCase):
    def setUp(self):
        self.mock_session = MagicMock()
        self.ui = UI(self.mock_session)

    def test_get_clickable_ui_elements_success(self):
        self.ui._call_mcp_tool = MagicMock(
            return_value=OperationResult(
                request_id="request-123",
                success=True,
                data="""[
            {
                "bounds": "48,90,1032,630",
                "className": "LinearLayout",
                "text": "digital_widget 5月31日周六",
                "type": "clickable",
                "resourceId": "com.android.deskclock:id/digital_widget",
                "index": 11,
                "isParent": false
            }
        ]"""
            )
        )
        success, elements = self.ui.get_clickable_ui_elements()
        self.assertTrue(success)
        self.assertEqual(len(elements), 1)
        self.assertEqual(elements[0]["bounds"], "48,90,1032,630")
        self.assertEqual(elements[0]["className"], "LinearLayout")
        self.assertEqual(elements[0]["text"], "digital_widget 5月31日周六")
        self.assertEqual(elements[0]["type"], "clickable")
        self.assertEqual(
            elements[0]["resourceId"], "com.android.deskclock:id/digital_widget"
        )

    def test_get_clickable_ui_elements_failure(self):
        self.ui._call_mcp_tool = MagicMock(
            return_value=OperationResult(
                request_id="request-123",
                success=False,
                error_message="Failed to get clickable UI elements"
            )
        )
        success, error_msg = self.ui.get_clickable_ui_elements()
        self.assertFalse(success)
        self.assertEqual(error_msg, "Failed to get clickable UI elements")

    def test_send_key_success(self):
        self.ui._call_mcp_tool = MagicMock(
            return_value=OperationResult(
                request_id="request-123",
                success=True,
                data=True
            )
        )
        success, result = self.ui.send_key(KeyCode.HOME)
        self.assertTrue(success)
        self.assertTrue(result)

    def test_send_key_failure(self):
        self.ui._call_mcp_tool = MagicMock(
            return_value=OperationResult(
                request_id="request-123",
                success=False,
                error_message="Failed to send key"
            )
        )
        success, error_msg = self.ui.send_key(KeyCode.HOME)
        self.assertFalse(success)
        self.assertEqual(error_msg, "Failed to send key")

    def test_swipe_success(self):
        self.ui._call_mcp_tool = MagicMock(
            return_value=OperationResult(
                request_id="request-123",
                success=True,
                data=None
            )
        )
        success, result = self.ui.swipe(100, 200, 300, 400, duration_ms=500)
        self.assertTrue(success)

    def test_swipe_failure(self):
        self.ui._call_mcp_tool = MagicMock(
            return_value=OperationResult(
                request_id="request-123",
                success=False,
                error_message="Failed to perform swipe"
            )
        )
        success, error_msg = self.ui.swipe(100, 200, 300, 400, duration_ms=500)
        self.assertFalse(success)
        self.assertEqual(error_msg, "Failed to perform swipe")

    def test_click_success(self):
        self.ui._call_mcp_tool = MagicMock(
            return_value=OperationResult(
                request_id="request-123",
                success=True,
                data=None
            )
        )
        success, result = self.ui.click(150, 250, button="left")
        self.assertTrue(success)

    def test_click_failure(self):
        self.ui._call_mcp_tool = MagicMock(
            return_value=OperationResult(
                request_id="request-123",
                success=False,
                error_message="Failed to perform click"
            )
        )
        success, error_msg = self.ui.click(150, 250, button="left")
        self.assertFalse(success)
        self.assertEqual(error_msg, "Failed to perform click")

    def test_input_text_success(self):
        self.ui._call_mcp_tool = MagicMock(
            return_value=OperationResult(
                request_id="request-123",
                success=True,
                data=None
            )
        )
        success, result = self.ui.input_text("Hello, world!")
        self.assertTrue(success)

    def test_input_text_failure(self):
        self.ui._call_mcp_tool = MagicMock(
            return_value=OperationResult(
                request_id="request-123",
                success=False,
                error_message="Failed to input text"
            )
        )
        success, error_msg = self.ui.input_text("Hello, world!")
        self.assertFalse(success)
        self.assertEqual(error_msg, "Failed to input text")

    def test_get_all_ui_elements_success(self):
        self.ui._call_mcp_tool = MagicMock(
            return_value=OperationResult(
                request_id="request-123",
                success=True,
                data="""[
            {
                "bounds": "48,90,1032,630",
                "className": "LinearLayout",
                "text": "Sample Text",
                "type": "UIElement",
                "resourceId": "com.example:id/sample",
                "index": 0,
                "isParent": true,
                "children": [
                    {
                        "bounds": "50,100,200,300",
                        "className": "TextView",
                        "text": "Child Text",
                        "type": "UIElement",
                        "resourceId": "com.example:id/child",
                        "index": 1,
                        "isParent": false,
                        "children": []
                    }
                ]
            }
        ]"""
            )
        )
        success, elements = self.ui.get_all_ui_elements()
        self.assertTrue(success)
        self.assertEqual(len(elements), 1)
        self.assertEqual(elements[0]["bounds"], "48,90,1032,630")
        self.assertEqual(elements[0]["className"], "LinearLayout")
        self.assertEqual(elements[0]["text"], "Sample Text")
        self.assertEqual(elements[0]["type"], "UIElement")
        self.assertEqual(elements[0]["resourceId"], "com.example:id/sample")
        self.assertEqual(len(elements[0]["children"]), 1)
        self.assertEqual(elements[0]["children"][0]["text"], "Child Text")

    def test_get_all_ui_elements_failure(self):
        self.ui._call_mcp_tool = MagicMock(
            return_value=OperationResult(
                request_id="request-123",
                success=False,
                error_message="Failed to get all UI elements"
            )
        )
        success, error_msg = self.ui.get_all_ui_elements()
        self.assertFalse(success)
        self.assertEqual(error_msg, "Failed to get all UI elements")

    def test_screenshot_success(self):
        OSS_URL = "https://oss-url/screenshot.png"
        self.ui._call_mcp_tool = MagicMock(
            return_value=OperationResult(
                request_id="request-123",
                success=True,
                data=OSS_URL
            )
        )
        success, result = self.ui.screenshot()
        self.assertTrue(success)
        self.assertEqual(result, OSS_URL)

    def test_screenshot_failure(self):
        self.ui._call_mcp_tool = MagicMock(
            return_value=OperationResult(
                request_id="request-123",
                success=False,
                error_message="Error in response: Failed to take screenshot"
            )
        )
        success, error_msg = self.ui.screenshot()
        self.assertFalse(success)
        self.assertEqual(error_msg, "Error in response: Failed to take screenshot")

    def test_screenshot_exception(self):
        self.ui._call_mcp_tool = MagicMock(side_effect=Exception("Network error"))
        success, error_msg = self.ui.screenshot()
        self.assertFalse(success)
        self.assertIn("Failed to take screenshot", error_msg)


if __name__ == "__main__":
    unittest.main()
