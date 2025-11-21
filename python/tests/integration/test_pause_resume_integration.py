"""Integration tests for Session pause and resume operations."""
import os
import time
import unittest
from uuid import uuid4
from dotenv import load_dotenv

from agentbay import AgentBay,CreateSessionParams
from agentbay.agentbay import Config
from agentbay.model.response import SessionPauseResult, SessionResumeResult
from agentbay.exceptions import AgentBayError


def get_test_api_key():
    """Get API key for testing."""
    return os.environ.get("AGENTBAY_API_KEY")


def get_test_endpoint():
    """Get endpoint for testing."""
    return os.environ.get("AGENTBAY_ENDPOINT")


class TestSessionPauseResumeIntegration(unittest.TestCase):
    """Integration tests for Session pause and resume operations."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures for the entire test class."""
        # Load environment variables from .env file
        load_dotenv()
        
        # Get API Key and Endpoint
        api_key = get_test_api_key()
        if not api_key:
            raise unittest.SkipTest("AGENTBAY_API_KEY environment variable not set")

        endpoint = get_test_endpoint()

        # Initialize AgentBay client
        if endpoint:
            config = Config(endpoint=endpoint, timeout_ms=60000)
            cls.agent_bay = AgentBay(api_key=api_key, cfg=config)
            print(f"Using endpoint: {endpoint}")
        else:
            cls.agent_bay = AgentBay(api_key=api_key)
            print("Using default endpoint")

    def setUp(self):
        """Set up test fixtures for each test method."""
        self.test_sessions = []  # Track sessions for cleanup in each test

    def tearDown(self):
        """Clean up test sessions after each test method."""
        print("\nCleaning up test sessions for this test...")
        for session in self.test_sessions:
            try:
                # Delete session
                result = self.agent_bay.delete(session)
                if result.success:
                    print(f"  ✓ Deleted session: {session.session_id}")
                else:
                    print(f"  ✗ Failed to delete session: {session.session_id}")
            except Exception as e:
                print(f"  ✗ Error deleting session {session.session_id}: {e}")
        # Clear the list for next test
        self.test_sessions = []

    # @classmethod
    # def tearDownClass(cls):
    #     """Clean up any remaining test sessions."""
    #     print("\nCleaning up test sessions...")
    #     for session in cls.test_sessions:
    #         try:
    #             # Delete session
    #             result = cls.agent_bay.delete(session)
    #             if result.success:
    #                 print(f"  ✓ Deleted session: {session.session_id}")
    #             else:
    #                 print(f"  ✗ Failed to delete session: {session.session_id}")
    #         except Exception as e:
    #             print(f"  ✗ Error deleting session {session.session_id}: {e}")

    def _create_test_session(self):
        """Helper method to create a test session."""
        session_name = f"test-pause-resume-{uuid4().hex[:8]}"
        print(f"\nCreating test session: {session_name}")

        # Create session
        params = CreateSessionParams(
            # image_id="imgc-0ab5takggkr3iekb6",
            # image_id="linux_latest",
            # is_vpc=True,
            labels={"project": "piaoyun-demo", "environment": "testing"},
        )
        result = self.agent_bay.create(params)
        self.assertTrue(result.success, f"Failed to create session: {result.error_message}")
        self.assertIsNotNone(result.session)

        session = result.session
        self.test_sessions.append(session)
        print(f"  ✓ Session created: {session.session_id}")

        return session

    def test_pause_and_resume_session_success(self):
        """Test successful pause and resume operations on a session."""
        print("\n" + "="*60)
        print("TEST: Pause and Resume Session Success")
        print("="*60)

        # Create a test session
        session = self._create_test_session()

        # Verify session is initially in RUNNING state
        print(f"\nStep 1: Verifying session is initially RUNNING...")
        get_result = self.agent_bay.get_session(session.session_id)
        self.assertTrue(get_result.success, f"Failed to get session: {get_result.error_message}")
        self.assertEqual(get_result.data.status, "RUNNING")
        print(f"  ✓ Session is RUNNING: {session.session_id}")

        # Pause the session
        print(f"\nStep 2: Pausing session...")
        pause_result = self.agent_bay.pause(session)
        
        # Verify pause result
        self.assertIsInstance(pause_result, SessionPauseResult)
        self.assertTrue(pause_result.success, f"Pause failed: {pause_result.error_message}")
        print(f"  ✓ Session pause initiated successfully")
        print(f"    Request ID: {pause_result.request_id}")

        # Wait a bit for pause to complete
        print(f"\nStep 3: Waiting for session to pause...")
        time.sleep(2)

        # Check session status after pause
        get_result = self.agent_bay.get_session(session.session_id)
        self.assertTrue(get_result.success, f"Failed to get session: {get_result.error_message}")
        # Session should be PAUSED or still PAUSING
        self.assertIn(get_result.data.status, ["PAUSED", "PAUSING"])
        print(f"  ✓ Session status after pause: {get_result.data.status}")
        get_result = self.agent_bay.get_session(session.session_id)
        self.assertTrue(get_result.success, f"Failed to get session: {get_result.error_message}")
        # Session should be PAUSED or still PAUSING
        self.assertIn(get_result.data.status, ["PAUSED", "PAUSING"])
        print(f"  ✓ Session status after pause: {get_result.data.status}")

        # Resume the session (synchronous)
        print(f"\nStep 4: Resuming session...")
        resume_result = self.agent_bay.resume(session, timeout=120, poll_interval=3)
        
        # Verify resume result
        self.assertIsInstance(resume_result, SessionResumeResult)
        self.assertTrue(resume_result.success, f"Resume failed: {resume_result.error_message}")
        self.assertEqual(resume_result.status, "RUNNING")
        print(f"  ✓ Session resumed successfully")
        print(f"    Final status: {resume_result.status}")
        print(f"    Request ID: {resume_result.request_id}")

        # Verify session is RUNNING after resume
        get_result = self.agent_bay.get_session(session.session_id)
        self.assertTrue(get_result.success, f"Failed to get session: {get_result.error_message}")
        self.assertEqual(get_result.data.status, "RUNNING")
        print(f"  ✓ Session is RUNNING after resume: {session.session_id}")

    def test_resume_async_session_success(self):
        """Test successful async resume operation on a session."""
        print("\n" + "="*60)
        print("TEST: Async Resume Session Success")
        print("="*60)

        # Create a test session
        session = self._create_test_session()

        # Pause the session first
        print(f"\nStep 1: Pausing session...")
        pause_result = self.agent_bay.pause(session)
        self.assertTrue(pause_result.success, f"Pause failed: {pause_result.error_message}")
        print(f"  ✓ Session pause initiated successfully")

        # Wait for pause to complete
        print(f"\nStep 2: Waiting for session to pause...")
        time.sleep(2)

        # Verify session is PAUSED or PAUSING
        get_result = self.agent_bay.get_session(session.session_id)
        self.assertTrue(get_result.success)
        self.assertIn(get_result.data.status, ["PAUSED", "PAUSING"])
        print(f"  ✓ Session status: {get_result.data.status}")

        # Resume the session (asynchronous)
        print(f"\nStep 3: Resuming session asynchronously...")
        import asyncio
        resume_result = asyncio.run(self.agent_bay.resume_async(session))
        
        # Verify async resume result
        self.assertIsInstance(resume_result, SessionResumeResult)
        self.assertTrue(resume_result.success, f"Async resume failed: {resume_result.error_message}")
        print(f"  ✓ Session resume initiated successfully")
        print(f"    Request ID: {resume_result.request_id}")

        # Wait a bit for resume to complete
        print(f"\nStep 4: Waiting for session to resume...")
        time.sleep(2)

        # Check session status after async resume
        get_result = self.agent_bay.get_session(session.session_id)
        self.assertTrue(get_result.success, f"Failed to get session: {get_result.error_message}")
        # Session should be RUNNING or still RESUMING
        self.assertIn(get_result.data.status, ["RUNNING", "RESUMING"])
        print(f"  ✓ Session status after async resume: {get_result.data.status}")

    def test_pause_nonexistent_session(self):
        """Test pause operation on non-existent session."""
        print("\n" + "="*60)
        print("TEST: Pause Non-Existent Session")
        print("="*60)

        # Create a mock session object with invalid session ID
        from agentbay.session import Session
        invalid_session = Session(self.agent_bay, "non-existent-session-12345")

        print(f"\nAttempting to pause non-existent session: {invalid_session.session_id}")

        # This should return a failed SessionPauseResult
        pause_result = self.agent_bay.pause(invalid_session)
        
        # Verify that the result is a SessionPauseResult and indicates failure
        self.assertIsInstance(pause_result, SessionPauseResult)
        self.assertFalse(pause_result.success)
        print(f"  ✓ Returned SessionPauseResult with success=False as expected")
        print(f"    Error: {pause_result.error_message}")
        self.assertIn("session", pause_result.error_message.lower())

    def test_resume_nonexistent_session(self):
        """Test resume operation on non-existent session."""
        print("\n" + "="*60)
        print("TEST: Resume Non-Existent Session")
        print("="*60)

        # Create a mock session object with invalid session ID
        from agentbay.session import Session
        invalid_session = Session(self.agent_bay, "non-existent-session-12345")

        print(f"\nAttempting to resume non-existent session: {invalid_session.session_id}")

        # This should return a failed SessionResumeResult
        resume_result = self.agent_bay.resume(invalid_session)
        
        # Verify that the result is a SessionResumeResult and indicates failure
        self.assertIsInstance(resume_result, SessionResumeResult)
        self.assertFalse(resume_result.success)
        print(f"  ✓ Returned SessionResumeResult with success=False as expected")
        print(f"    Error: {resume_result.error_message}")
        self.assertIn("session", resume_result.error_message.lower())

    def test_resume_async_nonexistent_session(self):
        """Test async resume operation on non-existent session."""
        print("\n" + "="*60)
        print("TEST: Async Resume Non-Existent Session")
        print("="*60)

        # Create a mock session object with invalid session ID
        from agentbay.session import Session
        invalid_session = Session(self.agent_bay, "non-existent-session-12345")

        print(f"\nAttempting to async resume non-existent session: {invalid_session.session_id}")

        # This should return a failed SessionResumeResult
        import asyncio
        resume_result = asyncio.run(self.agent_bay.resume_async(invalid_session))
        
        # Verify that the result is a SessionResumeResult and indicates failure
        self.assertIsInstance(resume_result, SessionResumeResult)
        self.assertFalse(resume_result.success)
        print(f"  ✓ Returned SessionResumeResult with success=False as expected")
        print(f"    Error: {resume_result.error_message}")
        self.assertIn("session", resume_result.error_message.lower())

    def test_pause_already_paused_session(self):
        """Test pausing a session that is already paused."""
        print("\n" + "="*60)
        print("TEST: Pause Already Paused Session")
        print("="*60)

        # Create a test session
        session = self._create_test_session()

        # Pause the session
        print(f"\nStep 1: Pausing session...")
        pause_result1 = self.agent_bay.pause(session)
        self.assertTrue(pause_result1.success, f"First pause failed: {pause_result1.error_message}")
        print(f"  ✓ Session paused successfully")

        # Wait for pause to complete
        print(f"\nStep 2: Waiting for session to pause...")
        time.sleep(2)

        # Verify session is PAUSED or PAUSING
        get_result = self.agent_bay.get_session(session.session_id)
        self.assertTrue(get_result.success)
        self.assertIn(get_result.data.status, ["PAUSED", "PAUSING"])
        print(f"  ✓ Session status: {get_result.data.status}")

        # Try to pause again
        print(f"\nStep 3: Attempting to pause already paused session...")
        pause_result2 = self.agent_bay.pause(session)
        
        # Second pause may succeed or fail depending on API behavior
        # Both are acceptable for this test
        print(f"  ✓ Second pause completed")
        print(f"    Success: {pause_result2.success}")
        if pause_result2.success:
            print(f"    Request ID: {pause_result2.request_id}")
        else:
            print(f"    Error: {pause_result2.error_message}")

    def test_resume_already_running_session(self):
        """Test resuming a session that is already running."""
        print("\n" + "="*60)
        print("TEST: Resume Already Running Session")
        print("="*60)

        # Create a test session (initially running)
        session = self._create_test_session()

        # Verify session is RUNNING
        get_result = self.agent_bay.get_session(session.session_id)
        self.assertTrue(get_result.success)
        self.assertEqual(get_result.data.status, "RUNNING")
        print(f"  ✓ Session is RUNNING: {session.session_id}")

        # Try to resume the already running session
        print(f"\nAttempting to resume already running session...")
        resume_result = self.agent_bay.resume(session, timeout=30, poll_interval=2)
        
        # Resume of already running session may succeed or have specific behavior
        # Just verify it doesn't crash and returns a proper result object
        self.assertIsInstance(resume_result, SessionResumeResult)
        print(f"  ✓ Resume completed")
        print(f"    Success: {resume_result.success}")
        if resume_result.success:
            print(f"    Status: {resume_result.status}")
            print(f"    Request ID: {resume_result.request_id}")
        else:
            print(f"    Error: {resume_result.error_message}")

    def test_pause_resume_with_custom_parameters(self):
        """Test pause and resume operations with custom timeout and poll interval."""
        print("\n" + "="*60)
        print("TEST: Pause and Resume with Custom Parameters")
        print("="*60)

        # Create a test session
        session = self._create_test_session()

        # Pause with custom parameters (using agent_bay method)
        print(f"\nStep 1: Pausing session with custom parameters...")
        pause_result = self.agent_bay.pause(session, timeout=300, poll_interval=3.0)
        
        self.assertIsInstance(pause_result, SessionPauseResult)
        self.assertTrue(pause_result.success, f"Pause with custom params failed: {pause_result.error_message}")
        print(f"  ✓ Session pause with custom parameters successful")

        # Wait for pause to complete
        print(f"\nStep 2: Waiting for session to pause...")
        time.sleep(2)

        # Verify session is PAUSED or PAUSING
        get_result = self.agent_bay.get_session(session.session_id)
        self.assertTrue(get_result.success)
        self.assertIn(get_result.data.status, ["PAUSED", "PAUSING"])
        print(f"  ✓ Session status: {get_result.data.status}")

        # Resume with custom parameters
        print(f"\nStep 3: Resuming session with custom parameters...")
        resume_result = self.agent_bay.resume(session, timeout=300, poll_interval=3.0)
        
        self.assertIsInstance(resume_result, SessionResumeResult)
        self.assertTrue(resume_result.success, f"Resume with custom params failed: {resume_result.error_message}")
        print(f"  ✓ Session resume with custom parameters successful")

        # Verify session is RUNNING after resume
        get_result = self.agent_bay.get_session(session.session_id)
        self.assertTrue(get_result.success)
        self.assertEqual(get_result.data.status, "RUNNING")
        print(f"  ✓ Session is RUNNING after resume with custom parameters")


class TestSessionPauseResumeEdgeCases(unittest.TestCase):
    """Edge case tests for Session pause and resume operations."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        # Load environment variables from .env file
        load_dotenv()
        
        api_key = get_test_api_key()
        if not api_key:
            raise unittest.SkipTest("AGENTBAY_API_KEY environment variable not set")

        endpoint = get_test_endpoint()
        if endpoint:
            config = Config(endpoint=endpoint, timeout_ms=60000)
            cls.agent_bay = AgentBay(api_key=api_key, cfg=config)
        else:
            cls.agent_bay = AgentBay(api_key=api_key)

    def setUp(self):
        """Set up test fixtures for each test method."""
        self.test_sessions = []  # Track sessions for cleanup in each test

    def tearDown(self):
        """Clean up test sessions after each test method."""
        print("\nCleaning up test sessions for this test...")
        for session in self.test_sessions:
            try:
                # Delete session
                result = self.agent_bay.delete(session)
                if result.success:
                    print(f"  ✓ Deleted session: {session.session_id}")
                else:
                    print(f"  ✗ Failed to delete session: {session.session_id}")
            except Exception as e:
                print(f"  ✗ Error deleting session {session.session_id}: {e}")
        # Clear the list for next test
        self.test_sessions = []

    def _create_test_session(self):
        """Helper method to create a test session."""
        session_name = f"test-pause-resume-edge-{uuid4().hex[:8]}"
        print(f"\nCreating test session: {session_name}")

        # Create session
        params = CreateSessionParams(
            labels={"project": "piaoyun-demo", "environment": "testing"},
        )
        result = self.agent_bay.create(params)
        self.assertTrue(result.success, f"Failed to create session: {result.error_message}")
        self.assertIsNotNone(result.session)

        session = result.session
        self.test_sessions.append(session)
        print(f"  ✓ Session created: {session.session_id}")

        return session

    def test_pause_with_short_timeout(self):
        """Test pause with a short timeout parameter."""
        print("\n" + "="*60)
        print("TEST: Pause with Short Timeout")
        print("="*60)

        # Create session
        session = self._create_test_session()

        # Pause with short timeout (using agent_bay method)
        print(f"\nPausing session with short timeout...")
        pause_result = self.agent_bay.pause(session, timeout=10, poll_interval=1)
        
        # Pause should succeed regardless of timeout parameter
        self.assertIsInstance(pause_result, SessionPauseResult)
        self.assertTrue(pause_result.success, f"Pause with short timeout failed: {pause_result.error_message}")
        print(f"  ✓ Pause with short timeout successful")


if __name__ == "__main__":
    # Print environment info
    print("\n" + "="*60)
    print("ENVIRONMENT CONFIGURATION")
    print("="*60)
    load_dotenv()
    print(f"API Key: {'✓ Set' if get_test_api_key() else '✗ Not Set'}")
    print(f"Endpoint: {get_test_endpoint() or 'Using default'}")
    print("="*60 + "\n")

    unittest.main(verbosity=2)