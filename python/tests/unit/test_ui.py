import unittest
from unittest.mock import MagicMock
from agentbay.ui.ui import UI, KeyCode
from agentbay.exceptions import AgentBayError

class TestUIApi(unittest.TestCase):
    def setUp(self):
        self.mock_session = MagicMock()
        self.ui = UI(self.mock_session)

    def test_get_clickable_ui_elements_success(self):
        self.ui._call_mcp_tool = MagicMock(return_value='''[
            {
                "bounds": "48,90,1032,630",
                "className": "LinearLayout",
                "text": "digital_widget 5月31日周六",
                "type": "clickable",
                "resourceId": "com.android.deskclock:id/digital_widget",
                "index": 11,
                "isParent": false
            }
        ]''')
        elements = self.ui.get_clickable_ui_elements()
        self.assertEqual(len(elements), 1)
        self.assertEqual(elements[0]["bounds"], "48,90,1032,630")
        self.assertEqual(elements[0]["className"], "LinearLayout")
        self.assertEqual(elements[0]["text"], "digital_widget 5月31日周六")
        self.assertEqual(elements[0]["type"], "clickable")
        self.assertEqual(elements[0]["resourceId"], "com.android.deskclock:id/digital_widget")

    def test_get_clickable_ui_elements_failure(self):
        self.ui._call_mcp_tool = MagicMock(side_effect=AgentBayError("Failed to get clickable UI elements"))
        with self.assertRaises(AgentBayError) as context:
            self.ui.get_clickable_ui_elements()
        self.assertEqual(str(context.exception), "Failed to get clickable UI elements")

    def test_send_key_success(self):
        self.ui._call_mcp_tool = MagicMock(return_value=True)
        result = self.ui.send_key(KeyCode.HOME)
        self.assertTrue(result)

    def test_send_key_failure(self):
        self.ui._call_mcp_tool = MagicMock(side_effect=AgentBayError("Failed to send key"))
        with self.assertRaises(AgentBayError) as context:
            self.ui.send_key(KeyCode.HOME)
        self.assertEqual(str(context.exception), "Failed to send key")

    def test_swipe_success(self):
        self.ui._call_mcp_tool = MagicMock(return_value=None)
        try:
            self.ui.swipe(100, 200, 300, 400, duration_ms=500)
        except AgentBayError:
            self.fail("swipe raised AgentBayError unexpectedly!")

    def test_swipe_failure(self):
        self.ui._call_mcp_tool = MagicMock(side_effect=AgentBayError("Failed to perform swipe"))
        with self.assertRaises(AgentBayError) as context:
            self.ui.swipe(100, 200, 300, 400, duration_ms=500)
        self.assertEqual(str(context.exception), "Failed to perform swipe")

    def test_click_success(self):
        self.ui._call_mcp_tool = MagicMock(return_value=None)
        try:
            self.ui.click(150, 250, button="left")
        except AgentBayError:
            self.fail("click raised AgentBayError unexpectedly!")

    def test_click_failure(self):
        self.ui._call_mcp_tool = MagicMock(side_effect=AgentBayError("Failed to perform click"))
        with self.assertRaises(AgentBayError) as context:
            self.ui.click(150, 250, button="left")
        self.assertEqual(str(context.exception), "Failed to perform click")

    def test_input_text_success(self):
        self.ui._call_mcp_tool = MagicMock(return_value=None)
        try:
            self.ui.input_text("Hello, world!")
        except AgentBayError:
            self.fail("input_text raised AgentBayError unexpectedly!")

    def test_input_text_failure(self):
        self.ui._call_mcp_tool = MagicMock(side_effect=AgentBayError("Failed to input text"))
        with self.assertRaises(AgentBayError) as context:
            self.ui.input_text("Hello, world!")
        self.assertEqual(str(context.exception), "Failed to input text")

    def test_get_all_ui_elements_success(self):
        self.ui._call_mcp_tool = MagicMock(return_value='''[
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
        ]''')
        elements = self.ui.get_all_ui_elements()
        self.assertEqual(len(elements), 1)
        self.assertEqual(elements[0]["bounds"], "48,90,1032,630")
        self.assertEqual(elements[0]["className"], "LinearLayout")
        self.assertEqual(elements[0]["text"], "Sample Text")
        self.assertEqual(elements[0]["type"], "UIElement")
        self.assertEqual(elements[0]["resourceId"], "com.example:id/sample")
        self.assertEqual(len(elements[0]["children"]), 1)
        self.assertEqual(elements[0]["children"][0]["text"], "Child Text")

    def test_get_all_ui_elements_failure(self):
        self.ui._call_mcp_tool = MagicMock(side_effect=AgentBayError("Failed to get all UI elements"))
        with self.assertRaises(AgentBayError) as context:
            self.ui.get_all_ui_elements()
        self.assertEqual(str(context.exception), "Failed to get all UI elements")

    def test_screenshot_success(self):
        OSS_URL = "https://oss-url/screenshot.png"
        self.ui._call_mcp_tool = MagicMock(return_value=OSS_URL)
        result = self.ui.screenshot()
        self.assertEqual(result, OSS_URL)

    def test_screenshot_failure(self):
        self.ui._call_mcp_tool = MagicMock(side_effect=AgentBayError("Error in response: Failed to take screenshot"))
        with self.assertRaises(AgentBayError) as context:
            self.ui.screenshot()
        self.assertEqual(str(context.exception), "Error in response: Failed to take screenshot")

    def test_screenshot_exception_handling(self):
        self.ui._call_mcp_tool = MagicMock(side_effect=Exception("Network error"))
        with self.assertRaises(AgentBayError) as context:
            self.ui.screenshot()
        self.assertIn("Failed to take screenshot", str(context.exception))

if __name__ == "__main__":
    unittest.main()