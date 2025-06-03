import os
import json
from typing import Dict, Any


def default_config() -> Dict[str, Any]:
    """Return the default configuration"""
    return {
        "region_id": "cn-shanghai",
        "endpoint": "wuyingai.cn-shanghai.aliyuncs.com",
        "timeout_ms": 60000
    }


def load_config() -> Dict[str, Any]:
    """Load configuration from file"""
    # First check if the config file path is specified in environment variables
    config_path = os.getenv("AGENTBAY_CONFIG_PATH")
    if not config_path:
        # Try to find the config file in the project root directory
        # First try the current directory
        config_path = "config.json"
        if not os.path.exists(config_path):
            # Then try the parent directory
            config_path = os.path.join("..", "config.json")
            if not os.path.exists(config_path):
                # Then try the grandparent directory
                config_path = os.path.join("..", "..", "config.json")
                if not os.path.exists(config_path):
                    # Config file not found, return default config
                    print("Warning: Configuration file not found, using default values")
                    return default_config()

    try:
        # Read the config file
        with open(config_path, "r") as f:
            config = json.load(f)
    except Exception as e:
        print(f"Warning: Failed to read configuration file: {e}, using default values")
        return default_config()

    # Allow environment variables to override config file values
    if region_id := os.getenv("AGENTBAY_REGION_ID"):
        config["region_id"] = region_id
    if endpoint := os.getenv("AGENTBAY_ENDPOINT"):
        config["endpoint"] = endpoint

    return config
