# Python SDK for Wuying AgentBay

This directory contains the Python implementation of the Wuying AgentBay SDK.

## Prerequisites

- Python 3.12 or later
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
from wuying_agentbay import AgentBay
from wuying_agentbay.exceptions import AgentBayError
from wuying_agentbay.session_params import CreateSessionParams

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
        session = agent_bay.create(params)
        print(f"Session created with ID: {session.session_id}")

        # Execute a command
        result = session.command.execute_command("ls -la")
        print(f"Command result: {result}")

        # Read a file
        content = session.filesystem.read_file("/path/to/file.txt")
        print(f"File content: {content}")

        # Run code
        python_code = """
import os
import platform

print(f"Current working directory: {os.getcwd()}")
print(f"Python version: {platform.python_version()}")
"""
        code_result = session.command.run_code(python_code, "python")
        print(f"Code execution result: {code_result}")

        # Get installed applications
        apps = session.application.get_installed_apps(include_system_apps=True,
                                                     include_store_apps=False,
                                                     include_desktop_apps=True)
        print(f"Found {len(apps)} installed applications")

        # List visible applications
        processes = session.application.list_visible_apps()
        print(f"Found {len(processes)} visible applications")

        # List root windows
        windows = session.window.list_root_windows()
        print(f"Found {len(windows)} root windows")

        # Get active window
        active_window = session.window.get_active_window()
        print(f"Active window: {active_window.title}")

        # Get session labels
        labels = session.get_labels()
        print(f"Session labels: {labels}")

        # List sessions by labels
        filtered_sessions = agent_bay.list_by_labels({
            "purpose": "demo"
        })
        print(f"Found {len(filtered_sessions)} matching sessions")

        # Clean up
        agent_bay.delete(session)
        print("Session deleted successfully")

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
