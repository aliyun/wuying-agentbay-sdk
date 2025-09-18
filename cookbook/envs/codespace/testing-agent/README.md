# Testing Agent

A testing agent that can generate test cases for projects and execute them using the AgentBay SDK. This project is designed with a modular architecture to support multiple agent frameworks.

## Features

- Scan Python projects to identify modules that need testing
- Generate test cases using LLMs based on project structure
- Execute tests in isolated AgentBay cloud sessions
- Save test results to local log files
- Support for multiple agent frameworks (currently LangChain, with plans for others)

## Framework Integration Guides

This project is structured to support multiple agent frameworks. Please refer to the specific framework integration guide for detailed setup and usage instructions:

- [LangChain Integration Guide](./langchain/README.md) - Complete setup and usage instructions for LangChain framework

## Project Structure

This project follows a modular structure that separates core functionality from framework-specific integrations:

```
├── README.md              # Documentation
├── .env                   # Environment variables
├── common/                # Public core functionality
│   ├── sample_project/    # Sample project for testing
│   └── src/               # Framework-agnostic code
│       └── base_testing_agent.py # Base testing agent class
├── langchain/             # LangChain integration
│   ├── data/              # Data directory for outputs (test results, etc.)
│   ├── src/               # LangChain-specific code
│   │   ├── testing_agent.py          # LangChain-specific implementation
│   │   └── testing_agent_example.py  # Example script for LangChain orchestration
│   └── requirements.txt   # Python dependencies
```

### Common Module

The [common](./common/) directory contains all the core functionality that can be used across different agent frameworks. This includes:

- Base testing agent class with shared functionality
- Project scanning and analysis capabilities
- Test case generation logic
- Session management with Agent-Bay
- Test execution and result saving functionality

### Framework Integration Modules

Framework-specific directories (like [langchain](./langchain/)) contain the integration code that uses the core functionality from the common module and wraps it in framework-specific components.

## How It Works

1. **Project Scanning**: The agent scans the project directory to identify all Python files that need testing.

2. **Test Generation**: It uses an LLM (via supported frameworks) to generate appropriate test cases for each module based on the project structure.

3. **Session Creation**: Creates an isolated AgentBay session with the project files synchronized.

4. **Test Execution**: Executes the generated test cases in the cloud environment.

5. **Result Saving**: Saves the test execution results to a local log file.

## Learn More

- [Agent-Bay Documentation](../../../wuying-agentbay-sdk/docs/getting-started.md)
- [Session Management Guide](../../../wuying-agentbay-sdk/docs/guides/session-management.md)
- [Code Automation Guide](../../../wuying-agentbay-sdk/docs/guides/automation.md)