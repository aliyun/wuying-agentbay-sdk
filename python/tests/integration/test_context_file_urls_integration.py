import os
import time
import unittest

from agentbay import AgentBay


class TestContextFileUrlsIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        api_key = os.environ.get("AGENTBAY_API_KEY")
        if not api_key or os.environ.get("CI"):
            raise unittest.SkipTest(
                "Skipping integration test: No API key available or running in CI"
            )
        cls.agent_bay = AgentBay(api_key)

        # Create a test context
        cls.context_name = f"test-file-url-py-{int(time.time())}"
        context_result = cls.agent_bay.context.create(cls.context_name)
        if not context_result.success or not context_result.context:
            raise unittest.SkipTest("Failed to create context for file URL test")
        cls.context = context_result.context
        print(f"Created context: {cls.context.name} (ID: {cls.context.id})")

    @classmethod
    def tearDownClass(cls):
        # Clean up created context
        if hasattr(cls, "context"):
            try:
                cls.agent_bay.context.delete(cls.context)
                print(f"Deleted context: {cls.context.name} (ID: {cls.context.id})")
            except Exception as e:
                print(f"Warning: Failed to delete context {cls.context.name}: {e}")

    def test_get_file_upload_url(self):
        """
        Create a context and request a presigned upload URL for a test path.
        Validate that a URL is returned.
        """
        test_path = "/tmp/integration_upload_test.txt"
        result = self.agent_bay.context.get_file_upload_url(self.context.id, test_path)

        self.assertTrue(result.request_id is not None and isinstance(result.request_id, str))
        self.assertTrue(result.success, "get_file_upload_url should be successful")
        self.assertTrue(isinstance(result.url, str) and len(result.url) > 0, "URL should be non-empty")
        # Expire time may be optional depending on backend; if present, should be int-like
        if result.expire_time is not None:
            self.assertTrue(isinstance(result.expire_time, int))

        print(f"Upload URL: {result.url[:80]}... (RequestID: {result.request_id})") 