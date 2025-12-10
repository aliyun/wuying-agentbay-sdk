# Agent Modules

Agent modules are specialized AI task execution units running in AgentBay windows environment to execute tasks described in natural language.

> **💡 Async API Support**: This guide uses synchronous API. For async patterns, see:

## 🤖 Agent Module Overview

Agent modules are specialized AI task execution units
runnning in Agentbay windows/linux environment to execute tasks decribed in natural language. 
The task to be executed can be as simple as "Create a word document, input some words and save the document.", in which only one application is involved, or as complex as "Find out the current weather in New York City by Google/Baidu, and write the weather report to a word document, send the word document to a specific email address", in which multiple applications are involved.

Currently, there are two types of agents: ComputerUseAgent and BrowserUseAgent.

The ComputerUseAgent module is designed for tasks that involve multiple applications, while the BrowserUseAgent module is designed for tasks that involve specially web browsers.

The agents are capable of understanding user instructions, planning task execution steps, operating various applications, and managing files and folders on the computer.

## System Image Support

Agent Module functionality is currently only available on specific system images:

| System Image | Agent Module Support | Available APIs | Supported Agent |
|-------------|---------------------|----------------|----------|
| `windows_latest` | ✅ Supported | `execute_task`, `get_task_status`, `terminate_task` | ComputerUseAgent |
| `linux_latest` | ✅ Supported | `execute_task`, `get_task_status`, `terminate_task` | BrowserUseAgent(⚠️BETA) |
| `browser_latest` | ❌ Not Supported | - |  - |
| `code_latest` | ❌ Not Supported | - |  - |
| `mobile_latest` | ❌ Not Supported | - |  - |

**Important:** When using ComputerUseAgent Module features, you must create sessions with `image_id="windows_latest"` to ensure the required MCP tools are available. When using BrowserUseAgent Module features, you must create sessions with `image_id="linux_latest"`.

**NOTE:** ⚠️ BrowserUseAgent is still in beta. Please use with caution.

## Creating Agent Sessions

```python
from agentbay import AgentBay, CreateSessionParams

agent_bay = AgentBay()

# Create a session for Agent module usage
agent_params = CreateSessionParams(
    image_id="windows_latest",
    labels={"project": "ai-agent"}
)

result = agent_bay.create(agent_params)
if result.success:
    agent_session = result.session
    print(f"Session created with ID: {agent_session.session_id}")
else:
    print(f"Session creation failed: {result.error_message}")
```

## Agent Capabilities
- Office Automation: Word/Excel/PowerPoint automation
- File Operations:Create/Delete/Move/Copy files and folders
- Infomation Processing: 
    - Gather information from webpages
    - Extract information from a web page
    - Fill forms in a web page
- Text Edition: Using notepad to edit(Read/Write/Edit) text file

### Task Execution
#### ComputerUseAgent
```python
# Execute a task using natural language
task_description = "Calculate the square root of 144"
execution_result = agent_session.agent.computer.execute_task_and_wait(task_description, max_try_times=5)

if execution_result.success:
    print("Task completed successfully!")
    print(f"Task ID: {execution_result.task_id}")
    print(f"Task status: {execution_result.task_status}")
else:
    print(f"Task failed: {execution_result.error_message}")
```

#### BrowserUseAgent
```python
# Execute a task using natural language
task_description = "Navigate to baidu.com and query the weather in Beijing"
execution_result = agent_session.agent.browser.execute_task_and_wait(task_description, max_try_times=5)

if execution_result.success:
    print("Task completed successfully!")
    print(f"Task ID: {execution_result.task_id}")
    print(f"Task status: {execution_result.task_status}")
else:
    print(f"Task failed: {execution_result.error_message}")
```

## 📚 Related Resources

- [Session Management Guide](../basics/session-management.md)
- [Data Persistence Guide](../basics/data-persistence.md)
- [VPC Sessions Guide](vpc-sessions.md)

## 🆘 Getting Help

If you encounter issues with Agent modules:

1. Check the [Documentation](../../README.md) for detailed information
2. Search [GitHub Issues](https://github.com/aliyun/wuying-agentbay-sdk/issues) for similar problems
3. Contact support with detailed error information and reproduction steps
4. Please refer to the [Agent Task Excution Example](../../../../python/docs/examples/_async/common-features/advanced/agent_module/main.py) to see how to use the Agent.
5. Please refer to the [Agent API Definition](../../../../python/docs/api/async/async-agent.md) for more details.
