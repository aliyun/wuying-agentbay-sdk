import unittest

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


if __name__ == "__main__":
    unittest.main() 