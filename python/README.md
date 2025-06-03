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

def main():
    # Initialize with API key
    api_key = "your_api_key"  # Or use os.environ.get("AGENTBAY_API_KEY")
    
    try:
        agent_bay = AgentBay(api_key=api_key)
        
        # Create a session
        session = agent_bay.create()
        print(f"Session created with ID: {session.session_id}")
        
        # Execute a command
        result = session.command.execute_command("ls -la")
        print(f"Command result: {result}")
        
        # Read a file
        content = session.file_system.read_file("/path/to/file.txt")
        print(f"File content: {content}")
        
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

For more detailed documentation, please refer to the main [README](../README.md) and [SDK Reference](../SDK_Reference.md) in the project root.
