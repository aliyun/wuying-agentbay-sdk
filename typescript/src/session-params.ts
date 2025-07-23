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
  /**
   * @deprecated This field is deprecated and will be removed in a future version.
   * Please use contextSync instead for more flexible and powerful data persistence.
   */
  contextId?: string;
  imageId?: string;
  contextSync: ContextSync[];
  /** Optional configuration for browser data synchronization */
  browserContext?: BrowserContext;
}

/**
 * CreateSessionParams provides a way to configure the parameters for creating a new session
 * in the AgentBay cloud environment.
 */
export class CreateSessionParams implements CreateSessionParamsConfig {
  /** Custom labels for the Session. These can be used for organizing and filtering sessions. */
  public labels: Record<string, string>;

  /**
   * ID of the context to bind to the session.
   * The context can include various types of persistence like file system (volume) and cookies.
   *
   * @deprecated This field is deprecated and will be removed in a future version.
   * Please use contextSync instead for more flexible and powerful data persistence.
   *
   * Important Limitations:
   * 1. One session at a time: A context can only be used by one session at a time.
   *    If you try to create a session with a context ID that is already in use by another active session,
   *    the session creation will fail.
   *
   * 2. OS binding: A context is bound to the operating system of the first session that uses it.
   *    When a context is first used with a session, it becomes bound to that session's OS.
   *    Any attempt to use the context with a session running on a different OS will fail.
   *    For example, if a context is first used with a Linux session, it cannot later be used
   *    with a Windows or Android session.
   */
  public contextId?: string;

  /** Image ID to use for the session. */
  public imageId?: string;

  /**
   * List of context synchronization configurations.
   * These configurations define how contexts should be synchronized and mounted.
   */
  public contextSync: ContextSync[];

  /** Optional configuration for browser data synchronization. */
  public browserContext?: BrowserContext;

  constructor() {
    this.labels = {};
    this.contextSync = [];
  }

  /**
   * WithLabels sets the labels for the session parameters and returns the updated parameters.
   */
  withLabels(labels: Record<string, string>): CreateSessionParams {
    this.labels = labels;
    return this;
  }

  /**
   * WithContextID sets the context ID for the session parameters and returns the updated parameters.
   */
  withContextID(contextId: string): CreateSessionParams {
    this.contextId = contextId;
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
      contextId: this.contextId,
      imageId: this.imageId,
      contextSync: this.contextSync,
      browserContext: this.browserContext,
    };
  }

  /**
   * Create from plain object
   */
  static fromJSON(config: CreateSessionParamsConfig): CreateSessionParams {
    const params = new CreateSessionParams();
    params.labels = config.labels || {};
    params.contextId = config.contextId;
    params.imageId = config.imageId;
    params.contextSync = config.contextSync || [];
    params.browserContext = config.browserContext;
    return params;
  }
}

/**
 * NewCreateSessionParams creates a new CreateSessionParams with default values.
 */
export function newCreateSessionParams(): CreateSessionParams {
  return new CreateSessionParams();
}
