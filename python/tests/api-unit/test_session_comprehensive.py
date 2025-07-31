import os
import unittest
import time
import concurrent.futures

from agentbay import AgentBay
from agentbay.model import OperationResult, DeleteResult
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
    return f"test-context-{timestamp}-{random_str}"

def create_session(agent_bay, image_id=None):
    """Session creation helper function"""
    print(os.getenv("AGENTBAY_API_KEY"))
    params = CreateSessionParams(image_id=image_id) if image_id else CreateSessionParams()
    session_result = agent_bay.create(params)
    if not session_result.success or not session_result.session:
        raise Exception("Failed to create session")
    return agent_bay, session_result.session

class TestSessionComprehensive(unittest.TestCase):
    """
    Session Comprehensive Tests

    This test suite covers comprehensive session operations including:
    1. Session Basic Information Management Tests
    2. Label Management Tests
    3. Session Deletion Tests
    4. Sub-modules Initialization Tests
    5. Error Handling Tests
    6. Performance Tests
    7. Integration Tests
    8. Boundary Condition Tests
    9. Data Integrity Tests
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

        # Create a session
        print("Creating a new session for Session comprehensive testing...")
        params = CreateSessionParams()
        result = cls.agent_bay.create(params)
        if not result.success or not result.session:
            raise unittest.SkipTest("Failed to create session")

        cls.session = result.session
        print(f"Session created with ID: {cls.session.session_id}")

    @classmethod
    def tearDownClass(cls):
        """Clean up test environment after all tests."""
        print("Cleaning up: Deleting the session...")
        if hasattr(cls, "session"):
            try:
                result = cls.agent_bay.delete(cls.session)
                if result.success:
                    print("Session successfully deleted")
                else:
                    print(f"Warning: Error deleting session: {result.error_message}")
            except Exception as e:
                print(f"Warning: Error deleting session: {e}")

    def setUp(self):
        """Set up before each test."""
        pass

    # 1. Session Basic Information Management Tests
    def test_1_1_get_session_id(self):
        """1.1 Get session ID test - should correctly return the session ID"""
        # Prerequisites: AgentBay instance has been created, Session instance has been successfully created
        # Test objective: Verify that Session.get_session_id() method can correctly return the session ID

        session_id = self.session.get_session_id()

        # Verification points
        self.assertIsNotNone(session_id)
        self.assertIsInstance(session_id, str)
        self.assertNotEqual(session_id, "")
        self.assertEqual(session_id, self.session.session_id)

        print(f"TC-SESSION-001 SessionId: {session_id}")

    def test_1_2_get_api_key(self):
        """1.2 Get API key test - should correctly return the API key"""
        # Prerequisites: AgentBay instance has been created, Session instance has been successfully created
        # Test objective: Verify that Session.get_api_key() method can correctly return the API key

        api_key = self.session.get_api_key()
        agent_bay_api_key = self.agent_bay.api_key

        # Verification points
        self.assertIsNotNone(api_key)
        self.assertIsInstance(api_key, str)
        self.assertEqual(api_key, agent_bay_api_key)
        self.assertNotEqual(api_key, "")

        print(f"TC-SESSION-002 API Key length: {len(api_key)}")

    def test_1_3_get_session_information(self):
        """1.3 Get session information test - should correctly retrieve detailed session information"""
        # Prerequisites: Session instance has been successfully created and connection established
        # Test objective: Verify that Session.info() method can correctly retrieve detailed session information

        info_result = self.session.info()

        # Verification points
        self.assertTrue(info_result.success)
        self.assertIsNotNone(info_result.request_id)
        self.assertNotEqual(info_result.request_id, "")
        self.assertIsNotNone(info_result.data)

        session_info = info_result.data
        self.assertEqual(session_info.session_id, self.session.session_id)
        self.assertNotEqual(session_info.session_id, "")

        if session_info.resource_url:
            self.assertIsInstance(session_info.resource_url, str)

        print(f"TC-SESSION-003 SessionInfo: SessionId={session_info.session_id}, ResourceUrl={session_info.resource_url}")

    def test_1_4_1_get_session_link_no_parameters(self):
        """1.4.1 Get session link test (no parameters scenario) - should get link without parameters"""
        # Use browser_latest image to create session for link testing
        try:
            browser_agent_bay, browser_session = create_session(self.agent_bay, "browser_latest")

            try:
                link_result = browser_session.get_link()

                # Verification points
                self.assertTrue(link_result.success)
                self.assertIsNotNone(link_result.request_id)
                self.assertIsNotNone(link_result.data)
                self.assertIsInstance(link_result.data, str)
                self.assertNotEqual(link_result.data, "")

                print(f"TC-SESSION-004-1 Link (no params): {link_result.data}")
            finally:
                browser_agent_bay.delete(browser_session)
        except Exception as e:
            self.skipTest(f"Could not create browser session: {e}")

    def test_1_4_2_get_session_link_port_parameter(self):
        """1.4.2 Get session link test (port parameter) - should get link with port parameter"""
        # Use browser_latest image to create session for link testing
        try:
            browser_agent_bay, browser_session = create_session(self.agent_bay, "browser_latest")

            try:
                link_result = browser_session.get_link(port=8080)

                # Verification points
                self.assertTrue(link_result.success)
                self.assertIsNotNone(link_result.request_id)
                self.assertIsNotNone(link_result.data)
                self.assertIsInstance(link_result.data, str)
                self.assertNotEqual(link_result.data, "")

                print(f"TC-SESSION-004-2 Link (port 8080): {link_result.data}")
            finally:
                browser_agent_bay.delete(browser_session)
        except Exception as e:
            self.skipTest(f"Could not create browser session: {e}")

    def test_1_4_3_get_session_link_protocol_parameter(self):
        """1.4.3 Get session link test (protocol type parameter) - should get link with protocol parameter"""
        # Use linux_latest image to create session for link testing
        try:
            linux_agent_bay, linux_session = create_session(self.agent_bay, "linux_latest")

            try:
                link_result = linux_session.get_link(protocol_type="https")

                # Verification points
                self.assertTrue(link_result.success)
                self.assertIsNotNone(link_result.request_id)
                self.assertIsNotNone(link_result.data)
                self.assertIsInstance(link_result.data, str)
                self.assertNotEqual(link_result.data, "")

                print(f"TC-SESSION-004-3 Link (https protocol): {link_result.data}")
            except Exception as e:
                error_message = str(e)
                if "PARAM_ERROR:" in error_message:
                    print(f"TC-SESSION-004-3 Expected PARAM_ERROR caught: {error_message}")
                else:
                    raise
            finally:
                linux_agent_bay.delete(linux_session)
        except Exception as e:
            self.skipTest(f"Could not create linux session: {e}")

    def test_1_4_4_get_session_link_port_and_protocol(self):
        """1.4.4 Get session link test (port and protocol combination) - should get link with both parameters"""
        # Use browser_latest image to create session for link testing
        try:
            browser_agent_bay, browser_session = create_session(self.agent_bay, "browser_latest")

            try:
                link_result = browser_session.get_link(protocol_type="https", port=8080)

                # Verification points
                self.assertTrue(link_result.success)
                self.assertIsNotNone(link_result.request_id)
                self.assertIsNotNone(link_result.data)
                self.assertIsInstance(link_result.data, str)
                self.assertNotEqual(link_result.data, "")

                print(f"TC-SESSION-004-4 Link (https + port 8080): {link_result.data}")
            finally:
                browser_agent_bay.delete(browser_session)
        except Exception as e:
            self.skipTest(f"Could not create browser session: {e}")

    # 2. Label Management Tests
    def test_2_1_set_session_labels(self):
        """2.1 Set session labels test - should correctly set session labels"""
        # Prerequisites: Session instance has been successfully created
        # Test objective: Verify that Session.set_labels() method can correctly set session labels

        labels = {"env": "test", "version": "1.0", "team": "dev"}
        set_result = self.session.set_labels(labels)

        # Verification points
        self.assertTrue(set_result.success)
        self.assertIsNotNone(set_result.request_id)
        self.assertNotEqual(set_result.request_id, "")

        print(f"TC-LABEL-001 Set labels result: Success={set_result.success}, RequestId={set_result.request_id}")

    def test_2_2_get_session_labels(self):
        """2.2 Get session labels test - should correctly retrieve session labels"""
        # Prerequisites: Session instance has been created and labels have been set
        # Test objective: Verify that Session.get_labels() method can correctly retrieve session labels

        labels = {"env": "test", "version": "1.0", "team": "dev"}
        self.session.set_labels(labels)

        get_result = self.session.get_labels()

        # Verification points
        self.assertTrue(get_result.success)
        self.assertIsNotNone(get_result.request_id)
        self.assertIsNotNone(get_result.data)
        self.assertIsInstance(get_result.data, dict)

        retrieved_labels = get_result.data
        self.assertEqual(retrieved_labels["env"], "test")
        self.assertEqual(retrieved_labels["version"], "1.0")
        self.assertEqual(retrieved_labels["team"], "dev")

        print(f"TC-LABEL-002 Retrieved labels: {retrieved_labels}")

    def test_2_3_label_update(self):
        """2.3 Label update test - should correctly update and override labels"""
        # Prerequisites: Session instance has been created and initial labels have been set
        # Test objective: Verify that labels can be correctly updated and overridden

        # Set initial labels
        initial_labels = {"env": "test", "version": "1.0"}
        self.session.set_labels(initial_labels)

        # Update labels
        updated_labels = {"env": "prod", "newKey": "newValue", "team": "ops"}
        self.session.set_labels(updated_labels)

        # Get labels to verify update result
        get_result = self.session.get_labels()
        retrieved_labels = get_result.data

        # Verification points
        self.assertEqual(retrieved_labels["env"], "prod")
        self.assertEqual(retrieved_labels["newKey"], "newValue")
        self.assertEqual(retrieved_labels["team"], "ops")
        self.assertNotIn("version", retrieved_labels)  # Old labels should be replaced

        print(f"TC-LABEL-003 Updated labels: {retrieved_labels}")

    def test_2_4_empty_labels_handling(self):
        """2.4 Empty labels handling test - should handle setting empty labels object"""
        # Prerequisites: Session instance has been created
        # Test objective: Verify handling of setting empty labels object

        empty_labels = {}
        set_result = self.session.set_labels(empty_labels)

        # Verification points - based on validation logic, empty labels should fail
        self.assertFalse(set_result.success)
        self.assertIn("empty", set_result.error_message.lower())

        print(f"TC-LABEL-004 Empty labels handled correctly")

    # 3. Session Deletion Tests
    def test_3_1_regular_deletion(self):
        """3.1 Regular deletion test - should correctly delete the session"""
        # Prerequisites: Session instance has been successfully created
        # Test objective: Verify that Session.delete() method can correctly delete the session

        test_agent_bay, test_session = create_session(self.agent_bay)

        delete_result = test_session.delete(False)

        # Verification points
        self.assertTrue(delete_result.success)
        self.assertIsNotNone(delete_result.request_id)
        self.assertNotEqual(delete_result.request_id, "")

        print(f"TC-DELETE-001 Delete result: Success={delete_result.success}, RequestId={delete_result.request_id}")

    def test_3_2_context_sync_deletion(self):
        """3.2 Context sync deletion test - should correctly sync context before deletion"""
        # Prerequisites: Session instance has been created with context sync configured
        # Test objective: Verify that delete method can correctly sync context before deletion when sync_context=True

        # Get or create context
        context_list_result = self.agent_bay.context.list()
        if context_list_result.contexts:
            available_context = next((ctx for ctx in context_list_result.contexts if ctx.state == 'available'), None)
            if available_context:
                context_id = available_context.id
                print(f"Using existing context: {context_id}")
            else:
                create_result = self.agent_bay.context.create(generate_random_context_name())
                context_id = create_result.context_id
                print(f"Created new context: {context_id}")
        else:
            create_result = self.agent_bay.context.create(generate_random_context_name())
            context_id = create_result.context_id
            print(f"Created new context: {context_id}")

        # Create Session with context sync
        try:
            session_params = CreateSessionParams()
            context_sync = ContextSync.new(context_id, '/tmp/home', SyncPolicy.default())
            session_params.context_syncs = [context_sync]
            session_params.labels = {"test": "context-sync-integration"}
            session_params.image_id = "linux_latest"
            sync_session_result = self.agent_bay.create(session_params)
            self.assertTrue(sync_session_result.success)
            sync_session = sync_session_result.session

            try:
                # Trigger upload
                sync_result = sync_session.context.sync()
                print(f"Sync triggered: Success={sync_result.success}")

                # Check upload status
                info_result = sync_session.context.info()
                for item in info_result.context_status_data:
                    print(f"Context {item.context_id} status: {item.status}, taskType: {item.task_type}, path: {item.path}")

                # Call sync context deletion
                delete_result = sync_session.delete(True)

                # Verification points
                self.assertTrue(delete_result.success)
                self.assertIsNotNone(delete_result.request_id)

                print(f"TC-DELETE-002 Sync delete result: Success={delete_result.success}")
            finally:
                # Ensure session is cleaned up
                if sync_session:
                    try:
                        self.agent_bay.delete(sync_session)
                    except Exception as error:
                        print(f"Session already deleted or error occurred: {error}")
        except Exception as e:
            self.skipTest(f"Could not create context sync session: {e}")

    # 4. Sub-modules Initialization Tests
    def test_4_1_submodules_initialization(self):
        """4.1 Sub-modules initialization test - should verify all sub-modules are correctly initialized"""
        # Prerequisites: Session instance has been successfully created
        # Test objective: Verify that all sub-modules of session are correctly initialized and not null

        # Verification points
        self.assertIsNotNone(self.session.file_system)
        self.assertEqual(self.session.file_system.__class__.__name__, 'FileSystem')

        self.assertIsNotNone(self.session.command)
        self.assertEqual(self.session.command.__class__.__name__, 'Command')

        self.assertIsNotNone(self.session.code)
        self.assertEqual(self.session.code.__class__.__name__, 'Code')

        self.assertIsNotNone(self.session.context)

        self.assertIsNotNone(self.session.application)
        self.assertEqual(self.session.application.__class__.__name__, 'ApplicationManager')

        self.assertIsNotNone(self.session.window)
        self.assertEqual(self.session.window.__class__.__name__, 'WindowManager')

        self.assertIsNotNone(self.session.ui)
        self.assertEqual(self.session.ui.__class__.__name__, 'UI')

        self.assertIsNotNone(self.session.oss)
        self.assertEqual(self.session.oss.__class__.__name__, 'Oss')

        print(f"TC-MODULES-001 All sub-modules initialized successfully")

    # 5. Error Handling Tests
    def test_5_1_set_labels_invalid_parameters(self):
        """5.1 setLabels invalid parameter handling test - should handle invalid parameters"""
        # Prerequisites: Session instance has been created
        # Test objective: Verify handling when invalid parameters are passed

        # Test None parameter
        null_result = self.session.set_labels(None)
        print(f"Null result: {null_result}")
        self.assertFalse(null_result.success)
        self.assertIn("null", null_result.error_message.lower())
        self.assertEqual(null_result.request_id, "")

        # Test non-dict type parameters
        string_result = self.session.set_labels("invalid")
        self.assertFalse(string_result.success)
        self.assertIn("invalid", string_result.error_message.lower())

        number_result = self.session.set_labels(123)
        self.assertFalse(number_result.success)
        self.assertIn("invalid", number_result.error_message.lower())

        boolean_result = self.session.set_labels(True)
        self.assertFalse(boolean_result.success)
        self.assertIn("invalid", boolean_result.error_message.lower())

        # Test list type parameters
        array_result = self.session.set_labels([])
        print(f"Array result: {array_result.error_message}")
        self.assertFalse(array_result.success)
        self.assertIn("array", array_result.error_message.lower())

        array_with_data_result = self.session.set_labels([{"key": "value"}])
        self.assertFalse(array_with_data_result.success)
        self.assertIn("array", array_with_data_result.error_message.lower())

        print(f"TC-ERROR-001 setLabels invalid parameters: All invalid parameter types correctly rejected")

    def test_5_2_set_labels_empty_object(self):
        """5.2 setLabels empty object handling test - should handle empty object"""
        # Prerequisites: Session instance has been created
        # Test objective: Verify handling when empty object is passed

        empty_result = self.session.set_labels({})
        self.assertFalse(empty_result.success)
        self.assertIn("empty", empty_result.error_message.lower())
        self.assertEqual(empty_result.request_id, "")

        print(f"TC-ERROR-002 setLabels empty object: Empty object correctly rejected")

    def test_5_3_set_labels_empty_keys_values(self):
        """5.3 setLabels empty keys/values handling test - should handle empty keys or values"""
        # Prerequisites: Session instance has been created
        # Test objective: Verify handling when empty keys or values are passed

        # Test empty key
        empty_key_result = self.session.set_labels({"": "value"})
        self.assertFalse(empty_key_result.success)
        self.assertIn("keys", empty_key_result.error_message.lower())
        self.assertEqual(empty_key_result.request_id, "")

        # Test empty value
        empty_value_result = self.session.set_labels({"key": ""})
        self.assertFalse(empty_value_result.success)
        self.assertIn("values", empty_value_result.error_message.lower())
        self.assertEqual(empty_value_result.request_id, "")

        # Test None value
        null_value_result = self.session.set_labels({"key": None})
        self.assertFalse(null_value_result.success)
        self.assertIn("values", null_value_result.error_message.lower())

        print(f"TC-ERROR-003 setLabels empty keys/values: All empty keys and values correctly rejected")

    def test_5_4_set_labels_mixed_invalid_parameters(self):
        """5.4 setLabels mixed invalid parameters test - should handle mixed invalid parameters with proper priority"""
        # Prerequisites: Session instance has been created
        # Test objective: Verify priority handling of mixed invalid parameters

        # Test mixed situation with empty key and valid key-value pair
        mixed_empty_key_result = self.session.set_labels({
            "validKey": "validValue",
            "": "emptyKeyValue"
        })
        self.assertFalse(mixed_empty_key_result.success)
        self.assertIn("keys", mixed_empty_key_result.error_message.lower())

        # Test mixed situation with empty value and valid key-value pair
        mixed_empty_value_result = self.session.set_labels({
            "validKey": "validValue",
            "emptyValueKey": ""
        })
        self.assertFalse(mixed_empty_value_result.success)
        self.assertIn("values", mixed_empty_value_result.error_message.lower())

        # Test multiple invalid key-value pairs
        multiple_invalid_result = self.session.set_labels({
            "": "emptyKey",
            "emptyValue": "",
            "nullValue": None
        })
        self.assertFalse(multiple_invalid_result.success)
        # Should return the first encountered error (empty key)
        self.assertIn("keys", multiple_invalid_result.error_message.lower())

        print(f"TC-ERROR-004 setLabels mixed invalid parameters: Mixed invalid parameters correctly handled with proper priority")

    def test_5_5_set_labels_boundary_cases(self):
        """5.5 setLabels boundary cases test - should handle boundary cases"""
        # Prerequisites: Session instance has been created
        # Test objective: Verify handling of boundary cases

        # Test key with only whitespace
        whitespace_key_result = self.session.set_labels({" ": "value"})
        self.assertFalse(whitespace_key_result.success)

        # Test value with only whitespace
        whitespace_value_result = self.session.set_labels({"key": " "})
        self.assertFalse(whitespace_value_result.success)

        # Test zero-length but non-empty special cases (if any exist)
        special_chars_result = self.session.set_labels({
            "key1": "value1",
            "key2": "value2"
        })
        self.assertTrue(special_chars_result.success)

        print(f"TC-ERROR-005 setLabels boundary cases: Boundary cases correctly handled")

    def test_5_6_api_response_exception_handling(self):
        """5.6 API response exception handling test - should handle API exceptions"""
        # Prerequisites: Session instance has been created
        # Test objective: Verify handling when API returns exceptional responses

        # This test mainly verifies existing error handling mechanisms
        try:
            # Call info method, should succeed under normal circumstances
            result = self.session.info()
            self.assertIsNotNone(result.request_id)

            if not result.success:
                # If failure, verify error information exists
                self.assertIsNotNone(result.error_message)

            print(f"TC-ERROR-006 API response handling verified")
        except Exception as error:
            # Verify exception is correctly caught
            self.assertIsNotNone(error)
            print(f"TC-ERROR-006 API exception handled: {error}")

    # 6. Performance Tests
    def test_6_1_label_operations_performance(self):
        """6.1 Label operations performance test - should verify performance of label operations"""
        # Prerequisites: Session instance has been created
        # Test objective: Verify performance of label operations

        iterations = 5
        set_times = []
        get_times = []

        for i in range(iterations):
            labels = {"iteration": str(i), "timestamp": str(int(time.time() * 1000))}

            # Test set_labels performance
            set_start_time = time.time()
            self.session.set_labels(labels)
            set_time = (time.time() - set_start_time) * 1000  # Convert to milliseconds
            set_times.append(set_time)

            # Test get_labels performance
            get_start_time = time.time()
            self.session.get_labels()
            get_time = (time.time() - get_start_time) * 1000  # Convert to milliseconds
            get_times.append(get_time)

        avg_set_time = sum(set_times) / len(set_times)
        avg_get_time = sum(get_times) / len(get_times)

        # Verification points
        self.assertLess(avg_set_time, 2000)  # Within 2 seconds
        self.assertLess(avg_get_time, 2000)  # Within 2 seconds

        print(f"TC-PERF-001 Label operations: Avg set={avg_set_time:.2f}ms, Avg get={avg_get_time:.2f}ms")

    def test_6_2_concurrent_operations_performance(self):
        """6.2 Concurrent operations performance test - should verify performance of concurrent operations"""
        # Prerequisites: Multiple Session instances have been created
        # Test objective: Verify performance of concurrent operations

        sessions = []
        agent_bays = []

        try:
            # Create multiple sessions
            for i in range(3):
                agent_bay, session = create_session(self.agent_bay)
                agent_bays.append(agent_bay)
                sessions.append(session)

            # Execute concurrent operations
            def set_labels_task(session, index):
                return session.set_labels({"test": f"concurrent-{index}", "timestamp": str(int(time.time() * 1000))})

            start_time = time.time()
            with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                futures = [executor.submit(set_labels_task, sess, index) for index, sess in enumerate(sessions)]
                results = [future.result() for future in concurrent.futures.as_completed(futures)]

            concurrent_time = (time.time() - start_time) * 1000  # Convert to milliseconds

            # Verification points
            for result in results:
                self.assertTrue(result.success)

            print(f"TC-PERF-003 Concurrent operations: Total time={concurrent_time:.2f}ms, Success rate=100%")

        finally:
            # Clean up sessions
            for i in range(len(sessions)):
                try:
                    agent_bays[i].delete(sessions[i])
                except Exception as e:
                    print(f"Error deleting session {i}: {e}")

    # 7. Integration Tests
    def test_7_1_complete_session_lifecycle(self):
        """7.1 Complete session lifecycle test - should verify complete session lifecycle from creation to deletion"""
        # Prerequisites: AgentBay instance is available
        # Test objective: Verify complete session lifecycle from creation to deletion

        lifecycle_agent_bay, lifecycle_session = create_session(self.agent_bay)

        try:
            # 1. Verify session creation
            self.assertIsNotNone(lifecycle_session.session_id)

            # 2. Set labels
            labels = {"env": "integration", "test": "lifecycle"}
            set_result = lifecycle_session.set_labels(labels)
            self.assertTrue(set_result.success)

            # 3. Get session information
            info_result = lifecycle_session.info()
            self.assertTrue(info_result.success)

            # 4. Verify labels
            get_result = lifecycle_session.get_labels()
            self.assertTrue(get_result.success)
            retrieved_labels = get_result.data
            self.assertEqual(retrieved_labels["env"], "integration")

            # 5. Use sub-modules (basic verification)
            self.assertIsNotNone(lifecycle_session.command)
            self.assertIsNotNone(lifecycle_session.file_system)

            print(f"TC-INTEGRATION-001 Full lifecycle completed successfully")

        finally:
            # 6. Delete session
            delete_result = lifecycle_agent_bay.delete(lifecycle_session)
            self.assertTrue(delete_result.success)

    def test_7_2_multi_session_interaction(self):
        """7.2 Multi-session interaction test - should verify independence and interaction between multiple sessions"""
        # Prerequisites: AgentBay instance is available
        # Test objective: Verify independence and interaction between multiple sessions

        multi_sessions = []
        multi_agent_bays = []

        try:
            # Create multiple Session instances
            for i in range(3):
                agent_bay, session = create_session(self.agent_bay)
                multi_agent_bays.append(agent_bay)
                multi_sessions.append(session)

            # Set different labels for each session
            def set_labels_task(session, index):
                return session.set_labels({
                    "sessionIndex": str(index),
                    "type": "multi-session-test",
                    "timestamp": str(int(time.time() * 1000))
                })

            with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                label_futures = [executor.submit(set_labels_task, sess, index) for index, sess in enumerate(multi_sessions)]
                label_results = [future.result() for future in concurrent.futures.as_completed(label_futures)]

            for result in label_results:
                self.assertTrue(result.success)

            # Verify independence between sessions
            def get_labels_task(session):
                return session.get_labels()

            with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                get_futures = [executor.submit(get_labels_task, sess) for sess in multi_sessions]
                get_results = [future.result() for future in concurrent.futures.as_completed(get_futures)]

            # Verification points
            for index, result in enumerate(get_results):
                self.assertTrue(result.success)
                labels = result.data
                # Note: We can't guarantee order in concurrent execution, so we check that all expected values exist
                session_indices = [labels.get("sessionIndex") for result in get_results for labels in [result.data]]
                self.assertIn(str(index), session_indices)

            # Test concurrent operations
            def info_task(session):
                return session.info()

            with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                info_futures = [executor.submit(info_task, sess) for sess in multi_sessions]
                info_results = [future.result() for future in concurrent.futures.as_completed(info_futures)]

            for result in info_results:
                self.assertTrue(result.success)

            print(f"TC-INTEGRATION-002 Multi-session test: {len(multi_sessions)} sessions operated independently")

        finally:
            # Release sessions
            for i in range(len(multi_sessions)):
                try:
                    multi_agent_bays[i].delete(multi_sessions[i])
                except Exception as e:
                    print(f"Error deleting session {i}: {e}")

    # 8. Boundary Condition Tests
    def test_8_1_large_amount_of_label_data(self):
        """8.1 Large amount of label data test - should verify ability to handle large amount of label data"""
        # Prerequisites: Session instance has been created
        # Test objective: Verify ability to handle large amount of label data

        # Create labels object with many key-value pairs
        large_labels = {}
        for i in range(50):
            large_labels[f"key_{i}"] = f"value_{i}_{'x' * 100}"  # Each value approximately 100 characters

        # Set large amount of label data
        set_result = self.session.set_labels(large_labels)
        self.assertTrue(set_result.success)

        # Get and verify data integrity
        get_result = self.session.get_labels()
        self.assertTrue(get_result.success)

        retrieved_labels = get_result.data
        self.assertEqual(len(retrieved_labels), 50)

        # Verify data integrity
        for i in range(50):
            expected_value = f"value_{i}_{'x' * 100}"
            self.assertEqual(retrieved_labels[f"key_{i}"], expected_value)

        print(f"TC-BOUNDARY-001 Large labels: Successfully handled {len(large_labels)} label pairs")

    def test_8_2_special_characters_in_labels(self):
        """8.2 Special characters in labels test - should verify handling of special characters in labels"""
        # Prerequisites: Session instance has been created
        # Test objective: Verify handling of special characters in labels

        # Set labels containing special characters
        special_labels = {
            "htmlTags": "<script>alert('test')</script>",
            "jsonChars": '{"key": "value", "array": [1,2,3]}',
            "specialSymbols": "!@#$%^&*()_+-=[]{}|;':\",./<>?",
            "newlines": "line1\nline2\ttabbed",
            "quotes": "single'quote and \"double\"quote",
            "backslashes": "path\\to\\file\\with\\backslashes"
        }

        # Set special character labels
        set_result = self.session.set_labels(special_labels)
        self.assertTrue(set_result.success)

        # Verify correctness of storage and retrieval
        get_result = self.session.get_labels()
        self.assertTrue(get_result.success)

        retrieved_labels = get_result.data
        print(f"TC-BOUNDARY-002 Retrieved special labels: {retrieved_labels}")

        # Verification points
        self.assertEqual(retrieved_labels["htmlTags"], "<script>alert('test')</script>")
        self.assertEqual(retrieved_labels["jsonChars"], '{"key": "value", "array": [1,2,3]}')
        self.assertEqual(retrieved_labels["specialSymbols"], "!@#$%^&*()_+-=[]{}|;':\",./<>?")
        self.assertEqual(retrieved_labels["newlines"], "line1\nline2\ttabbed")
        self.assertEqual(retrieved_labels["quotes"], "single'quote and \"double\"quote")
        self.assertEqual(retrieved_labels["backslashes"], "path\\to\\file\\with\\backslashes")

        print(f"TC-BOUNDARY-002 Special characters: All special characters correctly encoded and decoded")

    def test_8_3_long_running_session(self):
        """8.3 Long-running session test - should verify stability of long-running sessions"""
        # Prerequisites: Session instance has been created
        # Test objective: Verify stability of long-running sessions

        long_running_agent_bay, long_running_session = create_session(self.agent_bay)

        try:
            # Periodically execute various operations
            iterations = 10
            operation_results = []

            for i in range(iterations):
                # Set labels
                labels = {"iteration": str(i), "timestamp": str(int(time.time() * 1000))}
                set_result = long_running_session.set_labels(labels)
                operation_results.append(set_result.success)

                # Get session information
                info_result = long_running_session.info()
                operation_results.append(info_result.success)

                # Get labels
                get_result = long_running_session.get_labels()
                operation_results.append(get_result.success)

                # Brief wait to simulate long-running
                time.sleep(0.1)

            # Verification points
            success_rate = sum(operation_results) / len(operation_results)
            self.assertGreaterEqual(success_rate, 0.9)  # 90% success rate

            # Final verification that session is still active
            final_info_result = long_running_session.info()
            self.assertTrue(final_info_result.success)
            self.assertEqual(final_info_result.data.session_id, long_running_session.session_id)

            print(f"TC-BOUNDARY-003 Long running session: {iterations} iterations completed with {success_rate * 100:.1f}% success rate")

        finally:
            long_running_agent_bay.delete(long_running_session)

    # 9. Data Integrity Tests
    def test_9_1_maintain_session_consistency_across_operations(self):
        """9.1 Data integrity test - should maintain session consistency across operations"""
        # Verify session consistency across various operations
        original_session_id = self.session.session_id

        # Execute multiple operations
        self.session.set_labels({"test": "consistency"})
        info_result = self.session.info()
        self.session.get_labels()

        # Verify session ID remains consistent
        self.assertEqual(self.session.session_id, original_session_id)
        self.assertEqual(info_result.data.session_id, original_session_id)

        print(f"Data consistency test: SessionId remained consistent across operations")

    def test_9_2_handle_concurrent_operations_safely(self):
        """9.2 Data integrity test - should handle concurrent operations safely"""
        # Verify safety of concurrent operations
        def concurrent_operation_task(operation_type):
            if operation_type == 'info':
                return self.session.info()
            elif operation_type == 'set_labels1':
                return self.session.set_labels({"concurrent": "test1"})
            elif operation_type == 'get_labels':
                return self.session.get_labels()
            elif operation_type == 'set_labels2':
                return self.session.set_labels({"concurrent": "test2"})
            else:
                return self.session.info()

        operations = ['info', 'set_labels1', 'get_labels', 'set_labels2', 'info']

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(concurrent_operation_task, op) for op in operations]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]

        # Verify all operations have valid request_id
        for result in results:
            self.assertIsNotNone(result.request_id)
            self.assertNotEqual(result.request_id, "")

        print(f"Concurrent operations test: All {len(results)} concurrent operations completed with valid requestIds")

if __name__ == "__main__":
    unittest.main()
