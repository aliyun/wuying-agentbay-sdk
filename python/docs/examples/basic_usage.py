from agentbay.session_params import CreateSessionParams
from agentbay.exceptions import AgentBayError
from agentbay import AgentBay
import os
import sys

# Add the parent directory to the path so we can import the agentbay package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def main():
    # Initialize the AgentBay client
    # You can provide the API key as a parameter or set the AGENTBAY_API_KEY
    # environment variable
    api_key = os.environ.get("AGENTBAY_API_KEY") or "your_api_key_here"
    session = None
    linux_session = None
    try:
        agent_bay = AgentBay(api_key=api_key)

        # Create a new session
        # image_id: linux_latest, code_latest, windows_latest etc.
        # use linux_latest because it supports "shell" command
        params = CreateSessionParams(
            image_id="browser_latest",
        )
        print("Creating a new session...")
        session_result = agent_bay.create(params)
        print(f"Session created with ID: {session_result.session.session_id}")
        print(f"Request ID: {session_result.request_id}")

        # Get the session object from the result
        session = session_result.session

        # Execute a command
        print("\nExecuting a command...")
        result = session.command.execute_command("ls -la")
        print(f"Command execution success: {result.success}")
        if result.success:
            print(f"Command output: {result.output}")
        else:
            print(f"Command error: {result.error_message}")

        # Read a file
        print("\nReading a file...")
        result = session.file_system.read_file("/etc/hosts")
        print(f"File reading success: {result.success}")
        if result.success:
            print(f"File content: {result.content}")
        else:
            print(f"File reading error: {result.error_message}")

        # Get session link
        print("\nGetting session link...")
        link_result = session.get_link()
        print(f"Link request ID: {link_result.request_id}")
        print(f"Link: {link_result.data}")

         # Test get_link with port 8080
        print("\nTesting get_link with port 8080...")
        link_result_port_8080 = session.get_link(None, 8080)
        print(f"Link with port 8080 request ID: {link_result_port_8080.request_id}")
        print(f"Link with port 8080: {link_result_port_8080.data}")

        # Create a new Linux session for testing get_link with parameters
        print("\n=== Testing Linux Session with get_link parameters ===")
        linux_params = CreateSessionParams(
            image_id="linux_latest",
        )
        print("Creating a linux_latest session...")
        linux_session_result = agent_bay.create(linux_params)
        print(f"Linux session created with ID: {linux_session_result.session.session_id}")
        print(f"Request ID: {linux_session_result.request_id}")

        # Get the Linux session object from the result
        linux_session = linux_session_result.session

        # Test get_link with parameters (protocol_type="https", port=443)
        print("\nTesting get_link with parameters (https, 443)...")
        link_result_with_params = linux_session.get_link("https", 443)
        print(f"Link with params request ID: {link_result_with_params.request_id}")
        print(f"Link with params: {link_result_with_params.data}")

        # List all sessions
        print("\nListing all sessions...")
        sessions_result = agent_bay.list()
        print(f"Available sessions count: {len(sessions_result)}")
        for s in sessions_result:
            print(f"Session ID: {s.session_id}")

        # Delete the browser session
        print("\nDeleting the browser session...")
        delete_result = agent_bay.delete(session)
        session = None
        print(f"Delete operation request ID: {delete_result.request_id}")
        print(f"Delete operation success: {delete_result.success}")
        print("Browser session deleted successfully")

        # Delete the Linux session
        print("\nDeleting the Linux session...")
        linux_delete_result = agent_bay.delete(linux_session)
        linux_session = None
        print(f"Linux delete operation request ID: {linux_delete_result.request_id}")
        print(f"Linux delete operation success: {linux_delete_result.success}")
        print("Linux session deleted successfully")

    except AgentBayError as e:
        print(f"AgentBay error: {e}")
        if session:
            try:
                agent_bay.delete(session)
                print("Browser session deleted during AgentBayError handling")
            except Exception as delete_error:
                print(f"Failed to delete browser session during error handling: {delete_error}")
        if linux_session:
            try:
                agent_bay.delete(linux_session)
                print("Linux session deleted during AgentBayError handling")
            except Exception as delete_error:
                print(f"Failed to delete Linux session during error handling: {delete_error}")
    except Exception as e:
        print(f"Unexpected error: {e}")
        if session:
            try:
                agent_bay.delete(session)
                print("Browser session deleted during other error handling")
            except Exception as delete_error:
                print(f"Failed to delete browser session during error handling: {delete_error}")
        if linux_session:
            try:
                agent_bay.delete(linux_session)
                print("Linux session deleted during other error handling")
            except Exception as delete_error:
                print(f"Failed to delete Linux session during error handling: {delete_error}")

if __name__ == "__main__":
    main()
