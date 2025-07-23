import json
import os
from typing import Any, Dict
import dotenv
from pathlib import Path


def default_config() -> Dict[str, Any]:
    """Return the default configuration"""
    return {
        "region_id": "cn-shanghai",
        "endpoint": "wuyingai.cn-shanghai.aliyuncs.com",
        "timeout_ms": 60000,
    }


# Browser data path constant
BROWSER_DATA_PATH = "/tmp/agentbay_browser"


"""
The SDK uses the following precedence order for configuration (highest to lowest):
1. Explicitly passed configuration in code.
2. Environment variables.
3. .env file.
4. Default configuration.
"""


def load_config(cfg) -> Dict[str, Any]:
    if cfg is not None:
        config = {
            "region_id": cfg.region_id,
            "endpoint": cfg.endpoint,
            "timeout_ms": cfg.timeout_ms,
        }
    else:
        config = default_config()
        try:
            env_path = Path(os.getcwd()) / ".env"
            dotenv.load_dotenv(env_path)
        except:
            print("Warning: Failed to load .env file")
        if region_id := os.getenv("AGENTBAY_REGION_ID"):
            config["region_id"] = region_id
        if endpoint := os.getenv("AGENTBAY_ENDPOINT"):
            config["endpoint"] = endpoint
        if timeout_ms := os.getenv("AGENTBAY_TIMEOUT_MS"):
            config["timeout_ms"] = int(timeout_ms)
    return config
