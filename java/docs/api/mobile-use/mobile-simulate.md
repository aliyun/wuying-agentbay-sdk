# MobileSimulate API Reference

## Overview

The MobileSimulate module provides capabilities for managing persistent mobile device information and syncing it to mobile devices. This allows you to simulate specific mobile device characteristics and maintain consistent device profiles across sessions.

## Enums

### MobileSimulateMode

```java
public enum MobileSimulateMode
```

Defines the simulation mode for mobile device characteristics.

**Values:**
- `PROPERTIES_ONLY`: Only simulate device properties (default)
- `SENSORS_ONLY`: Only simulate sensor data
- `PACKAGES_ONLY`: Only simulate installed packages
- `SERVICES_ONLY`: Only simulate system services
- `ALL`: Simulate all aspects

**Methods:**
- `String getValue()`: Get the string value of the mode

**Example:**

```java
MobileSimulateMode mode = MobileSimulateMode.ALL;
System.out.println(mode.getValue()); // Output: "All"
```

## Result Classes

### MobileSimulateUploadResult

```java
public class MobileSimulateUploadResult
```

Result of uploading mobile simulation data.

**Fields:**
- `success` (boolean): True if the upload succeeded
- `mobileSimulateContextId` (String): The context ID of the uploaded mobile simulation data
- `errorMessage` (String): Error description (if success is false)

**Constructor:**

```java
public MobileSimulateUploadResult(
    boolean success,
    String mobileSimulateContextId,
    String errorMessage
)
```

## Configuration Classes

### MobileSimulateConfig

```java
public class MobileSimulateConfig
```

Configuration for mobile device simulation.

**Fields:**
- `simulate` (boolean): Whether simulation is enabled
- `mobileDevInfoPath` (String): Path to mobile device info file
- `simulateMode` (MobileSimulateMode): The simulation mode
- `simulatedContextId` (String): The context ID containing simulation data

**Constructor:**

```java
public MobileSimulateConfig(
    boolean simulate,
    String mobileDevInfoPath,
    MobileSimulateMode simulateMode,
    String simulatedContextId
)
```

**Methods:**
- `boolean isSimulate()`: Check if simulation is enabled
- `String getMobileDevInfoPath()`: Get the mobile device info path
- `MobileSimulateMode getSimulateMode()`: Get the simulation mode
- `String getSimulatedContextId()`: Get the simulated context ID

## MobileSimulate

```java
public class MobileSimulate
```

Service for managing persistent mobile device info and syncing to mobile devices.

### Constructor

```java
public MobileSimulate(AgentBay agentBay)
```

Creates a new MobileSimulate instance.

**Parameters:**
- `agentBay` (AgentBay): The AgentBay client instance (required)

**Throws:**
- `IllegalArgumentException`: If agentBay or agentBay.context is null

---

## Configuration Methods

### setSimulateEnable

```java
public void setSimulateEnable(boolean enable)
```

Enable or disable mobile device simulation.

**Parameters:**
- `enable` (boolean): True to enable simulation, false to disable

**Example:**

```java
MobileSimulate mobileSimulate = new MobileSimulate(agentBay);
mobileSimulate.setSimulateEnable(true);
```

### getSimulateEnable

```java
public boolean getSimulateEnable()
```

Get the current simulation enable status.

**Returns:**
- `boolean`: True if simulation is enabled

**Example:**

```java
boolean isEnabled = mobileSimulate.getSimulateEnable();
System.out.println("Simulation enabled: " + isEnabled);
```

### setSimulateMode

```java
public void setSimulateMode(MobileSimulateMode mode)
```

Set the simulation mode.

**Parameters:**
- `mode` (MobileSimulateMode): The simulation mode to use

**Example:**

```java
mobileSimulate.setSimulateMode(MobileSimulateMode.ALL);
```

### getSimulateMode

```java
public MobileSimulateMode getSimulateMode()
```

Get the current simulation mode.

**Returns:**
- `MobileSimulateMode`: The current simulation mode

**Example:**

```java
MobileSimulateMode mode = mobileSimulate.getSimulateMode();
System.out.println("Current mode: " + mode.getValue());
```

### setSimulateContextId

```java
public void setSimulateContextId(String contextId)
```

Set a previously saved simulate context ID.

This allows you to reuse mobile device simulation data from a previous upload.

**Parameters:**
- `contextId` (String): The context ID of the previously saved mobile simulate context

**Example:**

```java
// Use a previously uploaded simulation context
String previousContextId = "ctx_abc123...";
mobileSimulate.setSimulateContextId(previousContextId);
```

### getSimulateContextId

```java
public String getSimulateContextId()
```

Get the simulate context ID.

**Returns:**
- `String`: The context ID of the mobile simulate context

**Example:**

```java
String contextId = mobileSimulate.getSimulateContextId();
System.out.println("Context ID: " + contextId);
```

### getSimulateConfig

```java
public MobileSimulateConfig getSimulateConfig()
```

Get the complete simulation configuration.

**Returns:**
- `MobileSimulateConfig`: The current simulation configuration

**Example:**

```java
MobileSimulateConfig config = mobileSimulate.getSimulateConfig();
System.out.println("Simulation enabled: " + config.isSimulate());
System.out.println("Simulation mode: " + config.getSimulateMode().getValue());
```

---

## Mobile Info Management

### hasMobileInfo

```java
public boolean hasMobileInfo(ContextSync contextSync)
```

Check if the mobile device info file exists in a context sync.

**Parameters:**
- `contextSync` (ContextSync): The context sync to check (required)

**Returns:**
- `boolean`: True if the mobile device info file exists, false otherwise

**Throws:**
- `IllegalArgumentException`: If contextSync, contextId, or path is null

**Example:**

```java
ContextSync contextSync = new ContextSync();
contextSync.setContextId("ctx_123");
contextSync.setPath("/data");

boolean exists = mobileSimulate.hasMobileInfo(contextSync);
System.out.println("Mobile info exists: " + exists);
```

### uploadMobileInfo

```java
public MobileSimulateUploadResult uploadMobileInfo(String mobileDevInfo)
```

Upload mobile device info to create a simulation context.

This method:
1. Creates a new context for storing mobile simulation data
2. Uploads the provided mobile device information as JSON
3. Returns the context ID that can be reused in future sessions

**Parameters:**
- `mobileDevInfo` (String): The mobile device information as a JSON string (required)

**Returns:**
- `MobileSimulateUploadResult`: Upload result containing the context ID

**Throws:**
- `IllegalArgumentException`: If mobileDevInfo is null or empty

**Example:**

```java
// Prepare mobile device info JSON
String mobileDevInfo = "{" +
    "\"device\": {" +
    "  \"brand\": \"Samsung\"," +
    "  \"model\": \"Galaxy S21\"," +
    "  \"android_version\": \"12\"," +
    "  \"screen\": {" +
    "    \"width\": 1080," +
    "    \"height\": 2400," +
    "    \"density\": 3.0" +
    "  }" +
    "}," +
    "\"build\": {" +
    "  \"manufacturer\": \"Samsung\"," +
    "  \"product\": \"beyond1\"," +
    "  \"fingerprint\": \"samsung/beyond1/beyond1:12/..\"" +
    "}" +
    "}";

MobileSimulateUploadResult result = mobileSimulate.uploadMobileInfo(mobileDevInfo);
if (result.isSuccess()) {
    String contextId = result.getMobileSimulateContextId();
    System.out.println("Upload successful! Context ID: " + contextId);
    
    // Save this contextId for future use
    // You can reuse it with setSimulateContextId()
} else {
    System.err.println("Upload failed: " + result.getErrorMessage());
}
```

**Mobile Device Info JSON Structure:**

The mobile device info JSON should contain device characteristics you want to simulate:

```json
{
  "device": {
    "brand": "Device brand name",
    "model": "Device model",
    "android_version": "Android version",
    "screen": {
      "width": 1080,
      "height": 2400,
      "density": 3.0
    }
  },
  "build": {
    "manufacturer": "Manufacturer name",
    "product": "Product name",
    "fingerprint": "Build fingerprint"
  },
  "properties": {
    "ro.build.version.sdk": "31",
    "ro.product.cpu.abi": "arm64-v8a"
  },
  "sensors": [...],
  "packages": [...],
  "services": [...]
}
```

---

## Complete Example: Upload and Reuse Simulation Data

```java
import com.aliyun.agentbay.AgentBay;
import com.aliyun.agentbay.mobile.MobileSimulate;
import com.aliyun.agentbay.mobile.MobileSimulateMode;
import com.aliyun.agentbay.mobile.MobileSimulateUploadResult;
import com.aliyun.agentbay.session.CreateSessionParams;
import com.aliyun.agentbay.session.Session;

public class MobileSimulateExample {
    public static void main(String[] args) {
        String apiKey = System.getenv("AGENTBAY_API_KEY");
        
        try {
            AgentBay agentBay = new AgentBay(apiKey);
            MobileSimulate mobileSimulate = new MobileSimulate(agentBay);
            
            // Step 1: Configure simulation settings
            System.out.println("1. Configuring simulation...");
            mobileSimulate.setSimulateEnable(true);
            mobileSimulate.setSimulateMode(MobileSimulateMode.ALL);
            
            // Step 2: Upload mobile device info
            System.out.println("\n2. Uploading mobile device info...");
            String mobileDevInfo = "{" +
                "\"device\": {" +
                "  \"brand\": \"Samsung\"," +
                "  \"model\": \"Galaxy S21\"," +
                "  \"android_version\": \"12\"" +
                "}" +
                "}";
            
            MobileSimulateUploadResult uploadResult = 
                mobileSimulate.uploadMobileInfo(mobileDevInfo);
            
            if (!uploadResult.isSuccess()) {
                System.err.println("Upload failed: " + uploadResult.getErrorMessage());
                return;
            }
            
            String contextId = uploadResult.getMobileSimulateContextId();
            System.out.println("Upload successful! Context ID: " + contextId);
            System.out.println("Save this context ID for future use!");
            
            // Step 3: Create session with simulation
            System.out.println("\n3. Creating mobile session with simulation...");
            mobileSimulate.setSimulateContextId(contextId);
            
            CreateSessionParams params = new CreateSessionParams();
            params.setImageId("mobile_latest");
            params.setMobileSimulateConfig(mobileSimulate.getSimulateConfig());
            
            Session session = agentBay.create(params).getSession();
            System.out.println("Session created: " + session.getSessionId());
            System.out.println("The mobile device is now simulating Samsung Galaxy S21!");
            
            // Use the session for mobile operations...
            // session.getMobile().tap(100, 200);
            
            // Cleanup
            agentBay.delete(session);
            System.out.println("\n=== Example completed ===");
            
        } catch (Exception e) {
            System.err.println("Error: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
```

---

## Example: Reuse Previously Uploaded Simulation Data

```java
import com.aliyun.agentbay.AgentBay;
import com.aliyun.agentbay.mobile.MobileSimulate;
import com.aliyun.agentbay.mobile.MobileSimulateMode;
import com.aliyun.agentbay.session.CreateSessionParams;
import com.aliyun.agentbay.session.Session;

public class ReuseSimulationExample {
    public static void main(String[] args) {
        String apiKey = System.getenv("AGENTBAY_API_KEY");
        
        // Context ID from previous upload (save this in your database or config)
        String previousContextId = "ctx_abc123def456...";
        
        try {
            AgentBay agentBay = new AgentBay(apiKey);
            MobileSimulate mobileSimulate = new MobileSimulate(agentBay);
            
            // Configure simulation using previously uploaded context
            System.out.println("Reusing simulation context: " + previousContextId);
            mobileSimulate.setSimulateEnable(true);
            mobileSimulate.setSimulateMode(MobileSimulateMode.ALL);
            mobileSimulate.setSimulateContextId(previousContextId);
            
            // Create session with the reused simulation
            CreateSessionParams params = new CreateSessionParams();
            params.setImageId("mobile_latest");
            params.setMobileSimulateConfig(mobileSimulate.getSimulateConfig());
            
            Session session = agentBay.create(params).getSession();
            System.out.println("Session created with simulated device!");
            
            // Use the session...
            
            // Cleanup
            agentBay.delete(session);
            
        } catch (Exception e) {
            System.err.println("Error: " + e.getMessage());
        }
    }
}
```

---

## Integration with Session Creation

You can provide `MobileSimulateConfig` when creating a session:

```java
import com.aliyun.agentbay.mobile.MobileExtraConfig;

// Option 1: Using MobileSimulateConfig directly in CreateSessionParams
CreateSessionParams params = new CreateSessionParams();
params.setImageId("mobile_latest");
params.setMobileSimulateConfig(mobileSimulate.getSimulateConfig());

Session session = agentBay.create(params).getSession();

// Option 2: Using MobileExtraConfig for additional mobile settings
MobileExtraConfig extraConfig = new MobileExtraConfig();
extraConfig.setLockResolution(true);
extraConfig.setHideNavigationBar(true);

params.setMobileExtraConfig(extraConfig);
params.setMobileSimulateConfig(mobileSimulate.getSimulateConfig());

session = agentBay.create(params).getSession();
```

---

## Best Practices

### 1. Save and Reuse Context IDs

```java
// Upload once
MobileSimulateUploadResult result = mobileSimulate.uploadMobileInfo(deviceInfo);
String contextId = result.getMobileSimulateContextId();

// Save this contextId in database or configuration
saveToDatabase("device_profile_samsung_s21", contextId);

// Later, reuse it
String savedContextId = loadFromDatabase("device_profile_samsung_s21");
mobileSimulate.setSimulateContextId(savedContextId);
```

### 2. Create Device Profiles

```java
public class DeviceProfiles {
    public static final String SAMSUNG_S21 = "ctx_samsung_s21_...";
    public static final String IPHONE_13 = "ctx_iphone_13_...";
    public static final String PIXEL_6 = "ctx_pixel_6_...";
    
    public static MobileSimulate createWithProfile(
        AgentBay agentBay, 
        String profileContextId
    ) {
        MobileSimulate ms = new MobileSimulate(agentBay);
        ms.setSimulateEnable(true);
        ms.setSimulateMode(MobileSimulateMode.ALL);
        ms.setSimulateContextId(profileContextId);
        return ms;
    }
}

// Usage
MobileSimulate ms = DeviceProfiles.createWithProfile(
    agentBay, 
    DeviceProfiles.SAMSUNG_S21
);
```

### 3. Validate Mobile Info Before Upload

```java
import com.fasterxml.jackson.databind.ObjectMapper;

public void validateAndUpload(String mobileDevInfo) {
    ObjectMapper mapper = new ObjectMapper();
    try {
        // Validate JSON
        mapper.readTree(mobileDevInfo);
        
        // Upload
        MobileSimulateUploadResult result = 
            mobileSimulate.uploadMobileInfo(mobileDevInfo);
        
        if (result.isSuccess()) {
            System.out.println("Context ID: " + 
                result.getMobileSimulateContextId());
        }
    } catch (Exception e) {
        System.err.println("Invalid JSON: " + e.getMessage());
    }
}
```

---

## See Also

- [Mobile API](./mobile.md) - Mobile device UI automation and operations
- [Context Management](../common-features/basics/context.md) - Context storage and retrieval
- [Context Synchronization](../common-features/basics/context-sync.md) - Context sync operations
- [Session Management](../common-features/basics/session.md) - Session lifecycle management
