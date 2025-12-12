# AsyncAgent API Reference

> **💡 Sync Version**: This documentation covers the asynchronous API. For synchronous operations, see [`Agent`](../sync/agent.md).
>
> ⚡ **Performance Advantage**: Async API enables concurrent operations with 4-6x performance improvements for parallel tasks.

## 🤖 Related Tutorial

- [Agent Modules Guide](../../../../docs/guides/common-features/advanced/agent-modules.md) - Learn about agent modules and custom agents



## AsyncAgent

```python
class AsyncAgent(AsyncBaseService)
```

An Agent to manipulate applications to complete specific tasks.

### \_\_init\_\_

```python
def __init__(self, session)
```

## Computer

```python
class Computer()
```

An Agent to perform tasks on the computer.

### \_\_init\_\_

```python
def __init__(self, session)
```

### execute\_task

```python
async def execute_task(task: str) -> ExecutionResult
```

Execute a task in human language without waiting for completion (non-blocking).

This is a fire-and-return interface that immediately provides a task ID.
Call get_task_status to check the task status. You can control the timeout
of the task execution in your own code by setting the frequency of calling
get_task_status and the max_try_times.

**Arguments**:

    task: Task description in human language.
  

**Returns**:

    ExecutionResult: Result object containing success status, task ID,
  task status, and error message if any.
  

**Example**:

```python
session_result = await agent_bay.create()
session = session_result.session
result = await session.agent.computer.execute_task("Open Chrome browser")
print(f"Task ID: {result.task_id}, Status: {result.task_status}")
status = await session.agent.computer.get_task_status(result.task_id)
print(f"Task status: {status.task_status}")
await session.delete()
```

### execute\_task\_and\_wait

```python
async def execute_task_and_wait(task: str,
                                max_try_times: int) -> ExecutionResult
```

Execute a specific task described in human language synchronously.

This is a synchronous interface that blocks until the task is completed or
an error occurs, or timeout happens. The default polling interval is 3 seconds,
so set a proper max_try_times according to your task complexity.

**Arguments**:

    task: Task description in human language.
    max_try_times: Maximum number of retries.
  

**Returns**:

    ExecutionResult: Result object containing success status, task ID,
  task status, and error message if any.
  

**Example**:

```python
session_result = await agent_bay.create()
session = session_result.session
result = await session.agent.computer.execute_task_and_wait("Open Chrome browser", max_try_times=20)
print(f"Task result: {result.task_result}")
await session.delete()
```

### get\_task\_status

```python
async def get_task_status(task_id: str) -> QueryResult
```

Get the status of the task with the given task ID.

**Arguments**:

    task_id: The ID of the task to query.
  

**Returns**:

    QueryResult: Result object containing success status, task status,
  task action, task product, and error message if any.
  

**Example**:

```python
session_result = await agent_bay.create()
session = session_result.session
result = await session.agent.computer.execute_task("Query the weather in Shanghai with Baidu")
status = await session.agent.computer.get_task_status(result.task_id)
print(f"Status: {status.task_status}, Action: {status.task_action}")
await session.delete()
```

### terminate\_task

```python
async def terminate_task(task_id: str) -> ExecutionResult
```

Terminate a task with a specified task ID.

**Arguments**:

    task_id: The ID of the running task to terminate.
  

**Returns**:

    ExecutionResult: Result object containing success status, task ID,
  task status, and error message if any.
  

**Example**:

```python
session_result = await agent_bay.create()
session = session_result.session
result = await session.agent.computer.execute_task("Query the weather in Shanghai with Baidu")
terminate_result = await session.agent.computer.terminate_task(result.task_id)
print(f"Terminated: {terminate_result.success}")
await session.delete()
```

## Browser

```python
class Browser()
```

An Agent(⚠️ Still in BETA) to perform tasks on the browser

### \_\_init\_\_

```python
def __init__(self, session)
```

### initialize

```python
async def initialize(options: AgentOptions = None) -> InitializationResult
```

Initialize the browser agent with options.

**Arguments**:

    options: options for the agent.
  

**Returns**:

    InitializationResult: Result object containing success status, and error message if any.
  

**Example**:

```python
session_result = await agent_bay.create()
session = session_result.session
options:AgentOptions = AgentOptions(use_vision=False, output_schema="")
initialize_result = await session.agent.browser.initialize(options)
print(f"Initialized: {initialize_result.success}")
await session.delete()
```

### execute\_task

```python
async def execute_task(task: str) -> ExecutionResult
```

Execute a browser task in human language without waiting for completion (non-blocking).

This is a fire-and-return interface that immediately provides a task ID.
Call get_task_status to check the task status. You can control the timeout
of the task execution in your own code by setting the frequency of calling
get_task_status and the max_try_times.

**Arguments**:

    task: Task description in human language.
  

**Returns**:

    ExecutionResult: Result object containing success status, task ID,
  task status, and error message if any.
  

**Example**:

```python
session_result = await agent_bay.create()
session = session_result.session
result = await session.agent.browser.execute_task("Query the weather in Shanghai with Baidu")
print(f"Task ID: {result.task_id}, Status: {result.task_status}")
status = await session.agent.browser.get_task_status(result.task_id)
print(f"Task status: {status.task_status}")
await session.delete()
```

### execute\_task\_and\_wait

```python
async def execute_task_and_wait(task: str,
                                max_try_times: int) -> ExecutionResult
```

Execute a specific task described in human language synchronously.

This is a synchronous interface that blocks until the task is completed or
an error occurs, or timeout happens. The default polling interval is 3 seconds,
so set a proper max_try_times according to your task complexity.

**Arguments**:

    task: Task description in human language.
    max_try_times: Maximum number of retries.
  

**Returns**:

    ExecutionResult: Result object containing success status, task ID,
  task status, and error message if any.
  

**Example**:

```python
session_result = await agent_bay.create()
session = session_result.session
result = await session.agent.browser.execute_task_and_wait("Query the weather in Shanghai with Baidu", max_try_times=20)
print(f"Task result: {result.task_result}")
await session.delete()
```

### get\_task\_status

```python
async def get_task_status(task_id: str) -> QueryResult
```

Get the status of the task with the given task ID.

**Arguments**:

    task_id: The ID of the task to query.
  

**Returns**:

    QueryResult: Result object containing success status, task status,
  task action, task product, and error message if any.
  

**Example**:

```python
session_result = await agent_bay.create()
session = session_result.session
result = await session.agent.browser.execute_task("Open Chrome browser")
status = await session.agent.browser.get_task_status(result.task_id)
print(f"Status: {status.task_status}, Action: {status.task_action}")
await session.delete()
```

### terminate\_task

```python
async def terminate_task(task_id: str) -> ExecutionResult
```

Terminate a task with a specified task ID.

**Arguments**:

    task_id: The ID of the running task to terminate.
  

**Returns**:

    ExecutionResult: Result object containing success status, task ID,
  task status, and error message if any.
  

**Example**:

```python
session_result = await agent_bay.create()
session = session_result.session
result = await session.agent.browser.execute_task("Open Chrome browser")
terminate_result = await session.agent.browser.terminate_task(result.task_id)
print(f"Terminated: {terminate_result.success}")
await session.delete()
```

## See Also

- [Synchronous vs Asynchronous API](../../../docs/guides/async-programming/sync-vs-async.md)

**Related APIs:**
- [Session API Reference](./async-session.md)

---

*Documentation generated automatically from source code using pydoc-markdown.*
