import unittest
import os
import time
from agentbay import AgentBay
from agentbay.command import Command
from agentbay.session_params import CreateSessionParams
from agentbay.exceptions import CommandError

class TestCommandIntegration(unittest.TestCase):
    def setUp(self):
        """
        Set up the test environment by creating a session and initializing Command.
        """
        time.sleep(3)  # Ensure a delay to avoid session creation conflicts
        api_key = os.getenv("AGENTBAY_API_KEY")
        if not api_key:
            api_key = "akm-xxx"  # Replace with your actual API key for testing
            print("Warning: Using default API key. Set AGENTBAY_API_KEY environment variable for production use.")
        self.agent_bay = AgentBay(api_key=api_key)
        params = CreateSessionParams(
            image_id="code_latest",
        )
        self.session = self.agent_bay.create(params)
        self.command = Command(self.session)

    def tearDown(self):
        """
        Clean up resources after each test.
        """
        print("Cleaning up: Deleting the session...")
        try:
            self.agent_bay.delete(self.session)
        except Exception as e:
            print(f"Warning: Error deleting session: {e}")

    def test_execute_command_success(self):
        """
        Test executing a shell command successfully.
        """
        command = "echo 'Hello, AgentBay!'"
        response = self.command.execute_command(command)
        print(f"Command execution result: {response}")
        self.assertEqual(response.strip(), "Hello, AgentBay!")

    def test_execute_command_timeout(self):
        """
        Test executing a shell command with a timeout.
        """
        command = "sleep 5"
        timeout_ms = 1000  # 1 second timeout
        with self.assertRaises(CommandError) as context:
            self.command.execute_command(command, timeout_ms)
        self.assertIn("Failed to execute command", str(context.exception))

    def test_run_code_python_success(self):
        """
        Test running Python code successfully.
        """
        code = """
print("Hello, world!")
x = 1 + 1
print(x)
"""
        response = self.command.run_code(code, "python")
        print(f"Run code result: {response}")
        self.assertEqual(response.strip(), "Hello, world!\n2")

    def test_run_code_javascript_success(self):
        """
        Test running JavaScript code successfully.
        """
        code = """
console.log("Hello, world!");
let x = 1 + 1;
console.log(x);
"""
        response = self.command.run_code(code, "javascript")
        print(f"Run code result: {response}")
        self.assertEqual(response.strip(), "Hello, world!\n2")

    def test_run_code_unsupported_language(self):
        """
        Test running code with an unsupported language.
        """
        code = "print('Hello, world!')"
        language = "ruby"  # Unsupported language
        with self.assertRaises(CommandError) as context:
            self.command.run_code(code, language)
        self.assertIn("Unsupported language", str(context.exception))


if __name__ == "__main__":
    unittest.main()
