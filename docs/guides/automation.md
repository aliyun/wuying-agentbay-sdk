# Complete Automation Guide

This guide integrates all automation features of AgentBay SDK, including command execution, code execution, UI automation, and workflow orchestration.

## 📋 Table of Contents

- [Overview](#overview)
- [Command Execution](#command-execution)
- [Code Execution](#code-execution)
- [UI Automation](#ui-automation)
- [Workflow Orchestration](#workflow-orchestration)
- [Error Handling and Retry](#error-handling-and-retry)
- [Best Practices](#best-practices)

## 🎯 Overview

AgentBay provides three main automation capabilities:

1. **Command Execution** - Execute Shell commands and system operations in the cloud
2. **Code Execution** - Run code in programming languages like Python, JavaScript, Go
3. **UI Automation** - Interact with graphical interfaces (screenshots, clicks, input, etc.)

These features can be used individually or combined to build complex automation workflows.

## 💻 Command Execution

### Basic Command Execution

<details>
<summary><strong>Python</strong></summary>

```python
# Basic command execution
result = session.command.execute("ls -la /tmp")
if not result.is_error:
    print("Output:", result.data.stdout)
    print("Error:", result.data.stderr)
    print("Exit code:", result.data.exit_code)
else:
    print("Command execution failed:", result.error)

# Command execution with timeout
result = session.command.execute("sleep 10", timeout=5)
if result.is_error:
    print("Command timed out or failed")

# Interactive command
result = session.command.execute(
    "python3", 
    input_data="print('Hello from Python')\nexit()\n"
)
```
</details>

<details>
<summary><strong>TypeScript</strong></summary>

```typescript
// Basic command execution
const result = await session.command.execute("ls -la /tmp");
if (!result.isError) {
    console.log("Output:", result.data.stdout);
    console.log("Error:", result.data.stderr);
    console.log("Exit code:", result.data.exitCode);
} else {
    console.log("Command execution failed:", result.error);
}

// Command execution with timeout
const result = await session.command.execute("sleep 10", { timeout: 5000 });
if (result.isError) {
    console.log("Command timed out or failed");
}

// Interactive command
const result = await session.command.execute("python3", {
    inputData: "print('Hello from Python')\nexit()\n"
});
```
</details>

<details>
<summary><strong>Golang</strong></summary>

```go
// Basic command execution
result, err := session.Command.ExecuteCommand("ls -la /tmp")
if err == nil && !result.IsError {
    fmt.Println("Output:", result.Data.Stdout)
    fmt.Println("Error:", result.Data.Stderr)
    fmt.Println("Exit code:", result.Data.ExitCode)
} else {
    fmt.Println("Command execution failed:", err)
}

// Command execution with timeout
options := &agentbay.CommandOptions{Timeout: 5}
result, err := session.Command.ExecuteCommandWithOptions("sleep 10", options)

// Interactive command
inputData := "print('Hello from Python')\nexit()\n"
options := &agentbay.CommandOptions{InputData: inputData}
result, err := session.Command.ExecuteCommandWithOptions("python3", options)
```
</details>

### Advanced Command Patterns

```python
# Chain commands
commands = [
    "mkdir -p /tmp/workspace",
    "cd /tmp/workspace",
    "git clone https://github.com/user/repo.git",
    "cd repo && npm install"
]

for cmd in commands:
    result = session.command.execute(cmd)
    if result.is_error:
        print(f"Failed at: {cmd}")
        break

# Parallel command execution
import concurrent.futures

def execute_command(cmd):
    return session.command.execute(cmd)

commands = ["ls /tmp", "ps aux", "df -h"]
with concurrent.futures.ThreadPoolExecutor() as executor:
    results = list(executor.map(execute_command, commands))
```

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
if not result.is_error:
    print("Output:", result.data.output)

# Code with dependencies
code = """
import requests
response = requests.get('https://api.github.com/users/octocat')
print(response.json()['name'])
"""

# Install dependencies first
session.command.execute("pip install requests")
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
```

### Code Execution with File I/O

```python
# Upload code file
session.filesystem.write("/tmp/script.py", """
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
result = session.command.execute("python /tmp/script.py arg1 arg2")
print("Script output:", result.data.stdout)

# Read output file
output = session.filesystem.read("/tmp/output.json")
print("File content:", output.data)
```

## 🖱️ UI Automation

### Screenshot and Visual Operations

```python
# Take screenshot
screenshot = session.ui.screenshot()
if not screenshot.is_error:
    # Save screenshot locally
    with open("screenshot.png", "wb") as f:
        f.write(screenshot.data)

# Click at coordinates
result = session.ui.click(x=100, y=200)

# Double click
result = session.ui.double_click(x=150, y=250)

# Right click
result = session.ui.right_click(x=200, y=300)
```

### Keyboard and Text Input

```python
# Type text
result = session.ui.type("Hello AgentBay!")

# Press keys
result = session.ui.key_press("Enter")
result = session.ui.key_press("Ctrl+C")
result = session.ui.key_press("Alt+Tab")

# Key combinations
result = session.ui.key_combination(["Ctrl", "Shift", "N"])
```

### Element Detection and Interaction

```python
# Find element by image (template matching)
element = session.ui.find_element_by_image("button_template.png")
if element.success:
    session.ui.click(element.data.x, element.data.y)

# Wait for element to appear
element = session.ui.wait_for_element("login_button.png", timeout=10)
if element.success:
    session.ui.click(element.data.x, element.data.y)
```

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
            result = self.session.command.execute(cmd)
            if result.is_error:
                raise Exception(f"Setup failed at: {cmd}")
        
        return True
    
    def install_dependencies(self, requirements):
        """Install Python dependencies"""
        self.session.filesystem.write("/tmp/workspace/requirements.txt", requirements)
        result = self.session.command.execute(
            "cd /tmp/workspace && source venv/bin/activate && pip install -r requirements.txt"
        )
        return not result.is_error
    
    def run_tests(self):
        """Run automated tests"""
        result = self.session.command.execute(
            "cd /tmp/workspace && source venv/bin/activate && python -m pytest"
        )
        return not result.is_error
    
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
        return not result.is_error

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
        return self.agent_bay.create().session
    
    def task_1(self):
        """Data processing task"""
        session = self.create_session()
        try:
            # Process data
            result = session.command.execute("python data_processor.py")
            return {"task": "data_processing", "success": not result.is_error}
        finally:
            # Clean up session if needed
            pass
    
    def task_2(self):
        """Report generation task"""
        session = self.create_session()
        try:
            # Generate report
            result = session.command.execute("python report_generator.py")
            return {"task": "report_generation", "success": not result.is_error}
        finally:
            pass
    
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
            return {"task": "notification", "success": not result.is_error}
        finally:
            pass
    
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

## 🚨 Error Handling and Retry

### Retry Mechanisms

```python
import time
import random

def execute_with_retry(session, command, max_retries=3, delay=1):
    """Execute command with exponential backoff retry"""
    for attempt in range(max_retries):
        try:
            result = session.command.execute(command)
            if not result.is_error:
                return result
            
            print(f"Attempt {attempt + 1} failed: {result.error}")
            
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
    print("Command succeeded:", result.data.stdout)
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
    result = session.command.execute("flaky-command")
    if result.is_error:
        raise Exception(result.error)
    return result

try:
    result = breaker.call(unreliable_operation)
    print("Operation succeeded")
except Exception as e:
    print("Operation failed:", e)
```

## 💡 Best Practices

### 1. Resource Management

```python
# Use context managers for session management
from contextlib import contextmanager

@contextmanager
def managed_session(agent_bay):
    session = agent_bay.create().session
    try:
        yield session
    finally:
        # Cleanup if needed
        pass

# Usage
with managed_session(agent_bay) as session:
    result = session.command.execute("echo 'Hello'")
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
        result = session.command.execute(command)
        duration = time.time() - start_time
        
        if result.is_error:
            logger.error(f"Command failed in {duration:.2f}s: {result.error}")
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
result = session.command.execute("ls", timeout=config.timeout)
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
        mock_result.is_error = False
        mock_result.data.stdout = "test output"
        self.mock_session.command.execute.return_value = mock_result
        
        # Test your automation function
        result = execute_with_logging(self.mock_session, "test command")
        
        self.assertFalse(result.is_error)
        self.assertEqual(result.data.stdout, "test output")
        self.mock_session.command.execute.assert_called_once_with("test command")

if __name__ == "__main__":
    unittest.main()
```

This comprehensive guide covers all aspects of automation with AgentBay SDK. Use these patterns and best practices to build robust, scalable automation solutions! 