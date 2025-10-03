# SDK Configuration Guide

This guide explains how to configure the AgentBay SDK for different environments and requirements.

## Configuration Parameters

| Parameter | Environment Variable | Description | Default Value |
|-----------|---------------------|-------------|---------------|
| API Key | `AGENTBAY_API_KEY` | Authentication key for API access | Required |
| Region ID | `AGENTBAY_REGION_ID` | Service region identifier | `cn-shanghai` |
| Endpoint | `AGENTBAY_ENDPOINT` | Service endpoint URL | `wuyingai.cn-shanghai.aliyuncs.com` |

## Supported Regions

| Region Name | Region ID | Endpoint |
|-------------|-----------|----------|
| Shanghai | `cn-shanghai` | `wuyingai.cn-shanghai.aliyuncs.com` |
| Singapore | `ap-southeast-1` | `wuyingai.ap-southeast-1.aliyuncs.com` |

## Default Configuration

If no configuration is provided, the SDK uses the following default values:

```json
{
    "region_id": "cn-shanghai",
    "endpoint": "wuyingai.cn-shanghai.aliyuncs.com"
}
```

## Configuration Priority

Configuration values are resolved in the following order (highest to lowest priority):

1. **Hard-coded configuration** (passed directly to SDK)
2. **Environment variables**
3. **`.env` configuration file** (searched upward from current directory)
4. **Default configuration**

## Configuration Methods

### Method 1: Environment Variables

Set configuration using shell commands:

**Linux/macOS:**
```bash
export AGENTBAY_API_KEY=your-api-key-here
export AGENTBAY_REGION_ID=ap-southeast-1
export AGENTBAY_ENDPOINT=wuyingai.ap-southeast-1.aliyuncs.com
```

**Windows:**
```cmd
set AGENTBAY_API_KEY=your-api-key-here
set AGENTBAY_REGION_ID=ap-southeast-1
set AGENTBAY_ENDPOINT=wuyingai.ap-southeast-1.aliyuncs.com
```

### Method 2: .env File

The SDK automatically searches for `.env` files using the following strategy:

1. **Current directory** - starts from where your program runs
2. **Parent directories** - searches upward until it finds a `.env` file or reaches the root
3. **First match wins** - stops searching when the first `.env` file is found

**Basic usage:**
```env
# .env file (can be placed in project root or any parent directory)
AGENTBAY_API_KEY=your-api-key-here
AGENTBAY_REGION_ID=ap-southeast-1
AGENTBAY_ENDPOINT=wuyingai.ap-southeast-1.aliyuncs.com
```

**File locations examples:**
```
my-project/
├── .env                    # ✅ Found from any subdirectory
└── src/
    └── app/
        └── main.py         # Searches upward: app/ → src/ → my-project/ ✅
```

**Custom .env file path:**

```python
from agentbay import AgentBay
client = AgentBay(env_file="/path/to/custom.env")
```

### Method 3: Hard-coded Configuration (Debug Only)

For debugging purposes, you can pass configuration directly in code:

```python
from agentbay import AgentBay, Config

# Hard-coded configuration (not recommended for production)
config = Config(
    region_id="ap-southeast-1",
    endpoint="wuyingai.ap-southeast-1.aliyuncs.com",
    timeout_ms=60000
)
agent_bay = AgentBay(api_key="your-api-key-here", cfg=config)
```

> **Warning:** Hard-coding API keys and configuration is not recommended for production environments due to security risks.

### SDK Initialization

After setting configuration, initialize the SDK:

```python
from agentbay import AgentBay
agent_bay = AgentBay()  # Automatically searches for .env files
```

## Common Scenarios

### Switch to Singapore Region

```bash
export AGENTBAY_REGION_ID=ap-southeast-1
export AGENTBAY_ENDPOINT=wuyingai.ap-southeast-1.aliyuncs.com
```


### Development vs Production

**Development:** 
- Use `.env` file in project root for local configuration
- SDK automatically finds configuration regardless of execution directory
- For different environments, use custom paths: `AgentBay(env_file=".env.development")`

**Production:** 
- Use environment variables for secure deployment
- Environment variables always take precedence over `.env` files

## Troubleshooting

### Check Configuration

```bash
env | grep AGENTBAY  # Verify environment variables
```

**Debug .env file discovery:**
```bash
# Check if .env file exists in current directory or parent directories
find . -name ".env" -o -name ".git" -type d 2>/dev/null | head -10
```

### Common Error Messages

#### 1. Missing API Key
**Error:** `ValueError: API key is required. Provide it as a parameter or set the AGENTBAY_API_KEY environment variable`

**Solution:** 
- Set the `AGENTBAY_API_KEY` environment variable
- Or pass `api_key` parameter when creating AgentBay instance

#### 2. Invalid API Key
**Error:** `NOT_LOGIN code: 400, You are not logged in or your login token has expired`

**Solution:**
- Verify your API key is correct and not expired
- Check if your API key has proper permissions
- Contact support if the key should be valid

#### 3. API Key and Region Mismatch
**Error:** `NOT_LOGIN code: 400` with unexpected `HostId` in error response

**Example:** Error shows `'HostId': 'wuyingai.ap-southeast-1.aliyuncs.com'` but you expected to connect to Shanghai region.

**Solution:**
- Check if your API key belongs to the correct region
- Ensure `AGENTBAY_REGION_ID` and `AGENTBAY_ENDPOINT` match your API key's region
- Shanghai API keys work with `cn-shanghai` region and `wuyingai.cn-shanghai.aliyuncs.com` endpoint
- Singapore API keys work with `ap-southeast-1` region and `wuyingai.ap-southeast-1.aliyuncs.com` endpoint

#### 4. Wrong Endpoint/Network Issues
**Error:** `Failed to resolve 'invalid-endpoint.com'` or `NameResolutionError`

**Solution:**
- Verify the endpoint URL is correct
- Ensure your network can reach the endpoint
- Check if you're behind a corporate firewall
- Confirm region and endpoint match (see supported regions table above)

#### 5. .env File Not Found
**Symptom:** SDK uses default configuration despite having a `.env` file

**Solution:**
- Ensure `.env` file is in your project root or a parent directory
- Check file permissions (must be readable)
- Verify file format (no spaces around `=`, proper line endings)
- Use absolute path if needed: `AgentBay(env_file="/full/path/to/.env")`
- Debug with: `find . -name ".env" -type f` to locate your `.env` files

### Quick Diagnosis

```python
from agentbay import AgentBay

try:
    agent_bay = AgentBay()  # Test basic initialization
    result = agent_bay.create()  # Test API connectivity
    print("Configuration is working correctly")
except ValueError as e:
    print(f"Configuration issue: {e}")
except Exception as e:
    print(f"Network/API issue: {e}")
```

## Best Practices

- **Region:** Choose the region closest to your users
- **Security:** Use environment variables in production (not hardcoded values)
- **Validation:** Test configuration during application startup

## Related Documentation

- [Getting Started](../../../quickstart/installation.md)
- [Session Management](../basics/session-management.md)
