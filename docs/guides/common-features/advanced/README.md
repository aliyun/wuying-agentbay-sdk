# Advanced Features

Advanced features provide powerful capabilities for complex use cases, including network isolation, session connectivity, and AI-powered automation.

## 📚 Documentation

- [Session Link Access](session-link-access.md) - Session connectivity, URL generation, and port forwarding
- [VPC Sessions](vpc-sessions.md) - Isolated network environments with Virtual Private Cloud
- [Agent Modules](agent-modules.md) - AI-powered task execution for complex operations
- [OSS Integration](oss-integration.md) - Object Storage Service integration for file upload/download

## 🎯 What are Advanced Features?

Advanced features extend the basic capabilities with sophisticated functionality:

### 🔗 Session Link Access
Access sessions through various protocols:
- Generate session URLs and endpoints
- WebSocket and HTTPS connections
- Port forwarding and tunneling
- Custom port configurations
- Troubleshoot connectivity issues

### 🔒 VPC Sessions
Isolated network environments:
- Virtual Private Cloud integration
- Network security and isolation
- Custom network configurations
- Secure resource access
- Enterprise-grade security

### 🤖 Agent Modules
AI-powered task execution:
- Natural language task processing
- Web scraping and data extraction
- Automated testing and QA
- Code generation and review
- Complex workflow automation

### 📦 OSS Integration
Object Storage Service operations:
- Authenticated file upload/download
- Anonymous operations with presigned URLs
- Integration with Alibaba Cloud OSS
- Data backup and distribution
- Large file transfers

## 🚀 Quick Examples

### Session Link Access

```python
from agentbay import AgentBay

agent_bay = AgentBay(api_key="your-api-key")
result = agent_bay.create()

if result.success:
    session = result.session
    
    # Get session access link
    link_result = session.get_link()
    if link_result.success:
        print(f"Session URL: {link_result.url}")
        print(f"WebSocket URL: {link_result.ws_url}")
    
    agent_bay.delete(session)
```

### VPC Sessions

```python
from agentbay import AgentBay
from agentbay.session_params import CreateSessionParams

agent_bay = AgentBay(api_key="your-api-key")

# Create VPC session
session_params = CreateSessionParams(
    vpc_id="vpc-xxxxx",
    subnet_id="subnet-xxxxx"
)
result = agent_bay.create(session_params)

if result.success:
    session = result.session
    # VPC session with network isolation
    agent_bay.delete(session)
```

### Agent Modules

```python
from agentbay import AgentBay

agent_bay = AgentBay(api_key="your-api-key")
result = agent_bay.create()

if result.success:
    session = result.session
    
    # Use AI agent for complex tasks
    task_result = session.agent.execute_task(
        "Extract product prices from this e-commerce page"
    )
    
    agent_bay.delete(session)
```

### OSS Integration

```python
from agentbay import AgentBay
from agentbay.session_params import CreateSessionParams

agent_bay = AgentBay(api_key="your-api-key")
params = CreateSessionParams(image_id="code_latest")
result = agent_bay.create(params)

if result.success:
    session = result.session
    
    # Initialize OSS
    session.oss.env_init(
        access_key_id="your-oss-key",
        access_key_secret="your-oss-secret",
        endpoint="https://oss-cn-hangzhou.aliyuncs.com"
    )
    
    # Upload file to OSS
    session.oss.upload(
        bucket="my-bucket",
        object="data/file.txt",
        path="/home/guest/file.txt"
    )
    
    agent_bay.delete(session)
```

## 📖 When to Use Advanced Features

- **Session Link Access**: When you need to integrate sessions with external tools, browsers, or custom applications
- **VPC Sessions**: When you require network isolation, enhanced security, or need to access private resources
- **Agent Modules**: When you need AI-powered automation for complex tasks like web scraping, testing, or natural language processing
- **OSS Integration**: When you need to transfer large files, backup data, or integrate with Alibaba Cloud Object Storage

## 📖 Prerequisites

Before using advanced features:

1. Familiarize yourself with [Basic Features](../basics/README.md)
2. Review [SDK Configuration](../configuration/sdk-configuration.md)
3. Understand [Session Management](../basics/session-management.md)

## 🆘 Getting Help

- [GitHub Issues](https://github.com/aliyun/wuying-agentbay-sdk/issues)
- [API Reference](../../api-reference.md)
- [Main Documentation](../../README.md)
