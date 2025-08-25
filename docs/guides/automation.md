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
result = session.command.execute_command("sleep 10", timeout_ms=5000)
if not result.success:
    print("Command timed out or failed")

# Interactive command
# Note: Interactive commands are not directly supported in the current SDK
# You can achieve similar functionality by writing scripts to a file and executing them
session.file_system.write_file("/tmp/script.py", "print('Hello from Python')\nexit()\n")
result = session.command.execute_command("python3 /tmp/script.py")
```



<a id="code-execution"></a>
## 🐍 Code Execution

### Python Code Execution

```python
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

# Code with dependencies
code = """
import requests
response = requests.get('https://api.github.com/users/octocat')
print(response.json()['name'])
"""

# Install dependencies first
session.command.execute_command("pip install requests")
result = session.code.run_code(code, "python")
```

### JavaScript Code Execution

```python
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
```

### Code Execution with File I/O

```python
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

# Execute uploaded script
result = session.command.execute_command("python /tmp/script.py arg1 arg2")
if result.success:
    print("Script output:", result.output)

# Read output file
output = session.file_system.read_file("/tmp/output.json")
if output.success:
    print("File content:", output.content)
```

<a id="file-system-operations"></a>
## 📁 File System Operations

### Basic File Operations

```python
# Create a directory
result = session.file_system.create_directory("/tmp/test_dir")
if result.success:
    print("Directory created successfully")
else:
    print("Failed to create directory:", result.error_message)

# Write to a file
result = session.file_system.write_file("/tmp/test.txt", "Hello, AgentBay!")
if result.success:
    print("File written successfully")
else:
    print("Failed to write file:", result.error_message)

# Read a file
result = session.file_system.read_file("/tmp/test.txt")
if result.success:
    print("File content:", result.content)
else:
    print("Failed to read file:", result.error_message)

# Get file information
result = session.file_system.get_file_info("/tmp/test.txt")
if result.success:
    print("File info:", result.file_info)
else:
    print("Failed to get file info:", result.error_message)

# List directory contents
result = session.file_system.list_directory("/tmp")
if result.success:
    for entry in result.entries:
        print(f"Name: {entry['name']}, Is Directory: {entry['isDirectory']}")
else:
    print("Failed to list directory:", result.error_message)
```

<a id="ui-automation"></a>
## 🖱️ UI Automation

### Screenshot and Visual Operations
```python
# Take screenshot
screenshot = session.ui.screenshot()
if screenshot.success:
    # Save screenshot locally
    with open("screenshot.png", "wb") as f:
        f.write(screenshot.data)

# Click at coordinates
result = session.ui.click(x=100, y=200)
if result.success:
    print("Click successful")

# Note: Double click and right click methods are not available in the current SDK
# You can achieve similar functionality by calling click() multiple times or with different parameters
```

### Keyboard and Text Input

```python
# Type text
result = session.ui.input_text("Hello AgentBay!")
if result.success:
    print("Text input successful")

# Press keys
# The SDK provides predefined key codes for common keys
from agentbay.ui.ui import KeyCode
result = session.ui.send_key(KeyCode.ENTER)
if result.success:
    print("Enter key pressed")

# Note: The SDK does not support direct string-based key presses or key combinations
# You need to use the predefined key codes or implement custom solutions
```

### Element Detection and Interaction

```python
# Get all UI elements
elements = session.ui.get_all_ui_elements()
if elements.success:
    print(f"Found {len(elements.elements)} UI elements")
    for element in elements.elements:
        print(f"Element: {element}")

# Get clickable UI elements
clickable_elements = session.ui.get_clickable_ui_elements()
if clickable_elements.success:
    print(f"Found {len(clickable_elements.elements)} clickable elements")

# Note: The SDK does not provide image-based element detection or waiting functionality
# UI element interaction is done through the methods available in the SDK
```

<a id="workflow-orchestration"></a>
## 🔄 Workflow Orchestration

### Sequential Workflows

```python
class AutomationWorkflow:
    def __init__(self, session):
        self.session = session
        
    def setup_environment(self):
        """Setup the working environment"""
        commands = [
            "mkdir -p /tmp/workspace",
            "cd /tmp/workspace",
            "python -m venv venv",
            "source venv/bin/activate"
        ]
        
        for cmd in commands:
            result = self.session.command.execute_command(cmd)
            if not result.success:
                raise Exception(f"Setup failed at: {cmd}")
        
        return True
    
    def install_dependencies(self, requirements):
        """Install Python dependencies"""
        self.session.file_system.write_file("/tmp/workspace/requirements.txt", requirements)
        result = self.session.command.execute_command(
            "cd /tmp/workspace && source venv/bin/activate && pip install -r requirements.txt"
        )
        return result.success
    
    def run_tests(self):
        """Run automated tests"""
        result = self.session.command.execute_command(
            "cd /tmp/workspace && source venv/bin/activate && python -m pytest"
        )
        return result.success
    
    def generate_report(self):
        """Generate test report"""
        code = """
import json
import datetime

report = {
    'timestamp': datetime.datetime.now().isoformat(),
    'status': 'completed',
    'tests_passed': True
}

with open('/tmp/workspace/report.json', 'w') as f:
    json.dump(report, f, indent=2)
"""
        result = self.session.code.run_code(code, "python")
        return result.success

# Usage
workflow = AutomationWorkflow(session)
workflow.setup_environment()
workflow.install_dependencies("requests\npytest")
workflow.run_tests()
workflow.generate_report()
```

### Parallel Workflows

```python
import concurrent.futures
import threading

class ParallelWorkflow:
    def __init__(self, agent_bay):
        self.agent_bay = agent_bay
        
    def create_session(self):
        """Create a new session for parallel execution"""
        result = self.agent_bay.create()
        if result.success:
            return result.session
        else:
            raise Exception(f"Failed to create session: {result.error_message}")
    
    def task_1(self):
        """Data processing task"""
        session = self.create_session()
        try:
            # Process data
            result = session.command.execute_command("python data_processor.py")
            return {"task": "data_processing", "success": result.success}
        finally:
            # Clean up session if needed
            self.agent_bay.delete(session)
    
    def task_2(self):
        """Report generation task"""
        session = self.create_session()
        try:
            # Generate report
            result = session.command.execute_command("python report_generator.py")
            return {"task": "report_generation", "success": result.success}
        finally:
            self.agent_bay.delete(session)
    
    def task_3(self):
        """Notification task"""
        session = self.create_session()
        try:
            # Send notifications
            code = """
import requests
response = requests.post('https://api.slack.com/webhook', json={'text': 'Task completed'})
print(f'Notification sent: {response.status_code}')
"""
            result = session.code.run_code(code, "python")
            return {"task": "notification", "success": result.success}
        finally:
            self.agent_bay.delete(session)
    
    def run_parallel(self):
        """Run all tasks in parallel"""
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = [
                executor.submit(self.task_1),
                executor.submit(self.task_2),
                executor.submit(self.task_3)
            ]
            
            results = []
            for future in concurrent.futures.as_completed(futures):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    results.append({"error": str(e)})
            
            return results

# Usage
workflow = ParallelWorkflow(agent_bay)
results = workflow.run_parallel()
print("Parallel execution results:", results)
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
except Exception as e:
    print("Command ultimately failed:", e)
```

### Circuit Breaker Pattern

```python
class CircuitBreaker:
    def __init__(self, failure_threshold=5, timeout=60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
    
    def call(self, func, *args, **kwargs):
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.timeout:
                self.state = "HALF_OPEN"
            else:
                raise Exception("Circuit breaker is OPEN")
        
        try:
            result = func(*args, **kwargs)
            if self.state == "HALF_OPEN":
                self.state = "CLOSED"
                self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()
            
            if self.failure_count >= self.failure_threshold:
                self.state = "OPEN"
            
            raise e

# Usage
breaker = CircuitBreaker()

def unreliable_operation():
    result = session.command.execute_command("flaky-command")
    if not result.success:
        raise Exception(result.error_message)
    return result

try:
    result = breaker.call(unreliable_operation)
    print("Operation succeeded")
except Exception as e:
    print("Operation failed:", e)
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
    with managed_session(agent_bay) as session:
        result = session.command.execute_command("echo 'Hello'")
        if result.success:
            print("Command output:", result.output)
except Exception as e:
    print("Error:", e)
```

### 2. Logging and Monitoring

```python
import logging

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
```

### 3. Configuration Management

```python
import os
from dataclasses import dataclass

@dataclass
class AutomationConfig:
    max_retries: int = 3
    timeout: int = 30
    log_level: str = "INFO"
    workspace_dir: str = "/tmp/workspace"
    
    @classmethod
    def from_env(cls):
        return cls(
            max_retries=int(os.getenv("MAX_RETRIES", "3")),
            timeout=int(os.getenv("TIMEOUT", "30")),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            workspace_dir=os.getenv("WORKSPACE_DIR", "/tmp/workspace")
        )

# Usage
config = AutomationConfig.from_env()
result = session.command.execute_command("ls", timeout_ms=config.timeout*1000)
```

### 4. Testing Automation Scripts

```python
import unittest
from unittest.mock import Mock, patch

class TestAutomation(unittest.TestCase):
    def setUp(self):
        self.mock_session = Mock()
        
    def test_command_execution(self):
        # Mock successful command
        mock_result = Mock()
        mock_result.success = True
        mock_result.output = "test output"
        self.mock_session.command.execute_command.return_value = mock_result
        
        # Test your automation function
        result = execute_with_logging(self.mock_session, "test command")
        
        self.assertTrue(result.success)
        self.assertEqual(result.output, "test output")
        self.mock_session.command.execute_command.assert_called_once_with("test command")

if __name__ == "__main__":
    unittest.main()
```

This comprehensive guide covers all aspects of automation with AgentBay SDK. Use these patterns and best practices to build robust, scalable automation solutions! 