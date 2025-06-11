import os
from agentbay import AgentBay
from agentbay.mobile import KeyCode
from agentbay.session import Session
from agentbay.exceptions import AgentBayError
from typing import List, Dict, Any
def main():
    # Get API key from environment variable or use a default value for testing
    api_key = os.getenv("AGENTBAY_API_KEY")
    if not api_key:
        api_key = "akm-xxx"  # Replace with your actual API key

    try:
        agent_bay = AgentBay(api_key=api_key)

        # Create a new session with default parameters
        print("\nCreating a new session...")
        session = agent_bay.create()

        # Get installed applications
        print("\nGetting installed applications...")
        installed_apps = session.mobile.get_installed_apps(
            start_menu=True,
            desktop=False,
            ignore_system_apps=True
        )

        print(f"\nInstalled Applications: {installed_apps}")
        print(f"\nGetting installed appplications successfully")

        # Start the application
        print(f"\nStarting the application...")
        start_result = session.mobile.start_app("monkey -p com.autonavi.minimap -c android.intent.category.LAUNCHER 1")
        print(f"\nStarted Application successfully: {start_result}")


        # Stop the application
        print("\nStopping the application...")
        stop_result = session.mobile.stop_app_by_cmd("am force-stop com.sankuai.meituan")
        print(f"Application stopped: {stop_result}")

        # Get clickable ui elements
        print("\nGetting clickable UI elements...")
        clickable_elements = session.mobile.get_clickable_ui_elements()
        print(f"Clickable UI Elements: {clickable_elements}")

        # Get all ui elements
        print("\nGetting all UI elements...")
        def print_ui_element(element: Dict[str, Any], indent: int = 1):
            prefix = "  " * indent
            print(f"{prefix}- {element['className']} (text: '{element['text']}', resourceId: '{element['resourceId']}')")

            children = element.get("children", [])
            for child in children:
                print_ui_element(child, indent + 1)

        def print_all_ui_elements(elements: List[Dict[str, Any]]):
            print("\nUI Element Tree:")
            for element in elements:
                print_ui_element(element)
        all_elements = session.mobile.get_all_ui_elements()
        print_all_ui_elements(all_elements)


        # Send key event
        print("\nSending key event...")
        session.mobile.send_key(KeyCode.HOME)
        print(f"Key event sent successfully")

        # Input text
        print("\nInput text...")
        session.mobile.input_text("Hello, AgentBay!")
        print("\nText input successfully")

        # Swipe screen
        print("\nSwiping screen...")
        session.mobile.swipe(
            start_x=100,      # Starting X coordinate
            start_y=800,      # Starting Y coordinate
            end_x=900,        # Ending X coordinate
            end_y=200,        # Ending Y coordinate
            duration_ms=500   # Swipe duration in milliseconds
        )
        print("\nScreen swiped successfully")

        # Click event
        print("\nClicking screen...")
        session.mobile.click(
            x=500,         # X coordinate for click
            y=800,         # Y coordinate for click
            button="left"  # Mouse button type, default is "left"
        )
        print("\nScreen clicked successfully")


    except AgentBayError as e:
        print(f"Failed to test mobile api: {e}")

if __name__ == "__main__":
    main()