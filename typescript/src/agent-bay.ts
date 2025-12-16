import { $OpenApiUtil } from "@alicloud/openapi-core";
import "dotenv/config";
import * as fs from "fs";
import * as path from "path";
import * as dotenv from "dotenv";
import * as $_client from "./api";
import { ListSessionRequest, CreateMcpSessionRequestPersistenceDataList, GetSessionRequest as $GetSessionRequest } from "./api/models/model";
import { Client } from "./api/client";

import { Config, BROWSER_RECORD_PATH, loadConfig, loadDotEnvWithFallback } from "./config";
import { ContextService } from "./context";
import { ContextSync } from "./context-sync";
import { APIError, AuthenticationError } from "./exceptions";
import { Session } from "./session";
import { BrowserContext,CreateSessionParams } from "./session-params";
import { Context } from "./context";
import { ExtraConfigs } from "./types/extra-configs";
import {
  DeleteResult,
  extractRequestId,
  GetSessionResult as $GetSessionResult,
  SessionResult,
} from "./types/api-response";
import {
  ListSessionParams,
  SessionListResult,
} from "./types/list-session-params";
import {
  log,
  logError,
  logInfo,
  logDebug,
  logAPICall,
  logAPIResponseWithDetails,
  maskSensitiveData,
  setRequestId,
  getRequestId,
  logInfoWithColor,
  logWarn,
} from "./utils/logger";
import { VERSION, IS_RELEASE } from "./version";

// Browser data path constant (moved from config.ts)
const BROWSER_DATA_PATH = "/tmp/agentbay_browser";


/**
 * Parameters for creating a session.
 */
export interface CreateSeesionWithParams {
  labels?: Record<string, string>;
  imageId?: string;
  contextSync?: ContextSync[];
  browserContext?: BrowserContext;
  isVpc?: boolean;
  policyId?: string;
  enableBrowserReplay?: boolean;
  extraConfigs?: ExtraConfigs;
  framework?: string;
}

/**
 * Main class for interacting with the AgentBay cloud runtime environment.
 */
export class AgentBay {
  private apiKey: string;
  public client: Client;
  private endpoint: string;
  private config: Config;

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
   * @param options.envFile - Custom path to .env file. If not provided, will search upward from current directory.
   */
  constructor(
    options: {
      apiKey?: string;
      config?: Config;
      envFile?: string;
    } = {}
  ) {
    // Load .env file first to ensure AGENTBAY_API_KEY is available
    loadDotEnvWithFallback(options.envFile);

    this.apiKey = options.apiKey || process.env.AGENTBAY_API_KEY || "";

    if (!this.apiKey) {
      throw new AuthenticationError(
        "API key is required. Provide it as a parameter or set the AGENTBAY_API_KEY environment variable."
      );
    }

    this.config = loadConfig(options.config, options.envFile);

    // Load configuration using the enhanced loadConfig function
    const configData = loadConfig(options.config, options.envFile);
    this.endpoint = configData.endpoint;

    const config = new $OpenApiUtil.Config({
      regionId: "",
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
   * Get the region ID.
   * @returns The region ID or undefined if not set.
   */
  getRegionId(): string | undefined {
    return this.config.region_id;
  }

  /**
   * Wait for mobile simulate command to complete.
   *
   * @param session - The session to wait for mobile simulate
   * @param mobileSimPath - The dev info path to the mobile simulate
   * @param mobileSimMode - The mode of the mobile simulate. If not provided, will use the default mode.
   */
  private async _waitForMobileSimulate(
    session: Session,
    mobileSimPath: string,
    mobileSimMode?: string
  ): Promise<void> {
    log("⏳ Mobile simulate: Waiting for completion");

    if (!(session as any).mobile) {
      logInfo("Mobile module not found in session, skipping mobile simulate");
      return;
    }
    if (!(session as any).command) {
      logInfo("Command module not found in session, skipping mobile simulate");
      return;
    }
    if (!mobileSimPath) {
      logInfo("Mobile simulate path is empty, skipping mobile simulate");
      return;
    }

    try {
      // Run mobile simulate command
      const startTime = Date.now();
      const devInfoFilePath = `${mobileSimPath}/dev_info.json`;
      let wyaApplyOption = "";

      if (!mobileSimMode || mobileSimMode === "PropertiesOnly") {
        wyaApplyOption = "";
      } else if (mobileSimMode === "SensorsOnly") {
        wyaApplyOption = "-sensors";
      } else if (mobileSimMode === "PackagesOnly") {
        wyaApplyOption = "-packages";
      } else if (mobileSimMode === "ServicesOnly") {
        wyaApplyOption = "-services";
      } else if (mobileSimMode === "All") {
        wyaApplyOption = "-all";
      }

      const command = `chmod -R a+rwx ${mobileSimPath}; wya apply ${wyaApplyOption} ${devInfoFilePath}`.trim();
      logInfo(`ℹ️  ⏳ Waiting for mobile simulate completion, command: [${command}]`);

      const cmdResult = await (session as any).command.executeCommand(command);
      if (cmdResult.success) {
        const endTime = Date.now();
        const consumeTime = (endTime - startTime) / 1000;
        log(`✅ Mobile simulate completed with mode: ${mobileSimMode || 'PropertiesOnly'}, duration: ${consumeTime.toFixed(2)} seconds`);
        if (cmdResult.output) {
          log(`   Output: ${cmdResult.output.trim()}`);
        }
      } else {
        logInfo(`Failed to execute mobile simulate command: ${cmdResult.errorMessage}`);
      }
    } catch (error) {
      logInfo(`Error executing mobile simulate command: ${error}`);
    }
  }


  /**
   * Create a new session in the AgentBay cloud environment.
   *
   * @param params - Optional parameters for creating the session
   * @returns SessionResult containing the created session and request ID
   */
  /**
   * Creates a new AgentBay session with specified configuration.
   *
   * @param params - Configuration parameters for the session:
   *                 - labels: Key-value pairs for session metadata
   *                 - imageId: Custom image ID for the session environment
   *                 - contextSync: Array of context synchronization configurations
   *                 - browserContext: Browser-specific context configuration
   *                 - isVpc: Whether to create a VPC session
   *                 - policyId: Security policy ID
   *                 - enableBrowserReplay: Enable browser session recording
   *                 - extraConfigs: Additional configuration options
   *                 - framework: Framework identifier for tracking
   *
   * @returns Promise resolving to SessionResult containing:
   *          - success: Whether session creation succeeded
   *          - session: Session object for interacting with the environment
   *          - requestId: Unique identifier for this API request
   *          - errorMessage: Error description if creation failed
   *
   * @throws Error if API call fails or authentication is invalid.
   *
   * @example
   * ```typescript
   * const agentBay = new AgentBay({ apiKey: 'your_api_key' });
   * const result = await agentBay.create({ labels: { project: 'demo' } });
   * if (result.success) {
   *   await result.session.filesystem.readFile('/etc/hostname');
   *   await result.session.delete();
   * }
   * ```
   *
   * @remarks
   * **Behavior:**
   * - Creates a new isolated cloud runtime environment
   * - Automatically creates file transfer context if not provided
   * - Waits for context synchronization if contextSync is specified
   * - For VPC sessions, includes VPC-specific configuration
   * - Browser replay creates a separate recording context
   *
   * @see {@link get}, {@link list}, {@link Session.delete}
   */
  async create(params: CreateSessionParams | CreateSeesionWithParams): Promise<SessionResult> {
    try {
      logDebug(`default context syncs length: ${params.contextSync?.length}`);

      // Add context syncs for mobile simulate if provided
      if (params.extraConfigs?.mobile?.simulateConfig) {
        const mobileSimContextId = params.extraConfigs.mobile.simulateConfig.simulatedContextId;
        if (mobileSimContextId) {
          const mobileSimContextSync = new ContextSync(
            mobileSimContextId,
            "/data/agentbay_mobile_info"
          );
          if (!params.contextSync) {
            params.contextSync = [];
          }
          logInfo(`Adding context sync for mobile simulate: ${JSON.stringify(mobileSimContextSync)}`);
          params.contextSync.push(mobileSimContextSync);
        }
      }

      const request = new $_client.CreateMcpSessionRequest({
        authorization: "Bearer " + this.apiKey,
      });

      // browser replay is enabled by default, so if enableBrowserReplay is False, set enableRecord to False
      if (params.enableBrowserReplay === false) {
        request.enableRecord = false;
      }

      // Add SDK stats for tracking
      const framework = params?.framework || "";
      const sdkStatsJson = `{"source":"sdk","sdk_language":"typescript","sdk_version":"${VERSION}","is_release":${IS_RELEASE},"framework":"${framework}"}`;
      request.sdkStats = sdkStatsJson;

      // Add LoginRegionId if region_id is set
      if (this.config.region_id) {
        request.loginRegionId = this.config.region_id;
      }

      // Add labels if provided
      if (params.labels) {
        request.labels = JSON.stringify(params.labels);
      }

      // Add image_id if provided
      if (params.imageId) {
        request.imageId = params.imageId;
      }

      // Add PolicyId if provided
      if (params.policyId) {
        request.mcpPolicyId = params.policyId;
      }

      // Add VPC resource if specified
      request.vpcResource = params.isVpc || false;

      // Flag to indicate if we need to wait for context synchronization
      let needsContextSync = false;

      // Flag to indicate if we need to wait for mobile simulate
      let needsMobileSim = false;
      let mobileSimMode: string | undefined = undefined;
      let mobileSimPath: string | undefined = undefined;

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
        needsContextSync = persistenceDataList.length > 0;
      }

      // Add BrowserContext as a ContextSync if provided
      if (params.browserContext) {
        // Create a simple sync policy for browser context
        const syncPolicy = {
          uploadPolicy: { autoUpload: params.browserContext.autoUpload },
          downloadPolicy: null,
          deletePolicy: null,
          bwList: null,
          recyclePolicy: null,
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
        needsContextSync = true;
      }

      // Add extra configs if provided
      if (params.extraConfigs) {
        request.extraConfigs = JSON.stringify(params.extraConfigs);

        // Check mobile simulate config
        if (params.extraConfigs.mobile?.simulateConfig?.simulate) {
          mobileSimPath = params.extraConfigs.mobile.simulateConfig.simulatePath;
          if (!mobileSimPath) {
            logInfo("mobile_sim_path is not set now, skip mobile simulate operation");
          } else {
            needsMobileSim = true;
            mobileSimMode = params.extraConfigs.mobile.simulateConfig.simulateMode;
          }
        }
      }

      // Log API request
      logAPICall("CreateMcpSession", {
        labels: params.labels,
        imageId: params.imageId,
        policyId: params.policyId,
        isVpc: params.isVpc,
        persistenceDataCount: params.contextSync ? params.contextSync.length : 0,
      });

      const response = await this.client.createMcpSession(request);

      // Extract request ID
      const requestId = extractRequestId(response) || "";
      setRequestId(requestId);

      const sessionData = response.body;

      if (!sessionData || typeof sessionData !== "object") {
        logAPIResponseWithDetails(
          "CreateMcpSession",
          requestId,
          false,
          {},
          "Invalid response format: expected a dictionary"
        );
        logDebug("Full response:", JSON.stringify(sessionData, null, 2));
        return {
          requestId,
          success: false,
          errorMessage: "Invalid response format: expected a dictionary",
        };
      }

      // Check for API-level errors
      if (sessionData.success === false && sessionData.code) {
        const errorMessage = `[${sessionData.code}] ${sessionData.message || 'Unknown error'}`;
        logAPIResponseWithDetails(
          "CreateMcpSession",
          requestId,
          false,
          {},
          errorMessage
        );
        logDebug("Full response:", JSON.stringify(sessionData, null, 2));
        return {
          requestId,
          success: false,
          errorMessage,
        };
      }

      const data = sessionData.data;
      if (!data || typeof data !== "object") {
        logAPIResponseWithDetails(
          "CreateMcpSession",
          requestId,
          false,
          {},
          "Invalid response format: 'data' field is not a dictionary"
        );
        logDebug("Full response:", JSON.stringify(sessionData, null, 2));
        return {
          requestId,
          success: false,
          errorMessage:
            "Invalid response format: 'data' field is not a dictionary",
        };
      }

      // Check data-level success field (business logic success)
      if (data.success === false) {
        const errorMessage = data.errMsg || "Session creation failed";
        logAPIResponseWithDetails(
          "CreateMcpSession",
          requestId,
          false,
          {},
          errorMessage
        );
        logDebug("Full response:", JSON.stringify(sessionData, null, 2));
        return {
          requestId,
          success: false,
          errorMessage,
        };
      }

      const sessionId = data.sessionId;
      if (!sessionId) {
        logAPIResponseWithDetails(
          "CreateMcpSession",
          requestId,
          false,
          {},
          "SessionId not found in response"
        );
        logDebug("Full response:", JSON.stringify(sessionData, null, 2));
        return {
          requestId,
          success: false,
          errorMessage: "SessionId not found in response",
        };
      }

      // ResourceUrl is optional in CreateMcpSession response
      const resourceUrl = data.resourceUrl || "";

      logAPIResponseWithDetails(
        "CreateMcpSession",
        requestId,
        true,
        {
          sessionId,
          resourceUrl,
        }
      );

      const session = new Session(this, sessionId);

      // Set VPC-related information from response
      session.isVpc = params.isVpc || false;
      if (data.networkInterfaceIp) {
        session.networkInterfaceIp = data.networkInterfaceIp;
      }
      if (data.httpPort) {
        session.httpPort = data.httpPort;
      }
      if (data.token) {
        session.token = data.token;
      }

      // Set ResourceUrl
      session.resourceUrl = resourceUrl;

      // Set browser recording state
      session.enableBrowserReplay = params.enableBrowserReplay || false;

      // Store imageId used for this session
      (session as any).imageId = params.imageId;

      // Apply mobile configuration if provided
      if (params.extraConfigs && params.extraConfigs.mobile) {
        log("Applying mobile configuration...");
        try {
          const configResult = await session.mobile.configure(params.extraConfigs.mobile);
          if (configResult.success) {
            log("Mobile configuration applied successfully");
          } else {
            logError(`Warning: Failed to apply mobile configuration: ${configResult.errorMessage}`);
            // Continue with session creation even if mobile config fails
          }
        } catch (error) {
          logError(`Warning: Failed to apply mobile configuration: ${error}`);
          // Continue with session creation even if mobile config fails
        }
      }

      // For VPC sessions, automatically fetch MCP tools information
      if (params.isVpc) {
        logDebug("VPC session detected, automatically fetching MCP tools...");
        try {
          const toolsResult = await session.listMcpTools();
          logDebug(`Successfully fetched ${toolsResult.tools.length} MCP tools for VPC session (RequestID: ${toolsResult.requestId})`);
        } catch (error) {
          logError(`Warning: Failed to fetch MCP tools for VPC session: ${error}`);
          // Continue with session creation even if tools fetch fails
        }
      }

      // If we have persistence data, wait for context synchronization
      if (needsContextSync) {
        logDebug("Waiting for context synchronization to complete...");

        // Wait for context synchronization to complete
        const maxRetries = 150; // Maximum number of retries
        const retryInterval = 1500; // Milliseconds to wait between retries

        for (let retry = 0; retry < maxRetries; retry++) {
          try {
            // Get context status data
            const infoResult = await session.context.info();

            // Check if all context items have status "Success" or "Failed"
            let allCompleted = true;
            let hasFailure = false;

            for (const item of infoResult.contextStatusData) {
              logDebug(`Context ${item.contextId} status: ${item.status}, path: ${item.path}`);

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
                logDebug("Context synchronization completed with failures");
              } else {
                logDebug("Context synchronization completed successfully");
              }
              break;
            }

            logDebug(`Waiting for context synchronization, attempt ${retry+1}/${maxRetries}`);
            await new Promise(resolve => setTimeout(resolve, retryInterval));
          } catch (error) {
            logError(`Error checking context status on attempt ${retry+1}: ${error}`);
            await new Promise(resolve => setTimeout(resolve, retryInterval));
          }
        }
      }

      // If we need to do mobile simulate by command, wait for it
      if (needsMobileSim && mobileSimPath) {
        await this._waitForMobileSimulate(session, mobileSimPath, mobileSimMode);
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
   * Returns paginated list of session IDs filtered by labels.
   *
   * @param labels - Optional labels to filter sessions (defaults to empty object)
   * @param page - Optional page number for pagination (starting from 1, defaults to 1)
   * @param limit - Optional maximum number of items per page (defaults to 10)
   * @returns SessionListResult - Paginated list of session IDs that match the labels
   *
   * @example
   * ```typescript
   * const agentBay = new AgentBay({ apiKey: "your_api_key" });
   * const result = await agentBay.list({ project: "demo" }, 1, 10);
   * if (result.success) {
   *   console.log(`Found ${result.sessionIds.length} sessions`);
   * }
   * ```
   */
  async list(
    labels: Record<string, string> = {},
    page?: number,
    limit = 10
  ): Promise<SessionListResult> {
    try {
      // Validate page number
      if (page !== undefined && page < 1) {
        return {
          requestId: "",
          success: false,
          errorMessage: `Cannot reach page ${page}: Page number must be >= 1`,
          sessionIds: [],
          nextToken: "",
          maxResults: limit,
          totalCount: 0,
        };
      }

      // Calculate next_token based on page number
      // Page 1 or undefined means no next_token (first page)
      // For page > 1, we need to make multiple requests to get to that page
      let nextToken = "";
      if (page !== undefined && page > 1) {
        // We need to fetch pages 1 through page-1 to get the next_token
        let currentPage = 1;
        while (currentPage < page) {
          // Make API call to get next_token
          const request = new ListSessionRequest({
            authorization: `Bearer ${this.apiKey}`,
            labels: JSON.stringify(labels),
            maxResults: limit,
          });
          if (nextToken) {
            request.nextToken = nextToken;
          }

          const response = await this.client.listSession(request);
          const requestId = extractRequestId(response) || "";

          if (!response.body?.success) {
            const code = response.body?.code || "Unknown";
            const message = response.body?.message || "Unknown error";
            return {
              requestId,
              success: false,
              errorMessage: `[${code}] ${message}`,
              sessionIds: [],
              nextToken: "",
              maxResults: limit,
              totalCount: 0,
            };
          }

          nextToken = response.body.nextToken || "";
          if (!nextToken) {
            // No more pages available
            return {
              requestId,
              success: false,
              errorMessage: `Cannot reach page ${page}: No more pages available`,
              sessionIds: [],
              nextToken: "",
              maxResults: limit,
              totalCount: response.body.totalCount || 0,
            };
          }
          currentPage += 1;
        }
      }

      // Make the actual request for the desired page
      const request = new ListSessionRequest({
        authorization: `Bearer ${this.apiKey}`,
        labels: JSON.stringify(labels),
        maxResults: limit,
      });
      if (nextToken) {
        request.nextToken = nextToken;
      }

      // Log API request
      logAPICall("ListSession", {
        labels,
        maxResults: limit,
        nextToken: nextToken || undefined,
      });

      const response = await this.client.listSession(request);

      // Extract request ID
      const requestId = extractRequestId(response) || "";
      setRequestId(requestId);

      // Check for errors in the response
      if (!response.body?.success) {
        const code = response.body?.code || "Unknown";
        const message = response.body?.message || "Unknown error";
        logAPIResponseWithDetails(
          "ListSession",
          requestId,
          false,
          {},
          `[${code}] ${message}`
        );
        logDebug("Full ListSession response:", JSON.stringify(response.body, null, 2));
        return {
          requestId,
          success: false,
          errorMessage: `[${code}] ${message}`,
          sessionIds: [],
          nextToken: "",
          maxResults: limit,
          totalCount: 0,
        };
      }

      const sessionIds: string[] = [];

      // Extract session data
      if (response.body.data) {
        for (const sessionData of response.body.data) {
          if (sessionData.sessionId) {
            sessionIds.push(sessionData.sessionId);
          }
        }
      }

      logAPIResponseWithDetails(
        "ListSession",
        requestId,
        true,
        {
          sessionCount: sessionIds.length,
          totalCount: response.body.totalCount || 0,
          maxResults: response.body.maxResults || limit,
        }
      );

      // Return SessionListResult with request ID and pagination info
      return {
        requestId,
        success: true,
        sessionIds,
        nextToken: response.body.nextToken || "",
        maxResults: response.body.maxResults || limit,
        totalCount: response.body.totalCount || 0,
      };
    } catch (error) {
      logError("Error calling list_session:", error);
      return {
        requestId: "",
        success: false,
        errorMessage: `Failed to list sessions: ${error}`,
        sessionIds: [],
      };
    }
  }

  /**
   * Delete a session by session object.
   *
   * @param session - The session to delete.
   * @param syncContext - Whether to sync context data (trigger file uploads) before deleting the session. Defaults to false.
   * @returns DeleteResult indicating success or failure and request ID
   *
   * @example
   * ```typescript
   * const agentBay = new AgentBay({ apiKey: 'your_api_key' });
   * const result = await agentBay.create();
   * if (result.success) {
   *   await agentBay.delete(result.session);
   * }
   * ```
   */
  async delete(session: Session, syncContext = false): Promise<DeleteResult> {
    try {
      // Delete the session and get the result
      logAPICall("DeleteSession", { sessionId: session.sessionId });
      const deleteResult = await session.delete(syncContext);

      logAPIResponseWithDetails(
        "DeleteSession",
        deleteResult.requestId,
        deleteResult.success,
        { sessionId: session.sessionId }
      );

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
   * Get session information by session ID.
   *
   * @param sessionId - The ID of the session to retrieve.
   * @returns GetSessionResult containing session information
   */
  async getSession(sessionId: string): Promise<$GetSessionResult> {
    try {
      logAPICall("GetSession", { sessionId });

      const request = new $GetSessionRequest({
        authorization: `Bearer ${this.apiKey}`,
        sessionId: sessionId,
      });

      const response = await this.client.getSession(request);
      const requestId = extractRequestId(response) || "";
      const body = response.body;

      setRequestId(requestId);

      // Check for API-level errors
      if (body?.success === false && body.code) {
        logAPIResponseWithDetails(
          "GetSession",
          requestId,
          false,
          {},
          `[${body.code}] ${body.message || 'Unknown error'}`
        );
        logDebug("Full GetSession response:", JSON.stringify(body, null, 2));
        return {
          requestId,
          httpStatusCode: body.httpStatusCode || 0,
          code: body.code,
          success: false,
          errorMessage: `[${body.code}] ${body.message || 'Unknown error'}`,
        };
      }

      const result: $GetSessionResult = {
        requestId,
        httpStatusCode: body?.httpStatusCode || 0,
        code: body?.code || "",
        success: body?.success || false,
        errorMessage: "",
      };

      if (body?.data) {
        // Extract contexts list from response
        const contextsList = body.data.contexts || [];
        const contexts: Array<{ name: string; id: string }> = [];
        if (Array.isArray(contextsList)) {
          for (const ctx of contextsList) {
            if (ctx && typeof ctx === 'object' && ctx.name && ctx.id) {
              contexts.push({
                name: ctx.name,
                id: ctx.id,
              });
            }
          }
        }

        result.data = {
          appInstanceId: body.data.appInstanceId || "",
          resourceId: body.data.resourceId || "",
          sessionId: body.data.sessionId || "",
          success: body.data.success || false,
          httpPort: body.data.httpPort || "",
          networkInterfaceIp: body.data.networkInterfaceIp || "",
          token: body.data.token || "",
          vpcResource: body.data.vpcResource || false,
          resourceUrl: body.data.resourceUrl || "",
          status: body.data.status || "",
          contexts: contexts.length > 0 ? contexts : undefined,
        };

        logAPIResponseWithDetails(
          "GetSession",
          requestId,
          true,
          {
            sessionId: result.data.sessionId,
            resourceId: result.data.resourceId,
            httpPort: result.data.httpPort,
          }
        );
      }

      return result;
    } catch (error: any) {
      // Check if this is an expected business error (e.g., session not found)
      const errorStr = String(error);
      const errorCode = error?.data?.Code || error?.code || "";

      if (errorCode === "InvalidMcpSession.NotFound" || errorStr.includes("NotFound")) {
        // This is an expected error - session doesn't exist
        // Use info level logging without stack trace, but with red color for visibility
        logInfo(`Session not found: ${sessionId}`);
        logDebug(`GetSession error details: ${errorStr}`);
        return {
          requestId: "",
          httpStatusCode: 400,
          code: "InvalidMcpSession.NotFound",
          success: false,
          errorMessage: `Session ${sessionId} not found`,
        };
      } else {
        // This is an unexpected error - log with full error
        logError("Error calling GetSession:", error);
        return {
          requestId: "",
          httpStatusCode: 0,
          code: "",
          success: false,
          errorMessage: `Failed to get session ${sessionId}: ${error}`,
        };
      }
    }
  }

  /**
   * Get a session by its ID.
   *
   * This method retrieves a session by calling the GetSession API
   * and returns a SessionResult containing the Session object and request ID.
   *
   * @param sessionId - The ID of the session to retrieve
   * @returns Promise resolving to SessionResult with the Session instance, request ID, and success status
   *
   * @example
   * ```typescript
   * const agentBay = new AgentBay({ apiKey: 'your_api_key' });
   * const createResult = await agentBay.create();
   * if (createResult.success) {
   *   const result = await agentBay.get(createResult.session.sessionId);
   *   await result.session?.filesystem.readFile('/etc/hostname');
   *   await result.session?.delete();
   * }
   * ```
   */
  async get(sessionId: string): Promise<SessionResult> {
    // Validate input
    if (
      !sessionId ||
      (typeof sessionId === "string" && !sessionId.trim())
    ) {
      return {
        requestId: "",
        success: false,
        errorMessage: "session_id is required",
      };
    }

    // Call GetSession API
    const getResult = await this.getSession(sessionId);

    // Check if the API call was successful
    if (!getResult.success) {
      const errorMsg = getResult.errorMessage || "Unknown error";
      return {
        requestId: getResult.requestId,
        success: false,
        errorMessage: `Failed to get session ${sessionId}: ${errorMsg}`,
      };
    }

    // Create the Session object
    const session = new Session(this, sessionId);

    // Set VPC-related information and ResourceUrl from GetSession response
    if (getResult.data) {
      session.isVpc = getResult.data.vpcResource;
      session.networkInterfaceIp = getResult.data.networkInterfaceIp;
      session.httpPort = getResult.data.httpPort;
      session.token = getResult.data.token;
      session.resourceUrl = getResult.data.resourceUrl;
    }

    return {
      requestId: getResult.requestId,
      success: true,
      session,
    };
  }

  /**
   * Get the internal HTTP client instance.
   *
   * This is primarily for internal use and advanced scenarios where you need direct access
   * to the underlying API client.
   *
   * @returns The Client instance used for API communication
   *
   * @internal
   *
   * @remarks
   * **Note:** This method is primarily for internal use. Most users should interact
   * with the SDK through higher-level methods like `create()`, `get()`, and `list()`.
   */
  getClient(): Client {
    return this.client;
  }

  /**
   * Get the API key used for authentication.
   *
   * @returns The API key string
   *
   * @internal
   *
   * @remarks
   * **Security Note:** Be careful when logging or exposing API keys. Always keep them secure
   * and never commit them to version control.
   */
  getAPIKey(): string {
    return this.apiKey;
  }

  /**
   * Asynchronously pause a session, putting it into a dormant state.
   *
   * This method directly calls the PauseSessionAsync API without waiting for the session
   * to reach the PAUSED state.
   *
   * @param session - The session to pause.
   * @param timeout - Timeout in seconds to wait for the session to pause. Defaults to 600 seconds.
   * @param pollInterval - Interval in seconds between status polls. Defaults to 2.0 seconds.
   * @returns SessionPauseResult indicating success or failure and request ID
   *
   * @example
   * ```typescript
   * const agentBay = new AgentBay({ apiKey: 'your_api_key' });
   * const session = (await agentBay.create()).session;
   * const pauseResult = await agentBay.pauseAsync(session);
   * await agentBay.resumeAsync(session);
   * await session.delete();
   * ```
   *
   * @remarks
   * **Behavior:**
   * - This method does not wait for the session to reach the PAUSED state
   * - It only submits the pause request to the API
   * - The session state transitions from RUNNING -> PAUSING -> PAUSED
   * - Paused sessions consume fewer resources but maintain their state
   *
   * @see {@link resumeAsync}, {@link Session.pauseAsync}
   */
  async pauseAsync(session: Session, timeout = 600, pollInterval = 2.0): Promise<import("./types/api-response").SessionPauseResult> {
    try {
      // Call session's pause_async method directly
      return await session.pauseAsync(timeout, pollInterval);
    } catch (error) {
      logError("Error calling pause session async:", error);
      return {
        requestId: "",
        success: false,
        errorMessage: `Failed to pause session ${session.sessionId}: ${error}`,
      };
    }
  }

  /**
   * Asynchronously resume a session from a paused state.
   *
   * This method directly calls the ResumeSessionAsync API without waiting for the session
   * to reach the RUNNING state.
   *
   * @param session - The session to resume.
   * @param timeout - Timeout in seconds to wait for the session to resume. Defaults to 600 seconds.
   * @param pollInterval - Interval in seconds between status polls. Defaults to 2.0 seconds.
   * @returns SessionResumeResult indicating success or failure and request ID
   *
   * @example
   * ```typescript
   * const agentBay = new AgentBay({ apiKey: 'your_api_key' });
   * const session = (await agentBay.create()).session;
   * await agentBay.pauseAsync(session);
   * const resumeResult = await agentBay.resumeAsync(session);
   * await session.delete();
   * ```
   *
   * @remarks
   * **Behavior:**
   * - This method does not wait for the session to reach the RUNNING state
   * - It only submits the resume request to the API
   * - The session state transitions from PAUSED -> RESUMING -> RUNNING
   * - Only sessions in PAUSED state can be resumed
   *
   * @see {@link pauseAsync}, {@link Session.resumeAsync}
   */
  async resumeAsync(session: Session, timeout = 600, pollInterval = 2.0): Promise<import("./types/api-response").SessionResumeResult> {
    try {
      // Call session's resume_async method directly
      return await session.resumeAsync(timeout, pollInterval);
    } catch (error) {
      logError("Error calling resume session async:", error);
      return {
        requestId: "",
        success: false,
        errorMessage: `Failed to resume session ${session.sessionId}: ${error}`,
      };
    }
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
