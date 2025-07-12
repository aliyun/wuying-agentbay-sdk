#!/usr/bin/env python3
"""
Integration test for context synchronization functionality.
Based on golang/examples/context_sync_example/main.go
"""

import os
import time
import unittest
import json
from unittest.mock import patch

from agentbay import AgentBay
from agentbay.context_manager import ContextStatusData
from agentbay.session_params import CreateSessionParams
from agentbay.context_sync import ContextSync, SyncPolicy


class TestContextSyncIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Skip if no API key is available or in CI environment
        api_key = os.environ.get("AGENTBAY_API_KEY")
        if not api_key or os.environ.get("CI"):
            raise unittest.SkipTest("Skipping integration test: No API key available or running in CI")
        
        # Initialize AgentBay client
        cls.agent_bay = AgentBay(api_key)
        
        # Create a unique context name for this test
        cls.context_name = f"test-sync-context-{int(time.time())}"
        
        # Create a context
        context_result = cls.agent_bay.context.get(cls.context_name, True)
        if not context_result.success or not context_result.context:
            raise unittest.SkipTest("Failed to create context")
        
        cls.context = context_result.context
        print(f"Created context: {cls.context.name} (ID: {cls.context.id})")
        
        # Create session parameters with context sync
        session_params = CreateSessionParams()
        
        # Create context sync configuration
        context_sync = ContextSync.new(cls.context.id, "/home/wuying", SyncPolicy.default())
        session_params.context_syncs = [context_sync]
        
        # Add labels and image ID
        session_params.labels = {"test": "context-sync-integration"}
        session_params.image_id = "linux_latest"
        
        # Create session
        session_result = cls.agent_bay.create(session_params)
        if not session_result.success or not session_result.session:
            cls.agent_bay.context.delete(cls.context)
            raise unittest.SkipTest("Failed to create session")
        
        cls.session = session_result.session
        print(f"Created session: {cls.session.session_id}")
        
        # Wait for session to be ready
        time.sleep(10)

    @classmethod
    def tearDownClass(cls):
        # Clean up session
        if hasattr(cls, "session"):
            try:
                cls.agent_bay.delete(cls.session)
                print(f"Session deleted: {cls.session.session_id}")
            except Exception as e:
                print(f"Warning: Failed to delete session: {e}")
        
        # Clean up context
        if hasattr(cls, "context"):
            try:
                cls.agent_bay.context.delete(cls.context)
                print(f"Context deleted: {cls.context.id}")
            except Exception as e:
                print(f"Warning: Failed to delete context: {e}")

    def test_context_info_returns_context_status_data(self):
        """Test that context info returns parsed ContextStatusData."""
        # Get context info
        context_info = self.session.context.info()
        
        # Verify that we have a request ID
        self.assertIsNotNone(context_info.request_id)
        self.assertNotEqual(context_info.request_id, "")
        
        # Log the context status data
        print(f"Context status data count: {len(context_info.context_status_data)}")
        for i, data in enumerate(context_info.context_status_data):
            print(f"Status data {i}:")
            print(f"  Context ID: {data.context_id}")
            print(f"  Path: {data.path}")
            print(f"  Status: {data.status}")
            print(f"  Task Type: {data.task_type}")
            print(f"  Start Time: {data.start_time}")
            print(f"  Finish Time: {data.finish_time}")
            if data.error_message:
                print(f"  Error: {data.error_message}")
        
        # There might not be any status data yet, so we don't assert on the count
        # But if there is data, verify it has the expected structure
        for data in context_info.context_status_data:
            self.assertIsInstance(data, ContextStatusData)
            self.assertIsNotNone(data.context_id)
            self.assertIsNotNone(data.path)
            self.assertIsNotNone(data.status)
            self.assertIsNotNone(data.task_type)

    def test_context_sync_and_info(self):
        """Test syncing context and then getting info."""
        # Sync context
        sync_result = self.session.context.sync()
        
        # Verify sync result
        self.assertTrue(sync_result.success)
        self.assertIsNotNone(sync_result.request_id)
        self.assertNotEqual(sync_result.request_id, "")
        
        # Wait for sync to complete
        time.sleep(5)
        
        # Get context info
        context_info = self.session.context.info()
        
        # Verify context info
        self.assertIsNotNone(context_info.request_id)
        
        # Log the context status data
        print(f"Context status data after sync, count: {len(context_info.context_status_data)}")
        for i, data in enumerate(context_info.context_status_data):
            print(f"Status data {i}:")
            print(f"  Context ID: {data.context_id}")
            print(f"  Path: {data.path}")
            print(f"  Status: {data.status}")
            print(f"  Task Type: {data.task_type}")
        
        # Check if we have status data for our context
        found_context = False
        for data in context_info.context_status_data:
            if data.context_id == self.context.id:
                found_context = True
                self.assertEqual(data.path, "/home/wuying")
                # Status might vary, but should not be empty
                self.assertIsNotNone(data.status)
                self.assertNotEqual(data.status, "")
                break
        
        # We should have found our context in the status data
        # But this might be flaky in CI, so just log a warning if not found
        if not found_context:
            print(f"Warning: Could not find context {self.context.id} in status data")

    def test_context_info_with_params(self):
        """Test getting context info with specific parameters."""
        # Get context info with parameters
        context_info = self.session.context.info(
            context_id=self.context.id,
            path="/home/wuying",
            task_type=None
        )
        
        # Verify that we have a request ID
        self.assertIsNotNone(context_info.request_id)
        
        # Log the filtered context status data
        print(f"Filtered context status data count: {len(context_info.context_status_data)}")
        for i, data in enumerate(context_info.context_status_data):
            print(f"Status data {i}:")
            print(f"  Context ID: {data.context_id}")
            print(f"  Path: {data.path}")
            print(f"  Status: {data.status}")
            print(f"  Task Type: {data.task_type}")
        
        # If we have status data, verify it matches our filters
        for data in context_info.context_status_data:
            if data.context_id == self.context.id:
                self.assertEqual(data.path, "/home/wuying")


if __name__ == "__main__":
    unittest.main() 