# Wuying AgentBay SDK - Python Examples

This directory contains examples demonstrating how to use the Wuying AgentBay SDK in Python.

## Examples Overview

- **basic_usage/**: Demonstrates the basic usage of the SDK, including creating a session, executing commands, reading files, and cleaning up.
- **session_creation/**: Shows how to create, list, and manage multiple sessions.
- **session_params/**: Demonstrates how to use session parameters and labels.
- **context_management/**: Shows how to create, list, update, and delete contexts, and how to use them with sessions.
- **application_window/**: Demonstrates application and window management features.

## Running Examples

To run any example, use the Python interpreter:

```bash
# For example, to run the basic usage example:
python basic_usage.py
```

## API Key

Most examples require an API key for authentication. You can provide it in two ways:

1. Set the `AGENTBAY_API_KEY` environment variable:
   ```bash
   export AGENTBAY_API_KEY=your_api_key_here
   ```

2. Replace the placeholder in the example code with your actual API key (not recommended for production use).

## Prerequisites

- Python 3.10 or later
- Wuying AgentBay SDK installed:
  ```bash
  pip install wuying-agentbay-sdk
  ```

## Example Descriptions

### Basic Usage

The basic usage example demonstrates the fundamental operations of the SDK, including:
- Initializing the AgentBay client
- Creating a session
- Executing commands
- Reading files
- Using shell commands
- Listing and deleting sessions

### Session Creation

The session creation example demonstrates how to create and manage multiple sessions, including:
- Creating sessions with default parameters
- Listing all available sessions
- Creating multiple sessions
- Deleting sessions
- Verifying session deletion

### Session Parameters

The session parameters example demonstrates how to use custom parameters and labels with sessions, including:
- Creating sessions with custom labels
- Listing sessions by labels
- Deleting sessions

### Context Management

The context management example demonstrates how to work with contexts, including:
- Listing all contexts
- Getting a context (creating if it doesn't exist)
- Creating a session with a context
- Updating a context
- Deleting a context

### Application and Window Management

The application and window management example demonstrates how to interact with applications and windows, including:
- Getting installed applications
- Listing visible applications
- Listing root windows
- Getting the active window
- Window operations (activate, maximize, minimize, restore, resize)
- Focus mode
