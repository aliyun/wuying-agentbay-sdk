#!/usr/bin/env python3

import os
from agentbay import AgentBay
from agentbay.exceptions import AgentBayError

# This example demonstrates how to create, list, and delete sessions
# using the Wuying AgentBay SDK.

def main():
    # Get API key from environment variable or use a default value for testing
    api_key = os.environ.get("AGENTBAY_API_KEY")
    if not api_key:
        api_key = "akm-xxx"  # Replace with your actual API key for testing
        print("Warning: Using default API key. Set AGENTBAY_API_KEY environment variable for production use.")

    try:
        # Initialize the AgentBay client
        agent_bay = AgentBay(api_key=api_key)

        # Create a new session with default parameters
        print("\nCreating a new session...")
        session = agent_bay.create()
        print(f"\nSession created with ID: {session.session_id}")

        # List all sessions
        print("\nListing all sessions...")
        sessions = agent_bay.list()

        # Extract session_id list and join as string
        session_ids = [s.session_id for s in sessions]
        session_ids_str = ", ".join(session_ids)
        print(f"\nAvailable sessions: {session_ids_str}")

        # Create multiple sessions to demonstrate listing
        print("\nCreating additional sessions...")
        additional_sessions = []
        for i in range(2):
            try:
                additional_session = agent_bay.create()
                print(f"Additional session created with ID: {additional_session.session_id}")

                # Store the session for later cleanup
                additional_sessions.append(additional_session)
            except AgentBayError as e:
                print(f"\nError creating additional session: {e}")
                continue

        # List sessions again to show the new sessions
        print("\nListing all sessions after creating additional ones...")
        try:
            updated_sessions = agent_bay.list()
            updated_session_ids = [s.session_id for s in updated_sessions]
            updated_session_ids_str = ", ".join(updated_session_ids)
            print(f"\nUpdated list of sessions: {updated_session_ids_str}")
        except AgentBayError as e:
            print(f"\nError listing sessions: {e}")

        # Clean up all sessions
        print("\nCleaning up sessions...")
        # First delete the initial session
        try:
            agent_bay.delete(session)
            print(f"Session {session.session_id} deleted successfully")
        except AgentBayError as e:
            print(f"Error deleting session {session.session_id}: {e}")

        # Then delete the additional sessions
        for s in additional_sessions:
            try:
                agent_bay.delete(s)
                print(f"Session {s.session_id} deleted successfully")
            except AgentBayError as e:
                print(f"Error deleting session {s.session_id}: {e}")

        # List sessions one more time to confirm deletion
        print("\nListing sessions after cleanup...")
        try:
            final_sessions = agent_bay.list()
            if len(final_sessions) == 0:
                print("All sessions have been deleted successfully.")
            else:
                final_session_ids = [s.session_id for s in final_sessions]
                final_session_ids_str = ", ".join(final_session_ids)
                print(f"\nRemaining sessions: {final_session_ids_str}")
        except AgentBayError as e:
            print(f"\nError listing sessions: {e}")

        # test get_link with special imageid
        try:
            from agentbay.session_params import CreateSessionParams

            # Define session creation parameters
            params = CreateSessionParams(
                image_id="imgc-07if81c4ktj9shiru",
            )

            # Create session with parameters
            session_with_params = agent_bay.create(params)
            print(f"\nSession created successfully with ID: {session_with_params.session_id}")
        except AgentBayError as e:
            print(f"Error creating session with parameters: {e}")

        # Test get_link method
        print("\nTesting get_link method...")
        try:
            link = session_with_params.get_link()
            print(f"Link retrieved successfully: {link}")
        except AgentBayError as e:
            print(f"Error retrieving link: {e}")

        # Test get_link_async method
        print("\nTesting get_link_async method...")
        try:
            import asyncio
            link_async = asyncio.run(session_with_params.get_link_async())
            print(f"Link retrieved successfully (async): {link_async}")
        except AgentBayError as e:
            print(f"Error retrieving link asynchronously: {e}")

        # Test creating a session with specific parameters
        print("\nTesting session creation with parameters...")

        # delete session
        try:
            session_with_params.delete()
            print(f"Session(session_with_params) deleted successfully")
            ssession_with_params = None
        except AgentBayError as e:
            print(f"Error deleting session session_with_params: {e}")


    except Exception as e:
        print(f"Error initializing AgentBay client: {e}")
        if session:
            try:
                session.delete()
                print("Session deleted successfully after error")
            except AgentBayError as delete_error:
                print(f"Error deleting session after error: {delete_error}")
        for s in additional_sessions:
            try:
                agent_bay.delete(s)
                print(f"Session {s.session_id} deleted successfully")
            except AgentBayError as e:
                print(f"Error deleting session {s.session_id}: {e}")

if __name__ == "__main__":
    main()
