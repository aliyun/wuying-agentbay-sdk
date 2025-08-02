# Python API Reference

This section provides detailed API reference documentation for the Python version of the AgentBay SDK.

## Core Classes

- [AgentBay](agentbay.md) - The main entry point of the SDK, used to create sessions and manage global configuration
- [Session](session.md) - Represents a session in the AgentBay cloud environment, providing interfaces to access various features

## Functional Components

- [Agent](agent.md) - Provides AI-powered capabilities for executing tasks using natural language descriptions
- [FileSystem](filesystem.md) - Provides file system operations such as uploading, downloading, and managing files
- [Command](command.md) - Provides functionality to execute shell commands in a session
- [Code](code.md) - Handles code execution operations in Python and JavaScript languages
- [Application](application.md) - Manages application operations and state
- [Window](window.md) - Manages window and view operations
- [UI](ui.md) - Provides user interface interaction functionality
- [OSS](oss.md) - Provides Object Storage Service (OSS) integration

## Context Management

- [Context](context.md) - Manages context data in a session
- [ContextManager](context-manager.md) - Provides context management functionality

## Examples

Check out the [Python Examples](../../examples/python/) for code samples and use cases.

## Installation

Install the Python version of the AgentBay SDK via pip:

```bash
pip install wuying-agentbay-sdk
```

## Configuration

The AgentBay SDK supports multiple ways to configure the client. The SDK uses the following precedence order for configuration (highest to lowest):

1. Explicitly passed configuration in code (using the `cfg` parameter)
2. Environment variables
3. .env file
4. Default configuration

### Using Config Object

```python
from agentbay import AgentBay, Config

# Initialize with custom configuration
config = Config(
    region_id="cn-shanghai",
    endpoint="wuyingai.cn-shanghai.aliyuncs.com",
    timeout_ms=60000
)
agent_bay = AgentBay(api_key="your_api_key", cfg=config)
```

### Using Environment Variables

Set the following environment variables:

```bash
export AGENTBAY_API_KEY="your_api_key"
export AGENTBAY_REGION_ID="cn-shanghai"
export AGENTBAY_ENDPOINT="wuyingai.cn-shanghai.aliyuncs.com"
export AGENTBAY_TIMEOUT_MS=60000
```

Then initialize without explicit config:

```python
from agentbay import AgentBay

agent_bay = AgentBay(api_key="your_api_key")
```

### Using .env File

Create a `.env` file in your project directory:

```env
AGENTBAY_API_KEY=your_api_key
AGENTBAY_REGION_ID=cn-shanghai
AGENTBAY_ENDPOINT=wuyingai.cn-shanghai.aliyuncs.com
AGENTBAY_TIMEOUT_MS=60000
```

Then initialize without explicit config:

```python
from agentbay import AgentBay

agent_bay = AgentBay()  # Will automatically load from environment/.env
```

## Quick Start

```python
from agentbay import AgentBay

# Initialize the SDK (will use default configuration or environment variables)
agent_bay = AgentBay(api_key="your_api_key")

# Create a session
result = agent_bay.create()
if result.success:
    session = result.session
    print(f"Session created with ID: {session.session_id}")
    
    # Use the file system
    fs = session.file_system
    
    # Execute commands
    cmd = session.command
    
    # Delete the session when done
    delete_result = session.delete()
    if delete_result.success:
        print("Session deleted successfully")
``` 