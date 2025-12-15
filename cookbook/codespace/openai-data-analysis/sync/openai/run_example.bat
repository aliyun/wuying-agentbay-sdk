@echo off
REM Quick start script for the OpenAI Data Analysis example (Windows version)

echo =========================================
echo OpenAI Data Analysis with AgentBay
echo =========================================
echo.

REM Check for required environment variables
if "%AGENTBAY_API_KEY%"=="" (
    echo ❌ Error: AGENTBAY_API_KEY environment variable is not set
    echo Please set it with: set AGENTBAY_API_KEY=your_api_key
    pause
    exit /b 1
)

if "%OPENAI_API_KEY%"=="" (
    echo ❌ Error: OPENAI_API_KEY environment variable is not set
    echo Please set it with: set OPENAI_API_KEY=your_api_key
    pause
    exit /b 1
)

echo ✓ Environment variables checked
echo.

REM Check if dataset exists, if not, generate it
set DATA_FILE=..\common\data\ecommerce_sales.csv
if not exist "%DATA_FILE%" (
    echo 📊 Dataset not found, generating sample data...
    cd ..\common\src
    python generate_ecommerce_data.py
    if errorlevel 1 (
        echo ❌ Failed to generate sample data
        pause
        exit /b 1
    )
    cd ..\..\openai
    echo ✓ Sample data generated
    echo.
)

REM Check and create virtual environment if needed
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Failed to create virtual environment
        pause
        exit /b 1
    )
    echo ✓ Virtual environment created
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo ✓ Virtual environment activated
echo.

REM Check if dependencies are installed
python -c "import openai" 2>nul
if errorlevel 1 (
    echo 📦 Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Failed to install dependencies
        pause
        exit /b 1
    )
    echo ✓ Dependencies installed
    echo.
)

REM Run the analysis
echo 🚀 Starting sales analysis...
echo.
cd src
python agentbay_openai_sales_analysis.py

echo.
echo =========================================
echo ✓ Analysis complete!
if exist "sales_analysis.png" (
    echo ✓ Visualization saved: sales_analysis.png
)
echo =========================================
pause
