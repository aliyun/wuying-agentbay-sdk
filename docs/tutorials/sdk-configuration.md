# SDK Configuration

This tutorial explains how to configure the AgentBay SDK, including setting region, endpoint, and timeout parameters.

## Configuration Precedence

The SDK uses the following precedence order for configuration (highest to lowest):

1. Explicitly passed configuration in code
2. Environment variables
3. `.env` file
4. Default configuration

## Default Configuration

If no configuration is provided, the SDK uses the following default values:

```json
{
    "region_id": "cn-shanghai",
    "endpoint": "wuyingai.cn-shanghai.aliyuncs.com",
    "timeout_ms": 60000
}
```

## Configuration Methods

### 1. Explicitly Pass Configuration in Code

#### Python

```python
from agentbay import AgentBay, Config

custom_config = Config(
    region_id="cn-beijing",
    endpoint="wuyingai.cn-beijing.aliyuncs.com",
    timeout_ms=30000
)

agent_bay = AgentBay(api_key="your-api-key", cfg=custom_config)
```

#### TypeScript

```typescript
import { AgentBay, Config } from 'wuying-agentbay-sdk';

const customConfig: Config = {
  region_id: 'cn-beijing',
  endpoint: 'wuyingai.cn-beijing.aliyuncs.com',
  timeout_ms: 30000,
};

const agentBay = new AgentBay({
  apiKey: 'your-api-key-here',
  config: customConfig,
});
```

#### Golang

```go
package main

import (
    "github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

func main() {
    customConfig := &agentbay.Config{
        RegionID:  "cn-beijing",
        Endpoint:  "wuyingai.cn-beijing.aliyuncs.com",
        TimeoutMs: 30000,
    }

    client, err := agentbay.NewAgentBay("your-api-key", agentbay.WithConfig(customConfig))
    if err != nil {
        panic(err)
    }
}
```

### 2. Use Environment Variables

Set environment variables in your shell:

```bash
export AGENTBAY_REGION_ID=cn-qingdao
export AGENTBAY_ENDPOINT=wuyingai.cn-qingdao.aliyuncs.com
export AGENTBAY_TIMEOUT_MS=120000
```

Then create the SDK client without explicit configuration:

```python
# Python
agent_bay = AgentBay(api_key="your-api-key")
```

```typescript
// TypeScript
const agentBay = new AgentBay({ apiKey: 'your-api-key-here' });
```

```go
// Golang
client, err := agentbay.NewAgentBay("your-api-key", nil)
```

### 3. Use a `.env` File

Create a `.env` file in your project root directory:

```env
AGENTBAY_REGION_ID=cn-hangzhou
AGENTBAY_ENDPOINT=wuyingai.cn-hangzhou.aliyuncs.com
AGENTBAY_TIMEOUT_MS=45000
```

The SDK will automatically load this file when initialized:

```python
# Python
agent_bay = AgentBay(api_key="your-api-key")
```

```typescript
// TypeScript
const agentBay = new AgentBay({ apiKey: 'your-api-key-here' });
```

```go
// Golang
client, err := agentbay.NewAgentBay("your-api-key", nil)
```

## Troubleshooting

If you're experiencing connectivity issues:

1. Verify your region and endpoint settings
2. Check that your timeout value is appropriate for your network conditions
3. If using environment variables, ensure they are correctly set in your current shell
4. For `.env` file configuration, verify the file is in the correct location and properly formatted 