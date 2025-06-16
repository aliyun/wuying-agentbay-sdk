import os
import time
import unittest
from agentbay import AgentBay
from agentbay.exceptions import AgentBayError
from agentbay.ui.ui import UI, KeyCode

class TestUISystemIntegration(unittest.TestCase):
    def setUp(self):
        api_key = os.getenv("AGENTBAY_API_KEY", "your_api_key")
        self.agent_bay = AgentBay(api_key=api_key)
        self.session = self.agent_bay.create()
        self.ui = UI(self.session)
        time.sleep(3)

    def test_get_clickable_ui_elements(self):
        try:
            clickable_elements = self.ui.get_clickable_ui_elements(timeout_ms=1000)
            self.assertIsInstance(clickable_elements, list)
            print("\nClickable UI Elements:")
            for element in clickable_elements:
                print(element)
        except AgentBayError as e:
            self.fail(f"get_clickable_ui_elements failed with error: {e}")

    def test_click(self):
        try:
            x, y = 100, 200
            self.ui.click(x, y, button="left")
            print(f"\nClicked on coordinates ({x}, {y}) successfully.")
        except AgentBayError as e:
            self.fail(f"click failed with error: {e}")

    def test_send_key(self):
        try:
            self.ui.send_key(KeyCode.HOME)
            print("\nSent HOME key successfully.")
        except AgentBayError as e:
            self.fail(f"send_key failed with error: {e}")

    def test_swipe(self):
        try:
            start_x, start_y, end_x, end_y, duration_ms = 100, 200, 300, 400, 500
            self.ui.swipe(start_x, start_y, end_x, end_y, duration_ms)
            print(f"\nSwipe performed successfully from ({start_x}, {start_y}) to ({end_x}, {end_y}) in {duration_ms}ms.")
        except AgentBayError as e:
            self.fail(f"swipe failed with error: {e}")

    def test_input_text(self):
        try:
            text = "Hello, world!"
            self.ui.input_text(text)
            print(f"\nInput text '{text}' successfully.")
        except AgentBayError as e:
            self.fail(f"input_text failed with error: {e}")

    def test_get_all_ui_elements(self):
        try:
            ui_elements = self.ui.get_all_ui_elements(timeout_ms=1000)
            self.assertIsInstance(ui_elements, list)
            print("\nAll UI Elements:")
            for element in ui_elements:
                print(element)
        except AgentBayError as e:
            self.fail(f"get_all_ui_elements failed with error: {e}")

    def test_screenshot(self):
        try:
            screenshot = self.ui.screenshot()
            self.assertIsInstance(screenshot, str)
            print(f"\nScreenshot saved to: {screenshot}")
        except AgentBayError as e:
            self.fail(f"screenshot failed with error: {e}")

if __name__ == "__main__":
    unittest.main()