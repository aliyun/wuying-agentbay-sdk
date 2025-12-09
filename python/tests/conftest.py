import os
import sys

# Set environment variables for IDE testing
os.environ["FORCE_COLOR"] = "1"
os.environ["TERM"] = "xterm-256color"
os.environ.setdefault("AGENTBAY_LOG_LEVEL", "INFO")
os.environ["PYTHONUNBUFFERED"] = "1"


def pytest_configure(config):
    """Configure pytest to apply color formatting to logs"""
    # Import after environment variables are set
    from loguru import logger

    from agentbay import AgentBayLogger
    from agentbay import _colorize_log_message

    # Reset the logger initialization flag
    AgentBayLogger._initialized = False

    # Remove all handlers
    logger.remove()

    # Re-add stderr handler with color filter
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<bold><blue>AgentBay</blue></bold> | "
        "<level>{level}</level> | "
        "<yellow>{process.id}:{thread.id}</yellow> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>",
        level=os.getenv("AGENTBAY_LOG_LEVEL", "WARNING"),
        filter=_colorize_log_message,
        colorize=True,
        backtrace=True,
        diagnose=True,
    )

    # Also add file handler without the color filter
    log_file = os.getenv("AGENTBAY_LOG_FILE")
    if not log_file:
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        log_file = os.path.join(current_dir, "agentbay.log")

    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    logger.add(
        log_file,
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | AgentBay | {level: <8} | {process.id}:{thread.id} | {name}:{function}:{line} | {message}",
        level=os.getenv("AGENTBAY_LOG_LEVEL", "WARNING"),
        colorize=False,
        backtrace=True,
        diagnose=True,
    )
