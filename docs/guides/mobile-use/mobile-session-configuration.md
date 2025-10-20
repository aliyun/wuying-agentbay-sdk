# Mobile Session Configuration

This guide demonstrates how to create mobile sessions with advanced configuration options using the AgentBay SDK. The mobile configuration allows you to control application access and screen resolution settings for mobile environments.

## Table of Contents
- [Overview](#overview)
- [Configuration Options](#configuration-options)
- [Navigation Bar Control](#navigation-bar-control)
- [Uninstall Protection](#uninstall-protection)
- [Whitelist Configuration](#whitelist-configuration)
- [Blacklist Configuration](#blacklist-configuration)
- [Advanced Configuration Examples](#advanced-configuration-examples)

## Overview

When creating mobile sessions, you can configure advanced settings using the `extra_configs` parameter in `CreateSessionParams`. This allows you to:

- Control application access through whitelist or blacklist rules
- Lock or unlock screen resolution
- Hide or show the system navigation bar
- Protect critical applications from uninstallation
- Enhance security and testing flexibility

## Configuration Options

The mobile configuration supports the following options:

### Resolution Settings

- **`lock_resolution`** (bool): Controls whether the screen resolution is locked
  - `True`: Locks the resolution to prevent changes
  - `False`: Allows resolution changes for flexible display adaptation

### Navigation Bar Control

- **`hide_navigation_bar`** (bool): Controls the visibility of the system navigation bar
  - `True`: Hides the navigation bar for immersive full-screen experience
  - `False`: Shows the navigation bar (default system behavior)

### Uninstall Protection

- **`uninstall_blacklist`** (list): A list of package names protected from uninstallation
  - Prevents accidental or malicious removal of critical applications
  - Commonly used to protect system apps, security tools, and essential services

### App Manager Rule

- **`app_manager_rule`** (AppManagerRule): Controls application access
  - **`rule_type`**: Either "White" (whitelist) or "Black" (blacklist)
  - **`app_package_name_list`**: List of package names to allow or block

## Navigation Bar Control

The navigation bar control feature allows you to create immersive mobile experiences by hiding the system navigation bar. This is particularly useful for:

- **Kiosk Applications**: Creating dedicated-purpose applications without system navigation
- **Immersive Gaming**: Full-screen gaming experiences without distractions
- **UI Testing**: Testing applications in full-screen mode
- **Digital Signage**: Creating clean, distraction-free displays

### Example: Hiding Navigation Bar

```python
from agentbay import AgentBay
from agentbay.session_params import CreateSessionParams
from agentbay.api.models import ExtraConfigs, MobileExtraConfig

# Initialize the SDK
agent_bay = AgentBay(api_key="your_api_key")

# Configure mobile settings with hidden navigation bar
mobile_config = MobileExtraConfig(
    lock_resolution=True,
    hide_navigation_bar=True  # Hide navigation bar for immersive experience
)

# Create extra configs
extra_configs = ExtraConfigs(mobile=mobile_config)

# Create session with immersive configuration
params = CreateSessionParams(
    image_id="mobile_latest",
    labels={"project": "immersive-ui", "mode": "kiosk"},
    extra_configs=extra_configs
)

session_result = agent_bay.create(params)
if session_result.success:
    session = session_result.session
    print(f"Immersive mobile session created with ID: {session.session_id}")
    print("Navigation bar hidden for full-screen experience")
```

## Uninstall Protection

The uninstall protection feature prevents critical applications from being accidentally or maliciously uninstalled. This is essential for:

- **System Stability**: Protecting essential system applications
- **Security**: Preventing removal of security and management tools
- **Compliance**: Ensuring required applications remain installed
- **Kiosk Mode**: Maintaining application integrity in public devices

### Example: Protecting Critical Applications

```python
from agentbay import AgentBay
from agentbay.session_params import CreateSessionParams
from agentbay.api.models import ExtraConfigs, MobileExtraConfig

# Initialize the SDK
agent_bay = AgentBay(api_key="your_api_key")

# Configure uninstall protection for critical apps
mobile_config = MobileExtraConfig(
    lock_resolution=True,
    uninstall_blacklist=[
        "com.android.systemui",        # System UI
        "com.android.settings",        # Settings app
        "com.google.android.gms",      # Google Play Services
        "com.company.security.app",    # Company security app
        "com.company.management.tool"  # Device management tool
    ]
)

# Create extra configs
extra_configs = ExtraConfigs(mobile=mobile_config)

# Create session with uninstall protection
params = CreateSessionParams(
    image_id="mobile_latest",
    labels={"project": "secure-deployment", "protection": "enabled"},
    extra_configs=extra_configs
)

session_result = agent_bay.create(params)
if session_result.success:
    session = session_result.session
    print(f"Protected mobile session created with ID: {session.session_id}")
    print("Critical applications protected from uninstallation")
```

## Whitelist Configuration

Use whitelists in production environments to ensure only approved applications can be installed and accessed. This provides the highest level of security by explicitly allowing only trusted applications.

### Example: Creating a Session with App Whitelist

```python
from agentbay import AgentBay
from agentbay.session_params import CreateSessionParams
from agentbay.api.models import ExtraConfigs, MobileExtraConfig, AppManagerRule

# Initialize the SDK
agent_bay = AgentBay(api_key="your_api_key")

# Configure mobile app management with whitelist
app_whitelist_rule = AppManagerRule(
    rule_type="White",
    app_package_name_list=[
        "com.example.allowed.app",
        "com.company.trusted.app",
        "com.system.essential.service"
    ]
)

# Configure mobile settings with comprehensive options
mobile_config = MobileExtraConfig(
    lock_resolution=True,
    hide_navigation_bar=True,  # Hide navigation bar for clean UI
    uninstall_blacklist=[      # Protect critical system apps
        "com.android.systemui",
        "com.android.settings",
        "com.google.android.gms"
    ],
    app_manager_rule=app_whitelist_rule
)

# Create extra configs
extra_configs = ExtraConfigs(mobile=mobile_config)

# Create session with mobile configuration
params = CreateSessionParams(
    image_id="mobile_latest",
    labels={"project": "mobile-testing", "environment": "development"},
    extra_configs=extra_configs
)

session_result = agent_bay.create(params)
if session_result.success:
    session = session_result.session
    print(f"Mobile session created with ID: {session.session_id}")
    print("Mobile configuration applied:")
    print("- Resolution locked")
    print("- App whitelist enabled with allowed packages")
else:
    print(f"Failed to create mobile session: {session_result.error_message}")
```

## Blacklist Configuration

Use blacklists in development and testing to block known problematic applications while allowing flexibility for other apps. This approach is useful when you want to prevent access to specific applications without restricting the entire environment.

### Example: Creating a Session with App Blacklist

```python
from agentbay import AgentBay
from agentbay.session_params import CreateSessionParams
from agentbay.api.models import ExtraConfigs, MobileExtraConfig, AppManagerRule

# Initialize the SDK
agent_bay = AgentBay(api_key="your_api_key")

# Configure mobile app management with blacklist
app_blacklist_rule = AppManagerRule(
    rule_type="Black",
    app_package_name_list=[
        "com.malware.suspicious.app",
        "com.unwanted.adware",
        "com.blocked.social.media"
    ]
)

# Configure mobile settings with resolution flexibility and security
mobile_config = MobileExtraConfig(
    lock_resolution=False,
    hide_navigation_bar=False,  # Keep navigation bar visible
    uninstall_blacklist=[       # Protect essential apps even in blacklist mode
        "com.android.systemui",
        "com.android.settings"
    ],
    app_manager_rule=app_blacklist_rule
)

# Create extra configs
extra_configs = ExtraConfigs(mobile=mobile_config)

# Create session with mobile blacklist configuration
params = CreateSessionParams(
    image_id="mobile_latest",
    labels={"project": "security-testing"},
    extra_configs=extra_configs
)

session_result = agent_bay.create(params)
if session_result.success:
    session = session_result.session
    print(f"Secure mobile session created with ID: {session.session_id}")
    print("Security configuration applied:")
    print("- Resolution unlocked for flexibility")
    print("- App blacklist enabled to block malicious packages")
else:
    print(f"Failed to create mobile session: {session_result.error_message}")
```

## Advanced Configuration Examples

### Comprehensive Mobile Configuration

This example demonstrates all available mobile configuration options working together:

```python
from agentbay import AgentBay
from agentbay.session_params import CreateSessionParams
from agentbay.api.models import ExtraConfigs, MobileExtraConfig, AppManagerRule

# Initialize the SDK
agent_bay = AgentBay(api_key="your_api_key")

# Create comprehensive app management rule
app_rule = AppManagerRule(
    rule_type="White",
    app_package_name_list=[
        "com.android.settings",
        "com.company.business.app",
        "com.trusted.productivity.suite"
    ]
)

# Configure all mobile options
mobile_config = MobileExtraConfig(
    lock_resolution=True,           # Lock resolution for consistent testing
    hide_navigation_bar=True,       # Hide navigation bar for immersive experience
    uninstall_blacklist=[           # Protect critical applications
        "com.android.systemui",     # System UI components
        "com.android.settings",     # Device settings
        "com.google.android.gms",   # Google Play Services
        "com.company.security.app", # Company security application
        "com.company.mdm.agent"     # Mobile device management agent
    ],
    app_manager_rule=app_rule       # Application access control
)

# Create extra configs
extra_configs = ExtraConfigs(mobile=mobile_config)

# Create session with comprehensive configuration
params = CreateSessionParams(
    image_id="mobile_latest",
    labels={
        "project": "enterprise-mobile",
        "config_type": "comprehensive",
        "security_level": "high",
        "ui_mode": "immersive"
    },
    extra_configs=extra_configs
)

session_result = agent_bay.create(params)
if session_result.success:
    session = session_result.session
    print(f"Comprehensive mobile session created with ID: {session.session_id}")
    print("Configuration applied:")
    print("✓ Resolution locked for consistent testing")
    print("✓ Navigation bar hidden for immersive experience")
    print("✓ Critical system apps protected from uninstallation")
    print("✓ App whitelist enforced for security")
else:
    print(f"Failed to create comprehensive session: {session_result.error_message}")
```

## Related Documentation

- [Mobile Application Management](./mobile-application-management.md)
- [Mobile UI Automation](./mobile-ui-automation.md)
- [Session Creation Basics](../common-features/basics/session-management.md)
