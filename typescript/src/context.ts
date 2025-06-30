import { AgentBay } from './agent-bay';
import { APIError } from './exceptions';
import * as $_client from './api';
import { log, logError } from './utils/logger';
import { ApiResponse, ApiResponseWithData, extractRequestId } from './types/api-response';

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
   * The current state of the context (e.g., "available", "in-use").
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
   * The operating system type this context is bound to.
   */
  osType?: string;

  /**
   * Initialize a Context object.
   *
   * @param id - The unique identifier of the context.
   * @param name - The name of the context.
   * @param state - The current state of the context.
   * @param createdAt - Date and time when the Context was created.
   * @param lastUsedAt - Date and time when the Context was last used.
   * @param osType - The operating system type this context is bound to.
   */
  constructor(
    id: string,
    name: string,
    state: string = 'available',
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
   * Lists all available contexts.
   *
   * @returns API response with contexts list and requestId
   */
  async list(): Promise<ApiResponseWithData<Context[]>> {
    try {
      const request = new $_client.ListContextsRequest({
        authorization: `Bearer ${this.agentBay.getAPIKey()}`
      });

      // Log API request
      log("API Call: ListContexts");
      log("Request: No parameters");

      const response = await this.agentBay.getClient().listContexts(request);

      // Log API response
      log(`Response from ListContexts:`, response.body);

      const contexts: Context[] = [];
      if (response.body?.data) {
        for (const contextData of response.body.data) {
          contexts.push(new Context(
            contextData.id || '',
            contextData.name || '',
            contextData.state || 'available',
            contextData.createTime,
            contextData.lastUsedTime,
            contextData.osType
          ));
        }
      }

      return {
        requestId: extractRequestId(response),
        data: contexts
      };
    } catch (error) {
      logError("Error calling ListContexts:", error);
      throw new APIError(`Failed to list contexts: ${error}`);
    }
  }

  /**
   * Gets a context by name. Optionally creates it if it doesn't exist.
   *
   * @param name - The name of the context to get.
   * @param create - Whether to create the context if it doesn't exist.
   * @returns API response with context data and requestId
   */
  async get(name: string, create: boolean = false): Promise<ApiResponseWithData<Context | null>> {
    try {
      const request = new $_client.GetContextRequest({
        name: name,
        allowCreate: create ? 'true' : 'false',
        authorization: `Bearer ${this.agentBay.getAPIKey()}`
      });

      // Log API request
      log("API Call: GetContext");
      log(`Request: Name=${name}, AllowCreate=${create}`);

      const response = await this.agentBay.getClient().getContext(request);

      // Log API response
      log(`Response from GetContext:`, response.body);

      const contextId = response.body?.data?.id;
      if (!contextId) {
        return {
          requestId: extractRequestId(response),
          data: null
        };
      }

      // Get the full context details
      const contextsResponse = await this.list();
      for (const context of contextsResponse.data) {
        if (context.id === contextId) {
          return {
            requestId: extractRequestId(response),
            data: context
          };
        }
      }

      // If we couldn't find the context in the list, create a basic one
      const context = new Context(contextId, name);
      return {
        requestId: extractRequestId(response),
        data: context
      };
    } catch (error) {
      logError("Error calling GetContext:", error);
      throw new APIError(`Failed to get context ${name}: ${error}`);
    }
  }

  /**
   * Creates a new context with the given name.
   *
   * @param name - The name for the new context.
   * @returns API response with created context data and requestId
   */
  async create(name: string): Promise<ApiResponseWithData<Context>> {
    const contextResponse = await this.get(name, true);
    if (!contextResponse.data) {
      throw new APIError(`Failed to create context ${name}`);
    }
    return {
      requestId: contextResponse.requestId,
      data: contextResponse.data
    };
  }

  /**
   * Updates the specified context.
   *
   * @param context - The Context object to update.
   * @returns API response with updated context data and requestId
   */
  async update(context: Context): Promise<ApiResponseWithData<Context>> {
    try {
      const request = new $_client.ModifyContextRequest({
        id: context.id,
        name: context.name,
        authorization: `Bearer ${this.agentBay.getAPIKey()}`
      });

      // Log API request
      log("API Call: ModifyContext");
      log(`Request: Id=${context.id}, Name=${context.name}`);

      const response = await this.agentBay.getClient().modifyContext(request);

      // Log API response
      log(`Response from ModifyContext:`, response.body);

      // Return the updated context
      return {
        requestId: extractRequestId(response),
        data: context
      };
    } catch (error) {
      logError("Error calling ModifyContext:", error);
      throw new APIError(`Failed to update context ${context.id}: ${error}`);
    }
  }

  /**
   * Deletes the specified context.
   *
   * @param context - The Context object to delete.
   * @returns API response with requestId
   */
  async delete(context: Context): Promise<ApiResponse> {
    try {
      const request = new $_client.DeleteContextRequest({
        id: context.id,
        authorization: `Bearer ${this.agentBay.getAPIKey()}`
      });

      // Log API request
      log("API Call: DeleteContext");
      log(`Request: Id=${context.id}`);

      const response = await this.agentBay.getClient().deleteContext(request);

      // Log API response
      log(`Response from DeleteContext:`, response.body);

      return {
        requestId: extractRequestId(response)
      };
    } catch (error) {
      logError("Error calling DeleteContext:", error);
      throw new APIError(`Failed to delete context ${context.id}: ${error}`);
    }
  }
}
