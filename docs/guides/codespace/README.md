# CodeSpace Guide

CodeSpace is AgentBay's development-focused environment that provides code execution capabilities and development tools.

## 📚 Documentation

### Core Features
- [Code Execution](code-execution.md) - Run Python, JavaScript, and other programming languages

## 🎯 What is CodeSpace?

CodeSpace provides a dedicated development environment optimized for:

- **Multi-language Code Execution** - Python and JavaScript/Node.js
- **Package Management** - Install dependencies (pip, npm, etc.)
- **Development Tools** - Pre-installed compilers, interpreters, and utilities
- **Isolated Execution** - Secure, containerized code execution

## 🚀 Quick Start

```python
from agentbay import AgentBay
from agentbay.session_params import CreateSessionParams

agent_bay = AgentBay(api_key="your-api-key")

# Create CodeSpace session
session_params = CreateSessionParams(image_id="code_latest")
result = agent_bay.create(session_params)

if result.success:
    session = result.session
    
    # Execute Python code
    code = "print('Hello from CodeSpace!')"
    result = session.code.run_code(code, "python")
    
    agent_bay.delete(session)
```

## 📖 Learn More

- [Code Execution Guide](code-execution.md) - Detailed code execution documentation
- [Main Documentation](../README.md) - Back to main guides

## 🆘 Getting Help

- [GitHub Issues](https://github.com/aliyun/wuying-agentbay-sdk/issues)
- [API Reference](../../api-reference.md)
