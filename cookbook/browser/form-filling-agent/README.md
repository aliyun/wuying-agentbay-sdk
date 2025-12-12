# Form-Filling Agent

This project demonstrates how to create a form-filling agent using the AgentBay SDK. The agent can automatically fill HTML forms with data based on natural language instructions.

## Features

- Uploads an HTML form to AgentBay environment
- Opens the form in a browser using AgentBay's browser capabilities
- Uses natural language instructions to fill form fields
- Submits the form automatically

## Framework Integration Guides

This project is structured to support multiple agent frameworks. Please refer to the specific framework integration guide for detailed setup and usage instructions:

- [LangChain Integration Guide (Sync)](./sync/langchain/README.md) - Complete setup and usage instructions for LangChain framework (synchronous version)
- [LangChain Integration Guide (Async)](./async/langchain/README.md) - Complete setup and usage instructions for LangChain framework (asynchronous version)

## Project Structure

This project follows a modular structure that separates core functionality from framework-specific integrations:

```
├── README.md            # Documentation
├── sync/                # Synchronous implementation
│   ├── common/          # Sync core functionality
│   │   └── src/         # Framework-agnostic code
│   └── langchain/       # Sync LangChain integration
│       ├── README.md    # Integration documentation
│       ├── requirements.txt # Dependencies
│       └── src/         # LangChain-specific code
└── async/               # Asynchronous implementation
    ├── common/          # Async core functionality
    │   └── src/         # Framework-agnostic code
    └── langchain/       # Async LangChain integration
        ├── README.md    # Integration documentation
        ├── requirements.txt # Dependencies
        └── src/         # LangChain-specific code
```

### Common Module

The `common/` directories contain core functionality that can be used across different agent frameworks, with separate implementations for synchronous and asynchronous patterns.

### Framework Integration Modules

Framework-specific directories (like `sync/langchain/` and `async/langchain/`) contain the integration code that implements form filling functionality using specific agent frameworks with different execution patterns.

## Customization

You can customize the form filling behavior by modifying the implementation in the framework-specific directories and providing your own forms and instructions.

## AgentBay SDK Features Used

- Session management
- File system operations (uploading files)
- Browser initialization and control
- BrowserAgent for natural language web automation