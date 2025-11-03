/**
 * Mobile module for mobile UI automation.
 * Provides touch, input, and app management operations for mobile environments.
 */

import { OperationResult } from "../types/api-response";
import { MobileExtraConfig } from "../types/extra-configs";
import { log, logError } from "../utils/logger";
import { getMobileCommandTemplate, replaceTemplatePlaceholders } from "../command/command-templates";

export interface BoolResult extends OperationResult {
  data?: boolean;
}

export interface UIBounds {
  left: number;
  top: number;
  right: number;
  bottom: number;
}

export interface UIElement {
  text: string;
  className: string;
  bounds: UIBounds | string;  // Can be either object or string format "left,top,right,bottom"
}

export interface UIElementsResult extends OperationResult {
  elements: UIElement[];
}

export interface InstalledApp {
  name: string;
  startCmd: string;
  workDirectory: string;
}

export interface InstalledAppsResult extends OperationResult {
  apps: InstalledApp[];
}

export interface Process {
  pid: number;
  pname: string;
}

export interface ProcessResult extends OperationResult {
  processes: Process[];
}

export interface ScreenshotResult extends OperationResult {
  data: string; // Screenshot URL
}

export interface AdbUrlResult extends OperationResult {
  data?: string; // ADB connection URL (e.g., "adb connect xx.xx.xx.xx:xxxxx")
  url?: string; // Alternative field name for compatibility
}

// Session interface for Mobile module
interface MobileSession {
  callMcpTool(toolName: string, args: Record<string, any>): Promise<any>;
  sessionId: string;
  getAPIKey(): string;
  imageId?: string;
  getLink(protocolType?: string, port?: number, options?: string): Promise<any>;
}

/**
 * Parse bounds string format "left,top,right,bottom" to UIBounds object
 */
function parseBoundsString(boundsStr: string): UIBounds | null {
  const parts = boundsStr.split(',');
  if (parts.length !== 4) {
    return null;
  }

  const [left, top, right, bottom] = parts.map(p => parseInt(p.trim(), 10));
  if (isNaN(left) || isNaN(top) || isNaN(right) || isNaN(bottom)) {
    return null;
  }

  return { left, top, right, bottom };
}

/**
 * Normalize UIElement bounds field from string to object format if needed
 */
function normalizeUIElement(element: any): UIElement {
  if (element.bounds && typeof element.bounds === 'string') {
    const parsedBounds = parseBoundsString(element.bounds);
    if (parsedBounds) {
      element.bounds = parsedBounds;
    }
  }

  // Recursively normalize children if present
  if (element.children && Array.isArray(element.children)) {
    element.children = element.children.map(normalizeUIElement);
  }

  return element;
}

export class Mobile {
  private session: MobileSession;

  constructor(session: MobileSession) {
    this.session = session;
  }


  /**
   * Tap at specified coordinates.
   */
  async tap(x: number, y: number): Promise<BoolResult> {
    const args = { x, y };
    try {
      const result = await this.session.callMcpTool('tap', args);
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
        errorMessage: `Failed to tap: ${error instanceof Error ? error.message : String(error)}`,
        data: false
      };
    }
  }

  /**
   * Swipe from one position to another.
   */
  async swipe(startX: number, startY: number, endX: number, endY: number, durationMs = 300): Promise<BoolResult> {
    const args = { start_x: startX, start_y: startY, end_x: endX, end_y: endY, duration_ms: durationMs };
    try {
      const result = await this.session.callMcpTool('swipe', args);
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
        errorMessage: `Failed to swipe: ${error instanceof Error ? error.message : String(error)}`,
        data: false
      };
    }
  }

  /**
   * Input text.
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
   * Send Android key code.
   */
  async sendKey(key: number): Promise<BoolResult> {
    const args = { key };
    try {
      const result = await this.session.callMcpTool('send_key', args);
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
        errorMessage: `Failed to send key: ${error instanceof Error ? error.message : String(error)}`,
        data: false
      };
    }
  }

  /**
   * Get clickable UI elements.
   */
  async getClickableUIElements(timeoutMs = 5000): Promise<UIElementsResult> {
    const args = { timeout_ms: timeoutMs };
    try {
      const result = await this.session.callMcpTool('get_clickable_ui_elements', args);

      if (!result.success) {
        return {
          success: false,
          requestId: result.requestId || '',
          errorMessage: result.errorMessage || 'Failed to get clickable UI elements',
          elements: []
        };
      }

      if (!result.data) {
        return {
          success: true,
          requestId: result.requestId || '',
          errorMessage: '',
          elements: []
        };
      }

      try {
        const elements = JSON.parse(result.data);
        // Normalize bounds from string to object format if needed
        const normalizedElements = (elements || []).map(normalizeUIElement);
        return {
          success: true,
          requestId: result.requestId || '',
          errorMessage: '',
          elements: normalizedElements
        };
      } catch (parseError) {
        return {
          success: false,
          requestId: result.requestId || '',
          errorMessage: `Failed to parse UI elements: ${parseError}`,
          elements: []
        };
      }
    } catch (error) {
      return {
        success: false,
        requestId: '',
        errorMessage: `Failed to get clickable UI elements: ${error instanceof Error ? error.message : String(error)}`,
        elements: []
      };
    }
  }

  /**
   * Get all UI elements.
   */
  async getAllUIElements(timeoutMs = 3000): Promise<UIElementsResult> {
    const args = { timeout_ms: timeoutMs };
    try {
      const result = await this.session.callMcpTool('get_all_ui_elements', args);

      if (!result.success) {
        return {
          success: false,
          requestId: result.requestId || '',
          errorMessage: result.errorMessage || 'Failed to get all UI elements',
          elements: []
        };
      }

      if (!result.data) {
        return {
          success: true,
          requestId: result.requestId || '',
          errorMessage: '',
          elements: []
        };
      }

      try {
        const elements = JSON.parse(result.data);
        // Normalize bounds from string to object format if needed
        const normalizedElements = (elements || []).map(normalizeUIElement);
        return {
          success: true,
          requestId: result.requestId || '',
          errorMessage: '',
          elements: normalizedElements
        };
      } catch (parseError) {
        return {
          success: false,
          requestId: result.requestId || '',
          errorMessage: `Failed to parse UI elements: ${parseError}`,
          elements: []
        };
      }
    } catch (error) {
      return {
        success: false,
        requestId: '',
        errorMessage: `Failed to get all UI elements: ${error instanceof Error ? error.message : String(error)}`,
        elements: []
      };
    }
  }

  /**
   * Get installed apps.
   */
  async getInstalledApps(startMenu = false, desktop = true, ignoreSystemApps = true): Promise<InstalledAppsResult> {
    const args = { start_menu: startMenu, desktop, ignore_system_apps: ignoreSystemApps };
    try {
      const result = await this.session.callMcpTool('get_installed_apps', args);
      
      if (!result.success) {
        return {
          success: false,
          requestId: result.requestId || '',
          errorMessage: result.errorMessage || 'Failed to get installed apps',
          apps: []
        };
      }

      if (!result.data) {
        return {
          success: true,
          requestId: result.requestId || '',
          errorMessage: '',
          apps: []
        };
      }

      try {
        const apps = JSON.parse(result.data);
        return {
          success: true,
          requestId: result.requestId || '',
          errorMessage: '',
          apps: apps || []
        };
      } catch (parseError) {
        return {
          success: false,
          requestId: result.requestId || '',
          errorMessage: `Failed to parse installed apps: ${parseError}`,
          apps: []
        };
      }
    } catch (error) {
      return {
        success: false,
        requestId: '',
        errorMessage: `Failed to get installed apps: ${error instanceof Error ? error.message : String(error)}`,
        apps: []
      };
    }
  }

  /**
   * Start an app.
   */
  async startApp(startCmd: string, workDirectory = '', activity = ''): Promise<ProcessResult> {
    const args = { start_cmd: startCmd, work_directory: workDirectory, activity };
    try {
      const result = await this.session.callMcpTool('start_app', args);
      
      if (!result.success) {
        return {
          success: false,
          requestId: result.requestId || '',
          errorMessage: result.errorMessage || 'Failed to start app',
          processes: []
        };
      }

      if (!result.data) {
        return {
          success: true,
          requestId: result.requestId || '',
          errorMessage: '',
          processes: []
        };
      }

      try {
        const processes = JSON.parse(result.data);
        return {
          success: true,
          requestId: result.requestId || '',
          errorMessage: '',
          processes: processes || []
        };
      } catch (parseError) {
        return {
          success: false,
          requestId: result.requestId || '',
          errorMessage: `Failed to parse process result: ${parseError}`,
          processes: []
        };
      }
    } catch (error) {
      return {
        success: false,
        requestId: '',
        errorMessage: `Failed to start app: ${error instanceof Error ? error.message : String(error)}`,
        processes: []
      };
    }
  }

  /**
   * Stop app by package name.
   */
  async stopAppByPName(pname: string): Promise<BoolResult> {
    const args = { pname };
    try {
      const result = await this.session.callMcpTool('stop_app_by_pname', args);
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
        errorMessage: `Failed to stop app: ${error instanceof Error ? error.message : String(error)}`,
        data: false
      };
    }
  }

  /**
   * Take a screenshot.
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

      return {
        success: true,
        requestId: result.requestId || '',
        errorMessage: '',
        data: result.data || ''
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
   * Retrieves the ADB connection URL for the mobile environment.
   * This method is only supported in mobile environments (mobile_latest image).
   * It uses the provided ADB public key to establish the connection and returns
   * the ADB connect URL.
   * 
   * @param adbkeyPub - ADB public key for authentication
   * @returns AdbUrlResult containing the ADB connection URL
   */
  async getAdbUrl(adbkeyPub: string): Promise<AdbUrlResult> {
    try {
      // Build options JSON with adbkey_pub
      const optionsJson = JSON.stringify({ adbkey_pub: adbkeyPub });

      // Call getLink with protocol_type="adb" and options
      const result = await this.session.getLink('adb', undefined, optionsJson);

      return {
        success: result.success || false,
        requestId: result.requestId || '',
        errorMessage: result.errorMessage || '',
        data: result.data,
        url: result.data
      };
    } catch (error) {
      const errorMsg = `Failed to get ADB URL: ${error instanceof Error ? error.message : String(error)}`;
      return {
        success: false,
        requestId: '',
        errorMessage: errorMsg,
        data: undefined,
        url: undefined
      };
    }
  }

  /**
   * Configure mobile device settings based on MobileExtraConfig.
   * This method applies various mobile configuration settings including
   * resolution lock and app access management.
   * 
   * @param config - The mobile configuration to apply
   * @returns OperationResult indicating success or failure
   */
  async configure(config: MobileExtraConfig): Promise<OperationResult> {
    try {
      if (!config) {
        return {
          success: false,
          requestId: '',
          errorMessage: 'No mobile configuration provided'
        };
      }

      // Configure resolution lock
      const resolutionResult = await this.setResolutionLock(config.lockResolution);
      if (!resolutionResult.success) {
        return {
          success: false,
          requestId: resolutionResult.requestId,
          errorMessage: `Failed to set resolution lock: ${resolutionResult.errorMessage}`
        };
      }

      // Configure app management rules
      if (config.appManagerRule && config.appManagerRule.ruleType) {
        const appRule = config.appManagerRule;
        const packageNames = appRule.appPackageNameList;

        if (packageNames && packageNames.length > 0 && 
            (appRule.ruleType === "White" || appRule.ruleType === "Black")) {
          
          let appResult: OperationResult;
          if (appRule.ruleType === "White") {
            appResult = await this.setAppWhitelist(packageNames);
          } else {
            appResult = await this.setAppBlacklist(packageNames);
          }

          if (!appResult.success) {
            return {
              success: false,
              requestId: appResult.requestId,
              errorMessage: `Failed to set app ${appRule.ruleType.toLowerCase()}list: ${appResult.errorMessage}`
            };
          }
        } else if (packageNames && packageNames.length === 0) {
          return {
            success: false,
            requestId: '',
            errorMessage: `No package names provided for ${appRule.ruleType} list`
          };
        }
      }

      // Configure navigation bar visibility
      if (config.hideNavigationBar !== undefined) {
        const navResult = await this.setNavigationBarVisibility(config.hideNavigationBar);
        if (!navResult.success) {
          return {
            success: false,
            requestId: navResult.requestId,
            errorMessage: `Failed to set navigation bar visibility: ${navResult.errorMessage}`
          };
        }
      }

      // Configure uninstall blacklist
      if (config.uninstallBlacklist && config.uninstallBlacklist.length > 0) {
        const uninstallResult = await this.setUninstallBlacklist(config.uninstallBlacklist);
        if (!uninstallResult.success) {
          return {
            success: false,
            requestId: uninstallResult.requestId,
            errorMessage: `Failed to set uninstall blacklist: ${uninstallResult.errorMessage}`
          };
        }
      }

      log("Mobile configuration applied successfully");
      return {
        success: true,
        requestId: '',
        errorMessage: ''
      };
    } catch (error) {
      const errorMsg = `Failed to configure mobile: ${error instanceof Error ? error.message : String(error)}`;
      logError(errorMsg);
      return {
        success: false,
        requestId: '',
        errorMessage: errorMsg
      };
    }
  }

  /**
   * Set display resolution lock for mobile devices.
   * 
   * @param enable - Whether to enable resolution lock
   * @returns OperationResult indicating success or failure
   */
  async setResolutionLock(enable: boolean): Promise<OperationResult> {
    try {
      const templateName = enable ? "resolution_lock_enable" : "resolution_lock_disable";
      const template = getMobileCommandTemplate(templateName);
      
      if (!template) {
        return {
          success: false,
          requestId: '',
          errorMessage: `Resolution lock template not found: ${templateName}`
        };
      }

      const description = `Resolution lock ${enable ? 'enable' : 'disable'}`;
      return await this.executeCommand(template, description);
    } catch (error) {
      return {
        success: false,
        requestId: '',
        errorMessage: `Failed to set resolution lock: ${error instanceof Error ? error.message : String(error)}`
      };
    }
  }

  /**
   * Set app whitelist configuration.
   * 
   * @param packageNames - List of package names to whitelist
   * @returns OperationResult indicating success or failure
   */
  async setAppWhitelist(packageNames: string[]): Promise<OperationResult> {
    try {
      const template = getMobileCommandTemplate("app_whitelist");
      if (!template) {
        return {
          success: false,
          requestId: '',
          errorMessage: "App whitelist template not found"
        };
      }

      // Replace placeholder with actual package names (newline-separated for file content)
      const packageList = packageNames.join('\n');
      const command = replaceTemplatePlaceholders(template, { package_list: packageList });
      
      const description = `App whitelist configuration (${packageNames.length} packages)`;
      return await this.executeCommand(command, description);
    } catch (error) {
      return {
        success: false,
        requestId: '',
        errorMessage: `Failed to set app whitelist: ${error instanceof Error ? error.message : String(error)}`
      };
    }
  }

  /**
   * Set app blacklist configuration.
   * 
   * @param packageNames - List of package names to blacklist
   * @returns OperationResult indicating success or failure
   */
  async setAppBlacklist(packageNames: string[]): Promise<OperationResult> {
    try {
      const template = getMobileCommandTemplate("app_blacklist");
      if (!template) {
        return {
          success: false,
          requestId: '',
          errorMessage: "App blacklist template not found"
        };
      }

      // Replace placeholder with actual package names (newline-separated for file content)
      const packageList = packageNames.join('\n');
      const command = replaceTemplatePlaceholders(template, { package_list: packageList });
      
      const description = `App blacklist configuration (${packageNames.length} packages)`;
      return await this.executeCommand(command, description);
    } catch (error) {
      return {
        success: false,
        requestId: '',
        errorMessage: `Failed to set app blacklist: ${error instanceof Error ? error.message : String(error)}`
      };
    }
  }

  /**
   * Set navigation bar visibility for mobile devices.
   * 
   * @param hide - True to hide navigation bar, false to show navigation bar
   * @returns OperationResult indicating success or failure
   */
  async setNavigationBarVisibility(hide: boolean): Promise<OperationResult> {
    try {
      const templateName = hide ? "hide_navigation_bar" : "show_navigation_bar";
      const template = getMobileCommandTemplate(templateName);
      
      if (!template) {
        return {
          success: false,
          requestId: '',
          errorMessage: `Navigation bar template not found: ${templateName}`
        };
      }

      const description = `Navigation bar visibility (hide: ${hide})`;
      return await this.executeCommand(template, description);
    } catch (error) {
      return {
        success: false,
        requestId: '',
        errorMessage: `Failed to set navigation bar visibility: ${error instanceof Error ? error.message : String(error)}`
      };
    }
  }

  /**
   * Set uninstall protection blacklist for mobile devices.
   * 
   * @param packageNames - List of Android package names to protect from uninstallation
   * @returns OperationResult indicating success or failure
   */
  async setUninstallBlacklist(packageNames: string[]): Promise<OperationResult> {
    try {
      const template = getMobileCommandTemplate("uninstall_blacklist");
      if (!template) {
        return {
          success: false,
          requestId: '',
          errorMessage: "Uninstall blacklist template not found"
        };
      }

      // Use semicolon-separated format for uninstall blacklist property
      const packageList = packageNames.join(';');
      const command = replaceTemplatePlaceholders(template, { package_list: packageList });
      
      const description = `Uninstall blacklist configuration (${packageNames.length} packages)`;
      return await this.executeCommand(command, description);
    } catch (error) {
      return {
        success: false,
        requestId: '',
        errorMessage: `Failed to set uninstall blacklist: ${error instanceof Error ? error.message : String(error)}`
      };
    }
  }

  /**
   * Execute a command template for mobile configuration.
   * 
   * @param command - The command to execute
   * @param description - Description of the operation
   * @returns OperationResult indicating success or failure
   */
  private async executeCommand(command: string, description: string): Promise<OperationResult> {
    try {
      log(`Executing ${description}`);
      
      // Use the session's command module to execute the command with longer timeout for mobile operations
      const result = await (this.session as any).command.executeCommand(command, 10000);
      
      if (result && result.success) {
        log(`✅ ${description} completed successfully`);
        if (result.output) {
          log(`Command output: ${result.output}`);
        }
        return {
          success: true,
          requestId: result.requestId || '',
          errorMessage: ''
        };
      } else {
        const errorMessage = result?.errorMessage || `Failed to execute ${description}`;
        logError(`Failed to execute ${description}: ${errorMessage}`);
        return {
          success: false,
          requestId: result?.requestId || '',
          errorMessage: errorMessage
        };
      }
    } catch (error) {
      const errorMsg = `Failed to execute ${description}: ${error instanceof Error ? error.message : String(error)}`;
      logError(errorMsg);
      return {
        success: false,
        requestId: '',
        errorMessage: errorMsg
      };
    }
  }
} 