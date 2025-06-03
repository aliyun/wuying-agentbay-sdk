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

- **Format the code**:
  ```bash
  npm run format
  ```

## Running Examples

You can run the example file using ts-node:

```bash
npx ts-node examples/basic-usage.ts
```

## TypeScript-Specific Usage

```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

async function main() {
  // Initialize with API key
  const agentBay = new AgentBay({ apiKey: 'your_api_key' });
  
  try {
    // Create a session
    const session = await agentBay.create();
    
    // Execute a command
    const result = await session.command.execute_command('ls -la');
    console.log(result);
    
    // Read a file
    const content = await session.filesystem.read_file('/path/to/file.txt');
    console.log(content);
    
    // Clean up
    await agentBay.delete(session.sessionId);
  } catch (error) {
    console.error('Error:', error);
  }
}

main();
```

For more detailed documentation, please refer to the main [README](../README.md) and [SDK Reference](../SDK_Reference.md) in the project root.
