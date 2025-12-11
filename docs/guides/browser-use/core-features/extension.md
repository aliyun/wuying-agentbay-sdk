# Browser Extension Management

Browser Extension Management is a core feature of the AgentBay SDK that enables you to upload, manage, and synchronize browser extensions with your browser sessions. This is particularly useful for automated testing of browser extensions, web scraping with custom extensions, and browser automation workflows.

## Overview

The Extension Management feature allows you to:
- Upload browser extensions to the cloud
- Manage multiple extensions in a context
- Automatically synchronize extensions to browser sessions
- Test extension functionality in controlled environments
- Update and maintain extensions across sessions

## Key Concepts

### ExtensionsService

The `ExtensionsService` is the main class for managing browser extensions. It handles:
- Extension storage in cloud contexts
- Extension upload and management
- Extension synchronization to sessions
- Automatic cleanup of resources

### ExtensionOption

The `ExtensionOption` encapsulates extension configuration for browser sessions, including:
- Context ID where extensions are stored
- List of extension IDs to synchronize
- Automatic generation of context sync configurations

### Extension Synchronization

Extensions are automatically synchronized to browser sessions at:
- Path: `/tmp/extensions/{extension_id}/` in each session
- Each extension gets its own directory with all extension files
- Session isolation ensures each session has its own copy

## Python Implementation

### Basic Extension Usage

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
    extension = extensions_service.create(extension_path)
    print(f"✅ Extension uploaded successfully!")
    print(f"   - Name: {extension.name}")
    print(f"   - ID: {extension.id}")
    
    # Create extension option for browser session
    ext_option = extensions_service.create_extension_option([extension.id])
    
    # Create browser session with extension
    session_params = CreateSessionParams(
        labels={"purpose": "basic_extension_example", "type": "demo"},
        browser_context=BrowserContext(
            context_id="basic_extension_session",
            auto_upload=True,
            extension_option=ext_option
        )
    )
    
    session_result = agent_bay.create(session_params)
    if not session_result.success:
        print(f"❌ Failed to create session: {session_result.error_message}")
    else:
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
```

### Working with Multiple Extensions

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

### Extension Development Workflow

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
        if not os.path.exists(extension_path):
            raise FileNotFoundError(f"Extension file not found: {extension_path}")
        
        extension = self.extensions_service.create(extension_path)
        self.extension_id = extension.id
        
        print(f"✅ Extension uploaded successfully!")
        print(f"   - Name: {extension.name}")
        print(f"   - ID: {extension.id}")
        
        return extension.id
    
    def update_extension(self, new_extension_path: str) -> str:
        """Update existing extension during development."""
        if not self.extension_id:
            raise ValueError("No extension uploaded yet. Call upload_extension() first.")
        
        updated_ext = self.extensions_service.update(self.extension_id, new_extension_path)
        
        print(f"✅ Extension updated successfully!")
        print(f"   - Name: {updated_ext.name}")
        print(f"   - ID: {self.extension_id}")
        
        return self.extension_id
    
    def create_test_session(self, session_name: Optional[str] = None):
        """Create a browser session with the current extension for testing."""
        if not self.extension_id:
            raise ValueError("No extension available. Upload an extension first.")
        
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
    
    def cleanup(self):
        """Clean up development resources."""
        if self.extension_id:
            deleted = self.extensions_service.delete(self.extension_id)
            if deleted:
                print(f"   ✅ Deleted extension: {self.extension_id}")
        
        self.extensions_service.cleanup()
        print("✅ Cleanup completed")


# Usage example
workflow = ExtensionDevelopmentWorkflow(api_key=os.getenv("AGENTBAY_API_KEY"), 
                                       project_name="my_extension_project")
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

## TypeScript Implementation

### Basic Extension Usage

```typescript
import { AgentBay, ExtensionsService, CreateSessionParams, BrowserContext } from 'wuying-agentbay-sdk';

// Initialize AgentBay and Extensions Service
const agentBay = new AgentBay({ apiKey: "your_api_key" });
const extensionsService = new ExtensionsService(agentBay);

// Upload your extension
const extension = await extensionsService.create("/path/to/your-extension.zip");
console.log(`Extension uploaded: ${extension.name} (ID: ${extension.id})`);

// Create extension option for browser integration
const extOption = extensionsService.createExtensionOption([extension.id]);

// Create browser session with extension
const sessionParams = new CreateSessionParams()
    .withLabels({ purpose: "extension_testing" })
    .withBrowserContext(new BrowserContext(
        "extension_test_session",
        true,
        extOption
    ));

// Create session - extension will be automatically synchronized
const sessionResult = await agentBay.create(sessionParams);
const session = sessionResult.session;

// Extensions are now available at /tmp/extensions/ in the session
console.log("Extension session created successfully!");

// Clean up when done
await extensionsService.cleanup();
```

### Working with Multiple Extensions

```typescript
// Upload multiple extensions
const extensionPaths = [
    "/path/to/extension1.zip",
    "/path/to/extension2.zip",
    "/path/to/extension3.zip"
];

const extensionIds: string[] = [];
for (const path of extensionPaths) {
    const ext = await extensionsService.create(path);
    extensionIds.push(ext.id);
    console.log(`Uploaded: ${ext.name}`);
}

// Create session with all extensions
const extOption = extensionsService.createExtensionOption(extensionIds);

const sessionParams = new CreateSessionParams()
    .withBrowserContext(new BrowserContext(
        "multi_extension_session",
        true,
        extOption
    ));

const session = (await agentBay.create(sessionParams)).session;

// Extensions are available at /tmp/extensions/{extension_id}/
```

## Extension Context Management

The SDK automatically manages extension storage contexts:

### Auto-Generated Contexts

```python
import os
from agentbay import AgentBay, ExtensionsService

agent_bay = AgentBay(api_key=os.getenv("AGENTBAY_API_KEY"))

# Auto-generated context (recommended for simple use cases)
extensions_service = ExtensionsService(agent_bay)
# Context name will be automatically generated as "extensions-{timestamp}"
```

### Named Contexts

```python
import os
from agentbay import AgentBay, ExtensionsService

agent_bay = AgentBay(api_key=os.getenv("AGENTBAY_API_KEY"))

# Named context (recommended for persistent extension management)
extensions_service = ExtensionsService(agent_bay, "my_project_extensions")
# Context will be created if it doesn't exist
```

## Best Practices

1. **Use Named Contexts**: For persistent extension management, use named contexts instead of auto-generated ones
2. **Clean Up Resources**: Always call `cleanup()` to remove auto-created contexts
3. **Validate Extensions**: Ensure your extensions are properly packaged as ZIP files with manifest.json
4. **Handle Errors**: Implement proper error handling for extension operations
5. **Version Control**: Keep track of extension versions for consistent testing

## Extension Requirements

### File Format
- Extensions must be packaged as ZIP files (.zip)
- Standard browser extension structure with manifest.json
- Manifest V2 or V3 format supported

### File Structure
```
your-extension.zip
├── manifest.json
├── background.js
├── content.js
├── popup.html
├── icons/
│   ├── 16.png
│   ├── 48.png
│   └── 128.png
└── ...
```

### Size Limits
- Check AgentBay documentation for current size limits
- Large extensions may affect session startup time

## Error Handling

Common errors and how to handle them:

```python
import os
from agentbay import AgentBay, ExtensionsService

agent_bay = AgentBay(api_key=os.getenv("AGENTBAY_API_KEY"))
extensions_service = ExtensionsService(agent_bay)

try:
    extension_path = "/path/to/extension.zip"
    
    if not os.path.exists(extension_path):
        print(f"❌ Extension file not found: {extension_path}")
    else:
        extension = extensions_service.create(extension_path)
        print(f"✅ Extension uploaded: {extension.name}")
        
except FileNotFoundError as e:
    print(f"❌ Extension file not found: {e}")
except ValueError as e:
    print(f"❌ Invalid extension format: {e}")
except Exception as e:
    print(f"❌ Failed to upload extension: {e}")
finally:
    extensions_service.cleanup()
    print("✅ Cleanup completed")
```

## Advanced Features

### Extension Updates

```python
import os
from agentbay import AgentBay, ExtensionsService

agent_bay = AgentBay(api_key=os.getenv("AGENTBAY_API_KEY"))
extensions_service = ExtensionsService(agent_bay)

# Upload initial extension
extension = extensions_service.create("/path/to/extension-v1.zip")
extension_id = extension.id

# Update the extension with a new version
updated_extension = extensions_service.update(
    extension_id=extension_id,
    new_local_path="/path/to/extension-v2.zip"
)
print(f"✅ Extension updated: {updated_extension.name}")
```

### Listing Extensions

```python
import os
from agentbay import AgentBay, ExtensionsService

agent_bay = AgentBay(api_key=os.getenv("AGENTBAY_API_KEY"))
extensions_service = ExtensionsService(agent_bay, "my_extensions")

# List all extensions in the current context
extensions = extensions_service.list()
print(f"📋 Extensions in context:")
for ext in extensions:
    print(f"   - {ext.name} (ID: {ext.id})")
```

### Deleting Extensions

```python
import os
from agentbay import AgentBay, ExtensionsService

agent_bay = AgentBay(api_key=os.getenv("AGENTBAY_API_KEY"))
extensions_service = ExtensionsService(agent_bay)

# Upload extension
extension = extensions_service.create("/path/to/extension.zip")

# Delete a specific extension
success = extensions_service.delete(extension.id)
if success:
    print(f"✅ Extension deleted successfully: {extension.id}")
else:
    print(f"❌ Failed to delete extension: {extension.id}")
```

## Integration with Browser Context

Extensions integrate seamlessly with Browser Context for persistent browser environments:

```python
import os
from agentbay import AgentBay, ExtensionsService, CreateSessionParams
from agentbay import BrowserContext

agent_bay = AgentBay(api_key=os.getenv("AGENTBAY_API_KEY"))

# Create both browser context and extension service
browser_context_result = agent_bay.context.get("persistent-browser", create=True)
browser_context = browser_context_result.context

extensions_service = ExtensionsService(agent_bay, "project-extensions")

try:
    # Upload extension
    extension = extensions_service.create("/path/to/extension.zip")
    ext_option = extensions_service.create_extension_option([extension.id])
    
    # Use both in session
    session_params = CreateSessionParams(
        labels={"purpose": "persistent_with_extension"},
        browser_context=BrowserContext(
            context_id=browser_context.id,  # Persistent browser state
            auto_upload=True,
            extension_option=ext_option     # Extension integration
        )
    )
    
    session_result = agent_bay.create(session_params)
    session = session_result.session
    
    print(f"✅ Session created with persistent browser state and extensions")
    print(f"   - Session ID: {session.session_id}")
    # Session has both persistent browser state AND extensions
    
finally:
    extensions_service.cleanup()
```

## 📚 Related Guides

- [Browser Context](browser-context.md) - Persistent browser state management
- [Session Management](../../common-features/basics/session-management.md) - Session lifecycle and configuration
- [Browser Use Overview](../README.md) - Complete browser automation features

## 🆘 Getting Help

- [GitHub Issues](https://github.com/aliyun/wuying-agentbay-sdk/issues)
- [Documentation Home](../../README.md)