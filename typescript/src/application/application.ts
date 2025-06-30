import { CallMcpToolRequest } from '../api/models/CallMcpToolRequest';
import {Client} from '../api/client';
import { log, logError } from '../utils/logger';
import { APIError } from '../exceptions';
import { ApiResponseWithData, extractRequestId } from '../types/api-response';

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
 * Represents an installed application.
 */
export interface InstalledApp {
  name: string;
  start_cmd: string;
  stop_cmd?: string;
  work_directory?: string;
}

/**
 * Represents a running process.
 */
export interface Process {
  pname: string;
  pid: number;
  cmdline?: string;
  path?: string;
}

/**
 * Handles application management operations in the AgentBay cloud environment.
 */
export class Application {
  private session: {
    getAPIKey(): string;
    getClient(): Client;
    getSessionId(): string;
  };

  /**
   * Creates a new Application instance.
   * @param session The session object that provides access to the AgentBay API.
   */
  constructor(session: {
    getAPIKey(): string;
    getClient(): Client;
    getSessionId(): string;
  }) {
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
      const request = new CallMcpToolRequest({
        authorization: `Bearer ${this.session.getAPIKey()}`,
        sessionId: this.session.getSessionId(),
        name: toolName,
        args: argsJSON
      });

      // Log API request
      log(`API Call: CallMcpTool - ${toolName}`);
      log(`Request: SessionId=${request.sessionId}, Args=${request.args}`);

      const client = this.session.getClient();
      const response = await client.callMcpTool(request);

      // Log API response
      if (response && response.body) {
        log(`Response from CallMcpTool - ${toolName}:`, response.body);
      }

      // Extract data from response
      if (!response.body?.data) {
        throw new Error('Invalid response data format');
      }

      const data = response.body.data as Record<string, any>;

      // Create result object
      const result: CallMcpToolResult = {
        data,
        statusCode: response.statusCode || 0,
        isError: false,
        requestId: extractRequestId(response)
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
   * @param startMenu Whether to include applications from the start menu. Defaults to true.
   * @param desktop Whether to include applications from the desktop. Defaults to true.
   * @param ignoreSystemApps Whether to ignore system applications. Defaults to true.
   * @returns API response with installed apps and requestId
   * @throws Error if the operation fails.
   */
  async getInstalledApps(
    startMenu: boolean = true,
    desktop: boolean = true,
    ignoreSystemApps: boolean = true
  ): Promise<ApiResponseWithData<InstalledApp[]>> {
    const args = {
      start_menu: startMenu,
      desktop,
      ignore_system_apps: ignoreSystemApps
    };

    const result = await this.callMcpTool('get_installed_apps', args, 'Failed to get installed apps');

    let apps: InstalledApp[] = [];
    if (result.textContent) {
      apps = this.parseJSON<InstalledApp[]>(result.textContent);
    }

    return {
      requestId: result.requestId,
      data: apps
    };
  }

  /**
   * Starts an application with the given command and optional working directory.
   * @param startCmd The command to start the application.
   * @param workDirectory The working directory for the application. Defaults to an empty string.
   * @returns API response with started processes and requestId
   * @throws Error if the operation fails.
   */
  async startApp(startCmd: string, workDirectory: string = ''): Promise<ApiResponseWithData<Process[]>> {
    const args: any = {
      start_cmd: startCmd
    };

    if (workDirectory) {
      args.work_directory = workDirectory;
    }

    const result = await this.callMcpTool('start_app', args, 'Failed to start app');

    let processes: Process[] = [];
    if (result.textContent) {
      processes = this.parseJSON<Process[]>(result.textContent);
    }

    return {
      requestId: result.requestId,
      data: processes
    };
  }

  /**
   * Stops an application by process name.
   * @param pname The name of the process to stop.
   * @returns API response with requestId
   * @throws Error if the operation fails.
   */
  async stopAppByPName(pname: string): Promise<ApiResponseWithData<void>> {
    const args = {
      pname
    };

    const result = await this.callMcpTool('stop_app_by_pname', args, 'Failed to stop app by pname');

    return {
      requestId: result.requestId,
      data: undefined
    };
  }

  /**
   * Stops an application by process ID.
   * @param pid The ID of the process to stop.
   * @returns API response with requestId
   * @throws Error if the operation fails.
   */
  async stopAppByPID(pid: number): Promise<ApiResponseWithData<void>> {
    const args = {
      pid
    };

    const result = await this.callMcpTool('stop_app_by_pid', args, 'Failed to stop app by pid');

    return {
      requestId: result.requestId,
      data: undefined
    };
  }

  /**
   * Stops an application by stop command.
   * @param stopCmd The command to stop the application.
   * @returns API response with requestId
   * @throws Error if the operation fails.
   */
  async stopAppByCmd(stopCmd: string): Promise<ApiResponseWithData<void>> {
    const args = {
      stop_cmd: stopCmd
    };

    const result = await this.callMcpTool('stop_app_by_cmd', args, 'Failed to stop app by command');

    return {
      requestId: result.requestId,
      data: undefined
    };
  }

  /**
   * Lists all currently visible applications.
   * @returns API response with visible processes and requestId
   * @throws Error if the operation fails.
   */
  async listVisibleApps(): Promise<ApiResponseWithData<Process[]>> {
    const args = {};

    const result = await this.callMcpTool('list_visible_apps', args, 'Failed to list visible apps');

    let processes: Process[] = [];
    if (result.textContent) {
      processes = this.parseJSON<Process[]>(result.textContent);
    }

    return {
      requestId: result.requestId,
      data: processes
    };
  }
}
