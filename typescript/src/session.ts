import { AgentBay } from "./agent-bay";
import { Client } from "./api/client";
import {
  GetLabelRequest,
  GetLinkRequest,
  GetMcpResourceRequest,
  ReleaseMcpSessionRequest,
  SetLabelRequest,
} from "./api/models/model";
import { Application } from "./application";
import { Code } from "./code";
import { Command } from "./command";
import { ContextManager, newContextManager } from "./context-manager";
import { APIError } from "./exceptions";
import { FileSystem } from "./filesystem";
import { Oss } from "./oss";
import {
  DeleteResult,
  extractRequestId,
  OperationResult,
} from "./types/api-response";
import { UI } from "./ui";
import { log, logError } from "./utils/logger";
import { WindowManager } from "./window";

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
  ticket?: string;
}

/**
 * SessionInfo class to match Python version structure
 */
export class SessionInfoClass {
  sessionId: string;
  resourceUrl: string;
  appId: string;
  authCode: string;
  connectionProperties: string;
  resourceId: string;
  resourceType: string;
  ticket: string;

  constructor(
    sessionId = "",
    resourceUrl = "",
    appId = "",
    authCode = "",
    connectionProperties = "",
    resourceId = "",
    resourceType = "",
    ticket = ""
  ) {
    this.sessionId = sessionId;
    this.resourceUrl = resourceUrl;
    this.appId = appId;
    this.authCode = authCode;
    this.connectionProperties = connectionProperties;
    this.resourceId = resourceId;
    this.resourceType = resourceType;
    this.ticket = ticket;
  }
}

/**
 * Represents a session in the AgentBay cloud environment.
 */
export class Session {
  private agentBay: AgentBay;
  public sessionId: string;
  public resourceUrl = "";

  // File, command, code, and oss handlers (matching Python naming)
  public fileSystem: FileSystem; // file_system in Python
  public command: Command;
  public code: Code;
  public oss: Oss;

  // Application, window, and UI management (matching Python naming)
  public application: Application; // application in Python (ApplicationManager)
  public window: WindowManager;
  public ui: UI;

  // Context management (matching Go version)
  public context: ContextManager;

  /**
   * Initialize a Session object.
   *
   * @param agentBay - The AgentBay instance that created this session.
   * @param sessionId - The ID of this session.
   */
  constructor(agentBay: AgentBay, sessionId: string) {
    this.agentBay = agentBay;
    this.sessionId = sessionId;
    this.resourceUrl = "";

    // Initialize file system, command and code handlers (matching Python naming)
    this.fileSystem = new FileSystem(this);
    this.command = new Command(this);
    this.code = new Code(this);
    this.oss = new Oss(this);

    // Initialize application and window managers (matching Python naming)
    this.application = new Application(this);
    this.window = new WindowManager(this);
    this.ui = new UI(this);

    // Initialize context manager (matching Go version)
    this.context = newContextManager(this);
  }

  /**
   * Return the API key for this session.
   */
  getAPIKey(): string {
    return this.agentBay.getAPIKey();
  }

  /**
   * Return the HTTP client for this session.
   */
  getClient(): Client {
    return this.agentBay.getClient();
  }

  /**
   * Return the session_id for this session.
   */
  getSessionId(): string {
    return this.sessionId;
  }

  /**
   * Delete this session.
   *
   * @param syncContext - Whether to sync context data (trigger file uploads) before deleting the session. Defaults to false.
   * @returns DeleteResult indicating success or failure and request ID
   */
  async delete(syncContext = false): Promise<DeleteResult> {
    try {
      // If syncContext is true, trigger file uploads first
      if (syncContext) {
        log("Triggering context synchronization before session deletion...");

        // Trigger file upload
        try {
          const syncResult = await this.context.sync();
          if (!syncResult.success) {
            log("Warning: Context sync operation returned failure status");
          }
        } catch (error) {
          logError("Warning: Failed to trigger context sync:", error);
          // Continue with deletion even if sync fails
        }

        // Wait for uploads to complete
        const maxRetries = 150; // Maximum number of retries
        const retryInterval = 2000; // Milliseconds to wait between retries

        for (let retry = 0; retry < maxRetries; retry++) {
          try {
            // Get context status data
            const infoResult = await this.context.info();

            // Check if all upload context items have status "Success" or "Failed"
            let allCompleted = true;
            let hasFailure = false;
            let hasUploads = false;

            for (const item of infoResult.contextStatusData) {
              // We only care about upload tasks
              if (item.taskType !== "upload") {
                continue;
              }

              hasUploads = true;
              log(`Upload context ${item.contextId} status: ${item.status}, path: ${item.path}`);

              if (item.status !== "Success" && item.status !== "Failed") {
                allCompleted = false;
                break;
              }
              
              if (item.status === "Failed") {
                hasFailure = true;
                logError(`Upload failed for context ${item.contextId}: ${item.errorMessage}`);
              }
            }

            if (allCompleted || !hasUploads) {
              if (hasFailure) {
                log("Context upload completed with failures");
              } else if (hasUploads) {
                log("Context upload completed successfully");
              } else {
                log("No upload tasks found");
              }
              break;
            }

            log(`Waiting for context upload to complete, attempt ${retry+1}/${maxRetries}`);
            await new Promise(resolve => setTimeout(resolve, retryInterval));
          } catch (error) {
            logError(`Error checking context status on attempt ${retry+1}:`, error);
            await new Promise(resolve => setTimeout(resolve, retryInterval));
          }
        }
      }

      // Proceed with session deletion
      const request = new ReleaseMcpSessionRequest({
        authorization: `Bearer ${this.getAPIKey()}`,
        sessionId: this.sessionId,
      });

      const response = await this.getClient().releaseMcpSession(request);
      log(`Response from release_mcp_session: ${JSON.stringify(response)}`);

      // Extract request ID
      const requestId = extractRequestId(response) || "";

      // Check if the response is success (matching Python logic)
      const responseBody = response.body;
      const success = responseBody?.success !== false; // Note: capital S to match Python

      if (!success) {
        return {
          requestId,
          success: false,
          errorMessage: "Failed to delete session",
        };
      }

      // Return success result with request ID
      return {
        requestId,
        success: true,
      };
    } catch (error) {
      logError("Error calling release_mcp_session:", error);
      // In case of error, return failure result with error message (matching Python)
      return {
        requestId: "",
        success: false,
        errorMessage: `Failed to delete session ${this.sessionId}: ${error}`,
      };
    }
  }

  /**
   * Sets the labels for this session.
   *
   * @param labels - The labels to set for the session.
   * @returns OperationResult indicating success or failure with request ID
   * @throws Error if the operation fails (matching Python SessionError)
   */
  async setLabels(labels: Record<string, string>): Promise<OperationResult> {
    try {
      // Convert labels to JSON string
      const labelsJSON = JSON.stringify(labels);

      const request = new SetLabelRequest({
        authorization: `Bearer ${this.getAPIKey()}`,
        sessionId: this.sessionId,
        labels: labelsJSON,
      });

      const response = await this.getClient().setLabel(request);

      // Extract request ID
      const requestId = extractRequestId(response) || "";

      return {
        requestId,
        success: true,
      };
    } catch (error) {
      logError("Error calling set_label:", error);
      throw new Error(
        `Failed to set labels for session ${this.sessionId}: ${error}`
      );
    }
  }

  /**
   * Gets the labels for this session.
   *
   * @returns OperationResult containing the labels as data and request ID
   * @throws Error if the operation fails (matching Python SessionError)
   */
  async getLabels(): Promise<OperationResult> {
    try {
      const request = new GetLabelRequest({
        authorization: `Bearer ${this.getAPIKey()}`,
        sessionId: this.sessionId,
      });

      const response = await this.getClient().getLabel(request);

      // Extract request ID
      const requestId = extractRequestId(response) || "";

      // Extract labels from response (matching Python structure)
      const responseBody = response?.body;
      const data = responseBody?.data; // Capital D to match Python
      const labelsJSON = data?.labels; // Capital L to match Python

      let labels = {};
      if (labelsJSON) {
        labels = JSON.parse(labelsJSON);
      }

      return {
        requestId,
        success: true,
        data: labels,
      };
    } catch (error) {
      logError("Error calling get_label:", error);
      throw new Error(
        `Failed to get labels for session ${this.sessionId}: ${error}`
      );
    }
  }

  /**
   * Gets information about this session.
   *
   * @returns OperationResult containing the session information as data and request ID
   * @throws Error if the operation fails (matching Python SessionError)
   */
  async info(): Promise<OperationResult> {
    try {
      const request = new GetMcpResourceRequest({
        authorization: `Bearer ${this.getAPIKey()}`,
        sessionId: this.sessionId,
      });

      log("API Call: GetMcpResource");
      log(`Request: SessionId=${this.sessionId}`);

      const response = await this.getClient().getMcpResource(request);
      log(`Response from GetMcpResource: ${JSON.stringify(response)}`);

      // Extract request ID
      const requestId = extractRequestId(response) || "";

      // Extract session info from response (matching Python structure)
      const responseBody = response.body;
      const data = responseBody?.data; // Capital D to match Python

      const sessionInfo = new SessionInfoClass();

      if (data?.sessionId) {
        // Capital S and I to match Python
        sessionInfo.sessionId = data.sessionId;
      }

      if (data?.resourceUrl) {
        // Capital R and U to match Python
        sessionInfo.resourceUrl = data.resourceUrl;
        // Update the session's resource_url with the latest value
        this.resourceUrl = data.resourceUrl;
      }

      // Transfer DesktopInfo fields to SessionInfo (matching Python structure)
      if (data?.desktopInfo) {
        // Capital D and I to match Python
        const desktopInfo = data.desktopInfo;
        if (desktopInfo.appId) {
          sessionInfo.appId = desktopInfo.appId;
        }
        if (desktopInfo.authCode) {
          sessionInfo.authCode = desktopInfo.authCode;
        }
        if (desktopInfo.connectionProperties) {
          sessionInfo.connectionProperties = desktopInfo.connectionProperties;
        }
        if (desktopInfo.resourceId) {
          sessionInfo.resourceId = desktopInfo.resourceId;
        }
        if (desktopInfo.resourceType) {
          sessionInfo.resourceType = desktopInfo.resourceType;
        }
        if (desktopInfo.ticket) {
          sessionInfo.ticket = desktopInfo.ticket;
        }
      }

      return {
        requestId,
        success: true,
        data: sessionInfo,
      };
    } catch (error) {
      logError("Error calling GetMcpResource:", error);
      throw new Error(
        `Failed to get session info for session ${this.sessionId}: ${error}`
      );
    }
  }

  /**
   * Get a link associated with the current session.
   *
   * @param protocolType - Optional protocol type to use for the link
   * @param port - Optional port to use for the link
   * @returns OperationResult containing the link as data and request ID
   * @throws Error if the operation fails (matching Python SessionError)
   */
  async getLink(
    protocolType?: string,
    port?: number
  ): Promise<OperationResult> {
    try {
      const request = new GetLinkRequest({
        authorization: `Bearer ${this.getAPIKey()}`,
        sessionId: this.getSessionId(),
        protocolType,
        port,
      });

      const response = await this.agentBay.getClient().getLink(request);

      // Extract request ID
      const requestId = extractRequestId(response) || "";

      const responseBody = response.body;

      if (typeof responseBody !== "object") {
        throw new Error(
          "Invalid response format: expected a dictionary from response body"
        );
      }

      let data = responseBody.data || {}; // Capital D to match Python
      log(`Data: ${JSON.stringify(data)}`);

      if (typeof data !== "object") {
        try {
          data = typeof data === "string" ? JSON.parse(data) : {};
        } catch (jsonError) {
          data = {};
        }
      }

      const url = (data as any).Url || "";

      return {
        requestId,
        success: true,
        data: url,
      };
    } catch (error) {
      if (
        error instanceof Error &&
        error.message.includes("Invalid response format")
      ) {
        throw error;
      }
      throw new Error(`Failed to get link: ${error}`);
    }
  }

  /**
   * Asynchronously get a link associated with the current session.
   *
   * @param protocolType - Optional protocol type to use for the link
   * @param port - Optional port to use for the link
   * @returns OperationResult containing the link as data and request ID
   * @throws Error if the operation fails (matching Python SessionError)
   */
  async getLinkAsync(
    protocolType?: string,
    port?: number
  ): Promise<OperationResult> {
    try {
      const request = new GetLinkRequest({
        authorization: `Bearer ${this.getAPIKey()}`,
        sessionId: this.getSessionId(),
        protocolType,
        port,
      });

      // Note: In TypeScript, async is the default, but keeping this method for API compatibility
      const response = await this.agentBay.getClient().getLink(request);

      // Extract request ID
      const requestId = extractRequestId(response) || "";

      const responseBody = response?.body;

      if (typeof responseBody !== "object") {
        throw new Error(
          "Invalid response format: expected a dictionary from response body"
        );
      }

      let data = responseBody?.data || {}; // Capital D to match Python
      log(`Data: ${JSON.stringify(data)}`);

      if (typeof data !== "object") {
        try {
          data = typeof data === "string" ? JSON.parse(data) : {};
        } catch (jsonError) {
          data = {};
        }
      }

      const url = (data as any).Url || "";

      return {
        requestId,
        success: true,
        data: url,
      };
    } catch (error) {
      if (
        error instanceof Error &&
        error.message.includes("Invalid response format")
      ) {
        throw error;
      }
      throw new Error(`Failed to get link asynchronously: ${error}`);
    }
  }
}
