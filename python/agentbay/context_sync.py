from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class UploadStrategy(Enum):
    """Upload strategy for context synchronization"""
    UPLOAD_BEFORE_RESOURCE_RELEASE = "UploadBeforeResourceRelease"
    UPLOAD_AFTER_FILE_CLOSE = "UploadAfterFileClose"
    PERIODIC_UPLOAD = "PERIODIC_UPLOAD"


class DownloadStrategy(Enum):
    """Download strategy for context synchronization"""
    DOWNLOAD_SYNC = "DownloadSync"
    DOWNLOAD_ASYNC = "DownloadAsync"


@dataclass
class UploadPolicy:
    """
    Defines the upload policy for context synchronization
    
    Attributes:
        auto_upload: Enables automatic upload
        upload_strategy: Defines the upload strategy
        period: Defines the upload period in minutes (for periodic upload)
    """
    auto_upload: bool = True
    upload_strategy: UploadStrategy = UploadStrategy.UPLOAD_BEFORE_RESOURCE_RELEASE
    period: Optional[int] = 30  # Default to 30 minutes

    @classmethod
    def default(cls):
        """Creates a new upload policy with default values"""
        return cls()


@dataclass
class DownloadPolicy:
    """
    Defines the download policy for context synchronization
    
    Attributes:
        auto_download: Enables automatic download
        download_strategy: Defines the download strategy
    """
    auto_download: bool = True
    download_strategy: DownloadStrategy = DownloadStrategy.DOWNLOAD_ASYNC

    @classmethod
    def default(cls):
        """Creates a new download policy with default values"""
        return cls()


@dataclass
class DeletePolicy:
    """
    Defines the delete policy for context synchronization
    
    Attributes:
        sync_local_file: Enables synchronization of local file deletions
    """
    sync_local_file: bool = True

    @classmethod
    def default(cls):
        """Creates a new delete policy with default values"""
        return cls()


@dataclass
class WhiteList:
    """
    Defines the white list configuration
    
    Attributes:
        path: Path to include in the white list
        exclude_paths: Paths to exclude from the white list
    """
    path: str = ""
    exclude_paths: List[str] = field(default_factory=list)


@dataclass
class BWList:
    """
    Defines the black and white list configuration
    
    Attributes:
        white_lists: Defines the white lists
    """
    white_lists: List[WhiteList] = field(default_factory=list)


@dataclass
class SyncPolicy:
    """
    Defines the synchronization policy
    
    Attributes:
        upload_policy: Defines the upload policy
        download_policy: Defines the download policy
        delete_policy: Defines the delete policy
        bw_list: Defines the black and white list
        sync_paths: Defines the paths to synchronize
    """
    upload_policy: Optional[UploadPolicy] = None
    download_policy: Optional[DownloadPolicy] = None
    delete_policy: Optional[DeletePolicy] = None
    bw_list: Optional[BWList] = None
    sync_paths: List[str] = field(default_factory=list)

    @classmethod
    def default(cls):
        """Creates a new sync policy with default values"""
        return cls(
            upload_policy=UploadPolicy.default(),
            download_policy=DownloadPolicy.default(),
            delete_policy=DeletePolicy.default(),
            bw_list=BWList(
                white_lists=[
                    WhiteList(
                        path="",
                        exclude_paths=[]
                    )
                ]
            ),
            sync_paths=[""]
        )


@dataclass
class ContextSync:
    """
    Defines the context synchronization configuration
    
    Attributes:
        context_id: ID of the context to synchronize
        path: Path where the context should be mounted
        policy: Defines the synchronization policy
    """
    context_id: str
    path: str
    policy: Optional[SyncPolicy] = None

    @classmethod
    def new(cls, context_id: str, path: str, policy: Optional[SyncPolicy] = None):
        """Creates a new context sync configuration"""
        return cls(context_id=context_id, path=path, policy=policy)

    def with_policy(self, policy: SyncPolicy):
        """Sets the policy"""
        self.policy = policy
        return self 