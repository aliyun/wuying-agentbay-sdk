# E-commerce Inspector Agent - LangChain Integration (Sync)

This directory contains the LangChain-specific integration for the e-commerce inspector agent.

## Sample Output

When the agent successfully inspects an e-commerce website, you will see output similar to the following:

```
Initializing LLM...
Initializing AgentBay session...
[DATE] [TIME] | AgentBay | INFO | [PID]:[TID] | agentbay.agentbay:create:625 | ✅ API Response: CreateSession, RequestId=[REQUEST_ID]
Session created with ID: [SESSION_ID]
Browser initialized successfully

================================================================================
E-commerce Inspector Agent Ready!
================================================================================

--- Example 1: Inspect a single e-commerce website ---

> Entering new AgentExecutor chain...

Invoking: `inspect_website` with `{'url': 'https://waydoo.com/collections/all'}`

Acting: Navigate to the product listing page...
Extraction attempt 1/3 for https://waydoo.com/collections/all...
Extraction successful on attempt 1. Found 12 valid products.
Screenshot for https://waydoo.com/collections/all saved to: ./data/screenshot_waydoo.com.png
waydoo.com -> 12 items (with price: 12) saved: ./data/inspection_waydoo.com.json
Successfully inspected waydoo.com. Found 12 products. Results saved to: ./data/inspection_waydoo.com.json

Result:
Successfully inspected waydoo.com/collections/all and extracted product information. Found 12 products with prices and links. The results have been saved to ./data/inspection_waydoo.com.json and a screenshot has been captured for verification.

================================================================================
Inspection completed! Check the ./data directory for results.
================================================================================
```

## Setup

### 1. Create Virtual Environment

First, create a virtual environment to isolate project dependencies:

```bash
# Create virtual environment
python -m venv e-commerce-inspector-env

# Activate virtual environment
# On Windows:
e-commerce-inspector-env\Scripts\activate
# On macOS/Linux:
source e-commerce-inspector-env/bin/activate
```

### 2. Install Dependencies

Install the required packages:

```bash
# Update pip
pip install --upgrade pip

# Install dependencies
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
4. Copy the API Key and set it as the value of `DASHSCOPE_API_KEY`

## Structure

- [src/](./src/): Contains the LangChain-specific implementation
  - `inspector_tools.py`: Core inspection tools and utilities
  - `e_commerce_inspector.py`: Main inspector agent implementation
  - `e_commerce_inspector_example.py`: Example usage script
- `data/`: Output directory for inspection results (created automatically)
- [README.md](./README.md): This documentation file
- [requirements.txt](./requirements.txt): Python dependencies

## Integration Details

The LangChain integration uses the core functionality and wraps it in LangChain-specific components.

This demonstrates how to:
1. Use LangChain agents with AgentBay SDK
2. Create custom tools for e-commerce inspection
3. Structure the code to separate core functionality from framework-specific integration
4. Maintain clean separation of concerns between core logic and framework integration
5. Orchestrate inspection tasks using LangChain's agent framework

## LangChain Orchestration

The e-commerce inspector agent is orchestrated using LangChain's agent framework. This provides a flexible way to interact with the inspection functionality:

1. **Tool-based approach**: The agent exposes tools for inspecting websites
2. **Natural language interface**: Users can interact with the agent using natural language commands
3. **Automatic workflow**: The agent automatically determines the correct sequence of operations

### Available Tools

1. `inspect_website`: Inspect a single e-commerce website and extract product information
   - Input: URL of the website to inspect
   - Output: Summary of products found and file paths

2. `inspect_multiple_websites`: Inspect multiple e-commerce websites at once
   - Input: Comma-separated list of URLs
   - Output: Summary of all inspection results

### Running the Example Script

To run the LangChain orchestration example:

```bash
cd YOUR_PREFIX_PATH/cookbook/browser/e-commerce-inspector/sync/langchain/
python src/e_commerce_inspector_example.py
```

This example script demonstrates:
1. Creating a LangChain e-commerce inspector agent
2. Inspecting a single e-commerce website
3. Extracting product names, prices, and links
4. Saving results to JSON files with screenshots

## Customization

You can customize the inspector behavior by:

### 1. Modify Extraction Instructions

Edit the instruction text in `inspector_tools.py`:

```python
instruction=(
    "Please extract all products on this page. "
    "Price can be a range (e.g., $199–$299) or 'from $199'. "
    # Add your custom instructions here
)
```

### 2. Adjust Validation Rules

Modify the `is_valid_product` function in `inspector_tools.py`:

```python
def is_valid_product(p: ProductInfo) -> bool:
    """Check if a product has valid information."""
    # Add your custom validation logic here
    has_name = bool(p.name and p.name.strip())
    has_valid_link = bool(p.link and p.link.strip())
    has_price = bool(p.price and p.price.strip())
    return has_name and (has_valid_link or has_price)
```

### 3. Change Output Directory

Specify a different output directory when creating the inspector:

```python
inspector = ECommerceInspector(
    llm=llm,
    agentbay_api_key=agentbay_api_key,
    output_dir="/path/to/your/output/directory"
)
```

### 4. Use Different LLM Models

You can use different LLM models by changing the model parameter:

```python
from langchain_community.chat_models import ChatTongyi

llm = ChatTongyi(
    model="qwen-max",  # or "qwen-turbo", "qwen-plus"
    dashscope_api_key=dashscope_api_key,
    temperature=0
)
```

## Advanced Usage

### Inspect Multiple Websites

You can inspect multiple websites in a single run:

```python
task = "Please inspect these websites: https://site1.com, https://site2.com, https://site3.com"
result = inspector.run(task)
```

### Use as Context Manager

The inspector supports context manager for automatic cleanup:

```python
with ECommerceInspector(llm, agentbay_api_key, output_dir) as inspector:
    result = inspector.run("Inspect https://example.com")
    # Session is automatically cleaned up when exiting the context
```

### Manual Session Management

If you need more control over the session lifecycle:

```python
inspector.initialize()

result = inspector.run("Inspect https://example.com")

inspector.cleanup()
```

## Output Files

The inspector generates two types of files for each inspected website:

### 1. JSON File (inspection_[domain].json)

Contains the extracted product information:

```json
[
  {
    "name": "Product Name",
    "price": "$199.99",
    "link": "https://example.com/products/item1"
  },
  {
    "name": "Another Product",
    "price": "from $299.99",
    "link": "https://example.com/products/item2"
  }
]
```

### 2. Screenshot (screenshot_[domain].png)

A full-page screenshot of the product listing page for visual verification.

## Troubleshooting

If you encounter issues:

1. **API Key Issues**: Ensure your API keys are correct and properly set as environment variables
   ```bash
   echo $AGENTBAY_API_KEY
   echo $DASHSCOPE_API_KEY
   ```

2. **Network Connectivity**: Check that you have network connectivity to AgentBay services
   ```bash
   ping agentbay.console.aliyun.com
   ```

3. **Package Installation**: Verify that all required packages are installed
   ```bash
   pip list | grep -E "(wuying-agentbay-sdk|langchain|playwright)"
   ```

4. **Virtual Environment**: Check that you've activated your virtual environment before running the scripts
   ```bash
   which python  # Should point to your virtual environment
   ```

5. **Playwright Installation**: If you encounter browser-related issues, install Playwright browsers
   ```bash
   playwright install chromium
   ```

6. **Session Cleanup**: If sessions are not being cleaned up properly, you can manually delete them from the [AgentBay Console](https://agentbay.console.aliyun.com/session-management)

## Performance Tips

1. **Batch Processing**: Use `inspect_multiple_websites` for better efficiency when inspecting multiple sites
2. **Screen Size**: Adjust browser screen size in `BrowserScreen` for faster rendering
3. **Extraction Attempts**: Modify `max_steps` parameter in `ensure_listing_page` to control retry behavior
4. **CAPTCHA Handling**: Enable `solve_captchas=True` for sites with CAPTCHA protection

## Known Limitations

1. **Dynamic Content**: Some websites with heavy JavaScript may require additional wait time
2. **Anti-Bot Protection**: Some sites may have advanced anti-bot protection that requires additional configuration
3. **Rate Limiting**: Inspecting too many sites in quick succession may trigger rate limits
4. **Regional Restrictions**: Some sites may have geographical restrictions

## Next Steps

- Add support for more complex product extraction scenarios
- Implement price change tracking over time
- Add support for pagination to extract more products
- Integrate with databases for persistent storage
- Add email notifications for price changes

