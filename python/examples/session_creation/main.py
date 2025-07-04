#!/usr/bin/env python3

import os

from agentbay import AgentBay
from agentbay.exceptions import AgentBayError
from agentbay.session_params import CreateSessionParams

# This example demonstrates how to create, list, and delete sessions
# using the Wuying AgentBay SDK.


def main():
    # Get API key from environment variable or use a default value for testing
    api_key = os.environ.get("AGENTBAY_API_KEY")
    if not api_key:
        api_key = "akm-xxx"  # Replace with your actual API key for testing
        print(
            "Warning: Using default API key. Set AGENTBAY_API_KEY environment variable for production use."
        )

    session = None
    additional_sessions = []
    session_with_params = None

    try:
        # Initialize the AgentBay client
        agent_bay = AgentBay(api_key=api_key)

        # Create a new session with default parameters
        print("\nCreating a new session...")
        session_result = agent_bay.create()
        print(f"\nSession created with ID: {session_result.session.session_id}")
        print(f"Request ID: {session_result.request_id}")

        session = session_result.session

        # List all sessions
        print("\nListing all sessions...")
        sessions_result = agent_bay.list()

        # Extract session_id list and join as string
        session_ids = [s.session_id for s in sessions_result]
        session_ids_str = ", ".join(session_ids)
        print(f"\nAvailable sessions: {session_ids_str}")

        # Create multiple sessions to demonstrate listing
        print("\nCreating additional sessions...")
        additional_sessions = []
        for i in range(2):
            try:
                additional_result = agent_bay.create()
                additional_session = additional_result.session
                print(
                    f"Additional session created with ID: "
                    f"{additional_session.session_id}"
                )
                print(f"Request ID: {additional_result.request_id}")

                # Store the session for later cleanup
                additional_sessions.append(additional_session)
            except AgentBayError as e:
                print(f"\nError creating additional session: {e}")
                continue

        # List sessions again to show the new sessions
        print("\nListing all sessions after creating additional ones...")
        try:
            updated_sessions_result = agent_bay.list()
            updated_session_ids = [s.session_id for s in updated_sessions_result]
            updated_session_ids_str = ", ".join(updated_session_ids)
            print(f"\nUpdated list of sessions: {updated_session_ids_str}")
        except AgentBayError as e:
            print(f"\nError listing sessions: {e}")

        # Clean up all sessions
        print("\nCleaning up sessions...")
        # First delete the initial session
        try:
            delete_result = agent_bay.delete(session)
            print(f"Session {session.session_id} deleted successfully")
            print(f"Request ID: {delete_result.request_id}")
        except AgentBayError as e:
            print(f"Error deleting session {session.session_id}: {e}")

        # Then delete the additional sessions
        for s in additional_sessions:
            try:
                delete_result = agent_bay.delete(s)
                print(f"Session {s.session_id} deleted successfully")
                print(f"Request ID: {delete_result.request_id}")
            except AgentBayError as e:
                print(f"Error deleting session {s.session_id}: {e}")

        # List sessions one more time to confirm deletion
        print("\nListing sessions after cleanup...")
        try:
            final_sessions_result = agent_bay.list()
            if len(final_sessions_result) == 0:
                print("All sessions have been deleted successfully.")
            else:
                final_session_ids = [s.session_id for s in final_sessions_result]
                final_session_ids_str = ", ".join(final_session_ids)
                print(f"\nRemaining sessions: {final_session_ids_str}")
        except AgentBayError as e:
            print(f"\nError listing sessions: {e}")

        # test get_link with special imageid
        try:
            # Define session creation parameters
            params = CreateSessionParams(
                image_id="code_latest",
            )

            # Create session with parameters
            session_with_params_result = agent_bay.create(params)
            session_with_params = session_with_params_result.session
            print(
                f"\nSession created successfully with ID: "
                f"{session_with_params.session_id}"
            )
            print(f"Request ID: {session_with_params_result.request_id}")
        except AgentBayError as e:
            print(f"Error creating session with parameters: {e}")
            session_with_params = None

        if session_with_params:
            # Test get_link method
            print("\nTesting get_link method...")
            try:
                link_result = session_with_params.get_link()
                print(f"Link retrieved successfully: {link_result.data}")
                print(f"Request ID: {link_result.request_id}")
            except AgentBayError as e:
                print(f"Error retrieving link: {e}")

            # Using new parameter - only specify protocol type
            print("\nTesting get_link method with protocol_type parameter...")
            try:
                link_with_protocol_result = session_with_params.get_link(
                    protocol_type="https"
                )
                print(
                    f"Link with protocol https retrieved successfully: "
                    f"{link_with_protocol_result.data}"
                )
                print(f"Request ID: {link_with_protocol_result.request_id}")
            except AgentBayError as e:
                print(f"Error retrieving link with protocol type: {e}")

            # Using new parameter - only specify port
            print("\nTesting get_link method with port parameter...")
            try:
                link_with_port_result = session_with_params.get_link(port=8080)
                print(
                    f"Link with port 8080 retrieved successfully: "
                    f"{link_with_port_result.data}"
                )
                print(f"Request ID: {link_with_port_result.request_id}")
            except AgentBayError as e:
                print(f"Error retrieving link with port: {e}")

            # Using new parameters - specify both protocol type and port
            print(
                "\nTesting get_link method with both protocol_type and port parameters..."
            )
            try:
                link_with_both_result = session_with_params.get_link(
                    protocol_type="https", port=443
                )
                print(
                    f"Link with protocol https and port 443 retrieved successfully: "
                    f"{link_with_both_result.data}"
                )
                print(f"Request ID: {link_with_both_result.request_id}")
            except AgentBayError as e:
                print(f"Error retrieving link with protocol and port: {e}")

            # Test get_link_async method
            print("\nTesting get_link_async method...")
            try:
                import asyncio

                # Default parameters
                link_async_result = asyncio.run(session_with_params.get_link_async())
                print(f"Link retrieved successfully (async): {link_async_result.data}")
                print(f"Request ID: {link_async_result.request_id}")
            except AgentBayError as e:
                print(f"Error retrieving link asynchronously: {e}")

            # Using new parameters - protocol type and port
            print(
                "\nTesting get_link_async method with both protocol_type and port parameters..."
            )
            try:
                import asyncio

                link_async_with_params_result = asyncio.run(
                    session_with_params.get_link_async(protocol_type="https", port=8080)
                )
                print(
                    f"Link with https and port 8080 retrieved successfully (async): "
                    f"{link_async_with_params_result.data}"
                )
                print(f"Request ID: {link_async_with_params_result.request_id}")
            except AgentBayError as e:
                print(f"Error retrieving link asynchronously with parameters: {e}")

            # delete session
            try:
                delete_result = session_with_params.delete()
                print(f"Session deleted successfully")
                print(f"Request ID: {delete_result.request_id}")
                session_with_params = None
            except AgentBayError as e:
                print(f"Error deleting session: {e}")

    except Exception as e:
        print(f"Error initializing AgentBay client: {e}")


if __name__ == "__main__":
    main()
