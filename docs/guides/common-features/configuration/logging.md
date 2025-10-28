# Logging Configuration Guide

This guide shows how to configure logging in AgentBay SDK. Each language has its own documentation with specific details.

## Quick Links

- **[Python Logging Guide](../../../../python/docs/api/common-features/basics/logging.md)** - Setup, configuration, and file logging
- **[Go Logging Guide](../../../../golang/docs/api/common-features/basics/logging.md)** - Environment variables and code-level configuration
- **[TypeScript Logging Guide](../../../../typescript/docs/api/common-features/basics/logging.md)** - Import-time setup and RequestID tracking

---

## Overview

All AgentBay SDKs provide:
- Multiple log levels (DEBUG, INFO, WARNING/WARN, ERROR)
- **.env file support** - Automatically loaded from project directory
- Environment variable configuration (AGENTBAY_LOG_LEVEL or LOG_LEVEL)
- Code-level setup
- Automatic sensitive data masking
- Color output detection

### Quick Start: Using .env File (Recommended)

Create a `.env` file in your project root:

```
# .env file
AGENTBAY_LOG_LEVEL=DEBUG

# Other configuration
AGENTBAY_API_KEY=your_api_key_here
```

All SDKs automatically load this file - no additional code needed!

### Priority System (All Languages)

Log levels are applied in this order (highest to lowest):

1. **setup() method** - Explicitly calling setup() always takes effect (code-level configuration)
2. **Environment variables** - AGENTBAY_LOG_LEVEL or LOG_LEVEL
3. **.env file** - Automatically loaded from current directory or parent directories
4. **Default values** - INFO level if nothing else is configured

---

## Python Example

### Set Log Level via .env File (Recommended)

Create a `.env` file in your project root:

```
# .env file
AGENTBAY_LOG_LEVEL=DEBUG
```

The SDK automatically loads this file.

### Set Log Level via Environment Variable

```bash
export AGENTBAY_LOG_LEVEL=DEBUG
python your_script.py
```

### Set Log Level in Code

```python
from agentbay.logger import AgentBayLogger, get_logger

# Configure logging level with setup()
AgentBayLogger.setup(level="DEBUG")

logger = get_logger("my_app")
logger.debug("Debug message")
logger.info("Info message")
```

### Available Log Levels

| Level | Use Case |
|-------|----------|
| **DEBUG** | Development - see everything |
| **INFO** | Default - important events |
| **WARNING** | Issues but not failures |
| **ERROR** | Only failures |

### File Logging

> **Note**: File logging is currently only available in the Python SDK. TypeScript and Golang SDKs log to stdout/stderr.

The Python SDK supports file logging with automatic log rotation and retention. By default, logs are written to `python/agentbay.log`.

```python
from agentbay.logger import AgentBayLogger

# Configure file logging with rotation
AgentBayLogger.setup(
    level="DEBUG",
    log_file="/var/log/myapp.log",  # Custom log file path
    rotation="100 MB",               # Rotate when file reaches 100 MB
    retention="30 days"              # Keep logs for 30 days
)
```

---

## Sensitive Data Masking

All SDKs automatically mask sensitive information:

- API keys, tokens, passwords
- Authorization headers
- Private keys

No configuration needed - it works automatically.

