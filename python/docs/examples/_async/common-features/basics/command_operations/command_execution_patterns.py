"""Command Execution Patterns Example

This example demonstrates command execution patterns:
- Setting working directory with cwd parameter
- Setting environment variables with envs parameter
- Accessing command results: exit_code, stdout, stderr, trace_id
- Note: Maximum timeout is 50s (50000ms). If a larger value is provided, it will be automatically limited.
"""

import asyncio
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))

from agentbay import AsyncAgentBay
from agentbay import CreateSessionParams


async def main():
    print("=== Command Execution Patterns ===\n")
    client = AsyncAgentBay()
    session = None

    try:
        session_result = await client.create(CreateSessionParams(image_id="linux_latest"))
        session = session_result.session
        print(f"Session: {session.session_id}\n")

        # Simple command with new return format
        result = await session.command.execute_command("echo 'Hello'")
        print(f"1. Simple command:")
        print(f"   Output: {result.output}")
        print(f"   Exit Code: {result.exit_code}")
        print(f"   Stdout: {result.stdout}")
        print()

        # Piped commands (still supported)
        result = await session.command.execute_command("echo 'test' | wc -c")
        print(f"2. Piped commands:")
        print(f"   Output: {result.output.strip()}")
        print()

        # Working directory with cwd parameter
        result = await session.command.execute_command("pwd", cwd="/tmp")
        print(f"3. Working directory (using cwd parameter):")
        print(f"   Command: pwd (cwd=/tmp)")
        print(f"   Current directory: {result.stdout.strip()}")
        print()

        # Environment variables with envs parameter
        result = await session.command.execute_command(
            "echo $TEST_VAR",
            envs={"TEST_VAR": "test_value"}
        )
        print(f"4. Environment variables (using envs parameter):")
        print(f"   Command: echo $TEST_VAR")
        print(f"   Environment: {{'TEST_VAR': 'test_value'}}")
        print(f"   Output: {result.stdout.strip()}")
        print()

        # Error handling with exit_code, stderr, and trace_id
        result = await session.command.execute_command("ls /non_existent_12345")
        print(f"5. Error handling:")
        print(f"   Command: ls /non_existent_12345")
        print(f"   Success: {result.success}")
        print(f"   Exit Code: {result.exit_code}")
        print(f"   Stderr: {result.stderr.strip() if result.stderr else 'N/A'}")
        if result.trace_id:
            print(f"   Trace ID: {result.trace_id}  # For error tracking")
        print()

        print("=== Completed ===")

    finally:
        if session:
            await client.delete(session)


if __name__ == "__main__":
    asyncio.run(main())

