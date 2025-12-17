/**
 * Computer module for desktop UI automation.
 * Provides mouse, keyboard, and screen operations for desktop environments.
 */

import { logInfo } from "../../src/utils/logger";
import { OperationResult, WindowListResult, WindowInfoResult, BoolResult as WindowBoolResult } from "../types/api-response";
import { convertObjectKeys, convertWindowData, convertWindowList } from "../utils/field-converter";

export enum MouseButton {
  LEFT = 'left',
  RIGHT = 'right',
  MIDDLE = 'middle',
  DOUBLE_LEFT = 'double_left'
}

export enum ScrollDirection {
  UP = 'up',
  DOWN = 'down',
  LEFT = 'left',
  RIGHT = 'right'
}

export interface BoolResult extends OperationResult {
  data?: boolean;
}

export interface CursorPosition extends OperationResult {
  x: number;
  y: number;
}

export interface ScreenSize extends OperationResult {
  width: number;
  height: number;
  dpiScalingFactor: number;
}

export interface ScreenshotResult extends OperationResult {
  data: string; // Screenshot URL
}

// Session interface for Computer module
// eslint-disable-next-line @typescript-eslint/no-explicit-any
interface ComputerSession {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  callMcpTool(toolName: string, args: Record<string, any>): Promise<any>;
  sessionId: string;
  getAPIKey(): string;
  getSessionId(): string;
}

export class Computer {
  private session: ComputerSession;

  constructor(session: ComputerSession) {
    this.session = session;
  }

  /**
   * Click mouse at specified coordinates.
   *
   * @param x - X coordinate for the click
   * @param y - Y coordinate for the click
   * @param button - Mouse button to click (default: 'left'). Valid values: 'left', 'right', 'middle', 'double_left'
   * @returns Promise resolving to result with success status
   *
   * @example
   * ```typescript
   * const agentBay = new AgentBay({ apiKey: 'your_api_key' });
   * const result = await agentBay.create({ imageId: 'windows_latest' });
   * if (result.success) {
   *   const clickResult = await result.session.computer.clickMouse(100, 100, 'left');
   *   console.log('Clicked:', clickResult.success);
   *   await result.session.delete();
   * }
   * ```
   */
  async clickMouse(x: number, y: number, button: MouseButton | string = MouseButton.LEFT): Promise<BoolResult> {
    const buttonStr = typeof button === 'string' ? button : button;
    const validButtons = Object.values(MouseButton);
    if (!validButtons.includes(buttonStr as MouseButton)) {
      throw new Error(`Invalid button '${buttonStr}'. Must be one of ${validButtons.join(', ')}`);
    }

    const args = { x, y, button: buttonStr };
    try {
      const result = await this.session.callMcpTool('click_mouse', args);
      return {
        success: result.success || false,
        requestId: result.requestId || '',
        errorMessage: result.errorMessage || '',
        data: result.success || false
      };
    } catch (error) {
      return {
        success: false,
        requestId: '',
        errorMessage: `Failed to click mouse: ${error instanceof Error ? error.message : String(error)}`,
        data: false
      };
    }
  }

  /**
   * Move mouse to specified coordinates.
   *
   * @param x - X coordinate to move to
   * @param y - Y coordinate to move to
   * @returns Promise resolving to result with success status
   *
   * @example
   * ```typescript
   * const agentBay = new AgentBay({ apiKey: process.env.AGENTBAY_API_KEY });
   * const result = await agentBay.create({ imageId: 'windows_latest' });
   * if (result.success) {
   *   await result.session.computer.moveMouse(300, 400);
   *   const pos = await result.session.computer.getCursorPosition();
   *   console.log(`Position: (${pos.x}, ${pos.y})`);
   *   await result.session.delete();
   * }
   * ```
   */
  async moveMouse(x: number, y: number): Promise<BoolResult> {
    const args = { x, y };
    try {
      const result = await this.session.callMcpTool('move_mouse', args);
      return {
        success: result.success || false,
        requestId: result.requestId || '',
        errorMessage: result.errorMessage || '',
        data: result.success || false
      };
    } catch (error) {
      return {
        success: false,
        requestId: '',
        errorMessage: `Failed to move mouse: ${error instanceof Error ? error.message : String(error)}`,
        data: false
      };
    }
  }

  /**
   * Drag mouse from one position to another.
   *
   * @param fromX - Starting X coordinate
   * @param fromY - Starting Y coordinate
   * @param toX - Ending X coordinate
   * @param toY - Ending Y coordinate
   * @param button - Mouse button to use for drag (default: 'left'). Valid values: 'left', 'right', 'middle'
   * @returns Promise resolving to result with success status
   *
   * @example
   * ```typescript
   * const agentBay = new AgentBay({ apiKey: process.env.AGENTBAY_API_KEY });
   * const result = await agentBay.create({ imageId: 'windows_latest' });
   * if (result.success) {
   *   const dragResult = await result.session.computer.dragMouse(100, 100, 300, 300, 'left');
   *   console.log('Dragged:', dragResult.success);
   *   await result.session.delete();
   * }
   * ```
   */
  async dragMouse(fromX: number, fromY: number, toX: number, toY: number, button: MouseButton | string = MouseButton.LEFT): Promise<BoolResult> {
    const buttonStr = typeof button === 'string' ? button : button;
    const validButtons = [MouseButton.LEFT, MouseButton.RIGHT, MouseButton.MIDDLE];
    if (!validButtons.includes(buttonStr as MouseButton)) {
      throw new Error(`Invalid button '${buttonStr}'. Must be one of ${validButtons.join(', ')}`);
    }

    const args = { from_x: fromX, from_y: fromY, to_x: toX, to_y: toY, button: buttonStr };
    try {
      const result = await this.session.callMcpTool('drag_mouse', args);
      return {
        success: result.success || false,
        requestId: result.requestId || '',
        errorMessage: result.errorMessage || '',
        data: result.success || false
      };
    } catch (error) {
      return {
        success: false,
        requestId: '',
        errorMessage: `Failed to drag mouse: ${error instanceof Error ? error.message : String(error)}`,
        data: false
      };
    }
  }

  /**
   * Scroll at specified coordinates.
   *
   * @param x - X coordinate to scroll at
   * @param y - Y coordinate to scroll at
   * @param direction - Scroll direction (default: 'up'). Valid values: 'up', 'down', 'left', 'right'
   * @param amount - Scroll amount (default: 1)
   * @returns Promise resolving to result with success status
   *
   * @example
   * ```typescript
   * const agentBay = new AgentBay({ apiKey: process.env.AGENTBAY_API_KEY });
   * const result = await agentBay.create({ imageId: 'windows_latest' });
   * if (result.success) {
   *   await result.session.computer.scroll(400, 300, 'up', 3);
   *   await result.session.delete();
   * }
   * ```
   */
  async scroll(x: number, y: number, direction: ScrollDirection | string = ScrollDirection.UP, amount = 1): Promise<BoolResult> {
    const directionStr = typeof direction === 'string' ? direction : direction;
    const validDirections = Object.values(ScrollDirection);
    if (!validDirections.includes(directionStr as ScrollDirection)) {
      throw new Error(`Invalid direction '${directionStr}'. Must be one of ${validDirections.join(', ')}`);
    }

    const args = { x, y, direction: directionStr, amount };
    try {
      const result = await this.session.callMcpTool('scroll', args);
      return {
        success: result.success || false,
        requestId: result.requestId || '',
        errorMessage: result.errorMessage || '',
        data: result.success || false
      };
    } catch (error) {
      return {
        success: false,
        requestId: '',
        errorMessage: `Failed to scroll: ${error instanceof Error ? error.message : String(error)}`,
        data: false
      };
    }
  }

  /**
   * Input text at the current cursor position.
   *
   * @param text - Text to input
   * @returns Promise resolving to result with success status
   *
   * @example
   * ```typescript
   * const agentBay = new AgentBay({ apiKey: process.env.AGENTBAY_API_KEY });
   * const result = await agentBay.create({ imageId: 'windows_latest' });
   * if (result.success) {
   *   await result.session.computer.inputText('Hello AgentBay!');
   *   await result.session.delete();
   * }
   * ```
   */
  async inputText(text: string): Promise<BoolResult> {
    const args = { text };
    try {
      const result = await this.session.callMcpTool('input_text', args);
      return {
        success: result.success || false,
        requestId: result.requestId || '',
        errorMessage: result.errorMessage || '',
        data: result.success || false
      };
    } catch (error) {
      return {
        success: false,
        requestId: '',
        errorMessage: `Failed to input text: ${error instanceof Error ? error.message : String(error)}`,
        data: false
      };
    }
  }

  /**
   * Press one or more keys.
   *
   * @param keys - Array of key names to press
   * @param hold - Whether to hold the keys down (default: false)
   * @returns Promise resolving to result with success status
   *
   * @example
   * ```typescript
   * const agentBay = new AgentBay({ apiKey: process.env.AGENTBAY_API_KEY });
   * const result = await agentBay.create({ imageId: 'windows_latest' });
   * if (result.success) {
   *   await result.session.computer.pressKeys(['Ctrl', 'c'], true);
   *   await result.session.computer.releaseKeys(['Ctrl', 'c']);
   *   await result.session.delete();
   * }
   * ```
   */
  async pressKeys(keys: string[], hold = false): Promise<BoolResult> {
    const args = { keys, hold };
    try {
      const result = await this.session.callMcpTool('press_keys', args);
      return {
        success: result.success || false,
        requestId: result.requestId || '',
        errorMessage: result.errorMessage || '',
        data: result.success || false
      };
    } catch (error) {
      return {
        success: false,
        requestId: '',
        errorMessage: `Failed to press keys: ${error instanceof Error ? error.message : String(error)}`,
        data: false
      };
    }
  }

  /**
   * Release previously pressed keys.
   *
   * @param keys - Array of key names to release
   * @returns Promise resolving to result with success status
   *
   * @example
   * ```typescript
   * const agentBay = new AgentBay({ apiKey: process.env.AGENTBAY_API_KEY });
   * const result = await agentBay.create({ imageId: 'windows_latest' });
   * if (result.success) {
   *   await result.session.computer.pressKeys(['Ctrl'], true);
   *   await result.session.computer.releaseKeys(['Ctrl']);
   *   await result.session.delete();
   * }
   * ```
   */
  async releaseKeys(keys: string[]): Promise<BoolResult> {
    const args = { keys };
    try {
      const result = await this.session.callMcpTool('release_keys', args);
      return {
        success: result.success || false,
        requestId: result.requestId || '',
        errorMessage: result.errorMessage || '',
        data: result.success || false
      };
    } catch (error) {
      return {
        success: false,
        requestId: '',
        errorMessage: `Failed to release keys: ${error instanceof Error ? error.message : String(error)}`,
        data: false
      };
    }
  }

  /**
   * Get cursor position.
   *
   * @returns Promise resolving to result containing cursor coordinates
   *
   * @example
   * ```typescript
   * const agentBay = new AgentBay({ apiKey: process.env.AGENTBAY_API_KEY });
   * const result = await agentBay.create({ imageId: 'windows_latest' });
   * if (result.success) {
   *   const pos = await result.session.computer.getCursorPosition();
   *   console.log(`Cursor: (${pos.x}, ${pos.y})`);
   *   await result.session.delete();
   * }
   * ```
   */
  async getCursorPosition(): Promise<CursorPosition> {
    try {
      const result = await this.session.callMcpTool('get_cursor_position', {});
      
      if (!result.success) {
        return {
          success: false,
          requestId: result.requestId || '',
          errorMessage: result.errorMessage || 'Failed to get cursor position',
          x: 0,
          y: 0
        };
      }

      // Parse JSON response from data field (callMcpTool already extracts content[0].text to data)
      const content = result.data;
      if (!content) {
        return {
          success: false,
          requestId: result.requestId || '',
          errorMessage: 'No content in response',
          x: 0,
          y: 0
        };
      }

      try {
        const position = JSON.parse(content);
        return {
          success: true,
          requestId: result.requestId || '',
          errorMessage: '',
          x: position.x || 0,
          y: position.y || 0
        };
      } catch (parseError) {
        return {
          success: false,
          requestId: result.requestId || '',
          errorMessage: `Failed to parse cursor position: ${parseError}`,
          x: 0,
          y: 0
        };
      }
    } catch (error) {
      return {
        success: false,
        requestId: '',
        errorMessage: `Failed to get cursor position: ${error instanceof Error ? error.message : String(error)}`,
        x: 0,
        y: 0
      };
    }
  }

  /**
   * Get screen size.
   *
   * @returns Promise resolving to result containing screen dimensions and DPI scaling
   *
   * @example
   * ```typescript
   * const agentBay = new AgentBay({ apiKey: process.env.AGENTBAY_API_KEY });
   * const result = await agentBay.create({ imageId: 'windows_latest' });
   * if (result.success) {
   *   const size = await result.session.computer.getScreenSize();
   *   console.log(`Screen: ${size.width}x${size.height}`);
   *   await result.session.delete();
   * }
   * ```
   */
  async getScreenSize(): Promise<ScreenSize> {
    try {
      const result = await this.session.callMcpTool('get_screen_size', {});
      
      if (!result.success) {
        return {
          success: false,
          requestId: result.requestId || '',
          errorMessage: result.errorMessage || 'Failed to get screen size',
          width: 0,
          height: 0,
          dpiScalingFactor: 1.0
        };
      }

      // Parse JSON response from data field (callMcpTool already extracts content[0].text to data)
      const content = result.data;
      if (!content) {
        return {
          success: false,
          requestId: result.requestId || '',
          errorMessage: 'No content in response',
          width: 0,
          height: 0,
          dpiScalingFactor: 1.0
        };
      }

      try {
        const screenInfo = JSON.parse(content);
        return {
          success: true,
          requestId: result.requestId || '',
          errorMessage: '',
          width: screenInfo.width || 0,
          height: screenInfo.height || 0,
          dpiScalingFactor: screenInfo.dpiScalingFactor || 1.0
        };
      } catch (parseError) {
        return {
          success: false,
          requestId: result.requestId || '',
          errorMessage: `Failed to parse screen size: ${parseError}`,
          width: 0,
          height: 0,
          dpiScalingFactor: 1.0
        };
      }
    } catch (error) {
      return {
        success: false,
        requestId: '',
        errorMessage: `Failed to get screen size: ${error instanceof Error ? error.message : String(error)}`,
        width: 0,
        height: 0,
        dpiScalingFactor: 1.0
      };
    }
  }

  /**
   * Take a screenshot.
   *
   * @returns Promise resolving to result containing screenshot URL
   *
   * @example
   * ```typescript
   * const agentBay = new AgentBay({ apiKey: process.env.AGENTBAY_API_KEY });
   * const result = await agentBay.create({ imageId: 'windows_latest' });
   * if (result.success) {
   *   const screenshot = await result.session.computer.screenshot();
   *   console.log('Screenshot URL:', screenshot.data);
   *   await result.session.delete();
   * }
   * ```
   */
  async screenshot(): Promise<ScreenshotResult> {
    try {
      const result = await this.session.callMcpTool('system_screenshot', {});
      
      if (!result.success) {
        return {
          success: false,
          requestId: result.requestId || '',
          errorMessage: result.errorMessage || 'Failed to take screenshot',
          data: ''
        };
      }

      const screenshotUrl = result.content?.[0]?.text || '';
      return {
        success: true,
        requestId: result.requestId || '',
        errorMessage: '',
        data: screenshotUrl
      };
    } catch (error) {
      return {
        success: false,
        requestId: '',
        errorMessage: `Failed to take screenshot: ${error instanceof Error ? error.message : String(error)}`,
        data: ''
      };
    }
  }

  /**
   * Lists all root windows.
   *
   * @param timeoutMs - Timeout in milliseconds (default: 3000)
   * @returns Promise resolving to result containing array of root windows
   *
   * @example
   * ```typescript
   * const agentBay = new AgentBay({ apiKey: process.env.AGENTBAY_API_KEY });
   * const result = await agentBay.create({ imageId: 'windows_latest' });
   * if (result.success) {
   *   const windows = await result.session.computer.listRootWindows();
   *   console.log(`Found ${windows.windows.length} windows`);
   *   await result.session.delete();
   * }
   * ```
   */
  async listRootWindows(timeoutMs = 3000): Promise<WindowListResult> {
    try {
      const args = { timeout_ms: timeoutMs };
      const response = await this.session.callMcpTool('list_root_windows', args);

      if (!response.success) {
        return {
          requestId: response.requestId,
          success: false,
          windows: [],
          errorMessage: response.errorMessage,
        };
      }

      const rawWindows = response.data ? JSON.parse(response.data) : [];
      
      // Convert snake_case fields to camelCase to match Go SDK behavior
      const windows = convertWindowList(rawWindows);
      logInfo('listRootWindows', `Windows: ${JSON.stringify(windows)}`);
      return {
        requestId: response.requestId,
        success: true,
        windows,
      };
    } catch (error) {
      return {
        requestId: '',
        success: false,
        windows: [],
        errorMessage: `Failed to list root windows: ${error}`,
      };
    }
  }

  /**
   * Gets the currently active window.
   *
   * @param timeoutMs - Timeout in milliseconds (default: 3000)
   * @returns Promise resolving to result containing active window information
   *
   * @example
   * ```typescript
   * const agentBay = new AgentBay({ apiKey: process.env.AGENTBAY_API_KEY });
   * const result = await agentBay.create({ imageId: 'windows_latest' });
   * if (result.success) {
   *   const activeWindow = await result.session.computer.getActiveWindow();
   *   console.log(`Active: ${activeWindow.window?.title}`);
   *   await result.session.delete();
   * }
   * ```
   */
  async getActiveWindow(): Promise<WindowInfoResult> {
    try {
      const args = {};
      const response = await this.session.callMcpTool('get_active_window', args);

      if (!response.success) {
        return {
          requestId: response.requestId,
          success: false,
          window: null,
          errorMessage: response.errorMessage,
        };
      }

      const rawWindow = response.data ? JSON.parse(response.data) : null;
      
      // Convert snake_case fields to camelCase to match Go SDK behavior
      const window = convertWindowData(rawWindow);
      logInfo('getActiveWindow', `Window: ${JSON.stringify(window)}`);
      return {
        requestId: response.requestId,
        success: true,
        window,
      };
    } catch (error) {
      return {
        requestId: '',
        success: false,
        window: null,
        errorMessage: `Failed to get active window: ${error}`,
      };
    }
  }

  /**
   * Activates the specified window.
   *
   * @param windowId - ID of the window to activate
   * @returns Promise resolving to result with success status
   *
   * @example
   * ```typescript
   * const agentBay = new AgentBay({ apiKey: 'your_api_key' });
   * const result = await agentBay.create({ imageId: 'windows_latest' });
   * if (result.success) {
   *   const windows = await result.session.computer.listRootWindows();
   *   await result.session.computer.activateWindow(windows.windows[0].id);
   *   await result.session.delete();
   * }
   * ```
   */
  async activateWindow(windowId: number): Promise<WindowBoolResult> {
    try {
      const args = { window_id: windowId };
      const response = await this.session.callMcpTool('activate_window', args);

      return {
        requestId: response.requestId,
        success: response.success,
        errorMessage: response.errorMessage || '',
      };
    } catch (error) {
      return {
        requestId: '',
        success: false,
        errorMessage: `Failed to activate window: ${error}`,
      };
    }
  }

  /**
   * Closes the specified window.
   *
   * @param windowId - ID of the window to close
   * @returns Promise resolving to result with success status
   *
   * @example
   * ```typescript
   * const agentBay = new AgentBay({ apiKey: process.env.AGENTBAY_API_KEY });
   * const result = await agentBay.create({ imageId: 'windows_latest' });
   * if (result.success) {
   *   await result.session.computer.startApp('notepad.exe');
   *   const win = await result.session.computer.getActiveWindow();
   *   await result.session.computer.closeWindow(win.window!.id);
   *   await result.session.delete();
   * }
   * ```
   */
  async closeWindow(windowId: number): Promise<WindowBoolResult> {
    try {
      const args = { window_id: windowId };
      const response = await this.session.callMcpTool('close_window', args);

      return {
        requestId: response.requestId,
        success: response.success,
        errorMessage: response.errorMessage || '',
      };
    } catch (error) {
      return {
        requestId: '',
        success: false,
        errorMessage: `Failed to close window: ${error}`,
      };
    }
  }

  /**
   * Maximizes the specified window.
   *
   * @param windowId - ID of the window to maximize
   * @returns Promise resolving to result with success status
   *
   * @example
   * ```typescript
   * const agentBay = new AgentBay({ apiKey: process.env.AGENTBAY_API_KEY });
   * const result = await agentBay.create({ imageId: 'windows_latest' });
   * if (result.success) {
   *   await result.session.computer.startApp('notepad.exe');
   *   const win = await result.session.computer.getActiveWindow();
   *   await result.session.computer.maximizeWindow(win.window!.id);
   *   await result.session.delete();
   * }
   * ```
   */
  async maximizeWindow(windowId: number): Promise<WindowBoolResult> {
    try {
      const args = { window_id: windowId };
      const response = await this.session.callMcpTool('maximize_window', args);

      return {
        requestId: response.requestId,
        success: response.success,
        errorMessage: response.errorMessage || '',
      };
    } catch (error) {
      return {
        requestId: '',
        success: false,
        errorMessage: `Failed to maximize window: ${error}`,
      };
    }
  }

  /**
   * Minimizes the specified window.
   *
   * @param windowId - ID of the window to minimize
   * @returns Promise resolving to result with success status
   *
   * @example
   * ```typescript
   * const agentBay = new AgentBay({ apiKey: process.env.AGENTBAY_API_KEY });
   * const result = await agentBay.create({ imageId: 'windows_latest' });
   * if (result.success) {
   *   await result.session.computer.startApp('notepad.exe');
   *   const win = await result.session.computer.getActiveWindow();
   *   await result.session.computer.minimizeWindow(win.window!.id);
   *   await result.session.delete();
   * }
   * ```
   */
  async minimizeWindow(windowId: number): Promise<WindowBoolResult> {
    try {
      const args = { window_id: windowId };
      const response = await this.session.callMcpTool('minimize_window', args);

      return {
        requestId: response.requestId,
        success: response.success,
        errorMessage: response.errorMessage || '',
      };
    } catch (error) {
      return {
        requestId: '',
        success: false,
        errorMessage: `Failed to minimize window: ${error}`,
      };
    }
  }

  /**
   * Restores the specified window.
   *
   * @param windowId - ID of the window to restore
   * @returns Promise resolving to result with success status
   *
   * @example
   * ```typescript
   * const agentBay = new AgentBay({ apiKey: process.env.AGENTBAY_API_KEY });
   * const result = await agentBay.create({ imageId: 'windows_latest' });
   * if (result.success) {
   *   await result.session.computer.startApp('notepad.exe');
   *   const win = await result.session.computer.getActiveWindow();
   *   await result.session.computer.minimizeWindow(win.window!.id);
   *   await result.session.computer.restoreWindow(win.window!.id);
   *   await result.session.delete();
   * }
   * ```
   */
  async restoreWindow(windowId: number): Promise<WindowBoolResult> {
    try {
      const args = { window_id: windowId };
      const response = await this.session.callMcpTool('restore_window', args);

      return {
        requestId: response.requestId,
        success: response.success,
        errorMessage: response.errorMessage || '',
      };
    } catch (error) {
      return {
        requestId: '',
        success: false,
        errorMessage: `Failed to restore window: ${error}`,
      };
    }
  }

  /**
   * Resizes the specified window.
   *
   * @param windowId - ID of the window to resize
   * @param width - New width of the window
   * @param height - New height of the window
   * @returns Promise resolving to result with success status
   *
   * @example
   * ```typescript
   * const agentBay = new AgentBay({ apiKey: process.env.AGENTBAY_API_KEY });
   * const result = await agentBay.create({ imageId: 'windows_latest' });
   * if (result.success) {
   *   await result.session.computer.startApp('notepad.exe');
   *   const win = await result.session.computer.getActiveWindow();
   *   await result.session.computer.resizeWindow(win.window!.id, 800, 600);
   *   await result.session.delete();
   * }
   * ```
   */
  async resizeWindow(windowId: number, width: number, height: number): Promise<WindowBoolResult> {
    try {
      const args = { window_id: windowId, width, height };
      const response = await this.session.callMcpTool('resize_window', args);

      return {
        requestId: response.requestId,
        success: response.success,
        errorMessage: response.errorMessage || '',
      };
    } catch (error) {
      return {
        requestId: '',
        success: false,
        errorMessage: `Failed to resize window: ${error}`,
      };
    }
  }

  /**
   * Makes the specified window fullscreen.
   *
   * @param windowId - ID of the window to make fullscreen
   * @returns Promise resolving to result with success status
   *
   * @example
   * ```typescript
   * const agentBay = new AgentBay({ apiKey: process.env.AGENTBAY_API_KEY });
   * const result = await agentBay.create({ imageId: 'windows_latest' });
   * if (result.success) {
   *   await result.session.computer.startApp('notepad.exe');
   *   const win = await result.session.computer.getActiveWindow();
   *   await result.session.computer.fullscreenWindow(win.window!.id);
   *   await result.session.delete();
   * }
   * ```
   */
  async fullscreenWindow(windowId: number): Promise<WindowBoolResult> {
    try {
      const args = { window_id: windowId };
      const response = await this.session.callMcpTool('fullscreen_window', args);

      return {
        requestId: response.requestId,
        success: response.success,
        errorMessage: response.errorMessage || '',
      };
    } catch (error) {
      return {
        requestId: '',
        success: false,
        errorMessage: `Failed to make window fullscreen: ${error}`,
      };
    }
  }

  /**
   * Toggles focus mode on or off.
   *
   * @param on - Whether to enable (true) or disable (false) focus mode
   * @returns Promise resolving to result with success status
   *
   * @example
   * ```typescript
   * const agentBay = new AgentBay({ apiKey: process.env.AGENTBAY_API_KEY });
   * const result = await agentBay.create({ imageId: 'windows_latest' });
   * if (result.success) {
   *   await result.session.computer.focusMode(true);
   *   await result.session.computer.focusMode(false);
   *   await result.session.delete();
   * }
   * ```
   */
  async focusMode(on: boolean): Promise<WindowBoolResult> {
    try {
      const args = { on };
      const response = await this.session.callMcpTool('focus_mode', args);

      return {
        requestId: response.requestId,
        success: response.success,
        errorMessage: response.errorMessage || '',
      };
    } catch (error) {
      return {
        requestId: '',
        success: false,
        errorMessage: `Failed to toggle focus mode: ${error}`,
      };
    }
  }

  // Application Management Operations

  /**
   * Gets the list of installed applications.
   *
   * @param startMenu - Whether to include applications from start menu (default: true)
   * @param desktop - Whether to include applications from desktop (default: false)
   * @param ignoreSystemApps - Whether to exclude system applications (default: true)
   * @returns Promise resolving to result containing array of installed applications
   *
   * @example
   * ```typescript
   * const agentBay = new AgentBay({ apiKey: 'your_api_key' });
   * const result = await agentBay.create({ imageId: 'windows_latest' });
   * if (result.success) {
   *   const apps = await result.session.computer.getInstalledApps();
   *   console.log(`Found ${apps.data.length} apps`);
   *   await result.session.delete();
   * }
   * ```
   */
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  async getInstalledApps(startMenu = true, desktop = false, ignoreSystemApps = true): Promise<any> {
    try {
      const args = {
        start_menu: startMenu,
        desktop,
        ignore_system_apps: ignoreSystemApps,
      };

      const response = await this.session.callMcpTool('get_installed_apps', args);

      if (!response.success) {
        return {
          requestId: response.requestId,
          success: false,
          data: [],
          errorMessage: response.errorMessage,
        };
      }

      const rawApps = response.data ? JSON.parse(response.data) : [];
      const apps = convertObjectKeys(rawApps);
      logInfo('Found %d new apps', apps);
      return {
        requestId: response.requestId,
        success: true,
        data: apps,
      };
    } catch (error) {
      return {
        requestId: '',
        success: false,
        data: [],
        errorMessage: `Failed to get installed apps: ${error}`,
      };
    }
  }

  /**
   * Starts the specified application.
   *
   * @param startCmd - The command to start the application (e.g., 'notepad.exe', 'calculator:')
   * @param workDirectory - The working directory for the application (optional)
   * @param activity - The activity parameter (optional, primarily for mobile use)
   * @returns Promise resolving to result containing array of started processes
   *
   * @example
   * ```typescript
   * const agentBay = new AgentBay({ apiKey: 'your_api_key' });
   * const result = await agentBay.create({ imageId: 'windows_latest' });
   * if (result.success) {
   *   const startResult = await result.session.computer.startApp('notepad.exe');
   *   console.log(`Started ${startResult.data.length} process(es)`);
   *   await result.session.delete();
   * }
   * ```
   */
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  async startApp(startCmd: string, workDirectory = "", activity = ""): Promise<any> {
    try {
      const args: Record<string, string> = { start_cmd: startCmd };
      if (workDirectory) args.work_directory = workDirectory;
      if (activity) args.activity = activity;

      const response = await this.session.callMcpTool('start_app', args);

      if (!response.success) {
        return {
          requestId: response.requestId,
          success: false,
          data: [],
          errorMessage: response.errorMessage,
        };
      }

      const rawProcesses = response.data ? JSON.parse(response.data) : [];
      const processes = convertObjectKeys(rawProcesses);
      logInfo('Found %d processes', processes);
      return {
        requestId: response.requestId,
        success: true,
        data: processes,
      };
    } catch (error) {
      return {
        requestId: '',
        success: false,
        data: [],
        errorMessage: `Failed to start app: ${error}`,
      };
    }
  }

  /**
   * Stops an application by process name.
   *
   * @param pname - The process name to stop (e.g., 'notepad.exe', 'chrome.exe')
   * @returns Promise resolving to result with success status
   *
   * @example
   * ```typescript
   * const agentBay = new AgentBay({ apiKey: 'your_api_key' });
   * const result = await agentBay.create({ imageId: 'windows_latest' });
   * if (result.success) {
   *   await result.session.computer.startApp('notepad.exe');
   *   await result.session.computer.stopAppByPName('notepad.exe');
   *   await result.session.delete();
   * }
   * ```
   */
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  async stopAppByPName(pname: string): Promise<any> {
    try {
      const args = { pname };
      const response = await this.session.callMcpTool('stop_app_by_pname', args);

      return {
        requestId: response.requestId,
        success: response.success,
        errorMessage: response.errorMessage || '',
      };
    } catch (error) {
      return {
        requestId: '',
        success: false,
        errorMessage: `Failed to stop app by pname: ${error}`,
      };
    }
  }

  /**
   * Stops an application by process ID.
   *
   * @param pid - The process ID to stop
   * @returns Promise resolving to result with success status
   *
   * @example
   * ```typescript
   * const agentBay = new AgentBay({ apiKey: 'your_api_key' });
   * const result = await agentBay.create({ imageId: 'windows_latest' });
   * if (result.success) {
   *   const startResult = await result.session.computer.startApp('notepad.exe');
   *   const pid = startResult.data[0].pid;
   *   await result.session.computer.stopAppByPID(pid);
   *   await result.session.delete();
   * }
   * ```
   */
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  async stopAppByPID(pid: number): Promise<any> {
    try {
      const args = { pid };
      const response = await this.session.callMcpTool('stop_app_by_pid', args);

      return {
        requestId: response.requestId,
        success: response.success,
        errorMessage: response.errorMessage || '',
      };
    } catch (error) {
      return {
        requestId: '',
        success: false,
        errorMessage: `Failed to stop app by pid: ${error}`,
      };
    }
  }

  /**
   * Stops an application by stop command.
   *
   * @param cmd - The command to stop the application
   * @returns Promise resolving to result with success status
   *
   * @example
   * ```typescript
   * const agentBay = new AgentBay({ apiKey: 'your_api_key' });
   * const result = await agentBay.create({ imageId: 'windows_latest' });
   * if (result.success) {
   *   await result.session.computer.startApp('notepad.exe');
   *   await result.session.computer.stopAppByCmd('taskkill /IM notepad.exe /F');
   *   await result.session.delete();
   * }
   * ```
   */
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  async stopAppByCmd(cmd: string): Promise<any> {
    try {
      const args = { stop_cmd: cmd };
      const response = await this.session.callMcpTool('stop_app_by_cmd', args);

      return {
        requestId: response.requestId,
        success: response.success,
        errorMessage: response.errorMessage || '',
      };
    } catch (error) {
      return {
        requestId: '',
        success: false,
        errorMessage: `Failed to stop app by cmd: ${error}`,
      };
    }
  }

  /**
   * Lists all visible applications.
   *
   * @returns Promise resolving to result containing array of visible application processes
   *
   * @example
   * ```typescript
   * const agentBay = new AgentBay({ apiKey: 'your_api_key' });
   * const result = await agentBay.create({ imageId: 'windows_latest' });
   * if (result.success) {
   *   const apps = await result.session.computer.listVisibleApps();
   *   console.log(`Found ${apps.data.length} visible apps`);
   *   await result.session.delete();
   * }
   * ```
   */
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  async listVisibleApps(): Promise<any> {
    try {
      const response = await this.session.callMcpTool('list_visible_apps', {});

      if (!response.success) {
        return {
          requestId: response.requestId,
          success: false,
          data: [],
          errorMessage: response.errorMessage,
        };
      }

      const rawProcesses = response.data ? JSON.parse(response.data) : [];
      const processes = convertObjectKeys(rawProcesses);
      logInfo('Found %d processes', processes);
      return {
        requestId: response.requestId,
        success: true,
        data: processes,
      };
    } catch (error) {
      return {
        requestId: '',
        success: false,
        data: [],
        errorMessage: `Failed to list visible apps: ${error}`,
      };
    }
  }
} 