#!/bin/bash
# Quick start script for the OpenAI Data Analysis example

set -e  # Exit on error

echo "========================================="
echo "OpenAI Data Analysis with AgentBay"
echo "========================================="
echo ""

# Check for required environment variables
if [ -z "$AGENTBAY_API_KEY" ]; then
    echo "❌ Error: AGENTBAY_API_KEY environment variable is not set"
    echo "Please set it with: export AGENTBAY_API_KEY=your_api_key"
    exit 1
fi

if [ -z "$DASHSCOPE_API_KEY" ]; then
    echo "❌ Error: DASHSCOPE_API_KEY environment variable is not set"
    echo "Please set it with: export DASHSCOPE_API_KEY=your_api_key"
    exit 1
fi

echo "✓ Environment variables checked"
echo ""

# Detect Python command
PYTHON_CMD="python3"
if command -v python &> /dev/null; then
    PYTHON_CMD="python"
fi

# Check if dataset exists, if not, generate it
DATA_FILE="../common/data/ecommerce_sales.csv"
if [ ! -f "$DATA_FILE" ]; then
    echo "📊 Dataset not found, generating sample data..."
    cd ../common/src
    $PYTHON_CMD generate_ecommerce_data.py
    cd ../../openai
    echo "✓ Sample data generated"
    echo ""
fi

# Check and create virtual environment if needed
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
    echo ""
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
PYTHON_CMD="python"  # Use python command in venv
PIP_CMD="pip"
echo "✓ Virtual environment activated"
echo ""

# Check if dependencies are installed
if ! $PYTHON_CMD -c "import openai" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    $PIP_CMD install -r requirements.txt
    echo "✓ Dependencies installed"
    echo ""
fi

# Run the analysis
echo "🚀 Starting sales analysis..."
echo ""
cd src
$PYTHON_CMD agentbay_openai_sales_analysis.py

echo ""
echo "========================================="
echo "✓ Analysis complete!"
if [ -f "sales_analysis.png" ]; then
    echo "✓ Visualization saved: sales_analysis.png"
fi
echo "========================================="
