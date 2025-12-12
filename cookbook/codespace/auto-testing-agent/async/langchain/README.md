# LangChain Integration

This directory contains the LangChain-specific integration for the testing agent.

## Sample Output

When the agent successfully tests a Python project, you will see output similar to the following:

```
> Entering new AgentExecutor chain...

Invoking: `scan_project` with `/path/to/sample_project`

Project root: /path/to/sample_project

Directories:

Python files:
  calculator.py
    Classes:
      - Calculator (methods: add, subtract, multiply, divide)
    Functions: add, subtract, multiply, divide, is_even

Invoking: `generate_tests` with `Project root: /path/to/sample_project...`

Generated 1 test case files:
test_calculator.py

Invoking: `execute_tests` with `test_calculator.py`

Session created with ID: session-xxxxxxxxxxxxxxxxx
Uploaded calculator.py to AgentBay environment at calculator.py
Executing test case test_calculator.py

.......................
----------------------------------------------------------------------
Ran 23 tests in 0.001s

OK

Final result: The testing process for the Python project has been completed successfully:

1. **Project Scanning**: I scanned the project structure at the specified path and found a single Python file `calculator.py` containing:
   - A `Calculator` class with methods: `add`, `subtract`, `multiply`, `divide`
   - Standalone functions: `add`, `subtract`, `multiply`, `divide`, `is_even`

2. **Test Generation**: Based on the project structure, I generated a test file `test_calculator.py` that covers all the functions and class methods.

3. **Test Execution**: All tests passed successfully:
   - 23 tests were executed in 0.001 seconds
   - All tests passed (1/1 test files passed)
   - No failures or errors were detected

The project's calculator functionality is working correctly according to the generated test cases.
```

## Setup

### 1. Create Virtual Environment

First, create a virtual environment to isolate project dependencies:

```bash
# Create virtual environment
python -m venv auto-testing-agent-env

# Activate virtual environment
# On Windows:
auto-testing-agent-env\Scripts\activate
# On macOS/Linux:
source auto-testing-agent-env/bin/activate
```

### 2. Install Dependencies

Install the required packages:

```bash
# Upgrade pip
pip install --upgrade pip
```

You can install dependencies using the requirements file:

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Set your API keys as environment variables:

```bash
export AGENTBAY_API_KEY="YOUR_AGENTBAY_API_KEY"
export DASHSCOPE_API_KEY="YOUR_DASHSCOPE_API_KEY"
```

You can get your AgentBay API key from the AgentBay platform dashboard:
1. Visit [AgentBay Console](https://agentbay.console.aliyun.com/service-management)
2. Sign up or log in to your Alibaba Cloud account
3. Navigate to the Service Management section
4. Create a new API KEY or select an existing one
5. Copy the API Key and set it as the value of `AGENTBAY_API_KEY`

For the DashScope API key, you need to register on the Alibaba Cloud DashScope platform:
1. Visit [DashScope Platform](https://bailian.console.aliyun.com/#/home)
2. Sign up or log in to your account
3. Navigate to the API Key management section
4. Create a new API Key and copy it for use as `DASHSCOPE_API_KEY`

## Structure

- [src/](./src/): Contains the LangChain-specific implementation
- `data/`: Data directory for outputs (test results, etc.) - created automatically when running tests
- [README.md](./README.md): This documentation file

## Integration Details

The LangChain integration uses the core functionality from the [common](../common/) directory and wraps it in LangChain-specific components.

This demonstrates how to:
1. Use LangChain agents with AgentBay SDK
2. Structure the code to separate core functionality from framework-specific integration
3. Maintain clean separation of concerns between core logic and framework integration
4. Orchestrate testing tasks using LangChain's agent framework

## LangChain Orchestration

The testing agent can be orchestrated using LangChain's agent framework. This provides a more flexible way to interact with the testing functionality:

1. **Tool-based approach**: The agent exposes tools for scanning projects, generating tests, and executing them
2. **Natural language interface**: Users can interact with the agent using natural language commands
3. **Sequential workflow**: The agent can automatically determine the correct sequence of operations

### Available Tools

1. `scan_project`: Scan a project directory to identify Python files that need testing
2. `generate_tests`: Generate test cases for the loaded project using LLM
3. `execute_tests`: Execute generated test cases in AgentBay session
4. `save_results`: Save test results to a local log file

### Running the Example Script

To run the LangChain orchestration example:

```bash
cd YOUR_PREFIX_PATH/cookbook/codespace/auto-testing-agent/async/langchain/
python src/auto_testing_agent_example.py
```

This example script demonstrates:
1. Creating a LangChain testing agent
2. Scanning a project structure
3. Generating tests using LLM
4. Executing the tests in AgentBay session
5. Saving the results to a log file

```

## Troubleshooting

If you encounter issues:

1. Ensure your API key is correct and properly set in the `.env` file
2. Check that you have network connectivity to AgentBay services
3. Verify that all required packages are installed:
   ```bash
   pip list | grep -E "(wuying-agentbay-sdk|langchain)"
   ```
4. Check that you've activated your virtual environment before running the scripts
5. Make sure the project path specified in PROJECT_PATH exists and contains Python files