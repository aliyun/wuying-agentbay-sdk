import os
import unittest
import time

from agentbay import AgentBay
from agentbay.session_params import CreateSessionParams
from agentbay.context_sync import (
    ContextSync,
    SyncPolicy,
    UploadPolicy,
    DownloadPolicy,
    DeletePolicy,
    BWList,
    WhiteList
)

def generate_random_context_name():
    """Helper function to generate random context name"""
    import time
    import random
    import string
    timestamp = int(time.time() * 1000)
    random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"test-context-{timestamp}-{random_str}"

class TestContextSync(unittest.TestCase):
    """
    Context Sync Integration Tests

    This test suite covers context sync functionality including:
    1. Single Session Context Sync Upload/Download
    2. Two SyncContext Sessions Creation
    3. Same ContextId Two Sessions Creation
    """

    @classmethod
    def setUpClass(cls):
        """Set up test environment before all tests."""
        # Get API key from environment
        cls.api_key = os.getenv("AGENTBAY_API_KEY")
        if not cls.api_key:
            raise unittest.SkipTest("AGENTBAY_API_KEY environment variable not set")

        # Initialize AgentBay client
        cls.agent_bay = AgentBay(cls.api_key)

    @classmethod
    def tearDownClass(cls):
        """Clean up test environment after all tests."""
        pass

    def setUp(self):
        """Set up before each test."""
        self.session = None
        self.session1 = None
        self.session2 = None
        self.context_objects = []  # Store context objects for deletion

    def tearDown(self):
        """Clean up after each test."""
        # Clean up sessions
        for session in [self.session, self.session1, self.session2]:
            if session:
                try:
                    self.agent_bay.delete(session, True)
                except Exception as e:
                    print(f"Error deleting session: {e}")

        # Clean up contexts
        for context_obj in self.context_objects:
            try:
                delete_result = self.agent_bay.context.delete(context_obj)
                if not delete_result.success:
                    print(f"Warning: Failed to delete context: {delete_result.error_message}")
            except Exception as e:
                print(f"Error deleting context: {e}")

        self.context_objects.clear()

    def test_1_1_single_session_context_sync_upload_download(self):
        """1.1 Single Session Context Sync Upload/Download - should complete single session context sync workflow"""
        # Step 1: Environment preparation
        self.assertIsNotNone(self.agent_bay)

        # Step 2: Get context manager
        context_manager = self.agent_bay.context
        self.assertIsNotNone(context_manager)

        # Step 3: Context query and creation
        existing_contexts = context_manager.list()
        available_context = next((ctx for ctx in existing_contexts.contexts if ctx.state == 'available'), None)

        if available_context:
            context_id = available_context.id
            context_object = available_context
        else:
            context_name = generate_random_context_name()
            create_result = context_manager.create(context_name)
            self.assertTrue(create_result.success)

            created_context_result = context_manager.get(context_name)
            self.assertTrue(created_context_result.success)
            self.assertIsNotNone(created_context_result.context)
            context_id = created_context_result.context_id
            context_object = created_context_result.context

        self.context_objects.append(context_object)
        self.assertIsNotNone(context_id)
        self.assertNotEqual(context_id, '')

        # Step 4: Session creation with context sync
        upload_policy = UploadPolicy()
        download_policy = DownloadPolicy()
        delete_policy = DeletePolicy()

        sync_policy = SyncPolicy()
        sync_policy.upload_policy = upload_policy
        sync_policy.download_policy = download_policy
        sync_policy.delete_policy = delete_policy

        white_list = WhiteList()
        white_list.path = '/tmp/user'
        white_list.exclude_paths = ['/tmp/user/excluded']

        bw_list = BWList()
        bw_list.white_lists = [white_list]

        context_sync = ContextSync.new(
            context_id,
            '/tmp/user',
            sync_policy
        )

        create_params = CreateSessionParams()
        create_params.image_id = 'linux_latest'
        create_params.labels = {
            'test': 'sync_context',
            'timestamp': str(int(time.time() * 1000))
        }
        create_params.context_syncs = [context_sync]

        session_result = self.agent_bay.create(create_params)
        self.assertTrue(session_result.success)
        self.assertIsNotNone(session_result.session)

        self.session = session_result.session
        self.assertIsNotNone(self.session.get_session_id())
        self.assertNotEqual(self.session.get_session_id(), '')

        # Step 5: Labels verification
        labels_result = self.session.get_labels()
        self.assertTrue(labels_result.success)
        self.assertEqual(labels_result.data['test'], 'sync_context')
        self.assertIsNotNone(labels_result.data['timestamp'])

        # Step 6: Context manager retrieval
        session_context_manager = self.session.context
        self.assertIsNotNone(session_context_manager)
        session_context_info = session_context_manager.info()

        context_status_data_info = session_context_info.context_status_data
        self.assertIsNotNone(context_status_data_info)
        self.assertGreater(len(context_status_data_info), 0)
        session_status_data_item = context_status_data_info[0]
        self.assertEqual(session_status_data_item.context_id, context_id)

        # Step 7: Sync operation
        sync_result = session_context_manager.sync()
        self.assertTrue(sync_result.success)

        # Step 8: Sync info query
        context_status_data = session_context_manager.info()
        self.assertIsNotNone(context_status_data)
        print('Context Status Data:', context_status_data)

        # Step 9: Session info retrieval
        api_key = self.session.get_api_key()
        session_id = self.session.get_session_id()
        self.assertIsNotNone(api_key)
        self.assertIsNotNone(session_id)

        # Step 10: Labels re-verification
        verify_labels_result = self.session.get_labels()
        self.assertTrue(verify_labels_result.success)
        self.assertEqual(verify_labels_result.data['test'], 'sync_context')

        # Step 11: Session info query
        session_info = self.session.info()
        self.assertTrue(session_info.success)

        # Step 12: Labels update
        new_labels = {
            'test': 'updated_sync_context',
            'version': 'v2'
        }
        set_labels_result = self.session.set_labels(new_labels)
        self.assertTrue(set_labels_result.success)

        # Step 13: Updated labels verification
        updated_labels_result = self.session.get_labels()
        self.assertTrue(updated_labels_result.success)
        self.assertEqual(updated_labels_result.data['test'], 'updated_sync_context')
        self.assertEqual(updated_labels_result.data['version'], 'v2')

    def test_1_2_two_sync_context_sessions_creation(self):
        """1.2 Two SyncContext Sessions Creation - should create two sessions with different context sync configurations"""
        # Step 1: Environment preparation
        self.assertIsNotNone(self.agent_bay)

        # Step 2: Get context manager
        context_manager = self.agent_bay.context
        self.assertIsNotNone(context_manager)

        # Step 3: Create two contexts
        context_name1 = generate_random_context_name()
        context_name2 = generate_random_context_name()

        create_result1 = context_manager.create(context_name1)
        create_result2 = context_manager.create(context_name2)

        self.assertTrue(create_result1.success)
        self.assertTrue(create_result2.success)

        # Step 4: Get context instances
        context_result1 = context_manager.get(context_name1)
        context_result2 = context_manager.get(context_name2)

        self.assertTrue(context_result1.success)
        self.assertTrue(context_result2.success)
        self.assertIsNotNone(context_result1.context)
        self.assertIsNotNone(context_result2.context)

        context_id1 = context_result1.context_id
        context_id2 = context_result2.context_id
        context_object1 = context_result1.context
        context_object2 = context_result2.context

        self.context_objects.extend([context_object1, context_object2])
        self.assertNotEqual(context_id1, context_id2)

        # Step 5: Create two sessions
        context_sync1 = ContextSync.new(
            context_id1,
            '/tmp/user1',
            SyncPolicy.default()
        )

        context_sync2 = ContextSync.new(
            context_id2,
            '/tmp/user2',
            SyncPolicy.default()
        )

        session_params1 = CreateSessionParams()
        session_params1.image_id = 'linux_latest'
        session_params1.context_syncs = [context_sync1]

        session_params2 = CreateSessionParams()
        session_params2.image_id = 'linux_latest'
        session_params2.context_syncs = [context_sync2]

        session_result1 = self.agent_bay.create(session_params1)
        session_result2 = self.agent_bay.create(session_params2)

        self.assertTrue(session_result1.success)
        self.assertTrue(session_result2.success)

        self.session1 = session_result1.session
        self.session2 = session_result2.session

        self.assertNotEqual(self.session1.get_session_id(), self.session2.get_session_id())

        # Step 6: Sync status query
        context_status1 = self.session1.context.info()
        context_status2 = self.session2.context.info()

        self.assertIsNotNone(context_status1)
        self.assertIsNotNone(context_status2)
        print('Session1 Context Status:', context_status1)
        print('Session2 Context Status:', context_status2)

        # Step 7: Concurrent sync test
        sync_result1 = self.session1.context.sync()
        sync_result2 = self.session2.context.sync()

        self.assertTrue(sync_result1.success)
        self.assertTrue(sync_result2.success)

        # Step 8: Concurrent sync verification
        verify_status1 = self.session1.context.info()
        verify_status2 = self.session2.context.info()

        self.assertIsNotNone(verify_status1)
        self.assertIsNotNone(verify_status2)

    def test_1_3_same_context_id_two_sessions_creation(self):
        """1.3 Same ContextId Two Sessions Creation - should create two sessions using the same contextId"""
        # Step 1: Environment preparation
        self.assertIsNotNone(self.agent_bay)

        # Step 2: Get context manager
        context_manager = self.agent_bay.context
        self.assertIsNotNone(context_manager)

        # Step 3: Create single context
        context_name = generate_random_context_name()
        create_result = context_manager.create(context_name)
        self.assertTrue(create_result.success)

        context_result = context_manager.get(context_name)
        self.assertTrue(context_result.success)
        self.assertIsNotNone(context_result.context)
        context_id = context_result.context_id
        context_object = context_result.context
        self.context_objects.append(context_object)

        # Step 4: Create two sessions with same contextId but different paths
        context_sync1 = ContextSync.new(
            context_id,
            '/tmp/path1',
            SyncPolicy.default()
        )

        context_sync2 = ContextSync.new(
            context_id,
            '/tmp/path2',
            SyncPolicy.default()
        )

        session_params1 = CreateSessionParams()
        session_params1.image_id = 'linux_latest'
        session_params1.context_syncs = [context_sync1]

        session_params2 = CreateSessionParams()
        session_params2.image_id = 'linux_latest'
        session_params2.context_syncs = [context_sync2]

        session_result1 = self.agent_bay.create(session_params1)
        session_result2 = self.agent_bay.create(session_params2)

        self.assertTrue(session_result1.success)
        self.assertTrue(session_result2.success)

        self.session1 = session_result1.session
        self.session2 = session_result2.session

        # Step 5: Context sharing verification
        session_context_manager1 = self.session1.context
        self.assertIsNotNone(session_context_manager1)
        session_context_info1 = session_context_manager1.info()

        context_status_data_info1 = session_context_info1.context_status_data
        self.assertIsNotNone(context_status_data_info1)
        self.assertGreater(len(context_status_data_info1), 0)
        session1_context_id = context_status_data_info1[0].context_id

        session_context_manager2 = self.session2.context
        self.assertIsNotNone(session_context_manager2)
        session_context_info2 = session_context_manager2.info()

        context_status_data_info2 = session_context_info2.context_status_data
        self.assertIsNotNone(context_status_data_info2)
        self.assertGreater(len(context_status_data_info2), 0)
        session2_context_id = context_status_data_info2[0].context_id

        self.assertEqual(session1_context_id, context_id)
        self.assertEqual(session2_context_id, context_id)
        self.assertEqual(session1_context_id, session2_context_id)

        # Step 6: Independent path verification
        # Paths are configured independently in each session's context sync
        # This is verified by the different path configurations above

if __name__ == "__main__":
    unittest.main()
