import { AgentBay } from "./agent-bay";
import { APIError } from "./exceptions";
import * as $_client from "./api";
import {
  log,
  logError,
  logInfo,
  logDebug,
  logAPICall,
  logAPIResponseWithDetails,
  setRequestId,
  getRequestId,
} from "./utils/logger";
import {
  extractRequestId,
  ContextResult,
  ContextListResult,
  OperationResult,
  FileUrlResult,
  ContextFileListResult,
  ContextFileEntry,
  ClearContextResult,
} from "./types/api-response";

/**
 * Represents a persistent storage context in the AgentBay cloud environment.
 */
export class Context {
  /**
   * The unique identifier of the context.
   */
  id: string;

  /**
   * The name of the context.
   */
  name: string;

  /**
   * @deprecated This field is no longer used and will be removed in a future version.
   */
  state: string;

  /**
   * Date and time when the Context was created.
   */
  createdAt?: string;

  /**
   * Date and time when the Context was last used.
   */
  lastUsedAt?: string;

  /**
   * @deprecated This field is no longer used and will be removed in a future version.
   */
  osType?: string;

  /**
   * Initialize a Context object.
   *
   * @param id - The unique identifier of the context.
   * @param name - The name of the context.
   * @param state - **Deprecated.** This parameter is no longer used.
   * @param createdAt - Date and time when the Context was created.
   * @param lastUsedAt - Date and time when the Context was last used.
   * @param osType - **Deprecated.** This parameter is no longer used.
   */
  constructor(
    id: string,
    name: string,
    state = "available",
    createdAt?: string,
    lastUsedAt?: string,
    osType?: string
  ) {
    this.id = id;
    this.name = name;
    this.state = state;
    this.createdAt = createdAt;
    this.lastUsedAt = lastUsedAt;
    this.osType = osType;
  }
}

/**
 * Parameters for listing contexts with pagination support.
 */
export interface ContextListParams {
  /**
   * Maximum number of results per page.
   * Defaults to 10 if not specified.
   */
  maxResults?: number;

  /**
   * Token for the next page of results.
   */
  nextToken?: string;
}

/**
 * Provides methods to manage persistent contexts in the AgentBay cloud environment.
 */
export class ContextService {
  private agentBay: AgentBay;

  /**
   * Initialize the ContextService.
   *
   * @param agentBay - The AgentBay instance.
   */
  constructor(agentBay: AgentBay) {
    this.agentBay = agentBay;
  }

  /**
   * Lists all available contexts with pagination support.
   * Corresponds to Python's list() method
   *
   * @param params - Optional parameters for listing contexts.
   * @returns ContextListResult with contexts list and pagination information
   */
  async list(params?: ContextListParams): Promise<ContextListResult> {
    try {
      // Set default maxResults if not specified
      const maxResults = params?.maxResults !== undefined ? params.maxResults : 10;

      const request = new $_client.ListContextsRequest({
        authorization: `Bearer ${this.agentBay.getAPIKey()}`,
        maxResults: maxResults,
        nextToken: params?.nextToken,
      });

      // Log API request
      logAPICall("ListContexts");
      logDebug(`Request: MaxResults=${maxResults}`, params?.nextToken ? `, NextToken=${params.nextToken}` : "");

      const response = await this.agentBay.getClient().listContexts(request);

      // Extract request ID
      const requestId = extractRequestId(response) || "";

      // Check for API-level errors
      if (response.body?.success === false && response.body?.code) {
        const errorMessage = `[${response.body.code}] ${response.body.message || 'Unknown error'}`;
        const fullResponse = response.body ? JSON.stringify(response.body, null, 2) : "";
        logAPIResponseWithDetails("ListContexts", requestId, false, undefined, fullResponse);
        return {
          requestId,
          success: false,
          contexts: [],
          errorMessage,
        };
      }

      const contexts: Context[] = [];
      if (response.body?.data) {
        for (const contextData of response.body.data) {
          contexts.push(
            new Context(
              contextData.id || "",
              contextData.name || "",
              contextData.state || "available",
              contextData.createTime,
              contextData.lastUsedTime,
              contextData.osType
            )
          );
        }
      }

      // Log API response with key fields
      const keyFields: Record<string, any> = {
        context_count: contexts.length,
        max_results: maxResults,
      };
      if (response.body?.totalCount !== undefined) {
        keyFields.total_count = response.body.totalCount;
      }
      const fullResponse = response.body ? JSON.stringify(response.body, null, 2) : "";
      logAPIResponseWithDetails("ListContexts", requestId, true, keyFields, fullResponse);

      return {
        requestId,
        success: true,
        contexts,
        nextToken: response.body?.nextToken,
        maxResults: response.body?.maxResults || maxResults,
        totalCount: response.body?.totalCount,
      };
    } catch (error) {
      logError("Error calling ListContexts:", error);
      return {
        requestId: "",
        success: false,
        contexts: [],
        errorMessage: `Failed to list contexts: ${error}`,
      };
    }
  }

  /**
   * Gets a context by name. Optionally creates it if it doesn't exist.
   * Corresponds to Python's get() method
   *
   * @param name - The name of the context to get.
   * @param create - Whether to create the context if it doesn't exist.
   * @returns ContextResult with context data and requestId
   */
  async get(name: string, create = false): Promise<ContextResult> {
    try {
      const request = new $_client.GetContextRequest({
        name: name,
        allowCreate: create ? "true" : "false",
        authorization: `Bearer ${this.agentBay.getAPIKey()}`,
      });

      // Log API request
      logAPICall("GetContext");
      logDebug(`Request: Name=${name}, AllowCreate=${create}`);

      const response = await this.agentBay.getClient().getContext(request);

      // Extract request ID
      const requestId = extractRequestId(response) || "";

      // Check for API-level errors
      if (response.body?.success === false && response.body?.code) {
        const errorMessage = `[${response.body.code}] ${response.body.message || 'Unknown error'}`;
        const fullResponse = response.body ? JSON.stringify(response.body, null, 2) : "";
        logAPIResponseWithDetails("GetContext", requestId, false, undefined, fullResponse);
        return {
          requestId,
          success: false,
          contextId: "",
          context: undefined,
          errorMessage,
        };
      }

      const contextId = response.body?.data?.id || "";
      if (!contextId) {
        logAPIResponseWithDetails("GetContext", requestId, false, undefined, "Context ID not found in response");
        return {
          requestId,
          success: false,
          contextId: "",
          context: undefined,
          errorMessage: "Context ID not found in response",
        };
      }

      // Get the full context details
      try {
        const contextsResponse = await this.list();
        for (const context of contextsResponse.contexts) {
          if (context.id === contextId) {
            // Log API response with key fields
            const keyFields: Record<string, any> = {
              context_id: contextId,
              context_name: context.name,
            };
            const fullResponse = response.body ? JSON.stringify(response.body, null, 2) : "";
            logAPIResponseWithDetails("GetContext", requestId, true, keyFields, fullResponse);
            return {
              requestId,
              success: true,
              contextId,
              context,
            };
          }
        }
      } catch (listError) {
        logDebug(`Warning: Failed to get full context details from list: ${listError}`);
      }

      // If we couldn't find the context in the list, create a basic one
      const context = new Context(contextId, name);
      const keyFields: Record<string, any> = {
        context_id: contextId,
        context_name: name,
      };
      const fullResponse = response.body ? JSON.stringify(response.body, null, 2) : "";
      logAPIResponseWithDetails("GetContext", requestId, true, keyFields, fullResponse);
      return {
        requestId,
        success: true,
        contextId,
        context,
      };
    } catch (error) {
      logError("Error calling GetContext:", error);
      return {
        requestId: "",
        success: false,
        contextId: "",
        context: undefined,
        errorMessage: `Failed to get context ${name}: ${error}`,
      };
    }
  }

  /**
   * Creates a new context with the given name.
   * Corresponds to Python's create() method
   *
   * @param name - The name for the new context.
   * @returns ContextResult with created context data and requestId
   */
  async create(name: string): Promise<ContextResult> {
    return await this.get(name, true);
  }

  /**
   * Updates the specified context.
   * Corresponds to Python's update() method
   *
   * @param context - The Context object to update.
   * @returns OperationResult with updated context data and requestId
   */
  async update(context: Context): Promise<OperationResult> {
    try {
      const request = new $_client.ModifyContextRequest({
        id: context.id,
        name: context.name,
        authorization: `Bearer ${this.agentBay.getAPIKey()}`,
      });

      // Log API request
      logAPICall("ModifyContext");
      logDebug(`Request: Id=${context.id}, Name=${context.name}`);

      const response = await this.agentBay.getClient().modifyContext(request);

      // Extract request ID
      const requestId = extractRequestId(response) || "";

      // Check for success (matching Python logic)
      const success = response.body?.success !== false;
      const errorMessage = success
        ? ""
        : `[${response.body?.code || 'Unknown'}] ${response.body?.message || 'Unknown error'}`;

      // Log API response with key fields
      const keyFields: Record<string, any> = {
        context_id: context.id,
        context_name: context.name,
      };
      const fullResponse = response.body ? JSON.stringify(response.body, null, 2) : "";
      logAPIResponseWithDetails("ModifyContext", requestId, success, keyFields, fullResponse);

      return {
        requestId,
        success,
        data: success,
        errorMessage,
      };
    } catch (error) {
      logError("Error calling ModifyContext:", error);
      return {
        requestId: "",
        success: false,
        errorMessage: `Failed to update context ${context.id}: ${error}`,
      };
    }
  }

  /**
   * Deletes the specified context.
   * Corresponds to Python's delete() method
   *
   * @param context - The Context object to delete.
   * @returns OperationResult with requestId
   */
  async delete(context: Context): Promise<OperationResult> {
    try {
      const request = new $_client.DeleteContextRequest({
        id: context.id,
        authorization: `Bearer ${this.agentBay.getAPIKey()}`,
      });

      // Log API request
      logAPICall("DeleteContext");
      logDebug(`Request: Id=${context.id}`);

      const response = await this.agentBay.getClient().deleteContext(request);

      // Extract request ID
      const requestId = extractRequestId(response) || "";

      // Check for success (matching Python logic)
      const success = response.body?.success !== false;
      const errorMessage = success
        ? ""
        : `[${response.body?.code || 'Unknown'}] ${response.body?.message || 'Unknown error'}`;

      // Log API response with key fields
      const keyFields: Record<string, any> = {
        context_id: context.id,
      };
      const fullResponse = response.body ? JSON.stringify(response.body, null, 2) : "";
      logAPIResponseWithDetails("DeleteContext", requestId, success, keyFields, fullResponse);

      return {
        requestId,
        success,
        data: success,
        errorMessage,
      };
    } catch (error) {
      logError("Error calling DeleteContext:", error);
      return {
        requestId: "",
        success: false,
        errorMessage: `Failed to delete context ${context.id}: ${error}`,
      };
    }
  }

  /**
   * Get a presigned upload URL for a file in a context.
   */
  async getFileUploadUrl(contextId: string, filePath: string): Promise<FileUrlResult> {
    logAPICall("GetContextFileUploadUrl");
    logDebug(`Request: ContextId=${contextId}, FilePath=${filePath}`);
    const req = new $_client.GetContextFileUploadUrlRequest({
      authorization: `Bearer ${this.agentBay.getAPIKey()}`,
      contextId,
      filePath,
    });
    const resp = await this.agentBay.getClient().getContextFileUploadUrl(req);
    const requestId = extractRequestId(resp) || "";
    const body = resp.body;

    // Check for API-level errors
    if (body?.success === false && body.code) {
      const errorMessage = `[${body.code}] ${body.message || 'Unknown error'}`;
      const fullResponse = body ? JSON.stringify(body, null, 2) : "";
      logAPIResponseWithDetails("GetContextFileUploadUrl", requestId, false, undefined, fullResponse);
      return {
        requestId,
        success: false,
        url: "",
        expireTime: undefined,
        errorMessage,
      };
    }

    const data = body?.data;
    const success = !!(body && body.success);

    // Log API response with key fields
    const keyFields: Record<string, any> = {
      context_id: contextId,
      file_path: filePath,
    };
    if (data?.expireTime) {
      keyFields.expire_time = data.expireTime;
    }
    const fullResponse = body ? JSON.stringify(body, null, 2) : "";
    logAPIResponseWithDetails("GetContextFileUploadUrl", requestId, success, keyFields, fullResponse);

    return {
      requestId,
      success,
      url: data?.url || "",
      expireTime: data?.expireTime,
      errorMessage: undefined,
    };
  }

  /**
   * Get a presigned download URL for a file in a context.
   */
  async getFileDownloadUrl(contextId: string, filePath: string): Promise<FileUrlResult> {
    logAPICall("GetContextFileDownloadUrl");
    logDebug(`Request: ContextId=${contextId}, FilePath=${filePath}`);
    const req = new $_client.GetContextFileDownloadUrlRequest({
      authorization: `Bearer ${this.agentBay.getAPIKey()}`,
      contextId,
      filePath,
    });
    const resp = await this.agentBay.getClient().getContextFileDownloadUrl(req);
    const requestId = extractRequestId(resp) || "";
    const body = resp.body;

    // Check for API-level errors
    if (body?.success === false && body.code) {
      const errorMessage = `[${body.code}] ${body.message || 'Unknown error'}`;
      const fullResponse = body ? JSON.stringify(body, null, 2) : "";
      logAPIResponseWithDetails("GetContextFileDownloadUrl", requestId, false, undefined, fullResponse);
      return {
        requestId,
        success: false,
        url: "",
        expireTime: undefined,
        errorMessage,
      };
    }

    const data = body?.data;
    const success = !!(body && body.success);

    // Log API response with key fields
    const keyFields: Record<string, any> = {
      context_id: contextId,
      file_path: filePath,
    };
    if (data?.expireTime) {
      keyFields.expire_time = data.expireTime;
    }
    const fullResponse = body ? JSON.stringify(body, null, 2) : "";
    logAPIResponseWithDetails("GetContextFileDownloadUrl", requestId, success, keyFields, fullResponse);

    return {
      requestId,
      success,
      url: data?.url || "",
      expireTime: data?.expireTime,
      errorMessage: undefined,
    };
  }

  /**
   * Delete a file in a context.
   */
  async deleteFile(contextId: string, filePath: string): Promise<OperationResult> {
    logAPICall("DeleteContextFile");
    logDebug(`Request: ContextId=${contextId}, FilePath=${filePath}`);
    const req = new $_client.DeleteContextFileRequest({
      authorization: `Bearer ${this.agentBay.getAPIKey()}`,
      contextId,
      filePath,
    });
    const resp = await this.agentBay.getClient().deleteContextFile(req);
    const requestId = extractRequestId(resp) || "";
    const body = resp.body;
    const success = !!(body && body.success);

    // Check for API-level errors
    const errorMessage = success
      ? ""
      : `[${body?.code || 'Unknown'}] ${body?.message || 'Failed to delete file'}`;

    // Log API response with key fields
    const keyFields: Record<string, any> = {
      context_id: contextId,
      file_path: filePath,
    };
    const fullResponse = body ? JSON.stringify(body, null, 2) : "";
    logAPIResponseWithDetails("DeleteContextFile", requestId, success, keyFields, fullResponse);

    return {
      requestId,
      success,
      data: success,
      errorMessage,
    };
  }

  /**
   * List files under a specific folder path in a context.
   */
  async listFiles(
    contextId: string,
    parentFolderPath: string,
    pageNumber = 1,
    pageSize = 50
  ): Promise<ContextFileListResult> {
    logAPICall("DescribeContextFiles");
    logDebug(
      `Request: ContextId=${contextId}, ParentFolderPath=${parentFolderPath}, PageNumber=${pageNumber}, PageSize=${pageSize}`
    );
    const req = new $_client.DescribeContextFilesRequest({
      authorization: `Bearer ${this.agentBay.getAPIKey()}`,
      pageNumber,
      pageSize,
      parentFolderPath,
      contextId,
    });
    const resp = await this.agentBay.getClient().describeContextFiles(req);
    const requestId = extractRequestId(resp) || "";
    const body = resp.body;

    // Check for API-level errors
    if (body?.success === false && body.code) {
      const errorMessage = `[${body.code}] ${body.message || 'Unknown error'}`;
      const fullResponse = body ? JSON.stringify(body, null, 2) : "";
      logAPIResponseWithDetails("DescribeContextFiles", requestId, false, undefined, fullResponse);
      return {
        requestId,
        success: false,
        entries: [],
        count: undefined,
        errorMessage,
      };
    }

    const rawList = body?.data || [];
    const entries: ContextFileEntry[] = rawList.map((it: any) => ({
      fileId: it.fileId,
      fileName: it.fileName,
      filePath: it.filePath || "",
      fileType: it.fileType,
      gmtCreate: it.gmtCreate,
      gmtModified: it.gmtModified,
      size: it.size,
      status: it.status,
    }));

    const success = !!(body && body.success);

    // Log API response with key fields
    const keyFields: Record<string, any> = {
      context_id: contextId,
      parent_folder_path: parentFolderPath,
      file_count: entries.length,
      page_number: pageNumber,
      page_size: pageSize,
    };
    if (body?.count !== undefined) {
      keyFields.count = body.count;
    }
    const fullResponse = body ? JSON.stringify(body, null, 2) : "";
    logAPIResponseWithDetails("DescribeContextFiles", requestId, success, keyFields, fullResponse);

    return {
      requestId,
      success,
      entries,
      count: body?.count,
      errorMessage: undefined,
    };
  }

  /**
   * Asynchronously initiate a task to clear the context's persistent data.
   *
   * This is a non-blocking method that returns immediately after initiating the clearing task
   * on the backend. The context's state will transition to "clearing" while the operation
   * is in progress.
   *
   * @param contextId - Unique ID of the context to clear.
   * @returns A ClearContextResult object indicating the task has been successfully started,
   *          with status field set to "clearing".
   * @throws APIError - If the backend API rejects the clearing request (e.g., invalid ID).
   */
  async clearAsync(contextId: string): Promise<ClearContextResult> {
    try {
      logAPICall("ClearContext");
      logDebug(`Request: ContextId=${contextId}`);

      const request = new $_client.ClearContextRequest({
        authorization: `Bearer ${this.agentBay.getAPIKey()}`,
        id: contextId,
      });

      const response = await this.agentBay.getClient().clearContext(request);

      // Extract request ID
      const requestId = extractRequestId(response) || "";

      // Directly access response body object
      if (!response.body) {
        const fullResponse = "Empty response body";
        logAPIResponseWithDetails("ClearContext", requestId, false, undefined, fullResponse);
        return {
          requestId,
          success: false,
          errorMessage: "Empty response body",
        };
      }

      const body = response.body;

      // Check for API-level errors
      if (!body.success && body.code) {
        const errorMessage = `[${body.code}] ${body.message || 'Unknown error'}`;
        const fullResponse = body ? JSON.stringify(body, null, 2) : "";
        logAPIResponseWithDetails("ClearContext", requestId, false, undefined, fullResponse);
        return {
          requestId,
          success: false,
          errorMessage,
        };
      }

      // ClearContext API returns success info without Data field
      // Initial status is "clearing" when the task starts
      const keyFields: Record<string, any> = {
        context_id: contextId,
        status: "clearing",
      };
      const fullResponse = body ? JSON.stringify(body, null, 2) : "";
      logAPIResponseWithDetails("ClearContext", requestId, true, keyFields, fullResponse);

      return {
        requestId,
        success: true,
        contextId,
        status: "clearing",
        errorMessage: "",
      };
    } catch (error) {
      logError("Error calling ClearContext:", error);
      throw new APIError(`Failed to start context clearing for ${contextId}: ${error}`);
    }
  }

  /**
   * Queries the status of the clearing task.
   *
   * This method calls GetContext API directly and parses the raw response to extract
   * the state field, which indicates the current clearing status.
   *
   * @param contextId - ID of the context.
   * @returns ClearContextResult object containing the current task status.
   */
  async getClearStatus(contextId: string): Promise<ClearContextResult> {
    try {
      logAPICall("GetContext");
      logDebug(`Request: ContextId=${contextId} (for clear status)`);

      const request = new $_client.GetContextRequest({
        authorization: `Bearer ${this.agentBay.getAPIKey()}`,
        contextId: contextId,
        allowCreate: "false",
      });

      const response = await this.agentBay.getClient().getContext(request);

      // Extract request ID
      const requestId = extractRequestId(response) || "";

      // Directly access response body object
      if (!response.body) {
        const fullResponse = "Empty response body";
        logAPIResponseWithDetails("GetContext (for clear status)", requestId, false, undefined, fullResponse);
        return {
          requestId,
          success: false,
          errorMessage: "Empty response body",
        };
      }

      const body = response.body;

      // Check for API-level errors
      if (!body.success && body.code) {
        const errorMessage = `[${body.code}] ${body.message || 'Unknown error'}`;
        const fullResponse = body ? JSON.stringify(body, null, 2) : "";
        logAPIResponseWithDetails("GetContext (for clear status)", requestId, false, undefined, fullResponse);
        return {
          requestId,
          success: false,
          errorMessage,
        };
      }

      // Check if data exists
      if (!body.data) {
        const fullResponse = "No data in response";
        logAPIResponseWithDetails("GetContext (for clear status)", requestId, false, undefined, fullResponse);
        return {
          requestId,
          success: false,
          errorMessage: "No data in response",
        };
      }

      const data = body.data;

      // Extract clearing status from the response data object
      // The server's state field indicates the clearing status:
      // - "clearing": Clearing is in progress
      // - "available": Clearing completed successfully
      // - "in-use": Context is being used
      // - "pre-available": Context is being prepared
      const contextIdFromResponse = data.id || "";
      const state = data.state || "clearing"; // Extract state from response object
      const errorMessage = ""; // ErrorMessage is not in GetContextResponseBodyData

      const keyFields: Record<string, any> = {
        context_id: contextIdFromResponse,
        state: state,
      };
      const fullResponse = body ? JSON.stringify(body, null, 2) : "";
      logAPIResponseWithDetails("GetContext (for clear status)", requestId, true, keyFields, fullResponse);

      return {
        requestId,
        success: true,
        contextId: contextIdFromResponse,
        status: state,
        errorMessage,
      };
    } catch (error) {
      logError("Error calling GetContext (for clear status):", error);
      return {
        requestId: "",
        success: false,
        errorMessage: `Failed to get clear status: ${error}`,
      };
    }
  }

  /**
   * Synchronously clear the context's persistent data and wait for the final result.
   *
   * This method wraps the `clearAsync` and `getClearStatus` polling logic,
   * providing the simplest and most direct way to handle clearing tasks.
   *
   * The clearing process transitions through the following states:
   * - "clearing": Data clearing is in progress
   * - "available": Clearing completed successfully (final success state)
   *
   * @param contextId - Unique ID of the context to clear.
   * @param timeout - (Optional) Timeout in seconds to wait for task completion, default is 60 seconds.
   * @param pollInterval - (Optional) Interval in seconds between status polls, default is 2 seconds.
   * @returns A ClearContextResult object containing the final task result.
   *          The status field will be "available" on success, or other states if interrupted.
   * @throws APIError - If the task fails to complete within the specified timeout.
   */
  async clear(contextId: string, timeout = 60, pollInterval = 2.0): Promise<ClearContextResult> {
    // 1. Asynchronously start the clearing task
    const startResult = await this.clearAsync(contextId);
    if (!startResult.success) {
      return startResult;
    }

    logInfo(`Started context clearing task for: ${contextId}`);

    // 2. Poll task status until completion or timeout
    const startTime = Date.now();
    const maxAttempts = Math.floor(timeout / pollInterval);
    let attempt = 0;

    while (attempt < maxAttempts) {
      // Wait before querying
      await new Promise(resolve => setTimeout(resolve, pollInterval * 1000));
      attempt++;

      // Query task status (using GetContext API with context ID)
      const statusResult = await this.getClearStatus(contextId);

      if (!statusResult.success) {
        logError(`Failed to get clear status: ${statusResult.errorMessage}`);
        return statusResult;
      }

      const status = statusResult.status;
      logInfo(`Clear task status: ${status} (attempt ${attempt}/${maxAttempts})`);

      // Check if completed
      // When clearing is complete, the state changes from "clearing" to "available"
      if (status === "available") {
        const elapsed = (Date.now() - startTime) / 1000;
        logInfo(`Context cleared successfully in ${elapsed.toFixed(2)} seconds`);
        return {
          requestId: statusResult.requestId,
          success: true,
          contextId: statusResult.contextId,
          status,
          errorMessage: "",
        };
      } else if (status && !["clearing", "pre-available"].includes(status)) {
        // If status is not "clearing" or "pre-available", and not "available",
        // treat it as a potential error or unexpected state
        const elapsed = (Date.now() - startTime) / 1000;
        logError(`Context in unexpected state after ${elapsed.toFixed(2)} seconds: ${status}`);
        // Continue polling as the state might transition to "available"
      }
    }

    // Timeout
    const elapsed = (Date.now() - startTime) / 1000;
    const errorMsg = `Context clearing timed out after ${elapsed.toFixed(2)} seconds`;
    logError(errorMsg);
    throw new APIError(errorMsg);
  }
}
