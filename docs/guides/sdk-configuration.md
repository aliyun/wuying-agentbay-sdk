# SDK Configuration Guide

This comprehensive guide explains how to configure the AgentBay SDK, including API key authentication, region settings, endpoint configuration, timeout settings, and various configuration methods.

## Configuration Overview

The AgentBay SDK supports comprehensive configuration options to customize its behavior for different environments and requirements.

### Configuration Parameters

| Parameter | Environment Variable | Description | Default Value |
|-----------|---------------------|-------------|---------------|
| API Key | `AGENTBAY_API_KEY` | Authentication key for API access | Required |
| Region ID | `AGENTBAY_REGION_ID` | Service region identifier | `cn-shanghai` |
| Endpoint | `AGENTBAY_ENDPOINT` | Service endpoint URL | `wuyingai.cn-shanghai.aliyuncs.com` |
| Timeout | `AGENTBAY_TIMEOUT_MS` | Request timeout in milliseconds (max 60000) | `60000` |

### Supported Regions

| Region Name | Region ID | Endpoint |
|-------------|-----------|----------|
| Shanghai | `cn-shanghai` | `wuyingai.cn-shanghai.aliyuncs.com` |
| Singapore | `ap-southeast-1` | `wuyingai.ap-southeast-1.aliyuncs.com` |

## Default Configuration

If no configuration is provided, the SDK uses the following default values:

```json
{
    "region_id": "cn-shanghai",
    "endpoint": "wuyingai.cn-shanghai.aliyuncs.com",
    "timeout_ms": 60000
}
```

## Configuration Precedence

The SDK uses the following precedence order for configuration (highest to lowest):

1. **Explicitly passed configuration in code**
2. **Environment variables**
3. **`.env` configuration file**
4. **Default configuration**

> **Note:** The Golang implementation is slightly different - it loads the `.env` file into environment variables first, then reads environment variables, but the final precedence order remains consistent.

## Configuration Methods

### 1. Environment Variables Configuration

This is the most commonly used configuration method, suitable for switching regions across different environments.

#### Setting Environment Variables

**Linux/macOS:**
```bash
export AGENTBAY_API_KEY=your-api-key-here
export AGENTBAY_REGION_ID=ap-southeast-1
export AGENTBAY_ENDPOINT=wuyingai.ap-southeast-1.aliyuncs.com
export AGENTBAY_TIMEOUT_MS=60000
```

**Windows (PowerShell):**
```powershell
$env:AGENTBAY_API_KEY="your-api-key-here"
$env:AGENTBAY_REGION_ID="ap-southeast-1"
$env:AGENTBAY_ENDPOINT="wuyingai.ap-southeast-1.aliyuncs.com"
$env:AGENTBAY_TIMEOUT_MS="60000"
```

**Windows (Command Prompt):**
```cmd
set AGENTBAY_API_KEY=your-api-key-here
set AGENTBAY_REGION_ID=ap-southeast-1
set AGENTBAY_ENDPOINT=wuyingai.ap-southeast-1.aliyuncs.com
set AGENTBAY_TIMEOUT_MS=60000
```

#### Using Environment Variables

After setting environment variables, create the SDK client directly:

**Python:**
```python
from agentbay import AgentBay

# SDK will automatically read environment variable configuration
# API key can also be set via AGENTBAY_API_KEY environment variable
agent_bay = AgentBay()  # or AgentBay(api_key="your-api-key")
```

**TypeScript:**
```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

// SDK will automatically read environment variable configuration
// API key can also be set via AGENTBAY_API_KEY environment variable
const agentBay = new AgentBay();  // or new AgentBay({ apiKey: 'your-api-key' })
```

**Golang:**
```go
package main

import (
    "github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

func main() {
    // SDK will automatically read environment variable configuration
    // API key can also be set via AGENTBAY_API_KEY environment variable
    client, err := agentbay.NewAgentBay("")  // or agentbay.NewAgentBay("your-api-key")
    if err != nil {
        panic(err)
    }
}
```

### 2. Configuration File Method

Create a `.env` file in your project root directory:

```env
AGENTBAY_API_KEY=your-api-key-here
AGENTBAY_REGION_ID=ap-southeast-1
AGENTBAY_ENDPOINT=wuyingai.ap-southeast-1.aliyuncs.com
AGENTBAY_TIMEOUT_MS=60000
```

Then create the SDK client normally:

**Python:**
```python
from agentbay import AgentBay

# SDK will automatically load .env file
# No need to specify API key if it's in .env file
agent_bay = AgentBay()
```

**TypeScript:**
```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

// SDK will automatically load .env file
// No need to specify API key if it's in .env file
const agentBay = new AgentBay();
```

**Golang:**
```go
package main

import (
    "github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

func main() {
    // SDK will automatically load .env file
    // No need to specify API key if it's in .env file
    client, err := agentbay.NewAgentBay("")
    if err != nil {
        panic(err)
    }
}
```

### 3. Explicit Code Configuration

Pass configuration object directly in code - this method has the highest priority.

**Python:**
```python
from agentbay import AgentBay, Config

# Configure Singapore region
singapore_config = Config(
    region_id="ap-southeast-1",
    endpoint="wuyingai.ap-southeast-1.aliyuncs.com",
    timeout_ms=60000
)

agent_bay = AgentBay(api_key="your-api-key", cfg=singapore_config)
```

**TypeScript:**
```typescript
import { AgentBay, Config } from 'wuying-agentbay-sdk';

// Configure Singapore region
const singaporeConfig: Config = {
  region_id: 'ap-southeast-1',
  endpoint: 'wuyingai.ap-southeast-1.aliyuncs.com',
  timeout_ms: 60000,
};

const agentBay = new AgentBay({
  apiKey: 'your-api-key',
  config: singaporeConfig,
});
```

**Golang:**
```go
package main

import (
    "github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

func main() {
    // Configure Singapore region
    singaporeConfig := &agentbay.Config{
        RegionID:  "ap-southeast-1",
        Endpoint:  "wuyingai.ap-southeast-1.aliyuncs.com",
        TimeoutMs: 60000,
    }

    client, err := agentbay.NewAgentBay("your-api-key", agentbay.WithConfig(singaporeConfig))
    if err != nil {
        panic(err)
    }
}
```

## Common Configuration Scenarios

### Switching to Singapore Region

If you need to use Singapore region services, environment variables are recommended:

```bash
# Set Singapore region
export AGENTBAY_REGION_ID=ap-southeast-1
export AGENTBAY_ENDPOINT=wuyingai.ap-southeast-1.aliyuncs.com
```

### Custom Timeout Settings

Due to gateway restrictions, the maximum timeout is limited to 60 seconds. Values exceeding 60 seconds will be automatically set to 60 seconds.

```bash
# Set maximum timeout (60 seconds)
export AGENTBAY_TIMEOUT_MS=60000

# Values over 60000 will be capped at 60000
export AGENTBAY_TIMEOUT_MS=30000  # This will work
```

### Development Environment Configuration

For development environments, using a `.env` file is recommended:

```env
# .env file
AGENTBAY_API_KEY=your-development-api-key
AGENTBAY_REGION_ID=cn-shanghai
AGENTBAY_ENDPOINT=wuyingai.cn-shanghai.aliyuncs.com
AGENTBAY_TIMEOUT_MS=60000
```

### Production Environment Configuration

For production environments, use environment variables and choose the appropriate service region based on deployment location:

```bash
# If application is deployed in Asia-Pacific region, use Singapore
export AGENTBAY_REGION_ID=ap-southeast-1
export AGENTBAY_ENDPOINT=wuyingai.ap-southeast-1.aliyuncs.com

# If application is deployed in mainland China, use Shanghai
export AGENTBAY_REGION_ID=cn-shanghai
export AGENTBAY_ENDPOINT=wuyingai.cn-shanghai.aliyuncs.com
```

## Configuration Verification

You can verify if the configuration is effective through the following methods:

**Python:**
```python
from agentbay import AgentBay

agent_bay = AgentBay(api_key="your-api-key")
print(f"Current region: {agent_bay.region_id}")
```

**TypeScript:**
```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

const agentBay = new AgentBay({ apiKey: 'your-api-key' });
// Note: regionId is a private property, configuration can be verified through session creation logs or other methods
console.log('AgentBay client created, configuration loaded');
```

**Golang:**
```go
package main

import (
    "fmt"
    "github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

func main() {
    client, err := agentbay.NewAgentBay("your-api-key")
    if err != nil {
        panic(err)
    }
    
    fmt.Printf("Current region: %s\n", client.RegionId)
}
```

## Troubleshooting

### Connection Issues

If you encounter connection problems, check:

1. **Verify region and endpoint settings are correct**
   ```bash
   echo $AGENTBAY_REGION_ID
   echo $AGENTBAY_ENDPOINT
   ```

2. **Network connectivity**
   ```bash
   # Test endpoint connectivity
   curl -I https://wuyingai.ap-southeast-1.aliyuncs.com
   ```

3. **Timeout settings are appropriate**
   - Remember that timeout is capped at 60 seconds due to gateway restrictions
   - If network is slow, ensure you're not exceeding the 60-second limit

### Configuration Not Taking Effect

If configuration is not working, check:

1. **Environment variables are set correctly**
   ```bash
   env | grep AGENTBAY
   ```

2. **`.env` file location is correct**
   - Ensure `.env` file is in project root directory
   - Check file format is correct (no spaces, proper equals signs)

3. **Configuration precedence**
   - Remember explicit code configuration overrides environment variables
   - Environment variables override `.env` file configuration

### Common Errors

**Error: Cannot connect to service**
```
Solutions:
1. Check if region_id and endpoint match
2. Confirm network can access target endpoint
3. Verify API key is valid
```

**Error: Timeout**
```
Solutions:
1. Ensure timeout_ms value doesn't exceed 60000 (60 seconds)
2. Check network connection quality
3. Try switching to a closer region
```

**Error: Invalid timeout value**
```
Solutions:
1. Set timeout_ms to a value between 1000 and 60000
2. Values over 60000 will be automatically capped at 60000
```

## Best Practices

1. **Choose appropriate region**
   - Select the region closest to your users for optimal performance
   - Consider data compliance requirements

2. **Use environment variables**
   - Use environment variables in production rather than hardcoded configuration
   - Facilitates switching between different environments

3. **Set reasonable timeout values**
   - Adjust timeout based on network environment, but remember the 60-second limit
   - Avoid setting timeouts that are too short and cause request failures
   - Default 60-second timeout is recommended for most scenarios

4. **Configuration validation**
   - Validate configuration is correct during application startup
   - Log current region and endpoint information for debugging

5. **Timeout considerations**
   - Be aware of the 60-second maximum timeout limitation
   - Plan your application logic considering this constraint
   - For operations that might take longer, consider implementing retry mechanisms

## Related Documentation

- [Getting Started](../quickstart/installation.md)
- [API Reference](../api-reference.md)
- [Session Management](./session-management.md)
- [Troubleshooting](../quickstart/troubleshooting.md) 