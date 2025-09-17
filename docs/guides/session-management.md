# Session Management Documentation

This document provides comprehensive guidance on using the session management capabilities of the AgentBay SDK across all supported languages.

## Overview

Sessions are the fundamental unit of interaction with the AgentBay cloud environment. Each session represents an isolated environment where you can execute commands, manipulate files, run applications, and perform various operations in the cloud.

The session management system provides:
1. **Session Creation**: Create isolated environments with customizable parameters
2. **Session Lifecycle Management**: Manage the complete lifecycle of sessions
3. **Session Listing**: Retrieve and filter sessions based on various criteria
4. **Label Management**: Organize sessions using descriptive labels
5. **Context Synchronization**: Persist data across sessions using context synchronization
6. **Session Recovery**: Restore session objects using session IDs for continued operations

## Getting Started

### Prerequisites

To use session management, you need:
1. AgentBay SDK installed for your preferred language
2. Valid API key
3. Basic understanding of cloud computing concepts

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

You can customize sessions by specifying parameters such as image ID and labels:

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

## Session Context Synchronization

For data persistence across sessions, use context synchronization:

```python
from agentbay import AgentBay
from agentbay.context_sync import ContextSync, SyncPolicy
from agentbay.session_params import CreateSessionParams

# Initialize the SDK
agent_bay = AgentBay(api_key=api_key)

# Get or create a persistent context
context_result = agent_bay.context.get("my-persistent-context", create=True)

if context_result.success:
    # Configure context synchronization
    context_sync = ContextSync.new(
        context_id=context_result.context.id,
        path="/tmp/data",  # Mount path in the session
        policy=SyncPolicy.default()
    )

    # Create a session with context synchronization
    params = CreateSessionParams(context_syncs=[context_sync])
    session_result = agent_bay.create(params)

    if session_result.success:
        session = session_result.session
        print(f"Session created with ID: {session.session_id} and synchronized context at /tmp/data")
```

## Listing Sessions with Pagination

The session management system supports pagination for efficient handling of large numbers of sessions:

```python
from agentbay import AgentBay
from agentbay.session_params import ListSessionParams
from agentbay.session_params import CreateSessionParams

# Initialize the SDK
agent_bay = AgentBay()
# Create ten sessions
for i in range(10):
    # create parameters with labels
    params = CreateSessionParams(labels={"project": "demo"})
    agent_bay.create(params)

# List sessions by labels with pagination
params = ListSessionParams(
    labels={"project": "demo"},
    max_results=5
)
result = agent_bay.list_by_labels(params)

print(f"Found {len(result.sessions)} sessions")
if(len(result.sessions) > 0):
    # Handle pagination
    if result.next_token:
        params.next_token = result.next_token
        next_page = agent_bay.list_by_labels(params)
        print(f"Next page has {len(next_page.sessions)} sessions")
        if(len(next_page.sessions) > 0):
            for session in next_page.sessions:
                agent_bay.delete(session)
                print(f"Session ID: {session.session_id}")

    for session in result.sessions:
        print(f"Session ID: {session.session_id}")
        agent_bay.delete(session)
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

## Getting Session Information

The `info()` method provides detailed information about a session, including direct browser access URLs and SDK integration credentials. This API serves two primary purposes:

1. **Cloud Environment Access**: Get the `resource_url` to directly access the cloud environment in a web browser with real-time video streaming and full mouse/keyboard control
2. **Session Status Validation**: Check if a session is still active and hasn't been released
3. **SDK Integration**: Extract authentication credentials for Web SDK (desktop) and Android SDK (mobile) integration

### Basic Session Information Retrieval

```python
from agentbay import AgentBay

# Initialize the SDK and create a session
agent_bay = AgentBay(api_key=api_key)
session_result = agent_bay.create()
session = session_result.session

# Get session information for cloud environment access
info_result = session.info()

if info_result.success:
    session_info = info_result.data
    print(f"Session ID: {session_info.session_id}")
    print(f"Cloud Environment Access URL: {session_info.resource_url}")
    print(f"App Type: {session_info.app_id}")
    print(f"Request ID: {info_result.request_id}")

    # The resource_url can be directly opened in a browser for immediate access
    print("\n🌐 You can now open the resource_url in your browser to access the cloud environment!")
    print("   Features available: Video stream, Mouse control, Keyboard input")
else:
    print(f"Failed to get session info: {info_result.error_message}")
```

### Understanding Session Information Fields

The `SessionInfo` object contains comprehensive session details:

```python
from agentbay import AgentBay

# Get session information
info_result = session.info()

if info_result.success:
    info = info_result.data

    # Core session identifiers
    print(f"Session ID: {info.session_id}")
    print(f"Resource ID: {info.resource_id}")

    # Access and connection information
    print(f"Resource URL: {info.resource_url}")
    print(f"App ID: {info.app_id}")  # e.g., "agentBay-browser-cdp", "mcp-server-ubuntu"
    print(f"Resource Type: {info.resource_type}")  # e.g., "AIAgent"

    # Authentication and security
    print(f"Auth Code: {info.auth_code[:50]}...")  # Truncated for security
    print(f"Connection Properties: {info.connection_properties}")  # JSON string
    print(f"Ticket: {info.ticket[:100]}...")  # Contains gateway and token info
```

### Session Information Field Details

- **session_id**: Unique identifier for the session
- **resource_id**: Cloud resource identifier (e.g., "p-0cc7s1wz8fpx4kecc")
- **resource_url**: **Direct browser access URL** - Open this URL in any web browser to access the cloud environment with real-time video stream and full mouse/keyboard control
- **app_id**: Application type identifier:
  - `"agentBay-browser-cdp"` for browser sessions
  - `"mcp-server-ubuntu"` for Linux sessions
- **resource_type**: Resource classification (typically "AIAgent")
- **auth_code**: Authentication token required for Web SDK and Android SDK integration
- **connection_properties**: JSON configuration for SDK connection settings
- **ticket**: Gateway access ticket containing connection endpoints and tokens for SDK integration

### Practical Use Cases

#### 1. Cloud Environment Access via Browser
The most common use case is accessing the cloud environment directly through a web browser using the `resource_url`:

```python
def access_cloud_environment_browser(session):
    """Get cloud environment access URL for browser-based remote control."""
    info_result = session.info()

    if info_result.success:
        info = info_result.data
        resource_url = info.resource_url

        print(f"Cloud environment ready for session: {info.session_id}")
        print(f"Resource URL: {resource_url}")
        print("\n🌐 Copy and paste the Resource URL into any web browser to access the cloud environment")
        print("   Features available:")
        print("   - Real-time video stream of the desktop")
        print("   - Mouse and keyboard interaction capabilities")
        print("   - Full remote desktop experience")

        return {
            "session_id": info.session_id,
            "resource_url": resource_url,
            "access_method": "browser_direct"
        }
    else:
        print(f"Failed to get session info: {info_result.error_message}")
        return None

# Usage
access_info = access_cloud_environment_browser(session)
if access_info:
    print("Cloud environment URL is ready - open it in your browser to start using the remote desktop")
```

#### 2. Android SDK Configuration for Cloud Environment Access
The session information obtained from `session.info()` can be used as configuration parameters for the Alibaba Cloud Android SDK, enabling users to connect to the session's cloud environment through the Android SDK:

```python
def prepare_android_sdk_config(session):
    """Prepare Android SDK configuration for cloud environment connection."""
    info_result = session.info()
    
    if info_result.success:
        info = info_result.data
        
        # Android SDK Config parameters based on Alibaba Cloud Android SDK documentation
        # Reference: https://help.aliyun.com/zh/ecp/android-sdk-of-cloud-phone section 4.1 Config
        # info.resource_id maps to CONFIG_DESKTOP_ID
        # info.ticket maps to CONFIG_CONNECTION_TICKET
        android_config = {
            "CONFIG_DESKTOP_ID": info.resource_id,      # Desktop ID for connection
            "CONFIG_CONNECTION_TICKET": info.ticket,    # Connection ticket for authentication
            "CONFIG_USE_VPC": False,                     # VPC configuration (set based on your network setup)
            "OS_TYPE": "android",                        # OS type for the connection
            "CONFIG_USER": "",                           # User identifier (optional)
            "CONFIG_UUID": ""                            # UUID identifier (optional)
        }
        
        print("Android SDK Configuration:")
        print(f"CONFIG_DESKTOP_ID: {info.resource_id}")
        print(f"CONFIG_CONNECTION_TICKET: {info.ticket[:50]}...")  # Truncated for security
        print(f"CONFIG_USE_VPC: {android_config['CONFIG_USE_VPC']}")
        print(f"OS_TYPE: {android_config['OS_TYPE']}")
        
        return android_config
    else:
        print(f"Failed to prepare Android SDK config: {info_result.error_message}")
        return None

# Usage example for Android SDK integration
android_config = prepare_android_sdk_config(session)
if android_config:
    print("Android SDK configuration ready for StreamView connection")
    
    # Method 1: Using StreamView.start() with mConfigs (reference section 2.2)
    # Map<String, Object> mConfigs = new HashMap<>();
    # mConfigs.put("CONFIG_DESKTOP_ID", android_config.get("CONFIG_DESKTOP_ID"));
    # mConfigs.put("CONFIG_CONNECTION_TICKET", android_config.get("CONFIG_CONNECTION_TICKET"));
    # mConfigs.put("CONFIG_USE_VPC", android_config.get("CONFIG_USE_VPC"));
    # mConfigs.put("OS_TYPE", android_config.get("OS_TYPE"));
    # mConfigs.put("CONFIG_USER", android_config.get("CONFIG_USER"));
    # mConfigs.put("CONFIG_UUID", android_config.get("CONFIG_UUID"));
    # mStreamView.start(mConfigs);
    
    # Method 2: Using IAspEngine with ConnectionConfig (reference section 2.5)
    # ConnectionConfig cc = new ConnectionConfig();
    # cc.id = android_config.get("CONFIG_DESKTOP_ID");
    # cc.connectionTicket = android_config.get("CONFIG_CONNECTION_TICKET");
    # cc.useVPC = android_config.get("CONFIG_USE_VPC");
    # cc.type = android_config.get("OS_TYPE");
    # cc.user = android_config.get("CONFIG_USER");
    # cc.uuid = android_config.get("CONFIG_UUID");
    # engine.start(cc);
```

**Android SDK Integration Notes:**

- **`info.resource_id`** maps to **`CONFIG_DESKTOP_ID`** - This is the unique identifier for the cloud desktop/resource that the Android client will connect to
- **`info.ticket`** maps to **`CONFIG_CONNECTION_TICKET`** - This is the authentication ticket required to establish a secure connection to the cloud environment
- **`CONFIG_USE_VPC`** - Set to `true` if your cloud environment uses VPC networking, `false` for standard networking
- **`OS_TYPE`** - Specifies the OS type, typically set to "android" for mobile connections
- **`CONFIG_USER`** and **`CONFIG_UUID`** - Optional parameters that can be set based on your specific requirements
- The Android SDK supports two connection methods:
  1. **StreamView.start(mConfigs)** - Direct connection using configuration map (section 2.2)
  2. **IAspEngine with ConnectionConfig** - Multi-StreamView mode for advanced scenarios (section 2.5)
- For detailed Android SDK integration steps, refer to the [Alibaba Cloud Android SDK documentation](https://help.aliyun.com/zh/ecp/android-sdk-of-cloud-phone)

#### 3. Session Status Validation and Health Check
Use `info()` to check if a session is still active and hasn't been released:

```python
def check_session_status(session):
    """Check if session is still active and hasn't been released."""
    try:
        info_result = session.info()

        if info_result.success:
            info = info_result.data
            print(f"✅ Session {info.session_id} is ACTIVE")
            print(f"   Resource ID: {info.resource_id}")
            print(f"   App ID: {info.app_id}")
            print(f"   Resource Type: {info.resource_type}")
            return True
        else:
            print(f"❌ Session status check failed: {info_result.error_message}")
            return False

    except Exception as e:
        print(f"❌ Session has been RELEASED or is inaccessible: {e}")
        return False

def monitor_session_health(session, check_interval=30):
    """Continuously monitor session health."""
    import time

    print(f"Starting health monitoring for session: {session.session_id}")

    while True:
        is_active = check_session_status(session)

        if not is_active:
            print("🚨 Session is no longer active - stopping monitoring")
            break

        print(f"💚 Session health check passed - next check in {check_interval}s")
        time.sleep(check_interval)

# Usage examples
print("=== Session Status Check ===")
if check_session_status(session):
    print("Session is ready for use")
else:
    print("Session needs to be recreated")

# For continuous monitoring (run in background thread)
# import threading
# monitor_thread = threading.Thread(target=monitor_session_health, args=(session, 60))
# monitor_thread.daemon = True
# monitor_thread.start()
```



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

### Deleting Sessions with Context Synchronization

To ensure all context changes are synchronized before deletion:

```python
from agentbay import AgentBay

# Initialize the SDK and create a session
agent_bay = AgentBay(api_key=api_key)
# Get or create a persistent context
context_result = agent_bay.context.get("my-persistent-context", create=True)

if context_result.success:
    # Configure context synchronization
    context_sync = ContextSync.new(
        context_id=context_result.context.id,
        path="/tmp/data",  # Mount path in the session
        policy=SyncPolicy.default()
    )

    # Create a session with context synchronization
    params = CreateSessionParams(context_syncs=[context_sync])
    session_result = agent_bay.create(params)

    if session_result.success:
        session = session_result.session
        print(f"Session created with ID: {session.session_id} and synchronized context at /tmp/data")

# Perform operations on the session and make changes to synchronized contexts...

# Delete the session with context synchronization
delete_result = agent_bay.delete(session, sync_context=True)
# The delete() call will first trigger context.sync() to upload changes,
# then monitor all context operations until they complete (Success or Failed)
# or after maximum retry attempts (150 times with 2-second intervals)

if delete_result.success:
    print("Session deleted successfully with synchronized contexts")
else:
    # If any context operations failed, error messages will be printed automatically
    print(f"Failed to delete session: {delete_result.error_message}")
```

## Session Recovery

In certain scenarios, you may need to recover a Session object after it has been destroyed. This can be accomplished through the following methods:

### Basic Session Recovery

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

### Recovering Session with Additional Fields

While a recovered Session object contains the session ID and can perform most operations, some scenarios may require additional fields to be restored.

For VPC scenarios, you need to restore three specific fields: `is_vpc`, `network_interface_ip`, and `http_port`. Since these fields are not currently stored in the cloud, developers must save and restore them manually:

```python
from agentbay import AgentBay
from agentbay.session import Session

# Initialize the SDK
agent_bay = AgentBay(api_key=api_key)

# Recover session with VPC-specific fields
session_id = "your_vpc_session_id"
recovered_session = Session(agent_bay, session_id)

# Manually restore VPC-specific fields (these values must be saved by the developer)
recovered_session.is_vpc = True
recovered_session.network_interface_ip = "192.168.1.100"  # Your saved IP
recovered_session.http_port = 8080  # Your saved port

print(f"VPC session recovered with ID: {recovered_session.session_id}")
print(f"Network Interface IP: {recovered_session.network_interface_ip}")
print(f"HTTP Port: {recovered_session.http_port}")

# Verify the session is still active
info_result = recovered_session.info()
if info_result.success:
    print("VPC session is active and ready to use")
else:
    print("VPC session is no longer available")
```

### Session Recovery Validation

Before relying on a recovered session, always validate that the underlying cloud environment is still active:

```python
def validate_recovered_session(session):
    """Validate that a recovered session is still active and usable."""
    try:
        info_result = session.info()

        if info_result.success:
            info = info_result.data
            print(f"✅ Session {session.session_id} successfully recovered")
            print(f"   Resource ID: {info.resource_id}")
            print(f"   App ID: {info.app_id}")
            print(f"   Resource URL: {info.resource_url}")
            return True
        else:
            print(f"❌ Session recovery validation failed: {info_result.error_message}")
            return False

    except Exception as e:
        print(f"❌ Session {session.session_id} is no longer available: {e}")
        return False

# Usage example
recovered_session = Session(agent_bay, "your_session_id")
if validate_recovered_session(recovered_session):
    print("Session is ready for use")
    # Continue with session operations...
else:
    print("Need to create a new session and restore data from persistence")
    # Create new session and use data persistence for recovery
```

### Important Considerations

**Session Recovery Limitations:**

1. **Released Sessions Cannot Be Recovered**: If the session ID corresponds to a cloud environment that has been actually released (either through active deletion via `Session.delete()` or automatic timeout release), it cannot be recovered using the session ID. In such cases, you must:
   - Create a new session
   - Use data persistence (see [Data Persistence Guide](data-persistence.md)) to restore your data

2. **Session Status Validation**: Use the `Session.info()` method to determine if a session has been released. Only active (non-released) sessions can return information through the info interface.

3. **Automatic Release Timeout**: Session automatic release timeout can be configured in the console page (https://agentbay.console.aliyun.com/).

4. **Field Persistence**: Additional session fields (like VPC-specific fields) are not stored in the cloud and must be saved and restored manually by the developer.

## Best Practices

1. **Resource Management**:
   - Always delete sessions that are no longer in use to avoid unnecessary resource consumption
   - Use session pooling for applications with high session turnover

2. **Using Labels**:
   - Add descriptive labels to sessions to make them easier to identify and manage
   - Use consistent labeling schemes across your organization

3. **Error Handling**:
   - Always check the `success` and `error_message` fields in the result objects
   - Implement retry logic for transient failures
   - Log request IDs for debugging purposes

4. **Session Reuse**:
   - If you need to perform multiple operations, try to complete them in the same session
   - Avoid creating short-lived sessions for single operations

5. **Context Synchronization**:
   - Use context synchronization for data persistence across sessions
   - Choose appropriate synchronization policies based on your use case
   - Monitor context synchronization status during session creation and deletion

6. **Performance Optimization**:
   - Use pagination when listing large numbers of sessions
   - Implement efficient filtering using labels
   - Minimize the number of synchronized contexts per session

7. **Session Recovery**:
   - Always validate recovered sessions using the `info()` method before performing operations
   - Save critical session fields (like VPC configurations) externally for recovery purposes
   - Implement fallback logic to create new sessions when recovery fails
   - Use data persistence mechanisms to maintain state across session recreations
   - Monitor session timeout settings in the console to prevent unexpected releases

## Limitations

1. **Session Limits**: There are limits on the number of concurrent sessions
2. **Resource Constraints**: Sessions have limits on CPU, memory, and storage
3. **Session Duration**: Sessions have maximum lifetime limits
4. **Network Dependencies**: Session operations require network connectivity

## Troubleshooting

### Common Issues

1. **Session Creation Failures**:
   - Verify your API key is valid
   - Check if you've reached session limits
   - Ensure the specified image ID is valid

2. **Context Synchronization Issues**:
   - Check network connectivity
   - Verify context IDs are valid
   - Review synchronization policy settings

3. **Pagination Problems**:
   - Ensure next tokens are properly handled
   - Check max results parameter is within allowed limits
   - Verify label filters are correctly specified

4. **Session Deletion Failures**:
   - Confirm the session exists and is active
   - Check for ongoing operations that might prevent deletion
   - Review context synchronization status

5. **Session Recovery Issues**:
   - Verify the session ID is correct and corresponds to an active session
   - Use `Session.info()` to check if the session has been released
   - Ensure all required session fields are manually restored for specialized scenarios (e.g., VPC)
   - Check session timeout settings in the console if sessions are being released unexpectedly
   - Implement proper error handling for cases where recovery is not possible

## API Reference

For detailed API documentation, see:
- [Python Session API](https://github.com/aliyun/wuying-agentbay-sdk/blob/main/python/docs/api/session.md)
- [TypeScript Session API](https://github.com/aliyun/wuying-agentbay-sdk/blob/main/typescript/docs/api/session.md)
- [Golang Session API](https://github.com/aliyun/wuying-agentbay-sdk/blob/main/golang/docs/api/session.md)
- [Python AgentBay API](https://github.com/aliyun/wuying-agentbay-sdk/blob/main/python/docs/api/agentbay.md)
- [TypeScript AgentBay API](https://github.com/aliyun/wuying-agentbay-sdk/blob/main/typescript/docs/api/agentbay.md)
- [Golang AgentBay API](https://github.com/aliyun/wuying-agentbay-sdk/blob/main/golang/docs/api/agentbay.md)
