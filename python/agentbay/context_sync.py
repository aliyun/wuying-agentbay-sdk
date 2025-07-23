from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class UploadStrategy(Enum):
    """Upload strategy for context synchronization"""

    UPLOAD_BEFORE_RESOURCE_RELEASE = "UploadBeforeResourceRelease"


class DownloadStrategy(Enum):
    """Download strategy for context synchronization"""

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

    def __dict__(self):
        return {
            "autoUpload": self.auto_upload,
            "uploadStrategy": (
                self.upload_strategy.value if self.upload_strategy else None
            ),
            "period": self.period,
        }


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

    def __dict__(self):
        return {
            "autoDownload": self.auto_download,
            "downloadStrategy": (
                self.download_strategy.value if self.download_strategy else None
            ),
        }


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

    def __dict__(self):
        return {"syncLocalFile": self.sync_local_file}


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

    def __dict__(self):
        return {"path": self.path, "excludePaths": self.exclude_paths}


@dataclass
class BWList:
    """
    Defines the black and white list configuration

    Attributes:
        white_lists: Defines the white lists
    """

    white_lists: List[WhiteList] = field(default_factory=list)

    def __dict__(self):
        return {
            "whiteLists": (
                [wl.__dict__() for wl in self.white_lists] if self.white_lists else []
            )
        }


@dataclass
class SyncPolicy:
    """
    Defines the synchronization policy

    Attributes:
        upload_policy: Defines the upload policy
        download_policy: Defines the download policy
        delete_policy: Defines the delete policy
        bw_list: Defines the black and white list
    """

    upload_policy: Optional[UploadPolicy] = None
    download_policy: Optional[DownloadPolicy] = None
    delete_policy: Optional[DeletePolicy] = None
    bw_list: Optional[BWList] = None

    def __post_init__(self):
        """Post-initialization to ensure all policies have default values if not provided"""
        if self.upload_policy is None:
            self.upload_policy = UploadPolicy.default()
        if self.download_policy is None:
            self.download_policy = DownloadPolicy.default()
        if self.delete_policy is None:
            self.delete_policy = DeletePolicy.default()
        if self.bw_list is None:
            self.bw_list = BWList(white_lists=[WhiteList(path="", exclude_paths=[])])

    @classmethod
    def default(cls):
        """Creates a new sync policy with default values"""
        return cls(
            upload_policy=UploadPolicy.default(),
            download_policy=DownloadPolicy.default(),
            delete_policy=DeletePolicy.default(),
            bw_list=BWList(white_lists=[WhiteList(path="", exclude_paths=[])]),
        )

    def __dict__(self):
        result = {}
        if self.upload_policy:
            result["uploadPolicy"] = self.upload_policy.__dict__()
        if self.download_policy:
            result["downloadPolicy"] = self.download_policy.__dict__()
        if self.delete_policy:
            result["deletePolicy"] = self.delete_policy.__dict__()
        if self.bw_list:
            result["bwList"] = self.bw_list.__dict__()
        return result


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
