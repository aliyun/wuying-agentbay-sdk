import os
import sys
import unittest

from agentbay import AgentBay
from agentbay.session_params import CreateSessionParams
from agentbay.api.models import ExtraConfigs, MobileExtraConfig, AppManagerRule
from agentbay.exceptions import AgentBayError

# Add the parent directory to the path so we can import the agentbay package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestSessionExtraConfigsIntegration(unittest.TestCase):
    """Integration test cases for session creation with extra configurations using real API."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment with real API key."""
        cls.api_key = os.getenv("AGENTBAY_API_KEY")
        if not cls.api_key:
            raise unittest.SkipTest("AGENTBAY_API_KEY environment variable not set")
        
        cls.agent_bay = AgentBay(api_key=cls.api_key)
        print(f"AgentBay client initialized for extra configs testing")
    
    def setUp(self):
        """Set up for each test method."""
        self.session = None

    def test_create_session_with_mobile_extra_configs_integration(self):
        """Integration test for creating a mobile session with extra configurations."""
        print("=" * 80)
        print("TEST: Mobile Session with Extra Configurations")
        print("=" * 80)
        
        # Step 1: Create mobile configuration with all new features
        print("Step 1: Creating mobile configuration with extra configs...")
        app_rule = AppManagerRule(
            rule_type="White",
            app_package_name_list=[
                "com.android.settings",
                "com.example.test.app"
            ]
        )
        
        mobile_config = MobileExtraConfig(
            lock_resolution=True,
            app_manager_rule=app_rule,
            hide_navigation_bar=True,  # New feature: hide navigation bar
            uninstall_blacklist=[      # New feature: uninstall protection
                "com.android.systemui",
                "com.android.settings"
            ]
        )
        
        extra_configs = ExtraConfigs(mobile=mobile_config)
        print(f"Mobile config created: lock_resolution={mobile_config.lock_resolution}, "
              f"hide_navigation_bar={mobile_config.hide_navigation_bar}, "
              f"uninstall_blacklist={len(mobile_config.uninstall_blacklist)} packages, "
              f"app_rule={mobile_config.app_manager_rule.rule_type}")
        
        # Step 2: Create session parameters
        params = CreateSessionParams(
            image_id="mobile_latest",
            labels={
                "test_type": "mobile_extra_configs_integration",
                "created_by": "integration_test"
            },
            extra_configs=extra_configs
        )
        print(f"Session params: image_id={params.image_id}, labels={params.labels}")
        
        # Step 3: Create session
        print("Step 2: Creating mobile session with extra configurations...")
        create_result = self.__class__.agent_bay.create(params)
        
        # Verify SessionResult structure
        self.assertTrue(create_result.success, f"Session creation failed: {create_result.error_message}")
        self.assertIsNotNone(create_result.request_id)
        self.assertIsInstance(create_result.request_id, str)
        self.assertGreater(len(create_result.request_id), 0)
        self.assertIsNotNone(create_result.session)
        self.assertFalse(create_result.error_message)
        
        self.session = create_result.session
        print(f"✓ Mobile session created successfully with ID: {self.session.session_id} (RequestID: {create_result.request_id})")
        
        try:
            # Step 4: Verify session properties
            print("Step 3: Verifying session properties...")
            self.assertIsNotNone(self.session.session_id)
            self.assertTrue(len(self.session.session_id) > 0, "Session ID should not be empty")
            print(f"✓ Session properties verified: ID={self.session.session_id}")
            
            # Step 5: Verify mobile environment
            print("Step 4: Verifying mobile environment...")
            info_result = self.session.info()
            if info_result.success:
                resource_url = info_result.data.resource_url.lower()
                self.assertTrue(
                    "android" in resource_url or "mobile" in resource_url,
                    f"Session should be mobile-based, got URL: {info_result.data.resource_url}"
                )
                print(f"✓ Mobile environment verified (RequestID: {info_result.request_id})")
            else:
                print(f"⚠ Failed to get session info: {info_result.error_message}")
            
            # Step 6: Verify labels
            print("Step 5: Verifying session labels...")
            labels_result = self.session.get_labels()
            if labels_result.success:
                labels = labels_result.data
                self.assertEqual(labels.get("test_type"), "mobile_extra_configs_integration")
                print(f"✓ Labels verified: {labels} (RequestID: {labels_result.request_id})")
            else:
                print(f"⚠ Failed to get session labels: {labels_result.error_message}")
            
            # Step 7: Test mobile functionality
            print("Step 6: Testing mobile functionality...")
            
            # Test screenshot functionality
            screenshot_result = self.session.mobile.screenshot()
            if screenshot_result.success:
                self.assertIsNotNone(screenshot_result.data)
                print(f"✓ Mobile screenshot working (RequestID: {screenshot_result.request_id})")
            else:
                print(f"⚠ Mobile screenshot failed: {screenshot_result.error_message}")
            
            # Test mobile configuration methods
            print("Step 7: Testing mobile configuration methods...")
            try:
                self.session.mobile.set_resolution_lock(True)
                self.session.mobile.set_navigation_bar_visibility(True)
                self.session.mobile.set_uninstall_blacklist(["com.android.systemui"])
                print("✓ Mobile configuration methods executed successfully")
            except Exception as e:
                print(f"⚠ Mobile configuration methods failed: {e}")
                
        finally:
            # Step 8: Clean up
            print("Step 8: Cleaning up session...")
            if self.session:
                delete_result = self.__class__.agent_bay.delete(self.session)
                if delete_result.success:
                    print(f"✓ Session deleted successfully (RequestID: {delete_result.request_id})")
                else:
                    print(f"⚠ Failed to delete session: {delete_result.error_message}")
                    
        print("✓ Mobile extra configs integration test completed successfully")
    
    def tearDown(self):
        """Clean up after each test method."""
        if self.session:
            try:
                delete_result = self.__class__.agent_bay.delete(self.session)
                if not delete_result.success:
                    print(f"Warning: Failed to clean up session in tearDown: {delete_result.error_message}")
            except Exception as e:
                print(f"Warning: Error during tearDown cleanup: {e}")


if __name__ == "__main__":
    unittest.main()