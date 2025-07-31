# TypeScript API Reference

This section provides detailed API reference documentation for the TypeScript/JavaScript version of the AgentBay SDK.

## Core Classes

- [AgentBay](agentbay.md) - The main entry point of the SDK, used to create sessions and manage global configuration
- [Session](session.md) - Represents a session in the AgentBay cloud environment, providing interfaces to access various features

## Functional Components

- [Agent](agent.md) - Provides AI-powered capabilities for executing tasks using natural language descriptions
- [FileSystem](filesystem.md) - Provides file system operations such as uploading, downloading, and managing files
- [Command](command.md) - Provides functionality to execute shell commands in a session
- [Code](code.md) - Handles code execution operations in Python and JavaScript languages
- [Application](application.md) - Manages application operations and state
- [Window](window.md) - Manages window and view operations
- [UI](ui.md) - Provides user interface interaction functionality
- [OSS](oss.md) - Provides Object Storage Service (OSS) integration

## Context Management

- [Context](context.md) - Manages context data in a session
- [ContextManager](context-manager.md) - Provides context management functionality

## Examples

Check out the [TypeScript Examples](../../examples/typescript/) for code samples and use cases.

## Installation

Install the TypeScript version of the AgentBay SDK via npm:

```bash
npm install wuying-agentbay-sdk
```

## Quick Start

```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

// Initialize the SDK with default configuration
const agentBay = new AgentBay({ apiKey: 'your_api_key' });

// Or with custom configuration
const agentBayCustom = new AgentBay({
  apiKey: 'your_api_key',
  config: {
    region_id: 'us-west-1',
    endpoint: 'https://agentbay.example.com',
    timeout_ms: 30000
  }
});

// Create and use a session
async function createAndUseSession() {
  try {
    const result = await agentBay.create();
    if (result.success) {
      const session = result.session;
      console.log(`Session created with ID: ${session.sessionId}`);
      
      // Use the file system
      const fs = session.fileSystem;
      
      // Execute commands
      const cmd = session.command;
      
      // Delete the session when done
      const deleteResult = await session.delete();
      if (deleteResult.success) {
        console.log('Session deleted successfully');
      }
    }
  } catch (error) {
    console.error('Error:', error);
  }
}

createAndUseSession();
``` 