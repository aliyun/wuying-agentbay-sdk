# Context Synchronization Example

This example demonstrates how to use the context synchronization functionality in AgentBay.

## What This Example Shows

- Creating a basic context synchronization configuration with default settings
- Creating a custom context synchronization configuration with:
  - Custom upload policy (periodic upload with custom interval)
  - Custom download policy (synchronous download)
  - Custom delete policy (disable local file deletion sync)
  - Multiple white lists with exclude paths
  - Custom sync paths
- Updating an existing context synchronization configuration

## Running the Example

```bash
# Make sure you have the AgentBay SDK installed
python main.py
```

## Key Concepts

### Context Synchronization

Context synchronization allows you to configure how files are synchronized between the local environment and the cloud context. It provides control over:

- When and how files are uploaded
- When and how files are downloaded
- Whether local file deletions are synchronized
- Which paths are included or excluded from synchronization

### Policies

- **Upload Policy**: Controls how files are uploaded to the cloud context
  - Auto upload setting
  - Upload strategy (on resource release, after file close, or periodic)
  - Upload period (for periodic uploads)

- **Download Policy**: Controls how files are downloaded from the cloud context
  - Auto download setting
  - Download strategy (synchronous or asynchronous)

- **Delete Policy**: Controls deletion synchronization behavior
  - Whether local file deletions are synchronized to the cloud context

- **White Lists**: Specify which paths to include in synchronization
  - Path to include
  - Paths to exclude within the included path

## Code Structure

The example is structured into three main functions:

1. `basic_context_sync()`: Shows how to create a context sync configuration with default settings
2. `custom_context_sync()`: Demonstrates creating a fully customized configuration using method chaining
3. `update_existing_policy()`: Shows how to update an existing configuration

Each function prints details of the configuration to help understand the structure and options. 