# Create Your First Session

Now let's experience the core features of AgentBay through actual code.

## 🚀 Before You Start (2-minute setup)

If you haven't completed the setup yet, please complete the quick setup steps:

👉 **[Installation and API Key Setup Guide](installation.md)** - Complete SDK installation and API key configuration in 2 minutes

Already done? Great! Let's verify everything works with a quick test.

## 💡 30-Second Quick Verification

Let's first verify everything works with the simplest possible example:

```python
import os
from agentbay import AgentBay

# Initialize client
api_key = os.getenv("AGENTBAY_API_KEY")
agent_bay = AgentBay(api_key=api_key)

# Create session, run command, cleanup
result = agent_bay.create()
if result.success:
    session = result.session
    cmd_result = session.command.execute_command("echo 'Hello from the cloud!'")
    print(f"✅ Cloud says: {cmd_result.output.strip()}")
    agent_bay.delete(session)
else:
    print(f"❌ Failed: {result.error_message}")

# Expected output:
# ✅ Cloud says: Hello from the cloud!
```

If this works, you're ready to explore more! 🎉

## 🌟 Why Use Cloud Environment?

Here's what makes AgentBay special - things you can't easily do locally:

```python
import os
from agentbay import AgentBay

agent_bay = AgentBay(api_key=os.getenv("AGENTBAY_API_KEY"))
result = agent_bay.create()
session = result.session

# 1. Always clean environment - no leftover files or processes
cmd_result = session.command.execute_command("ps aux | wc -l")
print(f"Running processes: {cmd_result.output.strip()}")
# Expected: Running processes: 240

# 2. Internet access from cloud infrastructure
cmd_result = session.command.execute_command("curl -s https://httpbin.org/ip")
print(f"Cloud IP: {cmd_result.output}")
# Expected: Cloud IP: {"origin": "xxx.xxx.xxx.xxx"}

# 3. Pre-installed tools without local setup
cmd_result = session.command.execute_command("python3 --version && node --version")
print(f"Available tools:\n{cmd_result.output}")
# Expected: Available tools:
# Python 3.10.12
# v22.15.1

# 4. Different system environments
print(f"Running on: {session.command.execute_command('cat /etc/os-release | head -1').output}")
# Expected: Running on: PRETTY_NAME="Ubuntu 22.04.5 LTS"

agent_bay.delete(session)
```

## 📝 Complete Real-World Example: Smart Calculator Project

Let's build a complete project that showcases professional development practices in the cloud:

```python
import os
from agentbay import AgentBay
from agentbay.session_params import CreateSessionParams

def smart_calculator_project():
    """
    Complete project example: Build a Smart Calculator with OOP
    Perfect for learning programming concepts in a cloud environment
    """
    print("🧮 Building Smart Calculator in the Cloud...")
    
    # Use CodeSpace environment for development
    agent_bay = AgentBay(api_key=os.getenv("AGENTBAY_API_KEY"))
    code_params = CreateSessionParams(image_id="code_latest")
    result = agent_bay.create(code_params)
    session = result.session
    print(f"✅ Cloud development environment ready: {session.session_id}")
    
    try:
        # 1. Create the Smart Calculator class
        print("\n📝 Creating Smart Calculator project...")
        
        calculator_code = '''
"""Smart Calculator - Object-Oriented Programming Example"""
import json
from datetime import datetime

class SmartCalculator:
    """A smart calculator that tracks history and provides statistics"""
    
    def __init__(self, name="Smart Calculator"):
        self.name = name
        self.history = []
        self.created_time = datetime.now()
        print(f"🧮 {self.name} initialized!")
    
    def add(self, a, b):
        result = a + b
        self._save_operation(f"{a} + {b}", result)
        return result
    
    def subtract(self, a, b):
        result = a - b
        self._save_operation(f"{a} - {b}", result)
        return result
    
    def multiply(self, a, b):
        result = a * b
        self._save_operation(f"{a} × {b}", result)
        return result
    
    def divide(self, a, b):
        try:
            if b == 0:
                raise ValueError("Cannot divide by zero!")
            result = a / b
            self._save_operation(f"{a} ÷ {b}", result)
            return result
        except ValueError as e:
            error_msg = f"Error: {str(e)}"
            self._save_operation(f"{a} ÷ {b}", error_msg)
            print(f"❌ {error_msg}")
            return None
    
    def power(self, base, exponent):
        result = base ** exponent
        self._save_operation(f"{base} ^ {exponent}", result)
        return result
    
    def _save_operation(self, operation, result):
        """Private method to save operation history"""
        record = {
            "operation": operation,
            "result": result,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.history.append(record)
    
    def get_statistics(self):
        """Generate usage statistics"""
        total_ops = len(self.history)
        if total_ops == 0:
            return "No calculations yet"
        
        op_types = {}
        for record in self.history:
            op = record["operation"]
            if "+" in op: op_types["Addition"] = op_types.get("Addition", 0) + 1
            elif "-" in op: op_types["Subtraction"] = op_types.get("Subtraction", 0) + 1
            elif "×" in op: op_types["Multiplication"] = op_types.get("Multiplication", 0) + 1
            elif "÷" in op: op_types["Division"] = op_types.get("Division", 0) + 1
            elif "^" in op: op_types["Power"] = op_types.get("Power", 0) + 1
        
        return {
            "total_operations": total_ops,
            "operation_types": op_types,
            "uptime": str(datetime.now() - self.created_time)
        }
    
    def save_data(self, filename="/tmp/calculator_data.json"):
        """Save all data to file"""
        data = {
            "calculator_name": self.name,
            "history": self.history,
            "statistics": self.get_statistics()
        }
        
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
        print(f"💾 Data saved to {filename}")

# Demonstration function
def demo_calculator():
    print("\\n🚀 Smart Calculator Demo Starting...")
    
    calc = SmartCalculator("AgentBay Cloud Calculator")
    
    # Perform various operations
    print("\\n🔢 Performing calculations...")
    print(f"✅ 15 + 25 = {calc.add(15, 25)}")
    print(f"✅ 100 - 35 = {calc.subtract(100, 35)}")
    print(f"✅ 8 × 7 = {calc.multiply(8, 7)}")
    print(f"✅ 144 ÷ 12 = {calc.divide(144, 12)}")
    print(f"✅ 2 ^ 10 = {calc.power(2, 10)}")
    
    # Test error handling
    print("\\n⚠️ Testing error handling...")
    calc.divide(10, 0)  # This will show error handling
    
    # Show statistics
    print("\\n📊 Calculator Statistics:")
    stats = calc.get_statistics()
    print(f"  Total operations: {stats['total_operations']}")
    print(f"  Operation breakdown: {stats['operation_types']}")
    
    # Save data
    calc.save_data()
    
    return calc

if __name__ == "__main__":
    calculator = demo_calculator()
    print("\\n🎉 Smart Calculator demo completed!")
'''
        
        # Write to cloud environment
        session.file_system.write_file("/tmp/smart_calculator.py", calculator_code)
        
        # 2. Run the calculator
        print("\n🔄 Running Smart Calculator...")
        run_result = session.command.execute_command("cd /tmp && python3 smart_calculator.py")
        print("Calculator Output:")
        print(run_result.output)
        
        # 3. Read the saved data
        print("\n📊 Reading saved calculator data...")
        file_result = session.file_system.read_file("/tmp/calculator_data.json")
        if file_result.success:
            import json
            data = json.loads(file_result.content)
            print("📋 Data Summary:")
            print(f"  Calculator: {data['calculator_name']}")
            print(f"  Total Operations: {data['statistics']['total_operations']}")
            print(f"  Operation Types: {list(data['statistics']['operation_types'].keys())}")
        
        # 4. Show project files and statistics
        print("\n📁 Project Structure:")
        files_result = session.command.execute_command("ls -la /tmp/*.py /tmp/*.json && echo '\\nCode Statistics:' && wc -l /tmp/smart_calculator.py")
        print(files_result.output)
        
        print("\n🎉 Smart Calculator project completed!")
        print("\n💡 This example demonstrates:")
        print("  🎯 Object-Oriented Programming (classes, methods)")
        print("  🛡️ Error handling and exception management")
        print("  💾 File operations and data persistence")
        print("  📊 Data analysis and statistics")
        print("  🏗️ Complete project structure")
        print("\n🚀 All developed in the cloud - no local setup required!")
        
        # Expected output includes:
        # 🧮 AgentBay Cloud Calculator initialized!
        # ✅ 15 + 25 = 40
        # ✅ 100 - 35 = 65  
        # ✅ 8 × 7 = 56
        # ✅ 144 ÷ 12 = 12.0
        # ✅ 2 ^ 10 = 1024
        # ❌ Error: Cannot divide by zero!
        # 📊 Calculator Statistics:
        #   Total operations: 6
        #   Operation breakdown: {'Addition': 1, 'Subtraction': 1, 'Multiplication': 1, 'Division': 2, 'Power': 1}
        
    finally:
        agent_bay.delete(session)
        print("✅ Cloud environment cleaned up")

if __name__ == "__main__":
    smart_calculator_project()
```

## 🎯 Session Management in Practice

Now that you've seen sessions in action, let's dive deeper into session management best practices.

💡 **Need to understand Session concepts first?** Check out [Core Concepts - Sessions](basic-concepts.md#-session) for detailed explanations.

### Advanced Session Creation Patterns

**Pattern 1: Error-Safe Session Creation**
```python
def create_session_safely(image_id="linux_latest"):
    """Create session with proper error handling"""
    agent_bay = AgentBay(api_key=os.getenv("AGENTBAY_API_KEY"))
    
    # Create with specific environment
    params = CreateSessionParams(image_id=image_id) if image_id != "linux_latest" else None
    result = agent_bay.create(params)
    
    if result.success:
        print(f"✅ Session created: {result.session.session_id}")
        return result.session, agent_bay
    else:
        print(f"❌ Failed: {result.error_message}")
        return None, None

# Usage
session, client = create_session_safely("browser_latest")
if session:
    # Your work here
    client.delete(session)
```

**Pattern 2: Context Manager (Automatic Cleanup)**
```python
class SessionManager:
    def __init__(self, image_id="linux_latest"):
        self.agent_bay = AgentBay(api_key=os.getenv("AGENTBAY_API_KEY"))
        self.image_id = image_id
        self.session = None
    
    def __enter__(self):
        params = CreateSessionParams(image_id=self.image_id) if self.image_id != "linux_latest" else None
        result = self.agent_bay.create(params)
        if result.success:
            self.session = result.session
            return self.session
        else:
            raise Exception(f"Session creation failed: {result.error_message}")
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            self.agent_bay.delete(self.session)
            print("🧹 Session automatically cleaned up")

# Usage - automatic cleanup even if errors occur
try:
    with SessionManager("code_latest") as session:
        # Python code execution
        py_result = session.code.run_code("print('Hello from CodeSpace!')", "python")
        print(f"Python output: {py_result.result}")
        
        # JavaScript code execution
        js_result = session.code.run_code("console.log('Hello from CodeSpace!')", "javascript")
        print(f"JavaScript output: {js_result.result}")
        
        # Session automatically deleted when exiting 'with' block
except Exception as e:
    print(f"Error: {e}")
```

### Choosing the Right Environment

Based on your task, here's how to pick the optimal image:

```python
def get_session_for_task(task_type):
    """Get the right session for your specific task"""
    
    task_configs = {
        "web_scraping": {
            "image_id": "browser_latest",
            "description": "Pre-configured browsers with stealth mode"
        },
        "code_development": {
            "image_id": "code_latest", 
            "description": "Python and JavaScript development environment"
        },
        "windows_automation": {
            "image_id": "windows_latest",
            "description": "Full Windows desktop environment"
        },
        "mobile_testing": {
            "image_id": "mobile_latest",
            "description": "Android emulator environment"
        },
        "general_computing": {
            "image_id": "linux_latest",
            "description": "Standard Linux with common tools"
        }
    }
    
    if task_type in task_configs:
        config = task_configs[task_type]
        print(f"📋 Task: {task_type}")
        print(f"🎯 Environment: {config['description']}")
        
        params = CreateSessionParams(image_id=config["image_id"]) 
        return params
    else:
        print("⚠️  Unknown task type, using default Linux environment")
        return None

# Example usage
agent_bay = AgentBay(api_key=os.getenv("AGENTBAY_API_KEY"))

# Create session optimized for code development
params = get_session_for_task("code_development")
session = agent_bay.create(params).session

# Your Python/JavaScript development here...
agent_bay.delete(session)
```


## 🎯 Run These Examples

### Quick Test
1. Save this as `quick_test.py`:
```python
import os
from agentbay import AgentBay

agent_bay = AgentBay(api_key=os.getenv("AGENTBAY_API_KEY"))
result = agent_bay.create()
if result.success:
    print("✅ AgentBay is working!")
    agent_bay.delete(result.session)
else:
    print(f"❌ Error: {result.error_message}")

# Expected output when working:
# ✅ AgentBay is working!
```

2. Set up virtual environment and run:
```bash
# Create virtual environment (if needed)
python3 -m venv test_env
source test_env/bin/activate

# Install SDK
pip install wuying-agentbay-sdk

# Make sure API key is set
export AGENTBAY_API_KEY="your-api-key"

# Run the test
python quick_test.py
```

### Full Example
Save the web data processor example and run it to see real cloud computing in action!

## 💡 Key Takeaways

1. **Clean Environment**: Every session starts fresh - no leftover files or processes
2. **Cloud Resources**: Access internet, install packages, run intensive tasks
3. **Multiple Environments**: Choose Windows, Linux, Browser, or Mobile environments
4. **Session Management**: Always delete sessions when done to save resources

## 🚀 Next Steps

Now that you've successfully created your first session, learn the core features that every AgentBay developer needs:

### 🔧 **Core Features**
- **[Session Management](../guides/session-management.md)** - Cloud environment lifecycle management
- **[File Operations](../guides/file-operations.md)** - File upload, download, and management  
- **[Data Persistence](../guides/data-persistence.md)** - Cross-session data storage
- **[SDK Configuration](../guides/sdk-configuration.md)** - Configuration options and settings

### 🎯 **Specialized Use Cases**
- **[Automation](../guides/automation.md)** - Complex workflow automation and command execution patterns
- **[Browser Use](../guides/browser-use/README.md)** - Complete browser automation with Playwright integration
- **[Application & Window Operations](../guides/application-window-operations.md)** - Desktop application control and window management
- **[Advanced Features](../guides/advanced-features.md)** - VPC sessions, agent modules, and browser automation

### 🔧 **When You Need Help**
- **[Feature Guides Overview](../guides/README.md)** - Quick navigation to all advanced features

### 📖 **Reference Materials**  
- **[Getting Started](../getting-started.md)** - Overview and introduction

## 🎉 You're Ready!

You can now:
- ✅ Create and manage cloud sessions with confidence
- ✅ Execute commands remotely and handle errors gracefully
- ✅ Process data in the cloud environment
- ✅ Handle files and directories effectively
- ✅ Choose the right environment for your tasks
- ✅ Troubleshoot common issues independently

**Ready to build something amazing?** Pick a guide above that matches your next goal! 🚀
