import { APIError } from "../exceptions";
import { Session } from "../session";
import { Client } from "../api/client";
import { CallMcpToolRequest } from "../api/models/model";
import { log, logError } from "../utils/logger";
import {
  extractRequestId,
  CommandResult,
} from "../types/api-response";
import fetch from "node-fetch";

import * as $_client from "../api";

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
  requestId?: string;
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
   * Handle VPC-based MCP tool calls using HTTP requests.
   */
  private async callMcpToolVPC(
    toolName: string,
    argsJSON: string,
    defaultErrorMsg: string
  ): Promise<CallMcpToolResult> {
    log(`API Call: CallMcpTool (VPC) - ${toolName}`);
    log(`Request: Args=${argsJSON}`);

    // Find server for this tool
    const server = this.session.findServerForTool(toolName);
    if (!server) {
      throw new Error(`server not found for tool: ${toolName}`);
    }

    // Construct VPC URL with query parameters
    const baseURL = `http://${this.session.getNetworkInterfaceIp()}:${this.session.getHttpPort()}/callTool`;

    // Prepare query parameters
    const params = new URLSearchParams({
      server: server,
      tool: toolName,
      args: argsJSON,
      apiKey: this.session.getAPIKey()
    });

    const url = `${baseURL}?${params.toString()}`;

    try {
      // Send HTTP request
      const response = await fetch(url, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        },
        timeout: 30000 // 30 second timeout
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      // Parse response
      const responseData = await response.json() as any;
      log(`Response from VPC CallMcpTool - ${toolName}:`, responseData);

      // Create result object for VPC response
      const result: CallMcpToolResult = {
        data: responseData,
        statusCode: response.status,
        isError: false,
        requestId: "", // VPC requests don't have traditional request IDs
      };

      // Extract the actual result from the nested VPC response structure
      let actualResult: any = responseData;
      if (responseData && typeof responseData.data === 'string') {
        try {
          const dataMap = JSON.parse(responseData.data);
          if (dataMap.result) {
            actualResult = dataMap.result;
          }
        } catch (error) {
          // Keep original responseData if parsing fails
        }
      } else if (responseData && responseData.data && typeof responseData.data === 'object') {
        actualResult = responseData.data;
      }

      result.data = actualResult;
      return result;

    } catch (error) {
      const sanitizedError = this.sanitizeError(error);
      logError(`Error calling VPC CallMcpTool - ${toolName}:`, sanitizedError);
      throw new Error(`failed to call VPC ${toolName}: ${error}`);
    }
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

    const errorStr = String(error);
    
    // Remove API key from URLs
    // Pattern: apiKey=akm-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    let sanitized = errorStr.replace(/apiKey=akm-[a-f0-9-]+/g, 'apiKey=***REDACTED***');
    
    // Remove API key from Bearer tokens
    // Pattern: Bearer akm-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    sanitized = sanitized.replace(/Bearer akm-[a-f0-9-]+/g, 'Bearer ***REDACTED***');
    
    // Remove API key from query parameters
    // Pattern: &apiKey=akm-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    sanitized = sanitized.replace(/&apiKey=akm-[a-f0-9-]+/g, '&apiKey=***REDACTED***');
    
    // Remove API key from URL paths
    // Pattern: /callTool?apiKey=akm-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    sanitized = sanitized.replace(/\/callTool\?apiKey=akm-[a-f0-9-]+/g, '/callTool?apiKey=***REDACTED***');
    
    return sanitized;
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
      
      // Check if this is a VPC session
      if (this.session.isVpcEnabled()) {
        return await this.callMcpToolVPC(toolName, argsJSON, defaultErrorMsg);
      }

      // Non-VPC mode: use traditional API call
      const callToolRequest = new CallMcpToolRequest({
        authorization: `Bearer ${this.session.getAPIKey()}`,
        sessionId: this.session.getSessionId(),
        name: toolName,
        args: argsJSON,
      });

      // Log API request
      log(`API Call: CallMcpTool - ${toolName}`);
      log(
        `Request: SessionId=${this.session.getSessionId()}, Args=${argsJSON}`
      );

      const response = await this.session
        .getClient()
        .callMcpTool(callToolRequest);

      // Log API response
      log(`Response from CallMcpTool - ${toolName}:`, response.body);

      if (!response.body?.data) {
        throw new Error("Invalid response data format");
      }

      // Extract data from response
      const data = response.body.data as Record<string, any>;

      // Create result object
      const result: CallMcpToolResult = {
        data,
        statusCode: response.statusCode || 0,
        isError: false,
        requestId: extractRequestId(response),
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
            if (
              item &&
              typeof item === "object" &&
              item.text &&
              typeof item.text === "string"
            ) {
              textParts.push(item.text);
            }
          }
          result.textContent = textParts.join("\n");
        }
      }

      return result;
    } catch (error) {
      const sanitizedError = this.sanitizeError(error);
      logError(`Error calling CallMcpTool - ${toolName}:`, sanitizedError);
      throw new APIError(`Failed to call ${toolName}: ${error}`);
    }
  }

  /**
   * Execute a command in the cloud environment with a specified timeout.
   * Corresponds to Python's execute_command() method
   *
   * @param command - The command to execute.
   * @param timeoutMs - The timeout for the command execution in milliseconds. Default is 1000ms.
   * @returns CommandResult with command output and requestId
   */
  async executeCommand(
    command: string,
    timeoutMs = 1000
  ): Promise<CommandResult> {
    try {
      const args = {
        command,
        timeout_ms: timeoutMs,
      };

      const result = await this.callMcpTool(
        "shell",
        args,
        "Failed to execute command"
      );

      return {
        requestId: result.requestId || "",
        success: true,
        output: result.textContent || "",
      };
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
