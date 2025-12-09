import { Session } from "../session";
import {
  CommandResult,
} from "../types/api-response";


/**
 * Handles command execution operations in the AgentBay cloud environment.
 */
export class Command {
  private session: Session;

  /**
   * Initialize a Command object.
   *
   * @param session - The Session instance that this Command belongs to.
   */
  constructor(session: Session) {
    this.session = session;
  }

  /**
   * Sanitizes error messages to remove sensitive information like API keys.
   *
   * @param error - The error to sanitize
   * @returns The sanitized error
   */
  private sanitizeError(error: any): any {
    if (!error) {
      return error;
    }

    const errorString = String(error);
    return errorString.replace(/Bearer\s+[^\s]+/g, "Bearer [REDACTED]");
  }

  /**
   * Execute a shell command with optional working directory and environment variables.
   *
   * Executes a shell command in the session environment with configurable timeout,
   * working directory, and environment variables. The command runs with session
   * user permissions in a Linux shell environment.
   *
   * @param command - The shell command to execute
   * @param timeoutMs - Timeout in milliseconds (default: 1000ms/1s). Maximum allowed
   *                    timeout is 50000ms (50s). If a larger value is provided,
   *                    it will be automatically limited to 50000ms
   * @param cwd - The working directory for command execution. If not specified,
   *              the command runs in the default session directory
   * @param envs - Environment variables as a dictionary of key-value pairs.
   *              These variables are set for the command execution only
   *
   * @returns Promise resolving to CommandResult containing:
   *          - success: Whether the command executed successfully (exitCode === 0)
   *          - output: Command output for backward compatibility (stdout + stderr)
   *          - exitCode: The exit code of the command execution (0 for success)
   *          - stdout: Standard output from the command execution
   *          - stderr: Standard error from the command execution
   *          - traceId: Trace ID for error tracking (only present when exitCode !== 0)
   *          - requestId: Unique identifier for this API request
   *          - errorMessage: Error description if execution failed
   *
   * @example
   * ```typescript
   * const agentBay = new AgentBay({ apiKey: 'your_api_key' });
   * const result = await agentBay.create();
   * if (result.success) {
   *   const cmdResult = await result.session.command.executeCommand('echo "Hello"', 5000);
   *   console.log('Command output:', cmdResult.output);
   *   console.log('Exit code:', cmdResult.exitCode);
   *   console.log('Stdout:', cmdResult.stdout);
   *   await result.session.delete();
   * }
   * ```
   *
   * @example
   * ```typescript
   * const agentBay = new AgentBay({ apiKey: 'your_api_key' });
   * const result = await agentBay.create();
   * if (result.success) {
   *   const cmdResult = await result.session.command.executeCommand(
   *     'pwd',
   *     5000,
   *     '/tmp',
   *     { TEST_VAR: 'test_value' }
   *   );
   *   console.log('Working directory:', cmdResult.stdout);
   *   await result.session.delete();
   * }
   * ```
   */
  async executeCommand(
    command: string,
    timeoutMs = 1000,
    cwd?: string,
    envs?: Record<string, string>
  ): Promise<CommandResult> {
    try {
      // Limit timeout to maximum 50s (50000ms) as per SDK constraints
      const MAX_TIMEOUT_MS = 50000;
      if (timeoutMs > MAX_TIMEOUT_MS) {
        // Log warning (in production, you might want to use a proper logger)
        // Note: Warning is silently applied to maintain compatibility
        timeoutMs = MAX_TIMEOUT_MS;
      }

      // Build request arguments
      const args: Record<string, any> = {
        command,
        timeout_ms: timeoutMs,
      };
      if (cwd !== undefined) {
        args.cwd = cwd;
      }
      if (envs !== undefined) {
        args.envs = envs;
      }

      const result = await this.session.callMcpTool("shell", args);

      if (result.success) {
        // Try to parse the new JSON format response
        try {
          // Parse JSON string from result.data
          let dataJson: any;
          if (typeof result.data === "string") {
            dataJson = JSON.parse(result.data);
          } else {
            dataJson = result.data;
          }

          // Extract fields from new format
          const stdout = dataJson.stdout || "";
          const stderr = dataJson.stderr || "";
          const errorCode = dataJson.errorCode || 0;
          const traceId = dataJson.traceId || "";

          // Determine success based on errorCode (0 means success)
          const success = errorCode === 0;

          // For backward compatibility, output should be stdout + stderr
          const output = stdout + stderr;

          return {
            requestId: result.requestId,
            success,
            output,
            exitCode: errorCode,
            stdout,
            stderr,
            traceId: traceId || undefined,
            errorMessage: result.errorMessage,
          };
        } catch (parseError) {
          // Fallback to old format if JSON parsing fails
          return {
            requestId: result.requestId,
            success: true,
            output: typeof result.data === "string" ? result.data : String(result.data),
            errorMessage: result.errorMessage,
          };
        }
      } else {
        // Try to parse error message as JSON (in case backend returns JSON in error)
        try {
          const errorData = typeof result.errorMessage === "string" 
            ? JSON.parse(result.errorMessage) 
            : result.errorMessage;
          
          if (errorData && typeof errorData === "object") {
            const stdout = errorData.stdout || "";
            const stderr = errorData.stderr || "";
            const errorCode = errorData.errorCode || 0;
            const traceId = errorData.traceId || "";
            // For backward compatibility, output should be stdout + stderr
            const output = stdout + stderr;

            return {
              requestId: result.requestId,
              success: false,
              output,
              exitCode: errorCode,
              stdout,
              stderr,
              traceId: traceId || undefined,
              errorMessage: stderr || result.errorMessage,
            };
          }
        } catch {
          // If parsing fails, use original error message
        }

        return {
          requestId: result.requestId,
          success: false,
          output: "",
          errorMessage: result.errorMessage || "Failed to execute command",
        };
      }
    } catch (error) {
      return {
        requestId: "",
        success: false,
        output: "",
        errorMessage: `Failed to execute command: ${error}`,
      };
    }
  }
}
