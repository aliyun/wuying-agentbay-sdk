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

You can find examples in the `docs/examples/typescript` directory, including:

- Basic SDK usage
- Context management
- Command execution
- File system operations
- UI interaction
- Application management
- Window management
- Session management

To run the examples:

```bash
npx ts-node docs/examples/typescript/basic-usage.ts
```

## TypeScript-Specific Usage

```typescript
import { AgentBay, ListSessionParams } from 'wuying-agentbay-sdk';

async function main() {
  // Initialize with API key
  const agentBay = new AgentBay({ apiKey: 'your_api_key' });

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
  
  // Execute a command
  const commandResponse = await session.command.executeCommand('ls -la');
  
  // Run code
  const codeResponse = await session.code.runCode('print("Hello World")', 'python');
  
  // File operations
  const fileContent = await session.fileSystem.readFile('/etc/hosts');
  await session.fileSystem.writeFile('/tmp/test.txt', 'Hello World');
  
  // UI operations
  const screenshot = await session.ui.screenshot();
  
  // Application management
  const installedApps = await session.application.getInstalledApps(true, false, true);
  const visibleApps = await session.application.listVisibleApps();
  
  // Window management
  const windows = await session.window.listRootWindows();
  const activeWindow = await session.window.getActiveWindow();
  
  // Session management
  await session.setLabels({ environment: 'production' });
  const labels = await session.getLabels();
  const info = await session.info();
  
  // Context management
  const contexts = await agentBay.context.list();
  
  // Clean up
  await agentBay.delete(session);
}
```

## Key Features

### Session Management

- Create sessions with optional parameters (imageId, contextId, labels)
- List sessions with pagination and filtering by labels
- Delete sessions and clean up resources
- Manage session labels
- Get session information and links

### Command Execution

- Execute shell commands
- Run code in various languages
- Get command output and execution status

### File System Operations

- Read and write files
- List directory contents
- Create and delete files and directories
- Get file information

### UI Interaction

- Take screenshots
- Find UI elements by criteria
- Click on UI elements
- Send text input
- Perform swipe gestures
- Send key events

### Application Management

- Get installed applications
- List running applications
- Start and stop applications
- Get application information

### Window Management

- List windows
- Get active window
- Focus, resize, and move windows
- Get window properties

### Context Management

- Create, list, and delete contexts
- Bind sessions to contexts
- Synchronize context data
- Get context information

### OSS Integration

- Upload files to OSS
- Download files from OSS
- Initialize OSS environment

## Response Format

All API methods return responses that include:

- `requestId`: A unique identifier for the request
- `success`: A boolean indicating whether the operation was successful
- Operation-specific data (varies by method)

For more detailed documentation, refer to the [SDK Documentation](../docs/README.md).
