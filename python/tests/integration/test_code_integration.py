import os
import unittest

from agentbay import AgentBay


class TestCodeIntegration(unittest.TestCase):
    """Integration tests for Code module."""

    def setUp(self):
        """Set up test fixtures."""
        self.api_key = os.getenv("AGENTBAY_API_KEY")
        if not self.api_key:
            self.skipTest("AGENTBAY_API_KEY environment variable not set")

        self.agent_bay = AgentBay(api_key=self.api_key)
        # Use code_latest image for code execution tests
        session_result = self.agent_bay.create_session(
            resource_type="linux", image_id="code_latest"
        )
        self.session = session_result.session
        self.code = self.session.code

    def tearDown(self):
        """Clean up test fixtures."""
        if hasattr(self, "session"):
            self.session.delete()

    def test_run_code_python_success(self):
        """Test successful Python code execution."""
        code = '''
print("Hello, world!")
x = 1 + 1
print(x)
'''
        result = self.code.run_code(code, "python")

        print(f"Python code execution result: {result}")

        # Should have success, result, and request_id
        self.assertTrue(result.success)
        self.assertIsNotNone(result.result)
        self.assertIsNotNone(result.request_id)
        self.assertIn("Hello, world!", result.result)
        self.assertIn("2", result.result)

    def test_run_code_javascript_success(self):
        """Test successful JavaScript code execution."""
        code = '''
console.log("Hello, world!");
const x = 1 + 1;
console.log(x);
'''
        result = self.code.run_code(code, "javascript")

        print(f"JavaScript code execution result: {result}")

        # Should have success, result, and request_id
        self.assertTrue(result.success)
        self.assertIsNotNone(result.result)
        self.assertIsNotNone(result.request_id)
        self.assertIn("Hello, world!", result.result)
        self.assertIn("2", result.result)

    def test_run_code_unsupported_language(self):
        """Test code execution with unsupported language."""
        code = "print('Hello, world!')"
        language = "ruby"

        result = self.code.run_code(code, language)

        # Should return failure for unsupported language
        self.assertFalse(result.success)
        self.assertIn("Unsupported language", result.error_message)


if __name__ == "__main__":
    unittest.main() 