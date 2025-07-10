# Context Sync Example

This example demonstrates how to use the context synchronization functionality in the AgentBay TypeScript SDK. It shows how to create context sync configurations and use them when creating sessions.

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
- `autoUpload`: Whether to automatically upload files
- `uploadStrategy`: Strategy for uploading (PERIODIC_UPLOAD, UPLOAD_BEFORE_RESOURCE_RELEASE, UPLOAD_AFTER_FILE_CLOSE)
- `period`: Upload interval in minutes (for periodic uploads)

### Download Policy
- `autoDownload`: Whether to automatically download files
- `downloadStrategy`: Strategy for downloading (DOWNLOAD_SYNC, DOWNLOAD_ASYNC)

### Delete Policy
- `syncLocalFile`: Whether to sync local file deletions

### Black/White List
- `WhiteList`: Paths to include in synchronization
- `excludePaths`: Paths to exclude from synchronization

## Usage

```typescript
import { AgentBay } from "../src/agent-bay";
import {
  newBasicContextSync,
  newContextSync,
  UploadStrategy,
  DownloadStrategy
} from "../src/context-sync";

// Create a context sync configuration
const contextSync = newContextSync(contextId, "/data")
  .withUploadPolicy({
    autoUpload: true,
    uploadStrategy: UploadStrategy.PeriodicUpload,
    period: 15,
  })
  .withDownloadPolicy({
    autoDownload: true,
    downloadStrategy: DownloadStrategy.DownloadAsync,
  })
  .withWhiteList("/data/important", ["/data/important/temp"]);

// Create session with context sync
const sessionParams = newCreateSessionParams();
sessionParams.addContextSyncConfig(contextSync);
const sessionResult = await agentBay.create(sessionParams);

// Use context manager from session
const contextInfo = await session.context.info();
const syncResult = await session.context.sync();
```

## Running the Example

```bash
cd typescript/examples
npx ts-node context-sync-example.ts
```

Or compile and run:

```bash
cd typescript
npm run build
node dist/examples/context-sync-example.js
```

Make sure you have set the `AGENTBAY_API_KEY` environment variable or replace the placeholder in the code with your actual API key.

## Prerequisites

- Node.js 14 or later
- TypeScript 4.5 or later
- Valid AgentBay API key
- Network access to AgentBay services

## Key Differences from Go Version

- Uses `async/await` for asynchronous operations
- Uses `camelCase` naming convention instead of `PascalCase`
- Error handling with `try/catch` blocks
- Promise-based API calls
- TypeScript type definitions for better type safety

## Upload Strategies

- `UploadStrategy.UploadBeforeResourceRelease`: Upload files before resource is released
- `UploadStrategy.UploadAfterFileClose`: Upload files after file is closed
- `UploadStrategy.PeriodicUpload`: Upload files periodically based on the specified period

## Download Strategies

- `DownloadStrategy.DownloadSync`: Download files synchronously
- `DownloadStrategy.DownloadAsync`: Download files asynchronously

## Related Documentation

- [Context Management](../../docs/concepts/contexts.md)
- [Session Management](../../docs/concepts/sessions.md)
- [API Reference](../../docs/api-reference/)
