import json
import pytest
import unittest

from agentbay import CreateSessionParams, AppManagerRule, ExtraConfigs, MobileExtraConfig


class TestAsyncCreateSessionParams(unittest.TestCase):
    @pytest.mark.sync

    def test_default_initialization(self):
        """Test that CreateSessionParams initializes with default values."""
        params = CreateSessionParams()
        self.assertEqual(params.labels, {})

    @pytest.mark.sync


    def test_custom_labels(self):
        """Test that CreateSessionParams accepts custom labels."""
        labels = {"username": "alice", "project": "my-project"}
        params = CreateSessionParams(labels=labels)
        self.assertEqual(params.labels, labels)

    @pytest.mark.sync


    def test_labels_json_conversion(self):
        """Test that labels can be converted to JSON for the API request."""
        labels = {"username": "alice", "project": "my-project"}
        params = CreateSessionParams(labels=labels)

        # Simulate what happens in AgentBay.create()
        labels_json = json.dumps(params.labels)

        # Verify the JSON string
        parsed_labels = json.loads(labels_json)
        self.assertEqual(parsed_labels, labels)

    @pytest.mark.sync


    def test_policy_id(self):
        """Test that policy_id can be carried by CreateSessionParams."""
        params = CreateSessionParams(policy_id="policy-xyz")
        self.assertEqual(params.policy_id, "policy-xyz")

    @pytest.mark.sync


    def test_extra_configs_initialization(self):
        """Test that CreateSessionParams accepts extra_configs parameter."""
        # Create mobile configuration with whitelist
        app_rule = AppManagerRule(
            rule_type="White",
            app_package_name_list=["com.example.app", "com.trusted.service"],
        )
        mobile_config = MobileExtraConfig(
            lock_resolution=True, app_manager_rule=app_rule
        )
        extra_configs = ExtraConfigs(mobile=mobile_config)

        params = CreateSessionParams(extra_configs=extra_configs)
        self.assertEqual(params.extra_configs, extra_configs)
        self.assertEqual(params.extra_configs.mobile.lock_resolution, True)
        self.assertEqual(
            params.extra_configs.mobile.app_manager_rule.rule_type, "White"
        )
        self.assertEqual(
            len(params.extra_configs.mobile.app_manager_rule.app_package_name_list), 2
        )

    @pytest.mark.sync


    def test_mobile_extra_config_comprehensive(self):
        """Comprehensive test for MobileExtraConfig with all configuration options."""
        # Test whitelist configuration with all features
        whitelist_rule = AppManagerRule(
            rule_type="White",
            app_package_name_list=["com.allowed.app1", "com.allowed.app2"],
        )
        whitelist_config = MobileExtraConfig(
            lock_resolution=True,
            app_manager_rule=whitelist_rule,
            hide_navigation_bar=True,
            uninstall_blacklist=["com.android.systemui", "com.android.settings"],
        )

        # Verify whitelist configuration
        self.assertTrue(whitelist_config.lock_resolution)
        self.assertEqual(whitelist_config.app_manager_rule.rule_type, "White")
        self.assertIn(
            "com.allowed.app1", whitelist_config.app_manager_rule.app_package_name_list
        )
        self.assertIn(
            "com.allowed.app2", whitelist_config.app_manager_rule.app_package_name_list
        )
        self.assertTrue(whitelist_config.hide_navigation_bar)
        self.assertIsNotNone(whitelist_config.uninstall_blacklist)
        self.assertEqual(len(whitelist_config.uninstall_blacklist), 2)

        # Test blacklist configuration with different settings
        blacklist_rule = AppManagerRule(
            rule_type="Black",
            app_package_name_list=["com.malware.app", "com.blocked.service"],
        )
        blacklist_config = MobileExtraConfig(
            lock_resolution=False,
            app_manager_rule=blacklist_rule,
            hide_navigation_bar=False,
            uninstall_blacklist=["com.android.systemui"],
        )

        # Verify blacklist configuration
        self.assertFalse(blacklist_config.lock_resolution)
        self.assertEqual(blacklist_config.app_manager_rule.rule_type, "Black")
        self.assertIn(
            "com.malware.app", blacklist_config.app_manager_rule.app_package_name_list
        )
        self.assertFalse(blacklist_config.hide_navigation_bar)
        self.assertIsNotNone(blacklist_config.uninstall_blacklist)
        self.assertEqual(len(blacklist_config.uninstall_blacklist), 1)

        # Test minimal configuration (only new features)
        minimal_config = MobileExtraConfig(
            hide_navigation_bar=True, uninstall_blacklist=["com.critical.app"]
        )

        # Verify minimal configuration
        self.assertIsNone(minimal_config.lock_resolution)
        self.assertIsNone(minimal_config.app_manager_rule)
        self.assertTrue(minimal_config.hide_navigation_bar)
        self.assertEqual(len(minimal_config.uninstall_blacklist), 1)
        self.assertIn("com.critical.app", minimal_config.uninstall_blacklist)

    @pytest.mark.sync


    def test_app_manager_rule_validation(self):
        """Test AppManagerRule validation with various inputs."""
        # Test with valid string list
        app_rule = AppManagerRule(
            rule_type="White",
            app_package_name_list=["com.valid.app", "com.another.app"],
        )
        # Should not raise any exception
        app_rule.validate()

        # Test with empty list
        app_rule_empty = AppManagerRule(rule_type="Black", app_package_name_list=[])
        app_rule_empty.validate()  # Should not raise

    @pytest.mark.sync


    def test_extra_configs_serialization_comprehensive(self):
        """Comprehensive test for ExtraConfigs serialization and deserialization."""
        # Test complete configuration serialization
        app_rule = AppManagerRule(
            rule_type="White", app_package_name_list=["com.test.app", "com.another.app"]
        )
        mobile_config = MobileExtraConfig(
            lock_resolution=True,
            app_manager_rule=app_rule,
            hide_navigation_bar=True,
            uninstall_blacklist=["com.android.systemui", "com.android.settings"],
        )
        extra_configs = ExtraConfigs(mobile=mobile_config)

        # Test serialization (to_map)
        config_dict = extra_configs.to_map()

        self.assertIn("Mobile", config_dict)
        mobile_dict = config_dict["Mobile"]
        self.assertIn("LockResolution", mobile_dict)
        self.assertIn("AppManagerRule", mobile_dict)
        self.assertIn("HideNavigationBar", mobile_dict)
        self.assertIn("UninstallBlacklist", mobile_dict)

        self.assertTrue(mobile_dict["LockResolution"])
        self.assertTrue(mobile_dict["HideNavigationBar"])
        self.assertEqual(
            mobile_dict["UninstallBlacklist"],
            ["com.android.systemui", "com.android.settings"],
        )
        self.assertEqual(mobile_dict["AppManagerRule"]["RuleType"], "White")
        self.assertEqual(
            mobile_dict["AppManagerRule"]["AppPackageNameList"],
            ["com.test.app", "com.another.app"],
        )

        # Test deserialization (from_map) with different configuration
        different_config_dict = {
            "Mobile": {
                "LockResolution": False,
                "HideNavigationBar": False,
                "UninstallBlacklist": ["com.critical.system.app"],
                "AppManagerRule": {
                    "RuleType": "Black",
                    "AppPackageNameList": [
                        "com.blocked.app1",
                        "com.blocked.app2",
                        "com.malware.app",
                    ],
                },
            }
        }

        new_extra_configs = ExtraConfigs()
        new_extra_configs.from_map(different_config_dict)

        # Verify deserialization
        self.assertIsNotNone(new_extra_configs.mobile)
        mobile = new_extra_configs.mobile
        self.assertFalse(mobile.lock_resolution)
        self.assertFalse(mobile.hide_navigation_bar)
        self.assertEqual(len(mobile.uninstall_blacklist), 1)
        self.assertIn("com.critical.system.app", mobile.uninstall_blacklist)
        self.assertEqual(mobile.app_manager_rule.rule_type, "Black")
        self.assertEqual(len(mobile.app_manager_rule.app_package_name_list), 3)
        self.assertIn("com.blocked.app1", mobile.app_manager_rule.app_package_name_list)
        self.assertIn("com.malware.app", mobile.app_manager_rule.app_package_name_list)

        # Test round-trip serialization (serialize -> deserialize -> serialize)
        round_trip_dict = new_extra_configs.to_map()
        self.assertEqual(round_trip_dict, different_config_dict)


if __name__ == "__main__":
    unittest.main()
