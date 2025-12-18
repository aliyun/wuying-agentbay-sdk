# AgentBay SDK Cookbook

The AgentBay SDK Cookbook is a collection of practical examples and use cases demonstrating how to leverage the AgentBay SDK for various automation scenarios. Each cookbook showcases a specific application of the SDK, providing both basic implementations and integrations with popular frameworks like LangChain.

## Session Environments

Examples are organized by session environments. A session environment in AgentBay refers to an isolated cloud computing environment where specific types of operations can be performed safely and efficiently. Each environment provides specialized capabilities for different use cases.

Currently, distinct session environments are implemented:

1. **browser** - A web browser session environment that provides capabilities for web automation, including form filling, web scraping, and UI interactions.
2. **codespace** - A code execution session environment that provides capabilities for running and testing code in isolated environments.
3. **mobile** - A mobile device session environment (Android) that allows automation of mobile applications.

## Table of Contents

### Browser Environment

1. [Form-Filling Agent](./browser/form-filling-agent/) - Demonstrates browser automation capabilities by automatically filling HTML forms
2. [E-commerce Inspector](./browser/e-commerce-inspector/) - Automated product information extraction from e-commerce websites with AI-powered navigation

### Codespace Environment

3. [Auto Testing Agent](./codespace/auto-testing-agent/) - Shows how to automate Python testing workflows in cloud environments
4. [OpenAI Data Analysis](./codespace/openai-data-analysis/) - Demonstrates AI-powered data analysis using OpenAI function calling with AgentBay code execution
5. [AI Code Assistant](./codespace/ai-code-assistant/) - An interactive web-based AI code assistant with real-time Python execution and visualization powered by Alibaba Cloud Bailian

### Mobile Environment

6. [App Login Persistence](./mobile/app-login-persistence/) - Demonstrates how to maintain login state for mobile applications (Xiaohongshu, Pinduoduo, Weibo, Ele.me) across sessions

## Overview

The AgentBay SDK provides a comprehensive suite of tools for efficient interaction with AgentBay cloud environments. These cookbooks demonstrate real-world applications of the SDK across different domains:

### Form-Filling Agent
This cookbook demonstrates how to create a form-filling agent using the AgentBay SDK. The agent can:
- Upload an HTML form to AgentBay environment
- Open the form in a browser using AgentBay's browser capabilities
- Use natural language instructions to fill form fields
- Submit the form automatically

### E-commerce Inspector
This cookbook demonstrates how to create an e-commerce inspector agent using the AgentBay SDK. The agent can:
- Automatically navigate to product listing pages on e-commerce websites
- Extract product information (names, prices, links) using AI-powered extraction
- Handle popups, cookie banners, and overlays automatically
- Support batch inspection of multiple websites
- Save results as JSON files with screenshots for verification
- Built-in CAPTCHA solving support

### Auto Testing Agent
This cookbook demonstrates how to create a testing agent using LangChain and AgentBay SDK. The agent can:
- Scan Python projects to identify modules that need testing
- Generate test cases using LLMs based on project structure
- Execute tests in isolated AgentBay cloud sessions
- Save test results to local log files

### OpenAI Data Analysis
This cookbook demonstrates how to integrate OpenAI with AgentBay for automated data analysis. The example shows:
- Creating AgentBay sessions with `code_latest` image for Python code execution
- Uploading datasets to cloud environments for remote analysis
- Using OpenAI function calling to generate Python analytics code
- Executing AI-generated code in isolated AgentBay sessions
- Capturing matplotlib visualizations and analysis results
- Performing comprehensive e-commerce analytics including metrics, trends, and customer segmentation

### AI Code Assistant
This cookbook demonstrates how to build an interactive web-based AI code assistant using Next.js, AgentBay SDK, and Alibaba Cloud Bailian (DashScope). The application provides:
- Real-time AI chat interface with streaming responses
- Secure Python code execution in cloud environments
- Automatic chart generation and visualization display
- Pre-installed data science packages (pandas, numpy, matplotlib, scikit-learn, seaborn)
- Session persistence for continuous development workflow
- Dark mode UI with responsive design

### App Login Persistence (Mobile)
This cookbook demonstrates how to persist mobile application login states across session lifecycles using Context Synchronization. It includes examples for:
- **Xiaohongshu (Red)**
- **Pinduoduo**
- **Weibo**
- **Ele.me**

It shows how to mount application data directories to persistent Contexts so that you don't need to re-login every time you start a new mobile agent session.

## Framework Integration

Each cookbook is structured to support multiple agent frameworks. Currently, most examples include LangChain integration, with plans to expand to other frameworks. The projects follow a modular structure that separates core functionality from framework-specific integrations:

```
cookbook-name/
├── README.md              # Documentation
├── .env                   # Environment variables
├── common/                # Public core functionality
│   └── src/               # Framework-agnostic code
└── framework-name/        # Framework integration (e.g., langchain)
    ├── data/              # Data directory for outputs
    ├── src/               # Framework-specific code
    └── requirements.txt   # Dependencies (for Python)
```

## Getting Started

To use any of these cookbooks:

1. Ensure you have the AgentBay SDK installed for your preferred language
2. Set up your environment variables, either through:
   - Exporting environment variables directly:
     ```bash
     export AGENTBAY_API_KEY=your_api_key_here
     ```
   - Or using the `.env` file in each cookbook directory (recommended)
3. Some cookbooks may require additional API keys, such as DashScope API key for LLM functionality
4. Navigate to the specific cookbook you're interested in
5. Follow the setup instructions in that cookbook's README.md
6. Run the example scripts to see the SDK in action

## Prerequisites

Before using the cookbooks, you need to:

1. Register an Alibaba Cloud account: [https://aliyun.com](https://aliyun.com)
2. Get APIKEY credentials: [AgentBay Console](https://agentbay.console.aliyun.com/service-management)
3. Install the required dependencies for each cookbook (usually Python packages)

## Contributing

If you'd like to contribute new cookbooks or improve existing ones, please follow the established structure and submit a pull request. Each cookbook should demonstrate a clear, practical use case for the AgentBay SDK.
