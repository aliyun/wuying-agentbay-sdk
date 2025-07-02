# Mobile Application Management Example

This example demonstrates how to use the AgentBay SDK to interact with mobile applications on Android devices.

## Features Demonstrated

- Mobile Application Management:
  - Getting a list of installed mobile applications
  - Starting mobile applications with simple commands (monkey commands)
  - Starting mobile applications with specific activities
  - Stopping mobile applications by command (am force-stop)
  - Listing visible (running) mobile applications

- Mobile-Specific Operations:
  - Android package management commands
  - Activity-based application launching
  - Complete mobile application workflow demonstration

## Running the Example

Make sure you have set your AgentBay API key as an environment variable:

```bash
export AGENTBAY_API_KEY="your-api-key-here"
```

Then run the example:

```bash
npx ts-node application-mobile.ts
```

## Mobile Commands Used

The example demonstrates typical Android/mobile commands:

- **Start App**: `monkey -p com.autonavi.minimap -c android.intent.category.LAUNCHER 1`
- **Start App with Activity**: Using activity parameter like `com.xingin.outside.activity.VivoOutsideFeedActivity`
- **Stop App**: `am force-stop com.sankuai.meituan`

## Workflow Demonstrated

The example includes a complete mobile application workflow:

1. **Get Installed Apps**: Retrieve list of installed mobile applications
2. **Start Simple App**: Launch app using basic monkey command
3. **Start App with Activity**: Launch app with specific activity parameter
4. **Stop App**: Stop application using Android force-stop command

## Note

This example is specifically designed for mobile environments and requires a mobile session (`mobile_latest` image). The demonstrated functionality is Android-specific and includes error handling to deal with cases where certain mobile operations are not supported or when running in non-mobile environments.
