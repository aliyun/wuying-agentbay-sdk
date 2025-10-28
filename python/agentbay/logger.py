"""
Unified logging configuration for AgentBay SDK using loguru.

This module provides a centralized logging configuration with beautiful formatting
and structured output for different log levels.
"""

import sys
from pathlib import Path
from typing import Optional, Union, Dict, Any, List
from loguru import logger
import os


class AgentBayLogger:
    """AgentBay SDK Logger with beautiful formatting."""
    
    _initialized = False
    _log_level = "INFO"
    _log_file: Optional[Path] = None
    
    @classmethod
    def setup(
        cls,
        level: str = "INFO",
        log_file: Optional[Union[str, Path]] = None,
        enable_console: bool = True,
        enable_file: bool = True,
        rotation: str = "10 MB",
        retention: str = "30 days"
    ) -> None:
        """
        Setup the logger with custom configuration.
        
        Args:
            level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_file: Path to log file (optional)
            enable_console: Whether to enable console logging
            enable_file: Whether to enable file logging
            rotation: Log file rotation size
            retention: Log file retention period
        """
        if cls._initialized:
            return
            
        # Remove default handler
        logger.remove()
        
        cls._log_level = level.upper()
        
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
                colorize=True,
                backtrace=True,
                diagnose=True
            )
        
        # File handler with structured formatting
        if enable_file:
            if log_file:
                cls._log_file = Path(log_file) if isinstance(log_file, str) else log_file
            else:
                # Default log file path in python/ directory
                current_dir = Path(__file__).parent.parent  # Go up from agentbay/ to python/
                cls._log_file = current_dir / "agentbay.log"
            
            cls._log_file.parent.mkdir(parents=True, exist_ok=True)
            
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
                rotation=rotation,
                retention=retention,
                backtrace=True,
                diagnose=True
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
        if not cls._initialized:
            cls.setup()
        
        if name:
            return logger.bind(name=name)
        return logger
    
    @classmethod
    def set_level(cls, level: str) -> None:
        """
        Set the logging level.
        
        Args:
            level: New log level
        """
        cls._log_level = level.upper()
        if cls._initialized:
            # Re-initialize with new level
            cls._initialized = False
            cls.setup(level=cls._log_level)


# Initialize logger on import
AgentBayLogger.setup(
    level=os.getenv("AGENTBAY_LOG_LEVEL", "INFO"),
    enable_console=True,
    enable_file=True,  # Always enable file logging by default
    log_file=os.getenv("AGENTBAY_LOG_FILE")  # Use custom path if specified, otherwise use default
)

# Export the logger instance for easy import
log = AgentBayLogger.get_logger("agentbay")


def get_logger(name: str):
    """
    Convenience function to get a named logger.

    Args:
        name: Logger name

    Returns:
        Named logger instance
    """
    return AgentBayLogger.get_logger(name)


# Sensitive field names for data masking
SENSITIVE_FIELDS = [
    'api_key', 'apikey', 'api-key',
    'password', 'passwd', 'pwd',
    'token', 'access_token', 'auth_token',
    'secret', 'private_key',
    'authorization',
]


def mask_sensitive_data(data: Any, fields: List[str] = None) -> Any:
    """
    Mask sensitive information in data structures.

    Args:
        data: Data to mask (dict, str, list, etc.)
        fields: Additional sensitive field names

    Returns:
        Masked data (deep copy)
    """
    if fields is None:
        fields = SENSITIVE_FIELDS

    if isinstance(data, dict):
        masked = {}
        for key, value in data.items():
            if any(field in key.lower() for field in fields):
                if isinstance(value, str) and len(value) > 4:
                    masked[key] = value[:2] + '****' + value[-2:]
                else:
                    masked[key] = '****'
            else:
                masked[key] = mask_sensitive_data(value, fields)
        return masked
    elif isinstance(data, list):
        return [mask_sensitive_data(item, fields) for item in data]
    elif isinstance(data, str):
        # Don't mask plain strings, only dict keys
        return data
    else:
        return data


# Compatibility functions for common logging patterns
def log_api_call(api_name: str, request_data: str = "") -> None:
    """Log API call with consistent formatting."""
    log.opt(depth=1).info(f"🔗 API Call: {api_name}")
    if request_data:
        log.opt(depth=1).debug(f"📤 Request: {request_data}")


def log_api_response(response_data: str, success: bool = True) -> None:
    """Log API response with consistent formatting."""
    if success:
        log.opt(depth=1).info("✅ API Response received")
        log.opt(depth=1).debug(f"📥 Response: {response_data}")
    else:
        log.opt(depth=1).error("❌ API Response failed")
        log.opt(depth=1).error(f"📥 Response: {response_data}")


def log_api_response_with_details(
    api_name: str,
    request_id: str = "",
    success: bool = True,
    key_fields: Dict[str, Any] = None,
    full_response: str = ""
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
                log.opt(depth=1).info(f"  └─ {key}={value}")

        if full_response:
            log.opt(depth=1).debug(f"📥 Full Response: {full_response}")
    else:
        log.opt(depth=1).error(f"❌ API Response Failed: {api_name}, RequestId={request_id}")
        if full_response:
            log.opt(depth=1).error(f"📥 Response: {full_response}")


def log_operation_start(operation: str, details: str = "") -> None:
    """Log the start of an operation."""
    log.opt(depth=1).info(f"🚀 Starting: {operation}")
    if details:
        log.opt(depth=1).debug(f"📋 Details: {details}")


def log_operation_success(operation: str, result: str = "") -> None:
    """Log successful operation completion."""
    log.opt(depth=1).info(f"✅ Completed: {operation}")
    if result:
        log.opt(depth=1).debug(f"📊 Result: {result}")


def log_operation_error(operation: str, error: str, exc_info: bool = False) -> None:
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


def log_warning(message: str, details: str = "") -> None:
    """Log warning with consistent formatting."""
    log.opt(depth=1).warning(f"⚠️  {message}")
    if details:
        log.opt(depth=1).warning(f"📝 Details: {details}")
