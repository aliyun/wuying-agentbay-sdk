import os
import sys
import json

# Add the parent directory to the path so we can import the agentbay package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agentbay.agentbay import AgentBay
from agentbay.session_params import CreateSessionParams
from agentbay.exceptions import AgentBayError


def main():
    # Initialize the AgentBay client
    # You can provide the API key as a parameter or set the AGENTBAY_API_KEY environment variable
    api_key = os.environ.get("AGENTBAY_API_KEY") or "your_api_key_here"
    try:
        agent_bay = AgentBay(api_key=api_key)

        # Example 1: Create a session with default parameters
        print("\nExample 1: Creating a session with default parameters...")
        session1 = agent_bay.create()
        print(f"Session created with ID: {session1.session_id}")

        # Example 2: Create a session with custom labels
        print("\nExample 2: Creating a session with custom labels...")
        
        # Create parameters with labels
        params2 = CreateSessionParams(
            labels={"username": "alice", "project": "my-project"}
        )
        
        session2 = agent_bay.create(params2)
        print(f"Session created with ID: {session2.session_id} and labels: {json.dumps(params2.labels)}")

        # Example 3: Create a session with a context
        print("\nExample 3: Creating a session with a context...")
        
        # First, get or create a context
        # Note: In a real application, you would use the Context API to get or create a context
        # For this example, we'll create a new context
        context = agent_bay.context.create("my-context")
        print(f"Context created with ID: {context.id}")
        
        # Create parameters with context ID
        params3 = CreateSessionParams(context_id=context.id)
        
        session3 = agent_bay.create(params3)
        print(f"Session created with ID: {session3.session_id} and context ID: {params3.context_id}")

        # Example 4: Create a session with both labels and context
        print("\nExample 4: Creating a session with both labels and context...")
        
        params4 = CreateSessionParams(
            labels={"username": "bob", "project": "another-project"},
            context_id=context.id
        )
        
        session4 = agent_bay.create(params4)
        print(f"Session created with ID: {session4.session_id}, labels: {json.dumps(params4.labels)}, and context ID: {params4.context_id}")

        # Clean up
        print("\nCleaning up sessions...")
        
        agent_bay.delete(session1)
        print("Session 1 deleted successfully")
        
        agent_bay.delete(session2)
        print("Session 2 deleted successfully")
        
        agent_bay.delete(session3)
        print("Session 3 deleted successfully")
        
        agent_bay.delete(session4)
        print("Session 4 deleted successfully")

    except AgentBayError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
