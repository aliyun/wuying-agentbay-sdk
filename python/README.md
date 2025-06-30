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

You can run the example file:

```bash
# Using Poetry
poetry run python examples/basic_usage.py

# Or directly with Python if installed in your environment
python examples/basic_usage.py
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
        print(f"Session created with ID: {session.session_id}")
        print(f"Request ID: {session_result.request_id}")

        # Execute a command
        cmd_result = session.command.execute_command("ls -la")
        print(f"Command success: {cmd_result.success}")
        print(f"Command output: {cmd_result.output}")
        print(f"Request ID: {cmd_result.request_id}")

        # Read a file
        file_result = session.file_system.read_file("/path/to/file.txt")
        if file_result.success:
            print(f"File content: {file_result.content}")
        else:
            print(f"Error reading file: {file_result.error_message}")
        print(f"Request ID: {file_result.request_id}")

        # Run code
        python_code = """
import os
import platform

print(f"Current working directory: {os.getcwd()}")
print(f"Python version: {platform.python_version()}")
"""
        code_result = session.command.run_code(python_code, "python")
        if code_result.success:
            print(f"Code execution result: {code_result.result}")
        else:
            print(f"Error executing code: {code_result.error_message}")
        print(f"Request ID: {code_result.request_id}")

        # Get installed applications
        apps_result = session.application.get_installed_apps(
            include_system_apps=True,
            include_store_apps=False,
            include_desktop_apps=True
        )
        if apps_result.success:
            print(f"Found {len(apps_result.data)} installed applications")
        print(f"Request ID: {apps_result.request_id}")

        # List visible applications
        processes_result = session.application.list_visible_apps()
        if processes_result.success:
            print(f"Found {len(processes_result.processes)} visible applications")
        print(f"Request ID: {processes_result.request_id}")

        # List root windows
        windows_result = session.window.list_root_windows()
        if windows_result.success:
            print(f"Found {len(windows_result.windows)} root windows")
        print(f"Request ID: {windows_result.request_id}")

        # Get active window
        window_result = session.window.get_active_window()
        if window_result.success:
            print(f"Active window: {window_result.window.title}")
        print(f"Request ID: {window_result.request_id}")

        # Get session labels
        labels_result = session.get_labels()
        if labels_result.success:
            print(f"Session labels: {labels_result.data}")
        print(f"Request ID: {labels_result.request_id}")

        # List sessions by labels
        filtered_result = agent_bay.list_by_labels({
            "purpose": "demo"
        })
        if filtered_result.sessions:
            print(f"Found {len(filtered_result.sessions)} matching sessions")
        print(f"Request ID: {filtered_result.request_id}")

        # Clean up
        delete_result = agent_bay.delete(session)
        print(f"Session deleted successfully: {delete_result.success}")
        print(f"Request ID: {delete_result.request_id}")

    except AgentBayError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
```

## Development

### Building the SDK

```bash
poetry build
```

### Running Tests

```bash
poetry run pytest
```

For more detailed documentation, please refer to the main [README](../README.md) and [SDK Documentation](../docs/README.md) in the project root.
