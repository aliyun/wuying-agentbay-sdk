import { $OpenApiUtil } from "@alicloud/openapi-core";
import "dotenv/config";
import * as $_client from "./api";
import { ListSessionRequest } from "./api/models/model";
import { Client } from "./api/client";

import { loadConfig, Config } from "./config";
import { ContextService } from "./context";
import { APIError, AuthenticationError } from "./exceptions";
import { Session } from "./session";

import {
  ApiResponseWithData,
  DeleteResult,
  extractRequestId,
} from "./types/api-response";
import {
  ListSessionParams,
  SessionListResult,
} from "./types/list-session-params";
import { log, logError } from "./utils/logger";

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
   * @param options - Optional parameters for creating the session
   * @param options.contextId - ID of the context to bind to the session
   * @param options.labels - Custom labels for the session
   * @returns API response with session data and requestId
   */
  async create(
    options: {
      contextId?: string;
      labels?: Record<string, string>;
      imageId?: string;
    } = {}
  ): Promise<ApiResponseWithData<Session>> {
    try {
      const createSessionRequest = new $_client.CreateMcpSessionRequest({
        authorization: "Bearer " + this.apiKey,
        imageId: options.imageId,
      });

      // Add context_id if provided
      if (options.contextId) {
        createSessionRequest.contextId = options.contextId;
      }

      // Add labels if provided
      if (options.labels) {
        createSessionRequest.labels = JSON.stringify(options.labels);
      }

      // Log API request
      log("API Call: CreateMcpSession");
      log(
        `Request: ${
          options.contextId ? `ContextId=${options.contextId}, ` : ""
        }${options.labels ? `Labels=${JSON.stringify(options.labels)}, ` : ""}${
          options.imageId ? `ImageId=${options.imageId}` : ""
        }`
      );

      const response = await this.client.createMcpSession(createSessionRequest);

      // Log API response
      log(`Response from CreateMcpSession:`, response.body);

      const sessionId = response.body?.data?.sessionId;
      if (!sessionId) {
        throw new APIError("Invalid session ID in response");
      }

      // ResourceUrl is optional in CreateMcpSession response
      const resourceUrl = response.body?.data?.resourceUrl;

      const session = new Session(this, sessionId);
      if (resourceUrl) {
        session.resourceUrl = resourceUrl;
      }

      this.sessions.set(session.sessionId, session);

      return {
        requestId: extractRequestId(response),
        data: session,
      };
    } catch (error) {
      logError("Error calling CreateMcpSession:", error);
      throw new APIError(`Failed to create session: ${error}`);
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

      // Log API response
      log(`Response from ListSession:`, response.body);

      const sessions: Session[] = [];
      if (response.body?.data) {
        for (const sessionData of response.body.data) {
          if (sessionData.sessionId) {
            const session = new Session(this, sessionData.sessionId);
            sessions.push(session);
            // Also store in the local cache
            this.sessions.set(sessionData.sessionId, session);
          }
        }
      }

      return {
        requestId: extractRequestId(response),
        data: sessions,
        nextToken: response.body?.nextToken,
        maxResults: response.body?.maxResults || params.maxResults || 10,
        totalCount: response.body?.totalCount || 0,
      };
    } catch (error) {
      logError("Error calling ListSession:", error);
      throw new APIError(`Failed to list sessions by labels: ${error}`);
    }
  }

  /**
   * Delete a session by ID.
   *
   * @param session - The session to delete.
   * @returns API response with requestId
   */
  async delete(session: Session): Promise<DeleteResult> {
    const getSession = this.sessions.get(session.sessionId);
    if (!getSession) {
      throw new Error(`Session with ID ${session.sessionId} not found`);
    }

    try {
      const deleteResponse = await session.delete();
      return deleteResponse;
    } catch (error) {
      throw new APIError(`Failed to delete session: ${error}`);
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
