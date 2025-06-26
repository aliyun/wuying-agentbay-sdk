import { APIError } from '../exceptions';
import { Session } from '../session';
import { Client } from '../api/client';
import { CallMcpToolRequest } from '../api/models/model';
import { log, logError } from '../utils/logger';

import * as $_client from '../api';

/**
 * Result object for a CallMcpTool operation
 */
interface CallMcpToolResult {
  data: Record<string, any>;
  content?: any[];
  textContent?: string;
  isError: boolean;
  errorMsg?: string;
  statusCode: number;
}

/**
 * Represents the result of a command execution
 */
export interface CommandResult {
  output: string;
  exitCode?: number;
  durationMs?: number;
}

/**
 * Represents the result of code execution
 */
export interface CodeExecutionResult {
  output: string;
  durationMs?: number;
  memoryKb?: number;
}

/**
 * Handles command execution operations in the AgentBay cloud environment.
 */
export class Command {
  private session: Session;
  private client!: $_client.Client;
  private baseUrl!: string;

  /**
   * Initialize a Command object.
   * 
   * @param session - The Session instance that this Command belongs to.
   */
  constructor(session: Session) {
    this.session = session;
  }

  /**
   * Helper method to call MCP tools and handle common response processing
   * 
   * @param toolName - Name of the MCP tool to call
   * @param args - Arguments to pass to the tool
   * @param defaultErrorMsg - Default error message if specific error details are not available
   * @returns A CallMcpToolResult with the response data
   * @throws APIError if the call fails
   */
  private async callMcpTool(
    toolName: string, 
    args: Record<string, any>,
    defaultErrorMsg: string
  ): Promise<CallMcpToolResult> {
    try {
      const argsJSON = JSON.stringify(args);
      const callToolRequest = new CallMcpToolRequest({
        authorization: `Bearer ${this.session.getAPIKey()}`,
        sessionId: this.session.getSessionId(),
        name: toolName,
        args: argsJSON
      });
      
      // Log API request
      log(`API Call: CallMcpTool - ${toolName}`);
      log(`Request: SessionId=${this.session.getSessionId()}, Args=${argsJSON}`);
      
      const response = await this.session.getClient().callMcpTool(callToolRequest);
      
      // Log API response
      log(`Response from CallMcpTool - ${toolName}:`, response.body);
      
      if (!response.body?.data) {
        throw new Error('Invalid response data format');
      }
      
      // Extract data from response
      const data = response.body.data as Record<string, any>;
      
      // Create result object
      const result: CallMcpToolResult = {
        data,
        statusCode: response.statusCode || 0,
        isError: false
      };
      
      // Check if there's an error in the response
      if (data.isError === true) {
        result.isError = true;
        
        // Try to extract the error message from the content field
        const contentArray = data.content as any[] | undefined;
        if (contentArray && contentArray.length > 0) {
          result.content = contentArray;
          
          // Extract error message from the first content item
          if (contentArray[0]?.text) {
            result.errorMsg = contentArray[0].text;
            throw new Error(contentArray[0].text);
          }
        }
        throw new Error(defaultErrorMsg);
      }
      
      // Extract content array if it exists
      if (Array.isArray(data.content)) {
        result.content = data.content;
        
        // Extract textContent from content items
        if (result.content.length > 0) {
          const textParts: string[] = [];
          for (const item of result.content) {
            if (item && typeof item === 'object' && item.text && typeof item.text === 'string') {
              textParts.push(item.text);
            }
          }
          result.textContent = textParts.join('\n');
        }
      }
      
      return result;
    } catch (error) {
      logError(`Error calling CallMcpTool - ${toolName}:`, error);
      throw new APIError(`Failed to call ${toolName}: ${error}`);
    }
  }

  /**
   * Helper method to parse JSON string or return a simple object with output
   */
  private parseCommandResult(text: string): CommandResult {
    try {
      return JSON.parse(text) as CommandResult;
    } catch (error) {
      return { output: text };
    }
  }

  /**
   * Execute a command in the cloud environment with a specified timeout.
   * 
   * @param command - The command to execute.
   * @param timeoutMs - The timeout for the command execution in milliseconds. Default is 1000ms.
   * @returns A string containing the command output
   */
  async executeCommand(command: string, timeoutMs: number = 1000): Promise<string> {
    const args = {
      command,
      timeout_ms: timeoutMs
    };
    
    const result = await this.callMcpTool('shell', args, 'Failed to execute command');
    
    // Return the text content directly
    return result.textContent || '';
  }
  
  /**
   * Helper method to parse JSON string or return a simple object with output
   */
  private parseCodeExecutionResult(text: string): CodeExecutionResult {
    try {
      return JSON.parse(text) as CodeExecutionResult;
    } catch (error) {
      return { output: text };
    }
  }
  
  /**
   * Execute code in the specified language with a timeout.
   * 
   * @param code - The code to execute.
   * @param language - The programming language of the code. Must be either 'python' or 'javascript'.
   * @param timeoutS - The timeout for the code execution in seconds. Default is 300s.
   * @returns A string containing the code execution output
   * @throws APIError if the code execution fails or if an unsupported language is specified.
   */
  async runCode(code: string, language: string, timeoutS: number = 300): Promise<string> {
    // Validate language
    if (language !== 'python' && language !== 'javascript') {
      throw new Error(`Unsupported language: ${language}. Supported languages are 'python' and 'javascript'`);
    }
    
    const args = {
      code,
      language,
      timeout_s: timeoutS
    };
    
    const result = await this.callMcpTool('run_code', args, 'Failed to execute code');
    
    // Return the text content directly
    return result.textContent || '';
  }
}
