# Session Class API Reference

The `Session` class represents a session in the AgentBay cloud environment. It provides methods for managing file systems, executing commands, and more.

## Properties

### Python

```python
agent_bay  # The AgentBay instance that created this session
session_id  # The ID of this session
resource_url  # The URL of the resource associated with this session
file_system  # The FileSystem instance for this session
command  # The Command instance for this session
oss  # The Oss instance for this session
application  # The ApplicationManager instance for this session
window  # The WindowManager instance for this session
ui  # The UI instance for this session
context  # The ContextManager instance for this session
```

### TypeScript

```typescript
agentBay  // The AgentBay instance that created this session
sessionId  // The ID of this session
resourceUrl  // The URL of the resource associated with this session
fileSystem  // The FileSystem instance for this session
command  // The Command instance for this session
oss  // The Oss instance for this session
application  // The ApplicationManager instance for this session
window  // The WindowManager instance for this session
ui  // The UI instance for this session
context  // The ContextManager instance for this session
```

### Golang

```go
SessionID  // The ID of this session
ResourceURL  // The URL of the resource associated with this session
FileSystem  // The FileSystem instance for this session
Command  // The Command instance for this session
Oss  // The Oss instance for this session
Application  // The ApplicationManager instance for this session
Window  // The WindowManager instance for this session
UI  // The UI instance for this session
Context  // The ContextManager instance for this session
```

## Methods

### delete / Delete

Deletes this session.

#### Python

```python
delete() -> DeleteResult
```

**Returns:**
- `DeleteResult`: A result object containing success status, request ID, and error message if any.

**Example:**
```python
from agentbay import AgentBay

# Initialize the SDK
agent_bay = AgentBay(api_key="your_api_key")

# Create a session
result = agent_bay.create()
if result.success:
    session = result.session
    print(f"Session created with ID: {session.session_id}")
    
    # Use the session...
    
    # Delete the session when done
    delete_result = session.delete()
    if delete_result.success:
        print(f"Session deleted successfully")
    else:
        print(f"Failed to delete session: {delete_result.error_message}")
```

#### TypeScript

```typescript
delete(): Promise<DeleteResult>
```

**Returns:**
- `Promise<DeleteResult>`: A promise that resolves to a result object containing success status, request ID, and error message if any.

**Example:**
```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

// Initialize the SDK
const agentBay = new AgentBay({ apiKey: 'your_api_key' });

// Create and delete a session
async function createAndDeleteSession() {
  try {
    const result = await agentBay.create();
    if (result.success) {
      const session = result.session;
      console.log(`Created session with ID: ${session.sessionId}`);
      
      // Use the session...
      
      // Delete the session when done
      const deleteResult = await session.delete();
      if (deleteResult.success) {
        console.log('Session deleted successfully');
      } else {
        console.log(`Failed to delete session: ${deleteResult.errorMessage}`);
      }
    }
  } catch (error) {
    console.error('Error:', error);
  }
}

createAndDeleteSession();
```

#### Golang

```go
Delete() (*DeleteResult, error)
```

**Returns:**
- `*DeleteResult`: A result object containing success status and RequestID.
- `error`: An error if the session deletion fails.

**Example:**
```go
package main

import (
	"fmt"
	"os"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

func main() {
	// Initialize the SDK
	client, err := agentbay.NewAgentBay("your_api_key", nil)
	if err != nil {
		fmt.Printf("Error initializing AgentBay client: %v\n", err)
		os.Exit(1)
	}

	// Create a session
	createResult, err := client.Create(nil)
	if err != nil {
		fmt.Printf("Error creating session: %v\n", err)
		os.Exit(1)
	}
	
	session := createResult.Session
	fmt.Printf("Created session with ID: %s\n", session.SessionID)
	
	// Use the session...
	
	// Delete the session when done
	deleteResult, err := session.Delete()
	if err != nil {
		fmt.Printf("Error deleting session: %v\n", err)
		os.Exit(1)
	}
	
	fmt.Println("Session deleted successfully")
	fmt.Printf("Request ID: %s\n", deleteResult.RequestID)
}
```

### set_labels / setLabels / SetLabels

Sets labels for this session.

#### Python

```python
set_labels(labels: Dict[str, str]) -> OperationResult
```

**Parameters:**
- `labels` (Dict[str, str]): Key-value pairs representing the labels to set.

**Returns:**
- `OperationResult`: A result object containing success status, request ID, and error message if any.

**Raises:**
- `SessionError`: If the operation fails.

**Example:**
```python
from agentbay import AgentBay

# Initialize the SDK
agent_bay = AgentBay(api_key="your_api_key")

# Create a session
result = agent_bay.create()
if result.success:
    session = result.session
    
    # Set labels for the session
    labels = {
        "project": "demo",
        "environment": "testing",
        "owner": "user123"
    }
    
    label_result = session.set_labels(labels)
    if label_result.success:
        print(f"Labels set successfully, request ID: {label_result.request_id}")
    else:
        print(f"Failed to set labels: {label_result.error_message}")
```

#### TypeScript

```typescript
setLabels(labels: Record<string, string>): Promise<OperationResult>
```

**Parameters:**
- `labels` (Record<string, string>): Key-value pairs representing the labels to set.

**Returns:**
- `Promise<OperationResult>`: A promise that resolves to a result object containing success status, request ID, and error message if any.

**Example:**
```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

// Initialize the SDK
const agentBay = new AgentBay({ apiKey: 'your_api_key' });

// Create a session and set labels
async function setSessionLabels() {
  try {
    const result = await agentBay.create();
    if (result.success) {
      const session = result.session;
      
      // Set labels for the session
      const labels = {
        project: 'demo',
        environment: 'testing',
        owner: 'user123'
      };
      
      const labelResult = await session.setLabels(labels);
      if (labelResult.success) {
        console.log(`Labels set successfully, request ID: ${labelResult.requestId}`);
      } else {
        console.log(`Failed to set labels: ${labelResult.errorMessage}`);
      }
    }
  } catch (error) {
    console.error('Error:', error);
  }
}

setSessionLabels();
```

#### Golang

```go
SetLabels(labels map[string]string) (*OperationResult, error)
```

**Parameters:**
- `labels` (map[string]string): Key-value pairs representing the labels to set.

**Returns:**
- `*OperationResult`: A result object containing success status and RequestID.
- `error`: An error if the operation fails.

**Example:**
```go
package main

import (
	"fmt"
	"os"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

func main() {
	// Initialize the SDK
	client, err := agentbay.NewAgentBay("your_api_key", nil)
	if err != nil {
		fmt.Printf("Error initializing AgentBay client: %v\n", err)
		os.Exit(1)
	}

	// Create a session
	createResult, err := client.Create(nil)
	if err != nil {
		fmt.Printf("Error creating session: %v\n", err)
		os.Exit(1)
	}
	
	session := createResult.Session
	
	// Set labels for the session
	labels := map[string]string{
		"project":     "demo",
		"environment": "testing",
		"owner":       "user123",
	}
	
	labelResult, err := session.SetLabels(labels)
	if err != nil {
		fmt.Printf("Error setting labels: %v\n", err)
		os.Exit(1)
	}
	
	fmt.Println("Labels set successfully")
	fmt.Printf("Request ID: %s\n", labelResult.RequestID)
}
```

### get_labels / getLabels / GetLabels

Gets the labels for this session.

#### Python

```python
get_labels() -> OperationResult
```

**Returns:**
- `OperationResult`: A result object containing the labels as data, success status, request ID, and error message if any.

**Raises:**
- `SessionError`: If the operation fails.

**Example:**
```python
from agentbay import AgentBay

# Initialize the SDK
agent_bay = AgentBay(api_key="your_api_key")

# Create a session
result = agent_bay.create()
if result.success:
    session = result.session
    
    # Set some labels first
    session.set_labels({"project": "demo", "environment": "testing"})
    
    # Get the labels
    label_result = session.get_labels()
    if label_result.success:
        labels = label_result.data
        print(f"Session labels:")
        for key, value in labels.items():
            print(f"  {key}: {value}")
        print(f"Request ID: {label_result.request_id}")
    else:
        print(f"Failed to get labels: {label_result.error_message}")
```

#### TypeScript

```typescript
getLabels(): Promise<OperationResult>
```

**Returns:**
- `Promise<OperationResult>`: A promise that resolves to a result object containing the labels as data, success status, request ID, and error message if any.

**Example:**
```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

// Initialize the SDK
const agentBay = new AgentBay({ apiKey: 'your_api_key' });

// Create a session and get labels
async function getSessionLabels() {
  try {
    const result = await agentBay.create();
    if (result.success) {
      const session = result.session;
      
      // Set some labels first
      await session.setLabels({
        project: 'demo', 
        environment: 'testing'
      });
      
      // Get the labels
      const labelResult = await session.getLabels();
      if (labelResult.success) {
        const labels = labelResult.data;
        console.log('Session labels:');
        Object.entries(labels).forEach(([key, value]) => {
          console.log(`  ${key}: ${value}`);
        });
        console.log(`Request ID: ${labelResult.requestId}`);
      } else {
        console.log(`Failed to get labels: ${labelResult.errorMessage}`);
      }
    }
  } catch (error) {
    console.error('Error:', error);
  }
}

getSessionLabels();
```

#### Golang

```go
GetLabels() (*OperationResult, error)
```

**Returns:**
- `*OperationResult`: A result object containing the labels as data, success status, and RequestID.
- `error`: An error if the operation fails.

**Example:**
```go
package main

import (
	"fmt"
	"os"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

func main() {
	// Initialize the SDK
	client, err := agentbay.NewAgentBay("your_api_key", nil)
	if err != nil {
		fmt.Printf("Error initializing AgentBay client: %v\n", err)
		os.Exit(1)
	}

	// Create a session
	createResult, err := client.Create(nil)
	if err != nil {
		fmt.Printf("Error creating session: %v\n", err)
		os.Exit(1)
	}
	
	session := createResult.Session
	
	// Set some labels first
	labels := map[string]string{
		"project":     "demo",
		"environment": "testing",
	}
	_, err = session.SetLabels(labels)
	if err != nil {
		fmt.Printf("Error setting labels: %v\n", err)
		os.Exit(1)
	}
	
	// Get the labels
	labelResult, err := session.GetLabels()
	if err != nil {
		fmt.Printf("Error getting labels: %v\n", err)
		os.Exit(1)
	}
	
	// The data is returned as an interface{}, convert it to map[string]string
	labelsData, ok := labelResult.Data.(map[string]string)
	if !ok {
		fmt.Println("Error: Labels data is not in expected format")
		os.Exit(1)
	}
	
	fmt.Println("Session labels:")
	for key, value := range labelsData {
		fmt.Printf("  %s: %s\n", key, value)
	}
	fmt.Printf("Request ID: %s\n", labelResult.RequestID)
}
```

### info / Info

Gets information about this session.

#### Python

```python
info() -> OperationResult
```

**Returns:**
- `OperationResult`: A result object containing the session information as data, success status, request ID, and error message if any.

**Raises:**
- `SessionError`: If the operation fails.

**Example:**
```python
from agentbay import AgentBay

# Initialize the SDK
agent_bay = AgentBay(api_key="your_api_key")

# Create a session
result = agent_bay.create()
if result.success:
    session = result.session
    
    # Get session information
    info_result = session.info()
    if info_result.success:
        session_info = info_result.data
        print(f"Session Information:")
        print(f"  Session ID: {session_info.session_id}")
        print(f"  Resource URL: {session_info.resource_url}")
        print(f"  Resource ID: {session_info.resource_id}")
        print(f"  Resource Type: {session_info.resource_type}")
        print(f"Request ID: {info_result.request_id}")
    else:
        print(f"Failed to get session info: {info_result.error_message}")
```

#### TypeScript

```typescript
info(): Promise<OperationResult>
```

**Returns:**
- `Promise<OperationResult>`: A promise that resolves to a result object containing the session information as data, success status, request ID, and error message if any.

**Example:**
```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

// Initialize the SDK
const agentBay = new AgentBay({ apiKey: 'your_api_key' });

// Create a session and get info
async function getSessionInfo() {
  try {
    const result = await agentBay.create();
    if (result.success) {
      const session = result.session;
      
      // Get session information
      const infoResult = await session.info();
      if (infoResult.success) {
        const sessionInfo = infoResult.data;
        console.log('Session Information:');
        console.log(`  Session ID: ${sessionInfo.sessionId}`);
        console.log(`  Resource URL: ${sessionInfo.resourceUrl}`);
        console.log(`  Resource ID: ${sessionInfo.resourceId}`);
        console.log(`  Resource Type: ${sessionInfo.resourceType}`);
        console.log(`Request ID: ${infoResult.requestId}`);
      } else {
        console.log(`Failed to get session info: ${infoResult.errorMessage}`);
      }
    }
  } catch (error) {
    console.error('Error:', error);
  }
}

getSessionInfo();
```

#### Golang

```go
Info() (*OperationResult, error)
```

**Returns:**
- `*OperationResult`: A result object containing the session information as data, success status, and RequestID.
- `error`: An error if the operation fails.

**Example:**
```go
package main

import (
	"fmt"
	"os"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

func main() {
	// Initialize the SDK
	client, err := agentbay.NewAgentBay("your_api_key", nil)
	if err != nil {
		fmt.Printf("Error initializing AgentBay client: %v\n", err)
		os.Exit(1)
	}

	// Create a session
	createResult, err := client.Create(nil)
	if err != nil {
		fmt.Printf("Error creating session: %v\n", err)
		os.Exit(1)
	}
	
	session := createResult.Session
	
	// Get session information
	infoResult, err := session.Info()
	if err != nil {
		fmt.Printf("Error getting session info: %v\n", err)
		os.Exit(1)
	}
	
	// The data is returned as an interface{}, convert it to SessionInfo
	sessionInfo, ok := infoResult.Data.(*agentbay.SessionInfo)
	if !ok {
		fmt.Println("Error: Session info data is not in expected format")
		os.Exit(1)
	}
	
	fmt.Println("Session Information:")
	fmt.Printf("  Session ID: %s\n", sessionInfo.SessionID)
	fmt.Printf("  Resource URL: %s\n", sessionInfo.ResourceURL)
	fmt.Printf("  Resource ID: %s\n", sessionInfo.ResourceID)
	fmt.Printf("  Resource Type: %s\n", sessionInfo.ResourceType)
	fmt.Printf("Request ID: %s\n", infoResult.RequestID)
}
```

### get_link / getLink / GetLink

Gets a link to access the session via the specified protocol and port.

#### Python

```python
get_link(protocol_type: Optional[str] = None, port: Optional[int] = None) -> OperationResult
```

**Parameters:**
- `protocol_type` (str, optional): The protocol type for the link (e.g., "http", "https", "ssh"). If None, the default protocol is used.
- `port` (int, optional): The port number for the link. If None, the default port for the protocol is used.

**Returns:**
- `OperationResult`: A result object containing the link information as data, success status, request ID, and error message if any.

**Raises:**
- `SessionError`: If the operation fails.

**Example:**
```python
from agentbay import AgentBay

# Initialize the SDK
agent_bay = AgentBay(api_key="your_api_key")

# Create a session
result = agent_bay.create()
if result.success:
    session = result.session
    
    # Get an HTTP link on port 8080
    link_result = session.get_link(protocol_type="http", port=8080)
    if link_result.success:
        link_info = link_result.data
        print(f"Link Information:")
        print(f"  URL: {link_info.url}")
        print(f"  Connection string: {link_info.connection_string}")
        print(f"Request ID: {link_result.request_id}")
    else:
        print(f"Failed to get link: {link_result.error_message}")
```

#### TypeScript

```typescript
getLink(protocolType?: string, port?: number): Promise<OperationResult>
```

**Parameters:**
- `protocolType` (string, optional): The protocol type for the link (e.g., "http", "https", "ssh"). If not provided, the default protocol is used.
- `port` (number, optional): The port number for the link. If not provided, the default port for the protocol is used.

**Returns:**
- `Promise<OperationResult>`: A promise that resolves to a result object containing the link information as data, success status, request ID, and error message if any.

**Example:**
```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

// Initialize the SDK
const agentBay = new AgentBay({ apiKey: 'your_api_key' });

// Create a session and get link
async function getSessionLink() {
  try {
    const result = await agentBay.create();
    if (result.success) {
      const session = result.session;
      
      // Get an HTTP link on port 8080
      const linkResult = await session.getLink('http', 8080);
      if (linkResult.success) {
        const linkInfo = linkResult.data;
        console.log('Link Information:');
        console.log(`  URL: ${linkInfo.url}`);
        console.log(`  Connection string: ${linkInfo.connectionString}`);
        console.log(`Request ID: ${linkResult.requestId}`);
      } else {
        console.log(`Failed to get link: ${linkResult.errorMessage}`);
      }
    }
  } catch (error) {
    console.error('Error:', error);
  }
}

getSessionLink();
```

#### Golang

```go
GetLink(protocolType string, port int) (*OperationResult, error)
```

**Parameters:**
- `protocolType` (string): The protocol type for the link (e.g., "http", "https", "ssh"). If empty, the default protocol is used.
- `port` (int): The port number for the link. If 0, the default port for the protocol is used.

**Returns:**
- `*OperationResult`: A result object containing the link information as data, success status, and RequestID.
- `error`: An error if the operation fails.

**Example:**
```go
package main

import (
	"fmt"
	"os"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

func main() {
	// Initialize the SDK
	client, err := agentbay.NewAgentBay("your_api_key", nil)
	if err != nil {
		fmt.Printf("Error initializing AgentBay client: %v\n", err)
		os.Exit(1)
	}

	// Create a session
	createResult, err := client.Create(nil)
	if err != nil {
		fmt.Printf("Error creating session: %v\n", err)
		os.Exit(1)
	}
	
	session := createResult.Session
	
	// Get an HTTP link on port 8080
	linkResult, err := session.GetLink("http", 8080)
	if err != nil {
		fmt.Printf("Error getting session link: %v\n", err)
		os.Exit(1)
	}
	
	// The data is returned as an interface{}, convert it to LinkInfo
	linkInfo, ok := linkResult.Data.(*agentbay.LinkInfo)
	if !ok {
		fmt.Println("Error: Link info data is not in expected format")
		os.Exit(1)
	}
	
	fmt.Println("Link Information:")
	fmt.Printf("  URL: %s\n", linkInfo.URL)
	fmt.Printf("  Connection string: %s\n", linkInfo.ConnectionString)
	fmt.Printf("Request ID: %s\n", linkResult.RequestID)
}
```

## Related Classes

The Session class provides access to several other classes that provide specific functionality:

- [FileSystem](filesystem.md): Provides methods for file operations within a session.
- [Command](command.md): Provides methods for executing commands within a session.
- [UI](ui.md): Provides methods for interacting with the UI elements in the cloud environment.
- [Application](../concepts/applications.md): Provides methods for managing applications in the cloud environment.
- [Window](../concepts/applications.md): Provides methods for managing windows in the cloud environment.

## Usage Examples

### Python

```python
# Create a session with labels
params = CreateSessionParams()
params.labels = {
    "purpose": "demo",
    "environment": "development"
}
session = agent_bay.create(params)

# Use the session to execute a command
result = session.command.execute_command("ls -la")

# Use the session to read a file
content = session.filesystem.read_file("/etc/hosts")

# Get installed applications
apps = session.application.get_installed_apps(include_system_apps=True,
                                             include_store_apps=False,
                                             include_desktop_apps=True)

# List visible applications
processes = session.application.list_visible_apps()

# List root windows
windows = session.window.list_root_windows()

# Get active window
active_window = session.window.get_active_window()

# Get session labels
labels = session.get_labels()

# Get session info
session_info = session.info()
print(f"Session ID: {session_info['session_id']}")
print(f"Resource URL: {session_info['resource_url']}")
print(f"App ID: {session_info.get('app_id')}")
print(f"Auth Code: {session_info.get('auth_code')}")
print(f"Connection Properties: {session_info.get('connection_properties')}")
print(f"Resource ID: {session_info.get('resource_id')}")
print(f"Resource Type: {session_info.get('resource_type')}")

# Delete the session
session.delete()
```

### TypeScript

```typescript
// Create a session with labels
const session = await agentBay.create({
  labels: {
    purpose: 'demo',
    environment: 'development'
  }
});

// Use the session to execute a command
const result = await session.command.executeCommand('ls -la');

// Use the session to read a file
const content = await session.filesystem.readFile('/etc/hosts');

// Get installed applications
const apps = await session.application.getInstalledApps(true, false, true);

// List visible applications
const processes = await session.application.listVisibleApps();

// List root windows
const windows = await session.window.listRootWindows();

// Get active window
const activeWindow = await session.window.getActiveWindow();

// Get session labels
const labels = await session.getLabels();

// Get session info
const sessionInfo = await session.info();
log(`Session ID: ${sessionInfo.sessionId}`);
log(`Resource URL: ${sessionInfo.resourceUrl}`);
log(`App ID: ${sessionInfo.appId}`);
log(`Auth Code: ${sessionInfo.authCode}`);
log(`Connection Properties: ${sessionInfo.connectionProperties}`);
log(`Resource ID: ${sessionInfo.resourceId}`);
log(`Resource Type: ${sessionInfo.resourceType}`);

// Delete the session
await session.delete();
```

### Golang

```go
// Create a session with labels
params := agentbay.NewCreateSessionParams().
    WithLabels(map[string]string{
        "purpose":     "demo",
        "environment": "development",
    })
sessionResult, err := client.Create(params)
if err != nil {
    // Handle error
}
session := sessionResult.Session
fmt.Printf("Session created with ID: %s (RequestID: %s)\n", session.SessionID, sessionResult.RequestID)

// Use the session to execute a command
commandResult, err := session.Command.ExecuteCommand("ls -la")
if err != nil {
    // Handle error
}
fmt.Printf("Command output: %s (RequestID: %s)\n", commandResult.Output, commandResult.RequestID)

// Use the session to read a file
readResult, err := session.FileSystem.ReadFile("/etc/hosts")
if err != nil {
    // Handle error
}
fmt.Printf("File content: %s (RequestID: %s)\n", readResult.Content, readResult.RequestID)

// Get installed applications
appsResult, err := session.Application.GetInstalledApps(true, false, true)
if err != nil {
    // Handle error
}
fmt.Printf("Found %d installed apps (RequestID: %s)\n", len(appsResult.Apps), appsResult.RequestID)

// List visible applications
processesResult, err := session.Application.ListVisibleApps()
if err != nil {
    // Handle error
}
fmt.Printf("Found %d visible processes (RequestID: %s)\n", len(processesResult.Processes), processesResult.RequestID)

// List root windows
windowsResult, err := session.Window.ListRootWindows()
if err != nil {
    // Handle error
}
fmt.Printf("Found %d root windows (RequestID: %s)\n", len(windowsResult.Windows), windowsResult.RequestID)

// Get active window
activeWindowResult, err := session.Window.GetActiveWindow()
if err != nil {
    // Handle error
}
if activeWindowResult.Window != nil {
    fmt.Printf("Active window: %s (ID: %d, PID: %d) (RequestID: %s)\n",
        activeWindowResult.Window.Title, activeWindowResult.Window.WindowID,
        activeWindowResult.Window.PID, activeWindowResult.RequestID)
}

// Get session labels
labelsResult, err := session.GetLabels()
if err != nil {
    // Handle error
}
fmt.Printf("Session labels: %v (RequestID: %s)\n", labelsResult.Labels, labelsResult.RequestID)

// Get session info
infoResult, err := session.Info()
if err != nil {
    // Handle error
}
sessionInfo := infoResult.Info
fmt.Printf("Session ID: %s (RequestID: %s)\n", sessionInfo.SessionId, infoResult.RequestID)
fmt.Printf("Resource URL: %s\n", sessionInfo.ResourceUrl)
fmt.Printf("App ID: %s\n", sessionInfo.AppId)
fmt.Printf("Auth Code: %s\n", sessionInfo.AuthCode)
fmt.Printf("Connection Properties: %s\n", sessionInfo.ConnectionProperties)
fmt.Printf("Resource ID: %s\n", sessionInfo.ResourceId)
fmt.Printf("Resource Type: %s\n", sessionInfo.ResourceType)

// Delete the session
deleteResult, err := session.Delete()
if err != nil {
    // Handle error
}
fmt.Printf("Session deleted successfully (RequestID: %s)\n", deleteResult.RequestID)
```

## Related Resources

- [Sessions Concept](../concepts/sessions.md): Learn more about sessions in the AgentBay cloud environment.
- [AgentBay Class](agentbay.md): The main entry point for creating and managing sessions.
