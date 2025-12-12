"""
Unified logging configuration for AgentBay SDK using loguru.

This module provides a centralized logging configuration with beautiful formatting
and structured output for different log levels.
"""

import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from loguru import logger

# ANSI Color codes
_COLOR_RESET = "\033[0m"
_COLOR_GREEN = "\033[32m"
_COLOR_BLUE = "\033[34m"
_COLOR_CYAN = "\033[36m"


def _colorize_log_message(record):
    """
    Colorize log messages based on content.
    API Calls are blue, Responses are green, Operations are cyan.
    This filter modifies the message in the record and returns True to accept it.
    """
    message = record["message"]

    # Check for API Call
    if "🔗 API Call" in message:
        # Wrap the entire message in blue
        record["message"] = f"{_COLOR_BLUE}{message}{_COLOR_RESET}"
    # Check for API Response (success)
    elif "✅ API Response" in message or "✅ Completed" in message:
        # Wrap the entire message in green
        record["message"] = f"{_COLOR_GREEN}{message}{_COLOR_RESET}"
    # Check for operations starting
    elif "🚀 Starting" in message:
        # Wrap in cyan
        record["message"] = f"{_COLOR_CYAN}{message}{_COLOR_RESET}"

    # Return True to accept the record
    return True


class AgentBayLogger:
    """AgentBay SDK Logger with beautiful formatting."""

    _initialized = False
    _log_level = "INFO"
    _log_file: Optional[Path] = None

    @classmethod
    def _should_use_colors(cls) -> bool:
        """
        Determine whether to use colors in console output.

        Priority:
        1. DISABLE_COLORS environment variable (explicit disable)
        2. FORCE_COLOR environment variable (explicit enable)
        3. TTY detection (terminal output)
        4. IDE environment detection (VS Code, GoLand, IntelliJ)
        5. Default: no colors (safe for file output, CI/CD, pipes)

        Returns:
            bool: True if colors should be used, False otherwise
        """
        # Priority 1: Explicit disable
        if os.getenv("DISABLE_COLORS") == "1":
            return False

        # Priority 2: Explicit enable via FORCE_COLOR
        force_color = os.getenv("FORCE_COLOR", "")
        if force_color and force_color != "0":
            return True

        # Priority 3: TTY detection
        if sys.stderr.isatty():
            return True

        # Priority 4: IDE environment detection
        if os.getenv("TERM_PROGRAM") == "vscode":
            return True
        if os.getenv("GOLAND"):
            return True
        if os.getenv("IDEA_INITIAL_DIRECTORY"):
            return True

        # Default: no colors
        return False

    @classmethod
    def setup(
        cls,
        level: str = "INFO",
        log_file: Optional[Union[str, Path]] = None,
        enable_console: bool = True,
        enable_file: bool = True,
        rotation: Optional[str] = None,
        retention: str = "30 days",
        max_file_size: Optional[str] = None,
        colorize: Optional[bool] = None,
        force_reinit: bool = True,
    ) -> None:
        """
        Setup the logger with custom configuration.

        This method should be called early in your application, before any logging occurs.
        By default, force_reinit is True so the logger will be reinitialized on each call.
        Set force_reinit=False to keep an existing configuration.

        Args:
            level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_file: Path to log file (optional)
            enable_console: Whether to enable console logging
            enable_file: Whether to enable file logging
            rotation: Log file rotation size (deprecated, use max_file_size)
            retention: Log file retention period
            max_file_size: Maximum log file size before rotation (e.g., "10 MB", "100 MB")
            colorize: Whether to use colors in console output (None = auto-detect)
            force_reinit: Force reinitialization even if already initialized (default: False)

        Example:
            Configure logging for different scenarios::

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
        """
        # Automatically reset if already initialized and force_reinit is True
        if cls._initialized and force_reinit:
            cls._initialized = False

        if cls._initialized:
            return

        # Remove default handler
        # Use try-except to handle cases where _logger.remove() might fail
        # (e.g., in pytest environment where handlers might be managed externally)
        try:
            logger.remove()
        except Exception:
            # If removal fails, continue with setup
            # This can happen in test environments
            pass

        cls._log_level = level.upper()

        # Determine if colors should be used
        should_colorize = colorize if colorize is not None else cls._should_use_colors()

        # Console handler with beautiful formatting
        if enable_console:
            console_format = (
                "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
                "<bold><blue>AgentBay</blue></bold> | "
                "<level>{level}</level> | "
                "<yellow>{process.id}:{thread.id}</yellow> | "
                "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
                "<level>{message}</level>"
            )

            logger.add(
                sys.stderr,
                format=console_format,
                level=cls._log_level,
                colorize=should_colorize,
                filter=_colorize_log_message,
                backtrace=True,
                diagnose=True,
            )

        # File handler with structured formatting (no colors)
        if enable_file:
            if log_file:
                cls._log_file = (
                    Path(log_file) if isinstance(log_file, str) else log_file
                )
            else:
                # Default log file path in python/ directory
                current_dir = Path(
                    __file__
                ).parent.parent  # Go up from agentbay/ to python/
                cls._log_file = current_dir / "agentbay.log"

            cls._log_file.parent.mkdir(parents=True, exist_ok=True)

            # Priority: max_file_size > rotation > default
            file_rotation = (
                max_file_size
                if max_file_size is not None
                else (rotation if rotation is not None else "10 MB")
            )

            file_format = (
                "{time:YYYY-MM-DD HH:mm:ss.SSS} | "
                "AgentBay | "
                "{level: <8} | "
                "{process.id}:{thread.id} | "
                "{name}:{function}:{line} | "
                "{message}"
            )

            logger.add(
                str(cls._log_file),
                format=file_format,
                level=cls._log_level,
                colorize=False,
                rotation=file_rotation,
                retention=retention,
                backtrace=True,
                diagnose=True,
            )

        cls._initialized = True

    @classmethod
    def get_logger(cls, name: Optional[str] = None):
        """
        Get a logger instance.

        Args:
            name: Logger name (optional)

        Returns:
            Configured logger instance
        """
        if name:
            return logger.bind(name=name)
        return logger

    @classmethod
    def set_level(cls, level: str) -> None:
        """
        Set the logging level.

        Args:
            level: New log level

        Example:
            Change log level during runtime::

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
        """
        cls._log_level = level.upper()
        if cls._initialized:
            # Re-initialize with new level
            cls._initialized = False
            cls.setup(level=cls._log_level)


# Initialize the _logger automatically on module import
# This provides immediate logging capability without explicit setup
# Read from environment variable if available, otherwise use INFO
_env_log_level = os.getenv("AGENTBAY_LOG_LEVEL", "INFO")
AgentBayLogger.setup(level=_env_log_level)


# Export convenience functions for the _logger
def get_logger(name: str = "agentbay"):
    """
    Convenience function to get a named logger.

    Args:
        name: Logger name (defaults to "agentbay")

    Returns:
        Named logger instance
    """
    return AgentBayLogger.get_logger(name)


# Module-level _logger for convenience functions
log = get_logger("agentbay")


# Sensitive field names for data masking
_SENSITIVE_FIELDS = [
    "api_key",
    "apikey",
    "api-key",
    "password",
    "passwd",
    "pwd",
    "token",
    "access_token",
    "auth_token",
    "secret",
    "private_key",
    "authorization",
]


def _mask_sensitive_data(data: Any, fields: List[str] = None) -> Any:
    """
    Mask sensitive information in data structures.

    Args:
        data: Data to mask (dict, str, list, etc.)
        fields: Additional sensitive field names

    Returns:
        Masked data (deep copy)

    Example:
        Mask sensitive information in various data structures::

            from .logger import mask_sensitive_data

            # Mask API keys and passwords in a dictionary
            user_data = {
                "username": "john_doe",
                "password": "secret123",
                "api_key": "sk_live_1234567890abcdef",
                "email": "john@example.com"
            }
            masked = mask_sensitive_data(user_data)
            print(masked)
            # Output: {'username': 'john_doe', 'password': '****', 'api_key': 'sk****ef', 'email': 'john@example.com'}

            # Mask nested dictionaries
            config = {
                "database": {
                    "host": "localhost",
                    "password": "db_password_123"
                },
                "auth": {
                    "token": "Bearer xyz123abc456"
                }
            }
            masked_config = mask_sensitive_data(config)
            print(masked_config)
            # Output: {'database': {'host': 'localhost', 'password': '****'}, 'auth': {'token': 'Be****56'}}

            # Mask with custom field names
            custom_data = {
                "user_id": "12345",
                "credit_card": "1234-5678-9012-3456",
                "ssn": "123-45-6789"
            }
            masked_custom = mask_sensitive_data(custom_data, fields=['credit_card', 'ssn'])
            print(masked_custom)
            # Output: {'user_id': '12345', 'credit_card': '12****56', 'ssn': '12****89'}

            # Mask lists containing sensitive data
            user_list = [
                {"name": "Alice", "api_key": "key_alice_123"},
                {"name": "Bob", "api_key": "key_bob_456"}
            ]
            masked_list = mask_sensitive_data(user_list)
            print(masked_list)
            # Output: [{'name': 'Alice', 'api_key': 'ke****23'}, {'name': 'Bob', 'api_key': 'ke****56'}]
    """
    if fields is None:
        fields = _SENSITIVE_FIELDS

    if isinstance(data, dict):
        masked = {}
        for key, value in data.items():
            if any(field in key.lower() for field in fields):
                if isinstance(value, str) and len(value) > 4:
                    masked[key] = value[:2] + "****" + value[-2:]
                else:
                    masked[key] = "****"
            else:
                masked[key] = _mask_sensitive_data(value, fields)
        return masked
    elif isinstance(data, list):
        return [_mask_sensitive_data(item, fields) for item in data]
    elif isinstance(data, str):
        # Don't mask plain strings, only dict keys
        return data
    else:
        return data


# Compatibility functions for common logging patterns
def _log_api_call(api_name: str, request_data: str = "") -> None:
    """Log API call with consistent formatting."""
    log.opt(depth=1).info(f"🔗 API Call: {api_name}")
    if request_data:
        log.opt(depth=1).info(f"  └─ {request_data}")


def _log_api_response(response_data: str, success: bool = True) -> None:
    """Log API response with consistent formatting."""
    if success:
        log.opt(depth=1).info("✅ API Response received")
        log.opt(depth=1).debug(f"📥 Response: {response_data}")
    else:
        log.opt(depth=1).error("❌ API Response failed")
        log.opt(depth=1).error(f"📥 Response: {response_data}")


def _log_api_response_with_details(
    api_name: str,
    request_id: str = "",
    success: bool = True,
    key_fields: Dict[str, Any] = None,
    full_response: str = "",
) -> None:
    """
    Log API response with key details at INFO level.

    Args:
        api_name: Name of the API being called
        request_id: Request ID from the response
        success: Whether the API call was successful
        key_fields: Dictionary of key business fields to log
        full_response: Full response body (logged at DEBUG level)
    """
    if success:
        # Main response line with API name and requestId
        main_info = f"✅ API Response: {api_name}"
        if request_id:
            main_info += f", RequestId={request_id}"
        log.opt(depth=1).info(main_info)

        # Log key fields on separate lines for better readability
        if key_fields:
            for key, value in key_fields.items():
                # Add green color to parameter lines
                param_line = f"{_COLOR_GREEN}  └─ {key}={value}{_COLOR_RESET}"
                log.opt(depth=1).info(param_line)

        if full_response:
            log.opt(depth=1).debug(f"📥 Full Response: {full_response}")
    else:
        log.opt(depth=1).error(
            f"❌ API Response Failed: {api_name}, RequestId={request_id}"
        )
        if full_response:
            log.opt(depth=1).error(f"📥 Response: {full_response}")


def _log_code_execution_output(request_id: str, raw_output: str) -> None:
    """
    Extract and log the actual code execution output from run_code response.

    Args:
        request_id: Request ID from the API response
        raw_output: Raw JSON output from the MCP tool
    """
    import json

    try:
        # Parse the JSON response to extract the actual code output
        response = json.loads(raw_output)

        # Extract text from all content items
        texts = []
        if isinstance(response, dict) and "content" in response:
            for item in response.get("content", []):
                if isinstance(item, dict) and item.get("type") == "text":
                    texts.append(item.get("text", ""))

        if not texts:
            return

        actual_output = "".join(texts)

        # Format the output with a clear separator
        header = f"📋 Code Execution Output (RequestID: {request_id}):"
        colored_header = f"{_COLOR_GREEN}{header}{_COLOR_RESET}"

        log.opt(depth=1).info(colored_header)

        # Print each line with indentation
        lines = actual_output.rstrip("\n").split("\n")
        for line in lines:
            colored_line = f"{_COLOR_GREEN}   {line}{_COLOR_RESET}"
            log.opt(depth=1).info(colored_line)

    except (json.JSONDecodeError, KeyError, TypeError):
        # If parsing fails, just return without logging
        pass


def _log_operation_start(operation: str, details: str = "") -> None:
    """Log the start of an operation."""
    log.opt(depth=1).info(f"🚀 Starting: {operation}")
    if details:
        log.opt(depth=1).debug(f"📋 Details: {details}")


def _log_operation_success(operation: str, result: str = "") -> None:
    """Log successful operation completion."""
    log.opt(depth=1).info(f"✅ Completed: {operation}")
    if result:
        log.opt(depth=1).debug(f"📊 Result: {result}")


def _log_operation_error(operation: str, error: str, exc_info: bool = False) -> None:
    """
    Log operation error with optional exception info.

    Args:
        operation: Name of the operation that failed
        error: Error message
        exc_info: Whether to include exception traceback
    """
    if exc_info:
        log.opt(depth=1).exception(f"❌ Failed: {operation}")
    else:
        log.opt(depth=1).error(f"❌ Failed: {operation}")
        log.opt(depth=1).error(f"💥 Error: {error}")


def _log_warning(message: str, details: str = "") -> None:
    """Log warning with consistent formatting."""
    log.opt(depth=1).warning(f"⚠️  {message}")
    if details:
        log.opt(depth=1).warning(f"📝 Details: {details}")


def _log_info_with_color(message: str, color: str = "\033[31m") -> None:
    """
    Log an INFO level message with custom color.

    Args:
        message: Message to log
        color: ANSI color code (default is red: \033[31m)
    """
    colored_message = f"{color}{message}{_COLOR_RESET}"
    log.opt(depth=1).info(colored_message)
