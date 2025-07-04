#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Example demonstrating session pagination with AgentBay SDK.
This example shows how to list sessions with pagination using labels.
"""

from agentbay.session_params import CreateSessionParams, ListSessionParams
from agentbay import AgentBay
import os
import sys
import time

# Add the parent directory to the path so we can import the agentbay package
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)


def main():
    # Get API key from environment variable
    api_key = os.getenv("AGENTBAY_API_KEY")
    if not api_key:
        print("Error: AGENTBAY_API_KEY environment variable not set")
        return

    # Initialize AgentBay client
    print("Initializing AgentBay client...")
    agent_bay = AgentBay(api_key=api_key)

    # Create test sessions with labels for pagination example
    created_sessions = []
    try:
        # Create a few sessions with labels to test pagination
        print("\nCreating test sessions with labels...")
        for i in range(1, 2):  # Create 1 sessions
            params = CreateSessionParams(
                image_id="linux_latest",
                labels={
                    "environment": "production",
                    "project": "demo",
                    "test_index": str(i),
                },
            )
            result = agent_bay.create(params)
            if result.success:
                print(f"Created session {i} with ID: {result.session.session_id}")
                created_sessions.append(result.session)
            else:
                print(f"Failed to create session {i}: {result.error_message}")

        # Wait briefly to ensure sessions are available for listing
        print("\nWaiting for sessions to be ready...")
        time.sleep(3)

        # Define labels to filter sessions by
        labels = {"environment": "production", "project": "demo"}

        # Create pagination parameters
        page_size = 3  # Smaller page size to demonstrate pagination
        params = ListSessionParams(max_results=page_size, labels=labels)

        # Get the first page of results
        print(f"\nFetching first page of sessions with labels: {labels}")
        result = agent_bay.list_by_labels(params)

        # Process pagination
        page_num = 1
        all_sessions = []

        while True:
            if result.success:
                sessions = result.sessions
                all_sessions.extend(sessions)

                print(f"\nPage {page_num} - Found {len(sessions)} sessions")
                print(f"Request ID: {result.request_id}")

                # Display session information
                for i, session in enumerate(sessions):
                    print(f"  {i + 1}. Session ID: {session.session_id}")

                # Display pagination information
                print(f"\nPagination information:")
                print(f"  Total sessions: {result.total_count}")
                print(f"  Max results per page: {result.max_results}")
                print(f"  Next token: {result.next_token or 'None (last page)'}")

                # Check if there are more pages
                if not result.next_token:
                    print("\nNo more pages to fetch")
                    break

                # Get next page using the next_token
                print(f"\nFetching next page (page {page_num + 1})...")
                params.next_token = result.next_token
                result = agent_bay.list_by_labels(params)
                page_num += 1
            else:
                print(f"\nError fetching sessions: {result.error_message}")
                break

        # Summary
        print(
            f"\nSummary: Retrieved {len(all_sessions)} sessions in {page_num} page(s)"
        )

    finally:
        # Clean up: delete all created sessions
        print("\nCleaning up test sessions...")
        for i, session in enumerate(created_sessions):
            try:
                delete_result = agent_bay.delete(session)
                if delete_result.success:
                    print(
                        f"Deleted session {i + 1}/{len(created_sessions)}: "
                        f"{session.session_id}"
                    )
                else:
                    print(
                        f"Failed to delete session "
                        f"{session.session_id}: "
                        f"{delete_result.error_message}"
                    )
            except Exception as e:
                print(f"Error while deleting session {session.session_id}: {e}")

        print("\nTest completed.")


if __name__ == "__main__":
    main()
