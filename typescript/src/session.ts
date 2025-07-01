import { AgentBay } from "./agent-bay";
import { APIError } from "./exceptions";
import { FileSystem } from "./filesystem";
import { Command } from "./command";
import { Oss } from "./oss";
import { Application } from "./application";
import { WindowManager } from "./window";
import { UI } from "./ui";
import { Client } from "./api/client";
import {
  ReleaseMcpSessionRequest,
  SetLabelRequest,
  GetLabelRequest,
  GetMcpResourceRequest,
  GetLinkRequest,
} from "./api/models/model";
import { log, logError } from "./utils/logger";
import {
  ApiResponse,
  ApiResponseWithData,
  extractRequestId,
} from "./types/api-response";

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
  public client: Client;
  public sessionId: string;
  public resourceUrl: string = "";

  // File, command, and oss handlers
  public filesystem: FileSystem;
  public command: Command;
  public oss: Oss;

  // Application, window, and UI management
  public Application: Application;
  public window: WindowManager;
  public ui: UI;

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
    log(`Session created with ID: ${sessionId}`);

    // Initialize filesystem, command, and oss handlers
    this.filesystem = new FileSystem(this);
    this.command = new Command(this);
    this.oss = new Oss(this);

    // Initialize application, window, and UI managers
    this.Application = new Application(this);
    this.window = new WindowManager(this);
    this.ui = new UI(this);
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
   * @returns API response with requestId
   */
  async delete(): Promise<ApiResponse> {
    try {
      const releaseSessionRequest = new ReleaseMcpSessionRequest({
        authorization: `Bearer ${this.getAPIKey()}`,
        sessionId: this.sessionId,
      });

      // Log API request
      log("API Call: ReleaseMcpSession");
      log(`Request: SessionId=${this.sessionId}`);

      const response = await this.client.releaseMcpSession(
        releaseSessionRequest
      );

      // Log API response
      log(`Response from ReleaseMcpSession:`, response.body);

      this.agentBay.removeSession(this.sessionId);

      return {
        requestId: extractRequestId(response),
      };
    } catch (error) {
      logError("Error calling ReleaseMcpSession:", error);
      throw new APIError(`Failed to delete session: ${error}`);
    }
  }

  /**
   * Sets the labels for this session.
   *
   * @param labels - The labels to set for the session.
   * @returns API response with requestId
   * @throws APIError if the operation fails.
   */
  async setLabels(labels: Record<string, string>): Promise<ApiResponse> {
    try {
      // Convert labels to JSON string
      const labelsJSON = JSON.stringify(labels);

      const request = new SetLabelRequest({
        authorization: `Bearer ${this.getAPIKey()}`,
        sessionId: this.sessionId,
        labels: labelsJSON,
      });

      // Log API request
      log("API Call: SetLabel");
      log(`Request: SessionId=${this.sessionId}, Labels=${labelsJSON}`);

      const response = await this.client.setLabel(request);

      // Log API response
      log(`Response from SetLabel:`, response.body);

      return {
        requestId: extractRequestId(response),
      };
    } catch (error) {
      logError("Error calling SetLabel:", error);
      throw new APIError(`Failed to set labels for session: ${error}`);
    }
  }

  /**
   * Gets the labels for this session.
   *
   * @returns API response with labels data and requestId
   * @throws APIError if the operation fails.
   */
  async getLabels(): Promise<ApiResponseWithData<Record<string, string>>> {
    try {
      const request = new GetLabelRequest({
        authorization: `Bearer ${this.getAPIKey()}`,
        sessionId: this.sessionId,
      });

      // Log API request
      log("API Call: GetLabel");
      log(`Request: SessionId=${this.sessionId}`);

      const response = await this.client.getLabel(request);
      // Log API response
      log(`Response from GetLabel:`, response.body);

      // Extract labels from response
      const labelsJSON = response.body?.data?.labels;
      let labels: Record<string, string> = {};

      if (labelsJSON) {
        labels = JSON.parse(labelsJSON);
      }

      return {
        requestId: extractRequestId(response),
        data: labels,
      };
    } catch (error) {
      logError("Error calling GetLabel:", error);
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
   * @returns API response with session information and requestId
   * @throws APIError if the operation fails.
   */
  async info(): Promise<ApiResponseWithData<SessionInfo>> {
    try {
      const request = new GetMcpResourceRequest({
        authorization: `Bearer ${this.getAPIKey()}`,
        sessionId: this.sessionId,
      });

      log("API Call: GetMcpResource");
      log(`Request: SessionId=${this.sessionId}`);

      const response = await this.client.getMcpResource(request);
      log(`Response from GetMcpResource:`, response.body);

      // Extract session info from response
      const sessionInfo: SessionInfo = {
        sessionId: response.body?.data?.sessionId || "",
        resourceUrl: response.body?.data?.resourceUrl || "",
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

      return {
        requestId: extractRequestId(response),
        data: sessionInfo,
      };
    } catch (error) {
      logError("Error calling GetMcpResource:", error);
      throw new APIError(
        `Failed to get session info for session ${this.sessionId}: ${error}`
      );
    }
  }

  /**
   * Gets the link for this session.
   *
   * @returns API response with link data and requestId
   * @throws APIError if the operation fails.
   */
  async getLink(): Promise<ApiResponseWithData<string>> {
    try {
      const request = new GetLinkRequest({
        authorization: `Bearer ${this.getAPIKey()}`,
        sessionId: this.sessionId,
      });

      log("API Call: GetLink");
      log(`Request: SessionId=${this.sessionId}`);

      const response = await this.client.getLink(request);
      log(`Response from GetLink:`, response.body);

      const linkData = response.body?.data || "";

      return {
        requestId: extractRequestId(response),
        data: linkData,
      };
    } catch (error) {
      logError("Error calling GetLink:", error);
      throw new APIError(
        `Failed to get link for session ${this.sessionId}: ${error}`
      );
    }
  }
}
