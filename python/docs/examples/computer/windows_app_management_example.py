"""
Complete Windows Application Management Example

This example demonstrates the full workflow for managing desktop applications
on Windows using AgentBay SDK:

1. Find installed applications
2. Launch a target application (Notepad)
3. Monitor running applications
4. Stop the application

Based on: docs/guides/computer-use/computer-application-management.md
"""

import os
import time
from agentbay import AgentBay
from agentbay.session_params import CreateSessionParams


def main():
    """Main function demonstrating Windows application management workflow."""

    # Get API key from environment
    api_key = os.getenv("AGENTBAY_API_KEY")
    if not api_key:
        raise ValueError("AGENTBAY_API_KEY environment variable is required")

    print("=" * 80)
    print("Windows Application Management Example")
    print("=" * 80)

    # Initialize AgentBay client
    print("\nInitializing AgentBay client...")
    agent_bay = AgentBay(api_key=api_key)
    print("✅ Client initialized")

    # Create a Windows session with retry logic
    print("\nCreating Windows session...")
    params = CreateSessionParams(image_id="windows_latest")

    max_retries = 3
    retry_delay = 100  # seconds

    for attempt in range(max_retries):
        print(f"  Attempt {attempt + 1}/{max_retries}...")
        result = agent_bay.create(params)

        if result.success:
            break

        # Check if we need to retry
        if "please try again" in result.error_message.lower() and attempt < max_retries - 1:
            print(f"  ⚠️  Resource creation in progress, waiting {retry_delay} seconds...")
            time.sleep(retry_delay)
        else:
            print(f"  ❌ Failed to create session: {result.error_message}")
            return

    if not result.success:
        print(f"❌ Failed to create session after {max_retries} attempts")
        return

    session = result.session
    print(f"✅ Session created: {session.session_id}")

    try:
        # Step 1: Finding installed applications
        print("\n" + "=" * 80)
        print("Step 1: Finding installed applications...")
        print("=" * 80)

        apps_result = session.computer.get_installed_apps(
            start_menu=True,
            desktop=False,
            ignore_system_apps=True
        )

        if not apps_result.success:
            print(f"❌ Failed to get apps: {apps_result.error_message}")
            agent_bay.delete(session)
            return

        print(f"✅ Found {len(apps_result.data)} installed applications")

        # Display first 5 applications
        print("\nFirst 5 applications:")
        for i, app in enumerate(apps_result.data[:5], 1):
            print(f"\n{i}. {app.name}")
            print(f"   Start Command: {app.start_cmd}")
            if app.stop_cmd:
                print(f"   Stop Command: {app.stop_cmd}")
            if app.work_directory:
                print(f"   Work Directory: {app.work_directory}")

        # Step 2: Find Notepad application
        print("\n" + "=" * 80)
        print("Step 2: Finding Notepad application...")
        print("=" * 80)

        target_app = None
        for app in apps_result.data:
            if "notepad" in app.name.lower():
                target_app = app
                break

        # Fallback to common Notepad path if not found in installed apps
        if not target_app:
            print("⚠️  Notepad not found in installed apps, using default path")
            notepad_cmd = "C:\\Windows\\System32\\notepad.exe"
        else:
            print(f"✅ Found application: {target_app.name}")
            notepad_cmd = target_app.start_cmd

        print(f"Start Command: {notepad_cmd}")

        # Step 3: Launching application
        print("\n" + "=" * 80)
        print("Step 3: Launching application...")
        print("=" * 80)

        start_result = session.computer.start_app(notepad_cmd)

        if not start_result.success:
            print(f"❌ Failed to start app: {start_result.error_message}")
            agent_bay.delete(session)
            return

        print(f"✅ Application started with {len(start_result.data)} process(es)")

        for process in start_result.data:
            print(f"  - {process.pname} (PID: {process.pid})")
            if process.cmdline:
                print(f"    Command: {process.cmdline}")

        # Save the main process for later stopping
        main_process = start_result.data[0] if start_result.data else None

        # Step 4: Waiting for application to load
        print("\n" + "=" * 80)
        print("Step 4: Waiting for application to load...")
        print("=" * 80)
        print("Waiting 5 seconds...")
        time.sleep(5)
        print("✅ Wait complete")

        # Step 5: Checking running applications
        print("\n" + "=" * 80)
        print("Step 5: Checking running applications...")
        print("=" * 80)

        visible_result = session.computer.list_visible_apps()

        if visible_result.success:
            print(f"✅ Found {len(visible_result.data)} visible application(s)")
            for app in visible_result.data:
                print(f"  - {app.pname} (PID: {app.pid})")
                if app.cmdline:
                    print(f"    Command: {app.cmdline}")
        else:
            print(f"⚠️  Could not list visible apps: {visible_result.error_message}")

        # Step 6: Stopping application
        print("\n" + "=" * 80)
        print("Step 6: Stopping application...")
        print("=" * 80)

        if main_process:
            # Method 1: Stop by PID
            print(f"Attempting to stop process by PID: {main_process.pid}")
            stop_result = session.computer.stop_app_by_pid(main_process.pid)

            if stop_result.success:
                print("✅ Application stopped successfully (by PID)")
            else:
                print(f"⚠️  Failed to stop by PID: {stop_result.error_message}")

                # Method 2: Try stop by process name as fallback
                print(f"\nTrying to stop by process name: {main_process.pname}")
                stop_result = session.computer.stop_app_by_pname(main_process.pname)

                if stop_result.success:
                    print("✅ Application stopped successfully (by name)")
                else:
                    print(f"❌ Failed to stop by name: {stop_result.error_message}")
        else:
            print("⚠️  No process to stop")

        # Summary
        print("\n" + "=" * 80)
        print("Workflow Summary")
        print("=" * 80)
        print("✅ Session creation: Success")
        print(f"✅ Get installed apps: {len(apps_result.data)} applications found")
        print(f"✅ Find target app: {'Found' if target_app else 'Used default path'}")
        print(f"✅ Start application: {len(start_result.data)} processes started")
        print(f"✅ List visible apps: {len(visible_result.data) if visible_result.success else 'N/A'} visible applications")
        print(f"✅ Stop application: {'Success' if stop_result.success else 'Partial'}")
        print("=" * 80)
        print("\n🎉 Workflow completed successfully!")

    except Exception as e:
        print(f"\n❌ Error occurred: {e}")
        import traceback
        traceback.print_exc()

    finally:
        # Cleanup
        print("\n" + "=" * 80)
        print("Cleaning up session...")
        print("=" * 80)
        agent_bay.delete(session)
        print("✅ Session deleted")


if __name__ == "__main__":
    main()
