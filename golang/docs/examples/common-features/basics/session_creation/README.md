# Session Creation and Management Example

This example demonstrates comprehensive session creation and management using the Wuying AgentBay SDK. It covers various session types and configurations:

## Features Demonstrated

### 1. Basic Session Management
- Initializing the AgentBay client
- Creating a session with default parameters
- Listing all available sessions
- Creating multiple sessions
- Deleting sessions
- Verifying session deletion

### 2. Session with Labels
- Creating sessions with custom labels for organization
- Using labels for project management and environment tracking
- Retrieving and displaying session labels

### 3. Advanced Mobile Configuration Options

The example demonstrates comprehensive mobile session configuration using `MobileExtraConfig`. The following parameters are supported:

#### Core Configuration Parameters

- **`LockResolution`** (bool): Controls screen resolution behavior
  - `true`: Locks display resolution to prevent changes during session
  - `false`: Allows flexible resolution adjustments for different device types

- **`HideNavigationBar`** (bool): Controls system navigation bar visibility
  - `true`: Hides navigation bar for immersive full-screen experience
  - `false`: Shows navigation bar (default system behavior)

- **`UninstallBlacklist`** ([]string): List of package names protected from uninstallation
  - Prevents accidental or malicious removal of critical applications
  - Essential for system stability and security compliance
  - Example: `["com.android.systemui", "com.android.settings", "com.google.android.gms"]`

- **`AppManagerRule`** (*AppManagerRule): Application access control rules
  - **`RuleType`** (string): Either "White" (whitelist) or "Black" (blacklist)
  - **`AppPackageNameList`** ([]string): List of package names to allow or block

#### Configuration Examples

The example includes two configuration scenarios:

1. **Whitelist Mode**: Secure configuration with locked resolution, hidden navigation bar, and strict app control
2. **Blacklist Mode**: Flexible configuration with visible navigation bar and selective app blocking

#### JSON Structure

```json
{
  "mobile": {
    "lock_resolution": true,
    "hide_navigation_bar": true,
    "uninstall_blacklist": ["com.android.systemui", "com.android.settings"],
    "app_manager_rule": {
      "rule_type": "White",
      "app_package_name_list": ["com.allowed.app1", "com.allowed.app2"]
    }
  }
}

## Running the Example

```bash
cd session_creation
go run main.go
```

Make sure you have set the `AGENTBAY_API_KEY` environment variable or replace the placeholder in the code with your actual API key.
