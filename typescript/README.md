# TypeScript SDK for Wuying AgentBay

This directory contains the TypeScript implementation of the Wuying AgentBay SDK.

## Prerequisites

- Node.js (v14 or later)
- npm (v6 or later)

## Installation

### For Development

Clone the repository and install dependencies:

```bash
git clone https://github.com/aliyun/wuying-agentbay-sdk.git
cd wuying-agentbay-sdk/typescript
npm install
```

### For Usage in Your Project

```bash
npm install wuying-agentbay-sdk
```

## Development Scripts

- **Build the project**:
  ```bash
  npm run build
  ```

- **Run tests**:
  ```bash
  npm test
  ```

- **Lint the code**:
  ```bash
  npm run lint
  ```

## Examples

The SDK includes several examples demonstrating various features:

- **basic-usage.ts**: Basic SDK usage
- **context-usage.ts**: Context creation and management
- **command-example/**: Command execution examples
- **filesystem-example/**: File system operation examples
- **ui-example/**: UI interaction examples
- **application-mobile/**: Mobile application management
- **application-window/**: Window and application management
- **label-management/**: Session label management
- **session-params/**: Session parameter examples
- **session-creation/**: Session creation examples
- **context-management/**: Context management examples

## Running Examples

You can run the example files using ts-node:

```bash
npx ts-node examples/basic-usage.ts
npx ts-node examples/command-example/command-example.ts
npx ts-node examples/filesystem-example/filesystem-example.ts
```

## TypeScript-Specific Usage

```typescript
import { AgentBay, ListSessionParams } from 'wuying-agentbay-sdk';

async function main() {
  // Initialize with API key
  const agentBay = new AgentBay({ apiKey: 'your_api_key' });

  try {
    // Create a session with optional parameters
    const createResponse = await agentBay.create({
      imageId: 'linux_latest',  // Optional: specify the image to use
      contextId: 'your_context_id',  // Optional: bind to an existing context
      labels: {
        purpose: 'demo',
        environment: 'development'
      }
    });
    const session = createResponse.session;
    console.log(`Session created with ID: ${session.sessionId}`);
    console.log(`Request ID: ${createResponse.requestId}`);

    // Execute a command
    const commandResponse = await session.command.executeCommand('ls -la');
    console.log(`Command result: ${commandResponse.output}`);
    console.log(`Request ID: ${commandResponse.requestId}`);

    // Read a file
    const fileResponse = await session.fileSystem.readFile('/etc/hosts');
    console.log(`File content: ${fileResponse.content}`);
    console.log(`Request ID: ${fileResponse.requestId}`);

    // Write a file
    const writeResponse = await session.fileSystem.writeFile('/tmp/test.txt', 'Hello World');
    console.log(`Write file success: ${writeResponse.success}`);
    console.log(`Write file Request ID: ${writeResponse.requestId}`);

    // Run code
    const pythonCode = `
import os
import platform

print(f"Current working directory: {os.getcwd()}")
print(f"Python version: {platform.python_version()}")
`;
    const codeResponse = await session.command.runCode(pythonCode, 'python');
    console.log(`Code execution result: ${codeResponse.result}`);
    console.log(`Request ID: ${codeResponse.requestId}`);

    // Get installed applications
    const appsResponse = await session.application.getInstalledApps(true, false, true);
    console.log(`Found ${appsResponse.data.length} installed applications`);
    console.log(`Request ID: ${appsResponse.requestId}`);

    // List visible applications
    const processesResponse = await session.application.listVisibleApps();
    console.log(`Found ${processesResponse.data.length} visible applications`);
    console.log(`Request ID: ${processesResponse.requestId}`);

    // List root windows
    const windowsResponse = await session.window.listRootWindows();
    console.log(`Found ${windowsResponse.windows.length} root windows`);
    console.log(`Request ID: ${windowsResponse.requestId}`);

    // Get active window
    const activeWindowResponse = await session.window.getActiveWindow();
    if (activeWindowResponse.window) {
      console.log(`Active window: ${activeWindowResponse.window.title}`);
    }
    console.log(`Request ID: ${activeWindowResponse.requestId}`);

    // Take a screenshot
    const screenshotResponse = await session.ui.screenshot();
    console.log(`Screenshot data length: ${screenshotResponse.data.length} characters`);
    console.log(`Request ID: ${screenshotResponse.requestId}`);

    // Get session link
    const linkResponse = await session.getLink();
    console.log(`Session link: ${linkResponse.data}`);
    console.log(`Request ID: ${linkResponse.requestId}`);

    // Set session labels
    const setLabelsResponse = await session.setLabels({
      environment: 'production',
      version: '1.0.0'
    });
    console.log(`Set labels Request ID: ${setLabelsResponse.requestId}`);

    // Get session labels
    const labelsResponse = await session.getLabels();
    console.log(`Session labels: ${JSON.stringify(labelsResponse.labels)}`);
    console.log(`Request ID: ${labelsResponse.requestId}`);

    // Get session info
    const infoResponse = await session.info();
    console.log(`Session info: ${JSON.stringify(infoResponse.data)}`);
    console.log(`Request ID: ${infoResponse.requestId}`);

    // List sessions by labels with pagination support
    const listParams: ListSessionParams = {
      labels: {
        purpose: 'demo'
      },
      maxResults: 10,
      // nextToken: 'your_next_token'  // Optional: for pagination
    };
    const filteredSessionsResponse = await agentBay.listByLabels(listParams);
    console.log(`Found ${filteredSessionsResponse.sessions.length} matching sessions`);
    console.log(`Total count: ${filteredSessionsResponse.totalCount}`);
    console.log(`Request ID: ${filteredSessionsResponse.requestId}`);

    // Handle pagination if needed
    if (filteredSessionsResponse.nextToken) {
      const nextPageParams: ListSessionParams = {
        ...listParams,
        nextToken: filteredSessionsResponse.nextToken
      };
      const nextPageResponse = await agentBay.listByLabels(nextPageParams);
      console.log(`Next page sessions: ${nextPageResponse.sessions.length}`);
    }

    // Access context service
    const contextResponse = await agentBay.context.list();
    console.log(`Available contexts: ${contextResponse.contexts.length}`);
    console.log(`Request ID: ${contextResponse.requestId}`);

    // Clean up
    const deleteResponse = await agentBay.delete(session);
    console.log('Session deleted successfully');
    console.log(`Request ID: ${deleteResponse.requestId}`);
  } catch (error) {
    console.error('Error:', error);
  }
}

main();
```

## Key Features

### API Response Format

All API methods return responses in the following format:
```typescript
interface ApiResponse {
  requestId: string;
  success: boolean;
}

// Different response types based on the operation
interface SessionResult extends ApiResponse {
  session: Session;
}

interface CommandResult extends ApiResponse {
  output: string;
}

interface CodeExecutionResult extends ApiResponse {
  result: string;
}

interface FileContentResult extends ApiResponse {
  content: string;
}
```

### Session Management

- **Create sessions** with optional `imageId`, `contextId`, and `labels`
- **List sessions** with pagination support using `ListSessionParams`
- **Delete sessions** and clean up resources
- **Manage session labels** with `setLabels()` and `getLabels()`
- **Get session information** with `info()` method
- **Get session link** with `getLink()` method

### Available Session Modules

- `session.fileSystem` - File system operations (note: camelCase)
- `session.command` - Command execution and code running
- `session.oss` - Object Storage Service operations
- `session.application` - Application management (note: lowercase)
- `session.window` - Window management
- `session.ui` - UI interactions including screenshots

### Context Management

The SDK provides a context service accessible via `agentBay.context` for managing persistent contexts across sessions.

For more detailed documentation, please refer to the main [README](../README.md) and [SDK Documentation](../docs/README.md) in the project root.
