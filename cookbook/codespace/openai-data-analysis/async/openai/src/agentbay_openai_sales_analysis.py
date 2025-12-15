#!/usr/bin/env python3
"""
AgentBay + Alibaba Cloud Bailian Integration: E-commerce Sales Analysis (Async)

This example demonstrates how to integrate AgentBay with Alibaba Cloud Bailian (DashScope)
to perform automated data analysis on e-commerce sales data asynchronously.

Features:
1. Creating an AgentBay CodeSpace environment
2. Uploading a sales dataset to the session
3. Using Bailian's function calling to generate Python code for data analysis
4. Executing the code in the AgentBay CodeSpace
5. Retrieving and saving visualization results
"""

import os
import json
import asyncio
import traceback
from openai import AsyncOpenAI
from agentbay import AsyncAgentBay, CreateSessionParams


# Configuration
# Alibaba Cloud DashScope (Bailian) models
# Available models: qwen3-max, qwen-turbo, qwen-plus, etc.
MODEL_NAME = os.environ.get("DASHSCOPE_MODEL", "qwen3-max")

SYSTEM_PROMPT = """
## Role & Context
You are a data analyst specializing in e-commerce analytics. Your task is to analyze sales data and generate insights using Python code.

## Dataset Information
The sales dataset is located at `/tmp/user/ecommerce_sales.csv` with the following structure:
- Delimiter: `,` (comma)
- Columns:
  * Date: Order date in YYYY-MM-DD format
  * OrderID: Unique order identifier
  * ProductID, ProductName: Product identifiers
  * Category: Product category (Electronics, Clothing, Home & Garden, Books, Sports, Toys)
  * Brand: Brand name
  * UnitPrice: Price per unit in USD
  * Quantity: Number of units purchased
  * TotalAmount: Total order value (UnitPrice × Quantity)
  * CustomerID: Unique customer identifier
  * CustomerSegment: Customer tier (Premium, Regular, New)
  * Region: Geographic region (North America, Europe, Asia Pacific, Latin America)
  * City: City name
  * PaymentMethod: Payment type (Credit Card, PayPal, Bank Transfer, Digital Wallet)
  * ShippingMethod: Delivery method (Standard, Express, Next Day)

## Execution Environment
- Code runs in a secure AgentBay CodeSpace environment
- Pre-installed packages: pandas, numpy, matplotlib, seaborn, scikit-learn
- Each execute_python call runs in an isolated execution context
- Use matplotlib for visualizations (they will be captured automatically)
- You have full filesystem access and can install additional packages via pip if needed

## Guidelines
- Write clean, well-commented code
- Handle missing or invalid data appropriately
- Use appropriate visualization techniques for different data types
- Provide insights along with visualizations
- Create matplotlib figures as needed (they will be automatically saved)
"""

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "execute_python",
            "description": "Execute python code in the AgentBay session and returns any result, stdout, stderr, and error.",
            "parameters": {
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "The python code to execute."
                    }
                },
                "required": ["code"]
            }
        }
    }
]


async def execute_python_code(session, code: str) -> dict:
    """
    Execute Python code in the AgentBay session using run_code API asynchronously.

    Returns a dict with:
    - result: execution result text
    - error: error message if any
    - png_path: local path to downloaded PNG file if visualization was generated
    """
    print("🔧 Executing Python code in AgentBay session...")

    # Modify code to save matplotlib plots to a file
    code_with_save = code + '''

# Save matplotlib figure if it exists
import matplotlib.pyplot as plt
if plt.get_fignums():
    plt.savefig('/tmp/output.png', format='png', bbox_inches='tight', dpi=150)
    print("PLOT_SAVED: /tmp/output.png")
    plt.close('all')
'''

    # Execute code using session.code.run_code API
    result = await session.code.run_code(code_with_save, "python", timeout_s=60)

    parsed_result = {
        'result': '',
        'error': None,
        'png_path': None
    }

    if not result.success:
        parsed_result['error'] = result.error_message
        print(f"[Code Execution ERROR] {result.error_message}")
        return parsed_result

    # Store the execution result
    parsed_result['result'] = result.result
    print(f"[Code Execution Result]\n{result.result}")

    # Check if a plot was saved
    if "PLOT_SAVED:" in result.result:
        print("📊 Visualization detected, downloading...")
        # Download the plot file
        local_path = 'sales_analysis.png'
        download_result = await session.file_system.download_file(
            '/tmp/output.png',
            local_path
        )

        if download_result.success:
            parsed_result['png_path'] = local_path
            print(f"✓ Visualization downloaded to {local_path}")
        else:
            print(f"⚠️  Failed to download visualization: {download_result.error}")

    return parsed_result


async def process_tool_call(session, tool_call) -> dict:
    """Process a tool call from Bailian LLM asynchronously."""
    if tool_call.function.name == 'execute_python':
        tool_input = json.loads(tool_call.function.arguments)
        return await execute_python_code(session, tool_input['code'])
    return {}


async def chat_with_llm(llm_client, session, user_message: str) -> dict:
    """Send a message to Bailian LLM and execute any tool calls asynchronously."""
    print('\n' + '=' * 80)
    print(f'User Request: {user_message}')
    print('=' * 80)

    print('Waiting for the LLM to respond...')
    completion = await llm_client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
        tools=TOOLS,
        tool_choice="auto"
    )

    message = completion.choices[0].message
    print('\nLLM Response:', message.content or "(tool call)")

    if message.tool_calls:
        tool_call = message.tool_calls[0]
        print(f'\nTool Used: {tool_call.function.name}')
        print(f'Code to Execute:\n{"-" * 80}')

        # Pretty print the code
        tool_input = json.loads(tool_call.function.arguments)
        code = tool_input.get('code', '')
        for line in code.split('\n')[:20]:  # Show first 20 lines
            print(line)
        if len(code.split('\n')) > 20:
            newline = '\n'
            print(f"... ({len(code.split(newline)) - 20} more lines)")
        print('-' * 80)

        code_result = await process_tool_call(session, tool_call)
        return code_result

    raise Exception('Tool calls not found in message content.')


async def upload_dataset(session, local_path: str, remote_path: str = '/tmp/user/ecommerce_sales.csv'):
    """Upload a dataset file to the AgentBay session asynchronously."""
    print(f'📤 Uploading dataset to AgentBay session...')

    if not os.path.exists(local_path):
        raise FileNotFoundError(f'Dataset file not found: {local_path}')

    # Upload file using session file_system.upload_file
    result = await session.file_system.upload_file(local_path, remote_path)

    if result.success:
        print(f'✓ Uploaded to {remote_path}')
        return remote_path
    else:
        raise Exception(f'Failed to upload dataset: {result.error}')


async def validate_dataset(session, remote_path: str):
    """Validate the uploaded dataset structure asynchronously."""
    print(f'🔍 Validating dataset...')

    validation_code = f"""
import pandas as pd

df = pd.read_csv('{remote_path}')
print(f"Total rows: {{len(df)}}")
print(f"Total columns: {{len(df.columns)}}")
print(f"Date range: {{df['Date'].min()}} to {{df['Date'].max()}}")
print(f"Total revenue: ${{df['TotalAmount'].sum():,.2f}}")
print(f"Categories: {{', '.join(df['Category'].unique())}}")
"""

    result = await execute_python_code(session, validation_code)
    if result.get('result'):
        print(f"✓ Dataset validation results:")
        for line in result['result'].split('\n'):
            if line.strip() and not line.startswith('PLOT_SAVED'):
                print(f"  {line}")


async def main():
    """Main function to run the demo."""
    print("=" * 80)
    print("AgentBay + Alibaba Cloud Bailian Integration: E-commerce Sales Analysis (Async)")
    print("=" * 80)
    print()

    # Initialize Bailian LLM client using OpenAI-compatible API
    llm_client = AsyncOpenAI(
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        api_key=os.environ.get("DASHSCOPE_API_KEY"),
    )

    # Initialize AgentBay client
    print("🚀 Initializing AgentBay client...")
    agentbay = AsyncAgentBay(api_key=os.environ.get("AGENTBAY_API_KEY"))

    # Create a CodeSpace session
    print("📦 Creating AgentBay CodeSpace environment...")
    params = CreateSessionParams(image_id="linux_latest")
    result = await agentbay.create(params)

    if not result.success:
        print(f"❌ Failed to create session: {result.error_message}")
        return

    session = result.session
    print(f"✓ Session created: {session.session_id}")

    try:
        # Upload the dataset
        # Try multiple possible paths for the dataset (including absolute paths)

        current_dir = os.path.dirname(os.path.abspath(__file__))  # Get current script directory
        repo_root = os.path.join(current_dir, '..', '..', '..', '..', '..')  # Navigate to repo root
        repo_root = os.path.abspath(repo_root)  # Convert to absolute path
        
        possible_paths = [
            '../../common/data/ecommerce_sales.csv',  # Relative path from sync/openai/src/ to sync/common/data/
            os.path.join(repo_root, 'cookbook', 'codespace', 'openai-data-analysis', 'sync', 'common', 'data', 'ecommerce_sales.csv'),  # Absolute path
            os.path.join(current_dir, '..', '..', 'common', 'data', 'ecommerce_sales.csv'),  # Absolute path from current script
            './ecommerce_sales.csv',  # If run from data directory
        ]

        dataset_path = None
        for path in possible_paths:
            if os.path.exists(path):
                dataset_path = path
                break
        
        if dataset_path:
            print(f"✓ Found dataset at: {dataset_path}")
        else:
            print("⚠️  Dataset file not found in any expected locations")
        if dataset_path:
            remote_path = await upload_dataset(session, dataset_path)
            await validate_dataset(session, remote_path)
        else:
            print(f'⚠️  Dataset file not found in any of these locations:')
            for path in possible_paths:
                print(f'     - {path}')
            print('⚠️  Please run generate_ecommerce_data.py first or check file paths')
            return

        # Execute analysis with Bailian + AgentBay
        print("\n🤖 Starting AI-powered sales analysis...")

        analysis_request = (
            'Analyze the e-commerce sales dataset and provide a comprehensive overview. '
            'Your analysis should include: '
            '1) Calculate total revenue, total orders, and average order value, '
            '2) Find the top 5 best-selling product categories with their revenue, '
            '3) Create a horizontal bar chart showing the top 5 categories by revenue with values labeled, '
            '4) Use a professional color scheme and add a title. '
            'Write ALL code in ONE execute_python call.'
        )

        code_result = await chat_with_llm(llm_client, session, analysis_request)

        # Process results
        print('\n' + '=' * 80)
        print('Analysis Results:')
        print('=' * 80)

        if code_result.get('png_path'):
            print(f'✓ Visualization saved to {code_result["png_path"]}')
        else:
            print('⚠️  No visualization was generated')

        if code_result.get('result'):
            print('\nAnalysis Output:')
            # Filter out PLOT_SAVED line from output
            for line in code_result['result'].split('\n'):
                if not line.startswith('PLOT_SAVED:'):
                    print(line)

        if code_result.get('error'):
            print('⚠️  Error occurred:', code_result['error'])

    except Exception as e:
        print(f'❌ An error occurred: {e}')
        traceback.print_exc()
    finally:
        # Clean up
        print('\n🧹 Cleaning up...')
        await session.delete()
        print('✓ Session deleted')
        print('\n✓ Demo completed successfully!')


if __name__ == "__main__":
    asyncio.run(main())
