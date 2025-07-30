import { APIError } from "../exceptions";
import { Session } from "../session";
import { CallMcpToolRequest } from "../api/models/model";
import { log, logError } from "../utils/logger";
import {
  extractRequestId,
  UIElementListResult,
  BoolResult,
  OperationResult,
} from "../types/api-response";

/**
 * Interface representing a UI element in the UI hierarchy
 */
export interface UIElement {
  bounds: string;
  className: string;
  text: string;
  type: string;
  resourceId: string;
  index: number;
  isParent: boolean;
  children?: UIElement[];
}

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
 * KeyCode constants for mobile device input
 */
export const KeyCode = {
  HOME: 3,
  BACK: 4,
  VOLUME_UP: 24,
  VOLUME_DOWN: 25,
  POWER: 26,
  MENU: 82,
};

/**
 * UI handles UI operations in the AgentBay cloud environment.
 */
export class UI {
  private session: Session;

  /**
   * Initialize a UI object.
   *
   * @param session - The Session instance that this UI belongs to.
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
   * Retrieves all clickable UI elements within the specified timeout.
   * Corresponds to Python's get_clickable_ui_elements() method
   *
   * @param timeoutMs - The timeout in milliseconds. Default is 2000ms.
   * @returns UIElementListResult with clickable UI elements and requestId
   */
  async getClickableUIElements(timeoutMs = 2000): Promise<UIElementListResult> {
    try {
      const args = {
        timeout_ms: timeoutMs,
      };

      const result = await this.callMcpTool(
        "get_clickable_ui_elements",
        args,
        "Failed to get clickable UI elements"
      );

      let elements: UIElement[] = [];
      if (result.textContent) {
        try {
          elements = JSON.parse(result.textContent) as UIElement[];
        } catch (error) {
          return {
            requestId: result.requestId || "",
            success: false,
            elements: [],
            errorMessage: `Failed to parse clickable UI elements: ${error}`,
          };
        }
      }

      return {
        requestId: result.requestId || "",
        success: true,
        elements,
      };
    } catch (error) {
      return {
        requestId: "",
        success: false,
        elements: [],
        errorMessage: `Failed to get clickable UI elements: ${error}`,
      };
    }
  }

  /**
   * Retrieves all UI elements within the specified timeout.
   * Corresponds to Python's get_all_ui_elements() method
   *
   * @param timeoutMs - The timeout in milliseconds. Default is 2000ms.
   * @returns UIElementListResult with all UI elements and requestId
   */
  async getAllUIElements(timeoutMs = 2000): Promise<UIElementListResult> {
    try {
      const args = {
        timeout_ms: timeoutMs,
      };

      const result = await this.callMcpTool(
        "get_all_ui_elements",
        args,
        "Failed to get all UI elements"
      );

      let elements: UIElement[] = [];
      if (result.textContent) {
        try {
          elements = JSON.parse(result.textContent) as UIElement[];
        } catch (error) {
          return {
            requestId: result.requestId || "",
            success: false,
            elements: [],
            errorMessage: `Failed to parse all UI elements: ${error}`,
          };
        }
      }

      return {
        requestId: result.requestId || "",
        success: true,
        elements,
      };
    } catch (error) {
      return {
        requestId: "",
        success: false,
        elements: [],
        errorMessage: `Failed to get all UI elements: ${error}`,
      };
    }
  }

  /**
   * Sends a key press event.
   * Corresponds to Python's send_key() method
   *
   * @param key - The key code to send.
   * @returns BoolResult with key press result and requestId
   */
  async sendKey(key: number): Promise<BoolResult> {
    try {
      const args = {
        key,
      };

      const result = await this.callMcpTool(
        "send_key",
        args,
        "Failed to send key"
      );

      return {
        requestId: result.requestId || "",
        success: true,
        data: true,
      };
    } catch (error) {
      return {
        requestId: "",
        success: false,
        errorMessage: `Failed to send key: ${error}`,
      };
    }
  }

  /**
   * Inputs text into the active field.
   * Corresponds to Python's input_text() method
   *
   * @param text - The text to input.
   * @returns BoolResult with input result and requestId
   */
  async inputText(text: string): Promise<BoolResult> {
    try {
      const args = {
        text,
      };

      const result = await this.callMcpTool(
        "input_text",
        args,
        "Failed to input text"
      );

      return {
        requestId: result.requestId || "",
        success: true,
        data: true,
      };
    } catch (error) {
      return {
        requestId: "",
        success: false,
        errorMessage: `Failed to input text: ${error}`,
      };
    }
  }

  /**
   * Performs a swipe gesture on the screen.
   * Corresponds to Python's swipe() method
   *
   * @param startX - The starting X coordinate.
   * @param startY - The starting Y coordinate.
   * @param endX - The ending X coordinate.
   * @param endY - The ending Y coordinate.
   * @param durationMs - The duration of the swipe in milliseconds. Default is 300ms.
   * @returns BoolResult with swipe result and requestId
   */
  async swipe(
    startX: number,
    startY: number,
    endX: number,
    endY: number,
    durationMs = 300
  ): Promise<BoolResult> {
    try {
      const args = {
        start_x: startX,
        start_y: startY,
        end_x: endX,
        end_y: endY,
        duration_ms: durationMs,
      };

      const result = await this.callMcpTool(
        "swipe",
        args,
        "Failed to perform swipe"
      );

      return {
        requestId: result.requestId || "",
        success: true,
        data: true,
      };
    } catch (error) {
      return {
        requestId: "",
        success: false,
        errorMessage: `Failed to perform swipe: ${error}`,
      };
    }
  }

  /**
   * Performs a click at the specified coordinates.
   * Corresponds to Python's click() method
   *
   * @param x - The X coordinate.
   * @param y - The Y coordinate.
   * @param button - The mouse button to click. Default is 'left'.
   * @returns BoolResult with click result and requestId
   */
  async click(x: number, y: number, button = "left"): Promise<BoolResult> {
    try {
      const args = {
        x,
        y,
        button,
      };

      const result = await this.callMcpTool(
        "click",
        args,
        "Failed to perform click"
      );

      return {
        requestId: result.requestId || "",
        success: true,
        data: true,
      };
    } catch (error) {
      return {
        requestId: "",
        success: false,
        errorMessage: `Failed to perform click: ${error}`,
      };
    }
  }

  /**
   * Takes a screenshot of the current screen.
   * Corresponds to Python's screenshot() method
   *
   * @returns OperationResult with screenshot data and requestId
   */
  async screenshot(): Promise<OperationResult> {
    try {
      const args = {};

      const result = await this.callMcpTool(
        "system_screenshot",
        args,
        "Failed to take screenshot"
      );

      return {
        requestId: result.requestId || "",
        success: true,
        data: result.textContent || "",
      };
    } catch (error) {
      return {
        requestId: "",
        success: false,
        errorMessage: `Failed to take screenshot: ${error}`,
      };
    }
  }
}
