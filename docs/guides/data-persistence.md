# Complete Data Persistence Guide

This guide integrates AgentBay SDK's data persistence features, including context concepts, data synchronization strategies, cross-session data sharing, version control, and performance optimization.

## 📋 Table of Contents

- [Core Concepts](#core-concepts)
- [Context Management](#context-management)
- [Data Synchronization Strategies](#data-synchronization-strategies)
- [Cross-Session Data Sharing](#cross-session-data-sharing)
- [Version Control and Backup](#version-control-and-backup)
- [Performance Optimization](#performance-optimization)
- [Best Practices](#best-practices)

## 🎯 Core Concepts

### What is Data Persistence?

In AgentBay, by default, all data is lost when a session ends. Data persistence solves this problem through the **Context** system, allowing you to:

- Save and share data across multiple sessions
- Implement version control and backup for data
- Build continuous workflows

### Context vs Session

| Feature | Session | Context |
|---------|---------|---------|
| Lifecycle | Temporary, destroyed when session ends | Persistent, destroyed only when manually deleted |
| Data Storage | Not saved | Permanently saved |
| Sharing | Independent, not shared | Can be shared across multiple sessions |
| Use Case | Execute temporary tasks | Store project data, configurations, etc. |

## 📦 Context Management

### Creating and Getting Contexts

<details>
<summary><strong>Python</strong></summary>

```python
from agentbay import AgentBay

agent_bay = AgentBay()

# Get or create context
context_result = agent_bay.context.get("my-project", create=True)
if not context_result.is_error:
    context = context_result.context
    print(f"Context ID: {context.id}")
    print(f"Context Name: {context.name}")
    print(f"Created At: {context.created_at}")
else:
    print(f"Context operation failed: {context_result.error}")

# Get existing context only
existing_context = agent_bay.context.get("my-project", create=False)
if existing_context.is_error:
    print("Context does not exist")
```
</details>

<details>
<summary><strong>TypeScript</strong></summary>

```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

const agentBay = new AgentBay();

// Get or create context
const contextResult = await agentBay.context.get("my-project", { create: true });
if (!contextResult.isError) {
    const context = contextResult.context;
    console.log(`Context ID: ${context.id}`);
    console.log(`Context Name: ${context.name}`);
    console.log(`Created At: ${context.createdAt}`);
} else {
    console.log(`Context operation failed: ${contextResult.error}`);
}

// Get existing context only
const existingContext = await agentBay.context.get("my-project", { create: false });
if (existingContext.isError) {
    console.log("Context does not exist");
}
```
</details>

<details>
<summary><strong>Golang</strong></summary>

```go
import "github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"

client, _ := agentbay.NewAgentBay("", nil)

// Get or create context
contextResult, err := client.Context.Get("my-project", true)
if err == nil && !contextResult.IsError {
    context := contextResult.Context
    fmt.Printf("Context ID: %s\n", context.ID)
    fmt.Printf("Context Name: %s\n", context.Name)
    fmt.Printf("Created At: %s\n", context.CreatedAt)
} else {
    fmt.Printf("Context operation failed: %v\n", err)
}

// Get existing context only
existingContext, err := client.Context.Get("my-project", false)
if err != nil || existingContext.IsError {
    fmt.Println("Context does not exist")
}
```
</details>

### Listing and Managing Contexts

```python
# List all contexts
contexts_result = agent_bay.context.list()
if not contexts_result.is_error:
    for context in contexts_result.contexts:
        print(f"Context: {context.name} (ID: {context.id})")

# Delete context
delete_result = agent_bay.context.delete("my-project")
if not delete_result.is_error:
    print("Context deleted successfully")
```

### Context with Sessions

```python
from agentbay import ContextSync, SyncPolicy, CreateSessionParams

# Create context
context = agent_bay.context.get("my-project", create=True).context

# Create context sync (policy is optional, will use default if not specified)
context_sync = ContextSync.new(
    context_id=context.id,
    path="/tmp/data"  # Mount path in session
)

# Create session with context
params = CreateSessionParams(context_syncs=[context_sync])
session = agent_bay.create(params).session

# Now files written to /mnt/data will be persisted
session.filesystem.write("/mnt/data/config.json", '{"setting": "value"}')
session.filesystem.write("/mnt/data/data.txt", "Important data")

print("Data written to persistent storage")
```

## 🔄 Data Synchronization Strategies

### Sync Policies

AgentBay provides different synchronization policies:

```python
from agentbay import SyncPolicy

# Auto sync - automatically sync data at regular intervals
auto_policy = SyncPolicy.auto(interval_seconds=300)  # Sync every 5 minutes

# Manual sync - sync only when explicitly requested
manual_policy = SyncPolicy.manual()

# On-demand sync - sync when session starts/ends
ondemand_policy = SyncPolicy.on_demand()

# Default policy (recommended for most cases)
default_policy = SyncPolicy.default()
```

### Manual Synchronization

```python
# Create session with manual sync policy
manual_policy = SyncPolicy.manual()
context_sync = ContextSync.new(context.id, "/mnt/data", manual_policy)
session = agent_bay.create(CreateSessionParams(context_syncs=[context_sync])).session

# Write some data
session.filesystem.write("/mnt/data/temp.txt", "Temporary data")

# Manually trigger sync to save data
sync_result = session.context.sync()
if not sync_result.is_error:
    print("Data synchronized successfully")

# Data is now persisted even if session ends
```

### Bidirectional Sync

```python
# Download latest data from context
download_result = session.context.download()
if not download_result.is_error:
    print("Latest data downloaded from context")

# Upload local changes to context
upload_result = session.context.upload()
if not upload_result.is_error:
    print("Local changes uploaded to context")
```

## 🔗 Cross-Session Data Sharing

### Sharing Data Between Sessions

```python
# Session 1: Write data
context = agent_bay.context.get("shared-project", create=True).context
context_sync = ContextSync.new(context.id, "/mnt/shared", SyncPolicy.default())

session1 = agent_bay.create(CreateSessionParams(context_syncs=[context_sync])).session
session1.filesystem.write("/mnt/shared/shared_data.json", '{"message": "Hello from session 1"}')

# Ensure data is synced
session1.context.sync()
print("Session 1: Data written and synced")

# Session 2: Read data
session2 = agent_bay.create(CreateSessionParams(context_syncs=[context_sync])).session

# Download latest data
session2.context.download()

# Read shared data
data = session2.filesystem.read("/mnt/shared/shared_data.json")
if not data.is_error:
    print(f"Session 2: Read data: {data.data}")
```

### Multi-User Collaboration

```python
# User A creates and shares context
user_a_context = agent_bay.context.get("team-project", create=True).context

# Configure context for collaboration
collaboration_policy = SyncPolicy.auto(interval_seconds=60)  # Sync every minute
context_sync = ContextSync.new(user_a_context.id, "/mnt/team", collaboration_policy)

# User A session
session_a = agent_bay.create(CreateSessionParams(context_syncs=[context_sync])).session
session_a.filesystem.write("/mnt/team/task_list.txt", "Task 1: Setup environment\nTask 2: Write code")

# User B joins the same context (using same context ID)
session_b = agent_bay.create(CreateSessionParams(context_syncs=[context_sync])).session

# User B can see User A's work
task_list = session_b.filesystem.read("/mnt/team/task_list.txt")
print(f"User B sees: {task_list.data}")

# User B adds to the work
session_b.filesystem.write("/mnt/team/progress.txt", "Task 1: Completed\nTask 2: In progress")
```

## 📚 Version Control and Backup

### Context Snapshots

```python
# Create snapshot of current context state
snapshot_result = agent_bay.context.create_snapshot(context.id, "v1.0-release")
if not snapshot_result.is_error:
    snapshot = snapshot_result.snapshot
    print(f"Snapshot created: {snapshot.name} at {snapshot.created_at}")

# List all snapshots
snapshots_result = agent_bay.context.list_snapshots(context.id)
if not snapshots_result.is_error:
    for snapshot in snapshots_result.snapshots:
        print(f"Snapshot: {snapshot.name} ({snapshot.created_at})")

# Restore from snapshot
restore_result = agent_bay.context.restore_snapshot(context.id, snapshot.id)
if not restore_result.is_error:
    print("Context restored from snapshot")
```

### Backup Strategies

```python
import datetime

class ContextBackupManager:
    def __init__(self, agent_bay, context_id):
        self.agent_bay = agent_bay
        self.context_id = context_id
    
    def create_daily_backup(self):
        """Create daily backup snapshot"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
        snapshot_name = f"daily-backup-{timestamp}"
        
        result = self.agent_bay.context.create_snapshot(self.context_id, snapshot_name)
        return not result.is_error
    
    def cleanup_old_backups(self, keep_days=30):
        """Remove backups older than specified days"""
        snapshots = self.agent_bay.context.list_snapshots(self.context_id)
        if snapshots.is_error:
            return False
        
        cutoff_date = datetime.datetime.now() - datetime.timedelta(days=keep_days)
        
        for snapshot in snapshots.snapshots:
            if snapshot.created_at < cutoff_date:
                self.agent_bay.context.delete_snapshot(self.context_id, snapshot.id)
                print(f"Deleted old backup: {snapshot.name}")
        
        return True

# Usage
backup_manager = ContextBackupManager(agent_bay, context.id)
backup_manager.create_daily_backup()
backup_manager.cleanup_old_backups(keep_days=7)
```

## ⚡ Performance Optimization

### Efficient Data Transfer

```python
# Use compression for large data transfers
large_data_policy = SyncPolicy.auto(
    interval_seconds=600,  # Less frequent sync for large data
    compression=True,      # Enable compression
    batch_size=1000       # Batch multiple files
)

# Selective sync - only sync specific directories
selective_sync = ContextSync.new(
    context.id, 
    "/mnt/data",
    large_data_policy,
    include_patterns=["*.json", "*.txt"],  # Only sync these file types
    exclude_patterns=["*.tmp", "*.log"]    # Exclude temporary files
)
```

### Monitoring Sync Performance

```python
import time

def monitor_sync_performance(session):
    """Monitor context sync performance"""
    start_time = time.time()
    
    # Perform sync
    result = session.context.sync()
    
    end_time = time.time()
    duration = end_time - start_time
    
    if not result.is_error:
        print(f"Sync completed in {duration:.2f} seconds")
        
        # Get sync statistics if available
        if hasattr(result, 'stats'):
            stats = result.stats
            print(f"Files synced: {stats.files_count}")
            print(f"Data transferred: {stats.bytes_transferred} bytes")
            print(f"Sync speed: {stats.bytes_transferred / duration:.2f} bytes/sec")
    else:
        print(f"Sync failed after {duration:.2f} seconds: {result.error}")

# Usage
monitor_sync_performance(session)
```

## 💡 Best Practices

### 1. Context Organization

```python
# Use hierarchical naming for contexts
contexts = [
    "project-alpha-dev",
    "project-alpha-staging", 
    "project-alpha-prod",
    "project-beta-dev",
    "project-beta-prod"
]

# Create contexts with descriptive names
for context_name in contexts:
    agent_bay.context.get(context_name, create=True)
```

### 2. Data Structure Best Practices

```python
# Organize data in logical directories
session.filesystem.write("/mnt/data/config/app.json", app_config)
session.filesystem.write("/mnt/data/logs/app.log", log_data)
session.filesystem.write("/mnt/data/cache/temp.dat", cache_data)
session.filesystem.write("/mnt/data/output/results.csv", results)

# Use consistent file naming conventions
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
session.filesystem.write(f"/mnt/data/backups/backup_{timestamp}.json", backup_data)
```

### 3. Error Handling for Persistence

```python
def safe_persistent_write(session, path, data):
    """Safely write data with persistence"""
    try:
        # Write data
        write_result = session.filesystem.write(path, data)
        if write_result.is_error:
            print(f"Write failed: {write_result.error}")
            return False
        
        # Sync to ensure persistence
        sync_result = session.context.sync()
        if sync_result.is_error:
            print(f"Sync failed: {sync_result.error}")
            return False
        
        print(f"Data successfully written and persisted: {path}")
        return True
        
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

# Usage
success = safe_persistent_write(session, "/mnt/data/important.json", important_data)
```

### 4. Context Lifecycle Management

```python
class ContextManager:
    def __init__(self, agent_bay, context_name):
        self.agent_bay = agent_bay
        self.context_name = context_name
        self.context = None
    
    def __enter__(self):
        # Get or create context
        result = self.agent_bay.context.get(self.context_name, create=True)
        if result.is_error:
            raise Exception(f"Failed to get context: {result.error}")
        
        self.context = result.context
        return self.context
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # Optionally clean up or backup context
        if exc_type is not None:
            print(f"Error occurred, creating emergency backup")
            self.agent_bay.context.create_snapshot(
                self.context.id, 
                f"emergency-backup-{datetime.datetime.now().isoformat()}"
            )

# Usage
with ContextManager(agent_bay, "my-project") as context:
    # Work with context
    context_sync = ContextSync.new(context.id, "/mnt/data", SyncPolicy.default())
    session = agent_bay.create(CreateSessionParams(context_syncs=[context_sync])).session
    
    # Do work...
    session.filesystem.write("/mnt/data/work.txt", "Important work")
    session.context.sync()
```

This comprehensive guide covers all aspects of data persistence in AgentBay. Use these patterns to build robust, data-driven applications that maintain state across sessions and enable collaboration! 