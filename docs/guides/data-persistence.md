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

```python
from agentbay import AgentBay

# Initialize AgentBay client (requires valid API key)
agent_bay = AgentBay(api_key="your-api-key")

# Get or create context
context_result = agent_bay.context.get("my-project", create=True)
if context_result.success:
    context = context_result.context
    print(f"Context ID: {context.id}")
    print(f"Context Name: {context.name}")
    print(f"Created At: {context.created_at}")
else:
    print(f"Context operation failed: {context_result.error_message}")

# Get existing context only
existing_context_result = agent_bay.context.get("my-project", create=False)
if not existing_context_result.success:
    print("Context does not exist")
else:
    context = existing_context_result.context
    print(f"Found context: {context.name}")
```


### Listing and Managing Contexts

```python
# List all contexts
contexts_result = agent_bay.context.list()
if contexts_result.success:
    for context in contexts_result.contexts:
        print(f"Context: {context.name} (ID: {context.id})")
else:
    print(f"Failed to list contexts: {contexts_result.error_message}")

# Delete context
context_to_delete = agent_bay.context.get("my-project", create=False).context
if context_to_delete:
    delete_result = agent_bay.context.delete(context_to_delete)
    if delete_result.success:
        print("Context deleted successfully")
    else:
        print(f"Failed to delete context: {delete_result.error_message}")
```

### Context with Sessions

```python
from agentbay import ContextSync, CreateSessionParams

# Create context
context_result = agent_bay.context.get("my-project", create=True)
if context_result.success:
    context = context_result.context

    # Create context sync (policy is optional, will use default if not specified)
    context_sync = ContextSync.new(
        context_id=context.id,
        path="/mnt/data"  # Mount path in session
    )

    # Create session with context
    params = CreateSessionParams(context_syncs=[context_sync])
    session_result = agent_bay.create(params)
    if session_result.success:
        session = session_result.session

        # Now files written to /mnt/data will be persisted
        session.file_system.write("/mnt/data/config.json", '{"setting": "value"}')
        session.file_system.write("/mnt/data/data.txt", "Important data")

        print("Data written to persistent storage")
    else:
        print(f"Failed to create session: {session_result.error_message}")
else:
    print(f"Failed to create context: {context_result.error_message}")
```

## 🔄 Data Synchronization Strategies

### Sync Policies

AgentBay provides different synchronization policies:

```python
from agentbay import SyncPolicy

# Auto sync - automatically sync data at regular intervals
auto_policy = SyncPolicy.default()
# Note: The actual interval is controlled by the service, not configurable in the SDK

# Manual sync - sync only when explicitly requested
manual_policy = SyncPolicy(
    upload_policy=UploadPolicy(auto_upload=False),
    download_policy=DownloadPolicy(auto_download=False)
)

# On-demand sync - sync when session starts/ends
ondemand_policy = SyncPolicy.default()  # This is the default behavior

# Custom policy with specific settings
custom_policy = SyncPolicy(
    upload_policy=UploadPolicy(
        auto_upload=True,
        period=60  # Upload every 60 minutes
    ),
    download_policy=DownloadPolicy(auto_download=True)
)
```

### Manual Synchronization

```python
# Create session with manual sync policy
manual_policy = SyncPolicy(
    upload_policy=UploadPolicy(auto_upload=False),
    download_policy=DownloadPolicy(auto_download=False)
)

context_sync = ContextSync.new(context.id, "/mnt/data", manual_policy)
session_result = agent_bay.create(CreateSessionParams(context_syncs=[context_sync]))

if session_result.success:
    session = session_result.session

    # Write some data
    session.file_system.write("/mnt/data/temp.txt", "Temporary data")

    # Manually trigger sync to save data
    sync_result = session.context.sync()
    if sync_result.success:
        print("Data synchronized successfully")
    else:
        print(f"Sync failed: {sync_result.error_message}")

    # Data is now persisted even if session ends
else:
    print(f"Failed to create session: {session_result.error_message}")
```

### Bidirectional Sync

```python
# Download latest data from context
download_result = session.context.sync(mode="download")
if download_result.success:
    print("Latest data downloaded from context")
else:
    print(f"Download failed: {download_result.error_message}")

# Upload local changes to context
upload_result = session.context.sync(mode="upload")
if upload_result.success:
    print("Local changes uploaded to context")
else:
    print(f"Upload failed: {upload_result.error_message}")
```

## 🔗 Cross-Session Data Sharing

### Sharing Data Between Sessions

```python
# Session 1: Write data
context_result = agent_bay.context.get("shared-project", create=True)
if context_result.success:
    context = context_result.context
    context_sync = ContextSync.new(context.id, "/mnt/shared", SyncPolicy.default())

    session1_result = agent_bay.create(CreateSessionParams(context_syncs=[context_sync]))
    if session1_result.success:
        session1 = session1_result.session
        session1.file_system.write("/mnt/shared/shared_data.json", '{"message": "Hello from session 1"}')

        # Ensure data is synced
        sync_result = session1.context.sync()
        if sync_result.success:
            print("Session 1: Data written and synced")
        else:
            print(f"Session 1: Sync failed: {sync_result.error_message}")
    else:
        print(f"Session 1: Failed to create session: {session1_result.error_message}")
else:
    print(f"Failed to create context: {context_result.error_message}")

# Session 2: Read data
session2_result = agent_bay.create(CreateSessionParams(context_syncs=[context_sync]))
if session2_result.success:
    session2 = session2_result.session

    # Download latest data
    download_result = session2.context.sync(mode="download")
    if download_result.success:
        # Read shared data
        data_result = session2.file_system.read("/mnt/shared/shared_data.json")
        if not data_result.is_error:
            print(f"Session 2: Read data: {data_result.data}")
        else:
            print(f"Session 2: Failed to read data: {data_result.error}")
    else:
        print(f"Session 2: Download failed: {download_result.error_message}")
else:
    print(f"Session 2: Failed to create session: {session2_result.error_message}")
```

### Multi-User Collaboration

```python
# User A creates and shares context
user_a_context_result = agent_bay.context.get("team-project", create=True)
if user_a_context_result.success:
    user_a_context = user_a_context_result.context

    # Configure context for collaboration
    collaboration_policy = SyncPolicy.default()  # Auto sync by default
    
    context_sync = ContextSync.new(user_a_context.id, "/mnt/team", collaboration_policy)

    # User A session
    session_a_result = agent_bay.create(CreateSessionParams(context_syncs=[context_sync]))
    if session_a_result.success:
        session_a = session_a_result.session
        session_a.file_system.write("/mnt/team/task_list.txt", "Task 1: Setup environment\nTask 2: Write code")

        # User B joins the same context (using same context ID)
        session_b_result = agent_bay.create(CreateSessionParams(context_syncs=[context_sync]))
        if session_b_result.success:
            session_b = session_b_result.session

            # User B can see User A's work (after sync)
            download_result = session_b.context.sync(mode="download")
            if download_result.success:
                task_list_result = session_b.file_system.read("/mnt/team/task_list.txt")
                if not task_list_result.is_error:
                    print(f"User B sees: {task_list_result.data}")

                    # User B adds to the work
                    session_b.file_system.write("/mnt/team/progress.txt", "Task 1: Completed\nTask 2: In progress")
                else:
                    print(f"User B: Failed to read task list: {task_list_result.error}")
            else:
                print(f"User B: Download failed: {download_result.error_message}")
        else:
            print(f"User B: Failed to create session: {session_b_result.error_message}")
    else:
        print(f"User A: Failed to create session: {session_a_result.error_message}")
else:
    print(f"Failed to create context: {user_a_context_result.error_message}")
```

## 📚 Version Control and Backup

### Context Snapshots

```python
# Note: Snapshot functionality is not currently exposed in the SDK
# This is a planned feature for future releases

# Example of how snapshot functionality might work in the future:
# Create snapshot of current context state
# snapshot_result = agent_bay.context.create_snapshot(context.id, "v1.0-release")
# if snapshot_result.success:
#     snapshot = snapshot_result.snapshot
#     print(f"Snapshot created: {snapshot.name} at {snapshot.created_at}")

# List all snapshots
# snapshots_result = agent_bay.context.list_snapshots(context.id)
# if snapshots_result.success:
#     for snapshot in snapshots_result.snapshots:
#         print(f"Snapshot: {snapshot.name} ({snapshot.created_at})")

# Restore from snapshot
# restore_result = agent_bay.context.restore_snapshot(context.id, snapshot.id)
# if restore_result.success:
#     print("Context restored from snapshot")
```

### Backup Strategies

```python
import datetime

class ContextBackupManager:
    def __init__(self, agent_bay):
        self.agent_bay = agent_bay
    
    def create_daily_backup(self, context_name):
        """Create daily backup by creating a new context with timestamp"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
        backup_context_name = f"{context_name}-backup-{timestamp}"
        
        # Get the original context
        context_result = self.agent_bay.context.get(context_name, create=False)
        if not context_result.success:
            return False, "Original context not found"
            
        original_context = context_result.context
        
        # Create backup context
        backup_result = self.agent_bay.context.get(backup_context_name, create=True)
        if not backup_result.success:
            return False, f"Failed to create backup context: {backup_result.error_message}"
            
        backup_context = backup_result.context
        return True, f"Backup created: {backup_context.name}"
    
    def list_backups(self, context_name):
        """List all backup contexts for a given context"""
        contexts_result = self.agent_bay.context.list()
        if not contexts_result.success:
            return False, f"Failed to list contexts: {contexts_result.error_message}", []
            
        backups = []
        for context in contexts_result.contexts:
            if context.name.startswith(f"{context_name}-backup-"):
                backups.append(context)
                
        return True, "Backups listed successfully", backups

# Usage
backup_manager = ContextBackupManager(agent_bay)
success, message = backup_manager.create_daily_backup("my-project")
if success:
    print(message)
else:
    print(f"Backup failed: {message}")

success, message, backups = backup_manager.list_backups("my-project")
if success:
    print(message)
    for backup in backups:
        print(f"Backup: {backup.name} (ID: {backup.id})")
else:
    print(f"Failed to list backups: {message}")
```

## ⚡ Performance Optimization

### Efficient Data Transfer

```python
# Use compression and selective sync for large data transfers
from agentbay import SyncPolicy, BWList, WhiteList

# Create a policy that only syncs specific file types
selective_sync_policy = SyncPolicy(
    upload_policy=UploadPolicy(auto_upload=True),
    download_policy=DownloadPolicy(auto_download=True),
    bw_list=BWList(
        white_lists=[
            WhiteList(
                path="*.json",  # Only sync JSON files
                exclude_paths=["*.tmp", "*.log"]  # Exclude temporary files
            ),
            WhiteList(
                path="*.txt",  # Also sync text files
                exclude_paths=[]
            )
        ]
    )
)

# Create context sync with selective sync policy
selective_sync = ContextSync.new(
    context.id, 
    "/mnt/data",
    selective_sync_policy
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
    
    if result.success:
        print(f"Sync completed in {duration:.2f} seconds")
        # Note: Detailed statistics are not currently available in the SDK
    else:
        print(f"Sync failed after {duration:.2f} seconds: {result.error_message}")

# Usage
# monitor_sync_performance(session)
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
    result = agent_bay.context.get(context_name, create=True)
    if result.success:
        print(f"Created context: {result.context.name}")
    else:
        print(f"Failed to create context {context_name}: {result.error_message}")
```

### 2. Data Structure Best Practices

```python
import datetime

# Organize data in logical directories
session.file_system.write("/mnt/data/config/app.json", app_config)
session.file_system.write("/mnt/data/logs/app.log", log_data)
session.file_system.write("/mnt/data/cache/temp.dat", cache_data)
session.file_system.write("/mnt/data/output/results.csv", results)

# Use consistent file naming conventions
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
session.file_system.write(f"/mnt/data/backups/backup_{timestamp}.json", backup_data)
```

### 3. Error Handling for Persistence

```python
def safe_persistent_write(session, path, data):
    """Safely write data with persistence"""
    try:
        # Write data
        write_result = session.file_system.write(path, data)
        if write_result.is_error:
            print(f"Write failed: {write_result.error}")
            return False
        
        # Sync to ensure persistence
        sync_result = session.context.sync()
        if not sync_result.success:
            print(f"Sync failed: {sync_result.error_message}")
            return False
        
        print(f"Data successfully written and persisted: {path}")
        return True
        
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

# Usage
# success = safe_persistent_write(session, "/mnt/data/important.json", important_data)
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
        if not result.success:
            raise Exception(f"Failed to get context: {result.error_message}")
        
        self.context = result.context
        return self.context
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # Optionally clean up or backup context
        if exc_type is not None:
            print(f"Error occurred, creating emergency backup")
            # Note: Snapshot functionality not currently available
            # Would implement alternative backup strategy here

# Usage
# with ContextManager(agent_bay, "my-project") as context:
#     # Work with context
#     context_sync = ContextSync.new(context.id, "/mnt/data", SyncPolicy.default())
#     session_result = agent_bay.create(CreateSessionParams(context_syncs=[context_sync]))
#     
#     if session_result.success:
#         session = session_result.session
#         
#         # Do work...
#         session.file_system.write("/mnt/data/work.txt", "Important work")
#         session.context.sync()
#     else:
#         print(f"Failed to create session: {session_result.error_message}")
```

This comprehensive guide covers all aspects of data persistence in AgentBay. Use these patterns to build robust, data-driven applications that maintain state across sessions and enable collaboration!