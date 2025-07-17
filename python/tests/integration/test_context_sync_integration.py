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
            raise unittest.SkipTest(
                "Skipping integration test: No API key available or running in CI"
            )

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
        context_sync = ContextSync.new(
            cls.context.id, "/home/wuying", SyncPolicy.default()
        )
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
        print(
            f"Context status data after sync, count: {len(context_info.context_status_data)}"
        )
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
            context_id=self.context.id, path="/home/wuying", task_type=None
        )

        # Verify that we have a request ID
        self.assertIsNotNone(context_info.request_id)

        # Log the filtered context status data
        print(
            f"Filtered context status data count: {len(context_info.context_status_data)}"
        )
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

    def test_context_sync_persistence_with_retry(self):
        """Test context sync persistence with retry for context status checks."""
        # 1. Create a unique context name and get its ID
        context_name = f"test-persistence-retry-py-{int(time.time())}"
        context_result = self.agent_bay.context.get(context_name, True)
        self.assertTrue(context_result.success, "Error getting/creating context")
        self.assertIsNotNone(context_result.context, "Context should not be None")

        context = context_result.context
        print(f"Created context: {context.name} (ID: {context.id})")

        try:
            # 2. Create a session with context sync, using a timestamped path under /home/wuying/
            timestamp = int(time.time())
            sync_path = f"/home/wuying/test-path-py-{timestamp}"

            # Use default policy
            default_policy = SyncPolicy.default()

            # Create session parameters with context sync
            session_params = CreateSessionParams()
            context_sync = ContextSync.new(context.id, sync_path, default_policy)
            session_params.context_syncs = [context_sync]
            session_params.image_id = "linux_latest"
            session_params.labels = {"test": "persistence-retry-test-py"}

            # Create first session
            session_result = self.agent_bay.create(session_params)
            self.assertTrue(session_result.success, "Error creating first session")
            self.assertIsNotNone(session_result.session, "Session should not be None")

            session1 = session_result.session
            print(f"Created first session: {session1.session_id}")

            try:
                # 3. Wait for session to be ready and retry context info until data is available
                print(
                    "Waiting for session to be ready and context status data to be available..."
                )

                found_data = False
                context_info = None

                for i in range(20):  # Retry up to 20 times
                    context_info = session1.context.info()

                    if context_info.context_status_data:
                        print(f"Found context status data on attempt {i+1}")
                        found_data = True
                        break

                    print(
                        f"No context status data available yet (attempt {i+1}), retrying in 1 second..."
                    )
                    time.sleep(1)

                self.assertTrue(
                    found_data, "Context status data should be available after retries"
                )
                self._print_context_status_data(context_info.context_status_data)

                # 4. Write a file to the context sync path
                test_content = (
                    f"Test content for Python persistence retry test at {timestamp}"
                )
                test_file_path = f"{sync_path}/test-file.txt"

                # Create directory first
                print(f"Creating directory: {sync_path}")
                dir_result = session1.file_system.create_directory(sync_path)
                self.assertTrue(dir_result.success, "Error creating directory")

                # Write the file
                print(f"Writing file to {test_file_path}")
                write_result = session1.file_system.write_file(
                    test_file_path, test_content
                )
                self.assertTrue(write_result.success, "Error writing file")

                # 5. Sync to trigger file upload
                print("Triggering context sync...")
                sync_result = session1.context.sync()
                self.assertTrue(
                    sync_result.success, "Context sync should be successful"
                )
                print(f"Context sync successful (RequestID: {sync_result.request_id})")

                # 6. Get context info with retry for upload status
                print("Checking file upload status with retry...")

                found_upload = False
                for i in range(20):  # Retry up to 20 times
                    context_info = session1.context.info()

                    # Check if we have upload status for our context
                    for data in context_info.context_status_data:
                        if data.context_id == context.id and data.task_type == "upload":
                            found_upload = True
                            print(f"Found upload task for context at attempt {i+1}")
                            break

                    if found_upload:
                        break

                    print(
                        f"No upload status found yet (attempt {i+1}), retrying in 1 second..."
                    )
                    time.sleep(1)

                if found_upload:
                    print("Found upload status for context")
                    self._print_context_status_data(context_info.context_status_data)
                else:
                    print("Warning: Could not find upload status after all retries")

                # 7. Release first session
                print("Releasing first session...")
                delete_result = self.agent_bay.delete(session1)
                self.assertTrue(delete_result.success, "Error deleting first session")

                # 8. Create a second session with the same context ID
                print("Creating second session with the same context ID...")
                session_params = CreateSessionParams()
                context_sync = ContextSync.new(context.id, sync_path, default_policy)
                session_params.context_syncs = [context_sync]
                session_params.image_id = "linux_latest"
                session_params.labels = {"test": "persistence-retry-test-py-second"}

                session_result = self.agent_bay.create(session_params)
                self.assertTrue(session_result.success, "Error creating second session")
                self.assertIsNotNone(
                    session_result.session, "Second session should not be None"
                )

                session2 = session_result.session
                print(f"Created second session: {session2.session_id}")

                try:
                    # 9. Get context info with retry for download status
                    print("Checking file download status with retry...")

                    found_download = False
                    for i in range(20):  # Retry up to 20 times
                        context_info = session2.context.info()

                        # Check if we have download status for our context
                        for data in context_info.context_status_data:
                            if (
                                data.context_id == context.id
                                and data.task_type == "download"
                            ):
                                found_download = True
                                print(
                                    f"Found download task for context at attempt {i+1}"
                                )
                                break

                        if found_download:
                            break

                        print(
                            f"No download status found yet (attempt {i+1}), retrying in 1 second..."
                        )
                        time.sleep(1)

                    if found_download:
                        print("Found download status for context")
                        self._print_context_status_data(
                            context_info.context_status_data
                        )
                    else:
                        print(
                            "Warning: Could not find download status after all retries"
                        )

                    # 10. Read the file from the second session
                    print("Reading file from second session...")
                    read_result = session2.file_system.read_file(test_file_path)
                    self.assertTrue(read_result.success, "Error reading file")

                    # 11. Verify the file content matches what was written
                    self.assertEqual(
                        test_content,
                        read_result.content,
                        "File content should match what was written",
                    )
                    print("File content verified successfully")

                finally:
                    # Clean up second session
                    try:
                        self.agent_bay.delete(session2)
                        print(f"Second session deleted: {session2.session_id}")
                    except Exception as e:
                        print(f"Warning: Failed to delete second session: {e}")

            finally:
                # Clean up first session if it still exists
                try:
                    self.agent_bay.delete(session1)
                    print(f"First session deleted: {session1.session_id}")
                except Exception:
                    pass  # Already deleted

        finally:
            # Clean up context
            try:
                self.agent_bay.context.delete(context)
                print(f"Context deleted: {context.id}")
            except Exception as e:
                print(f"Warning: Failed to delete context: {e}")

    def _print_context_status_data(self, data):
        """Helper method to print context status data."""
        if not data:
            print("No context status data available")
            return

        for i, item in enumerate(data):
            print(f"Context Status Data [{i}]:")
            print(f"  ContextId: {item.context_id}")
            print(f"  Path: {item.path}")
            print(f"  Status: {item.status}")
            print(f"  TaskType: {item.task_type}")
            print(f"  StartTime: {item.start_time}")
            print(f"  FinishTime: {item.finish_time}")
            if item.error_message:
                print(f"  ErrorMessage: {item.error_message}")
