// UploadStrategy defines the upload strategy for context synchronization
export enum UploadStrategy {
  UploadBeforeResourceRelease = "UploadBeforeResourceRelease",
  UploadAfterFileClose = "UploadAfterFileClose",
  PeriodicUpload = "PERIODIC_UPLOAD"
}

// DownloadStrategy defines the download strategy for context synchronization
export enum DownloadStrategy {
  DownloadSync = "DownloadSync",
  DownloadAsync = "DownloadAsync"
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

  // WithUploadPolicy sets the upload policy
  withUploadPolicy(policy: UploadPolicy): ContextSync {
    if (!this.policy) {
      this.policy = newSyncPolicy();
    }
    this.policy.uploadPolicy = policy;
    return this;
  }

  // WithDownloadPolicy sets the download policy
  withDownloadPolicy(policy: DownloadPolicy): ContextSync {
    if (!this.policy) {
      this.policy = newSyncPolicy();
    }
    this.policy.downloadPolicy = policy;
    return this;
  }

  // WithDeletePolicy sets the delete policy
  withDeletePolicy(policy: DeletePolicy): ContextSync {
    if (!this.policy) {
      this.policy = newSyncPolicy();
    }
    this.policy.deletePolicy = policy;
    return this;
  }

  // WithBWList sets the black and white list
  withBWList(bwList: BWList): ContextSync {
    if (!this.policy) {
      this.policy = newSyncPolicy();
    }
    this.policy.bwList = bwList;
    return this;
  }

  // WithWhiteList sets the white list
  withWhiteList(path: string, excludePaths: string[] = []): ContextSync {
    const whiteList: WhiteList = {
      path,
      excludePaths
    };
    const bwList: BWList = {
      whiteLists: [whiteList]
    };
    return this.withBWList(bwList);
  }

  // WithWhiteLists sets multiple white lists
  withWhiteLists(whiteLists: WhiteList[]): ContextSync {
    const bwList: BWList = {
      whiteLists
    };
    return this.withBWList(bwList);
  }

  // WithSyncPaths sets the sync paths
  withSyncPaths(syncPaths: string[]): ContextSync {
    if (!this.policy) {
      this.policy = newSyncPolicy();
    }
    this.policy.syncPaths = syncPaths;
    return this;
  }
}

// NewUploadPolicy creates a new upload policy with default values
export function newUploadPolicy(): UploadPolicy {
  return {
    autoUpload: true,
    uploadStrategy: UploadStrategy.UploadBeforeResourceRelease,
    period: 30 // Default to 30 minutes
  };
}

// NewDownloadPolicy creates a new download policy with default values
export function newDownloadPolicy(): DownloadPolicy {
  return {
    autoDownload: true,
    downloadStrategy: DownloadStrategy.DownloadAsync
  };
}

// NewDeletePolicy creates a new delete policy with default values
export function newDeletePolicy(): DeletePolicy {
  return {
    syncLocalFile: true
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
          excludePaths: []
        }
      ]
    },
    syncPaths: [""]
  };
}

// NewContextSync creates a new context sync configuration
export function newContextSync(contextId: string, path: string): ContextSync {
  return new ContextSync(contextId, path, newSyncPolicy());
}

// NewBasicContextSync creates a basic context sync configuration with default policies
export function newBasicContextSync(contextId: string, path: string): ContextSync {
  return new ContextSync(contextId, path, newSyncPolicy());
}

// NewContextSyncWithoutPolicy creates a context sync configuration without any policies
export function newContextSyncWithoutPolicy(contextId: string, path: string): ContextSync {
  return new ContextSync(contextId, path);
}