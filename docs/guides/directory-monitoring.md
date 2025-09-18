# Directory Monitoring Guide

This guide explains how to use the directory monitoring functionality in AgentBay SDK to watch for file changes in real-time.

## Overview

The directory monitoring feature allows you to:
- Monitor a directory for file changes (create, modify, delete)
- Receive real-time notifications when changes occur
- Filter events by type (file vs directory)
- Handle events with custom callback functions

## Basic Usage

### Python

```python
import os
import time
import threading
from agentbay import AgentBay
from agentbay.session_params import CreateSessionParams

# Initialize AgentBay
api_key = os.getenv("AGENTBAY_API_KEY")
agentbay = AgentBay(api_key=api_key)

# Create session
session_params = CreateSessionParams(image_id="code_latest")
session_result = agentbay.create(session_params)
session = session_result.session

# Define callback function
def on_file_change(events):
    for event in events:
        print(f"{event.event_type}: {event.path} ({event.path_type})")

# Start monitoring
monitor_thread = session.file_system.watch_directory(
    path="/tmp/my_directory",
    callback=on_file_change,
    interval=1.0  # Check every second
)
monitor_thread.start()

# Do your work...
time.sleep(10)

# Stop monitoring
monitor_thread.stop_event.set()
monitor_thread.join()

# Clean up
agentbay.delete(session)
```

### TypeScript

```typescript
import { AgentBay, CreateSessionParams } from "wuying-agentbay-sdk";

async function main() {
  // Initialize AgentBay
  const apiKey = process.env.AGENTBAY_API_KEY!;
  const agentbay = new AgentBay({ apiKey });

  // Create session
  const sessionParams: CreateSessionParams = { imageId: "code_latest" };
  const sessionResult = await agentbay.create(sessionParams);
  const session = sessionResult.session;

  // Define callback function
  const onFileChange = (events) => {
    for (const event of events) {
      console.log(`${event.eventType}: ${event.path} (${event.pathType})`);
    }
  };

  // Start monitoring
  const controller = new AbortController();
  const watchPromise = session.fileSystem.watchDirectory(
    "/tmp/my_directory",
    onFileChange,
    1000, // Check every second
    controller.signal
  );

  // Do your work...
  await new Promise(resolve => setTimeout(resolve, 10000));

  // Stop monitoring
  controller.abort();
  await watchPromise;

  // Clean up
  await agentbay.delete(session);
}
```

### Go

```go
package main

import (
    "fmt"
    "os"
    "sync"
    "time"

    "github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
    "github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/filesystem"
)

func main() {
    // Initialize AgentBay
    apiKey := os.Getenv("AGENTBAY_API_KEY")
    agentbay, err := agentbay.NewAgentBay(apiKey)
    if err != nil {
        panic(err)
    }

    // Create session
    sessionParams := &agentbay.CreateSessionParams{
        ImageId: "code_latest",
    }
    sessionResult, err := agentbay.Create(sessionParams)
    if err != nil {
        panic(err)
    }
    session := sessionResult.Session

    // Define callback function
    callback := func(events []*filesystem.FileChangeEvent) {
        for _, event := range events {
            fmt.Printf("%s: %s (%s)\n", event.EventType, event.Path, event.PathType)
        }
    }

    // Start monitoring
    stopCh := make(chan struct{})
    wg := session.FileSystem().WatchDirectory(
        "/tmp/my_directory",
        callback,
        1*time.Second, // Check every second
        stopCh,
    )

    // Do your work...
    time.Sleep(10 * time.Second)

    // Stop monitoring
    close(stopCh)
    wg.Wait()

    // Clean up
    agentbay.Delete(session)
}
```

## Advanced Usage

### Filtering Events

You can filter events in your callback function:

```python
def on_file_change(events):
    # Only process file modifications
    for event in events:
        if event.event_type == "modify" and event.path_type == "file":
            print(f"File modified: {event.path}")
```

### Using FileChangeResult Helper Methods

```python
def on_file_change(events):
    # Create a result object for easier processing
    from agentbay.filesystem.filesystem import FileChangeResult
    
    result = FileChangeResult(success=True, events=events)
    
    modified_files = result.get_modified_files()
    created_files = result.get_created_files()
    deleted_files = result.get_deleted_files()
    
    if modified_files:
        print(f"Modified files: {modified_files}")
    if created_files:
        print(f"Created files: {created_files}")
    if deleted_files:
        print(f"Deleted files: {deleted_files}")
```

### Error Handling

```python
def on_file_change(events):
    try:
        for event in events:
            # Process event
            process_file_change(event)
    except Exception as e:
        print(f"Error processing file change: {e}")
        # Continue monitoring despite errors

# The monitoring thread will continue running even if callback fails
monitor_thread = session.file_system.watch_directory(
    path="/tmp/my_directory",
    callback=on_file_change,
    interval=1.0
)
```

## Best Practices

### 1. Choose Appropriate Polling Intervals

- **Fast monitoring** (0.1-0.5 seconds): For critical applications requiring immediate response
- **Normal monitoring** (1-2 seconds): For most use cases
- **Slow monitoring** (5+ seconds): For less critical monitoring to reduce resource usage

### 2. Handle Callback Exceptions

Always wrap your callback logic in try-catch blocks to prevent monitoring from stopping due to errors.

### 3. Clean Up Resources

Always stop monitoring and clean up sessions when done:

```python
try:
    # Your monitoring code
    pass
finally:
    monitor_thread.stop_event.set()
    monitor_thread.join(timeout=5)
    agentbay.delete(session)
```

### 4. Use Appropriate Session Images

Use `code_latest` image ID for the most up-to-date file system monitoring capabilities.

## Common Use Cases

### 1. Development File Watcher

Monitor source code changes during development:

```python
def on_code_change(events):
    for event in events:
        if event.path.endswith(('.py', '.js', '.ts', '.go')):
            print(f"Source file {event.event_type}: {event.path}")
            # Trigger build, test, or reload
```

### 2. Log File Monitor

Monitor log files for new entries:

```python
def on_log_change(events):
    for event in events:
        if event.event_type == "modify" and event.path.endswith('.log'):
            # Read new log entries
            content = session.file_system.read_file(event.path)
            process_log_content(content.content)
```

### 3. Configuration File Watcher

Monitor configuration files for changes:

```python
def on_config_change(events):
    for event in events:
        if event.path.endswith(('.json', '.yaml', '.toml', '.ini')):
            print(f"Configuration {event.event_type}: {event.path}")
            # Reload configuration
            reload_config(event.path)
```

## Troubleshooting

### Issue: No Events Detected

**Possible causes:**
1. Directory doesn't exist
2. No file changes occurring
3. Polling interval too long

**Solutions:**
1. Verify directory exists: `session.file_system.get_file_info(path)`
2. Create test files to verify monitoring works
3. Reduce polling interval

### Issue: Too Many Events

**Possible causes:**
1. Polling interval too short
2. Many files changing simultaneously

**Solutions:**
1. Increase polling interval
2. Filter events in callback
3. Batch process events

### Issue: Monitoring Stops Unexpectedly

**Possible causes:**
1. Callback function throwing exceptions
2. Session expired
3. Network issues

**Solutions:**
1. Add error handling in callback
2. Monitor session health
3. Implement retry logic

## Performance Considerations

- **Polling frequency**: Lower intervals provide faster response but use more resources
- **Directory size**: Large directories may take longer to scan
- **Network latency**: Remote sessions may have higher latency for change detection
- **Event volume**: High-frequency changes may impact performance

## Limitations

1. **Polling-based**: Uses polling rather than native file system events
2. **Network dependent**: Requires active session connection
3. **Resource usage**: Continuous polling consumes computational resources
4. **Latency**: Change detection limited by polling interval

For the most up-to-date information and additional examples, see the [API Reference](../api-reference.md). 