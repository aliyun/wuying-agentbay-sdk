import os
import sys
import time

# Add the parent directory to the path so we can import the agentbay package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agentbay import AgentBay
from agentbay.exceptions import AgentBayError


def main():
    # Initialize the AgentBay client
    # You can provide the API key as a parameter or set the AGENTBAY_API_KEY environment variable
    api_key = os.environ.get("AGENTBAY_API_KEY") or "your_api_key_here"
    try:
        agent_bay = AgentBay(api_key=api_key)

        # Create a new session
        print("Creating a new session...")
        session = agent_bay.create()
        print(f"Session created with ID: {session.session_id}")

        # Execute a command
        print("\nExecuting a command...")
        result = session.command.execute_command("ls -la")
        print(f"Command result: {result}")

        # Read a file
        print("\nReading a file...")
        content = session.file_system.read_file("/etc/hosts")
        print(f"File content: {content}")

        # List all sessions
        print("\nListing all sessions...")
        sessions = agent_bay.list()
        print(f"Available sessions: {sessions}")

        # Delete the session
        print("\nDeleting the session...")
        agent_bay.delete(session)
        print("Session deleted successfully")

    except AgentBayError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
