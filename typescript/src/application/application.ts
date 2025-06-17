import { CallMcpToolRequest } from '../api/models/CallMcpToolRequest';
import Client from '../api/client';
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
export class ApplicationManager {
  private session: {
    getAPIKey(): string;
    getClient(): Client;
    getSessionId(): string;
  };

  /**
   * Creates a new ApplicationManager instance.
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
      
      const client = this.session.getClient();
      const response = await client.callMcpTool(request);
      console.log(`Response from CallMcpTool - ${name}:`, response);

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
      console.log('Extracting text field from the first content item...',contentItem);
      
      const jsonText = contentItem.text;
      if (!jsonText) {
        throw new Error('Text field not found or tool not found');
      }

      // Parse the JSON text
      console.log('Parsing JSON text...',jsonText);
      
      return JSON.parse(jsonText) as InstalledApp[];
    } catch (error) {
      throw new Error(`Failed to call MCP tool ${name}: ${error}`);
    }
  }

  /**
   * Retrieves a list of installed applications.
   * @param startMenu Whether to include applications from the start menu. Defaults to true.
   * @param desktop Whether to include applications from the desktop. Defaults to true.
   * @param ignoreSystemApps Whether to ignore system applications. Defaults to true.
   * @returns A list of installed applications.
   * @throws Error if the operation fails.
   */
  async getInstalledApps(
    startMenu: boolean = true,
    desktop: boolean = true,
    ignoreSystemApps: boolean = true
  ): Promise<InstalledApp[]> {
    const args = {
      start_menu: startMenu,
      desktop,
      ignore_system_apps: ignoreSystemApps
    };

    try {
      const result = await this.callMcpTool('get_installed_apps', args);
      console.log('API Response:', result);
      
      return result as InstalledApp[];
    } catch (error) {
      throw new Error(`Failed to get installed apps: ${error}`);
    }
  }

  /**
   * Starts an application with the given command and optional working directory.
   * @param startCmd The command to start the application.
   * @param workDirectory The working directory for the application. Defaults to an empty string.
   * @returns A list of processes started.
   * @throws Error if the operation fails.
   */
  async startApp(startCmd: string, workDirectory: string = ''): Promise<Process[]> {
    const args: any = {
      start_cmd: startCmd
    };

    if (workDirectory) {
      args.work_directory = workDirectory;
    }

    try {
      const result = await this.callMcpTool('start_app', args);
      console.log('API Response start_app:', result);
      
      return result as Process[];
    } catch (error) {
      throw new Error(`Failed to start app: ${error}`);
    }
  }

  /**
   * Stops an application by process name.
   * @param pname The name of the process to stop.
   * @throws Error if the operation fails.
   */
  async stopAppByPName(pname: string): Promise<void> {
    const args = {
      pname
    };

    try {
      await this.callMcpTool('stop_app_by_pname', args);
    } catch (error) {
      throw new Error(`Failed to stop app by pname: ${error}`);
    }
  }

  /**
   * Stops an application by process ID.
   * @param pid The ID of the process to stop.
   * @throws Error if the operation fails.
   */
  async stopAppByPID(pid: number): Promise<void> {
    const args = {
      pid
    };

    try {
      await this.callMcpTool('stop_app_by_pid', args);
    } catch (error) {
      throw new Error(`Failed to stop app by pid: ${error}`);
    }
  }

  /**
   * Stops an application by stop command.
   * @param stopCmd The command to stop the application.
   * @throws Error if the operation fails.
   */
  async stopAppByCmd(stopCmd: string): Promise<void> {
    const args = {
      stop_cmd: stopCmd
    };

    try {
      await this.callMcpTool('stop_app_by_cmd', args);
    } catch (error) {
      throw new Error(`Failed to stop app by command: ${error}`);
    }
  }

  /**
   * Lists all currently visible applications.
   * @returns A list of visible processes.
   * @throws Error if the operation fails.
   */
  async listVisibleApps(): Promise<Process[]> {
    const args = {};

    try {
      const result = await this.callMcpTool('list_visible_apps', args);
      console.log('listVisibleApps Response:', result);
      
      return result as Process[];
    } catch (error) {
      throw new Error(`Failed to list visible apps: ${error}`);
    }
  }
}
