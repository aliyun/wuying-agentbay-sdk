# Class: ComputerUseAgent

An Agent to perform tasks on the computer.

## Table of contents


### Methods

- [executeTask](#executetask)
- [terminateTask](#terminatetask)

## Methods

### executeTask

▸ **executeTask**(`task`, `maxTryTimes`): `Promise`\<``ExecutionResult``\>

Execute a specific task described in human language.

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `task` | `string` | Task description in human language. |
| `maxTryTimes` | `number` | Maximum number of retry attempts. |

#### Returns

`Promise`\<``ExecutionResult``\>

ExecutionResult containing success status, task output, and error
    message if any.

**`Example`**

```typescript
const agentBay = new AgentBay({ apiKey: 'your_api_key' });
const result = await agentBay.create({ imageId: 'windows_latest' });
if (result.success) {
  const taskResult = await result.session.agent.computer.executeTask(
    'Open notepad',
    10
  );
  console.log(`Task status: ${taskResult.taskStatus}`);
  await result.session.delete();
}
```

### terminateTask

▸ **terminateTask**(`taskId`): `Promise`\<``ExecutionResult``\>

Terminate a task with a specified task ID.

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `taskId` | `string` | The ID of the running task. |

#### Returns

`Promise`\<``ExecutionResult``\>

ExecutionResult containing success status, task output, and
    error message if any.

**`Example`**

```typescript
const agentBay = new AgentBay({ apiKey: 'your_api_key' });
const result = await agentBay.create({ imageId: 'windows_latest' });
if (result.success) {
  const taskResult = await result.session.agent.computer.executeTask(
    'Open notepad',
    5
  );
  const terminateResult = await result.session.agent.computer.terminateTask(
    taskResult.taskId
  );
  console.log(`Terminated: ${terminateResult.taskStatus}`);
  await result.session.delete();
}
```
