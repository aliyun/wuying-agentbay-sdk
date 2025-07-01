import { APIError } from "../exceptions";
import { Session } from "../session";
import { CallMcpToolRequest } from "../api/models/model";
import { log, logError } from "../utils/logger";
import {
  ApiResponse,
  ApiResponseWithData,
  extractRequestId,
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
   * Retrieves all clickable UI elements within the specified timeout.
   *
   * @param timeoutMs - The timeout in milliseconds. Default is 2000ms.
   * @returns API response with clickable UI elements array and requestId
   * @throws Error if the operation fails.
   */
  async getClickableUIElements(
    timeoutMs = 2000
  ): Promise<ApiResponseWithData<UIElement[]>> {
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
        logError("Failed to parse clickable UI elements:", error);
        throw new APIError(`Failed to parse clickable UI elements: ${error}`);
      }
    }

    return {
      requestId: result.requestId,
      data: elements,
    };
  }

  /**
   * Retrieves all UI elements within the specified timeout.
   *
   * @param timeoutMs - The timeout in milliseconds. Default is 2000ms.
   * @returns API response with all UI elements array and requestId
   * @throws Error if the operation fails.
   */
  async getAllUIElements(
    timeoutMs = 2000
  ): Promise<ApiResponseWithData<UIElement[]>> {
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
        logError("Failed to parse all UI elements:", error);
        throw new APIError(`Failed to parse all UI elements: ${error}`);
      }
    }

    return {
      requestId: result.requestId,
      data: elements,
    };
  }

  /**
   * Sends a key press event.
   *
   * @param key - The key code to send.
   * @returns API response with key press result and requestId
   * @throws Error if the operation fails.
   */
  async sendKey(key: number): Promise<ApiResponseWithData<string>> {
    const args = {
      key,
    };

    const result = await this.callMcpTool(
      "send_key",
      args,
      "Failed to send key"
    );

    return {
      requestId: result.requestId,
      data: result.textContent || "",
    };
  }

  /**
   * Inputs text into the active field.
   *
   * @param text - The text to input.
   * @returns API response with input result and requestId
   * @throws Error if the operation fails.
   */
  async inputText(text: string): Promise<ApiResponseWithData<string>> {
    const args = {
      text,
    };

    const result = await this.callMcpTool(
      "input_text",
      args,
      "Failed to input text"
    );

    return {
      requestId: result.requestId,
      data: result.textContent || "",
    };
  }

  /**
   * Performs a swipe gesture on the screen.
   *
   * @param startX - The starting X coordinate.
   * @param startY - The starting Y coordinate.
   * @param endX - The ending X coordinate.
   * @param endY - The ending Y coordinate.
   * @param durationMs - The duration of the swipe in milliseconds. Default is 300ms.
   * @returns API response with swipe result and requestId
   * @throws Error if the operation fails.
   */
  async swipe(
    startX: number,
    startY: number,
    endX: number,
    endY: number,
    durationMs = 300
  ): Promise<ApiResponseWithData<string>> {
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
      requestId: result.requestId,
      data: result.textContent || "",
    };
  }

  /**
   * Performs a click at the specified coordinates.
   *
   * @param x - The X coordinate.
   * @param y - The Y coordinate.
   * @param button - The mouse button to click. Default is 'left'.
   * @returns API response with click result and requestId
   * @throws Error if the operation fails.
   */
  async click(
    x: number,
    y: number,
    button = "left"
  ): Promise<ApiResponseWithData<string>> {
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
      requestId: result.requestId,
      data: result.textContent || "",
    };
  }

  /**
   * Takes a screenshot of the current screen.
   *
   * @returns API response with screenshot data and requestId
   * @throws Error if the operation fails.
   */
  async screenshot(): Promise<ApiResponseWithData<string>> {
    const args = {};

    const result = await this.callMcpTool(
      "system_screenshot",
      args,
      "Failed to take screenshot"
    );

    return {
      requestId: result.requestId,
      data: result.textContent || "",
    };
  }
}
