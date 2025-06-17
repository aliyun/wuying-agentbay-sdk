import { CallMcpToolRequest } from '../api/models/CallMcpToolRequest';

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
    getClient(): any;
    getSessionId(): string;
  };

  /**
   * Creates a new WindowManager instance.
   * @param session The session object that provides access to the AgentBay API.
   */
  constructor(session: {
    getAPIKey(): string;
    getClient(): any;
    getSessionId(): string;
  }) {
    this.session = session;
  }

  /**
   * Call an MCP tool with the given name and arguments.
   * @param name The name of the tool to call.
   * @param args The arguments to pass to the tool.
   * @returns The response from the tool.
   * @throws Error if the tool call fails.
   */
  private async callMcpTool(name: string, args: any): Promise<any> {
    try {
      const argsJSON = JSON.stringify(args);
      const request = new CallMcpToolRequest({
        authorization: `Bearer ${this.session.getAPIKey()}`,
        sessionId: this.session.getSessionId(),
        name,
        args: argsJSON
      });

      // Log API request
      console.log(`API Call: CallMcpTool - ${name}`);
      console.log(`Request: SessionId=${request.sessionId}, Args=${request.args}`);

      const response = await this.session.getClient().callMcpTool(request);
      console.log(`Response from CallMcpTool - ${name}:`, JSON.stringify(response));

      // Log API response
      if (response && response.body) {
        console.log(`Response from CallMcpTool - ${name}:`, response.body);
      }

      // Parse the response
      const data = response.body?.data;
      if (!data) {
        throw new Error('Invalid response data format');
      }

      // Extract content array
      const content = data.content;
      if (!content || content.length === 0) {
        throw new Error('Invalid or empty content array in response');
      }

      // Extract text field from the first content item
      const contentItem = content[0];
      const jsonText = contentItem.text;
      if (!jsonText) {
        throw new Error('Text field not found or not a string');
      }

      // Parse the JSON text
      return JSON.parse(jsonText);
    } catch (error) {
      throw new Error(`Failed to call MCP tool ${name}: ${error}`);
    }
  }

  /**
   * Gets detailed window information for a process by name.
   * @param pname The name of the process.
   * @returns A list of windows for the process.
   * @throws Error if the operation fails.
   */
  async getWindowInfoByPName(pname: string): Promise<Window[]> {
    const args = {
      pname
    };

    try {
      const result = await this.callMcpTool('get_window_info_by_pname', args);
      return result as Window[];
    } catch (error) {
      throw new Error(`Failed to get window info by pname: ${error}`);
    }
  }

  /**
   * Gets detailed window information for a process by ID.
   * @param pid The ID of the process.
   * @returns A list of windows for the process.
   * @throws Error if the operation fails.
   */
  async getWindowInfoByPID(pid: number): Promise<Window[]> {
    const args = {
      pid
    };

    try {
      const result = await this.callMcpTool('get_window_info_by_pid', args);
      return result as Window[];
    } catch (error) {
      throw new Error(`Failed to get window info by pid: ${error}`);
    }
  }

  /**
   * Lists all root windows in the system.
   * @returns A list of root windows.
   * @throws Error if the operation fails.
   */
  async listRootWindows(): Promise<Window[]> {
    const args = {};

    try {
      const result = await this.callMcpTool('list_root_windows', args);
      console.log(result);
      
      return result as Window[];
    } catch (error) {
      throw new Error(`Failed to list root windows: ${error}`);
    }
  }

  /**
   * Gets the currently active window.
   * @returns The active window.
   * @throws Error if the operation fails.
   */
  async getActiveWindow(): Promise<Window> {
    const args = {};

    try {
      const result = await this.callMcpTool('get_active_window', args);
      return result as Window;
    } catch (error) {
      throw new Error(`Failed to get active window: ${error}`);
    }
  }

  /**
   * Activates a window by ID.
   * @param windowId The ID of the window to activate.
   * @throws Error if the operation fails.
   */
  async activateWindow(windowId: number): Promise<void> {
    const args = {
      window_id: windowId
    };

    try {
      await this.callMcpTool('activate_window', args);
    } catch (error) {
      throw new Error(`Failed to activate window: ${error}`);
    }
  }

  /**
   * Maximizes a window by ID.
   * @param windowId The ID of the window to maximize.
   * @throws Error if the operation fails.
   */
  async maximizeWindow(windowId: number): Promise<void> {
    const args = {
      window_id: windowId
    };

    try {
      await this.callMcpTool('maximize_window', args);
    } catch (error) {
      throw new Error(`Failed to maximize window: ${error}`);
    }
  }

  /**
   * Minimizes a window by ID.
   * @param windowId The ID of the window to minimize.
   * @throws Error if the operation fails.
   */
  async minimizeWindow(windowId: number): Promise<void> {
    const args = {
      window_id: windowId
    };

    try {
      await this.callMcpTool('minimize_window', args);
    } catch (error) {
      throw new Error(`Failed to minimize window: ${error}`);
    }
  }

  /**
   * Restores a window by ID.
   * @param windowId The ID of the window to restore.
   * @throws Error if the operation fails.
   */
  async restoreWindow(windowId: number): Promise<void> {
    const args = {
      window_id: windowId
    };

    try {
      await this.callMcpTool('restore_window', args);
    } catch (error) {
      throw new Error(`Failed to restore window: ${error}`);
    }
  }

  /**
   * Closes a window by ID.
   * @param windowId The ID of the window to close.
   * @throws Error if the operation fails.
   */
  async closeWindow(windowId: number): Promise<void> {
    const args = {
      window_id: windowId
    };

    try {
      await this.callMcpTool('close_window', args);
    } catch (error) {
      throw new Error(`Failed to close window: ${error}`);
    }
  }

  /**
   * Toggles fullscreen mode for a window by ID.
   * @param windowId The ID of the window to toggle fullscreen for.
   * @throws Error if the operation fails.
   */
  async fullscreenWindow(windowId: number): Promise<void> {
    const args = {
      window_id: windowId
    };

    try {
      await this.callMcpTool('fullscreen_window', args);
    } catch (error) {
      throw new Error(`Failed to fullscreen window: ${error}`);
    }
  }

  /**
   * Resizes a window by ID.
   * @param windowId The ID of the window to resize.
   * @param width The new width of the window.
   * @param height The new height of the window.
   * @throws Error if the operation fails.
   */
  async resizeWindow(windowId: number, width: number, height: number): Promise<void> {
    const args = {
      window_id: windowId,
      width,
      height
    };

    try {
      await this.callMcpTool('resize_window', args);
    } catch (error) {
      throw new Error(`Failed to resize window: ${error}`);
    }
  }

  /**
   * Enables or disables focus mode.
   * @param on Whether to enable focus mode.
   * @throws Error if the operation fails.
   */
  async focusMode(on: boolean): Promise<void> {
    const args = {
      on
    };

    try {
      await this.callMcpTool('focus_mode', args);
    } catch (error) {
      throw new Error(`Failed to set focus mode: ${error}`);
    }
  }
}
