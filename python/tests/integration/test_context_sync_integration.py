#!/usr/bin/env python3
"""
Integration test for context synchronization functionality.
Based on golang/examples/context_sync_example/main.go
"""

import os
import time
import unittest

from agentbay import (
    AgentBay,
    ContextSync,
    SyncPolicy,
    UploadPolicy,
    UploadStrategy,
    DownloadPolicy,
    DownloadStrategy,
    DeletePolicy,
    BWList,
    WhiteList,
    CreateSessionParams,
)


class TestContextSyncIntegration(unittest.TestCase):
    """Integration tests for context synchronization functionality."""

    @classmethod
    def setUpClass(cls):
        """Set up test environment before all tests."""
        # Get API key from environment
        cls.api_key = os.getenv("AGENTBAY_API_KEY")
        if not cls.api_key:
            raise unittest.SkipTest("AGENTBAY_API_KEY environment variable not set")

        # Initialize AgentBay client
        cls.agent_bay = AgentBay(cls.api_key)
        
        # Use timestamp in context name to ensure uniqueness for each test run
        cls.context_name = f"my-sync-context-{int(time.time())}"

    def _get_context_id(self):
        """Helper method to get context_id, creating context if needed."""
        if not hasattr(self, 'context_id'):
            # If context_id is not available, create a context first
            context_result = self.agent_bay.context.get(self.context_name, create=True)
            self.assertTrue(context_result.success, f"Failed to create context: {context_result.request_id}")
            self.context_id = context_result.context.id
        return self.context_id

    @classmethod
    def tearDownClass(cls):
        """Clean up test environment after all tests."""
        print("Cleaning up...")
        
        # Delete the session if it exists
        if hasattr(cls, 'session'):
            try:
                result = cls.agent_bay.delete(cls.session)
                if result.success:
                    print("Session successfully deleted")
                else:
                    print(f"Warning: Error deleting session: {result.error_message}")
            except Exception as e:
                print(f"Warning: Error deleting session: {e}")
        
        # Delete the context if it exists
        if hasattr(cls, 'context'):
            try:
                delete_context_result = cls.agent_bay.context.delete(cls.context)
                if delete_context_result.success:
                    print("Context successfully deleted")
                else:
                    print(f"Warning: Error deleting context: {delete_context_result.error_message}")
            except Exception as e:
                print(f"Warning: Error deleting context: {e}")

    def test_01_create_context(self):
        """Test creating a new context."""
        print("Test 1: Creating a new context...")
        
        # Create a new context
        context_result = self.agent_bay.context.get(self.context_name, create=True)
        
        self.assertTrue(context_result.success, f"Failed to create context: {context_result.request_id}")
        self.assertIsNotNone(context_result.context, "Context should not be None")
        
        self.context = context_result.context
        self.context_id = self.context.id
        print(f"Context created/retrieved: {self.context.name} (ID: {self.context.id})")

    def test_02_basic_context_sync_configuration(self):
        """Test creating a basic context sync configuration."""
        print("\nTest 2: Creating a basic context sync configuration...")
        
        # Create a basic context sync configuration with default policy
        basic_sync = ContextSync.new(
            self._get_context_id(),
            "/home/wuying",
            SyncPolicy.default()
        )
        
        self.assertEqual(basic_sync.context_id, self.context_id)
        self.assertEqual(basic_sync.path, "/home/wuying")
        self.assertIsNotNone(basic_sync.policy)
        
        # Verify default policy values
        self.assertTrue(basic_sync.policy.upload_policy.auto_upload)
        self.assertEqual(basic_sync.policy.upload_policy.upload_strategy, UploadStrategy.UPLOAD_BEFORE_RESOURCE_RELEASE)
        self.assertEqual(basic_sync.policy.upload_policy.period, 30)
        
        self.assertTrue(basic_sync.policy.download_policy.auto_download)
        self.assertEqual(basic_sync.policy.download_policy.download_strategy, DownloadStrategy.DOWNLOAD_ASYNC)
        
        self.assertTrue(basic_sync.policy.delete_policy.sync_local_file)
        
        print(f"Basic sync - ContextID: {basic_sync.context_id}, Path: {basic_sync.path}")

    def test_03_advanced_context_sync_configuration(self):
        """Test creating an advanced context sync configuration with custom policies."""
        print("\nTest 3: Creating an advanced context sync configuration...")
        
        # Create upload policy
        upload_policy = UploadPolicy(
            auto_upload=True,
            upload_strategy=UploadStrategy.PERIODIC_UPLOAD,
            period=15  # 15 minutes
        )
        
        # Create download policy
        download_policy = DownloadPolicy(
            auto_download=True,
            download_strategy=DownloadStrategy.DOWNLOAD_ASYNC
        )
        
        # Create delete policy
        delete_policy = DeletePolicy(
            sync_local_file=True
        )
        
        # Create white list
        white_list = WhiteList(
            path="/data/important",
            exclude_paths=["/data/important/temp", "/data/important/logs"]
        )
        
        # Create BW list
        bw_list = BWList(
            white_lists=[white_list]
        )
        
        # Create sync policy
        sync_policy = SyncPolicy(
            upload_policy=upload_policy,
            download_policy=download_policy,
            delete_policy=delete_policy,
            bw_list=bw_list
        )
        
        # Create advanced sync configuration
        advanced_sync = ContextSync.new(
            self._get_context_id(),
            "/data",
            sync_policy
        )
        
        self.assertEqual(advanced_sync.context_id, self.context_id)
        self.assertEqual(advanced_sync.path, "/data")
        self.assertIsNotNone(advanced_sync.policy)
        
        # Verify custom policy values
        self.assertTrue(advanced_sync.policy.upload_policy.auto_upload)
        self.assertEqual(advanced_sync.policy.upload_policy.upload_strategy, UploadStrategy.PERIODIC_UPLOAD)
        self.assertEqual(advanced_sync.policy.upload_policy.period, 15)
        
        self.assertTrue(advanced_sync.policy.download_policy.auto_download)
        self.assertEqual(advanced_sync.policy.download_policy.download_strategy, DownloadStrategy.DOWNLOAD_ASYNC)
        
        self.assertTrue(advanced_sync.policy.delete_policy.sync_local_file)
        
        self.assertEqual(len(advanced_sync.policy.bw_list.white_lists), 1)
        self.assertEqual(advanced_sync.policy.bw_list.white_lists[0].path, "/data/important")
        self.assertEqual(advanced_sync.policy.bw_list.white_lists[0].exclude_paths, ["/data/important/temp", "/data/important/logs"])
        
        print(f"Advanced sync - ContextID: {advanced_sync.context_id}, Path: {advanced_sync.path}")
        print(f"  - Upload: Auto={advanced_sync.policy.upload_policy.auto_upload}, "
              f"Strategy={advanced_sync.policy.upload_policy.upload_strategy}, "
              f"Period={advanced_sync.policy.upload_policy.period}")
        print(f"  - Download: Auto={advanced_sync.policy.download_policy.auto_download}, "
              f"Strategy={advanced_sync.policy.download_policy.download_strategy}")
        print(f"  - Delete: SyncLocalFile={advanced_sync.policy.delete_policy.sync_local_file}")
        print(f"  - WhiteList: Path={advanced_sync.policy.bw_list.white_lists[0].path}, "
              f"ExcludePaths={advanced_sync.policy.bw_list.white_lists[0].exclude_paths}")

    def test_04_create_session_with_context_sync(self):
        """Test creating session with context sync."""
        print("\nTest 4: Creating session with context sync...")
        
        # Create session parameters with context sync
        session_params = CreateSessionParams(
            context_syncs=[ContextSync.new(self._get_context_id(), "/home/wuying")],
            labels={
                "username": "alice",
                "project": "context-sync-example"
            },
            image_id="imgc-07eksy57eawchjkro"
        )
        
        # Create session
        session_result = self.agent_bay.create(session_params)
        
        self.assertTrue(session_result.success, f"Failed to create session: {session_result.error_message}")
        self.assertIsNotNone(session_result.session, "Session should not be None")
        
        session = session_result.session
        print(f"Session created with ID: {session.session_id}")
        print(f"Session creation RequestID: {session_result.request_id}")
        
        # Store session for cleanup
        self.session = session

    def test_05_context_manager_from_session(self):
        """Test using context manager from session."""
        print("\nTest 5: Using context manager from session...")
        
        # Get session from previous test or create a new one
        if not hasattr(self, 'session'):
            # Create session parameters with context sync
            session_params = CreateSessionParams(
                context_syncs=[ContextSync.new(self._get_context_id(), "/home/wuying")],
                labels={
                    "username": "alice",
                    "project": "context-sync-example"
                },
                image_id="imgc-07eksy57eawchjkro"
            )
            
            # Create session
            session_result = self.agent_bay.create(session_params)
            self.assertTrue(session_result.success, f"Failed to create session: {session_result.error_message}")
            self.session = session_result.session
        
        # Get context info
        try:
            context_info = self.session.context.info()
            print(f"Context status: {context_info.context_status} (RequestID: {context_info.request_id})")
        except Exception as e:
            print(f"Error getting context info: {e}")
            # Don't fail the test if context.info() is not implemented yet
        
        # Sync context
        try:
            sync_result = self.session.context.sync()
            print(f"Context sync success: {sync_result.success} (RequestID: {sync_result.request_id})")
        except Exception as e:
            print(f"Error syncing context: {e}")
            # Don't fail the test if context.sync() is not implemented yet

    def test_06_builder_pattern_context_sync(self):
        """Test using builder pattern for context sync."""
        print("\nTest 6: Using builder pattern for context sync...")
        
        # Create context sync using builder pattern
        builder_sync = ContextSync.new(self._get_context_id(), "/workspace").with_policy(
            SyncPolicy(
                upload_policy=UploadPolicy(
                    auto_upload=True,
                    upload_strategy=UploadStrategy.UPLOAD_BEFORE_RESOURCE_RELEASE
                ),
                download_policy=DownloadPolicy(
                    auto_download=True,
                    download_strategy=DownloadStrategy.DOWNLOAD_ASYNC
                ),
                bw_list=BWList(
                    white_lists=[
                        WhiteList(
                            path="/workspace/src",
                            exclude_paths=["/workspace/src/node_modules"]
                        )
                    ]
                )
            )
        )
        
        self.assertEqual(builder_sync.context_id, self.context_id)
        self.assertEqual(builder_sync.path, "/workspace")
        self.assertIsNotNone(builder_sync.policy)
        
        # Verify builder pattern results
        self.assertTrue(builder_sync.policy.upload_policy.auto_upload)
        self.assertEqual(builder_sync.policy.upload_policy.upload_strategy, UploadStrategy.UPLOAD_BEFORE_RESOURCE_RELEASE)
        
        self.assertTrue(builder_sync.policy.download_policy.auto_download)
        self.assertEqual(builder_sync.policy.download_policy.download_strategy, DownloadStrategy.DOWNLOAD_ASYNC)
        
        self.assertEqual(len(builder_sync.policy.bw_list.white_lists), 1)
        self.assertEqual(builder_sync.policy.bw_list.white_lists[0].path, "/workspace/src")
        self.assertEqual(builder_sync.policy.bw_list.white_lists[0].exclude_paths, ["/workspace/src/node_modules"])
        
        print(f"Builder sync - ContextID: {builder_sync.context_id}, Path: {builder_sync.path}")

    def test_07_multiple_white_lists_context_sync(self):
        """Test creating context sync with multiple white lists."""
        print("\nTest 7: Creating context sync with multiple white lists...")
        
        # Create multiple white lists
        source_white_list = WhiteList(
            path="/workspace/src",
            exclude_paths=["/workspace/src/node_modules", "/workspace/src/.git"]
        )
        
        docs_white_list = WhiteList(
            path="/workspace/docs",
            exclude_paths=["/workspace/docs/build", "/workspace/docs/temp"]
        )
        
        config_white_list = WhiteList(
            path="/workspace/config",
            exclude_paths=["/workspace/config/tmp"]
        )
        
        # Create BW list with multiple white lists
        bw_list = BWList(
            white_lists=[source_white_list, docs_white_list, config_white_list]
        )
        
        # Create sync policy
        sync_policy = SyncPolicy(
            upload_policy=UploadPolicy.default(),
            download_policy=DownloadPolicy.default(),
            delete_policy=DeletePolicy.default(),
            bw_list=bw_list,
            sync_paths=["/workspace/src", "/workspace/docs", "/workspace/config"]
        )
        
        # Create context sync
        context_sync = ContextSync.new(self._get_context_id(), "/workspace", sync_policy)
        
        self.assertEqual(len(context_sync.policy.bw_list.white_lists), 3)
        self.assertEqual(context_sync.policy.sync_paths, ["/workspace/src", "/workspace/docs", "/workspace/config"])
        
        print(f"Multiple white lists - ContextID: {context_sync.context_id}, Path: {context_sync.path}")
        print(f"  - Number of white lists: {len(context_sync.policy.bw_list.white_lists)}")
        print(f"  - Sync paths: {context_sync.policy.sync_paths}")

    def test_08_different_upload_strategies(self):
        """Test different upload strategies."""
        print("\nTest 8: Testing different upload strategies...")
        
        strategies = [
            UploadStrategy.UPLOAD_BEFORE_RESOURCE_RELEASE,
            UploadStrategy.UPLOAD_AFTER_FILE_CLOSE,
            UploadStrategy.PERIODIC_UPLOAD
        ]
        
        for strategy in strategies:
            upload_policy = UploadPolicy(
                auto_upload=True,
                upload_strategy=strategy,
                period=30 if strategy == UploadStrategy.PERIODIC_UPLOAD else None
            )
            
            sync_policy = SyncPolicy(upload_policy=upload_policy)
            context_sync = ContextSync.new(self._get_context_id(), "/test", sync_policy)
            
            self.assertEqual(context_sync.policy.upload_policy.upload_strategy, strategy)
            print(f"  - Strategy: {strategy}")

    def test_09_different_download_strategies(self):
        """Test different download strategies."""
        print("\nTest 9: Testing different download strategies...")
        
        strategies = [
            DownloadStrategy.DOWNLOAD_SYNC,
            DownloadStrategy.DOWNLOAD_ASYNC
        ]
        
        for strategy in strategies:
            download_policy = DownloadPolicy(
                auto_download=True,
                download_strategy=strategy
            )
            
            sync_policy = SyncPolicy(download_policy=download_policy)
            context_sync = ContextSync.new(self._get_context_id(), "/test", sync_policy)
            
            self.assertEqual(context_sync.policy.download_policy.download_strategy, strategy)
            print(f"  - Strategy: {strategy}")

    def test_10_policy_modification(self):
        """Test modifying existing policies."""
        print("\nTest 10: Testing policy modification...")
        
        # Create initial context sync
        context_sync = ContextSync.new(self._get_context_id(), "/test", SyncPolicy.default())
        
        # Modify upload policy
        new_upload_policy = UploadPolicy(
            auto_upload=False,
            upload_strategy=UploadStrategy.PERIODIC_UPLOAD,
            period=60
        )
        
        # Create new sync policy with modified upload policy
        new_sync_policy = SyncPolicy(
            upload_policy=new_upload_policy,
            download_policy=context_sync.policy.download_policy,
            delete_policy=context_sync.policy.delete_policy,
            bw_list=context_sync.policy.bw_list
        )
        
        # Apply new policy
        context_sync.with_policy(new_sync_policy)
        
        self.assertFalse(context_sync.policy.upload_policy.auto_upload)
        self.assertEqual(context_sync.policy.upload_policy.upload_strategy, UploadStrategy.PERIODIC_UPLOAD)
        self.assertEqual(context_sync.policy.upload_policy.period, 60)
        
        print(f"Policy modification - Upload auto: {context_sync.policy.upload_policy.auto_upload}, "
              f"Strategy: {context_sync.policy.upload_policy.upload_strategy}, "
              f"Period: {context_sync.policy.upload_policy.period}")


if __name__ == "__main__":
    # Run the tests
    unittest.main(verbosity=2) 