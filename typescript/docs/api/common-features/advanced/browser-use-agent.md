# Class: BrowserUseAgent

## Table of contents


### Methods

- [executeTask](#executetask)
- [initialize](#initialize)
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

ExecutionResult containing success status, task output, and
    error message if any.

**`Example`**

```typescript
const agentBay = new AgentBay({ apiKey: 'your_api_key' });
const result = await agentBay.create({ imageId: 'linux_latest' });
if (result.success) {
  const taskResult = await
result.session.agent.browser.executeTask('Navigate to baidu and query the
weather of Shanghai', 10); console.log(`Task status:
${taskResult.taskStatus}`); await result.session.delete();
}
```

### initialize

▸ **initialize**(`options`): `Promise`\<``InitializationResult``\>

Initialize the browser agent with specific options.

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `options` | ``AgentOptions`` | agent initialization options |

#### Returns

`Promise`\<``InitializationResult``\>

InitializationResult containing success status, task output,
    and error message if any.

**`Example`**

```typescript
const agentBay = new AgentBay({ apiKey: 'your_api_key' });
const result = await agentBay.create({ imageId: 'linux_latest' });
if (result.success) {
  options:AgentOptions = new AgentOptions(use_vision=False,
output_schema=""); const initResult = await
result.session.agent.browser.initialize(options); console.log(`Initialize
success: ${initResult.success}`); await result.session.delete();
}
```

___

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
  const taskResult = await
result.session.agent.browser.executeTask(Navigate to baidu and query the
weather of Shanghai, 10); const terminateResult = await
result.session.agent.browser.terminateTask(taskResult.taskId);
  console.log(`Terminated: ${terminateResult.taskStatus}`);
  await result.session.delete();
}
```
