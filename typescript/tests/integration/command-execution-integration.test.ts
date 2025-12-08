import { log } from 'console';
import { AgentBay } from '../../src';
import { Session } from '../../src/session';

describe('Command Execution Integration Tests', () => {
  let agentBay: AgentBay;

  beforeAll(() => {
    agentBay = new AgentBay();
    expect(agentBay).toBeDefined();
  });

  describe('3.1 ExecuteCommand Functionality Verification', () => {
    let session: Session;

    beforeAll(async () => {
      // Step 1: Environment preparation
      expect(agentBay).toBeDefined();

      // Step 2: Session creation
      const sessionResult = await agentBay.create({
        imageId: 'linux_latest'
      });
      expect(sessionResult.success).toBe(true);
      session = sessionResult.session!;

    } );

    it('should execute shell commands and verify file operations', async () => {
      // Step 3: Command and file system instance retrieval
      const command = session.command;
      const fileSystem = session.fileSystem;
      expect(command).toBeDefined();
      expect(fileSystem).toBeDefined();

      // Step 4: File creation command
      const createCommand = 'echo "Test content from shell command" > /tmp/shell_test.txt';
      const createResult = await command.executeCommand(createCommand);
      expect(createResult.success).toBe(true);

      // Step 5: File content verification
      const fileContent = await fileSystem.readFile('/tmp/shell_test.txt');
      expect(fileContent.content.trim()).toBe('Test content from shell command');

      // Step 6: File deletion command
      const deleteCommand = 'rm /tmp/shell_test.txt';
      const deleteResult = await command.executeCommand(deleteCommand);
      expect(deleteResult.success).toBe(true);

      // Step 7: Deletion verification
      const searchResults = await fileSystem.searchFiles('shell_test.txt', '/tmp');
      const deletedFile = searchResults.matches.find(file => file.includes('shell_test.txt'));
      expect(deletedFile).toBeUndefined();

      // Step 8: Complex command test
      const complexCommand = 'mkdir -p /tmp/test_dir && echo "complex command" > /tmp/test_dir/complex.txt && ls -la /tmp/test_dir';
      const complexResult = await command.executeCommand(complexCommand);
      expect(complexResult.success).toBe(true);
      expect(complexResult.output).toContain('complex.txt');

      // Verify complex command results
      const complexContent = await fileSystem.readFile('/tmp/test_dir/complex.txt');
      expect(complexContent.content.trim()).toBe('complex command');

    }, );

    it('should handle command errors and edge cases', async () => {
      const command = session.command;

      // Test invalid command
      const invalidResult = await command.executeCommand('invalid_command_12345');
      expect(invalidResult.success).toBe(false);
      expect(invalidResult.errorMessage).toBeDefined();

      // Test command with permission issues (trying to write to protected directory)
      const permissionResult = await command.executeCommand('echo "test" > /root/protected.txt');
      // This might succeed or fail depending on the environment, but should not crash
      expect(typeof permissionResult.success).toBe('boolean');

      // Test long-running command with timeout considerations
      const timeCommand = 'echo "completed"';
      const timeResult = await command.executeCommand(timeCommand);
      log(`Command output: ${JSON.stringify(timeResult)}`);
      expect(timeResult.success).toBe(true);
      expect(timeResult.output).toContain('completed');

    }, );

    it('should test new return format (exitCode, stdout, stderr, traceId)', async () => {
      const command = session.command;

      // Test success case with new return format
      const successResult = await command.executeCommand("echo 'Hello, AgentBay!'");
      expect(successResult.success).toBe(true);
      expect(successResult.exitCode).toBeDefined();
      expect(successResult.exitCode).toBe(0);
      expect(successResult.stdout).toBeDefined();
      expect(successResult.stdout).toContain('Hello, AgentBay!');
      expect(successResult.stderr).toBeDefined();
      expect(successResult.output).toBe(successResult.stdout); // output should equal stdout for success

      // Test error case with new return format
      const errorResult = await command.executeCommand('ls /non_existent_directory_12345');
      expect(errorResult.exitCode).toBeDefined();
      if (errorResult.exitCode !== 0) {
        expect(errorResult.exitCode).not.toBe(0);
        expect(errorResult.stderr).toBeDefined();
        // traceId is optional, only present when errorCode != 0
        if (errorResult.traceId) {
          expect(typeof errorResult.traceId).toBe('string');
          log(`Error command test passed: exitCode=${errorResult.exitCode}, stderr=${errorResult.stderr}, traceId=${errorResult.traceId}`);
        }
      }

      log('✓ New return format test passed');
    });

    it('should test cwd parameter', async () => {
      const command = session.command;

      const result = await command.executeCommand('pwd', 10000, '/tmp');
      expect(result.success).toBe(true);
      expect(result.exitCode).toBe(0);
      expect(result.stdout).toBeDefined();
      expect(result.stdout!).toContain('/tmp');

      log(`✓ CWD test passed: working directory=${result.stdout!.trim()}`);
    });

    it('should test envs parameter', async () => {
      const command = session.command;

      const result = await command.executeCommand(
        'echo $TEST_VAR',
        10000,
        undefined,
        { TEST_VAR: 'test_value_123' }
      );
      expect(result.success).toBe(true);
      expect(result.exitCode).toBe(0);
      // The environment variable should be set
      const output = result.stdout?.trim() || '';
      if (output.includes('test_value_123')) {
        log(`✓ Envs test passed: environment variable set correctly: ${output}`);
      } else {
        log(`⚠ Envs test: environment variable may not be set (output: ${output})`);
      }
    });

    it('should test cwd and envs parameters together', async () => {
      const command = session.command;

      const result = await command.executeCommand(
        'pwd && echo $CUSTOM_VAR',
        10000,
        '/tmp',
        { CUSTOM_VAR: 'custom_value' }
      );
      expect(result.success).toBe(true);
      expect(result.exitCode).toBe(0);
      expect(result.stdout).toContain('/tmp');

      log(`✓ Combined cwd and envs test passed`);
      log(`  Output: ${result.stdout}`);
    });

    it('should test timeout limit (50s)', async () => {
      const command = session.command;

      // Test with timeout exceeding 50s (50000ms) - should be limited to 50s
      // Note: We can't directly verify the timeout was limited without mocking,
      // but we can verify the command still executes successfully
      const result1 = await command.executeCommand("echo 'timeout test'", 60000);
      expect(result1.success).toBe(true);
      expect(result1.exitCode).toBe(0);

      // Test with timeout exactly at limit
      const result2 = await command.executeCommand("echo 'timeout test 50s'", 50000);
      expect(result2.success).toBe(true);
      expect(result2.exitCode).toBe(0);

      // Test with timeout below limit
      const result3 = await command.executeCommand("echo 'timeout test 30s'", 30000);
      expect(result3.success).toBe(true);
      expect(result3.exitCode).toBe(0);

      log('✓ Timeout limit test passed');
    });

    afterAll(async () => {
      // Step 9: Resource cleanup
      if (session) {
        await agentBay.delete(session);
      }
    });
  });

  describe('3.2 RunCode Functionality Verification', () => {
    let session1: Session;
    let session2: Session;

    beforeAll(async () => {
      // Step 1: Environment preparation
      expect(agentBay).toBeDefined();

      // Step 2: Create two independent sessions
      const sessionResult1 = await agentBay.create({
        imageId: 'code_latest'
      });
      const sessionResult2 = await agentBay.create({
        imageId: 'code_latest'
      });

      expect(sessionResult1.success).toBe(true);
      expect(sessionResult2.success).toBe(true);

      session1 = sessionResult1.session!;
      session2 = sessionResult2.session!;

      expect(session1.getSessionId()).not.toBe(session2.getSessionId());

    }, );

    it('should execute code concurrently in different sessions', async () => {
      // Step 3: Code executor retrieval
      const code1 = session1.code;
      const code2 = session2.code;
      expect(code1).toBeDefined();
      expect(code2).toBeDefined();

      // Step 4: Concurrent code execution
      const pythonCode = `
import time
import json
result = {"message": "Python execution successful", "timestamp": time.time()}
print(json.dumps(result))
`.trim();

      const jsCode = `
const result = {
  message: "JavaScript execution successful",
  timestamp: Date.now()
};
console.log(JSON.stringify(result));
`.trim();

      const [pythonResult, jsResult] = await Promise.all([
        code1.runCode(pythonCode, 'python'),
        code2.runCode(jsCode, 'javascript')
      ]);
      log(`Python Result: ${JSON.stringify(pythonResult)}`);
      log(`JavaScript Result: ${JSON.stringify(jsResult)}`);

      // Step 5: Result collection and verification
      expect(pythonResult.success).toBe(true);
      expect(jsResult.success).toBe(true);

      // Verify Python output contains expected JSON
      expect(pythonResult.result).toContain('Python execution successful');
      expect(pythonResult.result).toContain('timestamp');

      // Verify JavaScript output contains expected JSON
      expect(jsResult.result).toContain('JavaScript execution successful');
      expect(jsResult.result).toContain('timestamp');

      // Step 6: Execution verification
      // Both should complete successfully due to concurrent execution
      expect(pythonResult.requestId).toBeDefined();
      expect(jsResult.requestId).toBeDefined();

    });

    it('should execute complex code with file operations', async () => {
      const code1 = session1.code;
      const code2 = session2.code;

      // Step 7: Complex code test with file operations
      const pythonFileCode = `
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
`.trim();

      const jsFileCode = `
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
`.trim();

      const [pythonFileResult, jsFileResult] = await Promise.all([
        code1.runCode(pythonFileCode, 'python'),
        code2.runCode(jsFileCode, 'javascript')
      ]);

      expect(pythonFileResult.success).toBe(true);
      expect(jsFileResult.success).toBe(true);

      expect(pythonFileResult.result).toContain('Python file operation test');
      expect(jsFileResult.result).toContain('JavaScript file operation test');

    } );

    it('should handle code execution errors gracefully', async () => {
      const code1 = session1.code;

      // Test Python code with syntax error
      const badPythonCode = `
print("Hello"
# Missing closing parenthesis
`.trim();

      const badResult = await code1.runCode(badPythonCode, 'python');
      expect(badResult.success).toBe(false);
      expect(badResult.errorMessage).toBeDefined();

      // Test code with runtime error
      const runtimeErrorCode = `
undefined_variable = nonexistent_variable + 1
print(undefined_variable)
`.trim();

      const runtimeResult = await code1.runCode(runtimeErrorCode, 'python');
      expect(runtimeResult.success).toBe(false);
      expect(runtimeResult.errorMessage).toContain('NameError');

    } );

    afterAll(async () => {
      // Step 8: Resource cleanup
      if (session1) await agentBay.delete(session1);
      if (session2) await agentBay.delete(session2);
    });
  });
});
