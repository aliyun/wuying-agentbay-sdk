#!/bin/bash

# Python code formatting script
# This script runs flake8 and black to format Python code

echo "Running Python code formatting..."

# Check if poetry is available
if command -v poetry &> /dev/null; then
    # Using poetry if available
    echo "Using poetry for dependency management"

    # Run flake8 to check for code issues
    echo "Running flake8..."
    poetry run flake8 agentbay tests examples --count --select=E9,F63,F7,F82 --show-source --statistics || { echo "flake8 found critical errors"; exit 1; }

    # Run black to format code
    echo "Running black formatter..."
    poetry run black agentbay tests examples || { echo "black formatter failed"; exit 1; }
else
    # Fallback to pip if poetry is not available
    echo "Poetry not found, using pip instead"

    # Run flake8 to check for code issues
    echo "Running flake8..."
    python -m flake8 agentbay tests examples --count --select=E9,F63,F7,F82 --show-source --statistics || { echo "flake8 found critical errors"; exit 1; }

    # Run black to format code
    echo "Running black formatter..."
    python -m black agentbay tests examples || { echo "black formatter failed"; exit 1; }
fi

echo "Python code formatting completed successfully!"