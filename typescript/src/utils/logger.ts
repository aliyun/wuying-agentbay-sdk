/**
 * Utility functions for structured logging with multiple levels, API tracking,
 * sensitive data masking, and RequestID management.
 */

import * as fs from 'fs';
import * as path from 'path';

/**
 * Log level type
 */
export type LogLevel = 'DEBUG' | 'INFO' | 'WARN' | 'ERROR';

/**
 * Logger configuration options
 *
 * @example
 * ```typescript
 * import { AgentBay, setupLogger } from 'wuying-agentbay-sdk';
 *
 * const agentBay = new AgentBay({ apiKey: 'your_api_key' });
 *
 * async function demonstrateLogging() {
 *     try {
 *         // Configure logging with file output
 *         setupLogger({
 *             level: 'DEBUG',
 *             logFile: '/var/log/agentbay.log',
 *             maxFileSize: '100 MB',
 *             enableConsole: true
 *         });
 *
 *         // Create a session - logs will be written to both console and file
 *         const result = await agentBay.create();
 *         if (result.success) {
 *             const session = result.session;
 *             console.log(`Session created: ${session.sessionId}`);
 *             await session.delete();
 *         }
 *     } catch (error) {
 *         console.error('Error:', error);
 *     }
 * }
 *
 * demonstrateLogging().catch(console.error);
 * ```
 */
export interface LoggerConfig {
  level?: LogLevel;
  logFile?: string;
  maxFileSize?: string;
  enableConsole?: boolean;
}

/**
 * Log level numeric values for comparison
 */
const LOG_LEVEL_VALUES: Record<LogLevel, number> = {
  DEBUG: 0,
  INFO: 1,
  WARN: 2,
  ERROR: 3,
};

/**
 * RequestID storage for tracking across API calls
 */
let currentRequestId = '';

/**
 * Current log level configuration
 * Supports both LOG_LEVEL and AGENTBAY_LOG_LEVEL environment variables
 */
let currentLogLevel: LogLevel = (
  (process.env.LOG_LEVEL as LogLevel) ||
  (process.env.AGENTBAY_LOG_LEVEL as LogLevel) ||
  'INFO'
);

/**
 * File logging configuration
 */
let fileLoggingEnabled = false;
let logFilePath: string | null = null;
let logFileMaxSize = 10 * 1024 * 1024; // 10MB default
let consoleLoggingEnabled = true;

/**
 * Determine whether to use colors in output
 * Priority: DISABLE_COLORS > FORCE_COLOR > TTY > IDE > default
 */
function shouldUseColors(): boolean {
  // Priority 1: Explicit disable via DISABLE_COLORS
  if (process.env.DISABLE_COLORS === 'true') {
    return false;
  }

  // Priority 2: Explicit enable via FORCE_COLOR
  if (process.env.FORCE_COLOR !== undefined && process.env.FORCE_COLOR !== '0') {
    return true;
  }

  // Priority 3: TTY detection (terminal output)
  const isTTY = process.stdout?.isTTY || process.stderr?.isTTY;
  if (isTTY) {
    return true;
  }

  // Priority 4: IDE environment detection
  const isVSCode = process.env.TERM_PROGRAM === 'vscode';
  const isGoLand = process.env.GOLAND !== undefined;
  const isIntelliJ = process.env.IDEA_INITIAL_DIRECTORY !== undefined;
  if (isVSCode || isGoLand || isIntelliJ) {
    return true;
  }

  // Default: no colors (safe for file output, CI/CD, pipes)
  return false;
}

/**
 * ANSI color codes
 */
const ANSI_RESET = '\x1b[0m';
const ANSI_BLUE = '\x1b[34m';
const ANSI_CYAN = '\x1b[36m';
const ANSI_YELLOW = '\x1b[33m';
const ANSI_RED = '\x1b[31m';
const ANSI_GREEN = '\x1b[32m';

/**
 * Determine if colors should be used (evaluated once at startup)
 */
const useColors = shouldUseColors();

/**
 * Sensitive field names for data masking
 */
const SENSITIVE_FIELDS = [
  'api_key', 'apikey', 'api-key',
  'password', 'passwd', 'pwd',
  'token', 'access_token', 'auth_token',
  'secret', 'private_key', 'authorization',
];

/**
 * Get emoji for log level
 */
function getLogLevelEmoji(level: LogLevel): string {
  switch (level) {
    case 'DEBUG':
      return '🐛 DEBUG';
    case 'INFO':
      return 'ℹ️  INFO';
    case 'WARN':
      return '⚠️  WARN';
    case 'ERROR':
      return '❌ ERROR';
    default:
      return level;
  }
}

/**
 * Check if a message should be logged based on current log level
 */
function shouldLog(level: LogLevel): boolean {
  return LOG_LEVEL_VALUES[level] >= LOG_LEVEL_VALUES[currentLogLevel];
}

/**
 * Format log message with level and RequestID
 */
function formatLogMessage(level: LogLevel, message: string, forFile = false): string {
  let formattedMessage = `${getLogLevelEmoji(level)}: ${message}`;
  if (currentRequestId) {
    formattedMessage += ` [RequestId=${currentRequestId}]`;
  }

  if (forFile || !useColors) {
    return formattedMessage;
  }

  // Apply colors based on log level
  const color = getColorForLevel(level);
  return `${color}${formattedMessage}${ANSI_RESET}`;
}

/**
 * Get color code for log level
 */
function getColorForLevel(level: LogLevel): string {
  switch (level) {
    case 'DEBUG':
      return ANSI_CYAN;
    case 'INFO':
      return ANSI_BLUE;
    case 'WARN':
      return ANSI_YELLOW;
    case 'ERROR':
      return ANSI_RED;
    default:
      return '';
  }
}

/**
 * Mask sensitive information in data structures
 * @param data Data to mask (dict, str, list, etc.)
 * @param fields Additional sensitive field names
 * @returns Masked data (deep copy)
 */
export function maskSensitiveData(data: any, fields?: string[]): any {
  const sensitiveFields = fields || SENSITIVE_FIELDS;
  const visitedObjects = new WeakSet();

  function mask(obj: any): any {
    if (obj === null || obj === undefined) {
      return obj;
    }

    if (typeof obj === 'object') {
      if (visitedObjects.has(obj)) {
        return '[Circular]';
      }
      visitedObjects.add(obj);

      if (Array.isArray(obj)) {
        return obj.map(item => mask(item));
      }

      const masked: any = {};
      for (const key in obj) {
        if (Object.prototype.hasOwnProperty.call(obj, key)) {
          const value = obj[key];
          if (sensitiveFields.some(field => key.toLowerCase().includes(field.toLowerCase()))) {
            if (typeof value === 'string' && value.length > 4) {
              masked[key] = value.substring(0, 2) + '****' + value.substring(value.length - 2);
            } else {
              masked[key] = '****';
            }
          } else {
            masked[key] = mask(value);
          }
        }
      }
      return masked;
    }

    if (typeof obj === 'string') {
      return obj;
    }

    return obj;
  }

  return mask(data);
}

/**
 * Set the log level
 * @param level The log level to set
 */
export function setLogLevel(level: LogLevel): void {
  if (LOG_LEVEL_VALUES[level] !== undefined) {
    currentLogLevel = level;
  }
}

/**
 * Get the current log level
 * @returns The current log level
 */
export function getLogLevel(): LogLevel {
  return currentLogLevel;
}

/**
 * Set the RequestID for tracking
 * @param requestId The RequestID to set
 */
export function setRequestId(requestId: string): void {
  currentRequestId = requestId;
}

/**
 * Get the current RequestID
 * @returns The current RequestID or empty string
 */
export function getRequestId(): string {
  return currentRequestId;
}

/**
 * Clear the current RequestID
 */
export function clearRequestId(): void {
  currentRequestId = '';
}

/**
 * Parse file size string to bytes (e.g., "10 MB" -> 10485760)
 * @param sizeStr Size string like "10 MB", "100 MB", "1 GB"
 * @returns Size in bytes
 */
function parseFileSize(sizeStr: string): number {
  const match = sizeStr.match(/^(\d+)\s*(MB|GB|KB)?$/i);
  if (!match) {
    return 10 * 1024 * 1024; // Default 10MB
  }

  const value = parseInt(match[1], 10);
  const unit = (match[2] || 'MB').toUpperCase();

  switch (unit) {
    case 'KB':
      return value * 1024;
    case 'MB':
      return value * 1024 * 1024;
    case 'GB':
      return value * 1024 * 1024 * 1024;
    default:
      return value * 1024 * 1024;
  }
}

/**
 * Write log message to file
 * @param message The formatted log message
 */
function writeToFile(message: string): void {
  if (!fileLoggingEnabled || !logFilePath) {
    return;
  }

  try {
    // Check file size and rotate if necessary
    if (fs.existsSync(logFilePath)) {
      const stats = fs.statSync(logFilePath);
      if (stats.size >= logFileMaxSize) {
        // Rotate: rename current file to .log.1
        const rotatedPath = `${logFilePath}.1`;
        if (fs.existsSync(rotatedPath)) {
          fs.unlinkSync(rotatedPath);
        }
        fs.renameSync(logFilePath, rotatedPath);
      }
    }

    // Append to file (create if doesn't exist)
    fs.appendFileSync(logFilePath, message + '\n', 'utf8');
  } catch (error) {
    // Silently fail to avoid infinite loop
    if (consoleLoggingEnabled) {
      process.stderr.write(`Failed to write to log file: ${error}\n`);
    }
  }
}

/**
 * Setup logger configuration
 * @param config Logger configuration options
 *
 * @example
 * ```typescript
 * import { AgentBay, setupLogger } from 'wuying-agentbay-sdk';
 *
 * const agentBay = new AgentBay({ apiKey: 'your_api_key' });
 *
 * async function demonstrateLogging() {
 *     try {
 *         // Configure logging to file only
 *         setupLogger({
 *             level: 'DEBUG',
 *             logFile: '/var/log/myapp.log',
 *             maxFileSize: '100 MB',
 *             enableConsole: false
 *         });
 *
 *         // Create a session - logs will only be written to file
 *         const result = await agentBay.create({ imageId: 'browser_latest' });
 *         if (result.success) {
 *             const session = result.session;
 *             // All operations will be logged to file
 *             await session.delete();
 *         }
 *     } catch (error) {
 *         console.error('Error:', error);
 *     }
 * }
 *
 * demonstrateLogging().catch(console.error);
 * ```
 */
export function setupLogger(config: LoggerConfig): void {
  if (config.level) {
    setLogLevel(config.level);
  }

  if (config.logFile !== undefined) {
    if (config.logFile) {
      logFilePath = config.logFile;
      fileLoggingEnabled = true;

      // Ensure directory exists
      const dir = path.dirname(logFilePath);
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
      }

      // Parse max file size
      if (config.maxFileSize) {
        logFileMaxSize = parseFileSize(config.maxFileSize);
      }
    } else {
      fileLoggingEnabled = false;
      logFilePath = null;
    }
  }

  if (config.enableConsole !== undefined) {
    consoleLoggingEnabled = config.enableConsole;
  }
}

/**
 * Log a message without the log prefix and file location
 * Treated as INFO level - will be filtered if log level is WARN or higher
 * @param message The message to log
 * @param args Optional arguments to log
 */
export function log(message: string, ...args: any[]): void {
  if (!shouldLog('INFO')) return;

  if (consoleLoggingEnabled) {
    process.stdout.write(message + "\n");
  }

  // Write to file without colors
  writeToFile(message);

  if (args.length > 0) {
    for (const arg of args) {
      const argStr = typeof arg === "object" && arg !== null
        ? JSON.stringify(arg, null, 2)
        : String(arg);

      if (consoleLoggingEnabled) {
        process.stdout.write(argStr + "\n");
      }
      writeToFile(argStr);
    }
  }
}

/**
 * Log a debug level message
 * @param message The message to log
 * @param args Optional arguments to log
 */
export function logDebug(message: string, ...args: any[]): void {
  if (!shouldLog('DEBUG')) return;

  const formattedMessage = formatLogMessage('DEBUG', message);
  const fileMessage = formatLogMessage('DEBUG', message, true);

  if (consoleLoggingEnabled) {
    process.stdout.write(formattedMessage + "\n");
  }
  writeToFile(fileMessage);

  if (args.length > 0) {
    for (const arg of args) {
      const argStr = typeof arg === "object" && arg !== null
        ? JSON.stringify(arg, null, 2)
        : String(arg);

      if (consoleLoggingEnabled) {
        process.stdout.write(argStr + "\n");
      }
      writeToFile(argStr);
    }
  }
}

/**
 * Log an info level message
 * @param message The message to log
 * @param args Optional arguments to log
 */
export function logInfo(message: string, ...args: any[]): void {
  if (!shouldLog('INFO')) return;

  const formattedMessage = formatLogMessage('INFO', message);
  const fileMessage = formatLogMessage('INFO', message, true);

  if (consoleLoggingEnabled) {
    process.stdout.write(formattedMessage + "\n");
  }
  writeToFile(fileMessage);

  if (args.length > 0) {
    for (const arg of args) {
      const argStr = typeof arg === "object" && arg !== null
        ? JSON.stringify(arg, null, 2)
        : String(arg);

      if (consoleLoggingEnabled) {
        process.stdout.write(argStr + "\n");
      }
      writeToFile(argStr);
    }
  }
}

/**
 * Log a warning level message (outputs to stderr)
 * @param message The message to log
 * @param args Optional arguments to log
 */
export function logWarn(message: string, ...args: any[]): void {
  if (!shouldLog('WARN')) return;

  const formattedMessage = formatLogMessage('WARN', message);
  const fileMessage = formatLogMessage('WARN', message, true);

  if (consoleLoggingEnabled) {
    process.stderr.write(formattedMessage + "\n");
  }
  writeToFile(fileMessage);

  if (args.length > 0) {
    for (const arg of args) {
      const argStr = typeof arg === "object" && arg !== null
        ? JSON.stringify(arg, null, 2)
        : String(arg);

      if (consoleLoggingEnabled) {
        process.stderr.write(argStr + "\n");
      }
      writeToFile(argStr);
    }
  }
}

/**
 * Log an error message with optional error object (outputs to stderr)
 * @param message The error message to log
 * @param error Optional error object
 */
export function logError(message: string, error?: any): void {
  if (!shouldLog('ERROR')) return;

  const formattedMessage = formatLogMessage('ERROR', message);
  const fileMessage = formatLogMessage('ERROR', message, true);

  if (consoleLoggingEnabled) {
    process.stderr.write(formattedMessage + "\n");
  }
  writeToFile(fileMessage);

  if (error) {
    let errorStr = '';
    if (error instanceof Error) {
      errorStr = error.message;
      if (error.stack) {
        errorStr += `\nStack Trace:\n${error.stack}`;
      }
    } else if (typeof error === "object") {
      errorStr = JSON.stringify(error, null, 2);
    } else {
      errorStr = String(error);
    }

    if (consoleLoggingEnabled) {
      process.stderr.write(errorStr + "\n");
    }
    writeToFile(errorStr);
  }
}

/**
 * Log an API call
 * @param apiName Name of the API being called
 * @param requestData Optional request data to log at DEBUG level
 */
export function logAPICall(apiName: string, requestData?: any): void {
  if (!shouldLog('INFO')) return;
  const message = `🔗 API Call: ${apiName}`;

  // Temporarily clear RequestId since it's not available until API response
  const savedRequestId = currentRequestId;
  currentRequestId = '';

  if (useColors) {
    // Use cyan/bright blue for API calls
    process.stdout.write(`${ANSI_CYAN}ℹ️  INFO: ${message}${ANSI_RESET}\n`);
  } else {
    logInfo(message);
  }

  currentRequestId = savedRequestId;

  if (requestData && shouldLog('DEBUG')) {
    const maskedData = maskSensitiveData(requestData);
    logDebug(`📤 Request: ${JSON.stringify(maskedData)}`);
  }
}

/**
 * Log an API response with key details at INFO level
 * @param apiName Name of the API being called
 * @param requestId Request ID from the response
 * @param success Whether the API call was successful
 * @param keyFields Dictionary of key business fields to log
 * @param fullResponse Full response body (logged at DEBUG level)
 */
export function logAPIResponseWithDetails(
  apiName: string,
  requestId?: string,
  success = true,
  keyFields?: Record<string, any>,
  fullResponse?: string
): void {

  if (success) {
    if (shouldLog('INFO')) {
      let mainMessage = `✅ API Response: ${apiName}`;
      if (requestId) {
        mainMessage += `, RequestId=${requestId}`;
      }

      if (useColors) {
        // Use green for successful API responses
        process.stdout.write(`${ANSI_GREEN}ℹ️  INFO: ${mainMessage}${ANSI_RESET}\n`);
      } else {
        logInfo(mainMessage);
      }

      if (keyFields) {
        for (const [key, value] of Object.entries(keyFields)) {
          const maskedValue = maskSensitiveData({ [key]: value });
          const keyMessage = `  └─ ${key}=${maskedValue[key]}`;
          if (useColors) {
            process.stdout.write(`${ANSI_GREEN}ℹ️  INFO: ${keyMessage}${ANSI_RESET}\n`);
          } else {
            logInfo(keyMessage);
          }
        }
      }
    }

    if (fullResponse && shouldLog('DEBUG')) {
      logDebug(`📥 Full Response: ${fullResponse}`);
    }
  } else {
    if (shouldLog('ERROR')) {
      let errorMessage = `❌ API Response Failed: ${apiName}`;
      if (requestId) {
        errorMessage += `, RequestId=${requestId}`;
      }

      if (useColors) {
        // Use red for failed API responses
        process.stderr.write(`${ANSI_RED}❌ ERROR: ${errorMessage}${ANSI_RESET}\n`);
      } else {
        logError(errorMessage);
      }

      if (fullResponse) {
        if (useColors) {
          process.stderr.write(`${ANSI_RED}ℹ️  INFO: 📥 Response: ${fullResponse}${ANSI_RESET}\n`);
        } else {
          logError(`📥 Response: ${fullResponse}`);
        }
      }
    }
  }
}

/**
 * Extract and log the actual code execution output from run_code response
 * @param requestId Request ID from the API response
 * @param rawOutput Raw JSON output from the MCP tool
 */
export function logCodeExecutionOutput(requestId: string, rawOutput: string): void {
  if (!shouldLog('INFO')) return;

  try {
    // Parse the JSON response to extract the actual code output
    const response = JSON.parse(rawOutput);

    // Extract text from all content items
    const texts: string[] = [];
    if (response && typeof response === 'object' && 'content' in response) {
      const content = response.content;
      if (Array.isArray(content)) {
        for (const item of content) {
          if (item && typeof item === 'object' && item.type === 'text' && item.text) {
            texts.push(item.text);
          }
        }
      }
    }

    if (texts.length === 0) {
      return;
    }

    const actualOutput = texts.join('');

    // Format the output with a clear separator
    const header = `📋 Code Execution Output (RequestID: ${requestId}):`;

    if (useColors) {
      process.stdout.write(`${ANSI_GREEN}ℹ️  INFO: ${header}${ANSI_RESET}\n`);
    } else {
      logInfo(header);
    }

    // Print each line with indentation
    const lines = actualOutput.trimEnd().split('\n');
    for (const line of lines) {
      if (useColors) {
        process.stdout.write(`${ANSI_GREEN}ℹ️  INFO:    ${line}${ANSI_RESET}\n`);
      } else {
        logInfo(`   ${line}`);
      }
    }

    // Also write to file if enabled
    if (fileLoggingEnabled && logFilePath) {
      writeToFile(header);
      for (const line of lines) {
        writeToFile(`   ${line}`);
      }
    }
  } catch (error) {
    // If parsing fails, just return without logging
    return;
  }
}

/**
 * Log operation start
 * @param operation Name of the operation
 * @param details Optional operation details
 */
export function logOperationStart(operation: string, details?: string): void {
  if (!shouldLog('INFO')) return;
  const message = `🚀 Starting: ${operation}`;
  logInfo(message);

  if (details && shouldLog('DEBUG')) {
    logDebug(`📋 Details: ${details}`);
  }
}

/**
 * Log operation success
 * @param operation Name of the operation
 * @param result Optional operation result
 */
export function logOperationSuccess(operation: string, result?: string): void{
  if (!shouldLog('INFO')) return;
  const message = `✅ Completed: ${operation}`;
  logInfo(message);

  if (result && shouldLog('DEBUG')) {
    logDebug(`📊 Result: ${result}`);
  }
}

/**
 * Log operation error
 * @param operation Name of the operation that failed
 * @param error Error message or error object
 * @param includeStackTrace Whether to include stack trace
 */
export function logOperationError(
  operation: string,
  error: string | Error,
  includeStackTrace = false
): void {
  if (!shouldLog('ERROR')) return;
  const message = `❌ Failed: ${operation}`;

  if (typeof error === 'string') {
    logError(message, new Error(error));
  } else if (error instanceof Error) {
    if (includeStackTrace) {
      logError(message, error);
    } else {
      logError(message, error.message);
    }
  } else {
    logError(message, String(error));
  }
}

/**
 * Log an info level message with custom color
 * @param message The message to log
 * @param color ANSI color code (defaults to red)
 */
export function logInfoWithColor(message: string, color: string = ANSI_RED): void {
  if (!shouldLog('INFO')) return;

  const emoji = 'ℹ️  INFO';
  const fullMessage = `${emoji}: ${message}`;

  if (useColors) {
    if (consoleLoggingEnabled) {
      process.stdout.write(`${color}${fullMessage}${ANSI_RESET}\n`);
    }
  } else {
    if (consoleLoggingEnabled) {
      process.stdout.write(fullMessage + "\n");
    }
  }

  // Write to file without colors
  writeToFile(fullMessage);
}
