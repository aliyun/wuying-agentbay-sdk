import os
import sys

# Add the parent directory to the path so we can import the agentbay package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agentbay import AgentBay
from agentbay.exceptions import AgentBayError
from agentbay.session_params import CreateSessionParams

def main():
    # Initialize the AgentBay client
    # You can provide the API key as a parameter or set the AGENTBAY_API_KEY environment variable
    api_key = os.environ.get("AGENTBAY_API_KEY") or "your_api_key_here"
    try:
        agent_bay = AgentBay(api_key=api_key)

        # Create a new session
        # image_id: linux_latest, code_latest, windows_latest etc.
        # use linux_latest because it supports "shell" command
        params = CreateSessionParams(
            image_id="linux_latest",
        )
        print("Creating a new session...")
        session_result = agent_bay.create(params)
        print(f"Session created with ID: {session_result.session.session_id}")
        print(f"Request ID: {session_result.request_id}")

        # Get the session object from the result
        session = session_result.session

        # Execute a command
        print("\nExecuting a command...")
        success, result = session.command.execute_command("ls -la")
        print(f"Command execution success: {success}")
        if success:
            print(f"Command output: {result}")
        else:
            print(f"Command error: {result}")

        # Read a file
        print("\nReading a file...")
        success, content = session.file_system.read_file("/etc/hosts")
        print(f"File reading success: {success}")
        if success:
            print(f"File content: {content}")
        else:
            print(f"File reading error: {content}")

        # Get session link
        print("\nGetting session link...")
        link_result = session.get_link()
        print(f"Link request ID: {link_result.request_id}")
        print(f"Link: {link_result.data}")

        # List all sessions
        print("\nListing all sessions...")
        sessions_result = agent_bay.list()
        print(f"Available sessions count: {len(sessions_result.sessions)}")
        for s in sessions_result.sessions:
            print(f"Session ID: {s.session_id}")

        # Delete the session
        print("\nDeleting the session...")
        delete_result = agent_bay.delete(session)
        print(f"Delete operation request ID: {delete_result.request_id}")
        print(f"Delete operation success: {delete_result.success}")
        print("Session deleted successfully")

    except AgentBayError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
