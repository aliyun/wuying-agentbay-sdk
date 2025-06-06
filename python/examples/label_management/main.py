#!/usr/bin/env python3
"""
Label Management Example

This example demonstrates how to use the label management features
of the Wuying AgentBay SDK.
"""

import os
import sys
from agentbay import AgentBay
from agentbay.exceptions import AgentBayError
from agentbay.session_params import CreateSessionParams


def main():
    # Get API key from environment variable or use a default value for testing
    api_key = os.getenv("AGENTBAY_API_KEY")
    if not api_key:
        api_key = "akm-xxx"  # Replace with your actual API key for testing
        print("Warning: Using default API key. Set AGENTBAY_API_KEY environment variable for production use.")

    session1 = None
    session2 = None

    try:
        # Initialize the AgentBay client
        agent_bay = AgentBay(api_key=api_key)

        # Create a new session with labels
        print("\nCreating a new session with labels...")
        params = CreateSessionParams()
        params.labels = {
            "purpose": "demo",
            "feature": "label-management",
            "version": "1.0"
        }
        session1 = agent_bay.create(params)
        print(f"Session created with ID: {session1.session_id}")

        # Get labels for the session
        print("\nGetting labels for the session...")
        labels = session1.get_labels()
        print(f"Session labels: {labels}")

        # Create another session with different labels
        print("\nCreating another session with different labels...")
        params = CreateSessionParams()
        params.labels = {
            "purpose": "demo",
            "feature": "other-feature",
            "version": "2.0"
        }
        session2 = agent_bay.create(params)
        print(f"Session created with ID: {session2.session_id}")

        # Update labels for the second session
        print("\nUpdating labels for the second session...")
        session2.set_labels({
            "purpose": "demo",
            "feature": "label-management",
            "version": "2.0",
            "status": "active"
        })

        # Get updated labels for the second session
        print("\nGetting updated labels for the second session...")
        updated_labels = session2.get_labels()
        print(f"Updated session labels: {updated_labels}")

        # List all sessions
        print("\nListing all sessions...")
        all_sessions = agent_bay.list()
        print(f"Found {len(all_sessions)} sessions")
        for i, session in enumerate(all_sessions):
            print(f"Session {i+1} ID: {session.session_id}")

        # List sessions by label
        print("\nListing sessions with purpose=demo and feature=label-management...")
        filtered_sessions = agent_bay.list_by_labels({
            "purpose": "demo",
            "feature": "label-management"
        })
        print(f"Found {len(filtered_sessions)} matching sessions")
        for i, session in enumerate(filtered_sessions):
            print(f"Matching session {i+1} ID: {session.session_id}")
            session_labels = session.get_labels()
            print(f"Labels: {session_labels}")

        # Delete the sessions
        print("\nDeleting the sessions...")
        agent_bay.delete(session1)
        print(f"Session {session1.session_id} deleted successfully")
        session1 = None  # Clear reference to avoid deletion error
        agent_bay.delete(session2)
        print(f"Session {session2.session_id} deleted successfully")
        session2 = None  # Clear reference to avoid deletion error

    except AgentBayError as e:
        print(f"Error: {e}")

        if session1:
            agent_bay.delete(session1)
        if session2:
            agent_bay.delete(session2)
        sys.exit(1)


if __name__ == "__main__":
    main()
