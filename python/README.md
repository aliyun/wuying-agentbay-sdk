# Python SDK for Wuying AgentBay

This directory contains the Python implementation of the Wuying AgentBay SDK.

## Prerequisites

- Python 3.10 or later
- Poetry (for development)

## Installation

### For Development

Clone the repository and install dependencies using Poetry:

```bash
git clone https://github.com/aliyun/wuying-agentbay-sdk.git
cd wuying-agentbay-sdk/python
poetry install
```

### For Usage in Your Project

```bash
pip install wuying-agentbay-sdk
```

## Running Examples

You can find examples in the `docs/examples/python` directory, including:

- Basic SDK usage
- Context management
- Label management
- Mobile system integration
- OSS management
- File system operations
- Session creation

To run the examples:

```bash
# Using Poetry
poetry run python docs/examples/python/basic_usage.py

# Or directly with Python if installed in your environment
python docs/examples/python/basic_usage.py
```

## Python-Specific Usage

```python
from agentbay import AgentBay
from agentbay.exceptions import AgentBayError
from agentbay.session_params import CreateSessionParams

def main():
    # Initialize with API key
    api_key = "your_api_key"  # Or use os.environ.get("AGENTBAY_API_KEY")

    try:
        agent_bay = AgentBay(api_key=api_key)

        # Create a session with labels
        params = CreateSessionParams()
        params.labels = {
            "purpose": "demo",
            "environment": "development"
        }
        session_result = agent_bay.create(params)
        session = session_result.session
        
        # Execute a command
        cmd_result = session.command.execute_command("ls -la")
        
        # Read a file
        file_result = session.file_system.read_file("/path/to/file.txt")
        
        # Run code
        code_result = session.code.run_code("print('Hello, World!')", "python")
        
        # Application management
        apps_result = session.application.get_installed_apps(
            include_system_apps=True,
            include_store_apps=False,
            include_desktop_apps=True
        )
        
        # Window management
        windows_result = session.window.list_root_windows()
        window_result = session.window.get_active_window()
        
        # UI interactions
        screenshot_result = session.ui.screenshot()
        session.ui.send_key(3)  # Send HOME key
        
        # OSS operations
        upload_result = session.oss.upload_file("/local/path/file.txt", "remote/path/")
        
        # Context management
        contexts_result = agent_bay.context.list()
        
        # Session labels
        labels_result = session.get_labels()
        
        # Clean up
        delete_result = agent_bay.delete(session)

    except AgentBayError as e:
        print(f"Error: {e}")
```

## Key Features

### Session Management

- Create sessions with optional parameters (image_id, context_id, labels)
- List sessions with pagination and filtering by labels
- Delete sessions and clean up resources
- Manage session labels
- Get session information and links

### Command Execution

- Execute shell commands
- Run code in various languages
- Get command output and execution status

### File System Operations

- Read and write files
- List directory contents
- Create and delete files and directories
- Get file information

### UI Interaction

- Take screenshots
- Find UI elements by criteria
- Click on UI elements
- Send text input
- Perform swipe gestures
- Send key events (HOME, BACK, MENU, etc.)

### Application Management

- Get installed applications
- List running applications
- Start and stop applications
- Get application information

### Window Management

- List windows
- Get active window
- Focus, resize, and move windows
- Get window properties

### Context Management

- Create, list, and delete contexts
- Bind sessions to contexts
- Synchronize context data using policies
- Get context information

### OSS Integration

- Upload files to OSS
- Download files from OSS
- Initialize OSS environment

### Mobile System Support

- Special UI interactions for mobile environments
- Support for mobile application management
- Touch and gesture simulation

## Response Format

All API methods return responses that include:

- `request_id`: A unique identifier for the request
- `success`: A boolean indicating whether the operation was successful
- Operation-specific data (varies by method)
- `error_message`: Error details if the operation failed

## Development

### Building the SDK

```bash
poetry build
```

### Running Tests

```bash
poetry run pytest
```

For more detailed documentation, refer to the [SDK Documentation](../docs/README.md).
