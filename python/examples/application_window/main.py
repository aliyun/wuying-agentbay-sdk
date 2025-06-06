#!/usr/bin/env python3
"""
Application and Window Management Example

This example demonstrates how to use the application and window management features
of the Wuying AgentBay SDK.
"""

import os
import sys
from agentbay import AgentBay
from agentbay.exceptions import AgentBayError


def main():
    # Get API key from environment variable or use a default value for testing
    api_key = os.getenv("AGENTBAY_API_KEY")
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

        # Application Management Examples
        print("\n=== Application Management Examples ===")

        # Get installed applications
        print("\nGetting installed applications...")
        try:
            apps = session.application.get_installed_apps(
                start_menu=True,
                desktop=False,
                ignore_system_apps=True
            )
            print(f"Found {len(apps)} installed applications")
            # Print the first 3 apps or fewer if less than 3 are available
            count = min(len(apps), 3)
            for i in range(count):
                print(f"App {i+1}: {apps[i].name}")
        except AgentBayError as e:
            print(f"Error getting installed apps: {e}")

        # List visible applications
        print("\nListing visible applications...")
        try:
            visible_apps = session.application.list_visible_apps()
            print(f"Found {len(visible_apps)} visible applications")
            # Print the first 3 apps or fewer if less than 3 are available
            count = min(len(visible_apps), 3)
            for i in range(count):
                print(f"Process {i+1}: {visible_apps[i].pname} (PID: {visible_apps[i].pid})")
        except AgentBayError as e:
            print(f"Error listing visible apps: {e}")

        # Window Management Examples
        print("\n=== Window Management Examples ===")

        # List root windows
        print("\nListing root windows...")
        root_windows = []
        try:
            root_windows = session.window.list_root_windows()
            print(f"Found {len(root_windows)} root windows")
            # Print the first 3 windows or fewer if less than 3 are available
            count = min(len(root_windows), 3)
            for i in range(count):
                print(f"Window {i+1}: {root_windows[i].title} (ID: {root_windows[i].window_id})")
        except AgentBayError as e:
            print(f"Error listing root windows: {e}")

        # Get active window
        print("\nGetting active window...")
        try:
            active_window = session.window.get_active_window()
            print(f"Active window: {active_window.title} (ID: {active_window.window_id}, "
                  f"Process: {active_window.pname}, PID: {active_window.pid})")
        except AgentBayError as e:
            print(f"Error getting active window: {e}")

        # Window operations
        if root_windows:
            window_id = root_windows[0].window_id

            # Activate window
            print(f"\nActivating window with ID {window_id}...")
            try:
                session.window.activate_window(window_id)
                print("Window activated successfully")
            except AgentBayError as e:
                print(f"Error activating window: {e}")

            # Maximize window
            print(f"\nMaximizing window with ID {window_id}...")
            try:
                session.window.maximize_window(window_id)
                print("Window maximized successfully")
            except AgentBayError as e:
                print(f"Error maximizing window: {e}")

            # Minimize window
            print(f"\nMinimizing window with ID {window_id}...")
            try:
                session.window.minimize_window(window_id)
                print("Window minimized successfully")
            except AgentBayError as e:
                print(f"Error minimizing window: {e}")

            # Restore window
            print(f"\nRestoring window with ID {window_id}...")
            try:
                session.window.restore_window(window_id)
                print("Window restored successfully")
            except AgentBayError as e:
                print(f"Error restoring window: {e}")

            # Resize window
            print(f"\nResizing window with ID {window_id} to 800x600...")
            try:
                session.window.resize_window(window_id, 800, 600)
                print("Window resized successfully")
            except AgentBayError as e:
                print(f"Error resizing window: {e}")

        # Focus mode
        # Enable focus mode
        print("\nEnabling focus mode...")
        try:
            session.window.focus_mode(True)
            print("Focus mode enabled successfully")
        except AgentBayError as e:
            print(f"Error enabling focus mode: {e}")

        # Disable focus mode
        print("\nDisabling focus mode...")
        try:
            session.window.focus_mode(False)
            print("Focus mode disabled successfully")
        except AgentBayError as e:
            print(f"Error disabling focus mode: {e}")

        # Delete the session
        print("\nDeleting the session...")
        agent_bay.delete(session)
        print("Session deleted successfully")

    except AgentBayError as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
