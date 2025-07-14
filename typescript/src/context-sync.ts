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
  period?: number;
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

// WhiteList defines the white list configuration
export interface WhiteList {
  path: string;
  excludePaths?: string[];
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
  bwList?: BWList;
  syncPaths?: string[];
}

// ContextSync defines the context synchronization configuration
export class ContextSync {
  contextId: string;
  path: string;
  policy?: SyncPolicy;

  constructor(contextId: string, path: string, policy?: SyncPolicy) {
    this.contextId = contextId;
    this.path = path;
    this.policy = policy;
  }

  // WithPolicy sets the policy and returns the context sync for chaining
  withPolicy(policy: SyncPolicy): ContextSync {
    this.policy = policy;
    return this;
  }
}

// NewUploadPolicy creates a new upload policy with default values
export function newUploadPolicy(): UploadPolicy {
  return {
    autoUpload: true,
    uploadStrategy: UploadStrategy.UploadBeforeResourceRelease,
    period: 30, // Default to 30 minutes
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

// NewSyncPolicy creates a new sync policy with default values
export function newSyncPolicy(): SyncPolicy {
  return {
    uploadPolicy: newUploadPolicy(),
    downloadPolicy: newDownloadPolicy(),
    deletePolicy: newDeletePolicy(),
    bwList: {
      whiteLists: [
        {
          path: "",
          excludePaths: [],
        },
      ],
    },
    syncPaths: [""],
  };
}

// NewContextSync creates a new context sync configuration
export function newContextSync(contextId: string, path: string, policy?: SyncPolicy): ContextSync {
  return new ContextSync(contextId, path, policy);
}
