# Computer API Reference - Application Management

## ⚡ Related Tutorial

- [Computer Use Guide](../../../../../docs/guides/computer-use/README.md) - Learn about computer automation capabilities

## Overview

The Computer module provides application lifecycle management capabilities within a session in the AgentBay cloud environment. This document focuses on the application management APIs including starting, stopping, and listing applications.

## Result Classes

### ProcessListResult

```java
public class ProcessListResult extends ApiResponse
```

Result of application start and list operations.

**Fields:**
- `success` (boolean): True if the operation succeeded
- `data` (List\<Process\>): List of processes
- `requestId` (String): Unique identifier for this API request
- `errorMessage` (String): Error description (if success is false)

### Process

```java
public class Process
```

Represents a running process.

**Fields:**
- `pname` (String): Process name
- `pid` (int): Process ID
- `cmdline` (String): Command line used to start the process

### AppOperationResult

```java
public class AppOperationResult extends ApiResponse
```

Result of application stop operations.

**Fields:**
- `success` (boolean): True if the operation succeeded
- `requestId` (String): Unique identifier for this API request
- `errorMessage` (String): Error description (if success is false)

### InstalledAppListResult

```java
public class InstalledAppListResult extends ApiResponse
```

Result of getting installed applications.

**Fields:**
- `success` (boolean): True if the operation succeeded
- `data` (List\<InstalledApp\>): List of installed applications
- `requestId` (String): Unique identifier for this API request
- `errorMessage` (String): Error description (if success is false)

### InstalledApp

```java
public class InstalledApp
```

Represents an installed application.

**Fields:**
- `name` (String): Application name
- `startCmd` (String): Command to start the application
- `stopCmd` (String): Command to stop the application (optional)
- `workDirectory` (String): Working directory (optional)

## Computer

```java
public class Computer extends BaseService
```

Handles desktop UI automation and application management operations in the AgentBay cloud environment.

### startApp

```java
public ProcessListResult startApp(String startCmd)
public ProcessListResult startApp(String startCmd, String workDirectory)
public ProcessListResult startApp(String startCmd, String workDirectory, String activity)
```

Starts an application with the given command, optional working directory, and optional activity.

**Parameters:**
- `startCmd` (String): The command to start the application (e.g., "npm run dev", "notepad.exe", "sleep 30")
- `workDirectory` (String, optional): Working directory for the application (e.g., "/tmp/app/react-site-demo-1"). Defaults to empty string.
- `activity` (String, optional): Activity name to launch (for mobile apps, e.g., "com.package/.Activity"). Defaults to empty string.

**Returns:**
- `ProcessListResult`: Result object containing:
  - `success` (boolean): True if the operation succeeded
  - `data` (List\<Process\>): List of processes started, each containing:
    - `pname` (String): Process name
    - `pid` (int): Process ID
    - `cmdline` (String): Command line
  - `requestId` (String): Unique identifier for this API request
  - `errorMessage` (String): Error description (if success is false)

**Example:**

```java
Session session = agentBay.create().getSession();

// Simple command without work directory
ProcessListResult result = session.getComputer().startApp("sleep 30");
if (result.isSuccess()) {
    for (Process process : result.getData()) {
        System.out.println("Started: " + process.getPname() + " (PID: " + process.getPid() + ")");
    }
}

// Command with work directory
ProcessListResult result2 = session.getComputer().startApp("npm run dev", "/tmp/app/my-project");
if (result2.isSuccess()) {
    System.out.println("Application started successfully");
}

session.delete();
```

**Important Notes:**
- The backend uses **systemd** to manage started applications
- Simple commands like `sleep 30` work reliably
- Complex commands that fork multiple processes (like `npm run dev`) may fail with "Failed to get main PID from systemd" error
- **Before starting applications with work directories**, ensure:
  1. The work directory exists (use `session.getFileSystem().createDirectory()`)
  2. Required files (e.g., `package.json`) exist in the directory
  3. Dependencies are installed if needed

---

### stopAppByPName

```java
public AppOperationResult stopAppByPName(String pname)
```

Stops an application by its process name.

**Parameters:**
- `pname` (String): The process name of the application to stop (e.g., "sleep", "node", "chrome")

**Returns:**
- `AppOperationResult`: Result object containing success status and error message if any

**Example:**

```java
AppOperationResult result = session.getComputer().stopAppByPName("sleep");
if (result.isSuccess()) {
    System.out.println("Application stopped successfully");
}
```

---

### stopAppByPID

```java
public AppOperationResult stopAppByPID(int pid)
```

Stops an application by its process ID.

**Parameters:**
- `pid` (int): The process ID of the application to stop

**Returns:**
- `AppOperationResult`: Result object containing success status and error message if any

**Example:**

```java
// First, start an application and get its PID
ProcessListResult startResult = session.getComputer().startApp("sleep 60");
if (startResult.isSuccess() && !startResult.getData().isEmpty()) {
    int pid = startResult.getData().get(0).getPid();
    
    // Later, stop it by PID
    AppOperationResult stopResult = session.getComputer().stopAppByPID(pid);
    if (stopResult.isSuccess()) {
        System.out.println("Application stopped successfully");
    }
}
```

---

### stopAppByCmd

```java
public AppOperationResult stopAppByCmd(String stopCmd)
```

Stops an application using a stop command.

**Parameters:**
- `stopCmd` (String): The command to stop the application (e.g., "pkill -f my-app")

**Returns:**
- `AppOperationResult`: Result object containing success status and error message if any

**Example:**

```java
AppOperationResult result = session.getComputer().stopAppByCmd("pkill -f 'npm run dev'");
if (result.isSuccess()) {
    System.out.println("Application stopped successfully");
}
```

---

### listVisibleApps

```java
public ProcessListResult listVisibleApps()
```

Lists all applications with visible windows.

**Returns:**
- `ProcessListResult`: Result object containing list of visible applications with detailed process information

**Example:**

```java
ProcessListResult result = session.getComputer().listVisibleApps();
if (result.isSuccess()) {
    System.out.println("Found " + result.getData().size() + " visible app(s)");
    for (Process process : result.getData()) {
        System.out.println("  - " + process.getPname() + " (PID: " + process.getPid() + ")");
    }
}
```

---

### getInstalledApps

```java
public InstalledAppListResult getInstalledApps()
public InstalledAppListResult getInstalledApps(boolean startMenu, boolean desktop, boolean ignoreSystemApps)
```

Gets the list of installed applications.

**Parameters:**
- `startMenu` (boolean, optional): Whether to include start menu applications. Defaults to true.
- `desktop` (boolean, optional): Whether to include desktop applications. Defaults to false.
- `ignoreSystemApps` (boolean, optional): Whether to ignore system applications. Defaults to true.

**Returns:**
- `InstalledAppListResult`: Result object containing list of installed apps and error message if any

**Example:**

```java
// Get installed apps with default settings
InstalledAppListResult result = session.getComputer().getInstalledApps();
if (result.isSuccess()) {
    for (InstalledApp app : result.getData()) {
        System.out.println("App: " + app.getName());
        System.out.println("  Start: " + app.getStartCmd());
    }
}

// Get apps including desktop shortcuts
InstalledAppListResult result2 = session.getComputer().getInstalledApps(true, true, true);
```

## Best Practices

1. **Always ensure work directory exists** before starting applications that require one
2. **Use simple commands for testing** - `sleep N` is reliable for testing the API
3. **Check result.isSuccess()** before accessing process data
4. **Store PIDs** for later use if you need to stop processes
5. **Handle the "Failed to get main PID from systemd" error** gracefully - it often indicates:
   - Work directory doesn't exist
   - Required files are missing
   - Command forks in a way systemd can't track

## Common Error Messages

| Error Message | Cause | Solution |
|--------------|-------|----------|
| `Failed to get main PID from systemd` | Systemd couldn't track the process | Ensure work directory and files exist; use simpler commands |
| `Work directory does not exist` | Specified directory not found | Create directory first using `FileSystem.createDirectory()` |
| `Command not found` | Executable not available | Ensure the command/tool is installed in the environment |

## Complete Example

```java
// Complete workflow: Setup environment, start app, monitor, and stop
Session session = agentBay.create(params).getSession();

// 1. Create work directory
String workDir = "/tmp/app/my-app";
session.getFileSystem().createDirectory(workDir);

// 2. Create necessary files
String packageJson = "{\"name\": \"my-app\", \"scripts\": {\"dev\": \"node server.js\"}}";
session.getFileSystem().writeFile(workDir + "/package.json", packageJson);

String serverJs = "setInterval(() => console.log('Running...'), 1000);";
session.getFileSystem().writeFile(workDir + "/server.js", serverJs);

// 3. Start the application
ProcessListResult startResult = session.getComputer().startApp("npm run dev", workDir);
if (startResult.isSuccess()) {
    int pid = startResult.getData().get(0).getPid();
    System.out.println("Started with PID: " + pid);
    
    // 4. Do something...
    Thread.sleep(5000);
    
    // 5. Stop the application
    session.getComputer().stopAppByPID(pid);
}

session.delete();
```

## Related Resources

- [Session API Reference](../common-features/basics/session.md)
- [FileSystem API Reference](../common-features/basics/filesystem.md)
- [Computer Start App Example](../../../../agentbay/src/main/java/com/aliyun/agentbay/examples/ComputerStartAppExample.java)

---

*Documentation for AgentBay Java SDK*

