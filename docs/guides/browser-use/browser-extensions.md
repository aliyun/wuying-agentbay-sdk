# Browser Extension Management Guide

This guide covers how to use browser extensions with the AgentBay SDK for automated testing and browser automation workflows.

## Overview

The AgentBay SDK provides comprehensive browser extension management capabilities, allowing you to:

- Upload and manage browser extensions in the cloud
- Automatically synchronize extensions to browser sessions
- Test extension functionality in controlled environments
- Develop and iterate on extensions with cloud infrastructure

## Prerequisites

- AgentBay Python SDK installed (`pip install wuying-agentbay-sdk`)
- Valid AgentBay API key
- Browser extension packaged as ZIP file
- Basic understanding of browser automation concepts

## Quick Start

### 1. Basic Extension Upload and Usage

```python
import os
from agentbay import AgentBay, ExtensionsService, CreateSessionParams
from agentbay import BrowserContext

# Initialize AgentBay client
agent_bay = AgentBay(api_key=os.getenv("AGENTBAY_API_KEY"))

# Initialize extensions service (auto-creates context)
extensions_service = ExtensionsService(agent_bay)

try:
    # Upload extension to cloud
    extension_path = "/path/to/your-extension.zip"
    
    if not os.path.exists(extension_path):
        print(f"❌ Extension file not found: {extension_path}")
        exit(1)
    
    print(f"📦 Uploading extension: {extension_path}")
    extension = extensions_service.create(extension_path)
    print(f"✅ Extension uploaded successfully!")
    print(f"   - Name: {extension.name}")
    print(f"   - ID: {extension.id}")
    
    # Create extension option for browser session
    ext_option = extensions_service.create_extension_option([extension.id])
    
    # Create browser session with extension
    session_params = CreateSessionParams(
        labels={"purpose": "extension_testing", "type": "demo"},
        browser_context=BrowserContext(
            context_id="extension_test_session",
            auto_upload=True,  # Enable automatic extension synchronization
            extension_option=ext_option
        )
    )
    
    # Create session - extension will be automatically synchronized
    session_result = agent_bay.create(session_params)
    if not session_result.success:
        print(f"❌ Failed to create session: {session_result.error_message}")
        exit(1)
    
    session = session_result.session
    print(f"✅ Browser session created successfully!")
    print(f"   - Session ID: {session.session_id}")
    print(f"   - Extensions synchronized to: /tmp/extensions/")
    
    # List available extensions in context
    extensions = extensions_service.list()
    for ext in extensions:
        print(f"   - {ext.name} (ID: {ext.id})")

finally:
    # Clean up resources
    extensions_service.cleanup()
    print("✅ Cleanup completed")
```

### 2. Working with Multiple Extensions

```python
import os
from agentbay import AgentBay, ExtensionsService, CreateSessionParams
from agentbay import BrowserContext

agent_bay = AgentBay(api_key=os.getenv("AGENTBAY_API_KEY"))
extensions_service = ExtensionsService(agent_bay, "multi_ext_demo")

try:
    # List of extension paths
    extension_paths = [
        "/path/to/extension1.zip",
        "/path/to/extension2.zip",
        "/path/to/extension3.zip"
    ]
    
    # Filter existing files
    existing_paths = [path for path in extension_paths if os.path.exists(path)]
    if not existing_paths:
        print("❌ No extension files found")
        exit(1)
    
    print(f"📦 Uploading {len(existing_paths)} extensions...")
    
    # Upload all extensions
    extension_ids = []
    for path in existing_paths:
        ext = extensions_service.create(path)
        extension_ids.append(ext.id)
        print(f"   ✅ {ext.name} uploaded (ID: {ext.id})")
    
    # Create session with all extensions
    ext_option = extensions_service.create_extension_option(extension_ids)
    
    session_params = CreateSessionParams(
        labels={"purpose": "multiple_extensions", "count": str(len(extension_ids))},
        browser_context=BrowserContext(
            context_id="multi_extension_session",
            auto_upload=True,
            extension_option=ext_option
        )
    )
    
    session_result = agent_bay.create(session_params)
    session = session_result.session
    
    print(f"✅ Session created with {len(extension_ids)} extensions!")
    print(f"   - Session ID: {session.session_id}")

finally:
    extensions_service.cleanup()
```

## Core Concepts

### Extension Context Management

The SDK automatically manages extension storage contexts:

- **Auto-creation**: If no context is specified, a unique context is created automatically
- **Context reuse**: Specify a context name to reuse existing extension storage
- **Automatic cleanup**: Contexts created by the service can be automatically cleaned up

```python
# Auto-generated context (recommended for simple use cases)
extensions_service = ExtensionsService(agent_bay)

# Named context (recommended for persistent extension management)
extensions_service = ExtensionsService(agent_bay, "my_project_extensions")

# Context will be created if it doesn't exist
```

### Extension Synchronization

Extensions are automatically synchronized to browser sessions:

- **Automatic sync**: No manual intervention required
- **File location**: Extensions available at `/tmp/extensions/{extension_id}/` in sessions
- **Session isolation**: Each session gets its own copy of extensions

## Common Workflows

### Extension Development and Testing

```python
import os
import time
from typing import Optional
from agentbay import AgentBay, ExtensionsService, CreateSessionParams
from agentbay import BrowserContext

class ExtensionDevelopmentWorkflow:
    """
    A helper class for extension development and testing workflow.
    
    This class provides methods to:
    - Upload extensions for development
    - Create test sessions with extensions
    - Update extensions during development
    - Manage development lifecycle
    """
    
    def __init__(self, api_key: str, project_name: str = "dev_extensions"):
        """Initialize the development workflow."""
        self.agent_bay = AgentBay(api_key=api_key)
        self.extensions_service = ExtensionsService(self.agent_bay, project_name)
        self.extension_id: Optional[str] = None
        self.project_name = project_name
        
        print(f"🛠️  Extension Development Workflow initialized")
        print(f"   - Project: {project_name}")
    
    def upload_extension(self, extension_path: str) -> str:
        """Upload an extension for development testing."""
        try:
            print(f"📦 Uploading extension: {os.path.basename(extension_path)}")
            
            if not os.path.exists(extension_path):
                raise FileNotFoundError(f"Extension file not found: {extension_path}")
            
            extension = self.extensions_service.create(extension_path)
            self.extension_id = extension.id
            
            print(f"✅ Extension uploaded successfully!")
            print(f"   - Name: {extension.name}")
            print(f"   - ID: {extension.id}")
            
            return extension.id
            
        except Exception as e:
            print(f"❌ Upload failed: {e}")
            raise
    
    def update_extension(self, new_extension_path: str) -> str:
        """Update existing extension during development."""
        if not self.extension_id:
            raise ValueError("No extension uploaded yet. Call upload_extension() first.")
        
        try:
            print(f"🔄 Updating extension: {os.path.basename(new_extension_path)}")
            
            updated_ext = self.extensions_service.update(self.extension_id, new_extension_path)
            
            print(f"✅ Extension updated successfully!")
            print(f"   - Name: {updated_ext.name}")
            print(f"   - ID: {self.extension_id}")
            
            return self.extension_id
            
        except Exception as e:
            print(f"❌ Update failed: {e}")
            raise
    
    def create_test_session(self, session_name: Optional[str] = None):
        """Create a browser session with the current extension for testing."""
        if not self.extension_id:
            raise ValueError("No extension available. Upload an extension first.")
        
        try:
            # Generate session name if not provided
            if not session_name:
                timestamp = int(time.time())
                session_name = f"dev_session_{timestamp}"
            
            print(f"🌐 Creating test session: {session_name}")
            
            # Create extension option
            ext_option = self.extensions_service.create_extension_option([self.extension_id])
            
            # Create session parameters
            session_params = CreateSessionParams(
                labels={
                    "purpose": "extension_development",
                    "project": self.project_name,
                    "extension_id": self.extension_id
                },
                browser_context=BrowserContext(
                    context_id=session_name,
                    auto_upload=True,
                    extension_option=ext_option
                )
            )
            
            # Create session
            session_result = self.agent_bay.create(session_params)
            if not session_result.success:
                raise Exception(f"Session creation failed: {session_result.error_message}")
            
            session = session_result.session
            
            print(f"✅ Test session created successfully!")
            print(f"   - Session ID: {session.session_id}")
            print(f"   - Extension available at: /tmp/extensions/{self.extension_id}/")
            
            return session
            
        except Exception as e:
            print(f"❌ Session creation failed: {e}")
            raise
    
    def cleanup(self):
        """Clean up development resources."""
        try:
            print("🧹 Cleaning up development resources...")
            
            if self.extension_id:
                deleted = self.extensions_service.delete(self.extension_id)
                if deleted:
                    print(f"   ✅ Deleted extension: {self.extension_id}")
            
            self.extensions_service.cleanup()
            print("✅ Cleanup completed")
            
        except Exception as e:
            print(f"❌ Cleanup failed: {e}")

# Usage
workflow = ExtensionDevelopmentWorkflow(api_key=os.getenv("AGENTBAY_API_KEY"))
try:
    # Development cycle
    workflow.upload_extension("/path/to/extension-v1.zip")
    session1 = workflow.create_test_session()
    # Test extension functionality...

    # Update and test again
    workflow.update_extension("/path/to/extension-v2.zip")
    session2 = workflow.create_test_session()
    # Test updated functionality...

finally:
    workflow.cleanup()
```

### Automated Extension Testing

```python
import os
import time
from typing import List
from agentbay import AgentBay, ExtensionsService, CreateSessionParams
from agentbay import BrowserContext

def run_extension_tests(extension_paths: List[str]) -> bool:
    """Run automated tests on multiple extensions."""
    
    api_key = os.getenv("AGENTBAY_API_KEY")
    if not api_key:
        print("❌ Please set AGENTBAY_API_KEY environment variable")
        return False
    
    agent_bay = AgentBay(api_key=api_key)
    extensions_service = ExtensionsService(agent_bay, "automated_tests")
    
    try:
        print(f"🚀 Starting automated extension tests...")
        
        # Upload all test extensions
        extension_ids = []
        for path in extension_paths:
            if not os.path.exists(path):
                print(f"⚠️  Extension not found: {path}")
                continue
            
            ext = extensions_service.create(path)
            extension_ids.append(ext.id)
            print(f"   ✅ {ext.name} uploaded (ID: {ext.id})")
        
        if not extension_ids:
            raise Exception("No extensions uploaded successfully")
        
        # Create test session
        ext_option = extensions_service.create_extension_option(extension_ids)
        
        session_params = CreateSessionParams(
            labels={
                "purpose": "automated_testing",
                "test_type": "extension_validation",
                "extension_count": str(len(extension_ids))
            },
            browser_context=BrowserContext(
                context_id="auto_test_session",
                auto_upload=True,
                extension_option=ext_option
            )
        )
        
        session_result = agent_bay.create(session_params)
        if not session_result.success:
            raise Exception(f"Session creation failed: {session_result.error_message}")
        
        session = session_result.session
        print(f"✅ Test session created: {session.session_id}")
        
        # Wait for extension synchronization
        print("⏳ Waiting for extension synchronization...")
        time.sleep(5)  # Give time for extensions to sync
        
        # Run your extension tests here
        # Extensions are available at /tmp/extensions/ in the session
        test_passed = True
        for extension_id in extension_ids:
            print(f"🧪 Testing extension: {extension_id}")
            
            # Example: Check if extension files exist
            result = session.command.execute(f"ls /tmp/extensions/{extension_id}/")
            if result.success and "manifest.json" in result.output:
                print(f"   ✅ Extension loaded successfully")
            else:
                print(f"   ❌ Extension not found or invalid")
                test_passed = False
        
        return test_passed
    
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
    finally:
        extensions_service.cleanup()

# Usage
if __name__ == "__main__":
    test_extensions = [
        "/path/to/test-extension-1.zip",
        "/path/to/test-extension-2.zip"
    ]
    
    success = run_extension_tests(test_extensions)
    print(f"\n🎯 Test result: {'✅ PASSED' if success else '❌ FAILED'}")
```

## Best Practices

### 1. Context Management

✅ **Do:**

- Use descriptive context names for persistent projects
- Let the service auto-generate contexts for simple use cases
- Always call `cleanup()` in finally blocks

❌ **Don't:**

- Hardcode context IDs in your application code
- Forget to clean up auto-created contexts
- Mix extensions from different projects in the same context

### 2. Extension File Management

✅ **Do:**

- Use ZIP format for all extension packages
- Validate file existence before upload
- Include proper manifest.json in extensions
- Handle upload errors gracefully

❌ **Don't:**

- Upload uncompressed extension directories
- Skip file validation steps
- Ignore upload error responses

### 3. Session Management

✅ **Do:**

- Use meaningful labels for sessions
- Wait for extension synchronization before testing
- Create one ExtensionOption per session

❌ **Don't:**

- Start testing immediately after session creation
- Reuse ExtensionOption across multiple sessions
- Forget to specify browser_context when using extensions

### 4. Error Handling

```python
import os
from agentbay import AgentBay, ExtensionsService, CreateSessionParams
from agentbay import BrowserContext

def robust_extension_workflow():
    """Example of robust error handling in extension workflows."""
    extensions_service = None
    
    try:
        # Initialize with API key
        api_key = os.getenv("AGENTBAY_API_KEY")
        if not api_key:
            raise ValueError("AGENTBAY_API_KEY environment variable not set")
        
        agent_bay = AgentBay(api_key=api_key)
        extensions_service = ExtensionsService(agent_bay, "production_extensions")
        
        # Validate extension file
        extension_path = "/path/to/production-extension.zip"
        if not os.path.exists(extension_path):
            raise FileNotFoundError(f"Extension not found: {extension_path}")
        
        print(f"📦 Uploading extension: {extension_path}")
        
        # Upload with error handling
        extension = extensions_service.create(extension_path)
        print(f"✅ Extension uploaded: {extension.id}")
        
        # Create session with validation
        ext_option = extensions_service.create_extension_option([extension.id])
        
        session_params = CreateSessionParams(
            labels={"environment": "production", "purpose": "extension_deployment"},
            browser_context=BrowserContext(
                context_id="production_session",
                auto_upload=True,
                extension_option=ext_option
            )
        )
        
        print("🌐 Creating production session...")
        session_result = agent_bay.create(session_params)
        
        if not session_result.success:
            raise Exception(f"Session creation failed: {session_result.error_message}")
        
        session = session_result.session
        print(f"✅ Production session created: {session.session_id}")
        
        return session
    
    except FileNotFoundError as e:
        print(f"❌ File error: {e}")
        return None
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None
    finally:
        if extensions_service:
            print("🧹 Cleaning up resources...")
            extensions_service.cleanup()
            print("✅ Cleanup completed")

# Usage
if __name__ == "__main__":
    session = robust_extension_workflow()
    if session:
        print(f"🎉 Workflow completed successfully!")
    else:
        print(f"❌ Workflow failed")
```

## Troubleshooting

### Common Issues

**Extension not found in session:**

- Check that extension was uploaded successfully
- Verify session was created with proper ExtensionOption
- Wait for synchronization to complete before accessing files

**Upload failures:**

- Ensure file is in ZIP format
- Check file permissions and accessibility
- Verify API key and network connectivity

**Context errors:**

- Use unique context names to avoid conflicts
- Don't mix extensions from different sources
- Clean up contexts when no longer needed

### Debugging Tips

```python
import os
import logging
from agentbay import AgentBay, ExtensionsService

# Enable verbose logging
logging.basicConfig(level=logging.DEBUG)

# Initialize services
agent_bay = AgentBay(api_key=os.getenv("AGENTBAY_API_KEY"))
extensions_service = ExtensionsService(agent_bay, "debug_context")

try:
    # Check extension list
    extensions = extensions_service.list()
    print(f"📋 Available extensions: {len(extensions)}")
    for ext in extensions:
        print(f"   - {ext.name} (ID: {ext.id})")
    
    # Upload and validate extension
    extension_path = "/path/to/your-extension.zip"
    if os.path.exists(extension_path):
        extension = extensions_service.create(extension_path)
        print(f"✅ Extension uploaded: {extension.id}")
        
        # Create extension option
        ext_option = extensions_service.create_extension_option([extension.id])
        print(f"🔧 Extension option created: {ext_option}")
        
        # Create session with detailed error checking
        from agentbay import CreateSessionParams, BrowserContext
        
        session_params = CreateSessionParams(
            labels={"purpose": "debugging"},
            browser_context=BrowserContext(
                context_id="debug_session",
                auto_upload=True,
                extension_option=ext_option
            )
        )
        
        session_result = agent_bay.create(session_params)
        
        if not session_result.success:
            print(f"❌ Session creation failed: {session_result.error_message}")
        else:
            print(f"✅ Session created: {session_result.session.session_id}")
    else:
        print(f"❌ Extension file not found: {extension_path}")

finally:
    extensions_service.cleanup()
```

## Integration with Browser Automation

Extensions work seamlessly with browser automation tools:

```python
import os
from playwright.sync_api import sync_playwright
from agentbay import AgentBay, ExtensionsService, CreateSessionParams
from agentbay import BrowserContext

def create_extension_session():
    """Create a browser session with extensions."""
    agent_bay = AgentBay(api_key=os.getenv("AGENTBAY_API_KEY"))
    extensions_service = ExtensionsService(agent_bay)
    
    try:
        # Upload extension
        extension = extensions_service.create("/path/to/extension.zip")
        ext_option = extensions_service.create_extension_option([extension.id])
        
        # Create session
        session_params = CreateSessionParams(
            labels={"purpose": "browser_automation"},
            browser_context=BrowserContext(
                context_id="automation_session",
                auto_upload=True,
                extension_option=ext_option
            )
        )
        
        session_result = agent_bay.create(session_params)
        return session_result.session
    
    except Exception as e:
        print(f"❌ Failed to create session: {e}")
        raise

# Create session with extensions
session = create_extension_session()

# Get browser endpoint
endpoint_url = session.browser.get_endpoint_url()

# Connect with Playwright
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(endpoint_url)
    context = browser.contexts[0]
    page = context.new_page()
    
    # Extensions are already loaded and available
    page.goto("https://example.com")
    
    # Your extension should be active here
    # Test extension functionality...
    print(f"✅ Page loaded with extension active")
    
    browser.close()
```

## 📚 Related Guides

- [Extension Management](core-features/extension.md) - Detailed extension management guide
- [Browser Context](core-features/browser-context.md) - Persistent browser state management
- [Browser Use Overview](README.md) - Complete browser automation features
- [Session Management](../common-features/basics/session-management.md) - Session lifecycle and configuration

## 🆘 Getting Help

- [GitHub Issues](https://github.com/aliyun/wuying-agentbay-sdk/issues)
- [Documentation Home](../README.md)
