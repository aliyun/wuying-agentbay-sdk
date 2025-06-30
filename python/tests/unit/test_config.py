import json
import os
import unittest
from unittest.mock import patch, mock_open, MagicMock

from agentbay.config import default_config, load_config


class TestConfig(unittest.TestCase):
    """Test the configuration module functionality"""

    def test_default_config(self):
        """Test the default configuration values"""
        config = default_config()
        self.assertIsInstance(config, dict)
        self.assertEqual(config["region_id"], "cn-shanghai")
        self.assertEqual(config["endpoint"], "wuyingai.cn-shanghai.aliyuncs.com")
        self.assertEqual(config["timeout_ms"], 60000)

    @patch("os.getenv")
    def test_load_config_from_env_var(self, mock_getenv):
        """Test loading configuration from a file specified by environment variable"""
        # Mock environment variable
        mock_getenv.side_effect = lambda var, default=None: "/path/to/config.json" if var == "AGENTBAY_CONFIG_PATH" else None

        # Mock configuration file content
        mock_file_data = '{"region_id": "cn-beijing", "endpoint": "custom.endpoint.com", "timeout_ms": 30000}'

        # Use mock_open to simulate file operations
        with patch("builtins.open", mock_open(read_data=mock_file_data)):
            config = load_config()

        self.assertEqual(config["region_id"], "cn-beijing")
        self.assertEqual(config["endpoint"], "custom.endpoint.com")
        self.assertEqual(config["timeout_ms"], 30000)

    @patch("os.getenv", return_value=None)
    @patch("os.path.exists", return_value=True)
    @patch("os.getcwd", return_value="/current/dir")
    @patch("os.path.join")
    def test_load_config_from_current_dir(self, mock_join, mock_getcwd, mock_exists, mock_getenv):
        """Test loading configuration file from current directory"""
        # Mock path joining
        mock_join.side_effect = lambda *args: "/current/dir/.config.json" if args[1] == ".config.json" else "/other/path"

        # Mock configuration file content
        mock_file_data = '{"region_id": "cn-hongkong", "endpoint": "hk.endpoint.com", "custom_setting": true}'

        # Use mock_open to simulate file operations
        with patch("builtins.open", mock_open(read_data=mock_file_data)):
            config = load_config()

        self.assertEqual(config["region_id"], "cn-hongkong")
        self.assertEqual(config["endpoint"], "hk.endpoint.com")
        self.assertTrue(config["custom_setting"])

    @patch("os.getenv", return_value=None)
    @patch("os.path.exists", return_value=False)
    def test_load_config_fallback_to_default(self, mock_exists, mock_getenv):
        """Test fallback to default configuration when no config file is found"""
        config = load_config()

        self.assertEqual(config["region_id"], "cn-shanghai")
        self.assertEqual(config["endpoint"], "wuyingai.cn-shanghai.aliyuncs.com")
        self.assertEqual(config["timeout_ms"], 60000)

    @patch("os.getenv")
    @patch("os.path.exists", return_value=True)
    def test_environment_variables_override(self, mock_exists, mock_getenv):
        """Test environment variables overriding configuration file settings"""
        # Mock configuration file exists
        mock_getenv.side_effect = lambda var, default=None: {
            "AGENTBAY_CONFIG_PATH": None,
            "AGENTBAY_REGION_ID": "cn-zhangjiakou",
            "AGENTBAY_ENDPOINT": "env.endpoint.com"
        }.get(var, None)

        # Mock configuration file content
        mock_file_data = '{"region_id": "cn-beijing", "endpoint": "file.endpoint.com", "timeout_ms": 30000}'

        # Use mock_open to simulate file operations
        with patch("builtins.open", mock_open(read_data=mock_file_data)):
            config = load_config()

        # Environment variables should override settings in the file
        self.assertEqual(config["region_id"], "cn-zhangjiakou")
        self.assertEqual(config["endpoint"], "env.endpoint.com")
        # Values not set in environment variables should keep values from file
        self.assertEqual(config["timeout_ms"], 30000)

    @patch("os.getenv", return_value=None)
    @patch("os.path.exists", return_value=True)
    @patch("builtins.open")
    def test_load_config_handles_file_read_error(self, mock_open, mock_exists, mock_getenv):
        """Test handling configuration file read errors"""
        # Mock file read error
        mock_open.side_effect = IOError("Cannot read file")

        config = load_config()

        # Should fall back to default configuration
        self.assertEqual(config["region_id"], "cn-shanghai")
        self.assertEqual(config["endpoint"], "wuyingai.cn-shanghai.aliyuncs.com")
        self.assertEqual(config["timeout_ms"], 60000)


if __name__ == "__main__":
    unittest.main()