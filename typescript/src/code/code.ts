import { APIError } from "../exceptions";
import { Session } from "../session";
import { Client } from "../api/client";
import { CallMcpToolRequest } from "../api/models/model";
import { log, logError } from "../utils/logger";
import {
  extractRequestId,
  CodeExecutionResult,
} from "../types/api-response";

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
 * Handles code execution operations in the AgentBay cloud environment.
 */
export class Code {
  private session: Session;
  private client!: $_client.Client;
  private baseUrl!: string;

  /**
   * Initialize a Code object.
   *
   * @param session - The Session instance that this Code belongs to.
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
      logError(`Error calling CallMcpTool - ${toolName}:`, error);
      throw new APIError(`Failed to call ${toolName}: ${error}`);
    }
  }

  /**
   * Execute code in the specified language with a timeout.
   * Corresponds to Python's run_code() method
   *
   * @param code - The code to execute.
   * @param language - The programming language of the code. Must be either 'python' or 'javascript'.
   * @param timeoutS - The timeout for the code execution in seconds. Default is 300s.
   * @returns CodeExecutionResult with code execution output and requestId
   * @throws Error if an unsupported language is specified.
   */
  async runCode(
    code: string,
    language: string,
    timeoutS = 300
  ): Promise<CodeExecutionResult> {
    try {
      // Validate language
      if (language !== "python" && language !== "javascript") {
        return {
          requestId: "",
          success: false,
          result: "",
          errorMessage: `Unsupported language: ${language}. Supported languages are 'python' and 'javascript'`,
        };
      }

      const args = {
        code,
        language,
        timeout_s: timeoutS,
      };

      const result = await this.callMcpTool(
        "run_code",
        args,
        "Failed to execute code"
      );
      return {
        requestId: result.requestId || "",
        success: true,
        result: result.textContent || "",
      };
    } catch (error) {
      return {
        requestId: "",
        success: false,
        result: "",
        errorMessage: `Failed to run code: ${error}`,
      };
    }
  }
} 