import os
import time
import unittest
from agentbay import AgentBay
from agentbay.exceptions import AgentBayError
from agentbay.mobile import KeyCode


class TestMobileSystemIntegration(unittest.TestCase):
    def setUp(self):
        """
        Set up the test environment by creating a session and initializing MobileSystem.
        """
        api_key = os.getenv("AGENTBAY_API_KEY", "your_api_key")  # Replace with your actual API key
        self.agent_bay = AgentBay(api_key=api_key)
        self.session = self.agent_bay.create()
        self.mobile_system = self.session.mobile
        time.sleep(3)

    def test_get_installed_apps(self):
        """
        Test retrieving installed applications.
        """
        try:
            installed_apps = self.mobile_system.get_installed_apps(
                start_menu=True,
                desktop=False,
                ignore_system_apps=True
            )
            self.assertIsInstance(installed_apps, list)
            print("\nInstalled Applications:")
            for app in installed_apps:
                print(f"Name: {app.name}, Start Command: {app.start_cmd}")
        except AgentBayError as e:
            self.fail(f"get_installed_apps failed with error: {e}")

    def test_start_and_stop_app(self):
        """
        Test starting and stopping an application.
        """
        try:
            # Start an application
            start_cmd = "monkey -p com.autonavi.minimap -c android.intent.category.LAUNCHER 1"
            start_result = self.mobile_system.start_app(start_cmd)
            self.assertIsInstance(start_result, list)
            print("\nStart App Result:", start_result)

            # Stop the application
            stop_cmd = "am force-stop com.autonavi.minimap"
            self.mobile_system.stop_app_by_cmd(stop_cmd)
            print("\nApplication stopped successfully.")
        except AgentBayError as e:
            self.fail(f"start_and_stop_app failed with error: {e}")

    def test_get_clickable_ui_elements(self):
        """
        Test retrieving clickable UI elements.
        """
        try:
            clickable_elements = self.mobile_system.get_clickable_ui_elements(timeout_ms=1000)
            self.assertIsInstance(clickable_elements, list)
            print("\nClickable UI Elements:")
            for element in clickable_elements:
                print(element)
        except AgentBayError as e:
            self.fail(f"get_clickable_ui_elements failed with error: {e}")

    def test_click(self):
        """
        Test clicking on a specific coordinate.
        """
        try:
            x, y = 100, 200
            self.mobile_system.click(x, y, button="left")
            print(f"\nClicked on coordinates ({x}, {y}) successfully.")
        except AgentBayError as e:
            self.fail(f"click failed with error: {e}")

    def test_send_key(self):
        """
        Test sending a key press event.
        """
        try:
            self.mobile_system.send_key(KeyCode.HOME)
            print("\nSent HOME key successfully.")
        except AgentBayError as e:
            self.fail(f"send_key failed with error: {e}")

    def test_swipe(self):
        """
        Test performing a swipe gesture.
        """
        try:
            start_x, start_y, end_x, end_y, duration_ms = 100, 200, 300, 400, 500
            self.mobile_system.swipe(start_x, start_y, end_x, end_y, duration_ms)
            print(f"\nSwipe performed successfully from ({start_x}, {start_y}) to ({end_x}, {end_y}) in {duration_ms}ms.")
        except AgentBayError as e:
            self.fail(f"swipe failed with error: {e}")

    def test_input_text(self):
        """
        Test inputting text into the active field.
        """
        try:
            text = "Hello, world!"
            self.mobile_system.input_text(text)
            print(f"\nInput text '{text}' successfully.")
        except AgentBayError as e:
            self.fail(f"input_text failed with error: {e}")

    def test_get_all_ui_elements(self):
        """
        Test retrieving all UI elements.
        """
        try:
            ui_elements = self.mobile_system.get_all_ui_elements(timeout_ms=1000)
            self.assertIsInstance(ui_elements, list)
            print("\nAll UI Elements:")
            for element in ui_elements:
                print(element)
        except AgentBayError as e:
            self.fail(f"get_all_ui_elements failed with error: {e}")


    def test_screenshot(self):
        """
        Test taking a screenshot.
        """
        try:
            screenshot = self.mobile_system.screenshot()
            self.assertIsInstance(screenshot, str)
            print(f"\nScreenshot saved to: {screenshot}")
        except AgentBayError as e:
            self.fail(f"screenshot failed with error: {e}")
if __name__ == "__main__":
    unittest.main()