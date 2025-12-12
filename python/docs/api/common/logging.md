# Logging API Reference

Unified logging configuration for AgentBay SDK using loguru.

This module provides a centralized logging configuration with beautiful formatting
and structured output for different log levels.

## AgentBayLogger

```python
class AgentBayLogger()
```

AgentBay SDK Logger with beautiful formatting.

### setup

```python
@classmethod
def setup(cls,
          level: str = "INFO",
          log_file: Optional[Union[str, Path]] = None,
          enable_console: bool = True,
          enable_file: bool = True,
          rotation: Optional[str] = None,
          retention: str = "30 days",
          max_file_size: Optional[str] = None,
          colorize: Optional[bool] = None,
          force_reinit: bool = True) -> None
```

Setup the logger with custom configuration.

This method should be called early in your application, before any logging occurs.
By default, force_reinit is True so the logger will be reinitialized on each call.
Set force_reinit=False to keep an existing configuration.

**Arguments**:

    level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    log_file: Path to log file (optional)
    enable_console: Whether to enable console logging
    enable_file: Whether to enable file logging
    rotation: Log file rotation size (deprecated, use max_file_size)
    retention: Log file retention period
    max_file_size: Maximum log file size before rotation (e.g., "10 MB", "100 MB")
    colorize: Whether to use colors in console output (None = auto-detect)
    force_reinit: Force reinitialization even if already initialized (default: False)
  

**Example**:

Configure logging for different scenarios

```python
from .logger import AgentBayLogger, get_logger

# Basic setup with debug level
AgentBayLogger.setup(level="DEBUG")
logger = get_logger("app")
logger.debug("Debug mode enabled")
# Output: Debug mode enabled

# Setup with custom log file and rotation
AgentBayLogger.setup(
level="INFO",
log_file="/var/log/agentbay/app.log",
max_file_size="50 MB",
retention="7 days"
)
logger = get_logger("app")
logger.info("Application started with file logging")
# Output: Application started with file logging
# Also written to /var/log/agentbay/app.log

# Console-only logging without colors (for CI/CD)
AgentBayLogger.setup(
level="WARNING",
enable_file=False,
colorize=False
)
logger = get_logger("ci")
logger.warning("This is a warning in CI environment")
# Output: This is a warning in CI environment (no colors)

# File-only logging (no console output)
AgentBayLogger.setup(
level="DEBUG",
log_file="/tmp/debug.log",
enable_console=False,
enable_file=True
)
logger = get_logger("debug")
logger.debug("This only appears in the log file")
# No console output, but written to /tmp/debug.log

```
### get\_logger

```python
@classmethod
def get_logger(cls, name: Optional[str] = None)
```

Get a logger instance.

**Arguments**:

    name: Logger name (optional)
  

**Returns**:

  Configured logger instance

### set\_level

```python
@classmethod
def set_level(cls, level: str) -> None
```

Set the logging level.

**Arguments**:

    level: New log level
  

**Example**:

Change log level during runtime

```python
from .logger import AgentBayLogger, get_logger

# Start with INFO level
AgentBayLogger.setup(level="INFO")
logger = get_logger("app")

logger.info("This will appear")
# Output: This will appear
logger.debug("This won't appear")
# No output (DEBUG < INFO)

# Change to DEBUG level at runtime
AgentBayLogger.set_level("DEBUG")
logger.debug("Now debug messages appear")
# Output: Now debug messages appear

# Change to WARNING level
AgentBayLogger.set_level("WARNING")
logger.info("This won't appear anymore")
# No output (INFO < WARNING)
logger.warning("But warnings still appear")
# Output: But warnings still appear

```
### get\_logger

```python
def get_logger(name: str = "agentbay")
```

Convenience function to get a named logger.

**Arguments**:

    name: Logger name (defaults to "agentbay")
  

**Returns**:

  Named logger instance

#### log

```python
log = get_logger("agentbay")
```

## See Also

- [Synchronous vs Asynchronous API](../../../docs/guides/async-programming/sync-vs-async.md)

---

*Documentation generated automatically from source code using pydoc-markdown.*
