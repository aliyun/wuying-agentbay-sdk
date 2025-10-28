import os
import sys
import unittest
import typing
from agentbay.session import Session
from agentbay.session_params import CreateSessionParams
from agentbay.exceptions import SessionError
from agentbay.model.response import AdbUrlResult

from agentbay import AgentBay

# Add the parent directory to the path so we can import the agentbay package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def get_test_api_key():
    api_key = os.environ.get("AGENTBAY_API_KEY")
    if not api_key:
        api_key = "akm-xxx"  # Replace with your test API key
        print(
            "Warning: Using default API key. Set AGENTBAY_API_KEY environment variable for testing."
        )
    return api_key


class TestMobileGetAdbUrl(unittest.TestCase):
    """Integration test for mobile.get_adb_url API."""

    @classmethod
    def setUpClass(cls):
        api_key = get_test_api_key()
        cls.agent_bay = AgentBay(api_key=api_key)
        print("Creating a new session for mobile ADB URL testing...")
        # Use mobile_latest image for mobile environment
        params = CreateSessionParams(image_id="mobile_latest")
        result = cls.agent_bay.create(params=params)
        cls.session = getattr(result, "session", None)
        print(f"Session created with ID: {getattr(cls.session, 'session_id', None)}")
        print(f"Request ID: {getattr(result, 'request_id', None)}")

    @classmethod
    def tearDownClass(cls):
        print("Cleaning up: Deleting the session...")
        try:
            if cls.session is not None:
                result = cls.agent_bay.delete(cls.session)
                print(
                    f"Session deleted. Success: {getattr(result, 'success', None)}, Request ID: {getattr(result, 'request_id', None)}"
                )
            else:
                print("No session to delete.")
        except Exception as e:
            print(f"Warning: Error deleting session: {e}")

    def test_get_adb_url_e2e_with_valid_key(self):
        """Test session.mobile.get_adb_url() returns AdbUrlResult with valid adbkey_pub."""
        self.assertIsNotNone(self.session, "Session was not created successfully.")
        session: Session = typing.cast(Session, self.session)
        
        # Create a test ADB key
        adbkey_pub = "QAAAAM0muSn7yQCYRGkiXUXONYu35uaz8f2btkbjh07lNAHTRfTlvzeUXoqvoAgHyKhVGk+4exvjH9ml5kOUxY7LUEQ+a43zBkKtKPpLBMvgPZHYxvcdUnwQK2DOWlwUldZWwjXXGXav0vuioe7HHvkTc/LINIoeqJ//dkOzQehUdW0IOnzEm9v7MQhoSofsVxR3I2hmR012+EBWCzpqCS5h/WzoDJdnBCcxpMZMKDjYAxha8I50lOqpkdlNk0lTJRWt3TW5BopsRhK7tiK3IN4UH7wevhEeLQ7ahGuTZDFn9MXKOlv2nttOQouW2Xpv+3rxAUZcesqQM40TssSWn2mi7FZ28A65iuM3DSm4HxkVi3NiU99r4C0DUyDvrcmBq+hW7OAFeqKNctez/vFd25KNLoyjtRXjR9hkAiT3LgyMg2Wh/SRUJxHEdYjCibm9yi3Hs8sYuP9NVzjD8tXf/ePM31BWmDen/7HTMXRLGHkzWAhtNRmR9cbyt6ImRHvY0f2SPT/7n0uNo3TKHj+muQBOGSReJKKoEXZ0bcZgA5Z2Us/iW5gcLhh0mr5r0B1Kdz9aSNgbCygZXDMtl7lndBwEZ4wwgAKWY9rDfm58fIlQYwSzx4vosVIxI7ZbXuQx2ONKe7P46Aakeu1yzuQeFnuDGvuJmVK6JuV2/bDFHvvj8fotRA8JeQEAAQA="
        
        print(f"Calling session.mobile.get_adb_url() with adbkey_pub...")
        result = session.mobile.get_adb_url(adbkey_pub)
        
        self.assertTrue(result.success, f"session.mobile.get_adb_url() did not succeed: {result.error_message}")
        self.assertIsInstance(result, AdbUrlResult, "Result should be AdbUrlResult instance")
        
        adb_url = result.data
        print(f"ADB URL: {adb_url}")
        self.assertIsInstance(adb_url, str)
        self.assertTrue(
            adb_url.startswith("adb connect"),
            f"Returned ADB URL should start with 'adb connect', got: {adb_url}",
        )

    def test_get_adb_url_returns_valid_adb_url(self):
        """Test session.mobile.get_adb_url() returns properly formatted URL."""
        self.assertIsNotNone(self.session, "Session was not created successfully.")
        session: Session = typing.cast(Session, self.session)
        
        adbkey_pub = "test_key_123"
        print(f"Calling session.mobile.get_adb_url()...")
        result = session.mobile.get_adb_url(adbkey_pub)
        
        self.assertTrue(result.success)
        adb_url = result.data
        print(f"ADB URL: {adb_url}")
        
        # Verify URL format: "adb connect <IP>:<Port>"
        parts = adb_url.split()
        self.assertEqual(len(parts), 3, f"URL should have format 'adb connect <address>', got: {adb_url}")
        self.assertEqual(parts[0], "adb")
        self.assertEqual(parts[1], "connect")
        
        # Extract and verify IP:Port part
        address_parts = parts[2].split(":")
        self.assertEqual(len(address_parts), 2, f"Address should be <IP>:<Port>, got: {parts[2]}")

    def test_get_adb_url_request_id_exists(self):
        """Test session.mobile.get_adb_url() result has valid request_id."""
        self.assertIsNotNone(self.session, "Session was not created successfully.")
        session: Session = typing.cast(Session, self.session)
        
        adbkey_pub = "test_key_xyz"
        print(f"Calling session.mobile.get_adb_url()...")
        result = session.mobile.get_adb_url(adbkey_pub)
        
        self.assertTrue(result.success)
        self.assertIsNotNone(result.request_id, "Request ID should not be None")
        self.assertTrue(len(result.request_id) > 0, "Request ID should not be empty")
        print(f"Request ID: {result.request_id}")

    def test_get_adb_url_fails_on_non_mobile_image(self):
        """Test session.mobile.get_adb_url() fails when session uses non-mobile image."""
        # Create a new browser session
        print("Creating browser session for negative test...")
        params = CreateSessionParams(image_id="browser_latest")
        result = self.agent_bay.create(params=params)
        browser_session = getattr(result, "session", None)
        
        self.assertIsNotNone(browser_session, "Browser session was not created successfully.")
        
        try:
            adbkey_pub = "test_key_456"
            print(f"Calling session.mobile.get_adb_url() on browser session...")
            result = browser_session.mobile.get_adb_url(adbkey_pub)
            
            # Should fail because this is not a mobile environment
            self.assertFalse(result.success, "get_adb_url() should fail on non-mobile image")
            self.assertIn("mobile", result.error_message.lower(), "Error message should mention mobile environment")
            print(f"Expected error: {result.error_message}")
        finally:
            # Clean up browser session
            try:
                self.agent_bay.delete(browser_session)
            except Exception as e:
                print(f"Warning: Error deleting browser session: {e}")


if __name__ == "__main__":
    unittest.main()
