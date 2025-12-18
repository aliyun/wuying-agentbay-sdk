# DashScope/OpenAI-Compatible Data Analysis with AgentBay

This project demonstrates how to integrate AgentBay with Alibaba Cloud DashScope (Bailian) via the OpenAI-compatible API to perform automated data analysis using the `code_latest` system image. The example showcases e-commerce sales analytics with AI-generated Python code executed in secure cloud environments.

## Features

- Create and manage AgentBay sessions with `code_latest` image
- Upload datasets to AgentBay cloud environments
- Use DashScope (OpenAI-compatible) function calling to generate and execute Python code remotely
- Capture matplotlib visualizations from cloud execution using native rich output support
- Perform comprehensive data analysis including metrics, trends, and visualizations
- Handle stdout, stderr, and error reporting from remote execution

## Framework Integration Guides

Please refer to the detailed integration guide:

- [DashScope (OpenAI-compatible) Integration Guide](./openai/README.md) - Complete setup and usage instructions for function calling

## Project Structure

This project follows a modular structure:

```
├── README.md              # This documentation
├── .env.example           # Environment variable template
├── common/                # Shared resources
│   ├── data/              # Sample datasets
│   └── src/               # Data generation scripts
└── openai/                # OpenAI integration
    ├── README.md          # Integration documentation
    ├── requirements.txt   # Dependencies
    └── src/               # OpenAI-specific code
```

### Common Module

The `common/` directory contains shared resources:

- **Sample dataset**: Synthetic e-commerce sales data with 5000+ orders
- **Data generator**: Script to create custom datasets with configurable parameters

### OpenAI Module

The `openai/` directory contains the integration code that demonstrates how to use AgentBay with DashScope/OpenAI.

## Use Case

This example demonstrates automated e-commerce sales analytics including:

- **Sales Performance Metrics**: Calculate total revenue, order count, and average order value
- **Category Analysis**: Identify best-selling product categories and revenue distribution
- **Time-based Trends**: Analyze monthly revenue patterns and detect seasonality
- **Customer Segmentation**: Break down sales by customer tier (Premium, Regular, New)
- **Geographic Analysis**: Compare performance across regions and cities
- **Visualization**: Generate professional charts and graphs using matplotlib

## Dataset Description

The synthetic e-commerce dataset includes:

- **5000+ sample orders** spanning 2023-2024
- **6 product categories**: Electronics, Clothing, Home & Garden, Books, Sports, Toys
- **3 customer segments**: Premium (15%), Regular (60%), New (25%)
- **4 geographic regions**: North America, Europe, Asia Pacific, Latin America
- **15 data columns**: Date, OrderID, ProductID, ProductName, Category, Brand, UnitPrice, Quantity, TotalAmount, CustomerID, CustomerSegment, Region, City, PaymentMethod, ShippingMethod

## Customization

You can modify the data generation script to create custom datasets:

- Adjust the number of records in `generate_ecommerce_data.py`
- Add or modify product categories and pricing ranges
- Change customer segment distributions
- Customize geographic regions and cities

You can also modify the analysis prompt in the main script to perform different types of analysis on the dataset.

## AgentBay SDK Features Used

This example demonstrates the following AgentBay SDK capabilities:

- **Session Management**: Create and manage sessions with `code_latest` image using `agentbay.create(CreateSessionParams(image_id="code_latest"))`
- **File Upload**: Upload datasets to cloud environments using `session.file_system.upload_file()`
- **Code Execution**: Run Python code remotely using `session.code.run_code()` API
- **Rich Outputs**: Capture images/charts directly from code execution results
- **Resource Management**: Automatic session cleanup with `session.delete()`

## Learn More

- [AgentBay SDK Documentation](https://help.aliyun.com/zh/agentbay/)
- [OpenAI Function Calling Guide](https://platform.openai.com/docs/guides/function-calling)
- [AgentBay Console](https://agentbay.console.aliyun.com/)
