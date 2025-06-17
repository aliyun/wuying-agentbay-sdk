import unittest
from unittest.mock import MagicMock
from agentbay.application.application import ApplicationManager, InstalledApp, Process
from agentbay.exceptions import AgentBayError

class TestApplicationApi(unittest.TestCase):
    def setUp(self):
        self.mock_session = MagicMock()
        self.app_manager = ApplicationManager(self.mock_session)

    def test_get_installed_apps_success(self):
        self.app_manager._call_mcp_tool = MagicMock(return_value='''[
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
]''')
        apps = self.app_manager.get_installed_apps()
        self.assertEqual(len(apps), 3)
        self.assertIsInstance(apps[0], InstalledApp)
        self.assertEqual(apps[0].name, "美团")
        self.assertEqual(apps[1].name, "小红书")
        self.assertEqual(apps[2].name, "高德地图")

    def test_get_installed_apps_failure(self):
        self.app_manager._call_mcp_tool = MagicMock(side_effect=AgentBayError("Failed to get installed apps"))
        with self.assertRaises(AgentBayError) as context:
            self.app_manager.get_installed_apps()
        self.assertEqual(str(context.exception), "Failed to get installed apps")

    def test_start_app_success(self):
        self.app_manager._call_mcp_tool = MagicMock(return_value='''[
            {
                "pname": "com.autonavi.minimap",
                "pid": 12345,
                "cmdline": "monkey -p com.autonavi.minimap -c android.intent.category.LAUNCHER 1"
            }
        ]''')
        processes = self.app_manager.start_app("monkey -p com.autonavi.minimap -c android.intent.category.LAUNCHER 1")
        self.assertEqual(len(processes), 1)
        self.assertEqual(processes[0].pname, "com.autonavi.minimap")
        self.assertEqual(processes[0].pid, 12345)
        self.assertEqual(processes[0].cmdline, "monkey -p com.autonavi.minimap -c android.intent.category.LAUNCHER 1")

    def test_start_app_failure(self):
        self.app_manager._call_mcp_tool = MagicMock(side_effect=AgentBayError("Failed to start app"))
        with self.assertRaises(AgentBayError) as context:
            self.app_manager.start_app("monkey -p com.autonavi.minimap -c android.intent.category.LAUNCHER 1")
        self.assertEqual(str(context.exception), "Failed to start app")

    def test_stop_app_by_cmd_success(self):
        self.app_manager._call_mcp_tool = MagicMock(return_value=None)
        try:
            self.app_manager.stop_app_by_cmd("am force-stop com.autonavi.minimap")
        except AgentBayError:
            self.fail("stop_app_by_cmd raised AgentBayError unexpectedly!")

    def test_stop_app_by_cmd_failure(self):
        self.app_manager._call_mcp_tool = MagicMock(side_effect=AgentBayError("Failed to stop app"))
        with self.assertRaises(AgentBayError) as context:
            self.app_manager.stop_app_by_cmd("am force-stop com.autonavi.minimap")
        self.assertEqual(str(context.exception), "Failed to stop app")

    def test_stop_app_by_pname_success(self):
        self.app_manager._call_mcp_tool = MagicMock(return_value=None)
        try:
            self.app_manager.stop_app_by_pname("com.autonavi.minimap")
        except AgentBayError:
            self.fail("stop_app_by_pname raised AgentBayError unexpectedly!")

    def test_stop_app_by_pname_failure(self):
        self.app_manager._call_mcp_tool = MagicMock(side_effect=AgentBayError("Failed to stop app by pname"))
        with self.assertRaises(AgentBayError) as context:
            self.app_manager.stop_app_by_pname("com.autonavi.minimap")
        self.assertEqual(str(context.exception), "Failed to stop app by pname")

    def test_stop_app_by_pid_success(self):
        self.app_manager._call_mcp_tool = MagicMock(return_value=None)
        try:
            self.app_manager.stop_app_by_pid(12345)
        except AgentBayError:
            self.fail("stop_app_by_pid raised AgentBayError unexpectedly!")

    def test_stop_app_by_pid_failure(self):
        self.app_manager._call_mcp_tool = MagicMock(side_effect=AgentBayError("Failed to stop app by pid"))
        with self.assertRaises(AgentBayError) as context:
            self.app_manager.stop_app_by_pid(12345)
        self.assertEqual(str(context.exception), "Failed to stop app by pid")

    def test_list_visible_apps_success(self):
        self.app_manager._call_mcp_tool = MagicMock(return_value='''[
            {"pname": "com.autonavi.minimap", "pid": 12345, "cmdline": "cmd1"},
            {"pname": "com.xingin.xhs", "pid": 23456, "cmdline": "cmd2"}
        ]''')
        processes = self.app_manager.list_visible_apps()
        self.assertEqual(len(processes), 2)
        self.assertIsInstance(processes[0], Process)
        self.assertEqual(processes[0].pname, "com.autonavi.minimap")
        self.assertEqual(processes[1].pname, "com.xingin.xhs")

    def test_list_visible_apps_failure(self):
        self.app_manager._call_mcp_tool = MagicMock(side_effect=AgentBayError("Failed to list visible apps"))
        with self.assertRaises(AgentBayError) as context:
            self.app_manager.list_visible_apps()
        self.assertEqual(str(context.exception), "Failed to list visible apps")

if __name__ == "__main__":
    unittest.main()