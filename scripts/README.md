# Code Formatting Scripts

This directory contains scripts for formatting code in the Wuying AgentBay SDK project.

## Usage

### TypeScript Formatting

To format TypeScript code:

```bash
cd typescript
chmod +x scripts/format.sh
./scripts/format.sh
```

This script will:
1. Run ESLint with auto-fix to fix linting issues
2. Run Prettier to format all TypeScript files in the `src` directory

### Python Formatting

To format Python code:

```bash
cd python
chmod +x scripts/format.sh
./scripts/format.sh
```

This script will:
1. Run flake8 to check for critical code issues
2. Run black to format Python files in the `agentbay`, `tests`, and `examples` directories

### Golang Formatting

To format Golang code:

```bash
cd golang
chmod +x scripts/format.sh
./scripts/format.sh
```

This script will:
1. Run gofmt to format all Go files
2. Run golint to check for style issues
3. Run go vet to analyze code for potential problems

## CI Integration

These scripts are designed to be run locally before committing changes. They are not part of the CI workflows to avoid automatic changes to PR contents. Developers should run these scripts locally to ensure their code meets the project's formatting standards.

## Requirements

- For TypeScript formatting: Node.js and npm with required dependencies installed
- For Python formatting: Python with flake8 and black installed, or Poetry
- For Golang formatting: Go installed with golint (will be auto-installed if missing)