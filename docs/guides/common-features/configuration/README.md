# Configuration

This section covers SDK configuration options and settings for different environments and requirements.

## 📚 Documentation

- [SDK Configuration](sdk-configuration.md) - API keys, regions, endpoints, timeouts, and advanced options

## 🎯 What is Configuration?

Configuration allows you to customize the AgentBay SDK behavior for your specific needs:

### 🔑 Authentication
- API key management
- Environment variable configuration
- Secure credential handling

### 🌍 Region and Endpoints
- Select service regions
- Custom endpoint configuration
- Network routing options

### ⏱️ Timeouts and Limits
- Request timeout settings
- Retry policies
- Rate limiting

### 🔧 Advanced Options
- Logging configuration
- Debug mode
- Custom HTTP clients
- Proxy settings

## 🚀 Quick Example

```python
from agentbay import AgentBay
from agentbay.config import Config

# Basic configuration
agent_bay = AgentBay(api_key="your-api-key")

# Advanced configuration
config = Config(
    api_key="your-api-key",
    endpoint="https://custom-endpoint.example.com",
    timeout=60,
    region="cn-hangzhou"
)
agent_bay = AgentBay(config=config)
```

## 📖 Learn More

- [SDK Configuration Guide](sdk-configuration.md) - Complete configuration reference
- [Basic Features](../basics/README.md) - Get started with basic features
- [Advanced Features](../advanced/README.md) - Explore advanced capabilities

## 🆘 Getting Help

- [GitHub Issues](https://github.com/aliyun/wuying-agentbay-sdk/issues)
- [API Reference](../../api-reference.md)
- [Main Documentation](../../README.md)
