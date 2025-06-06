#!/usr/bin/env python3

import os
from agentbay import AgentBay
from agentbay.exceptions import AgentBayError
from agentbay.session_params import CreateSessionParams


def main():
    # Initialize the AgentBay client
    # You can provide the API key as a parameter or set the AGENTBAY_API_KEY environment variable
    api_key = os.environ.get("AGENTBAY_API_KEY")
    if not api_key:
        api_key = "akm-xxx"  # Replace with your actual API key

    try:
        agent_bay = AgentBay(api_key=api_key)

        # Example 1: List all contexts
        print("\nExample 1: Listing all contexts...")
        try:
            contexts = agent_bay.context.list()
            print(f"Found {len(contexts)} contexts:")
            for context in contexts:
                print(f"- {context.name} ({context.id}): state={context.state}, os={context.os_type}")
        except AgentBayError as e:
            print(f"Error listing contexts: {e}")

        # Example 2: Get a context (create if it doesn't exist)
        print("\nExample 2: Getting a context (creating if it doesn't exist)...")
        context_name = "my-test-context"
        try:
            context = agent_bay.context.get(context_name, create=True)
            if context:
                print(f"Got context: {context.name} ({context.id})")
            else:
                print("Context not found and could not be created")
                return
        except AgentBayError as e:
            print(f"Error getting context: {e}")
            return

        # Example 3: Create a session with the context
        session = None
        print("\nExample 3: Creating a session with the context...")
        try:
            params = CreateSessionParams(
                context_id=context.id,
                labels={
                    "username": "alice",
                    "project": "my-project"
                }
            )
            session = agent_bay.create(params)
            print(f"Session created with ID: {session.session_id}")
        except AgentBayError as e:
            print(f"Error creating session: {e}")
            return

        # Example 4: Update the context
        print("\nExample 4: Updating the context...")
        try:
            context.name = "renamed-test-context"
            success = agent_bay.context.update(context)
            if not success:
                print("Context update was not successful")
            else:
                print(f"Context updated successfully to: {context.name}")
        except AgentBayError as e:
            print(f"Error updating context: {e}")

        # Clean up
        print("\nCleaning up...")

        # Delete the session
        try:
            if session:
                agent_bay.delete(session)
            print("Session deleted successfully")
        except AgentBayError as e:
            print(f"Error deleting session: {e}")

        # Delete the context
        print("Deleting the context...")
        try:
            agent_bay.context.delete(context)
            print("Context deleted successfully")
        except AgentBayError as e:
            print(f"Error deleting context: {e}")

    except Exception as e:
        print(f"Error initializing AgentBay: {e}")

if __name__ == "__main__":
    main()
