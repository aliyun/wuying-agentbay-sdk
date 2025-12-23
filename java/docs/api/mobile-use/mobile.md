# Mobile API Reference

## Overview

The Mobile module provides comprehensive mobile device UI automation and configuration capabilities within a session in the AgentBay cloud environment. This includes touch operations, UI element interactions, application management, screenshot capabilities, and mobile environment configuration operations.

## Result Classes

### BoolResult

```java
public class BoolResult extends ApiResponse
```

Result of boolean operations (tap, swipe, input, etc.).

**Fields:**
- `success` (boolean): True if the operation succeeded
- `data` (Boolean): Operation result (true/false)
- `requestId` (String): Unique identifier for this API request
- `errorMessage` (String): Error description (if success is false)

### UIElementListResult

```java
public class UIElementListResult extends ApiResponse
```

Result of UI element listing operations.

**Fields:**
- `success` (boolean): True if the operation succeeded
- `elements` (List<Map<String, Object>>): List of UI elements
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

Represents an installed mobile application.

**Fields:**
- `name` (String): Application name
- `startCmd` (String): Command to start the application
- `stopCmd` (String): Command to stop the application (optional)
- `workDirectory` (String): Working directory (optional)

### ProcessListResult

```java
public class ProcessListResult extends ApiResponse
```

Result of application start operations.

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

### OperationResult

```java
public class OperationResult extends ApiResponse
```

Generic operation result (used for screenshot, etc.).

**Fields:**
- `success` (boolean): True if the operation succeeded
- `data` (Object): Operation result data
- `requestId` (String): Unique identifier for this API request
- `errorMessage` (String): Error description (if success is false)

### AdbUrlResult

```java
public class AdbUrlResult extends ApiResponse
```

Result of getting ADB connection URL.

**Fields:**
- `success` (boolean): True if the operation succeeded
- `data` (String): ADB connection URL (format: "adb connect <IP>:<Port>")
- `requestId` (String): Unique identifier for this API request
- `errorMessage` (String): Error description (if success is false)

## Mobile

```java
public class Mobile extends BaseService
```

Handles mobile UI automation operations and configuration in the AgentBay cloud environment.

---

## Touch Operations

### tap

```java
public BoolResult tap(int x, int y)
```

Taps on the mobile screen at the specified coordinates.

**Parameters:**
- `x` (int): X coordinate in pixels
- `y` (int): Y coordinate in pixels

**Returns:**
- `BoolResult`: Object with success status and error message if any

**Example:**

```java
Session session = agentBay.create(
    new CreateSessionParams().setImageId("mobile_latest")
).getSession();

BoolResult result = session.getMobile().tap(500, 800);
if (result.isSuccess()) {
    System.out.println("Tap successful");
} else {
    System.err.println("Tap failed: " + result.getErrorMessage());
}
```

### swipe

```java
public BoolResult swipe(int startX, int startY, int endX, int endY, int durationMs)
public BoolResult swipe(int startX, int startY, int endX, int endY)
```

Performs a swipe gesture from one point to another.

**Parameters:**
- `startX` (int): Starting X coordinate
- `startY` (int): Starting Y coordinate
- `endX` (int): Ending X coordinate
- `endY` (int): Ending Y coordinate
- `durationMs` (int, optional): Duration of the swipe in milliseconds. Defaults to 300

**Returns:**
- `BoolResult`: Result object containing success status and error message if any

**Example:**

```java
// Swipe down with custom duration
BoolResult result = session.getMobile().swipe(500, 1000, 500, 500, 500);

// Swipe down with default duration (300ms)
BoolResult result = session.getMobile().swipe(500, 1000, 500, 500);
```

### inputText

```java
public BoolResult inputText(String text)
```

Inputs text into the active field.

**Parameters:**
- `text` (String): The text to input

**Returns:**
- `BoolResult`: Result object containing success status and error message if any

**Example:**

```java
BoolResult result = session.getMobile().inputText("Hello Mobile!");
if (result.isSuccess()) {
    System.out.println("Text input successful");
}
```

### sendKey

```java
public BoolResult sendKey(int key)
```

Sends a key press event.

**Parameters:**
- `key` (int): The key code to send. Supported key codes:
  - `KeyCode.HOME` (3): Home button
  - `KeyCode.BACK` (4): Back button
  - `KeyCode.VOLUME_UP` (24): Volume up
  - `KeyCode.VOLUME_DOWN` (25): Volume down
  - `KeyCode.POWER` (26): Power button
  - `KeyCode.MENU` (82): Menu button

**Returns:**
- `BoolResult`: Result object containing success status and error message if any

**Example:**

```java
import com.aliyun.agentbay.mobile.KeyCode;

// Press HOME button
BoolResult result = session.getMobile().sendKey(KeyCode.HOME);

// Press BACK button
result = session.getMobile().sendKey(KeyCode.BACK);
```

---

## UI Element Operations

### getClickableUiElements

```java
public UIElementListResult getClickableUiElements(int timeoutMs)
public UIElementListResult getClickableUiElements()
```

Retrieves all clickable UI elements within the specified timeout.

**Parameters:**
- `timeoutMs` (int, optional): Timeout in milliseconds. Defaults to 2000

**Returns:**
- `UIElementListResult`: Result object containing clickable UI elements and error message if any

**Example:**

```java
UIElementListResult result = session.getMobile().getClickableUiElements();
if (result.isSuccess()) {
    List<Map<String, Object>> elements = result.getElements();
    System.out.println("Found " + elements.size() + " clickable elements");
    for (Map<String, Object> element : elements) {
        System.out.println("Element: " + element);
    }
}
```

### getAllUiElements

```java
public UIElementListResult getAllUiElements(int timeoutMs)
public UIElementListResult getAllUiElements()
```

Retrieves all UI elements within the specified timeout.

**Parameters:**
- `timeoutMs` (int, optional): Timeout in milliseconds. Defaults to 2000

**Returns:**
- `UIElementListResult`: Result object containing UI elements and error message if any

**Example:**

```java
UIElementListResult result = session.getMobile().getAllUiElements(3000);
if (result.isSuccess()) {
    System.out.println("Found " + result.getElements().size() + " UI elements");
}
```

---

## Application Management Operations

### getInstalledApps

```java
public InstalledAppListResult getInstalledApps(boolean startMenu, boolean desktop, boolean ignoreSystemApps)
```

Retrieves a list of installed applications.

**Parameters:**
- `startMenu` (boolean): Whether to include start menu applications
- `desktop` (boolean): Whether to include desktop applications
- `ignoreSystemApps` (boolean): Whether to ignore system applications

**Returns:**
- `InstalledAppListResult`: The result containing the list of installed applications

**Example:**

```java
InstalledAppListResult result = session.getMobile().getInstalledApps(
    true,   // startMenu
    false,  // desktop
    true    // ignoreSystemApps
);

if (result.isSuccess()) {
    for (InstalledApp app : result.getData()) {
        System.out.println("App: " + app.getName());
        System.out.println("  Start command: " + app.getStartCmd());
    }
}
```

### startApp

```java
public ProcessListResult startApp(String startCmd)
public ProcessListResult startApp(String startCmd, String workDirectory)
public ProcessListResult startApp(String startCmd, String workDirectory, String activity)
```

Starts an application with the given command, optional working directory, and optional activity.

**Parameters:**
- `startCmd` (String): The command to start the application
- `workDirectory` (String, optional): The working directory for the application
- `activity` (String, optional): Activity name to launch (e.g., ".SettingsActivity" or "com.package/.Activity")

**Returns:**
- `ProcessListResult`: The result containing the list of processes started

**Example:**

```java
// Start Settings app
ProcessListResult result = session.getMobile().startApp(
    "monkey -p com.android.settings -c android.intent.category.LAUNCHER 1"
);

// Start app with specific activity
result = session.getMobile().startApp(
    "am start -n com.android.settings/.Settings",
    "",
    ".Settings"
);
```

### stopAppByCmd

```java
public AppOperationResult stopAppByCmd(String stopCmd)
```

Stops an application by stop command.

**Parameters:**
- `stopCmd` (String): The command to stop the application

**Returns:**
- `AppOperationResult`: The result of the operation

**Example:**

```java
AppOperationResult result = session.getMobile().stopAppByCmd(
    "am force-stop com.android.settings"
);
if (result.isSuccess()) {
    System.out.println("App stopped successfully");
}
```

---

## Screenshot Operations

### screenshot

```java
public OperationResult screenshot()
```

Takes a screenshot of the current screen.

**Returns:**
- `OperationResult`: Result object containing the path to the screenshot and error message if any

**Example:**

```java
OperationResult result = session.getMobile().screenshot();
if (result.isSuccess()) {
    String screenshotUrl = (String) result.getData();
    System.out.println("Screenshot saved at: " + screenshotUrl);
}
```

---

## Mobile Configuration Operations

### configure

```java
public void configure(MobileExtraConfig mobileConfig)
```

Configure mobile settings from MobileExtraConfig.

This method is typically called automatically during session creation when MobileExtraConfig is provided in CreateSessionParams. It can also be called manually to reconfigure mobile settings during a session.

**Parameters:**
- `mobileConfig` (MobileExtraConfig): Mobile configuration object with settings for:
  - `lockResolution` (boolean): Whether to lock device resolution
  - `appManagerRule` (AppManagerRule): App whitelist/blacklist rules
  - `hideNavigationBar` (boolean): Whether to hide navigation bar
  - `uninstallBlacklist` (List<String>): Apps protected from uninstallation

**Example:**

```java
MobileExtraConfig config = new MobileExtraConfig();
config.setLockResolution(true);

session.getMobile().configure(config);
```

**Note:**
- This method is called automatically during session creation if MobileExtraConfig is provided
- Configuration changes are applied immediately
- Resolution lock prevents resolution changes
- App whitelist/blacklist affects app launching permissions
- Uninstall blacklist protects apps from being uninstalled

### setResolutionLock

```java
public void setResolutionLock(boolean enable)
```

Set display resolution lock for mobile devices.

**Parameters:**
- `enable` (boolean): True to enable, False to disable

**Example:**

```java
session.getMobile().setResolutionLock(true);  // Enable resolution lock
session.getMobile().setResolutionLock(false); // Disable resolution lock
```

### setAppWhitelist

```java
public void setAppWhitelist(List<String> packageNames)
```

Set application whitelist.

**Parameters:**
- `packageNames` (List<String>): List of Android package names to whitelist

**Example:**

```java
List<String> whitelist = Arrays.asList(
    "com.android.settings",
    "com.android.chrome"
);
session.getMobile().setAppWhitelist(whitelist);
```

**Notes:**
- Only apps in the whitelist will be allowed to run
- System apps may be affected depending on the configuration
- Whitelist takes precedence over blacklist if both are set

### setAppBlacklist

```java
public void setAppBlacklist(List<String> packageNames)
```

Set application blacklist.

**Parameters:**
- `packageNames` (List<String>): List of Android package names to blacklist

**Example:**

```java
List<String> blacklist = Arrays.asList(
    "com.example.app1",
    "com.example.app2"
);
session.getMobile().setAppBlacklist(blacklist);
```

**Notes:**
- Apps in the blacklist will be blocked from running
- Whitelist takes precedence over blacklist if both are set

### setNavigationBarVisibility

```java
public void setNavigationBarVisibility(boolean hide)
```

Set navigation bar visibility for mobile devices.

**Parameters:**
- `hide` (boolean): True to hide navigation bar, False to show navigation bar

**Example:**

```java
session.getMobile().setNavigationBarVisibility(true);  // Hide navigation bar
session.getMobile().setNavigationBarVisibility(false); // Show navigation bar
```

**Notes:**
- Hiding the navigation bar provides a fullscreen experience
- The navigation bar can still be accessed by swiping from the edge

### setUninstallBlacklist

```java
public void setUninstallBlacklist(List<String> packageNames)
```

Set uninstall protection blacklist for mobile devices.

**Parameters:**
- `packageNames` (List<String>): List of Android package names to protect from uninstallation

**Example:**

```java
List<String> protectedApps = Arrays.asList(
    "com.android.settings",
    "com.android.chrome"
);
session.getMobile().setUninstallBlacklist(protectedApps);
```

**Notes:**
- Apps in the uninstall blacklist cannot be uninstalled
- This is useful for protecting critical applications
- The protection persists for the session lifetime

---

## ADB Operations

### getAdbUrl

```java
public AdbUrlResult getAdbUrl(String adbkeyPub)
```

Retrieves the ADB connection URL for the mobile environment.

This method is only supported in mobile environments (mobile_latest image). It uses the provided ADB public key to establish the connection and returns the ADB connect URL.

**Parameters:**
- `adbkeyPub` (String): The ADB public key for connection authentication

**Returns:**
- `AdbUrlResult`: Result object containing the ADB connection URL (format: "adb connect <IP>:<Port>") and request ID. Returns error if not in mobile environment

**Throws:**
- `SessionError`: If the session is not in mobile environment

**Example:**

```java
String adbkeyPub = "your_adb_public_key_content_here";

AdbUrlResult result = session.getMobile().getAdbUrl(adbkeyPub);
if (result.isSuccess()) {
    String adbUrl = result.getData();
    System.out.println("ADB Connection URL: " + adbUrl);
    System.out.println("You can now connect using: " + adbUrl);
} else {
    System.err.println("Failed to get ADB URL: " + result.getErrorMessage());
}
```

---

## KeyCode Constants

The `KeyCode` class provides constants for common Android key codes:

```java
public class KeyCode {
    public static final int HOME = 3;
    public static final int BACK = 4;
    public static final int VOLUME_UP = 24;
    public static final int VOLUME_DOWN = 25;
    public static final int POWER = 26;
    public static final int MENU = 82;
}
```

---

## Complete Example

Here's a comprehensive example demonstrating various mobile operations:

```java
import com.aliyun.agentbay.AgentBay;
import com.aliyun.agentbay.model.*;
import com.aliyun.agentbay.session.CreateSessionParams;
import com.aliyun.agentbay.session.Session;
import com.aliyun.agentbay.mobile.KeyCode;

public class MobileExample {
    public static void main(String[] args) {
        String apiKey = System.getenv("AGENTBAY_API_KEY");
        Session session = null;
        
        try {
            AgentBay agentBay = new AgentBay(apiKey);
            
            // Create mobile session
            System.out.println("Creating mobile session...");
            CreateSessionParams params = new CreateSessionParams();
            params.setImageId("mobile_latest");
            
            SessionResult sessionResult = agentBay.create(params);
            session = sessionResult.getSession();
            System.out.println("Session ID: " + session.getSessionId());
            
            // 1. Get installed apps
            System.out.println("\n1. Getting installed apps...");
            InstalledAppListResult appsResult = session.getMobile()
                .getInstalledApps(true, false, true);
            if (appsResult.isSuccess()) {
                System.out.println("Found " + appsResult.getData().size() + " apps");
            }
            
            // 2. Start an application
            System.out.println("\n2. Starting Settings app...");
            ProcessListResult startResult = session.getMobile().startApp(
                "monkey -p com.android.settings -c android.intent.category.LAUNCHER 1"
            );
            System.out.println("App started: " + startResult.isSuccess());
            
            // 3. Perform touch operations
            System.out.println("\n3. Performing tap...");
            BoolResult tapResult = session.getMobile().tap(500, 800);
            System.out.println("Tap successful: " + tapResult.isSuccess());
            
            // 4. Swipe gesture
            System.out.println("\n4. Performing swipe...");
            BoolResult swipeResult = session.getMobile().swipe(500, 1000, 500, 500);
            System.out.println("Swipe successful: " + swipeResult.isSuccess());
            
            // 5. Input text
            System.out.println("\n5. Inputting text...");
            BoolResult inputResult = session.getMobile().inputText("Hello Mobile!");
            System.out.println("Text input successful: " + inputResult.isSuccess());
            
            // 6. Send key event
            System.out.println("\n6. Sending HOME key...");
            BoolResult keyResult = session.getMobile().sendKey(KeyCode.HOME);
            System.out.println("Key sent: " + keyResult.isSuccess());
            
            // 7. Take screenshot
            System.out.println("\n7. Taking screenshot...");
            OperationResult screenshotResult = session.getMobile().screenshot();
            if (screenshotResult.isSuccess()) {
                System.out.println("Screenshot URL: " + screenshotResult.getData());
            }
            
            // 8. Get UI elements
            System.out.println("\n8. Getting clickable UI elements...");
            UIElementListResult elementsResult = session.getMobile()
                .getClickableUiElements();
            if (elementsResult.isSuccess()) {
                System.out.println("Found " + elementsResult.getElements().size() 
                    + " clickable elements");
            }
            
            // 9. Stop application
            System.out.println("\n9. Stopping Settings app...");
            AppOperationResult stopResult = session.getMobile()
                .stopAppByCmd("am force-stop com.android.settings");
            System.out.println("App stopped: " + stopResult.isSuccess());
            
            System.out.println("\n=== Example completed successfully ===");
            
        } catch (Exception e) {
            System.err.println("Error: " + e.getMessage());
            e.printStackTrace();
        } finally {
            if (session != null) {
                try {
                    agentBay.delete(session);
                    System.out.println("\nSession closed");
                } catch (Exception e) {
                    System.err.println("Error closing session: " + e.getMessage());
                }
            }
        }
    }
}
```

---

## See Also

- [MobileSimulate API](./mobile-simulate.md) - Mobile device simulation capabilities
- [Session Management](../common-features/basics/session.md) - Session lifecycle management
- [Command Execution](../common-features/basics/command.md) - Execute shell commands on mobile devices
