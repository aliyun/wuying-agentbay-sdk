"""
Example: Get ADB Connection URL for Mobile Device

This example demonstrates how to use session.mobile.get_adb_url() to retrieve
an ADB connection URL for connecting to a mobile device. This API is only
available in mobile environments using the mobile_latest image.

The get_adb_url method requires an ADB public key for authentication and
returns the ADB connection URL that can be used with the `adb connect` command.
"""

import os
from agentbay import AgentBay
from agentbay.session_params import CreateSessionParams


def main():
    # Get API key from environment variable
    api_key = os.environ.get("AGENTBAY_API_KEY")
    if not api_key:
        raise ValueError("AGENTBAY_API_KEY environment variable is not set")

    # Initialize AgentBay client
    agent_bay = AgentBay(api_key=api_key)

    # Create a mobile session
    # NOTE: This will only work with mobile_latest image
    print("Creating a mobile session...")
    params = CreateSessionParams(image_id="mobile_latest")
    create_result = agent_bay.create(params=params)

    if not create_result.success:
        print(f"Failed to create session: {create_result.error_message}")
        return

    session = create_result.session
    print(f"✅ Session created: {session.session_id}")
    print(f"   Request ID: {create_result.request_id}")

    try:
        # Example ADB public key
        # In a real scenario, this would come from your ADB setup
        # Replace this with your actual ADB public key
        adbkey_pub = "QAAAAM0muSn7yQCY...your_adb_public_key...EAAQAA="

        # Get ADB URL for the mobile device
        print("\nRetrieving ADB connection URL...")
        adb_result = session.mobile.get_adb_url(adbkey_pub)

        if adb_result.success:
            print(f"✅ ADB URL retrieved successfully")
            print(f"   URL: {adb_result.data}")
            print(f"   Request ID: {adb_result.request_id}")

            # You can now use this URL to connect via ADB
            print(f"\nYou can use this command to connect:")
            print(f"   {adb_result.data}")
        else:
            print(f"❌ Failed to retrieve ADB URL: {adb_result.error_message}")

    finally:
        # Clean up: delete the session
        print("\nCleaning up...")
        delete_result = agent_bay.delete(session)
        if delete_result.success:
            print(f"✅ Session deleted successfully")
            print(f"   Request ID: {delete_result.request_id}")
        else:
            print(f"❌ Failed to delete session: {delete_result.error_message}")


if __name__ == "__main__":
    main()
