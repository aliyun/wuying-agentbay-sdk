# Code Execution Guide (CodeSpace)

This guide covers code execution capabilities in AgentBay SDK's CodeSpace environment. CodeSpace provides a dedicated development environment optimized for running code in Python and JavaScript.

## 📋 Table of Contents

- [Overview](#overview)
- [CodeSpace Environment](#codespace-environment)
- [Enhanced Code Execution](#enhanced-code-execution)
- [Python Code Execution](#python-code-execution)
- [JavaScript Code Execution](#javascript-code-execution)
- [Rich Output Formats](#rich-output-formats)
- [Code Execution with File I/O](#code-execution-with-file-io)
- [Best Practices](#best-practices)

<a id="overview"></a>
## 🎯 Overview

CodeSpace is AgentBay's development-focused environment that provides:

- **Multi-language Support** - Run Python and JavaScript/Node.js code
- **Isolated Execution** - Secure, containerized code execution
- **Enhanced Results** - Rich output formats including HTML, images, charts, and more
- **Development Tools** - Pre-installed interpreters and development utilities
- **File Operations** - Read and write files for script execution

<a id="codespace-environment"></a>
## 🔧 CodeSpace Environment

### Creating a CodeSpace Session

To use code execution features, create a session with the `code_latest` image:

```python
from agentbay import AgentBay
from agentbay import CreateSessionParams

agent_bay = AgentBay(api_key="your-api-key")

session_params = CreateSessionParams(image_id="code_latest")
result = agent_bay.create(session_params)

if result.success:
    session = result.session
    print(f"CodeSpace session created: {session.session_id}")
else:
    print(f"Failed to create session: {result.error_message}")
```

**Important:** The `run_code()` method requires `image_id="code_latest"` when creating the session.

<a id="enhanced-code-execution"></a>
## ✨ Enhanced Code Execution

AgentBay now provides enhanced code execution results with rich output formats and detailed execution information.

### Enhanced Result Structure

```python
from agentbay import AgentBay, CreateSessionParams, EnhancedCodeExecutionResult

agent_bay = AgentBay(api_key="your-api-key")
session_params = CreateSessionParams(image_id="code_latest")
result = agent_bay.create(session_params)

if result.success:
    session = result.session
    
    code = """
print("Hello, Enhanced AgentBay!")
result = 2 + 2
print(f"2 + 2 = {result}")
result
"""
    
    result = session.code.run_code(code, "python")
    
    # Enhanced result provides rich information
    print(f"Success: {result.success}")
    print(f"Execution time: {result.execution_time}s")
    print(f"Request ID: {result.request_id}")
    
    # Access logs
    print(f"Stdout: {result.logs.stdout}")
    print(f"Stderr: {result.logs.stderr}")
    
    # Access results in multiple formats
    for i, res in enumerate(result.results):
        print(f"Result {i}: {res.text}")
        print(f"Available formats: {res.formats()}")
    
    # Backward compatibility - still works
    print(f"Result (legacy): {result.result}")
    
    session.delete()
```

### Working with Result Types

```python
from agentbay import (
    AgentBay, 
    CreateSessionParams,
    EnhancedCodeExecutionResult,
    ExecutionResult,
    ExecutionLogs,
    ExecutionError
)

# Type checking and handling
result = session.code.run_code(code, "python")

if isinstance(result, EnhancedCodeExecutionResult):
    # Access execution logs
    if isinstance(result.logs, ExecutionLogs):
        print(f"Stdout lines: {len(result.logs.stdout)}")
        print(f"Stderr lines: {len(result.logs.stderr)}")
    
    # Process multiple results
    for exec_result in result.results:
        if isinstance(exec_result, ExecutionResult):
            if exec_result.text:
                print(f"Text output: {exec_result.text}")
            if exec_result.html:
                print(f"HTML output: {exec_result.html}")
    
    # Handle errors
    if result.error and isinstance(result.error, ExecutionError):
        print(f"Error: {result.error.name} - {result.error.value}")
```

<a id="python-code-execution"></a>
## 🐍 Python Code Execution

### Basic Python Execution

```python
from agentbay import AgentBay
from agentbay import CreateSessionParams

agent_bay = AgentBay(api_key="your-api-key")

session_params = CreateSessionParams(image_id="code_latest")
result = agent_bay.create(session_params)

if result.success:
    session = result.session
    
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
        # Output: Python version: 3.11.2 (main, Apr 28 2025, 14:11:48) [GCC 12.2.0]
        #         Current directory: /workspace
        #         Hello from AgentBay!
    else:
        print("Execution failed:", result.error_message)
    
    agent_bay.delete(session)
```

### Python with Calculations

```python
session_params = CreateSessionParams(image_id="code_latest")
result = agent_bay.create(session_params)

if result.success:
    session = result.session
    
    code = """
import math

# Calculate factorial
def factorial(n):
    return math.factorial(n)

# Fibonacci sequence
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(f"Factorial of 10: {factorial(10)}")
print(f"Fibonacci of 10: {fibonacci(10)}")

# List comprehension
squares = [x**2 for x in range(1, 11)]
print(f"Squares: {squares}")
"""
    
    result = session.code.run_code(code, "python")
    if result.success:
        print("Output:", result.result)
        # Output: Factorial of 10: 3628800
        #         Fibonacci of 10: 55
        #         Squares: [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
    
    agent_bay.delete(session)
```

<a id="javascript-code-execution"></a>
## 🟨 JavaScript Code Execution

### Node.js Code Execution

```python
from agentbay import AgentBay
from agentbay import CreateSessionParams

agent_bay = AgentBay(api_key="your-api-key")

session_params = CreateSessionParams(image_id="code_latest")
result = agent_bay.create(session_params)

if result.success:
    session = result.session
    
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
        # Output: Node.js version: v18.20.5
        #         Current directory: /workspace
        #         File created successfully
    else:
        print("Execution failed:", result.error_message)
    
    agent_bay.delete(session)
```

### JavaScript with Data Processing

```python
session_params = CreateSessionParams(image_id="code_latest")
result = agent_bay.create(session_params)

if result.success:
    session = result.session
    
    js_code = """
// Array operations
const numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

const sum = numbers.reduce((a, b) => a + b, 0);
const avg = sum / numbers.length;
const squares = numbers.map(x => x * x);

console.log('Numbers:', numbers);
console.log('Sum:', sum);
console.log('Average:', avg);
console.log('Squares:', squares);

// Object manipulation
const data = {
    name: 'AgentBay',
    version: '1.0',
    features: ['Python', 'JavaScript', 'File I/O']
};

console.log('\\nData:', JSON.stringify(data, null, 2));
"""
    
    result = session.code.run_code(js_code, "javascript")
    if result.success:
        print("Output:", result.result)
        # Output: Numbers: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        #         Sum: 55
        #         Average: 5.5
        #         Squares: [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
        #         
        #         Data: {
        #           "name": "AgentBay",
        #           "version": "1.0",
        #           "features": [
        #             "Python",
        #             "JavaScript",
        #             "File I/O"
        #           ]
        #         }
    
    agent_bay.delete(session)
```

<a id="rich-output-formats"></a>
## 🎨 Rich Output Formats

AgentBay's enhanced code execution supports multiple output formats including HTML, images, charts, and more.

### HTML Output

```python
from agentbay import AgentBay, CreateSessionParams

agent_bay = AgentBay(api_key="your-api-key")
session_params = CreateSessionParams(image_id="code_latest")
result = agent_bay.create(session_params)

if result.success:
    session = result.session
    
    code = """
from IPython.display import display, HTML

# Create HTML output
html_content = '''
<div style="background: #f0f8ff; padding: 20px; border-radius: 10px;">
    <h2 style="color: #2e8b57;">AgentBay Results</h2>
    <p>This is <strong>HTML output</strong> from code execution!</p>
    <ul>
        <li>Rich formatting</li>
        <li>Interactive elements</li>
        <li>Custom styling</li>
    </ul>
</div>
'''

display(HTML(html_content))
"""
    
    result = session.code.run_code(code, "python")
    
    # Check for HTML output
    for res in result.results:
        if res.html:
            print("HTML output found:")
            print(res.html)
    
    session.delete()
```

### Markdown Output

```python
code = """
from IPython.display import display, Markdown

markdown_content = '''
# AgentBay Code Execution

## Features

- **Enhanced Results**: Multiple output formats
- **Rich Content**: HTML, Markdown, Images
- **Performance**: Execution timing and metadata

### Example Table

| Language | Support | Performance |
|----------|---------|-------------|
| Python   | ✅      | Excellent   |
| JavaScript| ✅     | Excellent   |

> This is generated from code execution!
'''

display(Markdown(markdown_content))
"""

result = session.code.run_code(code, "python")

# Check for Markdown output
for res in result.results:
    if res.markdown:
        print("Markdown output found:")
        print(res.markdown)
```

### Image Output (Charts and Plots)

```python
code = """
import matplotlib.pyplot as plt
import numpy as np

# Create a simple plot
x = np.linspace(0, 10, 100)
y = np.sin(x)

plt.figure(figsize=(10, 6))
plt.plot(x, y, 'b-', linewidth=2, label='sin(x)')
plt.title('Sine Wave Generated by AgentBay')
plt.xlabel('x')
plt.ylabel('sin(x)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
"""

result = session.code.run_code(code, "python")

# Check for image output
for res in result.results:
    if res.png:
        print("PNG image found (base64 encoded)")
        # res.png contains base64 encoded image data
    if res.jpeg:
        print("JPEG image found (base64 encoded)")
        # res.jpeg contains base64 encoded image data
```

### SVG Output

```python
code = """
from IPython.display import display, SVG

svg_content = '''
<svg width="200" height="200" xmlns="http://www.w3.org/2000/svg">
  <circle cx="100" cy="100" r="80" fill="#4CAF50" stroke="#2E7D32" stroke-width="4"/>
  <text x="100" y="110" text-anchor="middle" fill="white" font-size="16" font-family="Arial">
    AgentBay
  </text>
</svg>
'''

display(SVG(svg_content))
"""

result = session.code.run_code(code, "python")

# Check for SVG output
for res in result.results:
    if res.svg:
        print("SVG output found:")
        print(res.svg)
```

### LaTeX Mathematical Expressions

```python
code = r"""
from IPython.display import display, Latex

latex_content = r'''
\begin{align}
E &= mc^2 \\
F &= ma \\
\nabla \cdot \mathbf{E} &= \frac{\rho}{\epsilon_0}
\end{align}
'''

display(Latex(latex_content))
"""

result = session.code.run_code(code, "python")

# Check for LaTeX output
for res in result.results:
    if res.latex:
        print("LaTeX output found:")
        print(res.latex)
```

### Chart Data (Vega-Lite)

```python
code = """
# Simulate chart output with structured data
class MockChart:
    def _repr_mimebundle_(self, include=None, exclude=None):
        return {
            "application/vnd.vegalite.v4+json": {
                "data": {"values": [
                    {"x": "A", "y": 28},
                    {"x": "B", "y": 55},
                    {"x": "C", "y": 43},
                    {"x": "D", "y": 91}
                ]},
                "mark": "bar",
                "encoding": {
                    "x": {"field": "x", "type": "nominal"},
                    "y": {"field": "y", "type": "quantitative"}
                }
            }
        }

from IPython.display import display
display(MockChart())
"""

result = session.code.run_code(code, "python")

# Check for chart data
for res in result.results:
    if res.chart:
        print("Chart data found:")
        print(res.chart)
```

<a id="code-execution-with-file-io"></a>
## 📁 Code Execution with File I/O

### Writing and Executing Scripts

```python
from agentbay import AgentBay

agent_bay = AgentBay(api_key="your-api-key")
result = agent_bay.create()

if result.success:
    session = result.session
    
    script_content = """
import json
import sys

data = {
    'message': 'Hello from uploaded script',
    'args': sys.argv[1:] if len(sys.argv) > 1 else []
}

with open('/tmp/output.json', 'w') as f:
    json.dump(data, f, indent=2)

print(json.dumps(data, indent=2))
"""
    
    write_result = session.file_system.write_file("/tmp/script.py", script_content)
    if write_result.success:
        print("Script uploaded successfully")
        
        exec_result = session.command.execute_command("python3 /tmp/script.py arg1 arg2")
        if exec_result.success:
            print("Script output:", exec_result.output)
            # Script output: {
            #   "message": "Hello from uploaded script",
            #   "args": [
            #     "arg1",
            #     "arg2"
            #   ]
            # }
            
            output_result = session.file_system.read_file("/tmp/output.json")
            if output_result.success:
                print("Output file content:", output_result.content)
                # Output file content: {
                #   "message": "Hello from uploaded script",
                #   "args": [
                #     "arg1",
                #     "arg2"
                #   ]
                # }
        else:
            print("Execution failed:", exec_result.error_message)
    else:
        print("Failed to write script:", write_result.error_message)
    
    agent_bay.delete(session)
```

### Multi-file Projects

```python
from agentbay import AgentBay
from agentbay import CreateSessionParams

agent_bay = AgentBay(api_key="your-api-key")

session_params = CreateSessionParams(image_id="code_latest")
result = agent_bay.create(session_params)

if result.success:
    session = result.session
    
    session.file_system.create_directory("/workspace/myproject")
    
    main_py = """
from utils import greet

if __name__ == "__main__":
    print(greet("AgentBay"))
"""
    
    utils_py = """
def greet(name):
    return f"Hello, {name}!"
"""
    
    session.file_system.write_file("/workspace/myproject/main.py", main_py)
    session.file_system.write_file("/workspace/myproject/utils.py", utils_py)
    
    result = session.command.execute_command("cd /workspace/myproject && python3 main.py")
    if result.success:
        print("Project output:", result.output)
        # Project output: Hello, AgentBay!
    else:
        print("Execution failed:", result.error_message)
    
    agent_bay.delete(session)
```

<a id="best-practices"></a>
## 💡 Best Practices

### 1. Use Enhanced Result Types

Always use the enhanced result types for better type safety and functionality:

```python
from agentbay import EnhancedCodeExecutionResult, ExecutionResult

result = session.code.run_code(code, "python")

# Type-safe access to enhanced features
if isinstance(result, EnhancedCodeExecutionResult):
    # Access execution metadata
    print(f"Execution time: {result.execution_time}s")
    
    # Check all available output formats
    for res in result.results:
        if isinstance(res, ExecutionResult):
            formats = res.formats()
            print(f"Available formats: {formats}")
```

### 2. Handle Multiple Output Formats

Code execution can produce multiple types of output. Check all available formats:

```python
result = session.code.run_code(code, "python")

for i, res in enumerate(result.results):
    print(f"Result {i}:")
    
    if res.text:
        print(f"  Text: {res.text}")
    if res.html:
        print(f"  HTML available: {len(res.html)} chars")
    if res.png:
        print(f"  PNG image available")
    if res.markdown:
        print(f"  Markdown available")
    if res.chart:
        print(f"  Chart data available")
```

### 3. Monitor Execution Logs

Use the enhanced logging capabilities to debug and monitor your code:

```python
result = session.code.run_code(code, "python")

# Check stdout and stderr separately
if result.logs.stdout:
    print("Standard output:")
    for line in result.logs.stdout:
        print(f"  {line.strip()}")

if result.logs.stderr:
    print("Error output:")
    for line in result.logs.stderr:
        print(f"  {line.strip()}")
```

### 4. Use Timeout for Long-Running Code

The default timeout for `run_code()` is 60 seconds. **Note: Due to gateway limitations, each request cannot exceed 60 seconds.**

```python
# Default timeout is 60 seconds
result = session.code.run_code(code, "python")

# You can specify a custom timeout (max 60 seconds)
result = session.code.run_code(code, "python", timeout_s=60)
```

### 5. Error Handling with Enhanced Details

Take advantage of enhanced error information:

```python
result = session.code.run_code(code, "python")

if not result.success:
    # Check for detailed error information
    if result.error:
        print(f"Error type: {result.error.name}")
        print(f"Error message: {result.error.value}")
        print(f"Traceback: {result.error.traceback}")
    else:
        # Fallback to basic error message
        print(f"Error: {result.error_message}")
    
    # Check stderr for additional error details
    if result.logs.stderr:
        print("Additional error output:")
        for line in result.logs.stderr:
            print(f"  {line.strip()}")
```

### 6. Use Standard Library Only

CodeSpace comes with Python and Node.js standard libraries pre-installed. For best performance and reliability, use only built-in modules:

**Python**: `os`, `sys`, `json`, `math`, `datetime`, `re`, `matplotlib`, `numpy`, etc.  
**JavaScript**: `fs`, `path`, `os`, `crypto`, etc.

### 7. Backward Compatibility

The enhanced results maintain backward compatibility with existing code:

```python
# Old way (still works)
result = session.code.run_code(code, "python")
print(result.result)  # Returns combined text output

# New way (recommended)
result = session.code.run_code(code, "python")
for res in result.results:
    if res.is_main_result:
        print(res.text)  # Get the main result specifically
```

## 📚 Related Documentation

- [Code API Reference (Sync)](../../python/docs/api/sync/code.md) - Synchronous code execution API
- [AsyncCode API Reference](../../python/docs/api/async/async-code.md) - Asynchronous code execution API
- [Code Execution Models](../../python/docs/api/common/code-models.md) - Enhanced result types and data models
- [File Operations](../common-features/basics/file-operations.md) - File handling and management
- [Session Management](../common-features/basics/session-management.md) - Session lifecycle and configuration
- [Command Execution](../common-features/basics/command-execution.md) - Shell command execution

## 🆘 Getting Help

- [GitHub Issues](https://github.com/aliyun/wuying-agentbay-sdk/issues)
- [Documentation Home](../README.md)

Happy coding with AgentBay CodeSpace! 🚀
