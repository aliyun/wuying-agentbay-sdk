#!/usr/bin/env python3
"""
AgentBay SDK - CodeSpace Example

This example demonstrates how to use AgentBay SDK code execution features:
- Python code execution
- JavaScript code execution
- File operations in code environment
- Command execution in code environment
"""

import os
from agentbay import AgentBay
from agentbay.session_params import CreateSessionParams


def main():
    """Main function demonstrating code execution features"""
    print("🚀 AgentBay CodeSpace Example")

    # Initialize AgentBay client
    api_key = os.getenv("AGENTBAY_API_KEY")
    if not api_key:
        print("❌ Error: AGENTBAY_API_KEY environment variable not set")
        return

    agent_bay = AgentBay(api_key=api_key)

    # Create session with code_latest image
    print("\n📱 Creating session with code_latest image...")
    params = CreateSessionParams(image_id="code_latest")
    session_result = agent_bay.create(params)

    if not session_result.success:
        print(f"❌ Session creation failed: {session_result.error_message}")
        return

    session = session_result.session
    print(f"✅ Session created successfully: {session.session_id}")

    try:
        # ===== PYTHON CODE EXECUTION =====
        print("\n===== PYTHON CODE EXECUTION =====")

        python_code = """
import sys
import os
import json
from datetime import datetime

# System information
system_info = {
    "python_version": sys.version,
    "current_directory": os.getcwd(),
    "timestamp": datetime.now().isoformat(),
    "environment_vars": len(os.environ)
}

print("Python code execution successful!")
print(f"System info: {json.dumps(system_info, indent=2)}")

# Simple calculation
numbers = list(range(1, 11))
total = sum(numbers)
print(f"Sum of 1 to 10: {total}")
"""

        print("🔄 Executing Python code...")
        result = session.code.run_code(python_code, "python")
        if result.success:
            print("✅ Python code executed successfully:")
            print(result.result)
        else:
            print(f"❌ Python code execution failed: {result.error_message}")

        # ===== JAVASCRIPT CODE EXECUTION =====
        print("\n===== JAVASCRIPT CODE EXECUTION =====")

        js_code = """
console.log("JavaScript code execution successful!");

// Get system information
const os = require('os');
const systemInfo = {
    platform: os.platform(),
    arch: os.arch(),
    nodeVersion: process.version,
    memory: Math.round(os.totalmem() / 1024 / 1024) + ' MB'
};

console.log("System info:", JSON.stringify(systemInfo, null, 2));

// Array operations
const numbers = [1, 2, 3, 4, 5];
const doubled = numbers.map(n => n * 2);
console.log("Original array:", numbers);
console.log("Doubled array:", doubled);
"""

        print("🔄 Executing JavaScript code...")
        result = session.code.run_code(js_code, "javascript")
        if result.success:
            print("✅ JavaScript code executed successfully:")
            print(result.result)
        else:
            print(f"❌ JavaScript code execution failed: {result.error_message}")

        # ===== FILE OPERATIONS =====
        print("\n===== FILE OPERATIONS =====")

        print("🔄 Testing file operations...")
        test_content = "Hello from AgentBay code execution!"
        test_file_path = "/tmp/test_code.txt"

        write_result = session.file_system.write_file(test_file_path, test_content)
        if write_result.success:
            print("✅ File written successfully")

            read_result = session.file_system.read_file(test_file_path)
            if read_result.success:
                print(f"✅ File content: {read_result.content}")
            else:
                print(f"❌ File read failed: {read_result.error_message}")
        else:
            print(f"❌ File write failed: {write_result.error_message}")

        # ===== COMMAND EXECUTION =====
        print("\n===== COMMAND EXECUTION =====")

        commands = [
            "whoami",
            "pwd",
            "python3 --version",
            "node --version",
            "ls -la /tmp"
        ]

        for cmd in commands:
            print(f"\n🔄 Executing command: {cmd}")
            result = session.command.execute_command(cmd)

            if result.success:
                print(f"✅ Output: {result.output.strip()}")
            else:
                print(f"❌ Command failed: {result.error_message}")

    finally:
        # Clean up session
        print(f"\n🧹 Cleaning up session: {session.session_id}")
        delete_result = agent_bay.delete(session)
        if delete_result.success:
            print("✅ Session deleted successfully")
        else:
            print(f"❌ Failed to delete session: {delete_result.error_message}")


if __name__ == "__main__":
    main()

