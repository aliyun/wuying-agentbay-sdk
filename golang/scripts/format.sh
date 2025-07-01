#!/bin/bash

# Golang code formatting script
# This script runs gofmt and golint to format and check Golang code

echo "Running Golang code formatting..."

# Check if go is installed
if ! command -v go &> /dev/null; then
    echo "Error: go is not installed"
    exit 1
fi

# Run gofmt to format code
echo "Running gofmt..."
find . -name "*.go" -not -path "./vendor/*" | xargs gofmt -w -s || { echo "gofmt failed"; exit 1; }

# Check if golint is installed
if ! command -v golint &> /dev/null; then
    echo "Installing golint..."
    go install golang.org/x/lint/golint@latest
fi

# Run golint to check for style issues
echo "Running golint..."
golint ./... || { echo "Note: golint found style issues, but continuing..."; }

# Run go vet for deeper code analysis
echo "Running go vet..."
go vet ./... || { echo "go vet found issues"; exit 1; }

echo "Golang code formatting completed successfully!"