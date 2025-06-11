import unittest
from unittest.mock import MagicMock
from agentbay.mobile import MobileSystem, InstalledApp
from agentbay.exceptions import AgentBayError


class TestMobileApi(unittest.TestCase):
    def setUp(self):
        # Create a mock session
        self.mock_session = MagicMock()
        self.mobile_system = MobileSystem(self.mock_session)

    def test_get_installed_apps_success(self):
        # Mock _call_mcp_tool return value
        self.mobile_system._call_mcp_tool = MagicMock(return_value='''[
    {
        "name" : "美团",
        "start_cmd" : "monkey -p com.sankuai.meituan -c android.intent.category.LAUNCHER 1",
        "stop_cmd" : "am force-stop com.sankuai.meituan",
        "work_directory" : ""
    },
    {
        "name" : "小红书",
        "start_cmd" : "monkey -p com.xingin.xhs -c android.intent.category.LAUNCHER 1",
        "stop_cmd" : "am force-stop com.xingin.xhs",
        "work_directory" : ""
    },
    {
        "name" : "高德地图",
        "start_cmd" : "monkey -p com.autonavi.minimap -c android.intent.category.LAUNCHER 1",
        "stop_cmd" : "am force-stop com.autonavi.minimap",
        "work_directory" : ""
    }
]
''')


        # Call get_installed_apps method
        apps = self.mobile_system.get_installed_apps()

        # Validate the result
        self.assertEqual(len(apps), 3)

        # First application
        self.assertIsInstance(apps[0], InstalledApp)
        self.assertEqual(apps[0].name, "美团")
        self.assertEqual(apps[0].start_cmd, "monkey -p com.sankuai.meituan -c android.intent.category.LAUNCHER 1")
        self.assertEqual(apps[0].stop_cmd, "am force-stop com.sankuai.meituan")
        self.assertEqual(apps[0].work_dir, "")

        # Second application
        self.assertIsInstance(apps[1], InstalledApp)
        self.assertEqual(apps[1].name, "小红书")
        self.assertEqual(apps[1].start_cmd, "monkey -p com.xingin.xhs -c android.intent.category.LAUNCHER 1")
        self.assertEqual(apps[1].stop_cmd, "am force-stop com.xingin.xhs")
        self.assertEqual(apps[1].work_dir, "")

        # Third application
        self.assertIsInstance(apps[2], InstalledApp)
        self.assertEqual(apps[2].name, "高德地图")
        self.assertEqual(apps[2].start_cmd, "monkey -p com.autonavi.minimap -c android.intent.category.LAUNCHER 1")
        self.assertEqual(apps[2].stop_cmd, "am force-stop com.autonavi.minimap")
        self.assertEqual(apps[2].work_dir, "")

    def test_get_installed_apps_failure(self):
        # 模拟 _call_mcp_tool 抛出异常
        self.mobile_system._call_mcp_tool = MagicMock(side_effect=AgentBayError("Failed to get installed apps"))

        # 调用 get_installed_apps 方法并验证异常
        with self.assertRaises(AgentBayError) as context:
            self.mobile_system.get_installed_apps()

        self.assertEqual(str(context.exception), "Failed to get installed apps")

    def test_start_app_success(self):
        # Mock _call_mcp_tool return value
        self.mobile_system._call_mcp_tool = MagicMock(return_value='''[
            {
                "pname": "com.autonavi.minimap",
                "pid": 12345,
                "cmdline": "monkey -p com.autonavi.minimap -c android.intent.category.LAUNCHER 1"
            }
        ]''')

        # Call start_app method
        processes = self.mobile_system.start_app("monkey -p com.autonavi.minimap -c android.intent.category.LAUNCHER 1")

        # Validate the result
        self.assertEqual(len(processes), 1)
        self.assertEqual(processes[0].pname, "com.autonavi.minimap")
        self.assertEqual(processes[0].pid, 12345)
        self.assertEqual(processes[0].cmdline, "monkey -p com.autonavi.minimap -c android.intent.category.LAUNCHER 1")

    def test_start_app_failure(self):
        # Mock _call_mcp_tool to raise an exception
        self.mobile_system._call_mcp_tool = MagicMock(side_effect=AgentBayError("Failed to start app"))

        # Call start_app and validate exception
        with self.assertRaises(AgentBayError) as context:
            self.mobile_system.start_app("monkey -p com.autonavi.minimap -c android.intent.category.LAUNCHER 1")

        self.assertEqual(str(context.exception), "Failed to start app")

    def test_stop_app_by_cmd_success(self):
        # Mock _call_mcp_tool return value
        self.mobile_system._call_mcp_tool = MagicMock(return_value=None)

        # Call stop_app_by_cmd method
        try:
            self.mobile_system.stop_app_by_cmd("am force-stop com.autonavi.minimap")
        except AgentBayError:
            self.fail("stop_app_by_cmd raised AgentBayError unexpectedly!")

    def test_stop_app_by_cmd_failure(self):
        # Mock _call_mcp_tool to raise an exception
        self.mobile_system._call_mcp_tool = MagicMock(side_effect=AgentBayError("Failed to stop app"))

        # Call stop_app_by_cmd and validate exception
        with self.assertRaises(AgentBayError) as context:
            self.mobile_system.stop_app_by_cmd("am force-stop com.autonavi.minimap")

        self.assertEqual(str(context.exception), "Failed to stop app")

    def test_get_clickable_ui_elements_success(self):
        # Mock _call_mcp_tool return value
        self.mobile_system._call_mcp_tool = MagicMock(return_value='''[
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

        # Call get_clickable_ui_elements method
        elements = self.mobile_system.get_clickable_ui_elements()

        # Validate the result
        self.assertEqual(len(elements), 1)
        self.assertEqual(elements[0]["bounds"], "48,90,1032,630")
        self.assertEqual(elements[0]["className"], "LinearLayout")
        self.assertEqual(elements[0]["text"], "digital_widget 5月31日周六")
        self.assertEqual(elements[0]["type"], "clickable")
        self.assertEqual(elements[0]["resourceId"], "com.android.deskclock:id/digital_widget")

    def test_get_clickable_ui_elements_failure(self):
        # Mock _call_mcp_tool to raise an exception
        self.mobile_system._call_mcp_tool = MagicMock(side_effect=AgentBayError("Failed to get clickable UI elements"))

        # Call get_clickable_ui_elements and validate exception
        with self.assertRaises(AgentBayError) as context:
            self.mobile_system.get_clickable_ui_elements()

        self.assertEqual(str(context.exception), "Failed to get clickable UI elements")

    def test_send_key_success(self):
        # Mock _call_mcp_tool return value
        self.mobile_system._call_mcp_tool = MagicMock(return_value=True)

        # Call send_key method
        result = self.mobile_system.send_key(3)  # KeyCode.HOME

        # Validate the result
        self.assertTrue(result)

    def test_send_key_failure(self):
        # Mock _call_mcp_tool to raise an exception
        self.mobile_system._call_mcp_tool = MagicMock(side_effect=AgentBayError("Failed to send key"))

        # Call send_key and validate exception
        with self.assertRaises(AgentBayError) as context:
            self.mobile_system.send_key(3)  # KeyCode.HOME

        self.assertEqual(str(context.exception), "Failed to send key")

    def test_swipe_success(self):
        # Mock _call_mcp_tool return value
        self.mobile_system._call_mcp_tool = MagicMock(return_value=None)

        # Call swipe method
        try:
            self.mobile_system.swipe(100, 200, 300, 400, duration_ms=500)
        except AgentBayError:
            self.fail("swipe raised AgentBayError unexpectedly!")

    def test_swipe_failure(self):
        # Mock _call_mcp_tool to raise an exception
        self.mobile_system._call_mcp_tool = MagicMock(side_effect=AgentBayError("Failed to perform swipe"))

        # Call swipe and validate exception
        with self.assertRaises(AgentBayError) as context:
            self.mobile_system.swipe(100, 200, 300, 400, duration_ms=500)

        self.assertEqual(str(context.exception), "Failed to perform swipe")

    def test_click_success(self):
        # Mock _call_mcp_tool return value
        self.mobile_system._call_mcp_tool = MagicMock(return_value=None)

        # Call click method
        try:
            self.mobile_system.click(150, 250, button="left")
        except AgentBayError:
            self.fail("click raised AgentBayError unexpectedly!")

    def test_click_failure(self):
        # Mock _call_mcp_tool to raise an exception
        self.mobile_system._call_mcp_tool = MagicMock(side_effect=AgentBayError("Failed to perform click"))

        # Call click and validate exception
        with self.assertRaises(AgentBayError) as context:
            self.mobile_system.click(150, 250, button="left")

        self.assertEqual(str(context.exception), "Failed to perform click")

    def test_input_text_success(self):
        # Mock _call_mcp_tool return value
        self.mobile_system._call_mcp_tool = MagicMock(return_value=None)

        # Call input_text method
        try:
            self.mobile_system.input_text("Hello, world!")
        except AgentBayError:
            self.fail("input_text raised AgentBayError unexpectedly!")

    def test_input_text_failure(self):
        # Mock _call_mcp_tool to raise an exception
        self.mobile_system._call_mcp_tool = MagicMock(side_effect=AgentBayError("Failed to input text"))

        # Call input_text and validate exception
        with self.assertRaises(AgentBayError) as context:
            self.mobile_system.input_text("Hello, world!")

        self.assertEqual(str(context.exception), "Failed to input text")

    def test_get_all_ui_elements_success(self):
        # Mock _call_mcp_tool return value
        self.mobile_system._call_mcp_tool = MagicMock(return_value='''[
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

        # Call get_all_ui_elements method
        elements = self.mobile_system.get_all_ui_elements()

        # Validate the result
        self.assertEqual(len(elements), 1)
        self.assertEqual(elements[0]["bounds"], "48,90,1032,630")
        self.assertEqual(elements[0]["className"], "LinearLayout")
        self.assertEqual(elements[0]["text"], "Sample Text")
        self.assertEqual(elements[0]["type"], "UIElement")
        self.assertEqual(elements[0]["resourceId"], "com.example:id/sample")
        self.assertEqual(len(elements[0]["children"]), 1)
        self.assertEqual(elements[0]["children"][0]["text"], "Child Text")

    def test_get_all_ui_elements_failure(self):
        # Mock _call_mcp_tool to raise an exception
        self.mobile_system._call_mcp_tool = MagicMock(side_effect=AgentBayError("Failed to get all UI elements"))

        # Call get_all_ui_elements and validate exception
        with self.assertRaises(AgentBayError) as context:
            self.mobile_system.get_all_ui_elements()

        self.assertEqual(str(context.exception), "Failed to get all UI elements")

if __name__ == "__main__":
    unittest.main()