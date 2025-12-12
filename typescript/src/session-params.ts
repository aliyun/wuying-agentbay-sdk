import { ContextSync, SyncPolicy, newUploadPolicy, newExtractPolicy, newRecyclePolicy, WhiteList, BWList, newDeletePolicy } from "./context-sync";
import { ExtensionOption } from "./extension";
import { BrowserFingerprintContext } from "./browser";
import { ExtraConfigs, extraConfigsToJSON } from "./types/extra-configs";

// Browser fingerprint persistent path constant (moved from config.ts)
const BROWSER_FINGERPRINT_PERSIST_PATH = "/tmp/browser_fingerprint";
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
} from "./utils/logger";

/**
 * Browser context configuration for session with optional extension support.
 *
 * This class provides browser context configuration for cloud sessions and supports
 * automatic extension synchronization when ExtensionOption is provided.
 *
 * Key Features:
 * - Browser context binding for sessions
 * - Automatic browser data upload on session end
 * - Optional browser fingerprint integration with automatic context sync generation
 * - Optional extension integration with automatic context sync generation
 * - Clean API with ExtensionOption encapsulation
 *
 * Extension Configuration:
 * - **ExtensionOption**: Pass an ExtensionOption object with contextId and extensionIds
 * - **No Extensions**: Don't provide extensionOption parameter (extensionContextSyncs will be undefined)
 *
 * Usage Examples:
 * ```typescript
 * // With extensions using ExtensionOption
 * import { ExtensionOption } from "./extension";
 * import { BrowserFingerprintContext } from "./browser";
 *
 * const extOption = new ExtensionOption(
 *   "my_extensions",
 *   ["ext1", "ext2"]
 * );
 *
 * const fingerprintContext = new BrowserFingerprintContext(
 *   "my_fingerprint_context"
 * );
 *
 * const browserContext = new BrowserContext(
 *   "browser_session",
 *   true,
 *   extOption,
 *   fingerprintContext
 * );
 *
 * // Without extensions (minimal configuration)
 * const browserContext = new BrowserContext(
 *   "browser_session",
 *   true
 * );
 * // extensionContextSyncs and fingerprintContextSync will be undefined
 *
 * // With fingerprint only
 * const browserContextWithFingerprint = new BrowserContext(
 *   "browser_session",
 *   true,
 *   undefined,
 *   fingerprintContext
 * );
 * ```
 */
export class BrowserContext {
  /** ID of the browser context to bind to the session */
  contextId: string;
  /** Whether to automatically upload browser data when the session ends */
  autoUpload: boolean;
  /** Optional browser fingerprint context configuration object containing fingerprintContextId */
  fingerprintContext?: BrowserFingerprintContext;
  /** ID of the fingerprint context for browser fingerprint. Set automatically from fingerprint_context. */
  fingerprintContextId?: string;
  /** Auto-generated context sync for fingerprint. None if no fingerprint configuration provided. */
  fingerprintContextSync?: ContextSync;
  /** Optional extension configuration object containing context_id and extension_ids */
  extensionOption?: ExtensionOption;
  /** ID of the extension context for browser extensions. Set automatically from extension_option. */
  extensionContextId?: string;
  /** List of extension IDs to synchronize. Set automatically from extension_option. */
  extensionIds?: string[];
  /** Auto-generated context syncs for extensions. None if no extension configuration provided. */
  extensionContextSyncs?: ContextSync[];

  /**
   * Initialize BrowserContextImpl with optional extension and fingerprint support.
   *
   * @param contextId - ID of the browser context to bind to the session.
   *                   This identifies the browser instance for the session.
   * @param autoUpload - Whether to automatically upload browser data
   *                    when the session ends. Defaults to true.
   * @param extensionOption - Extension configuration object containing
   *                         contextId and extensionIds. This encapsulates
   *                         all extension-related configuration.
   *                         Defaults to undefined.
   * @param fingerprintContext - Browser fingerprint context configuration object containing
   *                            fingerprintContextId. This encapsulates
   *                            all fingerprint-related configuration.
   *                            Defaults to undefined.
   *
   * Extension Configuration:
   * - **ExtensionOption**: Use extensionOption parameter with an ExtensionOption object
   * - **No Extensions**: Don't provide extensionOption parameter
   *
   * Fingerprint Configuration:
   * - **BrowserFingerprintContext**: Use fingerprintContext parameter with a BrowserFingerprintContext object
   * - **No Fingerprint**: Don't provide fingerprintContext parameter
   *
   * Auto-generation:
   * - extensionContextSyncs is automatically generated when extensionOption is provided
   * - extensionContextSyncs will be undefined if no extensionOption is provided
   * - extensionContextSyncs will be a ContextSync[] if extensionOption is valid
   * - fingerprintContextSync is automatically generated when fingerprintContext is provided
   * - fingerprintContextSync will be undefined if no fingerprintContext is provided
   * - fingerprintContextSync will be a ContextSync if fingerprintContext is valid
   */
  constructor(
    contextId: string,
    autoUpload = true,
    extensionOption?: ExtensionOption,
    fingerprintContext?: BrowserFingerprintContext
  ) {
    this.contextId = contextId;
    this.autoUpload = autoUpload;
    this.extensionOption = extensionOption;
    this.fingerprintContext = fingerprintContext;

    // Handle fingerprint configuration from BrowserFingerprintContext
    if (fingerprintContext) {
      // Extract fingerprint information from BrowserFingerprintContext
      this.fingerprintContextId = fingerprintContext.fingerprintContextId;
      // Auto-generate fingerprint context sync
      this.fingerprintContextSync = this._createFingerprintContextSync();
    } else {
      // No fingerprint configuration provided
      this.fingerprintContextId = undefined;
      this.fingerprintContextSync = undefined;
    }

    // Handle extension configuration from ExtensionOption
    if (extensionOption) {
      // Extract extension information from ExtensionOption
      this.extensionContextId = extensionOption.contextId;
      this.extensionIds = extensionOption.extensionIds;
      // Auto-generate extension context syncs
      this.extensionContextSyncs = this._createExtensionContextSyncs();
    } else {
      // No extension configuration provided
      this.extensionContextId = undefined;
      this.extensionIds = [];
      this.extensionContextSyncs = undefined;
    }
  }

  /**
   * Create ContextSync configurations for browser extensions.
   *
   * This method is called only when extensionOption is provided and contains
   * valid extension configuration (contextId and extensionIds).
   *
   * @returns ContextSync[] - List of context sync configurations for extensions.
   *                         Returns empty list if extension configuration is invalid.
   */
  private _createExtensionContextSyncs(): ContextSync[] {
    if (!this.extensionIds || this.extensionIds.length === 0 || !this.extensionContextId) {
      return [];
    }

    // Create whitelist for each extension ID
    const whiteLists: WhiteList[] = this.extensionIds.map(extId => ({
      path: extId,
      excludePaths: []
    }));

    // Create sync policy for extensions
    const syncPolicy: SyncPolicy = {
      uploadPolicy: {
        ...newUploadPolicy(),
        autoUpload: false
      },
      extractPolicy: {
        ...newExtractPolicy(),
        extract: true,
        deleteSrcFile: true
      },
      deletePolicy: {
        ...newDeletePolicy(),
        syncLocalFile: false
      },
      recyclePolicy: newRecyclePolicy(),
      bwList: {
        whiteLists: whiteLists
      }
    };

    // Create context sync for extensions
    const extensionSync = new ContextSync(
      this.extensionContextId,
      "/tmp/extensions/",
      syncPolicy
    );

    return [extensionSync];
  }

  /**
   * Create ContextSync configuration for browser fingerprint.
   *
   * This method is called only when fingerprintContext is provided and contains
   * valid fingerprint configuration (fingerprintContextId).
   *
   * @returns ContextSync - Context sync configuration for fingerprint.
   *                       Returns undefined if fingerprint configuration is invalid.
   */
  private _createFingerprintContextSync(): ContextSync | undefined {
    if (!this.fingerprintContextId || !this.fingerprintContextId.trim()) {
      return undefined;
    }

    // Create sync policy for fingerprint
    const syncPolicy: SyncPolicy = {
      uploadPolicy: {
        ...newUploadPolicy(),
        autoUpload: false
      },
      extractPolicy: {
        ...newExtractPolicy(),
        extract: true,
        deleteSrcFile: true
      },
      deletePolicy: {
        ...newDeletePolicy(),
        syncLocalFile: false
      },
      recyclePolicy: newRecyclePolicy(),
      bwList: {
        whiteLists: []
      }
    };

    // Create context sync for fingerprint
    const fingerprintSync = new ContextSync(
      this.fingerprintContextId,
      BROWSER_FINGERPRINT_PERSIST_PATH,
      syncPolicy
    );

    return fingerprintSync;
  }

  /**
   * Get context syncs for extensions.
   *
   * @returns ContextSync[] - Context sync configurations for extensions. Returns empty list if no extensions configured.
   */
  getExtensionContextSyncs(): ContextSync[] {
    return this.extensionContextSyncs || [];
  }

  /**
   * Get context sync for fingerprint.
   *
   * @returns ContextSync - Context sync configuration for fingerprint.
   *                       Returns undefined if fingerprint configuration is invalid.
   */
  getFingerprintContextSync(): ContextSync | undefined {
    return this.fingerprintContextSync;
  }
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
  /** Policy id to apply when creating the session. */
  policyId?: string;
  /** Whether to enable browser recording for the session. Defaults to false. */
  enableBrowserReplay?: boolean;
  /** Extra configuration settings for different session types (e.g., mobile) */
  extraConfigs?: ExtraConfigs;
  /** Framework name for SDK statistics tracking */
  framework?: string;
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

  /** Policy id to apply when creating the session. */
  public policyId?: string;

  /** Whether to enable browser recording for the session. Defaults to false. */
  public enableBrowserReplay: boolean;

  /** Extra configuration settings for different session types (e.g., mobile) */
  public extraConfigs?: ExtraConfigs;

  /** Framework name for SDK statistics tracking */
  public framework?: string;

  constructor() {
    this.labels = {};
    this.contextSync = [];
    this.isVpc = false;
    this.enableBrowserReplay = false;
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
    // Add extension and fingerprint context syncs if browser context has them
    if (this.browserContext && 'getExtensionContextSyncs' in this.browserContext) {
      const contextSyncs = this.browserContext.getExtensionContextSyncs();
      this.contextSync.push(...contextSyncs);
      logDebug(`Added ${contextSyncs.length} extension context syncs from browser context`);
    }
    // Add fingerprint context sync if browser context has it
    if (this.browserContext && 'getFingerprintContextSync' in this.browserContext) {
      const fingerprintContextSync = this.browserContext.getFingerprintContextSync();
      if (fingerprintContextSync) {
        this.contextSync.push(fingerprintContextSync);
        logDebug(`Added fingerprint context sync from browser context`);
      }
    }
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
   * WithPolicyId sets the policy id for the session parameters and returns the updated parameters.
   */
  withPolicyId(policyId: string): CreateSessionParams {
    this.policyId = policyId;
    return this;
  }

  /**
   * WithenableBrowserReplay sets the browser recording flag for the session parameters and returns the updated parameters.
   */
  withEnableBrowserReplay(enableBrowserReplay: boolean): CreateSessionParams {
    this.enableBrowserReplay = enableBrowserReplay;
    return this;
  }

  /**
   * Alias for withEnableBrowserReplay for backward compatibility.
   */
  withEnableRecord(enableRecord: boolean): CreateSessionParams {
    return this.withEnableBrowserReplay(enableRecord);
  }

  /**
   * WithExtraConfigs sets the extra configurations for the session parameters and returns the updated parameters.
   */
  withExtraConfigs(extraConfigs: ExtraConfigs): CreateSessionParams {
    this.extraConfigs = extraConfigs;
    return this;
  }

  /**
   * WithFramework sets the framework name for the session parameters and returns the updated parameters.
   */
  withFramework(framework: string): CreateSessionParams {
    this.framework = framework;
    return this;
  }

  /**
   * GetLabelsJSON returns the labels as a JSON string.
   * Returns an object with success status and result/error message to match Go version behavior.
   */
  private getLabelsJSON(): { result: string; error?: string } {
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
   * GetExtraConfigsJSON returns the extra configs as a JSON string.
   * Returns an object with result and optional error message to match Go version behavior.
   */
  private getExtraConfigsJSON(): { result: string; error?: string } {
    if (!this.extraConfigs) {
      return { result: "" };
    }

    try {
      const extraConfigsJSON = extraConfigsToJSON(this.extraConfigs);
      return { result: extraConfigsJSON };
    } catch (error) {
      return {
        result: "",
        error: `Failed to marshal extra configs to JSON: ${error}`,
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
    // Add extension and fingerprint context syncs if browser context has them
    if (this.browserContext && 'getExtensionContextSyncs' in this.browserContext) {
      const contextSyncs = this.browserContext.getExtensionContextSyncs();
      this.contextSync.push(...contextSyncs);
      logDebug(`Added ${contextSyncs.length} extension context syncs from browser context`);
    }
    // Add fingerprint context sync if browser context has it
    if (this.browserContext && 'getFingerprintContextSync' in this.browserContext) {
      const fingerprintContextSync = this.browserContext.getFingerprintContextSync();
      if (fingerprintContextSync) {
        this.contextSync.push(fingerprintContextSync);
        logDebug(`Added fingerprint context sync from browser context`);
      }
    }
    return this;
  }

  /**
   * Convert to plain object for JSON serialization
   */
  toJSON(): CreateSessionParamsConfig {
    // Get base context syncs
    let allContextSyncs = [...this.contextSync];

    // Add extension context syncs if browser context has them
    if (this.browserContext && 'getExtensionContextSyncs' in this.browserContext) {
      const extensionSyncs = this.browserContext.getExtensionContextSyncs();
      allContextSyncs = allContextSyncs.concat(extensionSyncs);
      logDebug(`Added ${extensionSyncs.length} extension context syncs from browser context`);
    }
    // Add fingerprint context sync if browser context has it
    if (this.browserContext && 'getFingerprintContextSync' in this.browserContext) {
      const fingerprintContextSync = this.browserContext.getFingerprintContextSync();
      if (fingerprintContextSync) {
        allContextSyncs.push(fingerprintContextSync);
        logDebug(`Added fingerprint context sync from browser context`);
      }
    }

    return {
      labels: this.labels,
      imageId: this.imageId,
      contextSync: allContextSyncs,
      browserContext: this.browserContext,
      isVpc: this.isVpc,
      policyId: this.policyId,
      enableBrowserReplay: this.enableBrowserReplay,
      extraConfigs: this.extraConfigs,
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

    // Handle browser context - convert to BrowserContext class if needed
    if (config.browserContext) {
      if ('getAllContextSyncs' in config.browserContext) {
        // It's already a BrowserContext instance
        params.browserContext = config.browserContext;
      } else {
        // It's a plain object, convert to BrowserContext class
        const bc = config.browserContext as any; // Type assertion for plain object
        params.browserContext = new BrowserContext(
          bc.contextId,
          bc.autoUpload,
          bc.extensionOption,
          bc.fingerprintContext
        );
      }
    }

    params.isVpc = config.isVpc || false;
    params.policyId = config.policyId;
    params.enableBrowserReplay = config.enableBrowserReplay || false;
    params.extraConfigs = config.extraConfigs;
    return params;
  }
}

/**
 * NewCreateSessionParams creates a new CreateSessionParams with default values.
 */
export function newCreateSessionParams(): CreateSessionParams {
  return new CreateSessionParams();
}