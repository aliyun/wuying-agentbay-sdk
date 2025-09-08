# Complete Automation Guide

This guide integrates all automation features of AgentBay SDK, including command execution, code execution, UI automation, and workflow orchestration.

## 📋 Table of Contents

- [Overview](#overview)
- [Command Execution](#command-execution)
- [Code Execution](#code-execution)
- [File System Operations](#file-system-operations)
- [UI Automation](#ui-automation)
- [Workflow Orchestration](#workflow-orchestration)
- [Error Handling and Retry](#error-handling-and-retry)
- [Best Practices](#best-practices)

<a id="overview"></a>
## 🎯 Overview

AgentBay provides four main automation capabilities:

1. **Command Execution** - Execute Shell commands and system operations in the cloud
2. **Code Execution** - Run code in programming languages like Python, JavaScript
3. **UI Automation** - Interact with graphical interfaces (screenshots, clicks, input, etc.)
4. **File System Operations** - Manage files and directories in the cloud environment

These features can be used individually or combined to build complex automation workflows.

<a id="command-execution"></a>
## 💻 Command Execution

### Basic Command Execution

```python
 # Basic command execution
result = session.command.execute_command("ls -la /tmp")
if result.success:
    print("Output:", result.output)
else:
    print("Command execution failed:", result.error_message)

# Command execution with timeout
result = session.command.execute_command("sleep 3", timeout_ms=5000)
if not result.success:
    print("Command timed out or failed")

# Interactive command
# Note: Interactive commands are not directly supported in the current SDK
# You can achieve similar functionality by writing scripts to a file and executing them
result = session.file_system.write_file("/tmp/script.py", "print('Hello from Python')\nexit()\n")
if result.success:
    print("File written successfully")
    result = session.command.execute_command("python3 /tmp/script.py")
    if result.success:
        print("Output:", result.output)
    else:
        print("Command execution failed:", result.error_message)
agent_bay.delete(session)
```



<a id="code-execution"></a>
## 🐍 Code Execution

**Note:** When executing run_code, you need to specify image_id when creating the session, image_id should be code_latest

### Python Code Execution


```python
session_params = CreateSessionParams(image_id="code_latest")
session = agent_bay.create(session_params).session
# Simple Python code
code = """
import os
import sys
print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")
print("Hello from AgentBay!")
"""

result = session.code.run_code(code, "python")
if result.success:
    print("Output:", result.result)
else:
    print("Command execution failed:", result.error_message)

# Code with dependencies
code = """
import requests
response = requests.get('https://api.github.com/users/octocat')
print(response.json()['name'])
"""

# Install dependencies first
result = session.command.execute_command("pip install requests")
if result.success:
    print("Dependencies installed successfully")
    print("Output:", result.output)

    result = session.code.run_code(code, "python")
    if result.success:
        print("Output:", result.result)
    else:
        print("Command execution failed:", result.error_message)
else:
    print("Command execution failed:", result.error_message)
agent_bay.delete(session)
```

### JavaScript Code Execution

```python
session_params = CreateSessionParams(image_id="code_latest")
session = agent_bay.create(session_params).session
# JavaScript Code Execution
# Node.js code
js_code = """
const fs = require('fs');
const path = require('path');

console.log('Node.js version:', process.version);
console.log('Current directory:', process.cwd());

// Create a simple file
fs.writeFileSync('/tmp/hello.txt', 'Hello from Node.js!');
console.log('File created successfully');
"""

result = session.code.run_code(js_code, "javascript")
if result.success:
    print("Output:", result.result)
else:
    print("Command execution failed:", result.error_message)
agent_bay.delete(session)
```

### Code Execution with File I/O

```python
session = agent_bay.create().session
# Code with File I/O
# Upload code file
session.file_system.write_file("/tmp/script.py", """
import json
import sys

data = {
    'message': 'Hello from uploaded script',
    'args': sys.argv[1:] if len(sys.argv) > 1 else []
}

with open('/tmp/output.json', 'w') as f:
    json.dump(data, f, indent=2)

print(json.dumps(data, indent=2))
""")
# Read output file
output = session.file_system.read_file("/tmp/script.py")
if output.success:
    print("File content:", output.content)
else:
    print("Failed to read file:", output.error_message)

# Execute uploaded script
result = session.command.execute_command("python3 /tmp/script.py")
if result.success:
    print("Script output:", result.output)
else:
    print("Command execution failed:", result.error_message)
agent_bay.delete(session)
```

<a id="file-system-operations"></a>
## 📁 File System Operations

### Basic File Operations

```python
session = agent_bay.create().session
# Create a directory
result = session.file_system.create_directory("/tmp/test_dir")
if result.success:
    print("Directory created successfully")
else:
    print("Failed to create directory:", result.error_message)

# Write to a file
result = session.file_system.write_file("/tmp/test_dir/test.txt", "Hello, AgentBay!")
if result.success:
    print("File written successfully")
else:
    print("Failed to write file:", result.error_message)

# Read a file
result = session.file_system.read_file("/tmp/test_dir/test.txt")
if result.success:
    print("File content:", result.content)
else:
    print("Failed to read file:", result.error_message)

# Get file information
result = session.file_system.get_file_info("/tmp/test_dir/test.txt")
if result.success:
    print("File info:", result.file_info)
else:
    print("Failed to get file info:", result.error_message)

# List directory contents
result = session.file_system.list_directory("/tmp/test_dir/")
if result.success:
    for entry in result.entries:
        print(f"Name: {entry['name']}, Is Directory: {entry['isDirectory']}")
else:
    print("Failed to list directory:", result.error_message)
agent_bay.delete(session)
```

<a id="ui-automation"></a>
## 🖱️ UI Automation

### Screenshot and Visual Operations
**Note:** When executing click、send_key、get_all_ui_elements、get_clickable_ui_elements, you need to specify image_id when creating the session, image_id should be mobile_latest

```python
session_params = CreateSessionParams(image_id="mobile_latest")
session = agent_bay.create(session_params).session
# Take screenshot
screenshot = session.ui.screenshot()
if screenshot.success:
    # Save screenshot locally
    with open("screenshot.png", "wb") as f:
        # Handle different data types
        if isinstance(screenshot.data, str):
            # Try to decode as base64 first (common for image data)
            try:
                import base64
                f.write(base64.b64decode(screenshot.data))
            except:
                # If not base64, encode as UTF-8
                f.write(screenshot.data.encode('utf-8'))
        else:
            # Already bytes
            f.write(screenshot.data)
else:
    print("Failed to take screenshot:", screenshot.error_message)

# Click at coordinates
result = session.ui.click(x=100, y=200,button="left")
if result.success:
    print("Click successful")
else:
    print("Click failed:", result.error_message)

# Note: Double click and right click methods are not available in the current SDK
# You can achieve similar functionality by calling click() multiple times or with different parameters
agent_bay.delete(session)
```

### Keyboard and Text Input

```python
session_params = CreateSessionParams(image_id="mobile_latest")
session = agent_bay.create(session_params).session
# Type text
result = session.ui.input_text("Hello AgentBay!")
if result.success:
    print("Text input successful")
else:
    print("Text input failed:", result.error_message)

# Press keys
# The SDK provides predefined key codes for common keys
from agentbay.ui.ui import KeyCode
result = session.ui.send_key(KeyCode.MENU)
if result.success:
    print("Enter key pressed")
else:
    print("Enter key press failed:", result.error_message)

# Note: The SDK does not support direct string-based key presses or key combinations
# You need to use the predefined key codes or implement custom solutions
agent_bay.delete(session)
```

### Element Detection and Interaction

```python
session_params = CreateSessionParams(image_id="mobile_latest")
session = agent_bay.create(session_params).session
# Get all UI elements
elements = session.ui.get_all_ui_elements()
if elements.success:
    print(f"Found {len(elements.elements)} UI elements")
    for element in elements.elements:
        print(f"Element: {element}")
else:
    print("Failed to get UI elements:", elements.error_message)

# Get clickable UI elements
clickable_elements = session.ui.get_clickable_ui_elements()
if clickable_elements.success:
    print(f"Found {len(clickable_elements.elements)} clickable elements")
else:
    print("Failed to get clickable elements:", clickable_elements.error_message)

# Note: The SDK does not provide image-based element detection or waiting functionality
# UI element interaction is done through the methods available in the SDK
agent_bay.delete(session)
```

<a id="workflow-orchestration"></a>
## 🔄 Workflow Orchestration

### Parallel Workflows

```python
"""
AgentBay SDK - Parallel Workflows Template

This template demonstrates how to use AgentBay SDK to execute multiple tasks in parallel.
Each task runs in its own isolated session, allowing for concurrent execution of different operations.

🔧 CUSTOMIZATION GUIDE:
- Replace the example tasks with your own business logic
- Modify task parameters and execution methods as needed
- Add or remove tasks based on your requirements
- Customize error handling and logging to fit your needs

Usage:
    python parallel_workflows.py

Requirements:
    - AgentBay SDK installed
    - Valid API key (set AGENTBAY_API_KEY environment variable)
"""

import os
import concurrent.futures
import threading
import time
from agentbay import AgentBay
from agentbay.session_params import CreateSessionParams


def initialize_agentbay():
    """
    Initialize AgentBay SDK with proper API key handling.

    Returns:
        AgentBay: Initialized AgentBay instance

    Raises:
        Exception: If API key is not provided and no default is available
    """
    api_key = os.getenv("AGENTBAY_API_KEY")
    if not api_key:
        # TODO: Replace with your actual API key or ensure environment variable is set
        api_key = "your-api-key-here"
        print("⚠️  Warning: Using placeholder API key. Set AGENTBAY_API_KEY environment variable for production use.")

    try:
        agent_bay = AgentBay(api_key=api_key)
        print("✅ AgentBay SDK initialized successfully")
        return agent_bay
    except Exception as e:
        print(f"❌ Failed to initialize AgentBay SDK: {e}")
        raise


class ParallelWorkflowManager:
    """
    Manages parallel execution of multiple tasks using AgentBay sessions.

    🔧 CUSTOMIZATION:
    - Add your own task methods following the same pattern
    - Modify session parameters (image_id, etc.) as needed
    - Customize error handling and logging
    """

    def __init__(self, agent_bay, image_id="code_latest"):
        """
        Initialize the workflow manager.

        Args:
            agent_bay (AgentBay): Initialized AgentBay instance
            image_id (str): Docker image ID to use for sessions
                          TODO: Replace with your preferred image
        """
        self.agent_bay = agent_bay
        self.image_id = image_id
        self.session_count = 0
        self.lock = threading.Lock()

    def create_session(self, task_name=""):
        """
        Create a new AgentBay session with proper error handling.

        Args:
            task_name (str): Optional task name for logging

        Returns:
            Session: Created session object

        Raises:
            Exception: If session creation fails
        """
        with self.lock:
            self.session_count += 1
            session_id = self.session_count

        session_params = CreateSessionParams(image_id=self.image_id)
        result = self.agent_bay.create(session_params)

        if result.success:
            print(f"📦 Session {session_id} created for task: {task_name}")
            return result.session
        else:
            raise Exception(f"Failed to create session for {task_name}: {result.error_message}")

    def cleanup_session(self, session, task_name=""):
        """
        Safely cleanup a session with error handling.

        Args:
            session: Session to cleanup
            task_name (str): Task name for logging
        """
        if session is not None:
            try:
                self.agent_bay.delete(session)
                print(f"🧹 Session cleaned up for task: {task_name}")
            except Exception as e:
                print(f"⚠️  Warning: Failed to cleanup session for {task_name}: {e}")

    def custom_task_1(self):
        """
        🔧 REPLACE THIS: Custom Task 1 Template

        Replace this method with your own business logic.
        This example shows file-based execution pattern.

        Returns:
            dict: Task result with success status and details
        """
        task_name = "Custom Task 1"  # TODO: Replace with your task name
        session = None

        try:
            session = self.create_session(task_name)

            # TODO: Replace this with your actual code
            your_code = """
# 🔧 REPLACE THIS SECTION WITH YOUR CODE
print("Starting your custom task 1...")

# Example: Your business logic here
# - Data processing
# - API calls
# - File operations
# - Database queries
# etc.

print("Your custom task 1 completed!")
"""

            # Write code to file and execute
            write_result = session.file_system.write_file('/workspace/your_script_1.py', your_code)
            if not write_result.success:
                return {
                    "task": task_name,
                    "success": False,
                    "error": f"Failed to write script: {write_result.error_message}"
                }

            # Execute your script
            exec_result = session.command.execute_command("python3 /workspace/your_script_1.py")

            return {
                "task": task_name,
                "success": exec_result.success,
                "execution_time": time.time(),
                "method": "file_execution"
            }

        except Exception as e:
            return {
                "task": task_name,
                "success": False,
                "error": str(e),
                "method": "file_execution"
            }
        finally:
            self.cleanup_session(session, task_name)

    def custom_task_2(self):
        """
        🔧 REPLACE THIS: Custom Task 2 Template

        Replace this method with your own business logic.
        This example shows another file-based execution pattern.

        Returns:
            dict: Task result with success status and details
        """
        task_name = "Custom Task 2"  # TODO: Replace with your task name
        session = None

        try:
            session = self.create_session(task_name)

            # TODO: Replace this with your actual code
            your_code = """
# 🔧 REPLACE THIS SECTION WITH YOUR CODE
print("Starting your custom task 2...")

# Example: Your business logic here
# - Report generation
# - Data analysis
# - Image processing
# - Machine learning inference
# etc.

print("Your custom task 2 completed!")
"""

            # Write and execute your script
            write_result = session.file_system.write_file('/workspace/your_script_2.py', your_code)
            if not write_result.success:
                return {
                    "task": task_name,
                    "success": False,
                    "error": f"Failed to write script: {write_result.error_message}"
                }

            exec_result = session.command.execute_command("python3 /workspace/your_script_2.py")

            return {
                "task": task_name,
                "success": exec_result.success,
                "execution_time": time.time(),
                "method": "file_execution"
            }

        except Exception as e:
            return {
                "task": task_name,
                "success": False,
                "error": str(e),
                "method": "file_execution"
            }
        finally:
            self.cleanup_session(session, task_name)

    def custom_task_3(self):
        """
        🔧 REPLACE THIS: Custom Task 3 Template

        Replace this method with your own business logic.
        This example shows direct code execution pattern.

        Returns:
            dict: Task result with success status and details
        """
        task_name = "Custom Task 3"  # TODO: Replace with your task name
        session = None

        try:
            session = self.create_session(task_name)

            # TODO: Replace this with your actual code
            your_code = """
# 🔧 REPLACE THIS SECTION WITH YOUR CODE
print("Starting your custom task 3...")

# Example: Your business logic here
# - Send notifications
# - Update databases
# - Call external APIs
# - Generate alerts
# etc.

print("Your custom task 3 completed!")
"""

            # Execute code directly (good for shorter scripts)
            exec_result = session.code.run_code(your_code, "python")

            return {
                "task": task_name,
                "success": exec_result.success,
                "execution_time": time.time(),
                "method": "direct_execution"
            }

        except Exception as e:
            return {
                "task": task_name,
                "success": False,
                "error": str(e),
                "method": "direct_execution"
            }
        finally:
            self.cleanup_session(session, task_name)

    # 🔧 ADD MORE TASKS: You can add more custom tasks here following the same pattern
    def your_additional_task(self):
        """
        🔧 TEMPLATE: Add your additional tasks here

        Copy this template and modify it for your needs:
        1. Change the task_name
        2. Replace the code with your logic
        3. Choose execution method (file_execution or direct_execution)
        4. Add the task to run_parallel_workflow method
        """
        task_name = "Your Additional Task"
        session = None

        try:
            session = self.create_session(task_name)

            # Your code here
            your_code = """
print("Your additional task logic here...")
"""

            # Choose your execution method:
            # Option 1: Direct execution
            exec_result = session.code.run_code(your_code, "python")

            # Option 2: File execution (uncomment if needed)
            # write_result = session.file_system.write_file('/workspace/your_additional_script.py', your_code)
            # if write_result.success:
            #     exec_result = session.command.execute_command("python3 /workspace/your_additional_script.py")
            # else:
            #     return {"task": task_name, "success": False, "error": "Failed to write file"}

            return {
                "task": task_name,
                "success": exec_result.success,
                "execution_time": time.time(),
                "method": "direct_execution"  # or "file_execution"
            }

        except Exception as e:
            return {
                "task": task_name,
                "success": False,
                "error": str(e)
            }
        finally:
            self.cleanup_session(session, task_name)

    def run_parallel_workflow(self, max_workers=3):
        """
        Execute all tasks in parallel using ThreadPoolExecutor.

        🔧 CUSTOMIZATION:
        - Add or remove tasks from the tasks list
        - Modify max_workers based on your needs
        - Add custom result processing logic

        Args:
            max_workers (int): Maximum number of concurrent threads

        Returns:
            list: Results from all tasks
        """
        print(f"🚀 Starting parallel workflow with {max_workers} workers...")
        start_time = time.time()

        # 🔧 TODO: Replace these with your actual tasks
        tasks = [
            ("Custom Task 1", self.custom_task_1),
            ("Custom Task 2", self.custom_task_2),
            ("Custom Task 3", self.custom_task_3),
            # 🔧 ADD MORE: Uncomment and add your additional tasks
            # ("Your Additional Task", self.your_additional_task),
        ]

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all tasks
            future_to_task = {
                executor.submit(task_func): task_name
                for task_name, task_func in tasks
            }

            results = []

            # Collect results as they complete
            for future in concurrent.futures.as_completed(future_to_task):
                task_name = future_to_task[future]
                try:
                    result = future.result()
                    results.append(result)

                    status_emoji = "✅" if result.get("success", False) else "❌"
                    print(f"{status_emoji} {task_name} completed")

                except Exception as e:
                    error_result = {
                        "task": task_name,
                        "success": False,
                        "error": f"Task execution failed: {str(e)}"
                    }
                    results.append(error_result)
                    print(f"❌ {task_name} failed: {e}")

        total_time = round(time.time() - start_time, 2)
        print(f"🏁 Parallel workflow completed in {total_time} seconds")

        return results


def main():
    """
    Main function demonstrating the parallel workflow usage.

    🔧 CUSTOMIZATION:
    - Modify workflow parameters
    - Add custom result processing
    - Integrate with your application logic
    """
    print("🎯 AgentBay Parallel Workflows - Custom Implementation")
    print("=" * 60)
    print("🔧 Remember to replace the example tasks with your own logic!")
    print("=" * 60)

    try:
        # Initialize AgentBay SDK
        agent_bay = initialize_agentbay()

        # Create workflow manager
        workflow_manager = ParallelWorkflowManager(agent_bay)

        # 🔧 TODO: Customize workflow parameters as needed
        results = workflow_manager.run_parallel_workflow(max_workers=3)

        # Display final results
        print("\n📊 Final Results Summary:")
        print("=" * 50)

        successful_tasks = 0
        for i, result in enumerate(results, 1):
            status = "✅ SUCCESS" if result.get("success", False) else "❌ FAILED"
            task_name = result.get("task", f"Task {i}")
            method = result.get("method", "unknown")

            print(f"{i}. {task_name}: {status} (Method: {method})")

            if not result.get("success", False) and "error" in result:
                print(f"   Error: {result['error']}")

            if result.get("success", False):
                successful_tasks += 1

        print(f"\n🎯 Overall Success Rate: {successful_tasks}/{len(results)} tasks completed successfully")

        # 🔧 TODO: Add your custom result processing logic here
        # Example: Save results to database, send notifications, etc.

    except Exception as e:
        print(f"❌ Application failed: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
```

<a id="error-handling-and-retry"></a>
## 🚨 Error Handling and Retry

### Retry Mechanisms

```python
import time
import random

def execute_with_retry(session, command, max_retries=3, delay=1):
    """Execute command with exponential backoff retry"""
    for attempt in range(max_retries):
        try:
            result = session.command.execute_command(command)
            if result.success:
                return result

            print(f"Attempt {attempt + 1} failed: {result.error_message}")

        except Exception as e:
            print(f"Attempt {attempt + 1} exception: {e}")

        if attempt < max_retries - 1:
            wait_time = delay * (2 ** attempt) + random.uniform(0, 1)
            print(f"Waiting {wait_time:.2f} seconds before retry...")
            time.sleep(wait_time)

    raise Exception(f"Command '{command}' failed after {max_retries} attempts")

# Usage
try:
    result = execute_with_retry(session, "unstable-command")
    if result.success:
        print("Command succeeded:", result.output)
        agent_bay.delete(session)
except Exception as e:
    print("Command ultimately failed:", e)
```

<a id="best-practices"></a>
## 💡 Best Practices

### 1. Resource Management

```python
# Use context managers for session management
from contextlib import contextmanager

@contextmanager
def managed_session(agent_bay):
    result = agent_bay.create()
    if result.success:
        session = result.session
        try:
            yield session
        finally:
            # Cleanup session
            agent_bay.delete(session)
    else:
        raise Exception(f"Failed to create session: {result.error_message}")

# Usage
try:
    agent_bay = self.common_code()
    with managed_session(agent_bay) as session:
        result = session.command.execute_command("echo 'Hello'")
        if result.success:
            print("Command output:", result.output)
            agent_bay.delete(session)
except Exception as e:
    print("Error:", e)
```

### 2. Logging and Monitoring

```python
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def execute_with_logging(session, command):
    logger.info(f"Executing command: {command}")
    start_time = time.time()

    try:
        result = session.command.execute_command(command)
        duration = time.time() - start_time

        if not result.success:
            logger.error(f"Command failed in {duration:.2f}s: {result.error_message}")
        else:
            logger.info(f"Command succeeded in {duration:.2f}s")

        return result
    except Exception as e:
        duration = time.time() - start_time
        logger.exception(f"Command exception in {duration:.2f}s: {e}")
        raise
execute_with_logging(session, "echo 'Hello'")
agent_bay.delete(session)
```


This comprehensive guide covers all aspects of automation with AgentBay SDK. Use these patterns and best practices to build robust, scalable automation solutions!
