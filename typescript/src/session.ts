import { AgentBay } from './agent-bay';
import { APIError } from './exceptions';
import { FileSystem } from './filesystem';
import { Command } from './command';
import { Adb } from './adb';
import { Oss } from './oss';
import { ApplicationManager } from './application';
import { WindowManager } from './window';
import Client from './api/client';
import { ReleaseMcpSessionRequest, SetLabelRequest, GetLabelRequest, GetMcpResourceRequest } from './api/models/model';

/**
 * Contains information about a session.
 */
export interface SessionInfo {
  sessionId: string;
  resourceUrl: string;
  appId?: string;
  authCode?: string;
  connectionProperties?: string;
  resourceId?: string;
  resourceType?: string;
}

/**
 * Represents a session in the AgentBay cloud environment.
 */
export class Session {
  private agentBay: AgentBay;
  public client:  Client;
  public sessionId: string;
  public resourceUrl: string = "";
  
  // File, command, adb, and oss handlers
  public filesystem: FileSystem;
  public command: Command;
  public adb: Adb;
  public oss: Oss;
  
  // Application and window management
  public application: ApplicationManager;
  public window: WindowManager;

  /**
   * Initialize a Session object.
   * 
   * @param agentBay - The AgentBay instance that created this session.
   * @param sessionId - The ID of this session.
   */
  constructor(agentBay: AgentBay, sessionId: string) {
    this.agentBay = agentBay;
    this.sessionId = sessionId;
    this.client = agentBay.getClient();
    console.log(`Session created with ID: ${sessionId}`);
    
    // Initialize filesystem, command, adb, and oss handlers
    this.filesystem = new FileSystem(this);
    this.command = new Command(this);
    this.adb = new Adb(this);
    this.oss = new Oss(this);
    
    // Initialize application and window managers
    this.application = new ApplicationManager(this);
    this.window = new WindowManager(this);
  }

  /**
   * Get information about this session.
   * 
   * @returns Session information.
   */
  // async get_info(): Promise<Record<string, any>> {
  //   // TODO: Implement the API call to get session info
  //   try {
  //     const response = await this.client.get(this.baseUrl);
  //     return response.data;
  //   } catch (error) {
  //     throw new APIError(`Failed to get session info: ${error}`);
  //   }
  // }

  /**
   * Delete this session.
   * 
   * @returns True if the session was successfully deleted.
   */
  async delete(): Promise<boolean> {
    try {
      const releaseSessionRequest = new ReleaseMcpSessionRequest({
        authorization: `Bearer ${this.getAPIKey()}`,
        sessionId: this.sessionId
      });
      console.log("API Call delete: ReleaseMcpSession",this.sessionId);
      
      await this.client.releaseMcpSession(releaseSessionRequest);
     
      this.agentBay.removeSession(this.sessionId);
    return true;
    } catch (error) {
      throw new APIError(`Failed to delete session: ${error}`);
    }
  }

  
  
  /**
   * Sets the labels for this session.
   * 
   * @param labels - The labels to set for the session.
   * @throws APIError if the operation fails.
   */
  async setLabels(labels: Record<string, string>): Promise<void> {
    try {
      // Convert labels to JSON string
      const labelsJSON = JSON.stringify(labels);
      
      const request = new SetLabelRequest({
        authorization: `Bearer ${this.getAPIKey()}`,
        sessionId: this.sessionId,
        labels: labelsJSON
      });
      
      const result = await this.client.setLabel(request);
      console.log( 'response from setLabels',result);
      
    } catch (error) {
      throw new APIError(`Failed to set labels for session: ${error}`);
    }
  }
  
  /**
   * Gets the labels for this session.
   * 
   * @returns The labels for the session.
   * @throws APIError if the operation fails.
   */
  async getLabels(): Promise<Record<string, string>> {
    try {
      const request = new GetLabelRequest({
        authorization: `Bearer ${this.getAPIKey()}`,
        sessionId: this.sessionId
      });
      
      const response = await this.client.getLabel(request);
      console.log(`Response from GetLabel: ${JSON.stringify(response)}`);
      
      // Extract labels from response
      const labelsJSON = response.body?.data?.labels;
      
      if (labelsJSON) {
        return JSON.parse(labelsJSON);
      }
      
      return {};
    } catch (error) {
      throw new APIError(`Failed to get labels for session: ${error}`);
    }
  }
  
  /**
   * Get the API key.
   * 
   * @returns The API key.
   */
  getAPIKey(): string {
    return this.agentBay.getAPIKey();
  }
  
  /**
   * Get the client.
   * 
   * @returns The client.
   */
  getClient(): Client {
    
    return this.client;
  }
  
  /**
   * Get the session ID.
   * 
   * @returns The session ID.
   */
  getSessionId(): string {
    return this.sessionId;
  }
  
  /**
   * Gets information about this session.
   * 
   * @returns Information about the session.
   * @throws APIError if the operation fails.
   */
  async info(): Promise<SessionInfo> {
    try {
      const request = new GetMcpResourceRequest({
        authorization: `Bearer ${this.getAPIKey()}`,
        sessionId: this.sessionId
      });
      
      console.log("API Call: GetMcpResource");
      console.log(`Request: SessionId=${this.sessionId}`);
      
      const response = await this.client.getMcpResource(request);
      console.log(`Response from GetMcpResource: ${JSON.stringify(response)}`);
      
      // Extract session info from response
      const sessionInfo: SessionInfo = {
        sessionId: response.body?.data?.sessionId || "",
        resourceUrl: response.body?.data?.resourceUrl || ""
      };
      
      // Update the session's resourceUrl with the latest value
      if (response.body?.data?.resourceUrl) {
        this.resourceUrl = response.body.data.resourceUrl;
      }
      
      // Transfer DesktopInfo fields to SessionInfo
      if (response.body?.data?.desktopInfo) {
        const desktopInfo = response.body.data.desktopInfo;
        sessionInfo.appId = desktopInfo.appId;
        sessionInfo.authCode = desktopInfo.authCode;
        sessionInfo.connectionProperties = desktopInfo.connectionProperties;
        sessionInfo.resourceId = desktopInfo.resourceId;
        sessionInfo.resourceType = desktopInfo.resourceType;
      }
      
      return sessionInfo;
    } catch (error) {
      console.error("Error calling GetMcpResource:", error);
      throw new APIError(`Failed to get session info for session ${this.sessionId}: ${error}`);
    }
  }
}
