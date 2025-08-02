import os
import unittest
import time

from agentbay import AgentBay
from agentbay.session_params import CreateSessionParams

class TestCommandExecution(unittest.TestCase):
    """
    Command Execution Integration Tests

    This test suite covers command execution functionality including:
    1. ExecuteCommand Functionality Verification
    2. RunCode Functionality Verification
    3. Shell command execution and file operations
    4. Code execution in different languages
    5. Error handling and edge cases
    """

    @classmethod
    def setUpClass(cls):
        """Set up test environment before all tests."""
        # Get API key from environment
        cls.api_key = os.getenv("AGENTBAY_API_KEY")
        if not cls.api_key:
            raise unittest.SkipTest("AGENTBAY_API_KEY environment variable not set")

        # Initialize AgentBay client
        cls.agent_bay = AgentBay(cls.api_key)

    @classmethod
    def tearDownClass(cls):
        """Clean up test environment after all tests."""
        pass

    def setUp(self):
        """Set up before each test."""
        self.sessions = []

    def tearDown(self):
        """Clean up after each test."""
        # Clean up sessions
        for session in self.sessions:
            if session:
                try:
                    self.agent_bay.delete(session)
                except Exception as e:
                    print(f"Error deleting session: {e}")
        self.sessions.clear()

    def test_3_1_execute_command_functionality_verification(self):
        """3.1 ExecuteCommand Functionality Verification - should execute shell commands and verify file operations"""
        # Step 1: Environment preparation
        self.assertIsNotNone(self.agent_bay)

        # Step 2: Session creation
        session_params = CreateSessionParams()
        session_params.image_id = 'linux_latest'

        session_result = self.agent_bay.create(session_params)
        self.assertTrue(session_result.success)
        session = session_result.session
        self.sessions.append(session)

        # Step 3: Command and file system instance retrieval
        command = session.command
        file_system = session.file_system
        self.assertIsNotNone(command)
        self.assertIsNotNone(file_system)

        # Step 4: File creation command
        create_command = 'echo "Test content from shell command" > /tmp/shell_test.txt'
        create_result = command.execute_command(create_command)
        self.assertTrue(create_result.success)

        # Step 5: File content verification
        file_content = file_system.read_file('/tmp/shell_test.txt')
        self.assertEqual(file_content.content.strip(), 'Test content from shell command')

        # Step 6: File deletion command
        delete_command = 'rm /tmp/shell_test.txt'
        delete_result = command.execute_command(delete_command)
        self.assertTrue(delete_result.success)

        # Step 7: Deletion verification
        search_results = file_system.search_files('/tmp', 'shell_test.txt')
        deleted_file = next((file for file in search_results.matches if 'shell_test.txt' in file), None)
        self.assertIsNone(deleted_file)

        # Step 8: Complex command test
        complex_command = 'mkdir -p /tmp/test_dir && echo "complex command" > /tmp/test_dir/complex.txt && ls -la /tmp/test_dir'
        complex_result = command.execute_command(complex_command)
        self.assertTrue(complex_result.success)
        self.assertIn('complex.txt', complex_result.output)

        # Verify complex command results
        complex_content = file_system.read_file('/tmp/test_dir/complex.txt')
        self.assertEqual(complex_content.content.strip(), 'complex command')

    def test_3_1_command_error_handling(self):
        """3.1 Command Error Handling - should handle command errors and edge cases"""
        # Step 1: Session creation
        session_params = CreateSessionParams()
        session_params.image_id = 'linux_latest'

        session_result = self.agent_bay.create(session_params)
        self.assertTrue(session_result.success)
        session = session_result.session
        self.sessions.append(session)

        command = session.command

        # Test invalid command
        invalid_result = command.execute_command('invalid_command_12345')
        self.assertFalse(invalid_result.success)
        self.assertIsNotNone(invalid_result.error_message)

        # Test command with permission issues (trying to write to protected directory)
        permission_result = command.execute_command('echo "test" > /root/protected.txt')
        # This might succeed or fail depending on the environment, but should not crash
        self.assertIsInstance(permission_result.success, bool)

        # Test long-running command with timeout considerations
        time_command = 'echo "completed"'
        time_result = command.execute_command(time_command)
        print(f'Command output: {time_result}')
        self.assertTrue(time_result.success)
        self.assertIn('completed', time_result.output)

    def test_3_2_run_code_functionality_verification(self):
        """3.2 RunCode Functionality Verification - should execute code concurrently in different sessions"""
        # Step 1: Environment preparation
        self.assertIsNotNone(self.agent_bay)

        # Step 2: Create two independent sessions
        session_params1 = CreateSessionParams()
        session_params1.image_id = 'code_latest'

        session_params2 = CreateSessionParams()
        session_params2.image_id = 'code_latest'

        session_result1 = self.agent_bay.create(session_params1)
        session_result2 = self.agent_bay.create(session_params2)

        self.assertTrue(session_result1.success)
        self.assertTrue(session_result2.success)

        session1 = session_result1.session
        session2 = session_result2.session
        self.sessions.extend([session1, session2])

        self.assertNotEqual(session1.get_session_id(), session2.get_session_id())

        # Step 3: Code executor retrieval
        code1 = session1.code
        code2 = session2.code
        self.assertIsNotNone(code1)
        self.assertIsNotNone(code2)

        # Step 4: Concurrent code execution
        python_code = '''
import time
import json
result = {"message": "Python execution successful", "timestamp": time.time()}
print(json.dumps(result))
'''.strip()

        js_code = '''
const result = {
  message: "JavaScript execution successful",
  timestamp: Date.now()
};
console.log(JSON.stringify(result));
'''.strip()

        python_result = code1.run_code(python_code, 'python')
        js_result = code2.run_code(js_code, 'javascript')

        print(f'Python Result: {python_result}')
        print(f'JavaScript Result: {js_result}')

        # Step 5: Result collection and verification
        self.assertTrue(python_result.success)
        self.assertTrue(js_result.success)

        # Verify Python output contains expected JSON
        self.assertIn('Python execution successful', python_result.result)
        self.assertIn('timestamp', python_result.result)

        # Verify JavaScript output contains expected JSON
        self.assertIn('JavaScript execution successful', js_result.result)
        self.assertIn('timestamp', js_result.result)

        # Step 6: Execution verification
        # Both should complete successfully due to concurrent execution
        self.assertIsNotNone(python_result.request_id)
        self.assertIsNotNone(js_result.request_id)

    def test_3_2_complex_code_with_file_operations(self):
        """3.2 Complex Code with File Operations - should execute complex code with file operations"""
        # Step 1: Session creation
        session_params1 = CreateSessionParams()
        session_params1.image_id = 'code_latest'

        session_params2 = CreateSessionParams()
        session_params2.image_id = 'code_latest'

        session_result1 = self.agent_bay.create(session_params1)
        session_result2 = self.agent_bay.create(session_params2)

        self.assertTrue(session_result1.success)
        self.assertTrue(session_result2.success)

        session1 = session_result1.session
        session2 = session_result2.session
        self.sessions.extend([session1, session2])

        code1 = session1.code
        code2 = session2.code

        # Step 7: Complex code test with file operations
        python_file_code = '''
import os
import json

# Create a test file
with open('/tmp/python_test.txt', 'w') as f:
    f.write('Python file operation test')

# Read the file
with open('/tmp/python_test.txt', 'r') as f:
    content = f.read()

result = {"operation": "file_write_read", "content": content, "file_exists": os.path.exists('/tmp/python_test.txt')}
print(json.dumps(result))
'''.strip()

        js_file_code = '''
const fs = require('fs');

// Create a test file
fs.writeFileSync('/tmp/js_test.txt', 'JavaScript file operation test');

// Read the file
const content = fs.readFileSync('/tmp/js_test.txt', 'utf8');

const result = {
  operation: "file_write_read",
  content: content,
  file_exists: fs.existsSync('/tmp/js_test.txt')
};
console.log(JSON.stringify(result));
'''.strip()

        python_file_result = code1.run_code(python_file_code, 'python')
        js_file_result = code2.run_code(js_file_code, 'javascript')

        self.assertTrue(python_file_result.success)
        self.assertTrue(js_file_result.success)

        self.assertIn('Python file operation test', python_file_result.result)
        self.assertIn('JavaScript file operation test', js_file_result.result)

    def test_3_2_code_execution_error_handling(self):
        """3.2 Code Execution Error Handling - should handle code execution errors gracefully"""
        # Step 1: Session creation
        session_params = CreateSessionParams()
        session_params.image_id = 'code_latest'

        session_result = self.agent_bay.create(session_params)
        self.assertTrue(session_result.success)
        session = session_result.session
        self.sessions.append(session)

        code = session.code

        # Test Python code with syntax error
        bad_python_code = '''
print("Hello"
# Missing closing parenthesis
'''.strip()

        bad_result = code.run_code(bad_python_code, 'python')
        self.assertFalse(bad_result.success)
        self.assertIsNotNone(bad_result.error_message)

        # Test code with runtime error
        runtime_error_code = '''
undefined_variable = nonexistent_variable + 1
print(undefined_variable)
'''.strip()

        runtime_result = code.run_code(runtime_error_code, 'python')
        self.assertFalse(runtime_result.success)
        self.assertIn('NameError', runtime_result.error_message)

if __name__ == "__main__":
    unittest.main()
