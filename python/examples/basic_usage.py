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

        # Create a new session using a context manager
        print("Creating a new session...")
        with agent_bay.create() as session:
            print(f"Session created with ID: {session.session_id}")

            # Execute a command
            print("\nExecuting a command...")
            result = session.command.execute_command("ls -la")
            print(f"Command result: {result}")

            # Read a file
            print("\nReading a file...")
            content = session.file_system.read_file("/etc/hosts")
            print(f"File content: {content}")

            # Execute an ADB shell command (for mobile environments)
            print("\nExecuting an ADB shell command...")
            adb_result = session.adb.shell("ls /sdcard")
            print(f"ADB shell result: {adb_result}")

        # The session is automatically deleted when exiting the 'with' block
        print("\nSession automatically deleted.")

        # List all sessions
        # This is to demonstrate that the session is no longer active.
        # Depending on AgentBay's list implementation, it might still show if list shows all ever created or recently deleted.
        print("\nListing all sessions...")
        sessions = agent_bay.list()
        print(f"Available sessions: {sessions}")

    except AgentBayError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
