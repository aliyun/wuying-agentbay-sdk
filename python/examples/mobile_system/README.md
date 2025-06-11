# Mobile System Example

This example demonstrates how to use the Wuying AgentBay SDK's `MobileSystem` module to perform various mobile device operations. It covers:

- Initializing the AgentBay client
- Retrieving installed applications
- Starting and stopping applications
- Fetching clickable and all UI elements
- Sending key events
- Inputting text
- Performing swipe gestures
- Clicking on the screen

This example is useful for understanding how to interact with mobile devices in the Wuying AgentBay cloud environment.

## Running the Example

```bash
cd mobile_system
python main.py
```

Make sure you have set the `AGENTBAY_API_KEY` environment variable or replace the placeholder in the code with your actual API key.

## Features Demonstrated

1. **Create a Session**:
   - Use `AgentBay` to create a new session.

2. **Retrieve Installed Applications**:
   - Call the `get_installed_apps` method to fetch a list of installed applications on the device.

3. **Start and Stop Applications**:
   - Use the `start_app` method to launch a specified application.
   - Use the `stop_app_by_cmd` method to stop a specified application.

4. **Fetch UI Elements**:
   - Call the `get_clickable_ui_elements` method to retrieve all clickable UI elements on the screen.
   - Call the `get_all_ui_elements` method to retrieve all UI elements on the screen and print them in a tree structure.

5. **Send Key Events**:
   - Use the `send_key` method to send key events, such as returning to the home screen.

6. **Input Text**:
   - Call the `input_text` method to input text into the currently active field.

7. **Perform Gestures**:
   - Use the `swipe` method to perform a swipe gesture on the screen.
   - Call the `click` method to perform a click action at specified coordinates.
