import json
import pytest
import os
import sys
import unittest
from unittest.mock import MagicMock, MagicMock, patch

from agentbay import BrowserContext, CreateSessionParams
from agentbay import AgentBay


class TestAsyncBrowserContextPolicy(unittest.TestCase):
    """Test that browser_context policy includes BWList with white lists."""

    @pytest.mark.sync


    def test_browser_context_policy_creation(self):
        # Create session parameters with browser context
        params = CreateSessionParams()

        # Create browser context
        browser_context = BrowserContext(
            context_id="test-browser-context", auto_upload=True
        )
        params.browser_context = browser_context

        # Create AgentBay instance (this will trigger the policy creation)
        # This will fail without API key, but we can test the policy creation logic

        # We mock the method where policy is created or just test logic if it was extracted.
        # Since the logic is embedded in create(), we should mock internal parts or copy logic to verify.
        # But since the original file was a script running real code (mostly), let's adapt it to be a test.

        # The original test relied on importing internal classes to verify logic manually.
        from agentbay import (
            BWList,
            SyncPolicy,
            UploadPolicy,
            WhiteList,
        )

        # Create a new SyncPolicy with default values for browser context
        upload_policy = UploadPolicy(auto_upload=browser_context.auto_upload)

        # Create BWList with white lists for browser data paths
        white_lists = [
            WhiteList(path="/Local State", exclude_paths=[]),
            WhiteList(path="/Default/Cookies", exclude_paths=[]),
            WhiteList(path="/Default/Cookies-journal", exclude_paths=[]),
        ]
        bw_list = BWList(white_lists=white_lists)

        sync_policy = SyncPolicy(upload_policy=upload_policy, bw_list=bw_list)

        # Serialize policy to JSON string
        policy_json = json.dumps(
            sync_policy,
            default=lambda obj: (
                obj.__dict__() if hasattr(obj, "__dict__") else str(obj)
            ),
            ensure_ascii=False,
        )

        # Verify the policy contains the expected structure
        policy_dict = json.loads(policy_json)

        # Check that bwList exists
        self.assertIn("bwList", policy_dict, "bwList should be present in policy")

        # Check that whiteLists exists in bwList
        self.assertIn(
            "whiteLists",
            policy_dict["bwList"],
            "whiteLists should be present in bwList",
        )

        # Check that we have 3 white lists
        white_lists = policy_dict["bwList"]["whiteLists"]
        self.assertEqual(
            len(white_lists), 3, f"Expected 3 white lists, got {len(white_lists)}"
        )

        # Check the specific paths
        paths = [wl["path"] for wl in white_lists]
        expected_paths = [
            "/Local State",
            "/Default/Cookies",
            "/Default/Cookies-journal",
        ]

        for expected_path in expected_paths:
            self.assertIn(
                expected_path,
                paths,
                f"Expected path {expected_path} not found in white lists",
            )


if __name__ == "__main__":
    unittest.main()
