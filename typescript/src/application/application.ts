import { Client } from "../api/client";
import {
  InstalledAppListResult,
  ProcessListResult,
  AppOperationResult,
} from "../types/api-response";


/**
 * Represents an installed application
 */
export interface InstalledApp {
  name: string;
  start_cmd: string;
  stop_cmd?: string;
  work_directory?: string;
}

/**
 * Represents a running process
 */
export interface Process {
  pname: string;
  pid: number;
  cmdline?: string;
  path?: string;
}

/**
 * Handles application operations in the AgentBay cloud environment.
 */
export class Application {
  private session: {
    getAPIKey(): string;
    getClient(): Client;
    getSessionId(): string;
    callMcpTool(toolName: string, args: any): Promise<{
      success: boolean;
      data: string;
      errorMessage: string;
      requestId: string;
    }>;
  };

  /**
   * Initialize an Application object.
   *
   * @param session - The Session instance that this Application belongs to.
   */
  constructor(session: {
    getAPIKey(): string;
    getClient(): Client;
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
   * Sanitizes error messages to remove sensitive information like API keys.
   *
   * @param error - The error to sanitize
   * @returns The sanitized error
   */
  private sanitizeError(error: any): any {
    if (!error) {
      return error;
    }

    const errorString = String(error);
    return errorString.replace(/Bearer\s+[^\s]+/g, "Bearer [REDACTED]");
  }

  /**
   * Helper method to parse JSON string into objects
   */
  private parseJSON<T>(jsonString: string): T {
    try {
      return JSON.parse(jsonString);
    } catch (error) {
      throw new Error(`Failed to parse JSON: ${error}`);
    }
  }

  /**
   * Retrieves a list of installed applications.
   * Corresponds to Python's get_installed_apps() method
   *
   * @param startMenu - Whether to include applications from the start menu. Defaults to true.
   * @param desktop - Whether to include applications from the desktop. Defaults to true.
   * @param ignoreSystemApps - Whether to ignore system applications. Defaults to true.
   * @returns InstalledAppListResult with installed apps and requestId
   * @throws Error if the operation fails.
   */
  async getInstalledApps(
    startMenu = true,
    desktop = true,
    ignoreSystemApps = true
  ): Promise<InstalledAppListResult> {
    try {
      const args = {
        start_menu: startMenu,
        desktop,
        ignore_system_apps: ignoreSystemApps,
      };

      const result = await this.session.callMcpTool("get_installed_apps", args);

      if (!result.success) {
        return {
          requestId: result.requestId,
          success: false,
          data: [],
          errorMessage: result.errorMessage,
        };
      }

      let apps: InstalledApp[] = [];
      try {
        apps = this.parseJSON<InstalledApp[]>(result.data);
      } catch (err) {
        return {
          requestId: result.requestId,
          success: false,
          data: [],
          errorMessage: `Failed to parse installed apps: ${err}`,
        };
      }

      return {
        requestId: result.requestId,
        success: true,
        data: apps,
      };
    } catch (error) {
      return {
        requestId: "",
        success: false,
        data: [],
        errorMessage: `Failed to get installed apps: ${error}`,
      };
    }
  }

  /**
   * Starts an application with the given command and optional working directory.
   * Corresponds to Python's start_app() method
   *
   * @param startCmd - The command to start the application.
   * @param workDirectory - The working directory for the application. Defaults to an empty string.
   * @param activity - Activity name to launch (e.g. ".SettingsActivity" or "com.package/.Activity"). Defaults to an empty string.
   * @returns ProcessListResult with started processes and requestId
   * @throws Error if the operation fails.
   */
  async startApp(
    startCmd: string,
    workDirectory = "",
    activity = ""
  ): Promise<ProcessListResult> {
    try {
      const args = {
        start_cmd: startCmd,
        work_directory: workDirectory,
        activity,
      };

      const result = await this.session.callMcpTool("start_app", args);

      if (!result.success) {
        return {
          requestId: result.requestId,
          success: false,
          data: [],
          errorMessage: result.errorMessage,
        };
      }

      let processes: Process[] = [];
      try {
        processes = this.parseJSON<Process[]>(result.data);
      } catch (err) {
        return {
          requestId: result.requestId,
          success: false,
          data: [],
          errorMessage: `Failed to parse processes: ${err}`,
        };
      }

      return {
        requestId: result.requestId,
        success: true,
        data: processes,
      };
    } catch (error) {
      return {
        requestId: "",
        success: false,
        data: [],
        errorMessage: `Failed to start app: ${error}`,
      };
    }
  }

  /**
   * Stops an application by process name.
   * Corresponds to Python's stop_app_by_pname() method
   *
   * @param pname - The process name to stop.
   * @returns AppOperationResult with operation result and requestId
   * @throws Error if the operation fails.
   */
  async stopAppByPName(pname: string): Promise<AppOperationResult> {
    try {
      const args = { pname };
      const result = await this.session.callMcpTool("stop_app_by_pname", args);

      if (!result.success) {
        return {
          requestId: result.requestId,
          success: false,
          errorMessage: result.errorMessage,
        };
      }

      return {
        requestId: result.requestId,
        success: true,
      };
    } catch (error) {
      return {
        requestId: "",
        success: false,
        errorMessage: `Failed to stop app by process name: ${error}`,
      };
    }
  }

  /**
   * Stops an application by process ID.
   * Corresponds to Python's stop_app_by_pid() method
   *
   * @param pid - The process ID to stop.
   * @returns AppOperationResult with operation result and requestId
   * @throws Error if the operation fails.
   */
  async stopAppByPID(pid: number): Promise<AppOperationResult> {
    try {
      const args = { pid };
      const result = await this.session.callMcpTool("stop_app_by_pid", args);

      if (!result.success) {
        return {
          requestId: result.requestId,
          success: false,
          errorMessage: result.errorMessage,
        };
      }

      return {
        requestId: result.requestId,
        success: true,
      };
    } catch (error) {
      return {
        requestId: "",
        success: false,
        errorMessage: `Failed to stop app by process ID: ${error}`,
      };
    }
  }

  /**
   * Stops an application by stop command.
   * Corresponds to Python's stop_app_by_cmd() method
   *
   * @param stopCmd - The stop command to execute.
   * @returns AppOperationResult with operation result and requestId
   * @throws Error if the operation fails.
   */
  async stopAppByCmd(stopCmd: string): Promise<AppOperationResult> {
    try {
      const args = { stop_cmd: stopCmd };
      const result = await this.session.callMcpTool("stop_app_by_cmd", args);

      if (!result.success) {
        return {
          requestId: result.requestId,
          success: false,
          errorMessage: result.errorMessage,
        };
      }

      return {
        requestId: result.requestId,
        success: true,
      };
    } catch (error) {
      return {
        requestId: "",
        success: false,
        errorMessage: `Failed to stop app by command: ${error}`,
      };
    }
  }

  /**
   * Returns a list of currently visible applications.
   * Corresponds to Python's list_visible_apps() method
   *
   * @returns ProcessListResult with visible apps and requestId
   * @throws Error if the operation fails.
   */
  async listVisibleApps(): Promise<ProcessListResult> {
    try {
      const result = await this.session.callMcpTool("list_visible_apps", {});

      if (!result.success) {
        return {
          requestId: result.requestId,
          success: false,
          data: [],
          errorMessage: result.errorMessage,
        };
      }

      let processes: Process[] = [];
      try {
        processes = this.parseJSON<Process[]>(result.data);
      } catch (err) {
        return {
          requestId: result.requestId,
          success: false,
          data: [],
          errorMessage: `Failed to parse visible apps: ${err}`,
        };
      }

      return {
        requestId: result.requestId,
        success: true,
        data: processes,
      };
    } catch (error) {
      return {
        requestId: "",
        success: false,
        data: [],
        errorMessage: `Failed to list visible apps: ${error}`,
      };
    }
  }
}
