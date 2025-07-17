import os
import time
import unittest

from agentbay import AgentBay
from agentbay.command import Command
from agentbay.session_params import CreateSessionParams


class TestCommandIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Set up the test environment by creating a session and initializing Command.
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
            image_id="code_latest",
        )
        session_result = cls.agent_bay.create(params)
        if not session_result.success or not session_result.session:
            raise unittest.SkipTest("Failed to create session")

        cls.session = session_result.session
        cls.command = Command(cls.session)

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

    def test_execute_command_success(self):
        """
        Test executing a shell command successfully.
        """
        command = "echo 'Hello, AgentBay!'"
        result = self.command.execute_command(command)
        print(f"Command execution result: {result.output}")
        self.assertTrue(result.success)
        self.assertEqual(result.output.strip(), "Hello, AgentBay!")
        self.assertNotEqual(result.request_id, "")
        self.assertEqual(result.error_message, "")

    def test_execute_command_with_timeout(self):
        """
        Test executing a shell command with a timeout.
        """
        command = "sleep 5"
        timeout_ms = 1000  # 1 second timeout
        result = self.command.execute_command(command, timeout_ms)
        print(f"Command execution result with timeout: {result}")
        self.assertFalse(result.success)
        self.assertNotEqual(result.request_id, "")
        self.assertNotEqual(result.error_message, "")
        self.assertEqual(result.output, "")

    def test_run_code_python_success(self):
        """
        Test running Python code successfully.
        """
        code = """
print("Hello, world!")
x = 1 + 1
print(x)
"""
        result = self.command.run_code(code, "python")
        print(f"Run code result: {result.result}")
        self.assertTrue(result.success)
        self.assertIn("Hello, world!", result.result)
        self.assertIn("2", result.result)
        self.assertNotEqual(result.request_id, "")
        self.assertEqual(result.error_message, "")

    def test_run_code_javascript_success(self):
        """
        Test running JavaScript code successfully.
        """
        code = """
console.log("Hello, world!");
let x = 1 + 1;
console.log(x);
"""
        result = self.command.run_code(code, "javascript")
        print(f"Run code result: {result.result}")
        self.assertTrue(result.success)
        self.assertIn("Hello, world!", result.result)
        self.assertIn("2", result.result)
        self.assertNotEqual(result.request_id, "")
        self.assertEqual(result.error_message, "")

    def test_run_code_unsupported_language(self):
        """
        Test running code with an unsupported language.
        """
        code = "print('Hello, world!')"
        language = "ruby"  # Unsupported language
        result = self.command.run_code(code, language)
        print(f"Unsupported language result: {result}")
        self.assertFalse(result.success)
        self.assertEqual(result.request_id, "")
        self.assertIn("Unsupported language", result.error_message)
        self.assertEqual(result.result, "")


if __name__ == "__main__":
    unittest.main()
