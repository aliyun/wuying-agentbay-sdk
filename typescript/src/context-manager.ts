import { ApiResponse, extractRequestId } from "./types/api-response";
import { Client } from "./api/client";
import { GetContextInfoRequest, SyncContextRequest } from "./api/models/model";
import { log, logError } from "./utils/logger";

export interface ContextInfoResult extends ApiResponse {
  contextStatus: string;
}

export interface ContextSyncResult extends ApiResponse {
  success: boolean;
}

export interface SessionInterface {
  getAPIKey(): string;
  getClient(): Client;
  getSessionId(): string;
}

export class ContextManager {
  private session: SessionInterface;

  constructor(session: SessionInterface) {
    this.session = session;
  }

  async info(): Promise<ContextInfoResult> {
    return this.infoWithParams();
  }

  async infoWithParams(
    contextId?: string,
    path?: string,
    taskType?: string
  ): Promise<ContextInfoResult> {
    const request = new GetContextInfoRequest({
      authorization: `Bearer ${this.session.getAPIKey()}`,
      sessionId: this.session.getSessionId(),
    });

    // Set optional parameters if provided
    if (contextId) {
      request.contextId = contextId;
    }
    if (path) {
      request.path = path;
    }
    if (taskType) {
      request.taskType = taskType;
    }

    // Log API request (matching Go version format)
    log("API Call: GetContextInfo");
    let requestLog = `Request: SessionId=${request.sessionId}`;
    if (request.contextId) {
      requestLog += `, ContextId=${request.contextId}`;
    }
    if (request.path) {
      requestLog += `, Path=${request.path}`;
    }
    if (request.taskType) {
      requestLog += `, TaskType=${request.taskType}`;
    }
    log(requestLog);

    try {
      const response = await this.session.getClient().getContextInfo(request);

      // Extract RequestID
      const requestId = extractRequestId(response) || "";

      if (response?.body) {
        log("Response from GetContextInfo:", response.body);
      }

      let contextStatus = "";
      if (response?.body?.data?.contextStatus) {
        contextStatus = response.body.data.contextStatus;
      }

      return {
        requestId,
        contextStatus,
      };
    } catch (error) {
      logError("Error calling GetContextInfo:", error);
      throw new Error(`Failed to get context info: ${error}`);
    }
  }

  async sync(): Promise<ContextSyncResult> {
    return this.syncWithParams();
  }

  async syncWithParams(
    contextId?: string,
    path?: string,
    mode?: string
  ): Promise<ContextSyncResult> {
    const request = new SyncContextRequest({
      authorization: `Bearer ${this.session.getAPIKey()}`,
      sessionId: this.session.getSessionId(),
    });

    // Set optional parameters if provided
    if (contextId) {
      request.contextId = contextId;
    }
    if (path) {
      request.path = path;
    }
    if (mode) {
      request.mode = mode;
    }

    // Log API request (matching Go version format)
    log("API Call: SyncContext");
    let requestLog = `Request: SessionId=${request.sessionId}`;
    if (request.contextId) {
      requestLog += `, ContextId=${request.contextId}`;
    }
    if (request.path) {
      requestLog += `, Path=${request.path}`;
    }
    if (request.mode) {
      requestLog += `, Mode=${request.mode}`;
    }
    log(requestLog);

    try {
      const response = await this.session.getClient().syncContext(request);

      // Extract RequestID
      const requestId = extractRequestId(response) || "";

      if (response?.body) {
        log("Response from SyncContext:", response.body);
      }

      let success = false;
      if (response?.body?.success !== undefined) {
        success = response.body.success;
      }

      return {
        requestId,
        success,
      };
    } catch (error) {
      logError("Error calling SyncContext:", error);
      throw new Error(`Failed to sync context: ${error}`);
    }
  }
}

export function newContextManager(session: SessionInterface): ContextManager {
  return new ContextManager(session);
}
