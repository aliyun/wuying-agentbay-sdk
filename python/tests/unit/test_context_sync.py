import unittest
import json

from agentbay import AgentBay

from agentbay.context_sync import (
    BWList,
    ContextSync,
    DeletePolicy,
    DownloadPolicy,
    DownloadStrategy,
    SyncPolicy,
    UploadPolicy,
    UploadStrategy,
    WhiteList,
)


class TestContextSync(unittest.TestCase):
    def test_initialization(self):
        context_sync = ContextSync.new("test-context", "/test/path")
        self.assertEqual(context_sync.context_id, "test-context")
        self.assertEqual(context_sync.path, "/test/path")
        self.assertIsNone(context_sync.policy)

    def test_new_with_policy(self):
        sync_policy = SyncPolicy.default()
        context_sync = ContextSync.new("test-context", "/test/path", sync_policy)
        self.assertEqual(context_sync.context_id, "test-context")
        self.assertEqual(context_sync.path, "/test/path")
        self.assertIs(context_sync.policy, sync_policy)

    def test_with_policy(self):
        context_sync = ContextSync.new("test-context", "/test/path")
        sync_policy = SyncPolicy.default()
        result = context_sync.with_policy(sync_policy)
        self.assertIs(result, context_sync)
        self.assertIs(context_sync.policy, sync_policy)

    def test_default_sync_policy_construction(self):
        """Test that default SyncPolicy matches the required structure"""
        policy = SyncPolicy.default()

        # Verify the policy is not None
        self.assertIsNotNone(policy)

        # Verify uploadPolicy
        self.assertIsNotNone(policy.upload_policy)
        upload_policy = policy.upload_policy
        assert upload_policy is not None  # type: ignore
        self.assertTrue(upload_policy.auto_upload)
        self.assertEqual(
            upload_policy.upload_strategy, UploadStrategy.UPLOAD_BEFORE_RESOURCE_RELEASE
        )
        self.assertEqual(upload_policy.period, 30)

        # Verify downloadPolicy
        self.assertIsNotNone(policy.download_policy)
        download_policy = policy.download_policy
        assert download_policy is not None  # type: ignore
        self.assertTrue(download_policy.auto_download)
        self.assertEqual(
            download_policy.download_strategy, DownloadStrategy.DOWNLOAD_ASYNC
        )

        # Verify deletePolicy
        self.assertIsNotNone(policy.delete_policy)
        delete_policy = policy.delete_policy
        assert delete_policy is not None  # type: ignore
        self.assertTrue(delete_policy.sync_local_file)

        # Verify bwList
        self.assertIsNotNone(policy.bw_list)
        bw_list = policy.bw_list
        assert bw_list is not None  # type: ignore
        self.assertIsNotNone(bw_list.white_lists)
        self.assertEqual(len(bw_list.white_lists), 1)

        white_list = bw_list.white_lists[0]
        self.assertEqual(white_list.path, "")
        self.assertIsNotNone(white_list.exclude_paths)
        self.assertEqual(len(white_list.exclude_paths), 0)

    def test_default_sync_policy_json_structure(self):
        """Test that default SyncPolicy JSON structure matches requirements"""
        policy = SyncPolicy.default()

        # Convert to JSON and verify structure
        # First convert to dict using dataclass asdict or manual conversion
        assert policy.upload_policy is not None  # type: ignore
        assert policy.download_policy is not None  # type: ignore
        assert policy.delete_policy is not None  # type: ignore
        assert policy.bw_list is not None  # type: ignore

        policy_dict = {
            "uploadPolicy": {
                "autoUpload": policy.upload_policy.auto_upload,
                "uploadStrategy": policy.upload_policy.upload_strategy.value,
                "period": policy.upload_policy.period,
            },
            "downloadPolicy": {
                "autoDownload": policy.download_policy.auto_download,
                "downloadStrategy": policy.download_policy.download_strategy.value,
            },
            "deletePolicy": {"syncLocalFile": policy.delete_policy.sync_local_file},
            "bwList": {
                "whiteLists": [
                    {
                        "path": policy.bw_list.white_lists[0].path,
                        "excludePaths": policy.bw_list.white_lists[0].exclude_paths,
                    }
                ]
            },
        }

        json_string = json.dumps(policy_dict)
        json_object = json.loads(json_string)

        # Verify uploadPolicy in JSON
        self.assertIn("uploadPolicy", json_object)
        self.assertTrue(json_object["uploadPolicy"]["autoUpload"])
        self.assertEqual(
            json_object["uploadPolicy"]["uploadStrategy"], "UploadBeforeResourceRelease"
        )
        self.assertEqual(json_object["uploadPolicy"]["period"], 30)

        # Verify downloadPolicy in JSON
        self.assertIn("downloadPolicy", json_object)
        self.assertTrue(json_object["downloadPolicy"]["autoDownload"])
        self.assertEqual(
            json_object["downloadPolicy"]["downloadStrategy"], "DownloadAsync"
        )

        # Verify deletePolicy in JSON
        self.assertIn("deletePolicy", json_object)
        self.assertTrue(json_object["deletePolicy"]["syncLocalFile"])

        # Verify bwList in JSON
        self.assertIn("bwList", json_object)
        self.assertIn("whiteLists", json_object["bwList"])
        self.assertEqual(len(json_object["bwList"]["whiteLists"]), 1)
        self.assertEqual(json_object["bwList"]["whiteLists"][0]["path"], "")
        self.assertIn("excludePaths", json_object["bwList"]["whiteLists"][0])
        self.assertEqual(len(json_object["bwList"]["whiteLists"][0]["excludePaths"]), 0)

        # Verify syncPaths should not exist in JSON
        self.assertNotIn("syncPaths", json_object)

        # Log the generated JSON for verification
        print(f"Generated JSON: {json_string}")

    def test_individual_policy_components_defaults(self):
        """Test individual policy components with default values"""
        # Test UploadPolicy defaults
        upload_policy = UploadPolicy.default()
        self.assertTrue(upload_policy.auto_upload)
        self.assertEqual(
            upload_policy.upload_strategy, UploadStrategy.UPLOAD_BEFORE_RESOURCE_RELEASE
        )
        self.assertEqual(upload_policy.period, 30)

        # Test DownloadPolicy defaults
        download_policy = DownloadPolicy.default()
        self.assertTrue(download_policy.auto_download)
        self.assertEqual(
            download_policy.download_strategy, DownloadStrategy.DOWNLOAD_ASYNC
        )

        # Test DeletePolicy defaults
        delete_policy = DeletePolicy.default()
        self.assertTrue(delete_policy.sync_local_file)

    def test_context_sync_with_default_policy(self):
        """Test creating ContextSync with default policy"""
        context_id = "test-context-123"
        path = "/test/path"
        policy = SyncPolicy.default()

        context_sync = ContextSync.new(context_id, path, policy)

        self.assertEqual(context_sync.context_id, context_id)
        self.assertEqual(context_sync.path, path)
        self.assertIs(context_sync.policy, policy)

    def test_white_list_default_construction(self):
        """Test WhiteList default construction"""
        white_list = WhiteList()
        self.assertEqual(white_list.path, "")
        self.assertEqual(len(white_list.exclude_paths), 0)

    def test_bw_list_default_construction(self):
        """Test BWList default construction"""
        bw_list = BWList()
        self.assertEqual(len(bw_list.white_lists), 0)

        # Test BWList with default white list
        bw_list_with_default = BWList(white_lists=[WhiteList()])
        self.assertEqual(len(bw_list_with_default.white_lists), 1)
        self.assertEqual(bw_list_with_default.white_lists[0].path, "")


if __name__ == "__main__":
    unittest.main()
