#!/bin/bash

# TypeScript code formatting script
# This script runs ESLint and Prettier to format TypeScript code

echo "Running TypeScript code formatting..."

# Run ESLint with auto-fix
echo "Running ESLint with auto-fix..."
npm run lint -- --fix || { echo "ESLint failed"; exit 1; }

# Run Prettier formatting
echo "Running Prettier formatting..."
npx prettier --write "src/**/*.ts" || { echo "Prettier failed"; exit 1; }

echo "TypeScript code formatting completed successfully!"