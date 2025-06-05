import unittest
import os
import sys
import json
import random
import time

# Add the parent directory to the path so we can import the agentbay package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agentbay import AgentBay
from agentbay.exceptions import AgentBayError


def get_test_api_key():
    """Get API key for testing"""
    api_key = os.environ.get("AGENTBAY_API_KEY")
    if not api_key:
        api_key = "akm-xxx"  # Replace with your test API key
        print("Warning: Using default API key. Set AGENTBAY_API_KEY environment variable for testing.")
    return api_key


def generate_unique_id():
    """Create a unique identifier for test labels to avoid conflicts with existing data"""
    timestamp = int(time.time() * 1000000)
    random_part = random.randint(0, 10000)
    return f"{timestamp}-{random_part}"


class TestSessionLabels(unittest.TestCase):
    """Test cases for session labels functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        api_key = get_test_api_key()
        self.agent_bay = AgentBay(api_key=api_key)
        
        # Create a session
        print("Creating a new session for labels testing...")
        self.session = self.agent_bay.create()
        print(f"Session created with ID: {self.session.session_id}")
        
        # Generate a unique identifier for this test run
        self.unique_id = generate_unique_id()
        print(f"Using unique ID for test labels: {self.unique_id}")
    
    def tearDown(self):
        """Tear down test fixtures."""
        print("Cleaning up: Deleting the session...")
        try:
            self.agent_bay.delete(self.session)
        except Exception as e:
            print(f"Warning: Error deleting session: {e}")
    
    def test_set_get_labels(self):
        """Test setting and getting labels for a session."""
        # Define test labels with unique values to avoid conflicts with existing data
        test_labels = {
            "environment": f"testing-{self.unique_id}",
            "owner": f"test-team-{self.unique_id}",
            "project": f"labels-test-{self.unique_id}",
            "version": "1.0.0"
        }
        
        # Test 1: Set labels using set_labels
        print("Setting labels for the session...")
        try:
            self.session.set_labels(test_labels)
        except Exception as e:
            self.fail(f"Error setting labels: {e}")
        
        # Test 2: Get labels using get_labels
        print("Getting labels for the session...")
        try:
            retrieved_labels = self.session.get_labels()
            print(f"Retrieved labels: {retrieved_labels}")
            
            # Verify that all expected labels are present with correct values
            for key, expected_value in test_labels.items():
                self.assertIn(key, retrieved_labels, f"Expected label '{key}' not found in retrieved labels")
                self.assertEqual(expected_value, retrieved_labels[key], 
                                f"Label '{key}' value mismatch: expected '{expected_value}', got '{retrieved_labels[key]}'")
        except Exception as e:
            self.fail(f"Error getting labels: {e}")
        
        # Test 3: Verify labels using list_by_labels
        print("Verifying labels using list_by_labels...")
        
        # Test with a single label (using the unique value)
        single_label_filter = {
            "environment": test_labels["environment"]
        }
        
        try:
            sessions = self.agent_bay.list_by_labels(single_label_filter)
            
            # Check if our session is in the results
            found_in_single_label_results = False
            for s in sessions:
                if s.session_id == self.session.session_id:
                    found_in_single_label_results = True
                    break
            
            self.assertTrue(found_in_single_label_results, "Session not found when filtering by single label")
            print("Session successfully found when filtering by single label")
        except Exception as e:
            self.fail(f"Error listing sessions by single label: {e}")
        
        # Test with multiple labels (using the unique values)
        multi_label_filter = {
            "environment": test_labels["environment"],
            "project": test_labels["project"]
        }
        
        try:
            sessions = self.agent_bay.list_by_labels(multi_label_filter)
            
            # Check if our session is in the results
            found_in_multi_label_results = False
            for s in sessions:
                if s.session_id == self.session.session_id:
                    found_in_multi_label_results = True
                    break
            
            self.assertTrue(found_in_multi_label_results, "Session not found when filtering by multiple labels")
            print("Session successfully found when filtering by multiple labels")
        except Exception as e:
            self.fail(f"Error listing sessions by multiple labels: {e}")
        
        # Test with non-matching label
        non_matching_filter = {
            "environment": f"production-{self.unique_id}"  # This doesn't match our session
        }
        
        try:
            sessions = self.agent_bay.list_by_labels(non_matching_filter)
            
            # Check that our session is NOT in the results
            found_in_non_matching_results = False
            for s in sessions:
                if s.session_id == self.session.session_id:
                    found_in_non_matching_results = True
                    break
            
            self.assertFalse(found_in_non_matching_results, "Session found when filtering by non-matching label")
            print("Session correctly not found when filtering by non-matching label")
        except Exception as e:
            self.fail(f"Error listing sessions by non-matching label: {e}")
        
        # Test 4: Update labels (using the unique values)
        updated_labels = {
            "environment": f"staging-{self.unique_id}",
            "owner": test_labels["owner"],
            "project": f"labels-test-updated-{self.unique_id}",
            "status": "active"
        }
        
        print("Updating labels for the session...")
        try:
            self.session.set_labels(updated_labels)
        except Exception as e:
            self.fail(f"Error updating labels: {e}")
        
        # Verify updated labels using get_labels
        print("Getting updated labels for the session...")
        try:
            retrieved_updated_labels = self.session.get_labels()
            print(f"Retrieved updated labels: {retrieved_updated_labels}")
            
            # Verify that all expected updated labels are present with correct values
            for key, expected_value in updated_labels.items():
                self.assertIn(key, retrieved_updated_labels, f"Expected updated label '{key}' not found in retrieved labels")
                self.assertEqual(expected_value, retrieved_updated_labels[key], 
                                f"Updated label '{key}' value mismatch: expected '{expected_value}', got '{retrieved_updated_labels[key]}'")
            
            # Verify that the old label that was removed is no longer present
            self.assertNotIn("version", retrieved_updated_labels, "Removed label 'version' still present in updated labels")
        except Exception as e:
            self.fail(f"Error getting updated labels: {e}")
        
        # Verify updated labels using list_by_labels with the new environment value
        updated_env_filter = {
            "environment": updated_labels["environment"]
        }
        
        try:
            sessions = self.agent_bay.list_by_labels(updated_env_filter)
            
            found_with_updated_env = False
            for s in sessions:
                if s.session_id == self.session.session_id:
                    found_with_updated_env = True
                    break
            
            self.assertTrue(found_with_updated_env, "Session not found when filtering by updated environment label")
            print("Session successfully found when filtering by updated environment label")
        except Exception as e:
            self.fail(f"Error listing sessions by updated environment label: {e}")
        
        # The session should no longer be found with the old environment value
        old_env_filter = {
            "environment": test_labels["environment"]
        }
        
        try:
            sessions = self.agent_bay.list_by_labels(old_env_filter)
            
            found_with_old_env = False
            for s in sessions:
                if s.session_id == self.session.session_id:
                    found_with_old_env = True
                    break
            
            self.assertFalse(found_with_old_env, "Session found when filtering by old environment label")
            print("Session correctly not found when filtering by old environment label")
        except Exception as e:
            self.fail(f"Error listing sessions by old environment label: {e}")
        
        print("Session labels test completed successfully")


if __name__ == '__main__':
    unittest.main()
