# Computer Use Guide

Computer Use is AgentBay's desktop automation environment for controlling applications and managing windows on Windows and Linux systems.

## 📚 Documentation

### Core Features
- [Application Management](application-management.md) - Desktop application lifecycle and process management
- [Window Management](window-management.md) - Window control, positioning, and focus management
- [Computer UI Automation](computer-ui-automation.md) - Mouse, keyboard, and UI interaction

## 🎯 What is Computer Use?

Computer Use (`windows_latest` or `linux_latest` images) provides a full desktop environment for:

- **Application Management** - Start, stop, and list desktop applications
- **Window Operations** - Maximize, minimize, resize, and close windows
- **Focus Management** - Control window focus and activation
- **Mouse & Keyboard** - Automated mouse clicks and keyboard input
- **Desktop Automation** - Automate complex desktop workflows

## 🚀 Quick Start

```python
import os
from agentbay import AgentBay
from agentbay.session_params import CreateSessionParams

api_key = os.getenv("AGENTBAY_API_KEY")
agent_bay = AgentBay(api_key=api_key)

session_params = CreateSessionParams(image_id="linux_latest")
result = agent_bay.create(session_params)

if result.success:
    session = result.session
    
    apps_result = session.application.get_installed_apps(
        start_menu=True,
        desktop=False,
        ignore_system_apps=True
    )
    
    if apps_result.success and apps_result.data:
        app = apps_result.data[0]
        start_result = session.application.start_app(app.start_cmd)
        
        if start_result.success:
            print(f"Started {app.name}")
    
    agent_bay.delete(session)
```

## 📖 Learn More

- [Application Management Guide](application-management.md) - Desktop application management
- [Window Management Guide](window-management.md) - Window control and positioning
- [Computer UI Automation Guide](computer-ui-automation.md) - Mouse and keyboard automation
- [Main Documentation](../../README.md) - Back to main guides

## 🆘 Getting Help

- [GitHub Issues](https://github.com/aliyun/wuying-agentbay-sdk/issues)
- [API Reference](../../api-reference.md)
