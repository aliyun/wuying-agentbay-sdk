# Auto Testing Agent

This project demonstrates how to create a testing agent using LangChain and AgentBay SDK. The agent can scan Python projects, generate test cases using LLMs, and execute them in isolated cloud environments.

## Features

- Scan Python projects to identify modules that need testing
- Generate test cases using LLMs based on project structure
- Execute tests in isolated AgentBay cloud environments
- Save test results to local log files
- Support for multiple agent frameworks (currently LangChain, with plans for others)

## Framework Integration Guides

This project is structured to support multiple agent frameworks. Please refer to the specific framework integration guide for detailed setup and usage instructions:

- [LangChain Integration Guide (Sync)](./sync/langchain/README.md) - Complete setup and usage instructions for LangChain framework (synchronous version)
- [LangChain Integration Guide (Async)](./async/langchain/README.md) - Complete setup and usage instructions for LangChain framework (asynchronous version)

## Project Structure

This project follows a modular structure that separates core functionality from framework-specific integrations:

```
├── README.md              # Documentation
├── sync/                  # Synchronous implementation
│   ├── common/            # Sync core functionality
│   │   ├── sample_project/ # Sample project for testing
│   │   └── src/           # Framework-agnostic code
│   └── langchain/         # Sync LangChain integration
│       ├── data/          # Output directory
│       ├── src/           # LangChain-specific code
│       └── requirements.txt # Dependencies
└── async/                 # Asynchronous implementation
    ├── common/            # Async core functionality
    │   ├── sample_project/ # Sample project for testing
    │   └── src/           # Framework-agnostic code
    └── langchain/         # Async LangChain integration
        ├── data/          # Output directory
        ├── src/           # LangChain-specific code
        └── requirements.txt # Dependencies
```

### Common Module

The `common/` directories contain all the core functionality that can be used across different agent frameworks, with separate implementations for synchronous and asynchronous patterns. This includes:

- Base testing agent class with shared functionality
- Project scanning and analysis capabilities
- Test case generation logic
- Session management with AgentBay
- Test execution and result saving functionality

### Framework Integration Modules

Framework-specific directories (like `sync/langchain/` and `async/langchain/`) contain the integration code that uses the core functionality from the common module and wraps it in framework-specific components.

## Customization

You can modify the code in the `common/sample_project/` directories to test with your own Python projects, and update the instructions in the example scripts to match your specific testing requirements.

## AgentBay SDK Features Used

- Session management
- File system operations (synchronizing project files)
- Command execution (running tests)
- Context management (isolated testing environments)