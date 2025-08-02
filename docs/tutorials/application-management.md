# Application Management Tutorial

AgentBay SDK provides methods for managing applications in the cloud environment. This tutorial will guide you through listing installed applications, starting applications, and managing running processes.

## Overview

The Application module allows you to:

- List installed applications
- Start applications with custom parameters
- List and manage running processes
- Work with both desktop and mobile applications

## Listing Installed Applications

### Getting All Installed Applications

The following example demonstrates how to list all installed applications:

```python
from agentbay import AgentBay

# Initialize the SDK and create a session
agent_bay = AgentBay(api_key="your_api_key")
session_result = agent_bay.create()
session = session_result.session

# Get installed applications
apps = session.application.get_installed_apps(
    include_system_apps=True,
    include_store_apps=False,
    include_desktop_apps=True
)

print(f"Found {len(apps)} installed applications:")
for app in apps:
    print(f"Name: {app.name}")
    print(f"  Start Command: {app.start_cmd}")
    if hasattr(app, 'stop_cmd') and app.stop_cmd:
        print(f"  Stop Command: {app.stop_cmd}")
    if hasattr(app, 'work_directory') and app.work_directory:
        print(f"  Work Directory: {app.work_directory}")
    print()

# Delete the session when done
agent_bay.delete(session)
```

```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

// Initialize the SDK
const agentBay = new AgentBay({ apiKey: 'your_api_key' });

async function listInstalledApps() {
  try {
    // Create a session
    const createResponse = await agentBay.create();
    const session = createResponse.session;
    
    // Get installed applications
    const apps = await session.application.getInstalledApps(true, false, true);
    
    console.log(`Found ${apps.length} installed applications:`);
    apps.forEach(app => {
      console.log(`Name: ${app.name}`);
      console.log(`  Start Command: ${app.start_cmd}`);
      if (app.stop_cmd) {
        console.log(`  Stop Command: ${app.stop_cmd}`);
      }
      if (app.work_directory) {
        console.log(`  Work Directory: ${app.work_directory}`);
      }
      console.log();
    });
    
    // Delete the session
    await agentBay.delete(session);
  } catch (error) {
    console.error('Error:', error);
  }
}

listInstalledApps();
```

```go
package main

import (
	"fmt"
	"os"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

func main() {
  // Initialize the SDK
  client, err := agentbay.NewAgentBay("your_api_key")
  if err != nil {
    fmt.Printf("Error initializing AgentBay client: %v\n", err)
    os.Exit(1)
  }

  // Create a session
  result, err := client.Create(nil)
  if err != nil {
    fmt.Printf("Error creating session: %v\n", err)
    os.Exit(1)
  }

  session := result.Session

  // Get installed applications
  appsResult, err := session.Application.GetInstalledApps(true, false, true)
  if err != nil {
    fmt.Printf("Error getting installed apps: %v\n", err)
    os.Exit(1)
  }

  fmt.Printf("Found %d installed applications:\n", len(appsResult.Apps))
  for _, app := range appsResult.Apps {
    fmt.Printf("Name: %s\n", app.Name)
    fmt.Printf("  Start Command: %s\n", app.StartCmd)
    if app.StopCmd != "" {
      fmt.Printf("  Stop Command: %s\n", app.StopCmd)
    }
    if app.WorkDirectory != "" {
      fmt.Printf("  Work Directory: %s\n", app.WorkDirectory)
    }
    fmt.Println()
  }

  // Delete the session
  _, err = client.Delete(session)
  if err != nil {
    fmt.Printf("Error deleting session: %v\n", err)
    os.Exit(1)
  }
}
```

### Filtering Applications

You can filter the applications that are returned using the parameters:

```python
# Get only desktop applications, excluding system apps
desktop_apps = session.application.get_installed_apps(
    include_system_apps=False,
    include_store_apps=False,
    include_desktop_apps=True
)

print(f"Found {len(desktop_apps)} desktop applications:")
for app in desktop_apps:
    print(f"Name: {app.name}")
```

## Starting Applications

### Starting an Application by Command

The following example demonstrates how to start an application using its start command:

```python
from agentbay import AgentBay

# Initialize the SDK and create a session
agent_bay = AgentBay(api_key="your_api_key")
session_result = agent_bay.create()
session = session_result.session

# Start a simple application (text editor)
start_cmd = "notepad"
processes = session.application.start_app(start_cmd)

if processes:
    print(f"Application started successfully. {len(processes)} processes created:")
    for process in processes:
        print(f"  Process: {process.pname} (PID: {process.pid})")
else:
    print("Failed to start application")

# Let the application run for a few seconds
import time
time.sleep(5)

# Delete the session when done
agent_bay.delete(session)
```

```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

// Initialize the SDK
const agentBay = new AgentBay({ apiKey: 'your_api_key' });

async function startApplication() {
  try {
    // Create a session
    const createResponse = await agentBay.create();
    const session = createResponse.session;
    
    // Start a simple application (text editor)
    const startCmd = 'notepad';
    const processes = await session.application.startApp(startCmd);
    
    if (processes && processes.length > 0) {
      console.log(`Application started successfully. ${processes.length} processes created:`);
      processes.forEach(process => {
        console.log(`  Process: ${process.pname} (PID: ${process.pid})`);
      });
    } else {
      console.log('Failed to start application');
    }
    
    // Let the application run for a few seconds
    await new Promise(resolve => setTimeout(resolve, 5000));
    
    // Delete the session
    await agentBay.delete(session);
  } catch (error) {
    console.error('Error:', error);
  }
}

startApplication();
```

### Starting an Application with Custom Working Directory

You can specify a working directory when starting an application:

```python
# Start an application with a specific working directory
start_cmd = "python3 -m http.server"
work_dir = "/tmp"
processes = session.application.start_app(start_cmd, work_dir)

if processes:
    print(f"Web server started in {work_dir}")
    for process in processes:
        print(f"  Process: {process.pname} (PID: {process.pid})")
else:
    print("Failed to start web server")
```

## Managing Running Processes

### Listing Running Processes

The following example demonstrates how to list all running processes:

```python
from agentbay import AgentBay

# Initialize the SDK and create a session
agent_bay = AgentBay(api_key="your_api_key")
session_result = agent_bay.create()
session = session_result.session

# Get all running processes
processes = session.application.get_running_processes()

print(f"Found {len(processes)} running processes:")
for process in processes[:10]:  # Show only the first 10 for brevity
    print(f"PID: {process.pid}, Name: {process.pname}")
    if hasattr(process, 'cmdline') and process.cmdline:
        print(f"  Command Line: {process.cmdline}")

# Delete the session when done
agent_bay.delete(session)
```

```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

// Initialize the SDK
const agentBay = new AgentBay({ apiKey: 'your_api_key' });

async function listRunningProcesses() {
  try {
    // Create a session
    const createResponse = await agentBay.create();
    const session = createResponse.session;
    
    // Get all running processes
    const processes = await session.application.getRunningProcesses();
    
    console.log(`Found ${processes.length} running processes:`);
    // Show only the first 10 for brevity
    processes.slice(0, 10).forEach(process => {
      console.log(`PID: ${process.pid}, Name: ${process.pname}`);
      if (process.cmdline) {
        console.log(`  Command Line: ${process.cmdline}`);
      }
    });
    
    // Delete the session
    await agentBay.delete(session);
  } catch (error) {
    console.error('Error:', error);
  }
}

listRunningProcesses();
```

### Stopping a Process

To stop a running process by its PID:

```python
from agentbay import AgentBay

# Initialize the SDK and create a session
agent_bay = AgentBay(api_key="your_api_key")
session_result = agent_bay.create()
session = session_result.session

# Start an application
start_cmd = "sleep 30"  # This will sleep for 30 seconds
processes = session.application.start_app(start_cmd)

if processes:
    target_pid = processes[0].pid
    print(f"Started process with PID: {target_pid}")
    
    # Stop the process
    result = session.application.stop_process(target_pid)
    if result:
        print(f"Successfully stopped process with PID: {target_pid}")
    else:
        print(f"Failed to stop process with PID: {target_pid}")
else:
    print("Failed to start application")

# Delete the session when done
agent_bay.delete(session)
```

```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

// Initialize the SDK
const agentBay = new AgentBay({ apiKey: 'your_api_key' });

async function stopProcess() {
  try {
    // Create a session
    const createResponse = await agentBay.create();
    const session = createResponse.session;
    
    // Start an application
    const startCmd = 'sleep 30';  // This will sleep for 30 seconds
    const processes = await session.application.startApp(startCmd);
    
    if (processes && processes.length > 0) {
      const targetPid = processes[0].pid;
      console.log(`Started process with PID: ${targetPid}`);
      
      // Stop the process
      const result = await session.application.stopProcess(targetPid);
      if (result) {
        console.log(`Successfully stopped process with PID: ${targetPid}`);
      } else {
        console.log(`Failed to stop process with PID: ${targetPid}`);
      }
    } else {
      console.log('Failed to start application');
    }
    
    // Delete the session
    await agentBay.delete(session);
  } catch (error) {
    console.error('Error:', error);
  }
}

stopProcess();
```

## Mobile Application Management

### Getting Installed Mobile Applications

For mobile environments, you can list installed applications:

```python
from agentbay import AgentBay

# Initialize the SDK and create a session for a mobile environment
agent_bay = AgentBay(api_key="your_api_key")
session_result = agent_bay.create()  # This assumes a mobile environment image is used
session = session_result.session

# Get installed mobile applications
mobile_apps = session.application.get_mobile_apps()

print(f"Found {len(mobile_apps)} mobile applications:")
for app in mobile_apps[:5]:  # Show only the first 5 for brevity
    print(f"Package: {app.package_name}")
    print(f"  App Name: {app.app_name}")
    if hasattr(app, 'version_name') and app.version_name:
        print(f"  Version: {app.version_name}")
    print()

# Delete the session when done
agent_bay.delete(session)
```

### Starting a Mobile Application

To start a mobile application by package name:

```python
# Start a mobile application
package_name = "com.example.app"
result = session.application.start_mobile_app(package_name)

if result:
    print(f"Successfully started mobile app: {package_name}")
else:
    print(f"Failed to start mobile app: {package_name}")
```

## Best Practices

1. **Application Selection**: When starting applications, be aware of the system resources they might consume.
2. **Error Handling**: Always check the return result of application operations to ensure they completed successfully.
3. **Resource Management**: After completing operations, make sure to stop any processes you've started and delete sessions that are no longer needed.
4. **Working Directories**: When starting applications that create or modify files, it's often good practice to specify a working directory.
5. **Platform Awareness**: Be aware of the differences between desktop and mobile application management APIs.

## Related Resources

- [API Reference: Application (Python)](../api-reference/python/application.md)
- [API Reference: Application (TypeScript)](../api-reference/typescript/application.md)
- [API Reference: Application (Golang)](../api-reference/golang/application.md)
- [Examples: Application Management](../examples/python/application_window) 