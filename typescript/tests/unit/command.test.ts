import { Command } from '../../src/command/command';
import { Session } from '../../src/session';
import { CommandResult } from '../../src/types/api-response';

// Mock Session
class MockSession {
  public callMcpTool = jest.fn();
  public sessionId = 'mock-session-id';
}

describe('Command', () => {
  let command: Command;
  let mockSession: MockSession;

  beforeEach(() => {
    mockSession = new MockSession() as any;
    command = new Command(mockSession as any);
  });

  describe('executeCommand', () => {
    it('should execute command with default timeout', async () => {
      const mockResult = {
        requestId: 'request-123',
        success: true,
        data: 'test output',
        errorMessage: undefined,
      };
      mockSession.callMcpTool.mockResolvedValue(mockResult);

      const result = await command.executeCommand('echo test');

      expect(result.requestId).toBe('request-123');
      expect(result.success).toBe(true);
      expect(result.output).toBe('test output');
      expect(mockSession.callMcpTool).toHaveBeenCalledWith('shell', {
        command: 'echo test',
        timeout_ms: 1000,
      });
    });

    it('should execute command with custom timeout', async () => {
      const mockResult = {
        requestId: 'request-123',
        success: true,
        data: 'test output',
        errorMessage: undefined,
      };
      mockSession.callMcpTool.mockResolvedValue(mockResult);

      const result = await command.executeCommand('echo test', 5000);

      expect(result.requestId).toBe('request-123');
      expect(result.success).toBe(true);
      expect(mockSession.callMcpTool).toHaveBeenCalledWith('shell', {
        command: 'echo test',
        timeout_ms: 5000,
      });
    });

    it('should parse new JSON format response', async () => {
      const jsonData = JSON.stringify({
        stdout: 'output text',
        stderr: 'error text',
        exit_code: 0,
        traceId: '',
      });
      const mockResult = {
        requestId: 'request-123',
        success: true,
        data: jsonData,
        errorMessage: undefined,
      };
      mockSession.callMcpTool.mockResolvedValue(mockResult);

      const result = await command.executeCommand('ls -la');

      expect(result.requestId).toBe('request-123');
      expect(result.success).toBe(true);
      expect(result.exitCode).toBe(0);
      expect(result.stdout).toBe('output text');
      expect(result.stderr).toBe('error text');
      expect(result.output).toBe('output texterror text'); // output = stdout + stderr for backward compatibility
      expect(result.traceId).toBeUndefined();
    });

    it('should parse new JSON format response with error', async () => {
      const jsonData = JSON.stringify({
        stdout: '',
        stderr: 'command not found',
        exit_code: 127,
        traceId: 'trace-123',
      });
      const mockResult = {
        requestId: 'request-123',
        success: true,
        data: jsonData,
        errorMessage: undefined,
      };
      mockSession.callMcpTool.mockResolvedValue(mockResult);

      const result = await command.executeCommand('invalid_command');

      expect(result.requestId).toBe('request-123');
      expect(result.success).toBe(false);
      expect(result.exitCode).toBe(127);
      expect(result.stdout).toBe('');
      expect(result.stderr).toBe('command not found');
      expect(result.output).toBe('command not found');
      expect(result.traceId).toBe('trace-123');
    });

    it('should handle cwd parameter', async () => {
      const mockResult = {
        requestId: 'request-123',
        success: true,
        data: '/tmp',
        errorMessage: undefined,
      };
      mockSession.callMcpTool.mockResolvedValue(mockResult);

      const result = await command.executeCommand('pwd', 1000, '/tmp');

      expect(mockSession.callMcpTool).toHaveBeenCalledWith('shell', {
        command: 'pwd',
        timeout_ms: 1000,
        cwd: '/tmp',
      });
      expect(result.success).toBe(true);
    });

    it('should handle envs parameter', async () => {
      const mockResult = {
        requestId: 'request-123',
        success: true,
        data: 'test_value',
        errorMessage: undefined,
      };
      mockSession.callMcpTool.mockResolvedValue(mockResult);

      const result = await command.executeCommand(
        'echo $TEST_VAR',
        1000,
        undefined,
        { TEST_VAR: 'test_value' }
      );

      expect(mockSession.callMcpTool).toHaveBeenCalledWith('shell', {
        command: 'echo $TEST_VAR',
        timeout_ms: 1000,
        envs: { TEST_VAR: 'test_value' },
      });
      expect(result.success).toBe(true);
    });

    it('should handle cwd and envs parameters together', async () => {
      const mockResult = {
        requestId: 'request-123',
        success: true,
        data: 'test output',
        errorMessage: undefined,
      };
      mockSession.callMcpTool.mockResolvedValue(mockResult);

      const result = await command.executeCommand(
        'pwd && echo $CUSTOM_VAR',
        1000,
        '/tmp',
        { CUSTOM_VAR: 'custom_value' }
      );

      expect(mockSession.callMcpTool).toHaveBeenCalledWith('shell', {
        command: 'pwd && echo $CUSTOM_VAR',
        timeout_ms: 1000,
        cwd: '/tmp',
        envs: { CUSTOM_VAR: 'custom_value' },
      });
      expect(result.success).toBe(true);
    });

    it('should limit timeout to maximum 50s', async () => {
      const mockResult = {
        requestId: 'request-123',
        success: true,
        data: 'test output',
        errorMessage: undefined,
      };
      mockSession.callMcpTool.mockResolvedValue(mockResult);

      // Test with timeout exceeding 50s (50000ms)
      await command.executeCommand('ls -la', 60000);

      expect(mockSession.callMcpTool).toHaveBeenCalledWith('shell', {
        command: 'ls -la',
        timeout_ms: 50000, // Should be limited to 50s
      });

      // Test with timeout exactly at limit
      mockSession.callMcpTool.mockClear();
      await command.executeCommand('ls -la', 50000);
      expect(mockSession.callMcpTool).toHaveBeenCalledWith('shell', {
        command: 'ls -la',
        timeout_ms: 50000, // Should remain 50s
      });

      // Test with timeout below limit
      mockSession.callMcpTool.mockClear();
      await command.executeCommand('ls -la', 30000);
      expect(mockSession.callMcpTool).toHaveBeenCalledWith('shell', {
        command: 'ls -la',
        timeout_ms: 30000, // Should remain unchanged
      });
    });

    it('should fallback to old format if JSON parsing fails', async () => {
      const mockResult = {
        requestId: 'request-123',
        success: true,
        data: 'plain text output',
        errorMessage: undefined,
      };
      mockSession.callMcpTool.mockResolvedValue(mockResult);

      const result = await command.executeCommand('echo test');

      expect(result.requestId).toBe('request-123');
      expect(result.success).toBe(true);
      expect(result.output).toBe('plain text output');
    });

    it('should handle error response', async () => {
      const mockResult = {
        requestId: 'request-123',
        success: false,
        data: '',
        errorMessage: 'Command execution failed',
      };
      mockSession.callMcpTool.mockResolvedValue(mockResult);

      const result = await command.executeCommand('invalid_command');

      expect(result.requestId).toBe('request-123');
      expect(result.success).toBe(false);
      expect(result.output).toBe('');
      expect(result.errorMessage).toBe('Command execution failed');
    });

    it('should handle exception', async () => {
      mockSession.callMcpTool.mockRejectedValue(new Error('Network error'));

      const result = await command.executeCommand('echo test');

      expect(result.requestId).toBe('');
      expect(result.success).toBe(false);
      expect(result.output).toBe('');
      expect(result.errorMessage).toContain('Failed to execute command');
    });

    it('should throw error for invalid envs value (not string)', async () => {
      const invalidEnvs = { TEST_VAR: 123 } as any; // Force invalid type (number instead of string)
      
      await expect(
        command.executeCommand('echo test', 1000, undefined, invalidEnvs)
      ).rejects.toThrow('Invalid environment variables');
      expect(invalidEnvs).toBeDefined(); // Suppress unused variable warning
    });

    it('should throw error for invalid envs value (boolean)', async () => {
      const invalidEnvs = { DEBUG: true } as any; // Force invalid type (boolean instead of string)
      
      await expect(
        command.executeCommand('echo test', 1000, undefined, invalidEnvs)
      ).rejects.toThrow('Invalid environment variables');
    });

    it('should throw error for mixed valid and invalid envs', async () => {
      const invalidEnvs = { VALID: 'ok', INVALID: true, ANOTHER: 123 } as any;
      
      await expect(
        command.executeCommand('echo test', 1000, undefined, invalidEnvs)
      ).rejects.toThrow('Invalid environment variables');
    });

    it('should accept valid envs (all strings)', async () => {
      const mockResult = {
        requestId: 'request-123',
        success: true,
        data: 'test output',
        errorMessage: undefined,
      };
      mockSession.callMcpTool.mockResolvedValue(mockResult);

      const result = await command.executeCommand(
        'echo test',
        1000,
        undefined,
        { TEST_VAR: '123', MODE: 'production' }
      );

      expect(result.success).toBe(true);
      expect(mockSession.callMcpTool).toHaveBeenCalledWith('shell', {
        command: 'echo test',
        timeout_ms: 1000,
        envs: { TEST_VAR: '123', MODE: 'production' },
      });
    });
  });
});

