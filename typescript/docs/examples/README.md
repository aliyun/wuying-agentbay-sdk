# TypeScript SDK Examples

This directory contains TypeScript/JavaScript examples demonstrating various features and capabilities of the Wuying AgentBay SDK.

## Quick Start

### [basic-usage.ts](./basic-usage.ts)
Single-file quick start example:
- Initializing the AgentBay client
- Creating sessions
- Basic operations
- Session cleanup

## Core Features

### [session-creation/](./session-creation)
Session creation and configuration:
- Creating sessions with different image types
- Session parameter configuration
- Session lifecycle management

### [filesystem-example/](./filesystem-example)
File system operations:
- **filesystem-example.ts**: Basic file operations
- **filesystem-filetransfer-example.ts**: File transfer between local and cloud
- **watch-directory-example.ts**: Directory monitoring and change detection

### [command-example/](./command-example)
Command execution capabilities:
- Running shell commands in cloud environments
- Capturing command output
- Command execution patterns

### [ui-example/](./ui-example)
UI automation:
- User interface interactions
- Screen automation
- UI element manipulation

### [context-management/](./context-management)
Data persistence across sessions:
- Context creation and management
- Data storage and retrieval
- Cross-session data sharing

### [data-persistence/](./data-persistence)
Persistent data storage with advanced patterns:
- Storing data across sessions
- Data retrieval patterns
- **context-sync-demo.ts**: Context synchronization demonstration

## Browser Automation

### [browser/](./browser)
Comprehensive browser automation examples:

**Basic Browser Usage:**
- **basic-usage.ts**: Getting started with browser automation

**Cookie and Session Management:**
- **browser-context-cookie-persistence.ts**: Cookie persistence across sessions

**Browser Configuration:**
- **browser-stealth.ts**: Stealth mode to avoid detection
- **browser-viewport.ts**: Custom viewport configuration
- **browser-proxies.ts**: Proxy configuration

**Real-World Use Cases:**
- **run-2048.ts**: 2048 game automation
- **run-sudoku.ts**: Sudoku game automation
- **captcha_tongcheng.ts**: CAPTCHA handling example
- **call_for_user_jd.ts**: JD.com user interaction automation

### [extension-example/](./extension-example)
Browser extension management:
- Loading and using browser extensions
- Extension development workflows
- Automated extension testing

## Advanced Features

### [automation/](./automation)
End-to-end automation workflows:
- **automation-example.ts**: Complex automation patterns
- Workflow orchestration
- Multi-step automation tasks

### [agent-module-example/](./agent-module-example)
Agent module integration:
- Using AI-powered automation
- Agent-based task execution
- Intelligent automation workflows

### [agent-module-example.ts](./agent-module-example.ts)
Single-file agent module example demonstrating:
- Quick agent module setup
- AI-powered task execution

### [vpc-session-example/](./vpc-session-example)
VPC network configuration:
- Creating sessions in VPC environments
- Network security groups
- Private network access

### [vpc-session-example.ts](./vpc-session-example.ts)
Single-file VPC session example for quick reference.

## Running the Examples

1. Install dependencies:
```bash
cd typescript
npm install
```

2. For browser examples, install Playwright:
```bash
npx playwright install chromium
```

3. Build the SDK:
```bash
npm run build
```

4. Set your API key:
```bash
export AGENTBAY_API_KEY=your_api_key_here
```

5. Run any example:
```bash
# Using ts-node for TypeScript files
npx ts-node docs/examples/basic-usage.ts

# Or run from subdirectories
npx ts-node docs/examples/session-creation/session-creation.ts
npx ts-node docs/examples/browser/browser-stealth.ts

# Or compile and run JavaScript
tsc docs/examples/basic-usage.ts
node docs/examples/basic-usage.js
```

## File Naming Convention

This SDK follows TypeScript conventions with kebab-case naming:
- Single-file examples: `example-name.ts`
- Directory-based examples: `example-name/example-name.ts` or `example-name/README.md`

## Prerequisites

- Node.js 16 or later
- TypeScript 4.5 or later
- Valid AgentBay API key
- Playwright (for browser examples)
- Internet connection

## Best Practices

1. **Type safety**: Leverage TypeScript's type system for better code quality
2. **Async/await**: Use async/await for better error handling
3. **Proper cleanup**: Always delete sessions when done
4. **Error handling**: Implement try-catch blocks for network operations
5. **Resource management**: Close connections properly
6. **API key security**: Never commit API keys to version control

## Getting Help

For more information, see:
- [TypeScript SDK Documentation](../../)
- [API Reference](../api/)
- [Quick Start Guide](../../../docs/quickstart/)
- [Browser Automation Guide](../../../docs/guides/browser-automation.md)
