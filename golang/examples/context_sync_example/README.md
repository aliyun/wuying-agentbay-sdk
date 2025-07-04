# Context Sync Example

This example demonstrates how to use the context synchronization functionality in the Wuying AgentBay SDK. It shows how to create context sync configurations and use them when creating sessions.

## Features Demonstrated

1. **Context Management**: Creating and managing contexts
2. **Basic Context Sync**: Simple context synchronization configuration
3. **Advanced Context Sync**: Complex sync policies with upload/download strategies
4. **Session Integration**: Creating sessions with context sync configurations  
5. **Context Manager**: Using the context manager from within a session
6. **Builder Pattern**: Creating context sync configurations using fluent API

## Context Sync Policies

The example shows how to configure various synchronization policies:

### Upload Policy
- `AutoUpload`: Whether to automatically upload files
- `UploadStrategy`: Strategy for uploading (PERIODIC_UPLOAD, IMMEDIATE_UPLOAD)
- `Period`: Upload interval in minutes (for periodic uploads)

### Download Policy
- `AutoDownload`: Whether to automatically download files
- `DownloadStrategy`: Strategy for downloading (DOWNLOAD_BEFORE_CONNECTED, DOWNLOAD_ON_DEMAND)

### Delete Policy
- `SyncLocalFile`: Whether to sync local file deletions

### Sync Mode
- `SOURCE_FILE`: Synchronize source files only
- `FULL_SYNC`: Perform full synchronization

### Black/White List
- `WhiteList`: Paths to include in synchronization
- `ExcludePaths`: Paths to exclude from synchronization

## Usage

```go
// Create a context sync configuration
contextSync := agentbay.NewContextSync(contextID, "/data").
    WithSyncMode(agentbay.SourceFile).
    WithUploadPolicy(&agentbay.UploadPolicy{
        AutoUpload:     true,
        UploadStrategy: agentbay.PeriodicUpload,
        Period:         15,
    }).
    WithDownloadPolicy(&agentbay.DownloadPolicy{
        AutoDownload:     true,
        DownloadStrategy: agentbay.DownloadBeforeConnected,
    }).
    WithWhiteList("/data/important", []string{"/data/important/temp"})

// Create session with context sync
sessionParams := agentbay.NewCreateSessionParams()
sessionParams.AddContextSyncConfig(contextSync)
session, err := agentBay.Create(sessionParams)

// Use context manager from session
contextInfo, err := session.Context.Info()
syncResult, err := session.Context.Sync()
```

## Running the Example

```bash
cd context_sync_example
go run main.go
```

Make sure you have set the `AGENTBAY_API_KEY` environment variable or replace the placeholder in the code with your actual API key.

## Prerequisites

- Go 1.19 or later
- Valid AgentBay API key
- Network access to AgentBay services

## Related Documentation

- [Context Management](../../docs/concepts/contexts.md)
- [Session Management](../../docs/concepts/sessions.md)
- [API Reference](../../docs/api-reference/) 