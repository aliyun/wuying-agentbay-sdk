import { AgentBay } from './agent-bay';
import { APIError } from './exceptions';
import * as $_client from './api';

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
   * @returns A list of Context objects.
   */
  async list(): Promise<Context[]> {
    try {
      const request = new $_client.ListContextsRequest({
        authorization: `Bearer ${this.agentBay.getAPIKey()}`
      });
      const response = await this.agentBay.getClient().listContexts(request);
      
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
      
      return contexts;
    } catch (error) {
      throw new APIError(`Failed to list contexts: ${error}`);
    }
  }

  /**
   * Gets a context by name. Optionally creates it if it doesn't exist.
   * 
   * @param name - The name of the context to get.
   * @param create - Whether to create the context if it doesn't exist.
   * @returns The Context object if found or created, null if not found and create is false.
   */
  async get(name: string, create: boolean = false): Promise<Context | null> {
    try {
      const request = new $_client.GetContextRequest({
        name: name,
        allowCreate: create ? 'true' : 'false',
        authorization: `Bearer ${this.agentBay.getAPIKey()}`
      });
      
      const response = await this.agentBay.getClient().getContext(request);
      
      const contextId = response.body?.data?.id;
      if (!contextId) {
        return null;
      }
      
      // Get the full context details
      const contexts = await this.list();
      for (const context of contexts) {
        if (context.id === contextId) {
          return context;
        }
      }
      
      // If we couldn't find the context in the list, create a basic one
      return new Context(contextId, name);
    } catch (error) {
      throw new APIError(`Failed to get context ${name}: ${error}`);
    }
  }

  /**
   * Creates a new context with the given name.
   * 
   * @param name - The name for the new context.
   * @returns The created Context object.
   */
  async create(name: string): Promise<Context> {
    const context = await this.get(name, true);
    if (!context) {
      throw new APIError(`Failed to create context ${name}`);
    }
    return context;
  }

  /**
   * Updates the specified context.
   * 
   * @param context - The Context object to update.
   * @returns The updated Context object.
   */
  async update(context: Context): Promise<Context> {
    try {
      const request = new $_client.ModifyContextRequest({
        id: context.id,
        name: context.name,
        authorization: `Bearer ${this.agentBay.getAPIKey()}`
      });
      
      await this.agentBay.getClient().modifyContext(request);
      
      // Return the updated context
      return context;
    } catch (error) {
      throw new APIError(`Failed to update context ${context.id}: ${error}`);
    }
  }

  /**
   * Deletes the specified context.
   * 
   * @param context - The Context object to delete.
   */
  async delete(context: Context): Promise<void> {
    try {
      const request = new $_client.DeleteContextRequest({
        id: context.id,
        authorization: `Bearer ${this.agentBay.getAPIKey()}`
      });
      
      await this.agentBay.getClient().deleteContext(request);
    } catch (error) {
      throw new APIError(`Failed to delete context ${context.id}: ${error}`);
    }
  }
}
