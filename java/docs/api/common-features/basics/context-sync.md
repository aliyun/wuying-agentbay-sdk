# Context Sync API Reference

## 📦 Related Tutorial

- [First Session Tutorial](../../../../../docs/quickstart/first-session.md) - Get started with creating your first AgentBay session

## Overview

The Context Sync API provides configuration classes for defining how data is synchronized between sessions and persistent storage contexts. These classes allow fine-grained control over upload, download, extraction, and deletion policies.

## UploadStrategy

```java
public enum UploadStrategy
```

Upload strategy for context synchronization.

### UPLOAD_BEFORE_RESOURCE_RELEASE

```java
UPLOAD_BEFORE_RESOURCE_RELEASE
```

Upload context data before releasing session resources.

**Value**: `"UploadBeforeResourceRelease"`

## DownloadStrategy

```java
public enum DownloadStrategy
```

Download strategy for context synchronization.

### DOWNLOAD_ASYNC

```java
DOWNLOAD_ASYNC
```

Download context data asynchronously.

**Value**: `"DownloadAsync"`

## UploadMode

```java
public enum UploadMode
```

Upload mode for context synchronization.

### FILE

```java
FILE
```

Upload files individually.

**Value**: `"File"`

### ARCHIVE

```java
ARCHIVE
```

Upload files as an archive.

**Value**: `"Archive"`

## UploadPolicy

```java
public class UploadPolicy
```

Defines the upload policy for context synchronization.

### Fields

#### autoUpload

```java
private boolean autoUpload = true
```

Enables automatic upload of context data.

**Default**: `true`

#### uploadStrategy

```java
private UploadStrategy uploadStrategy = UploadStrategy.UPLOAD_BEFORE_RESOURCE_RELEASE
```

Defines when to upload context data.

**Default**: `UploadStrategy.UPLOAD_BEFORE_RESOURCE_RELEASE`

#### uploadMode

```java
private UploadMode uploadMode = UploadMode.FILE
```

Defines how to upload context data.

**Default**: `UploadMode.FILE`

#### period

```java
private Integer period = 30
```

Upload period in seconds (for periodic uploads).

**Default**: `30`

### Constructor

```java
public UploadPolicy()
public UploadPolicy(boolean autoUpload, UploadStrategy uploadStrategy, Integer period)
public UploadPolicy(boolean autoUpload, UploadStrategy uploadStrategy, UploadMode uploadMode, Integer period)
```

### Methods

#### defaultPolicy

```java
public static UploadPolicy defaultPolicy()
```

Creates a new upload policy with default values.

**Returns:**
- `UploadPolicy`: Default upload policy

**Example:**

```java
UploadPolicy policy = UploadPolicy.defaultPolicy();
```

#### Getters and Setters

```java
public boolean isAutoUpload()
public void setAutoUpload(boolean autoUpload)

public UploadStrategy getUploadStrategy()
public void setUploadStrategy(UploadStrategy uploadStrategy)

public UploadMode getUploadMode()
public void setUploadMode(UploadMode uploadMode)

public Integer getPeriod()
public void setPeriod(Integer period)
```

**Example:**

```java
UploadPolicy uploadPolicy = new UploadPolicy();
uploadPolicy.setAutoUpload(true);
uploadPolicy.setUploadStrategy(UploadStrategy.UPLOAD_BEFORE_RESOURCE_RELEASE);
uploadPolicy.setUploadMode(UploadMode.FILE);
uploadPolicy.setPeriod(30);
```

## DownloadPolicy

```java
public class DownloadPolicy
```

Defines the download policy for context synchronization.

### Fields

#### autoDownload

```java
private boolean autoDownload = true
```

Enables automatic download of context data.

**Default**: `true`

#### downloadStrategy

```java
private DownloadStrategy downloadStrategy = DownloadStrategy.DOWNLOAD_ASYNC
```

Defines when to download context data.

**Default**: `DownloadStrategy.DOWNLOAD_ASYNC`

### Constructor

```java
public DownloadPolicy()
public DownloadPolicy(boolean autoDownload, DownloadStrategy downloadStrategy)
```

### Methods

#### defaultPolicy

```java
public static DownloadPolicy defaultPolicy()
```

Creates a new download policy with default values.

**Returns:**
- `DownloadPolicy`: Default download policy

**Example:**

```java
DownloadPolicy policy = DownloadPolicy.defaultPolicy();
```

#### Getters and Setters

```java
public boolean isAutoDownload()
public void setAutoDownload(boolean autoDownload)

public DownloadStrategy getDownloadStrategy()
public void setDownloadStrategy(DownloadStrategy downloadStrategy)
```

**Example:**

```java
DownloadPolicy downloadPolicy = new DownloadPolicy();
downloadPolicy.setAutoDownload(true);
downloadPolicy.setDownloadStrategy(DownloadStrategy.DOWNLOAD_ASYNC);
```

## DeletePolicy

```java
public class DeletePolicy
```

Defines the delete policy for context synchronization.

### Fields

#### syncLocalFile

```java
private boolean syncLocalFile = true
```

Enables synchronization of local file deletions to context storage.

**Default**: `true`

### Constructor

```java
public DeletePolicy()
public DeletePolicy(boolean syncLocalFile)
```

### Methods

#### defaultPolicy

```java
public static DeletePolicy defaultPolicy()
```

Creates a new delete policy with default values.

**Returns:**
- `DeletePolicy`: Default delete policy

**Example:**

```java
DeletePolicy policy = DeletePolicy.defaultPolicy();
```

#### Getters and Setters

```java
public boolean isSyncLocalFile()
public void setSyncLocalFile(boolean syncLocalFile)
```

**Example:**

```java
DeletePolicy deletePolicy = new DeletePolicy();
deletePolicy.setSyncLocalFile(true);
```

## ExtractPolicy

```java
public class ExtractPolicy
```

Defines the extract policy for context synchronization.

### Fields

#### extract

```java
private boolean extract = true
```

Enables file extraction from archives.

**Default**: `true`

#### deleteSrcFile

```java
private boolean deleteSrcFile = true
```

Enables deletion of source archive file after extraction.

**Default**: `true`

#### extractCurrentFolder

```java
private boolean extractCurrentFolder = false
```

Extract to current folder instead of creating a new folder.

**Default**: `false`

### Constructor

```java
public ExtractPolicy()
public ExtractPolicy(boolean extract, boolean deleteSrcFile, boolean extractCurrentFolder)
```

### Methods

#### defaultPolicy

```java
public static ExtractPolicy defaultPolicy()
```

Creates a new extract policy with default values.

**Returns:**
- `ExtractPolicy`: Default extract policy

**Example:**

```java
ExtractPolicy policy = ExtractPolicy.defaultPolicy();
```

#### Getters and Setters

```java
public boolean isExtract()
public void setExtract(boolean extract)

public boolean isDeleteSrcFile()
public void setDeleteSrcFile(boolean deleteSrcFile)

public boolean isExtractCurrentFolder()
public void setExtractCurrentFolder(boolean extractCurrentFolder)
```

**Example:**

```java
ExtractPolicy extractPolicy = new ExtractPolicy();
extractPolicy.setExtract(true);
extractPolicy.setDeleteSrcFile(true);
extractPolicy.setExtractCurrentFolder(false);
```

## WhiteList

```java
public class WhiteList
```

Defines the white list configuration for selective synchronization.

### Fields

#### path

```java
private String path = ""
```

Path to include in the white list.

**Default**: `""` (all paths)

#### excludePaths

```java
private List<String> excludePaths = new ArrayList<>()
```

Paths to exclude from the white list.

**Default**: Empty list

### Constructor

```java
public WhiteList()
public WhiteList(String path, List<String> excludePaths)
```

### Methods

#### Getters and Setters

```java
public String getPath()
public void setPath(String path)

public List<String> getExcludePaths()
public void setExcludePaths(List<String> excludePaths)
```

**Example:**

```java
// Include all files in /data, except /data/temp
WhiteList whiteList = new WhiteList("/data", Arrays.asList("/data/temp"));
```

## BWList

```java
public class BWList
```

Defines the black and white list configuration.

### Fields

#### whiteLists

```java
private List<WhiteList> whiteLists = new ArrayList<>()
```

List of white list configurations.

**Default**: Empty list

### Constructor

```java
public BWList()
public BWList(List<WhiteList> whiteLists)
```

### Methods

#### Getters and Setters

```java
public List<WhiteList> getWhiteLists()
public void setWhiteLists(List<WhiteList> whiteLists)
```

**Example:**

```java
WhiteList dataWhiteList = new WhiteList("/data", Arrays.asList("/data/temp"));
WhiteList configWhiteList = new WhiteList("/config", new ArrayList<>());

BWList bwList = new BWList(Arrays.asList(dataWhiteList, configWhiteList));
```

## SyncPolicy

```java
public class SyncPolicy
```

Defines the complete synchronization policy combining all sub-policies.

### Fields

#### uploadPolicy

```java
private UploadPolicy uploadPolicy
```

Defines the upload policy.

#### downloadPolicy

```java
private DownloadPolicy downloadPolicy
```

Defines the download policy.

#### deletePolicy

```java
private DeletePolicy deletePolicy
```

Defines the delete policy.

#### extractPolicy

```java
private ExtractPolicy extractPolicy
```

Defines the extract policy.

#### bwList

```java
private BWList bwList
```

Defines the black and white list configuration.

### Constructor

```java
public SyncPolicy()
public SyncPolicy(UploadPolicy uploadPolicy, DownloadPolicy downloadPolicy,
                 DeletePolicy deletePolicy, ExtractPolicy extractPolicy, BWList bwList)
```

### Methods

#### defaultPolicy

```java
public static SyncPolicy defaultPolicy()
```

Creates a new sync policy with default values for all sub-policies.

**Returns:**
- `SyncPolicy`: Default sync policy

**Example:**

```java
SyncPolicy policy = SyncPolicy.defaultPolicy();
```

#### Getters and Setters

```java
public UploadPolicy getUploadPolicy()
public void setUploadPolicy(UploadPolicy uploadPolicy)

public DownloadPolicy getDownloadPolicy()
public void setDownloadPolicy(DownloadPolicy downloadPolicy)

public DeletePolicy getDeletePolicy()
public void setDeletePolicy(DeletePolicy deletePolicy)

public ExtractPolicy getExtractPolicy()
public void setExtractPolicy(ExtractPolicy extractPolicy)

public BWList getBwList()
public void setBwList(BWList bwList)
```

**Example:**

```java
// Create custom sync policy
UploadPolicy uploadPolicy = new UploadPolicy();
uploadPolicy.setUploadMode(UploadMode.ARCHIVE);

DownloadPolicy downloadPolicy = DownloadPolicy.defaultPolicy();
DeletePolicy deletePolicy = DeletePolicy.defaultPolicy();
ExtractPolicy extractPolicy = ExtractPolicy.defaultPolicy();

WhiteList whiteList = new WhiteList("/data", new ArrayList<>());
BWList bwList = new BWList(Arrays.asList(whiteList));

SyncPolicy syncPolicy = new SyncPolicy(
    uploadPolicy,
    downloadPolicy,
    deletePolicy,
    extractPolicy,
    bwList
);
```

## ContextSync

```java
public class ContextSync
```

Defines the context synchronization configuration linking a context to a session path.

### Fields

#### contextId

```java
private String contextId
```

ID of the context to synchronize.

#### path

```java
private String path
```

Path where the context should be mounted in the session.

#### policy

```java
private SyncPolicy policy
```

Defines the synchronization policy.

### Constructor

```java
public ContextSync()
public ContextSync(String contextId, String path, SyncPolicy policy)
```

### Methods

#### create

```java
public static ContextSync create(String contextId, String path, SyncPolicy policy)
```

Creates a new context sync configuration.

**Parameters:**
- `contextId` (String): Context ID
- `path` (String): Mount path in session
- `policy` (SyncPolicy): Synchronization policy

**Returns:**
- `ContextSync`: New context sync configuration

**Example:**

```java
ContextSync contextSync = ContextSync.create(
    "context-id-123",
    "/data",
    SyncPolicy.defaultPolicy()
);
```

#### withPolicy

```java
public ContextSync withPolicy(SyncPolicy policy)
```

Sets the synchronization policy and returns this instance for method chaining.

**Parameters:**
- `policy` (SyncPolicy): Synchronization policy

**Returns:**
- `ContextSync`: This instance

**Example:**

```java
ContextSync contextSync = ContextSync.create("context-id", "/data", null)
    .withPolicy(SyncPolicy.defaultPolicy());
```

#### Getters and Setters

```java
public String getContextId()
public void setContextId(String contextId)

public String getPath()
public void setPath(String path)

public SyncPolicy getPolicy()
public void setPolicy(SyncPolicy policy)
```

## Complete Usage Example

```java
import com.aliyun.agentbay.AgentBay;
import com.aliyun.agentbay.session.Session;
import com.aliyun.agentbay.session.CreateSessionParams;
import com.aliyun.agentbay.context.*;
import com.aliyun.agentbay.model.ContextResult;

public class ContextSyncExample {
    public static void main(String[] args) throws Exception {
        AgentBay agentBay = new AgentBay(System.getenv("AGENTBAY_API_KEY"));
        
        // Get or create context
        ContextResult contextResult = agentBay.getContext().get("my-project", true);
        Context context = contextResult.getContext();
        
        // Create custom sync policy
        UploadPolicy uploadPolicy = new UploadPolicy();
        uploadPolicy.setAutoUpload(true);
        uploadPolicy.setUploadMode(UploadMode.ARCHIVE);
        
        DownloadPolicy downloadPolicy = new DownloadPolicy();
        downloadPolicy.setAutoDownload(true);
        
        // Configure white list - sync only /data, exclude /data/temp
        WhiteList whiteList = new WhiteList("/data", Arrays.asList("/data/temp"));
        BWList bwList = new BWList(Arrays.asList(whiteList));
        
        SyncPolicy syncPolicy = new SyncPolicy(
            uploadPolicy,
            downloadPolicy,
            DeletePolicy.defaultPolicy(),
            ExtractPolicy.defaultPolicy(),
            bwList
        );
        
        // Create context sync configuration
        ContextSync contextSync = ContextSync.create(
            context.getId(),
            "/data",
            syncPolicy
        );
        
        // Create session with context sync
        CreateSessionParams params = new CreateSessionParams();
        params.setContextSyncs(Arrays.asList(contextSync));
        
        Session session = agentBay.create(params).getSession();
        
        // Work with files - they'll be synced according to policy
        session.getFileSystem().writeFile("/data/output.txt", "results", "overwrite", false);
        session.getFileSystem().writeFile("/data/temp/cache.txt", "temp", "overwrite", false);
        
        // Delete with sync - only /data/output.txt will be synced (temp excluded)
        session.delete(true);
        
        System.out.println("Session completed with context synchronization");
    }
}
```

## Best Practices

1. **Default Policies**: Use `SyncPolicy.defaultPolicy()` for most cases
2. **Archive Mode**: Use `UploadMode.ARCHIVE` for large numbers of small files
3. **White Lists**: Configure white lists to sync only necessary files
4. **Auto Upload**: Enable auto upload to ensure data is saved on session deletion
5. **Extract Policy**: Configure extract policy for compressed context data
6. **Path Organization**: Use clear directory structures for easier white list configuration

## Common Patterns

### Simple Context Sync

```java
// Using default policy
ContextSync contextSync = ContextSync.create(
    contextId,
    "/workspace",
    SyncPolicy.defaultPolicy()
);
```

### Archive Upload Mode

```java
// Upload as archive for better performance with many files
UploadPolicy uploadPolicy = new UploadPolicy();
uploadPolicy.setUploadMode(UploadMode.ARCHIVE);

SyncPolicy policy = SyncPolicy.defaultPolicy();
policy.setUploadPolicy(uploadPolicy);

ContextSync contextSync = ContextSync.create(contextId, "/data", policy);
```

### Selective Synchronization

```java
// Sync only specific directories
WhiteList dataWhiteList = new WhiteList("/data/output", new ArrayList<>());
WhiteList logsWhiteList = new WhiteList("/logs", Arrays.asList("/logs/temp"));
BWList bwList = new BWList(Arrays.asList(dataWhiteList, logsWhiteList));

SyncPolicy policy = SyncPolicy.defaultPolicy();
policy.setBwList(bwList);

ContextSync contextSync = ContextSync.create(contextId, "/workspace", policy);
```

## Related Resources

- [Context API Reference](context.md)
- [Session API Reference](session.md)
- [AgentBay API Reference](agentbay.md)
- [Session Context Example](../../../../agentbay/src/main/java/com/aliyun/agentbay/examples/SessionContextExample.java)
- [Context Sync Lifecycle Example](../../../../agentbay/src/main/java/com/aliyun/agentbay/examples/ContextSyncLifecycleExample.java)

---

*Documentation for AgentBay Java SDK*
