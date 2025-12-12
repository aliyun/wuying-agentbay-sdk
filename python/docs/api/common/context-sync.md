# Context Sync API Reference

## UploadStrategy

```python
class UploadStrategy(Enum)
```

Upload strategy for context synchronization

#### UPLOAD\_BEFORE\_RESOURCE\_RELEASE

```python
UPLOAD_BEFORE_RESOURCE_RELEASE = "UploadBeforeResourceRelease"
```

## DownloadStrategy

```python
class DownloadStrategy(Enum)
```

Download strategy for context synchronization

#### DOWNLOAD\_ASYNC

```python
DOWNLOAD_ASYNC = "DownloadAsync"
```

## UploadMode

```python
class UploadMode(Enum)
```

Upload mode for context synchronization

#### FILE

```python
FILE = "File"
```

#### ARCHIVE

```python
ARCHIVE = "Archive"
```

## Lifecycle

```python
class Lifecycle(Enum)
```

Lifecycle options for recycle policy

#### LIFECYCLE\_1DAY

```python
LIFECYCLE_1DAY = "Lifecycle_1Day"
```

#### LIFECYCLE\_3DAYS

```python
LIFECYCLE_3DAYS = "Lifecycle_3Days"
```

#### LIFECYCLE\_5DAYS

```python
LIFECYCLE_5DAYS = "Lifecycle_5Days"
```

#### LIFECYCLE\_10DAYS

```python
LIFECYCLE_10DAYS = "Lifecycle_10Days"
```

#### LIFECYCLE\_15DAYS

```python
LIFECYCLE_15DAYS = "Lifecycle_15Days"
```

#### LIFECYCLE\_30DAYS

```python
LIFECYCLE_30DAYS = "Lifecycle_30Days"
```

#### LIFECYCLE\_90DAYS

```python
LIFECYCLE_90DAYS = "Lifecycle_90Days"
```

#### LIFECYCLE\_180DAYS

```python
LIFECYCLE_180DAYS = "Lifecycle_180Days"
```

#### LIFECYCLE\_360DAYS

```python
LIFECYCLE_360DAYS = "Lifecycle_360Days"
```

#### LIFECYCLE\_FOREVER

```python
LIFECYCLE_FOREVER = "Lifecycle_Forever"
```

## UploadPolicy

```python
@dataclass
class UploadPolicy()
```

Defines the upload policy for context synchronization

**Attributes**:

    auto_upload: Enables automatic upload
    upload_strategy: Defines the upload strategy
    upload_mode: Defines the upload mode (UploadMode.FILE or UploadMode.ARCHIVE)

#### auto\_upload: `bool`

```python
auto_upload = True
```

#### upload\_strategy: `UploadStrategy`

```python
upload_strategy = UploadStrategy.UPLOAD_BEFORE_RESOURCE_RELEASE
```

#### upload\_mode: `UploadMode`

```python
upload_mode = UploadMode.FILE
```

### default

```python
@classmethod
def default(cls)
```

Creates a new upload policy with default values

## DownloadPolicy

```python
@dataclass
class DownloadPolicy()
```

Defines the download policy for context synchronization

**Attributes**:

    auto_download: Enables automatic download
    download_strategy: Defines the download strategy

#### auto\_download: `bool`

```python
auto_download = True
```

#### download\_strategy: `DownloadStrategy`

```python
download_strategy = DownloadStrategy.DOWNLOAD_ASYNC
```

### default

```python
@classmethod
def default(cls)
```

Creates a new download policy with default values

## DeletePolicy

```python
@dataclass
class DeletePolicy()
```

Defines the delete policy for context synchronization

**Attributes**:

    sync_local_file: Enables synchronization of local file deletions

#### sync\_local\_file: `bool`

```python
sync_local_file = True
```

### default

```python
@classmethod
def default(cls)
```

Creates a new delete policy with default values

## ExtractPolicy

```python
@dataclass
class ExtractPolicy()
```

Defines the extract policy for context synchronization

**Attributes**:

    extract: Enables file extraction
    delete_src_file: Enables deletion of source file after extraction

#### extract: `bool`

```python
extract = True
```

#### delete\_src\_file: `bool`

```python
delete_src_file = True
```

#### extract\_current\_folder: `bool`

```python
extract_current_folder = False
```

### default

```python
@classmethod
def default(cls)
```

Creates a new extract policy with default values

## RecyclePolicy

```python
@dataclass
class RecyclePolicy()
```

Defines the recycle policy for context synchronization

**Attributes**:

    lifecycle: Defines how long the context data should be retained
  Available options:
  - LIFECYCLE_1DAY: Keep data for 1 day
  - LIFECYCLE_3DAYS: Keep data for 3 days
  - LIFECYCLE_5DAYS: Keep data for 5 days
  - LIFECYCLE_10DAYS: Keep data for 10 days
  - LIFECYCLE_15DAYS: Keep data for 15 days
  - LIFECYCLE_30DAYS: Keep data for 30 days
  - LIFECYCLE_90DAYS: Keep data for 90 days
  - LIFECYCLE_180DAYS: Keep data for 180 days
  - LIFECYCLE_360DAYS: Keep data for 360 days
  - LIFECYCLE_FOREVER: Keep data permanently (default)
    paths: Specifies which directories or files should be subject to the recycle policy
  Rules:
  - Must use exact directory/file paths
  - Wildcard patterns (* ? [ ]) are NOT supported
  - Empty string "" means apply to all paths in the context
  - Multiple paths can be specified as a list
    Default: [""] (applies to all paths)

#### lifecycle: `Lifecycle`

```python
lifecycle = Lifecycle.LIFECYCLE_FOREVER
```

#### paths: `List[str]`

```python
paths = field(default_factory=lambda: [""])
```

### default

```python
@classmethod
def default(cls)
```

Creates a new recycle policy with default values

## WhiteList

```python
@dataclass
class WhiteList()
```

Defines the white list configuration

**Attributes**:

    path: Path to include in the white list
    exclude_paths: Paths to exclude from the white list

#### path: `str`

```python
path = ""
```

#### exclude\_paths: `List[str]`

```python
exclude_paths = field(default_factory=list)
```

## BWList

```python
@dataclass
class BWList()
```

Defines the black and white list configuration

**Attributes**:

    white_lists: Defines the white lists

#### white\_lists: `List[WhiteList]`

```python
white_lists = field(default_factory=list)
```

## MappingPolicy

```python
@dataclass
class MappingPolicy()
```

Defines the mapping policy for cross-platform context synchronization

**Attributes**:

    path: The original path from a different OS that should be mapped to the current context path

#### path: `str`

```python
path = ""
```

### default

```python
@classmethod
def default(cls)
```

Creates a new mapping policy with default values

## SyncPolicy

```python
@dataclass
class SyncPolicy()
```

Defines the synchronization policy

**Attributes**:

    upload_policy: Defines the upload policy
    download_policy: Defines the download policy
    delete_policy: Defines the delete policy
    extract_policy: Defines the extract policy
    recycle_policy: Defines the recycle policy
    bw_list: Defines the black and white list
    mapping_policy: Defines the mapping policy for cross-platform context synchronization

#### upload\_policy: `Optional[UploadPolicy]`

```python
upload_policy = None
```

#### download\_policy: `Optional[DownloadPolicy]`

```python
download_policy = None
```

#### delete\_policy: `Optional[DeletePolicy]`

```python
delete_policy = None
```

#### extract\_policy: `Optional[ExtractPolicy]`

```python
extract_policy = None
```

#### recycle\_policy: `Optional[RecyclePolicy]`

```python
recycle_policy = None
```

#### bw\_list: `Optional[BWList]`

```python
bw_list = None
```

#### mapping\_policy: `Optional[MappingPolicy]`

```python
mapping_policy = None
```

### default

```python
@classmethod
def default(cls)
```

Creates a new sync policy with default values

## ContextSync

```python
@dataclass
class ContextSync()
```

Defines the context synchronization configuration

**Attributes**:

    context_id: ID of the context to synchronize
    path: Path where the context should be mounted
    policy: Defines the synchronization policy

#### context\_id: `str`

```python
context_id = None
```

#### path: `str`

```python
path = None
```

#### policy: `Optional[SyncPolicy]`

```python
policy = None
```

### new

```python
@classmethod
def new(cls, context_id: str, path: str, policy: Optional[SyncPolicy] = None)
```

Creates a new context sync configuration

### with\_policy

```python
def with_policy(policy: SyncPolicy)
```

Sets the policy

## See Also

- [Synchronous vs Asynchronous API](../../../docs/guides/async-programming/sync-vs-async.md)

---

*Documentation generated automatically from source code using pydoc-markdown.*
