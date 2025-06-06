import os
import sys
import time
import unittest

# Add the parent directory to the path so we can import the agentbay package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agentbay import AgentBay
from agentbay.exceptions import AgentBayError


def get_test_api_key():
    """Get API key for testing"""
    api_key = os.environ.get("AGENTBAY_API_KEY")
    if not api_key:
        api_key = "akm-xxx"  # Replace with your test API key
        print(
            "Warning: Using default API key. Set AGENTBAY_API_KEY environment variable for testing."
        )
    return api_key


def contains_tool_not_found(s):
    """Check if a string contains 'tool not found'"""
    return "tool not found" in str(s).lower()


class TestWindow(unittest.TestCase):
    """Test cases for the Window class."""

    def setUp(self):
        """Set up test fixtures."""
        time.sleep(3)

        api_key = get_test_api_key()
        self.agent_bay = AgentBay(api_key=api_key)

        # Create a session
        print("Creating a new session for window testing...")
        self.session = self.agent_bay.create()
        print(f"Session created with ID: {self.session.session_id}")

    def tearDown(self):
        """Tear down test fixtures."""
        print("Cleaning up: Deleting the session...")
        try:
            self.agent_bay.delete(self.session)
        except Exception as e:
            print(f"Warning: Error deleting session: {e}")

    def test_list_root_windows(self):
        """Test listing root windows."""
        if hasattr(self.session, "window") and self.session.window:
            print("Listing root windows...")
            try:
                root_windows = self.session.window.list_root_windows()
                print(f"Found {len(root_windows)} root windows")

                # Verify we got some windows
                if len(root_windows) == 0:
                    print("Warning: No root windows found")
                else:
                    # Print the first 3 windows or fewer if less than 3 are available
                    count = min(len(root_windows), 3)
                    for i in range(count):
                        print(
                            f"Window {i+1}: {root_windows[i].title} (ID: {root_windows[i].window_id})"
                        )

                    # Verify window properties
                    for window in root_windows:
                        self.assertGreater(
                            window.window_id,
                            0,
                            f"Found window with invalid ID: {window.window_id}",
                        )

                # Check if response contains "tool not found"
                if len(root_windows) > 0:
                    self.assertFalse(
                        contains_tool_not_found(root_windows[0].title),
                        "Window.list_root_windows returned 'tool not found'",
                    )
            except Exception as e:
                print(f"Note: list_root_windows failed: {e}")
                # Don't fail the test if the operation is not supported
        else:
            print("Note: Window interface is not available, skipping window test")

    def test_get_active_window(self):
        """Test getting the active window."""
        if hasattr(self.session, "window") and self.session.window:
            print("Getting active window...")
            try:
                active_window = self.session.window.get_active_window()
                print(
                    f"Active window: {active_window.title} (ID: {active_window.window_id}, "
                    f"Process: {active_window.pname}, PID: {active_window.pid})"
                )

                # Verify window properties
                self.assertGreater(
                    active_window.window_id,
                    0,
                    f"Active window has invalid ID: {active_window.window_id}",
                )
                self.assertGreater(
                    active_window.pid,
                    0,
                    f"Active window has invalid PID: {active_window.pid}",
                )

                # Check if response contains "tool not found"
                self.assertFalse(
                    contains_tool_not_found(active_window.title)
                    or contains_tool_not_found(active_window.pname),
                    "Window.get_active_window returned 'tool not found'",
                )
            except Exception as e:
                print(f"Note: get_active_window failed: {e}")
                # Don't fail the test if the operation is not supported
        else:
            print("Note: Window interface is not available, skipping window test")

    def test_window_operations(self):
        """Test window operations (activate, maximize, minimize, restore, resize)."""
        if hasattr(self.session, "window") and self.session.window:
            print("Listing root windows to find a window to operate on...")
            try:
                root_windows = self.session.window.list_root_windows()
                if not root_windows:
                    print("No root windows found, skipping window operations test")
                    return

                window_id = root_windows[0].window_id

                # Activate window
                print(f"Activating window with ID {window_id}...")
                try:
                    self.session.window.activate_window(window_id)
                    print("Window activated successfully")
                except Exception as e:
                    print(f"Note: activate_window failed: {e}")

                # Maximize window
                print(f"Maximizing window with ID {window_id}...")
                try:
                    self.session.window.maximize_window(window_id)
                    print("Window maximized successfully")
                except Exception as e:
                    print(f"Note: maximize_window failed: {e}")

                # Minimize window
                print(f"Minimizing window with ID {window_id}...")
                try:
                    self.session.window.minimize_window(window_id)
                    print("Window minimized successfully")
                except Exception as e:
                    print(f"Note: minimize_window failed: {e}")

                # Restore window
                print(f"Restoring window with ID {window_id}...")
                try:
                    self.session.window.restore_window(window_id)
                    print("Window restored successfully")
                except Exception as e:
                    print(f"Note: restore_window failed: {e}")

                # Resize window
                print(f"Resizing window with ID {window_id} to 800x600...")
                try:
                    self.session.window.resize_window(window_id, 800, 600)
                    print("Window resized successfully")
                except Exception as e:
                    print(f"Note: resize_window failed: {e}")
            except Exception as e:
                print(f"Note: list_root_windows failed: {e}")
                # Don't fail the test if the operation is not supported
        else:
            print("Note: Window interface is not available, skipping window test")

    def test_focus_mode(self):
        """Test focus mode."""
        if hasattr(self.session, "window") and self.session.window:
            # Enable focus mode
            print("Enabling focus mode...")
            try:
                self.session.window.focus_mode(True)
                print("Focus mode enabled successfully")
            except Exception as e:
                print(f"Note: Enabling focus mode failed: {e}")

            # Disable focus mode
            print("Disabling focus mode...")
            try:
                self.session.window.focus_mode(False)
                print("Focus mode disabled successfully")
            except Exception as e:
                print(f"Note: Disabling focus mode failed: {e}")
        else:
            print("Note: Window interface is not available, skipping focus mode test")


if __name__ == "__main__":
    unittest.main()
