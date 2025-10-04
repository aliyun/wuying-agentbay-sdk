// UploadStrategy defines the upload strategy for context synchronization
export enum UploadStrategy {
  UploadBeforeResourceRelease = "UploadBeforeResourceRelease",
}

// DownloadStrategy defines the download strategy for context synchronization
export enum DownloadStrategy {
  DownloadAsync = "DownloadAsync",
}

// UploadPolicy defines the upload policy for context synchronization
export interface UploadPolicy {
  autoUpload: boolean;
  uploadStrategy: UploadStrategy;
}

// DownloadPolicy defines the download policy for context synchronization
export interface DownloadPolicy {
  autoDownload: boolean;
  downloadStrategy: DownloadStrategy;
}

// DeletePolicy defines the delete policy for context synchronization
export interface DeletePolicy {
  syncLocalFile: boolean;
}

// ExtractPolicy defines the extract policy for context synchronization
export interface ExtractPolicy {
  extract: boolean;
  deleteSrcFile: boolean;
  extractToCurrentFolder: boolean;
}

// ExtractPolicyClass provides a class-based implementation with default values
export class ExtractPolicyClass implements ExtractPolicy {
  extract: boolean = true;
  deleteSrcFile: boolean = true;
  extractToCurrentFolder: boolean = false;

  constructor(extract: boolean = true, deleteSrcFile: boolean = true, extractToCurrentFolder: boolean = false) {
    this.extract = extract;
    this.deleteSrcFile = deleteSrcFile;
    this.extractToCurrentFolder = extractToCurrentFolder;
  }

  /**
   * Creates a new extract policy with default values
   */
  static default(): ExtractPolicyClass {
    return new ExtractPolicyClass();
  }

  /**
   * Converts to plain object for JSON serialization
   */
  toDict(): Record<string, any> {
    return {
      extract: this.extract,
      deleteSrcFile: this.deleteSrcFile,
      extractToCurrentFolder: this.extractToCurrentFolder
    };
  }
}

// WhiteList defines the white list configuration
export interface WhiteList {
  path: string;
  excludePaths?: string[];
}

export class WhiteListValidator {
  private static containsWildcard(path: string): boolean {
    return /[*?\[\]]/.test(path);
  }

  static validate(whitelist: WhiteList): void {
    if (this.containsWildcard(whitelist.path)) {
      throw new Error(
        `Wildcard patterns are not supported in path. Got: ${whitelist.path}. ` +
        "Please use exact directory paths instead."
      );
    }

    if (whitelist.excludePaths) {
      for (const excludePath of whitelist.excludePaths) {
        if (this.containsWildcard(excludePath)) {
          throw new Error(
            `Wildcard patterns are not supported in exclude_paths. Got: ${excludePath}. ` +
            "Please use exact directory paths instead."
          );
        }
      }
    }
  }
}

// BWList defines the black and white list configuration
export interface BWList {
  whiteLists?: WhiteList[];
}

// SyncPolicy defines the synchronization policy
export interface SyncPolicy {
  uploadPolicy?: UploadPolicy;
  downloadPolicy?: DownloadPolicy;
  deletePolicy?: DeletePolicy;
  extractPolicy?: ExtractPolicy;
  bwList?: BWList;
}

// SyncPolicyImpl provides a class-based implementation with default value handling
export class SyncPolicyImpl implements SyncPolicy {
  uploadPolicy?: UploadPolicy;
  downloadPolicy?: DownloadPolicy;
  deletePolicy?: DeletePolicy;
  extractPolicy?: ExtractPolicy;
  bwList?: BWList;

  constructor(policy?: Partial<SyncPolicy>) {
    if (policy) {
      this.uploadPolicy = policy.uploadPolicy;
      this.downloadPolicy = policy.downloadPolicy;
      this.deletePolicy = policy.deletePolicy;
      this.extractPolicy = policy.extractPolicy;
      this.bwList = policy.bwList;
    }
    this.ensureDefaults();
  }

  private ensureDefaults(): void {
    if (!this.uploadPolicy) {
      this.uploadPolicy = newUploadPolicy();
    }
    if (!this.downloadPolicy) {
      this.downloadPolicy = newDownloadPolicy();
    }
    if (!this.deletePolicy) {
      this.deletePolicy = newDeletePolicy();
    }
    if (!this.extractPolicy) {
      this.extractPolicy = newExtractPolicy();
    }
    if (!this.bwList) {
      this.bwList = {
        whiteLists: [
          {
            path: "",
            excludePaths: [],
          },
        ],
      };
    }
  }

  toJSON(): SyncPolicy {
    this.ensureDefaults();
    return {
      uploadPolicy: this.uploadPolicy,
      downloadPolicy: this.downloadPolicy,
      deletePolicy: this.deletePolicy,
      extractPolicy: this.extractPolicy,
      bwList: this.bwList,
    };
  }
}

// ContextSync defines the context synchronization configuration
export class ContextSync {
  contextId: string;
  path: string;
  policy?: SyncPolicy;

  constructor(contextId: string, path: string, policy?: SyncPolicy) {
    if (policy) {
      validateSyncPolicy(policy);
    }
    this.contextId = contextId;
    this.path = path;
    this.policy = policy;
  }

  // WithPolicy sets the policy and returns the context sync for chaining
  withPolicy(policy: SyncPolicy): ContextSync {
    validateSyncPolicy(policy);
    this.policy = policy;
    return this;
  }
}

// NewUploadPolicy creates a new upload policy with default values
export function newUploadPolicy(): UploadPolicy {
  return {
    autoUpload: true,
    uploadStrategy: UploadStrategy.UploadBeforeResourceRelease,
  };
}

// NewDownloadPolicy creates a new download policy with default values
export function newDownloadPolicy(): DownloadPolicy {
  return {
    autoDownload: true,
    downloadStrategy: DownloadStrategy.DownloadAsync,
  };
}

// NewDeletePolicy creates a new delete policy with default values
export function newDeletePolicy(): DeletePolicy {
  return {
    syncLocalFile: true,
  };
}

// NewExtractPolicy creates a new extract policy with default values
export function newExtractPolicy(): ExtractPolicy {
  return {
    extract: true,
    deleteSrcFile: true,
    extractToCurrentFolder: false,
  };
}

// NewSyncPolicy creates a new sync policy with default values
export function newSyncPolicy(): SyncPolicy {
  return {
    uploadPolicy: newUploadPolicy(),
    downloadPolicy: newDownloadPolicy(),
    deletePolicy: newDeletePolicy(),
    extractPolicy: newExtractPolicy(),
    bwList: {
      whiteLists: [
        {
          path: "",
          excludePaths: [],
        },
      ],
    },
  };
}

export function validateSyncPolicy(policy?: SyncPolicy): void {
  if (!policy?.bwList?.whiteLists) {
    return;
  }

  for (const whitelist of policy.bwList.whiteLists) {
    WhiteListValidator.validate(whitelist);
  }
}

// NewSyncPolicyWithDefaults creates a new sync policy with partial parameters and fills defaults
export function newSyncPolicyWithDefaults(policy?: Partial<SyncPolicy>): SyncPolicy {
  return new SyncPolicyImpl(policy).toJSON();
}

// NewContextSync creates a new context sync configuration
export function newContextSync(contextId: string, path: string, policy?: SyncPolicy): ContextSync {
  if (policy) {
    validateSyncPolicy(policy);
  }
  return new ContextSync(contextId, path, policy);
}
