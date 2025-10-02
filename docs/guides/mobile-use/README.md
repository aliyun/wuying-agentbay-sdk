# Mobile Use Guide

Mobile Use is AgentBay's mobile device automation environment for app testing, UI interaction, and gesture-based automation on Android/iOS devices.

## 📚 Documentation

### Core Features
- [Application Management](application-management.md) - Mobile app lifecycle and process management
- [Mobile UI Automation](mobile-ui-automation.md) - Touch gestures, UI elements, and input

## 🎯 What is Mobile Use?

Mobile Use (`mobile_latest` image) provides a mobile device simulation environment for:

- **Application Management** - Start, stop, and manage mobile applications
- **UI Element Detection** - Identify and locate UI elements
- **Touch Interactions** - Tap, swipe, and multi-touch gestures
- **Text Input** - Keyboard input and text entry
- **Key Events** - Send hardware key events (Home, Menu, Back, etc.)
- **Screenshot Capture** - Visual verification and debugging
- **Activity Management** - Launch specific Android activities

## 🚀 Quick Start

```python
import os
from agentbay import AgentBay
from agentbay.session_params import CreateSessionParams

api_key = os.getenv("AGENTBAY_API_KEY")
agent_bay = AgentBay(api_key=api_key)

session_params = CreateSessionParams(image_id="mobile_latest")
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

- [Application Management Guide](application-management.md) - Mobile app management
- [Mobile UI Automation Guide](mobile-ui-automation.md) - Touch gestures and UI interaction
- [Main Documentation](../../README.md) - Back to main guides

## 🆘 Getting Help

- [GitHub Issues](https://github.com/aliyun/wuying-agentbay-sdk/issues)
- [API Reference](../../api-reference.md)
