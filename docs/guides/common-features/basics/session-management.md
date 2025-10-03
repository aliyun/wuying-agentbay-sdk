# Session Management Documentation

This document provides comprehensive guidance on using the session management capabilities of the AgentBay SDK across all supported languages.

## Overview

Sessions are the fundamental unit of interaction with the AgentBay cloud environment. Each session represents an isolated cloud environment where you can execute commands, manipulate files, run applications, and perform automation tasks.

The session management system provides:
1. **Session Creation**: Create isolated cloud environments with customizable image types and parameters
2. **Session Information**: Access session details including direct browser URLs and connection credentials
3. **Label Management**: Organize and categorize sessions using descriptive labels
4. **Session Recovery**: Restore session objects using session IDs for continued operations
5. **Session Deletion**: Clean up sessions to free cloud resources

## Getting Started

### Prerequisites

Before running the example programs in this guide, please ensure you have completed the following setup:

**Required Setup (2 minutes):**
1. **SDK Installation & API Key Configuration**: Follow the [Installation and API Key Setup Guide](../../../quickstart/installation.md) to install the AgentBay SDK and configure your API key
2. **SDK Configuration**: Review the [SDK Configuration Guide](../configuration/sdk-configuration.md) for detailed configuration options including environment variables and region settings
3. **Core Concepts**: Review [Core Concepts Guide](../../../quickstart/basic-concepts.md) to understand AgentBay fundamentals including sessions, images, and data persistence

**Quick Verification:**
After setup, verify everything works with this simple test:
```python
import os
from agentbay import AgentBay

api_key = os.getenv("AGENTBAY_API_KEY")
agent_bay = AgentBay(api_key=api_key)
result = agent_bay.create()
if result.success:
    print("✅ Setup successful - ready to use session management!")
    agent_bay.delete(result.session)
else:
    print(f"❌ Setup issue: {result.error_message}")
```

### Creating a Session

Creating a session is the first step in using the AgentBay SDK:

```python
from agentbay import AgentBay

# Initialize the SDK
agent_bay = AgentBay(api_key=api_key)

# Create a session with default parameters
session_result = agent_bay.create()
if session_result.success:
    session = session_result.session
    print(f"Session created with ID: {session.session_id}")
```

## Creating Sessions with Custom Parameters

You can customize sessions by specifying parameters such as [image ID](../../../quickstart/basic-concepts.md#-image-types---four-main-environments) and [labels](#session-label-management):

```python
from agentbay import AgentBay
from agentbay.session_params import CreateSessionParams

# Initialize the SDK
agent_bay = AgentBay(api_key="your_api_key")

# Create a session with custom parameters
params = CreateSessionParams(
    image_id="linux_latest",
    labels={"project": "demo", "environment": "testing"}
)
session_result = agent_bay.create(params)
session = session_result.session

if session_result.success:
    session = session_result.session
    print(f"Session created with ID: {session.session_id}")
```



## Session Label Management

Labels help organize and categorize sessions for easier management:

### Setting Session Labels

```python
from agentbay import AgentBay

# Initialize the SDK and create a session
agent_bay = AgentBay(api_key=api_key)
session_result = agent_bay.create()
session = session_result.session

# Set labels
labels = {"project": "demo", "environment": "testing"}
result = session.set_labels(labels)

if result.success:
    print("Labels set successfully")
else:
    print(f"Failed to set labels: {result.error_message}")
```

### Getting Session Labels

```python
from agentbay import AgentBay

# Initialize the SDK and create a session
agent_bay = AgentBay(api_key=api_key)
session_result = agent_bay.create()
session = session_result.session

# Get labels
result = session.get_labels()

if result.success:
    print("Session labels:")
    for key, value in result.data.items():
        print(f"  {key}: {value}")
else:
    print(f"Failed to get labels: {result.error_message}")
```

### Filtering Sessions by Labels

You can list sessions based on their labels to organize and manage your sessions:

```python
from agentbay import AgentBay
from agentbay.session_params import ListSessionParams

# Initialize the SDK
agent_bay = AgentBay(api_key=api_key)

# List sessions by labels
params = ListSessionParams(labels={"project": "demo"})
result = agent_bay.list_by_labels(params)

print(f"Found {len(result.sessions)} sessions")
for session in result.sessions:
    print(f"Session ID: {session.session_id}")
    # Clean up sessions when done
    agent_bay.delete(session)
```

## Getting Session Information

The `info()` method provides detailed information about a session, including direct browser access URLs and SDK integration credentials. This API serves two primary purposes:

1. **Cloud Environment Access**: Get the `resource_url` to directly access the cloud environment in a web browser with real-time video streaming and full mouse/keyboard control
2. **Session Status Validation**: Check if a session is still active and hasn't been released
3. **SDK Integration**: Extract authentication credentials for Web SDK (desktop) and Android SDK (mobile) integration

### Session Information Retrieval

```python
from agentbay import AgentBay

# Initialize the SDK and create a session
agent_bay = AgentBay(api_key=api_key)
session_result = agent_bay.create()
session = session_result.session

# Get session information
info_result = session.info()

if info_result.success:
    info = info_result.data
    print(f"Session ID: {info.session_id}")
    print(f"Resource ID: {info.resource_id}")
    print(f"Resource URL: {info.resource_url}")
    print(f"App ID: {info.app_id}")
    print(f"Resource Type: {info.resource_type}")
    print(f"Request ID: {info_result.request_id}")

    # Authentication info (displayed safely)
    print(f"Auth Code: {info.auth_code[:8]}***{info.auth_code[-8:]}")
    print(f"Connection Properties: {len(info.connection_properties)} chars")
    print(f"Ticket: {info.ticket[:50]}...")

    # The resource_url can be opened in a browser for direct access
    print("\n🌐 Open the resource_url in your browser to access the cloud environment!")
else:
    print(f"Failed to get session info: {info_result.error_message}")
```

### Session Information Field Details

- **session_id**: Unique identifier for the session
- **resource_id**: Cloud resource identifier (e.g., "p-xxxxxxxxx")
- **resource_url**: **Direct browser access URL** - Open this URL in any web browser to access the cloud environment with real-time video stream and full mouse/keyboard control
- **app_id**: Application type identifier
- **resource_type**: Resource classification (typically "AIAgent")
- **auth_code**: Authentication token required for Web SDK and Android SDK integration
- **connection_properties**: JSON configuration for SDK connection settings
- **ticket**: Gateway access ticket containing connection endpoints and tokens for SDK integration

### Session Information Use Cases

For detailed practical examples and use cases of session information, including browser access, Android SDK integration, and session health monitoring, see the [Session Information Use Cases Guide](../use-cases/session-info-use-cases.md).



## Deleting Sessions

When you're done with a session, delete it to free up resources:

```python
from agentbay import AgentBay

# Initialize the SDK and create a session
agent_bay = AgentBay(api_key=api_key)
session_result = agent_bay.create()
session = session_result.session

# Perform operations on the session...

# Delete the session
delete_result = agent_bay.delete(session)
if delete_result.success:
    print("Session deleted successfully")
else:
    print(f"Failed to delete session: {delete_result.error_message}")
```


## Session Recovery

In certain scenarios, you may need to recover a Session object after it has been destroyed. This can be accomplished through the following methods:

> **Note**: Session recovery methods will be upgraded in upcoming versions to provide enhanced functionality and improved user experience.

### Session Recovery

To recover a session, you need:
1. An AgentBay object (create a new one if it doesn't exist)
2. Create a new Session object with the AgentBay object and the session ID you want to recover

```python
from agentbay import AgentBay
from agentbay.session import Session

# Initialize the SDK (or use existing instance)
agent_bay = AgentBay(api_key=api_key)

# Recover session using session ID
session_id = "your_existing_session_id"
recovered_session = Session(agent_bay, session_id)

# For VPC scenarios, manually restore VPC-specific fields (these values must be saved by the developer)
# recovered_session.is_vpc = True
# recovered_session.network_interface_ip = "192.168.1.100"  # Your saved IP
# recovered_session.http_port = 8080  # Your saved port

# The recovered session can perform most session operations
print(f"Recovered session with ID: {recovered_session.session_id}")

# Test if the session is still active
info_result = recovered_session.info()
if info_result.success:
    print("Session is active and ready to use")
    print(f"Resource URL: {info_result.data.resource_url}")
else:
    print(f"Session recovery failed: {info_result.error_message}")
```

**VPC Session Recovery**: While a recovered Session object contains the session ID and can perform most operations, VPC scenarios require additional fields to be restored. For VPC scenarios, you need to restore three specific fields: `is_vpc`, `network_interface_ip`, and `http_port`. Since these fields are not currently stored in the cloud, developers must save and restore them manually as shown in the commented lines above.


### Important Considerations

**Session Recovery Limitations:**

1. **Released Sessions Cannot Be Recovered**: If the session ID corresponds to a cloud environment that has been actually released (either through active deletion via `Session.delete()` or automatic timeout release), it cannot be recovered using the session ID. In such cases, you must:
   - Create a new session
   - Use data persistence (see [Data Persistence Guide](data-persistence.md)) to restore your data

2. **Session Status Validation**: Use the `Session.info()` method to determine if a session has been released. Only active (non-released) sessions can return information through the info interface.

3. **Automatic Release Timeout**: Session automatic release timeout can be configured in the [console page](https://agentbay.console.aliyun.com/).

4. **Field Persistence**: Additional session fields (like VPC-specific fields) are not stored in the cloud and must be saved and restored manually by the developer.



## API Reference

For detailed API documentation, see:
- [Python Session API](https://github.com/aliyun/wuying-agentbay-sdk/blob/main/python/docs/api/session.md)
- [TypeScript Session API](https://github.com/aliyun/wuying-agentbay-sdk/blob/main/typescript/docs/api/session.md)
- [Golang Session API](https://github.com/aliyun/wuying-agentbay-sdk/blob/main/golang/docs/api/session.md)
- [Python AgentBay API](https://github.com/aliyun/wuying-agentbay-sdk/blob/main/python/docs/api/agentbay.md)
- [TypeScript AgentBay API](https://github.com/aliyun/wuying-agentbay-sdk/blob/main/typescript/docs/api/agentbay.md)
- [Golang AgentBay API](https://github.com/aliyun/wuying-agentbay-sdk/blob/main/golang/docs/api/agentbay.md)

## 📚 Related Guides

- [Data Persistence](data-persistence.md) - Persistent data storage across sessions
- [File Operations](file-operations.md) - File handling and management
- [Command Execution](command-execution.md) - Execute shell commands
- [VPC Sessions](../advanced/vpc-sessions.md) - Isolated network environments

## 🆘 Getting Help

- [GitHub Issues](https://github.com/aliyun/wuying-agentbay-sdk/issues)
- [Documentation Home](../README.md)
