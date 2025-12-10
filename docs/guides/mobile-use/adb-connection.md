# ADB Connection Guide

This guide explains how to use the `getAdbUrl` method to connect to mobile sessions in AgentBay cloud environment via ADB (Android Debug Bridge).

## Overview

The `getAdbUrl` method provides an ADB connection URL that allows you to use standard ADB commands to interact with mobile sessions running in AgentBay cloud. This enables you to use ADB tools from your local machine to control and debug cloud-based mobile devices.

## Prerequisites

1. **Mobile Session**: A session created with a mobile environment image (e.g., `mobile_latest`)
2. **ADB Tool**: ADB installed on your local machine
3. **API Key**: Valid AgentBay API key

> **Note**: For ADB installation instructions, please refer to the [official Android documentation](https://developer.android.com/studio/command-line/adb).

## Usage Restrictions

⚠️ **Important**: The `getAdbUrl` method is **only available in mobile environments**.

- ✅ **Supported**: Sessions created with mobile environment images (e.g., `mobile_latest`)
- ❌ **Not Supported**: Browser, Linux, or other non-mobile environment images

If you attempt to use this method with a non-mobile session, you will receive an error indicating that the operation is only supported in mobile environments.

## Step-by-Step Guide

### Step 1: Obtain Your ADB Public Key

The `getAdbUrl` method requires your ADB public key for device authentication. You need to provide your actual ADB public key to establish an authorized connection.

**Locate your ADB public key:**

```bash
# ADB public key is typically located at:
# - Linux/macOS: ~/.android/adbkey.pub
# - Windows: %USERPROFILE%\.android\adbkey.pub

# View your ADB public key
cat ~/.android/adbkey.pub
```

Example output:
```
QAAAAI/NTd6RTmNt3enWSGR8iqLQF1/TkNWcMSxmy9vAqQkn6xha/lCkxtiQV4LYJ8nRbCiWIyCaslUCG2dFBcd9nPhhUTHvdMzYjf6DNJH3J0mPmErWrB0tg2BVPZ2eFNG7HnKmi+bztVLBJYx6NS/54Ki5rbWgqNPjRw5riOPtXJsu3KwVS1VMTI8VuBX+Xg401NW3tjrOfybf6fWnqKFpPX+B6dFASm3eIIye5tkhbuG4cNYURLpf10tyv9bssYi0Vdr0GcmTH9yQ0rDVn4L/n2HPa6eLuuX0WYQyj8uD2fKUryunOCbi95k1ZCQMt+ZTZRK+MvaZfly5QA2mNeQ7LURyMDi3g3C6J8Tu+8uzgrwBUPvdSwiTnht4ZyDjGr8JB+lDiDf5LfB52+Npl4wKBiMV2J/aa3FyBgzFEMRKtnRa+r1u2zB6e2LNG8xkDHVF3L7ODeI5QHDkTwz1X9betVss5mV5sALv45nfzOLo4IbAR94eH9jj3j+E8mclHKDqhpkR8KRoh/K4mHQCg+a3Qz3JTaO6ddLqqFN+wCn/7YnHfPfH3HF8m9CXEoPIhFAsWI7H3LH4lZ9AZZqVm3IZJ4UrSbR2pX7a1D4R+Cd7JcantfxmyXrc8K7Ui1/2W9qZkz9cczqnnQTNciqa0i7xITVNFtLGFWfCeEe/wFAds2qn+GKcSwEAAQA= user@hostname
```

**Read the key in Python:**

```python
import os

# Read your ADB public key
adbkey_path = os.path.expanduser('~/.android/adbkey.pub')
with open(adbkey_path, 'r') as f:
    adbkey_pub = f.read().strip()

print(f"ADB key loaded (first 50 chars): {adbkey_pub[:50]}...")
```

> **Important**: While the `adbkey_pub` parameter is not validated by the AgentBay server (any non-empty string will work for getting the URL), you **must use your actual ADB public key** for the subsequent ADB connection to work properly. Using a fake key will result in "unauthorized" device status when connecting via ADB.

### Step 2: Create a Mobile Session

```python
from agentbay import AgentBay, CreateSessionParams

# Initialize AgentBay client
client = AgentBay(api_key="your_api_key")

# Create a mobile session
result = client.create(CreateSessionParams(image_id="mobile_latest"))
session = result.session

print(f"Session created: {session.session_id}")
```

### Step 3: Get ADB Connection URL

```python
# Get ADB connection URL using your real ADB public key
adb_result = session.mobile.get_adb_url(adbkey_pub=adbkey_pub)

if adb_result.success:
    print(f"ADB URL: {adb_result.data}")
    print(f"Request ID: {adb_result.request_id}")
else:
    print(f"Error: {adb_result.error_message}")
```

Expected output:
```
ADB URL: adb connect 47.99.76.99:54321
Request ID: 1234567890ABCDEF
```

The returned URL format is: `adb connect <IP>:<Port>`

### Step 4: Connect to the Device via ADB

The returned URL is a complete ADB connect command. Simply copy and execute it:

```python
# The returned URL is already a complete command
# URL format: "adb connect 47.99.76.99:54321"
adb_url = adb_result.data
print(f"Run this command: {adb_url}")
```

Execute the command in your terminal:

```bash
# Copy and run the command from the output
adb connect 47.99.76.99:54321
```

Expected output:
```
connected to 47.99.76.99:54321
```

### Step 5: Verify the Connection

```bash
# List connected devices
adb devices
```

Expected output:
```
List of devices attached
47.99.76.99:54321    device
```

The device status should be `device` (not `offline` or `unauthorized`).

If the device shows as `unauthorized`, you need to use your actual ADB public key (see Step 1).

### Step 6: Use ADB Commands

Once connected, you can use any standard ADB command:

```bash
# Get device information
adb shell getprop ro.product.model
# Output: wuying android14

# List installed packages
adb shell pm list packages
# Output: package:com.android.providers.media.module
#         package:com.android.modulemetadata
#         ...

# Take a screenshot
adb shell screencap -p /sdcard/screenshot.png
adb pull /sdcard/screenshot.png
# Output: /sdcard/screenshot.png: 1 file pulled...

# View real-time logs (press Ctrl+C to stop)
adb logcat

# Install an application
adb install app.apk

# Access device shell
adb shell
# You'll get an interactive shell prompt
```

### Step 7: Disconnect and Cleanup

```bash
# Disconnect from the device
adb disconnect 47.99.76.99:54321
```

```python
# Delete the session when done
session.delete()
print("Session deleted")
```

## Complete Example

Here's a complete Python example that demonstrates the full workflow:

```python
from agentbay import AgentBay, CreateSessionParams
import subprocess
import time

def main():
    # Step 1: Read ADB public key
    import os
    adbkey_path = os.path.expanduser('~/.android/adbkey.pub')
    with open(adbkey_path, 'r') as f:
        adbkey_pub = f.read().strip()
    print(f"ADB key loaded (first 50 chars): {adbkey_pub[:50]}...")
    
    # Initialize client
    client = AgentBay(api_key="your_api_key")
    
    try:
        # Step 2: Create mobile session
        print("\nCreating mobile session...")
        result = client.create(CreateSessionParams(image_id="mobile_latest"))
        session = result.session
        print(f"✅ Session created: {session.session_id}")
        
        # Step 3: Get ADB connection URL
        print("\nGetting ADB connection URL...")
        adb_result = session.mobile.get_adb_url(adbkey_pub=adbkey_pub)
        
        if not adb_result.success:
            print(f"❌ Failed: {adb_result.error_message}")
            return
        
        print(f"✅ ADB URL: {adb_result.data}")
        print(f"✅ Request ID: {adb_result.request_id}")
        
        # Step 3: Parse the ADB connect command
        adb_url = adb_result.data  # "adb connect 47.99.76.99:54321"
        # Extract just the address part for later use
        address = adb_url.replace("adb connect ", "")
        
        # Step 4: Connect via ADB
        print(f"\nConnecting to device...")
        print(f"Command: {adb_url}")
        result = subprocess.run(
            ["adb", "connect", address],
            capture_output=True,
            text=True
        )
        print(result.stdout.strip())
        
        # Wait for connection to establish
        time.sleep(2)
        
        # Step 5: Verify connection
        print("\nVerifying connection...")
        print("Command: adb devices")
        result = subprocess.run(
            ["adb", "devices"],
            capture_output=True,
            text=True
        )
        print(result.stdout)
        
        # Check if device is connected
        if "unauthorized" in result.stdout:
            print("❌ Device is unauthorized - check your ADB public key")
            return
        elif address not in result.stdout or "device" not in result.stdout:
            print("❌ Device not connected properly")
            return
        
        print("✅ Device connected successfully!")
        
        # Step 6: Now you can use ADB commands
        print("\nYou can now use ADB commands:")
        print(f"  adb -s {address} shell getprop ro.product.model")
        print(f"  adb -s {address} shell pm list packages")
        print(f"  adb -s {address} shell screencap -p /sdcard/screenshot.png")
        
        # Example: Get device model
        print("\nExample - Getting device model...")
        result = subprocess.run(
            ["adb", "-s", address, "shell", "getprop", "ro.product.model"],
            capture_output=True,
            text=True
        )
        print(f"Device model: {result.stdout.strip()}")
        
        # Step 7: Disconnect
        print(f"\nDisconnecting from {address}...")
        subprocess.run(["adb", "disconnect", address])
        print("✅ Disconnected")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    finally:
        # Cleanup
        print("\nCleaning up session...")
        session.delete()
        print("✅ Session deleted")

if __name__ == "__main__":
    main()
```

## Error Handling

### Check ADB Key File

```python
import os

adbkey_path = os.path.expanduser('~/.android/adbkey.pub')
if not os.path.exists(adbkey_path):
    print(f"Error: ADB public key not found at {adbkey_path}")
    exit(1)
```

### Check getAdbUrl Result

```python
result = session.mobile.get_adb_url(adbkey_pub)

if not result.success:
    print(f"Error: {result.error_message}")
    exit(1)
```

### Verify ADB Connection

After connecting, verify the device status:

```bash
adb devices
```

Check the output:
- ✅ `device` - Connected and authorized
- ❌ `unauthorized` - ADB public key is incorrect
- ❌ `offline` - Connection issue

## Troubleshooting

### Device Shows as Unauthorized

If the device shows as "unauthorized" when running `adb devices`:

```
List of devices attached
47.99.76.99:54321	unauthorized
```

**Cause**: You are not using your actual ADB public key, or there's an ADB client-side authentication issue.

**Solution**: 
1. **First, ensure you're using your real ADB public key**:
   ```python
   import os
   adbkey_path = os.path.expanduser('~/.android/adbkey.pub')
   with open(adbkey_path, 'r') as f:
       adbkey_pub = f.read().strip()  # Read the entire key
   
   result = session.mobile.get_adb_url(adbkey_pub=adbkey_pub)
   ```

2. **If still unauthorized, restart the ADB server**:
   ```bash
   adb kill-server
   adb start-server
   ```

3. **Try reconnecting**:
   ```bash
   adb connect <IP>:<Port>
   ```

**Note**: While the AgentBay server doesn't validate the `adbkey_pub` parameter, the ADB client requires the correct key for device authorization.

### Connection Refused

If you get "connection refused" errors:

```bash
# Restart ADB server
adb kill-server
adb start-server

# Try connecting again
adb connect <IP>:<Port>
```

### Device Shows as Offline

If the device appears as "offline":

```bash
# Disconnect and reconnect
adb disconnect <IP>:<Port>
adb connect <IP>:<Port>
```

### Multiple Devices Connected

If you have multiple devices, specify the device for each command:

```bash
# Use -s flag to specify device
adb -s <IP>:<Port> shell getprop
adb -s <IP>:<Port> install app.apk
```

### Cannot Find ADB Command

If `adb` command is not found:

```bash
# Check if ADB is installed
which adb

# If not installed, refer to Android documentation for installation
```

## API Documentation

For detailed API documentation in other languages:

- **Python**: [Mobile API Documentation](../../../python/docs/api/sync/mobile.md#getadburl)
- **Golang**: [Mobile API Documentation](../../../golang/docs/api/mobile-use/mobile.md#getadburl)
- **TypeScript**: [Mobile API Documentation](../../../typescript/docs/api/mobile-use/mobile.md)

## Example Code

Complete working examples for all languages:

- **Python**: [mobile_get_adb_url_example.py](../../../python/docs/examples/_async/mobile-use/mobile_get_adb_url_example.py)
- **Golang**: [mobile_get_adb_url Example](../../../golang/docs/examples/mobile-use/mobile_get_adb_url/README.md)
- **TypeScript**: [mobile-get-adb-url Example](../../../typescript/docs/examples/mobile-use/mobile-get-adb-url/README.md)

## Related Guides

- [Mobile UI Automation](./mobile-ui-automation.md) - Touch gestures and UI interaction
- [Mobile Application Management](./mobile-application-management.md) - App lifecycle management
- [Session Management](../common-features/basics/session-management.md) - Session creation and management

## Summary

The ADB connection feature enables you to:

1. ✅ Connect to cloud-based mobile sessions from your local machine
2. ✅ Use standard ADB commands to control the device
3. ✅ Integrate with existing ADB-based tools and workflows
4. ✅ Debug and test mobile applications remotely

**Key Points:**
- Only works with `mobile_latest` sessions  
- Must use your actual ADB public key for successful device connection (server doesn't validate the parameter, but ADB client does)
- Returns URL in format: `adb connect <IP>:<Port>`
- Always verify connection with `adb devices` before running commands
- Remember to disconnect and delete the session when done
