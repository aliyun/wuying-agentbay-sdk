import { $OpenApiUtil } from "@alicloud/openapi-core";
import "dotenv/config";
import * as $_client from "./api";
import { ListSessionRequest, CreateMcpSessionRequestPersistenceDataList } from "./api/models/model";
import { Client } from "./api/client";

import { loadConfig, Config, BROWSER_DATA_PATH } from "./config";
import { ContextService } from "./context";
import { ContextSync } from "./context-sync";
import { APIError, AuthenticationError } from "./exceptions";
import { Session } from "./session";
import { BrowserContext } from "./session-params";

import {
  DeleteResult,
  extractRequestId,
  SessionResult,
} from "./types/api-response";
import {
  ListSessionParams,
  SessionListResult,
} from "./types/list-session-params";
import { log, logError } from "./utils/logger";

/**
 * Parameters for creating a session.
 */
export interface CreateSessionParams {
  contextId?: string;
  labels?: Record<string, string>;
  imageId?: string;
  contextSync?: ContextSync[];
  browserContext?: BrowserContext;
}

/**
 * Main class for interacting with the AgentBay cloud runtime environment.
 */
export class AgentBay {
  private apiKey: string;
  private client: Client;
  private regionId: string;
  private endpoint: string;
  private sessions: Map<string, Session> = new Map();

  /**
   * Context service for managing persistent contexts.
   */
  context: ContextService;

  /**
   * Initialize the AgentBay client.
   *
   * @param options - Configuration options
   * @param options.apiKey - API key for authentication. If not provided, will look for AGENTBAY_API_KEY environment variable.
   * @param options.config - Custom configuration object. If not provided, will use environment-based configuration.
   */
  constructor(
    options: {
      apiKey?: string;
      config?: Config;
    } = {}
  ) {
    this.apiKey = options.apiKey || process.env.AGENTBAY_API_KEY || "";

    if (!this.apiKey) {
      throw new AuthenticationError(
        "API key is required. Provide it as a parameter or set the AGENTBAY_API_KEY environment variable."
      );
    }

    // Load configuration using the enhanced loadConfig function
    const configData = loadConfig(options.config);
    this.regionId = configData.region_id;
    this.endpoint = configData.endpoint;

    const config = new $OpenApiUtil.Config({
      regionId: this.regionId,
      endpoint: this.endpoint,
    });

    config.readTimeout = configData.timeout_ms;
    config.connectTimeout = configData.timeout_ms;

    try {
      this.client = new Client(config);

      // Initialize context service
      this.context = new ContextService(this);
    } catch (error) {
      logError(`Failed to constructor:`, error);
      throw new AuthenticationError(`Failed to constructor: ${error}`);
    }
  }

  /**
   * Create a new session in the AgentBay cloud environment.
   *
   * @param params - Optional parameters for creating the session
   * @returns SessionResult containing the created session and request ID
   */
  async create(params: CreateSessionParams = {}): Promise<SessionResult> {
    try {
      const request = new $_client.CreateMcpSessionRequest({
        authorization: "Bearer " + this.apiKey,
      });

      // Add context_id if provided
      if (params.contextId) {
        request.contextId = params.contextId;
      }

      // Add labels if provided
      if (params.labels) {
        request.labels = JSON.stringify(params.labels);
      }

      // Add image_id if provided
      if (params.imageId) {
        request.imageId = params.imageId;
      }

      // Flag to indicate if we need to wait for context synchronization
      let hasPersistenceData = false;

      // Add context sync configurations if provided
      if (params.contextSync && params.contextSync.length > 0) {
        const persistenceDataList: CreateMcpSessionRequestPersistenceDataList[] = [];
        for (const contextSync of params.contextSync) {
          const persistenceItem = new CreateMcpSessionRequestPersistenceDataList({
            contextId: contextSync.contextId,
            path: contextSync.path,
          });

          // Convert policy to JSON string if provided
          if (contextSync.policy) {
            persistenceItem.policy = JSON.stringify(contextSync.policy);
          }

          persistenceDataList.push(persistenceItem);
        }
        request.persistenceDataList = persistenceDataList;
        hasPersistenceData = persistenceDataList.length > 0;
      }

      // Add BrowserContext as a ContextSync if provided
      if (params.browserContext) {
        // Create a simple sync policy for browser context
        const syncPolicy = {
          uploadPolicy: { autoUpload: params.browserContext.autoUpload },
          downloadPolicy: null,
          deletePolicy: null,
          bwList: null
        };

        // Create browser context sync item
        const browserContextSync = new CreateMcpSessionRequestPersistenceDataList({
          contextId: params.browserContext.contextId,
          path: BROWSER_DATA_PATH, // Using a constant path for browser data
          policy: JSON.stringify(syncPolicy)
        });

        // Add to persistence data list or create new one if not exists
        if (!request.persistenceDataList) {
          request.persistenceDataList = [];
        }
        request.persistenceDataList.push(browserContextSync);
        hasPersistenceData = true;
      }

      // Log API request
      log("API Call: CreateMcpSession");
      let requestLog = "Request: ";
      if (request.contextId) {
        requestLog += `ContextId=${request.contextId}, `;
      }
      if (request.imageId) {
        requestLog += `ImageId=${request.imageId}, `;
      }
      if (request.labels) {
        requestLog += `Labels=${request.labels}, `;
      }
      if (
        request.persistenceDataList &&
        request.persistenceDataList.length > 0
      ) {
        requestLog += `PersistenceDataList=${request.persistenceDataList.length} items, `;
        request.persistenceDataList.forEach((pd: CreateMcpSessionRequestPersistenceDataList, i: number) => {
          requestLog += `Item${i}[ContextId=${pd.contextId}, Path=${pd.path}`;
          if (pd.policy) {
            requestLog += `, Policy=${pd.policy}`;
          }
          requestLog += `], `;
        });
      }
      log(requestLog);

      const response = await this.client.createMcpSession(request);
      log("response =", response);

      // Extract request ID
      const requestId = extractRequestId(response) || "";

      const sessionData = response.body;

      if (!sessionData || typeof sessionData !== "object") {
        return {
          requestId,
          success: false,
          errorMessage: "Invalid response format: expected a dictionary",
        };
      }

      const data = sessionData.data;
      if (!data || typeof data !== "object") {
        return {
          requestId,
          success: false,
          errorMessage:
            "Invalid response format: 'data' field is not a dictionary",
        };
      }

      const sessionId = data.sessionId;
      if (!sessionId) {
        return {
          requestId,
          success: false,
          errorMessage: "SessionId not found in response",
        };
      }

      // ResourceUrl is optional in CreateMcpSession response
      const resourceUrl = data.resourceUrl;

      log("session_id =", sessionId);
      log("resource_url =", resourceUrl);

      const session = new Session(this, sessionId);
      if (resourceUrl) {
        session.resourceUrl = resourceUrl;
      }

      this.sessions.set(session.sessionId, session);

      // If we have persistence data, wait for context synchronization
      if (hasPersistenceData) {
        log("Waiting for context synchronization to complete...");

        // Wait for context synchronization to complete
        const maxRetries = 150; // Maximum number of retries
        const retryInterval = 2000; // Milliseconds to wait between retries

        for (let retry = 0; retry < maxRetries; retry++) {
          try {
            // Get context status data
            const infoResult = await session.context.info();

            // Check if all context items have status "Success" or "Failed"
            let allCompleted = true;
            let hasFailure = false;

            for (const item of infoResult.contextStatusData) {
              log(`Context ${item.contextId} status: ${item.status}, path: ${item.path}`);

              if (item.status !== "Success" && item.status !== "Failed") {
                allCompleted = false;
                break;
              }
              
              if (item.status === "Failed") {
                hasFailure = true;
                logError(`Context synchronization failed for ${item.contextId}: ${item.errorMessage}`);
              }
            }

            if (allCompleted || infoResult.contextStatusData.length === 0) {
              if (hasFailure) {
                log("Context synchronization completed with failures");
              } else {
                log("Context synchronization completed successfully");
              }
              break;
            }

            log(`Waiting for context synchronization, attempt ${retry+1}/${maxRetries}`);
            await new Promise(resolve => setTimeout(resolve, retryInterval));
          } catch (error) {
            logError(`Error checking context status on attempt ${retry+1}: ${error}`);
            await new Promise(resolve => setTimeout(resolve, retryInterval));
          }
        }
      }

      // Return SessionResult with request ID
      return {
        requestId,
        success: true,
        session,
      };
    } catch (error) {
      logError("Error calling create_mcp_session:", error);
      return {
        requestId: "",
        success: false,
        errorMessage: `Failed to create session: ${error}`,
      };
    }
  }

  /**
   * List all available sessions.
   *
   * @returns A list of session objects.
   */
  list(): Session[] {
    return Array.from(this.sessions.values());
  }

  /**
   * List sessions filtered by the provided labels with pagination support.
   * It returns sessions that match all the specified labels.
   *
   * **Breaking Change**: This method currently only accepts ListSessionParams parameters，
   *
   * @param params - Parameters including labels and pagination options (required)
   * @returns API response with sessions list and pagination info
   */
  async listByLabels(params?: ListSessionParams): Promise<SessionListResult> {
    if (!params) {
      params = {
        maxResults: 10,
        labels: {},
      };
    }

    try {
      // Convert labels to JSON
      const labelsJSON = JSON.stringify(params.labels);

      //Build request object with support for pagination parameters
      const listSessionRequest = new ListSessionRequest({
        authorization: `Bearer ${this.apiKey}`,
        labels: labelsJSON,
        maxResults: params.maxResults || 10,
        ...(params.nextToken && { nextToken: params.nextToken }),
      });

      log("API Call: ListSession");
      log(
        `Request: Labels=${labelsJSON}, MaxResults=${params.maxResults || 10}${
          params.nextToken ? `, NextToken=${params.nextToken}` : ""
        }`
      );

      const response = await this.client.listSession(listSessionRequest);
      const body = response.body;
      const requestId = extractRequestId(body?.requestId) || "";

      // Check for errors in the response
      if (
        body?.data &&
        typeof body.data === "object" &&
        body.success &&
        body.success !== true
      ) {
        return {
          requestId,
          success: false,
          errorMessage: "Failed to list sessions by labels",
          data: [],
          nextToken: "",
          maxResults: params.maxResults || 10,
          totalCount: 0,
        };
      }

      const sessions: Session[] = [];
      let nextToken = "";
      let maxResults = params.maxResults || 10;
      let totalCount = 0;

      log("body =", body);

      // Extract pagination information
      if (body && typeof body === "object") {
        nextToken = body.nextToken || "";
        maxResults = parseInt(String(body.maxResults || 0)) || maxResults;
        totalCount = parseInt(String(body.totalCount || 0));
      }

      // Extract session data
      const responseData = body?.data;

      // Handle both list and dict responses
      if (Array.isArray(responseData)) {
        // Data is a list of session objects
        for (const sessionData of responseData) {
          if (sessionData && typeof sessionData === "object") {
            const sessionId = (sessionData as any).sessionId; // Capital S and I to match Python
            if (sessionId) {
              // Check if we already have this session in our cache
              let session = this.sessions.get(sessionId);
              if (!session) {
                // Create a new session object
                session = new Session(this, sessionId);
                this.sessions.set(sessionId, session);
              }
              sessions.push(session);
            }
          }
        }
      }

      // Return SessionListResult with request ID and pagination info
      return {
        requestId,
        success: true,
        data: sessions,
        nextToken,
        maxResults,
        totalCount,
      };
    } catch (error) {
      logError("Error calling list_session:", error);
      return {
        requestId: "",
        success: false,
        data: [],
        errorMessage: `Failed to list sessions by labels: ${error}`,
      };
    }
  }

  /**
   * Delete a session by session object.
   *
   * @param session - The session to delete.
   * @param syncContext - Whether to sync context data (trigger file uploads) before deleting the session. Defaults to false.
   * @returns DeleteResult indicating success or failure and request ID
   */
  async delete(session: Session, syncContext = false): Promise<DeleteResult> {
    try {
      // Delete the session and get the result
      const deleteResult = await session.delete(syncContext);

      this.sessions.delete(session.sessionId);

      // Return the DeleteResult obtained from session.delete()
      return deleteResult;
    } catch (error) {
      logError("Error deleting session:", error);
      return {
        requestId: "",
        success: false,
        errorMessage: `Failed to delete session ${session.sessionId}: ${error}`,
      };
    }
  }

  /**
   *
   * @param sessionId - The ID of the session to remove.
   */
  public removeSession(sessionId: string): void {
    this.sessions.delete(sessionId);
  }

  // For internal use by the Session class
  getClient(): Client {
    return this.client;
  }

  getAPIKey(): string {
    return this.apiKey;
  }
}

/**
 * Creates a new AgentBay client using default configuration.
 * This is a convenience function that allows creating an AgentBay instance without a config parameter.
 *
 * @param apiKey - API key for authentication
 * @returns A new AgentBay instance with default configuration
 */
export function newAgentBayWithDefaults(apiKey: string): AgentBay {
  return new AgentBay({ apiKey });
}
