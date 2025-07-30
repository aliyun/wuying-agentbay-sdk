
import {
  WindowListResult,
  WindowInfoResult,
  BoolResult,
} from "../types/api-response";



/**
 * Represents a window in the system.
 */
export interface Window {
  window_id: number;
  title: string;
  absolute_upper_left_x?: number;
  absolute_upper_left_y?: number;
  width?: number;
  height?: number;
  pid?: number;
  pname?: string;
  child_windows?: Window[];
}

/**
 * Handles window management operations in the AgentBay cloud environment.
 */
export class WindowManager {
  private session: {
    getAPIKey(): string;
    getSessionId(): string;
    callMcpTool(toolName: string, args: any): Promise<{
      success: boolean;
      data: string;
      errorMessage: string;
      requestId: string;
    }>;
  };

  /**
   * Creates a new WindowManager instance.
   * @param session The session object that provides access to the AgentBay API.
   */
  constructor(session: {
    getAPIKey(): string;
    getSessionId(): string;
    callMcpTool(toolName: string, args: any): Promise<{
      success: boolean;
      data: string;
      errorMessage: string;
      requestId: string;
    }>;
  }) {
    this.session = session;
  }



  /**
   * Helper method to parse JSON string into Window objects
   * @param jsonStr - JSON string to parse
   * @returns Array of Window objects or single Window object
   */
  private parseWindowsFromJSON(jsonStr: string): Window[] {
    try {
      const parsed = JSON.parse(jsonStr);
      return Array.isArray(parsed) ? parsed : [parsed];
    } catch (error) {
      throw new Error(`Failed to parse window data: ${error}`);
    }
  }

  /**
   * Lists all root windows in the system.
   * Corresponds to Python's list_root_windows() method
   *
   * @param timeoutMs - The timeout in milliseconds. Default is 3000ms.
   * @returns WindowListResult with windows array and requestId
   */
  async listRootWindows(timeoutMs = 3000): Promise<WindowListResult> {
    try {
      const args = {
        timeout_ms: timeoutMs,
      };

      const response = await this.session.callMcpTool(
        "list_root_windows",
        args
      );

      if (!response.success) {
        return {
          requestId: response.requestId,
          success: false,
          windows: [],
          errorMessage: response.errorMessage,
        };
      }

      const windows = response.data
        ? this.parseWindowsFromJSON(response.data)
        : [];

      return {
        requestId: response.requestId,
        success: true,
        windows,
      };
    } catch (error) {
      return {
        requestId: "",
        success: false,
        windows: [],
        errorMessage: `Failed to list root windows: ${error}`,
      };
    }
  }

  /**
   * Gets the currently active window.
   * Corresponds to Python's get_active_window() method
   *
   * @param timeoutMs - The timeout in milliseconds. Default is 3000ms.
   * @returns WindowInfoResult with active window data and requestId
   */
  async getActiveWindow(timeoutMs = 3000): Promise<WindowInfoResult> {
    try {
      const args = {
        timeout_ms: timeoutMs,
      };

      const response = await this.session.callMcpTool(
        "get_active_window",
        args
      );

      if (!response.success) {
        return {
          requestId: response.requestId,
          success: false,
          errorMessage: response.errorMessage,
        };
      }

      let activeWindow: Window | undefined = undefined;
      if (response.data) {
        const windows = this.parseWindowsFromJSON(response.data);
        activeWindow = windows.length > 0 ? windows[0] : undefined;
      }

      return {
        requestId: response.requestId,
        success: true,
        window: activeWindow,
      };
    } catch (error) {
      return {
        requestId: "",
        success: false,
        errorMessage: `Failed to get active window: ${error}`,
      };
    }
  }

  /**
   * Activates a window by ID.
   * Corresponds to Python's activate_window() method
   *
   * @param windowId The ID of the window to activate.
   * @returns BoolResult with requestId
   */
  async activateWindow(windowId: number): Promise<BoolResult> {
    try {
      const args = {
        window_id: windowId,
      };

      const response = await this.session.callMcpTool(
        "activate_window",
        args
      );

      if (!response.success) {
        return {
          requestId: response.requestId,
          success: false,
          errorMessage: response.errorMessage,
        };
      }

      return {
        requestId: response.requestId,
        success: true,
        data: true,
      };
    } catch (error) {
      return {
        requestId: "",
        success: false,
        errorMessage: `Failed to activate window: ${error}`,
      };
    }
  }

  /**
   * Maximizes a window by ID.
   * Corresponds to Python's maximize_window() method
   *
   * @param windowId The ID of the window to maximize.
   * @returns BoolResult with requestId
   */
  async maximizeWindow(windowId: number): Promise<BoolResult> {
    try {
      const args = {
        window_id: windowId,
      };

      const response = await this.session.callMcpTool(
        "maximize_window",
        args
      );

      if (!response.success) {
        return {
          requestId: response.requestId,
          success: false,
          errorMessage: response.errorMessage,
        };
      }

      return {
        requestId: response.requestId,
        success: true,
        data: true,
      };
    } catch (error) {
      return {
        requestId: "",
        success: false,
        errorMessage: `Failed to maximize window: ${error}`,
      };
    }
  }

  /**
   * Minimizes a window by ID.
   * Corresponds to Python's minimize_window() method
   *
   * @param windowId The ID of the window to minimize.
   * @returns BoolResult with requestId
   */
  async minimizeWindow(windowId: number): Promise<BoolResult> {
    try {
      const args = {
        window_id: windowId,
      };

      const response = await this.session.callMcpTool(
        "minimize_window",
        args
      );

      if (!response.success) {
        return {
          requestId: response.requestId,
          success: false,
          errorMessage: response.errorMessage,
        };
      }

      return {
        requestId: response.requestId,
        success: true,
        data: true,
      };
    } catch (error) {
      return {
        requestId: "",
        success: false,
        errorMessage: `Failed to minimize window: ${error}`,
      };
    }
  }

  /**
   * Restores a window by ID.
   * Corresponds to Python's restore_window() method
   *
   * @param windowId The ID of the window to restore.
   * @returns BoolResult with requestId
   */
  async restoreWindow(windowId: number): Promise<BoolResult> {
    try {
      const args = {
        window_id: windowId,
      };

      const response = await this.session.callMcpTool(
        "restore_window",
        args
      );

      if (!response.success) {
        return {
          requestId: response.requestId,
          success: false,
          errorMessage: response.errorMessage,
        };
      }

      return {
        requestId: response.requestId,
        success: true,
        data: true,
      };
    } catch (error) {
      return {
        requestId: "",
        success: false,
        errorMessage: `Failed to restore window: ${error}`,
      };
    }
  }

  /**
   * Closes a window by ID.
   * Corresponds to Python's close_window() method
   *
   * @param windowId The ID of the window to close.
   * @returns BoolResult with requestId
   */
  async closeWindow(windowId: number): Promise<BoolResult> {
    try {
      const args = {
        window_id: windowId,
      };

      const response = await this.session.callMcpTool(
        "close_window",
        args
      );

      if (!response.success) {
        return {
          requestId: response.requestId,
          success: false,
          errorMessage: response.errorMessage,
        };
      }

      return {
        requestId: response.requestId,
        success: true,
        data: true,
      };
    } catch (error) {
      return {
        requestId: "",
        success: false,
        errorMessage: `Failed to close window: ${error}`,
      };
    }
  }

  /**
   * Sets a window to fullscreen by ID.
   * Corresponds to Python's fullscreen_window() method
   *
   * @param windowId The ID of the window to set to fullscreen.
   * @returns BoolResult with requestId
   */
  async fullscreenWindow(windowId: number): Promise<BoolResult> {
    try {
      const args = {
        window_id: windowId,
      };

      const response = await this.session.callMcpTool(
        "fullscreen_window",
        args
      );

      if (!response.success) {
        return {
          requestId: response.requestId,
          success: false,
          errorMessage: response.errorMessage,
        };
      }

      return {
        requestId: response.requestId,
        success: true,
        data: true,
      };
    } catch (error) {
      return {
        requestId: "",
        success: false,
        errorMessage: `Failed to make window fullscreen: ${error}`,
      };
    }
  }

  /**
   * Resizes a window by ID.
   * Corresponds to Python's resize_window() method
   *
   * @param windowId The ID of the window to resize.
   * @param width The new width of the window.
   * @param height The new height of the window.
   * @returns BoolResult with requestId
   */
  async resizeWindow(
    windowId: number,
    width: number,
    height: number
  ): Promise<BoolResult> {
    try {
      const args = {
        window_id: windowId,
        width,
        height,
      };

      const response = await this.session.callMcpTool(
        "resize_window",
        args
      );

      if (!response.success) {
        return {
          requestId: response.requestId,
          success: false,
          errorMessage: response.errorMessage,
        };
      }

      return {
        requestId: response.requestId,
        success: true,
        data: true,
      };
    } catch (error) {
      return {
        requestId: "",
        success: false,
        errorMessage: `Failed to resize window: ${error}`,
      };
    }
  }

  /**
   * Enables or disables focus mode.
   * Corresponds to Python's focus_mode() method
   *
   * @param on Whether to enable focus mode.
   * @returns BoolResult with requestId
   */
  async focusMode(on: boolean): Promise<BoolResult> {
    try {
      const args = {
        on,
      };

      const response = await this.session.callMcpTool(
        "focus_mode",
        args
      );

      if (!response.success) {
        return {
          requestId: response.requestId,
          success: false,
          errorMessage: response.errorMessage,
        };
      }

      return {
        requestId: response.requestId,
        success: true,
        data: true,
      };
    } catch (error) {
      return {
        requestId: "",
        success: false,
        errorMessage: `Failed to toggle focus mode: ${error}`,
      };
    }
  }
}
