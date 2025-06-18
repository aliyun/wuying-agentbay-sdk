import os
import time
import unittest
from agentbay import AgentBay
from agentbay.exceptions import AgentBayError
from agentbay.ui import KeyCode
from agentbay.session_params import CreateSessionParams


class TestMobileSystemIntegration(unittest.TestCase):
    def setUp(self):
        """
        Set up the test environment by creating a session and initializing ui model.
        """
        api_key = os.getenv("AGENTBAY_API_KEY", "your_api_key")  # Replace with your actual API key
        self.agent_bay = AgentBay(api_key=api_key)
        params = CreateSessionParams(
            image_id="mobile_latest",
        )
        self.session = self.agent_bay.create(params)
        self.ui = self.session.ui
        self.application = self.session.application
        time.sleep(3)

    def tearDown(self):
        """
        Clean up the test environment by deleting the session.
        """
        try:
            self.agent_bay.delete(self.session)
        except AgentBayError as e:
            print(f"Failed to delete session: {e}")
    def test_get_installed_apps(self):
        """
        Test retrieving installed applications.
        """
        try:
            installed_apps = self.application.get_installed_apps(
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
            start_result = self.application.start_app(start_cmd)
            self.assertIsInstance(start_result, list)
            print("\nStart App Result:", start_result)

            # Stop the application
            stop_cmd = "am force-stop com.autonavi.minimap"
            self.application.stop_app_by_cmd(stop_cmd)
            print("\nApplication stopped successfully.")
        except AgentBayError as e:
            self.fail(f"start_and_stop_app failed with error: {e}")

    def test_get_clickable_ui_elements(self):
        """
        Test retrieving clickable UI elements.
        """
        try:
            clickable_elements = self.ui.get_clickable_ui_elements(timeout_ms=1000)
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
            self.ui.click(x, y, button="left")
            print(f"\nClicked on coordinates ({x}, {y}) successfully.")
        except AgentBayError as e:
            self.fail(f"click failed with error: {e}")

    def test_send_key(self):
        """
        Test sending a key press event.
        """
        try:
            self.ui.send_key(KeyCode.HOME)
            print("\nSent HOME key successfully.")
        except AgentBayError as e:
            self.fail(f"send_key failed with error: {e}")

    def test_swipe(self):
        """
        Test performing a swipe gesture.
        """
        try:
            start_x, start_y, end_x, end_y, duration_ms = 100, 200, 300, 400, 500
            self.ui.swipe(start_x, start_y, end_x, end_y, duration_ms)
            print(f"\nSwipe performed successfully from ({start_x}, {start_y}) to ({end_x}, {end_y}) in {duration_ms}ms.")
        except AgentBayError as e:
            self.fail(f"swipe failed with error: {e}")

    def test_input_text(self):
        """
        Test inputting text into the active field.
        """
        try:
            text = "Hello, world!"
            self.ui.input_text(text)
            print(f"\nInput text '{text}' successfully.")
        except AgentBayError as e:
            self.fail(f"input_text failed with error: {e}")

    def test_get_all_ui_elements(self):
        """
        Test retrieving all UI elements.
        """
        try:
            ui_elements = self.ui.get_all_ui_elements(timeout_ms=1000)
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
            screenshot = self.ui.screenshot()
            self.assertIsInstance(screenshot, str)
            print(f"\nScreenshot saved to: {screenshot}")
        except AgentBayError as e:
            self.fail(f"screenshot failed with error: {e}")
if __name__ == "__main__":
    unittest.main()