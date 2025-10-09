# Get API Example

This example demonstrates how to use the `get` API to retrieve a session by its ID.

## Description

The `get` API allows you to retrieve a session object by providing its session ID. This is useful when you have a session ID from a previous operation and want to access or manage that session.

## Prerequisites

- Python 3.8 or higher
- Valid API key set in `AGENTBAY_API_KEY` environment variable
- agentbay package installed

## Installation

```bash
pip install agentbay
```

## Usage

```bash
# Set your API key
export AGENTBAY_API_KEY="your-api-key-here"

# Run the example
python main.py
```

## Code Example

```python
import os
from agentbay import AgentBay

# Initialize AgentBay client
api_key = os.getenv("AGENTBAY_API_KEY")
agentbay = AgentBay(api_key=api_key)

# Retrieve a session by ID
session_id = "your-session-id"
session = agentbay.get(session_id)

print(f"Retrieved session: {session.session_id}")

# Use the session for further operations
# ...
```

## API Reference

### get

```python
def get(session_id: str) -> Session
```

Get a session by its ID.

**Parameters:**
- `session_id` (str): The ID of the session to retrieve

**Returns:**
- `Session`: The Session instance

**Raises:**
- `ValueError`: If `session_id` is not provided or is empty
- `RuntimeError`: If the API call fails or session is not found

## Expected Output

```
Creating a session...
Created session with ID: session-xxxxxxxxxxxxx

Retrieving session using Get API...
Successfully retrieved session:
  Session ID: session-xxxxxxxxxxxxx

Session is ready for use

Cleaning up...
Session session-xxxxxxxxxxxxx deleted successfully
```

## Notes

- The session ID must be valid and from an existing session
- The get API internally calls the GetSession API endpoint
- The returned session object can be used for all session operations (commands, files, etc.)
- Always clean up sessions when done to avoid resource waste

## Error Handling

The `get` method will raise exceptions in the following cases:

1. **ValueError**: When session_id is empty or None
   ```python
   try:
       session = agentbay.get("")
   except ValueError as e:
       print(f"Invalid input: {e}")
   ```

2. **RuntimeError**: When the API call fails or session is not found
   ```python
   try:
       session = agentbay.get("non-existent-session-id")
   except RuntimeError as e:
       print(f"API error: {e}")
   ```

