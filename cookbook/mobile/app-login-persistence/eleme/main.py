import asyncio
import os
import sys

# Ensure agentbay can be imported
# If running from the repo root, this helps find the local package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../python")))

from agentbay import AsyncAgentBay, CreateSessionParams, ContextSync

# Configuration
# Note: Ensure the image has Ele.me (Taobao Shangou) app installed
IMAGE_NAME = "imgc-0aae4rgl3u35xrhoe"
APP_DATA_PATH = "/data/data/me.ele/"
CONTEXT_NAME = "eleme-login-persistence-ctx"

async def main():
    api_key = os.getenv("AGENTBAY_API_KEY")
    if not api_key:
        print("Error: AGENTBAY_API_KEY environment variable is not set.")
        print("Please set it: export AGENTBAY_API_KEY=your_key")
        return

    agent_bay = AsyncAgentBay(api_key=api_key)
    
    print(f"--- Step 1: Prepare Context '{CONTEXT_NAME}' ---")
    # Get or Create Context
    ctx_result = await agent_bay.context.get(name=CONTEXT_NAME, create=True)
    if not ctx_result.success:
        print(f"Failed to get/create context: {ctx_result.error_message}")
        return
    context = ctx_result.context
    print(f"Context ID: {context.id}")

    # Define how the context syncs with the container
    context_sync = ContextSync.new(
        context_id=context.id,
        path=APP_DATA_PATH
    )
    print(f"Context will sync to: {APP_DATA_PATH}")

    print("\n--- Step 2: Create First Session (Login) ---")
    params = CreateSessionParams(
        image_id=IMAGE_NAME,
        context_syncs=[context_sync]
    )
    
    session1_result = await agent_bay.create(params)
    if not session1_result.success:
        print(f"Failed to create session 1: {session1_result.error_message}")
        return
    session1 = session1_result.session
    
    print(f"Session 1 Created: {session1.session_id}")
    print(f"Resource URL: {session1.resource_url}")
    
    print("\n" + "="*50)
    print("ACTION REQUIRED:")
    print(f"1. Open the Resource URL in your browser: {session1.resource_url}")
    print("2. Login to the 'Ele.me' (Taobao Shangou) app.")
    print("3. Verify you are logged in.")
    print("4. Return here and press Enter.")
    print("="*50 + "\n")
    
    try:
        input("Press Enter to continue after login...")
    except EOFError:
        # Handle non-interactive environments (like CI) gracefully-ish
        print("Non-interactive mode detected. Waiting 30 seconds then proceeding (Login won't happen).")
        await asyncio.sleep(30)

    print("\n--- Step 3: Release First Session ---")
    print("Deleting Session 1. Data should be synced to context on termination.")
    await session1.delete()
    print("Session 1 deleted.")

    print("\nWaiting 5 seconds for data synchronization...")
    await asyncio.sleep(5)

    print("\n--- Step 4: Create Second Session (Verification) ---")
    print("Creating Session 2 with the same context...")
    
    session2_result = await agent_bay.create(params) 
    if not session2_result.success:
        print(f"Failed to create session 2: {session2_result.error_message}")
        return
    session2 = session2_result.session

    print(f"Session 2 Created: {session2.session_id}")
    print(f"Resource URL: {session2.resource_url}")
    
    print("\n" + "="*50)
    print("ACTION REQUIRED:")
    print(f"1. Open the Resource URL in your browser: {session2.resource_url}")
    print("2. Open 'Ele.me' (Taobao Shangou) app.")
    print("3. Check if you are still logged in.")
    print("="*50 + "\n")
    
    try:
        input("Press Enter to finish and cleanup...")
    except EOFError:
        print("Non-interactive mode. Waiting 30 seconds.")
        await asyncio.sleep(30)

    print("\n--- Step 5: Cleanup ---")
    await session2.delete()
    print("Session 2 deleted.")
    
    print("\nExample completed successfully.")

if __name__ == "__main__":
    asyncio.run(main())

