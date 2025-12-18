import os
import tempfile
import unittest
from pathlib import Path
from unittest import TestCase
from unittest.mock import mock_open, patch

from agentbay import Config
from agentbay import _default_config, _load_config

def _writable_temp_root() -> Path:
    root = Path(__file__).resolve().parent / ".pytest-tmp"
    root.mkdir(parents=True, exist_ok=True)
    return root


class LoadConfigTestCase(unittest.TestCase):
    def setUp(self):
        # Create temporary .env file directory
        self.test_dir = tempfile.TemporaryDirectory(dir=str(_writable_temp_root()))
        self.env_file = Path(self.test_dir.name) / ".env"

    def tearDown(self):
        self.test_dir.cleanup()

    def test_load_from_passed_config(self):
        """Test loading configuration from passed Config object"""
        os.chdir(self.test_dir.name)
        custom_cfg = Config(
            endpoint="custom-endpoint",
            timeout_ms=5000,
        )
        result = _load_config(custom_cfg)

        self.assertEqual(result["endpoint"], "custom-endpoint")
        self.assertEqual(result["timeout_ms"], 5000)

    def test_load_from_env_file(self):
        """Test loading configuration from .env file"""
        os.environ.pop("AGENTBAY_ENDPOINT", None)
        os.environ.pop("AGENTBAY_TIMEOUT_MS", None)

        os.chdir(self.test_dir.name)
        def _fake_load_dotenv(_path) -> bool:
            os.environ.setdefault("AGENTBAY_ENDPOINT", "env-endpoint")
            os.environ.setdefault("AGENTBAY_TIMEOUT_MS", "10000")
            return True

        with patch("agentbay._common.config._find_dotenv_file", return_value=self.env_file):
            with patch("agentbay._common.config.dotenv.load_dotenv", side_effect=_fake_load_dotenv):
                result = _load_config(None)

        self.assertEqual(result["endpoint"], "env-endpoint")
        self.assertEqual(result["timeout_ms"], 10000)

    @patch("pathlib.Path.is_file", return_value=False)
    def test_load_from_system_env_vars(self, mock_is_file):
        """Test loading configuration from system environment variables"""
        os.chdir(self.test_dir.name)
        os.environ["AGENTBAY_ENDPOINT"] = "sys-endpoint"
        os.environ["AGENTBAY_TIMEOUT_MS"] = "15000"

        result = _load_config(None)

        self.assertEqual(result["endpoint"], "sys-endpoint")
        self.assertEqual(result["timeout_ms"], 15000)

    @patch("pathlib.Path.is_file", return_value=False)
    def test_use__default_config_when_no_source_provided(self, mock_is_file):
        """Test using default values when no configuration source is provided"""
        # Clear all related environment variables
        os.chdir(self.test_dir.name)
        os.environ.pop("AGENTBAY_ENDPOINT", None)
        os.environ.pop("AGENTBAY_TIMEOUT_MS", None)

        result = _load_config(None)

        default = _default_config()
        self.assertEqual(result["endpoint"], default["endpoint"])
        self.assertEqual(result["timeout_ms"], default["timeout_ms"])

    def test_config_precedence_order(self):
        """Test configuration priority order"""
        def _fake_load_dotenv(_path) -> bool:
            os.environ.setdefault("AGENTBAY_ENDPOINT", "env-endpoint")
            os.environ.setdefault("AGENTBAY_TIMEOUT_MS", "10000")
            return True

        os.chdir(self.test_dir.name)
        # Set environment variables
        os.environ["AGENTBAY_ENDPOINT"] = "sys-endpoint"
        os.environ["AGENTBAY_TIMEOUT_MS"] = "15000"

        # Default configuration
        default = _default_config()

        # 1. Test that explicitly passed configuration has highest priority
        custom_cfg = Config(
            endpoint="explicit-endpoint",
            timeout_ms=2000,
        )
        result = _load_config(custom_cfg)
        self.assertEqual(result["endpoint"], "explicit-endpoint")
        self.assertEqual(result["timeout_ms"], 2000)

        # 2. When explicit configuration is None, should use environment variables
        with patch("agentbay._common.config._find_dotenv_file", return_value=self.env_file):
            with patch("agentbay._common.config.dotenv.load_dotenv", side_effect=_fake_load_dotenv):
                result = _load_config(None)
        self.assertEqual(result["endpoint"], "sys-endpoint")
        self.assertEqual(result["timeout_ms"], 15000)

        # 3. After clearing environment variables, should use .env file
        os.environ.pop("AGENTBAY_ENDPOINT")
        os.environ.pop("AGENTBAY_TIMEOUT_MS")
        with patch("agentbay._common.config._find_dotenv_file", return_value=self.env_file):
            with patch("agentbay._common.config.dotenv.load_dotenv", side_effect=_fake_load_dotenv):
                result = _load_config(None)
        self.assertEqual(result["endpoint"], "env-endpoint")
        self.assertEqual(result["timeout_ms"], 10000)


if __name__ == "__main__":
    unittest.main()
