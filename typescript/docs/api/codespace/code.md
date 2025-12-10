# Class: Code

## 💻 Related Tutorial

- [Code Execution Guide](../../../../docs/guides/codespace/code-execution.md) - Execute code in isolated environments

## Overview

The Code module provides secure code execution capabilities in isolated environments.
It supports multiple programming languages including Python, JavaScript, and more.


## Requirements

- Requires `code_latest` image for code execution features

Handles code execution operations in the AgentBay cloud environment.

## Table of contents


### Methods

- [runCode](#runcode)

## Methods

### runCode

▸ **runCode**(`code`, `language`, `timeoutS?`): `Promise`\<`CodeExecutionResult`\>

Execute code in the specified language with a timeout.
Corresponds to Python's run_code() method

#### Parameters

| Name | Type | Default value | Description |
| :------ | :------ | :------ | :------ |
| `code` | `string` | `undefined` | The code to execute. |
| `language` | `string` | `undefined` | The programming language of the code. Must be either 'python' or 'javascript'. |
| `timeoutS` | `number` | `60` | The timeout for the code execution in seconds. Default is 60s. Note: Due to gateway limitations, each request cannot exceed 60 seconds. |

#### Returns

`Promise`\<`CodeExecutionResult`\>

CodeExecutionResult with code execution output and requestId

**`Throws`**

Error if an unsupported language is specified.

**`Example`**

```typescript
const agentBay = new AgentBay({ apiKey: 'your_api_key' });
const result = await agentBay.create({ imageId: "code_latest" });
if (result.success) {
  const codeResult = await result.session.code.runCode('print("Hello")', "python");
  console.log(codeResult.result);
  if (codeResult.results) {
     // Access rich output like images or charts
  }
  await result.session.delete();
}
```

## Best Practices

1. Validate code syntax before execution
2. Set appropriate execution timeouts
3. Handle execution errors and exceptions
4. Use proper resource limits to prevent resource exhaustion
5. Clean up temporary files after code execution


## Related Resources

- [Session API Reference](../common-features/basics/session.md)

