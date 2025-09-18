# LangChain Integration Guide

This guide provides detailed setup and usage instructions for the LangChain integration of the Form-Filling Agent.

## Prerequisites

1. Python 3.7+
2. Agent-Bay SDK
3. Playwright
4. An Agent-Bay API key

## Setup

### 1. Create Virtual Environment

First, create a virtual environment to isolate project dependencies:

```bash
# Create virtual environment
python -m venv form-filling-agent-env

# Activate virtual environment
# On Windows:
form-filling-agent-env\Scripts\activate
# On macOS/Linux:
source form-filling-agent-env/bin/activate
```

### 2. Install Dependencies

Install the required packages:

```bash
# Install core dependencies
pip install wuying-agentbay-sdk playwright python-dotenv

# Install LangChain dependencies
pip install langchain langchain-openai

# Install Playwright browsers
playwright install
```

Alternatively, you can install dependencies using the requirements file:

```bash
pip install -r langchain/requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the project root with your API keys:

```env
# AgentBay API Key (required)
AGENTBAY_API_KEY=your_actual_api_key_here

# DashScope (Alibaba Cloud) API Key for Qwen LLM (required for LangChain orchestration)
DASHSCOPE_API_KEY=your_qwen_api_key_here

# Optional: specify which Qwen model to use (default: qwen-plus)
DASHSCOPE_MODEL=qwen-plus
```

You can get your Agent-Bay API key from the Agent-Bay platform dashboard.

For the DashScope API key, you can get it from the Alibaba Cloud DashScope platform.

## Usage

### LangChain Orchestration

The agent can be orchestrated using LangChain's agent framework, which provides:

1. **Tool-based approach**: The agent exposes tools for analyzing forms, setting filling instructions, and executing the filling process
2. **Natural language interface**: Users can interact with the agent using natural language commands
3. **Sequential workflow**: The agent can automatically determine the correct sequence of operations

#### Running the Example Script

To run the LangChain orchestration example:

```bash
python langchain/src/form_filling_agent_example.py
```

This example script demonstrates:
1. Creating a LangChain form filling agent
2. Analyzing a form and suggesting filling instructions
3. Filling the form with custom data
4. Executing the form filling process

Available tools:
1. `analyze_form`: Analyze a form and suggest filling instructions
2. `fill_form_fields`: Prepare to fill form fields with provided instructions
3. `execute_form_filling`: Execute the form filling process
# Form-Filling Agent

This project demonstrates how to create a form-filling agent using LangChain and Agent-Bay SDK. The agent can upload an HTML form to Agent-Bay, open it in a browser, and automatically fill it with data.

## Features

- Uploads an HTML form to Agent-Bay environment
- Opens the form in a browser using Agent-Bay's browser capabilities
- Uses natural language instructions to fill form fields
- Submits the form automatically

## Framework Integration Guides

This project is structured to support multiple agent frameworks. Please refer to the specific framework integration guide for detailed setup and usage instructions:

- [LangChain Integration Guide](./langchain/README.md) - Complete setup and usage instructions for LangChain framework

## Project Structure

This project follows a modular structure that separates core functionality from framework-specific integrations:

```
├── README.md            # Documentation
├── .env                 # Environment variables
├── common/              # Public core functionality
│   ├── src/             # Framework-agnostic code
│   │   ├── form.html    # Sample HTML form
│   │   └── form_filler.py # Core form filling functionality
│   └── README.md        # Documentation
├── langchain/           # LangChain integration
│   ├── data/            # Data directory for outputs (screenshots, etc.)
│   ├── src/             # LangChain-specific code
│   │   ├── form_filling_agent.py       # LangChain-specific implementation
│   │   └── form_filling_agent_example.py # Example script for LangChain orchestration
│   └── requirements.txt # Python dependencies
```

### Common Module

The [common](./common/) directory contains all the core functionality that can be used across different agent frameworks. This includes:

- Session management with Agent-Bay
- File upload operations
- Browser initialization and control
- Form filling operations
- Resource cleanup

### Framework Integration Modules

Framework-specific directories (like [langchain](./langchain/)) contain the integration code that uses the core functionality from the common module and wraps it in framework-specific components.

## Customization

You can modify the [form.html](./common/src/form.html) file to use your own form, and update the instructions in the example script to match the fields in your form.

## Agent-Bay SDK Features Used

- Session management
- File system operations (uploading files)
- Browser initialization and control
- BrowserAgent for natural language web automation

## Learn More

- [Agent-Bay Documentation](../../../wuying-agentbay-sdk/docs/getting-started.md)
- [Browser Extensions Guide](../../../wuying-agentbay-sdk/docs/guides/browser-extensions.md)