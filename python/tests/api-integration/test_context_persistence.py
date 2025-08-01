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
    random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"persistent-context-{timestamp}-{random_str}"

class TestContextPersistence(unittest.TestCase):
    """
    Context Data Persistence Integration Tests

    This test suite covers context data persistence functionality including:
    1. Same API Key and Context Data Sharing
    2. Data persistence between sessions with same apikey and contextId
    3. Context status verification
    4. File persistence across sessions
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
        self.session1 = None
        self.session2 = None
        self.session3 = None
        self.context_id = None
        self.context_object = None

    def tearDown(self):
        """Clean up after each test."""
        # Clean up sessions
        for session in [self.session1, self.session2, self.session3]:
            if session:
                try:
                    self.agent_bay.delete(session, True)
                except Exception as e:
                    print(f"Error deleting session: {e}")

        # Clean up context
        if self.context_object:
            try:
                delete_result = self.agent_bay.context.delete(self.context_object)
                if not delete_result.success:
                    print(f"Warning: Failed to delete context: {delete_result.error_message}")
            except Exception as e:
                print(f"Error deleting context: {e}")

    def test_4_1_same_api_key_context_data_sharing(self):
        """4.1 Same API Key and Context Data Sharing - should verify data persistence between sessions"""
        # Step 1.1.1: Environment preparation
        self.assertIsNotNone(self.agent_bay)
        print('Step 1.1.1: AgentBay instance created successfully')

        # Step 1.1.2: Context creation
        context_manager = self.agent_bay.context
        context_name = generate_random_context_name()
        create_result = context_manager.create(context_name)
        self.assertTrue(create_result.success)
        print(f'Step 1.1.2: Context created with name: {context_name}')

        context_result = context_manager.get(context_name)
        self.assertTrue(context_result.success)
        self.assertIsNotNone(context_result.context)
        self.context_id = context_result.context_id
        self.context_object = context_result.context
        print(f'Step 1.1.2: Got contextId: {self.context_id}')

        # Step 1.1.3: Context status check
        context_list = context_manager.list()
        created_context = next((ctx for ctx in context_list.contexts if ctx.id == self.context_id), None)
        self.assertIsNotNone(created_context)
        self.assertEqual(created_context.state, 'available')
        print(f'Step 1.1.3: Context status verified as available, contextId: {self.context_id}')

        # Step 1.1.4: First session creation
        context_sync1 = ContextSync.new(
            self.context_id,
            '/tmp/shared_data',
            SyncPolicy.default()
        )

        session_params1 = CreateSessionParams()
        session_params1.image_id = 'linux_latest'
        session_params1.context_syncs = [context_sync1]

        session_result1 = self.agent_bay.create(session_params1)
        self.assertTrue(session_result1.success)
        self.session1 = session_result1.session
        print('Step 1.1.4: First session created successfully')

        # Step 1.1.5: Context status update check
        updated_context_list = context_manager.list()
        in_use_context = next((ctx for ctx in updated_context_list.contexts if ctx.id == self.context_id), None)
        self.assertIsNotNone(in_use_context)
        print(f'Step 1.1.5: Context status checked, current state: {in_use_context.state}')

        # Step 1.1.6: File creation
        file_path = '/tmp/shared_data/persistent_file.txt'
        create_file_command = 'echo "Data from first session" > /tmp/shared_data/persistent_file.txt'
        create_file_result = self.session1.command.execute_command(create_file_command)
        self.assertTrue(create_file_result.success)
        print(f'Step 1.1.6: File created successfully at {file_path}')

        # Step 1.1.7: File content validation
        file_content = self.session1.file_system.read_file(file_path)
        self.assertEqual(file_content.content.strip(), 'Data from first session')
        print('Step 1.1.7: File content verified successfully')

        # Step 1.1.8: Session deletion with sync_context=True
        delete_result = self.agent_bay.delete(self.session1, True)
        self.assertTrue(delete_result.success)
        self.session1 = None  # Mark as deleted
        print('Step 1.1.8: Session deleted successfully with sync_context=True')

        # Step 1.1.9: Create two new sessions with same contextId
        context_sync2 = ContextSync.new(
            self.context_id,
            '/tmp/shared_data',
            SyncPolicy.default()
        )

        context_sync3 = ContextSync.new(
            self.context_id,
            '/tmp/shared_data',
            SyncPolicy.default()
        )

        session_params2 = CreateSessionParams()
        session_params2.image_id = 'linux_latest'
        session_params2.context_syncs = [context_sync2]

        session_params3 = CreateSessionParams()
        session_params3.image_id = 'linux_latest'
        session_params3.context_syncs = [context_sync3]

        session_result2 = self.agent_bay.create(session_params2)
        session_result3 = self.agent_bay.create(session_params3)

        self.assertTrue(session_result2.success)
        self.assertTrue(session_result3.success)

        self.session2 = session_result2.session
        self.session3 = session_result3.session
        print('Step 1.1.9: Two new sessions created successfully with same contextId')

        # Step 1.2.0: Wait for 20 seconds
        print('Step 1.2.0: Waiting for 20 seconds...')
        time.sleep(20)
        print('Step 1.2.0: Wait completed')

        # Step 1.2.0: Data persistence verification
        # Check with second session
        list_command1 = 'ls -la /tmp/shared_data/'
        list_result1 = self.session2.command.execute_command(list_command1)
        self.assertTrue(list_result1.success)
        self.assertIn('persistent_file.txt', list_result1.output)
        print('Step 1.2.0: Directory listing from session2:', list_result1.output)

        # Check with third session
        list_command2 = 'ls -la /tmp/shared_data/'
        list_result2 = self.session3.command.execute_command(list_command2)
        self.assertTrue(list_result2.success)
        self.assertIn('persistent_file.txt', list_result2.output)
        print('Step 1.2.0: Directory listing from session3:', list_result2.output)

        # Try to read the persistent file from both sessions
        try:
            persistent_content1 = self.session2.file_system.read_file(file_path)
            self.assertEqual(persistent_content1.content.strip(), 'Data from first session')
            print('Step 1.2.0: File content successfully read from session2')
        except Exception as error:
            print('Step 1.2.0: Failed to read file from session2:', error)

        try:
            persistent_content2 = self.session3.file_system.read_file(file_path)
            self.assertEqual(persistent_content2.content.strip(), 'Data from first session')
            print('Step 1.2.0: File content successfully read from session3')
        except Exception as error:
            print('Step 1.2.0: Failed to read file from session3:', error)

        print('Step 1.2.1: Data persistence test completed successfully')

if __name__ == "__main__":
    unittest.main()
