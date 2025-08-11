import { ContextSync, SyncPolicy } from "./context-sync";

/**
 * Browser context configuration for session.
 */
export interface BrowserContext {
  /** ID of the browser context to bind to the session */
  contextId: string;
  /** Whether to automatically upload browser data when the session ends */
  autoUpload: boolean;
}

/**
 * Configuration interface for CreateSessionParams
 */
export interface CreateSessionParamsConfig {
  labels: Record<string, string>;
  imageId?: string;
  contextSync: ContextSync[];
  /** Optional configuration for browser data synchronization */
  browserContext?: BrowserContext;
  /** Whether to create a VPC-based session. Defaults to false. */
  isVpc?: boolean;
  /** MCP policy id to apply when creating the session. */
  mcpPolicyId?: string;
}

/**
 * CreateSessionParams provides a way to configure the parameters for creating a new session
 * in the AgentBay cloud environment.
 */
export class CreateSessionParams implements CreateSessionParamsConfig {
  /** Custom labels for the Session. These can be used for organizing and filtering sessions. */
  public labels: Record<string, string>;

  /** Image ID to use for the session. */
  public imageId?: string;

  /**
   * List of context synchronization configurations.
   * These configurations define how contexts should be synchronized and mounted.
   */
  public contextSync: ContextSync[];

  /** Optional configuration for browser data synchronization. */
  public browserContext?: BrowserContext;

  /** Whether to create a VPC-based session. Defaults to false. */
  public isVpc: boolean;

  /** MCP policy id to apply when creating the session. */
  public mcpPolicyId?: string;

  constructor() {
    this.labels = {};
    this.contextSync = [];
    this.isVpc = false;
  }

  /**
   * WithLabels sets the labels for the session parameters and returns the updated parameters.
   */
  withLabels(labels: Record<string, string>): CreateSessionParams {
    this.labels = labels;
    return this;
  }


  /**
   * WithImageId sets the image ID for the session parameters and returns the updated parameters.
   */
  withImageId(imageId: string): CreateSessionParams {
    this.imageId = imageId;
    return this;
  }

  /**
   * WithBrowserContext sets the browser context for the session parameters and returns the updated parameters.
   */
  withBrowserContext(browserContext: BrowserContext): CreateSessionParams {
    this.browserContext = browserContext;
    return this;
  }

  /**
   * WithIsVpc sets the VPC flag for the session parameters and returns the updated parameters.
   */
  withIsVpc(isVpc: boolean): CreateSessionParams {
    this.isVpc = isVpc;
    return this;
  }

  /**
   * WithMcpPolicyId sets the MCP policy id for the session parameters and returns the updated parameters.
   */
  withMcpPolicyId(mcpPolicyId: string): CreateSessionParams {
    this.mcpPolicyId = mcpPolicyId;
    return this;
  }

  /**
   * GetLabelsJSON returns the labels as a JSON string.
   * Returns an object with success status and result/error message to match Go version behavior.
   */
  getLabelsJSON(): { result: string; error?: string } {
    if (Object.keys(this.labels).length === 0) {
      return { result: "" };
    }

    try {
      const labelsJSON = JSON.stringify(this.labels);
      return { result: labelsJSON };
    } catch (error) {
      return {
        result: "",
        error: `Failed to marshal labels to JSON: ${error}`,
      };
    }
  }

  /**
   * AddContextSync adds a context sync configuration to the session parameters.
   */
  addContextSync(
    contextId: string,
    path: string,
    policy?: SyncPolicy
  ): CreateSessionParams {
    const contextSync = new ContextSync(contextId, path, policy);
    this.contextSync.push(contextSync);
    return this;
  }

  /**
   * AddContextSyncConfig adds a pre-configured context sync to the session parameters.
   */
  addContextSyncConfig(contextSync: ContextSync): CreateSessionParams {
    this.contextSync.push(contextSync);
    return this;
  }

  /**
   * WithContextSync sets the context sync configurations for the session parameters.
   */
  withContextSync(contextSyncs: ContextSync[]): CreateSessionParams {
    this.contextSync = contextSyncs;
    return this;
  }

  /**
   * Convert to plain object for JSON serialization
   */
  toJSON(): CreateSessionParamsConfig {
    return {
      labels: this.labels,
      imageId: this.imageId,
      contextSync: this.contextSync,
      browserContext: this.browserContext,
      isVpc: this.isVpc,
      mcpPolicyId: this.mcpPolicyId,
    };
  }

  /**
   * Create from plain object
   */
  static fromJSON(config: CreateSessionParamsConfig): CreateSessionParams {
    const params = new CreateSessionParams();
    params.labels = config.labels || {};
    params.imageId = config.imageId;
    params.contextSync = config.contextSync || [];
    params.browserContext = config.browserContext;
    params.isVpc = config.isVpc || false;
    params.mcpPolicyId = config.mcpPolicyId;
    return params;
  }
}

/**
 * NewCreateSessionParams creates a new CreateSessionParams with default values.
 */
export function newCreateSessionParams(): CreateSessionParams {
  return new CreateSessionParams();
}
