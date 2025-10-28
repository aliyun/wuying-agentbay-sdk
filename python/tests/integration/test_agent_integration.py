import os
import time
import unittest

from agentbay import AgentBay
from agentbay.agent import Agent
from agentbay.session_params import CreateSessionParams
from agentbay.logger import get_logger

logger = get_logger("agentbay-integration-test")


class TestAgentIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Set up the test environment by creating a session and initializing task.
        """
        time.sleep(3)  # Ensure a delay to avoid session creation conflicts
        api_key = os.getenv("AGENTBAY_API_KEY")
        if not api_key:
            api_key = "akm-xxx"  # Replace with your actual API key for testing
            print(
                "Warning: Using default API key. Set AGENTBAY_API_KEY environment variable for production use."
            )
        cls.agent_bay = AgentBay(api_key=api_key)
        params = CreateSessionParams(
            image_id="windows_latest",
        )
        session_result = cls.agent_bay.create(params)
        if not session_result.success or not session_result.session:
            raise unittest.SkipTest("Failed to create session")

        cls.session = session_result.session
        cls.agent = cls.session.agent

    @classmethod
    def tearDownClass(cls):
        """
        Clean up resources after each test.
        """
        print("Cleaning up: Deleting the session...")
        try:
            cls.agent_bay.delete(cls.session)
        except Exception as e:
            print(f"Warning: Error deleting session: {e}")

    def test_execute_task_success(self):
        """
        Test executing a flux task successfully.
        """

        task = "create a folder named 'agentbay' in C:\\Window\\Temp"
        max_try_times = os.environ.get("AGENT_TASK_TIMEOUT")
        if not max_try_times:
            max_try_times = 100
        print("🚀 task of creating folders")
        result = self.agent.execute_task(task, int(max_try_times))
        self.assertTrue(result.success)
        self.assertNotEqual(result.request_id, "")
        self.assertEqual(result.error_message, "")
        print(f"✅ result {result.task_result}")

    def test_async_execute_task_success(self):
        """
        Test executing a flux task successfully.
        """

        task = "create a folder named 'agentbay' in C:\\Window\\Temp"
        max_try_times = os.environ.get("AGENT_TASK_TIMEOUT")
        if not max_try_times:
            max_try_times = 100
        print("🚀 async task of creating folders")
        result = self.agent.async_execute_task(task)
        self.assertTrue(result.success)
        self.assertNotEqual(result.request_id, "")
        self.assertEqual(result.error_message, "")
        retry_times: int = 0
        query_result = None
        while retry_times < int(max_try_times):
            query_result = self.agent.get_task_status(result.task_id)
            self.assertTrue(result.success)
            print(
                f"⏳ Task {query_result.task_id} running 🚀: {query_result.task_action}."
            )
            if query_result.task_status == "finished":
                break
            retry_times += 1
            time.sleep(3)
        # Verify the final task status
        self.assertTrue(retry_times < int(max_try_times))
        print(f"✅ result {query_result.task_product}")


if __name__ == "__main__":
    unittest.main()
