import json
import unittest

from agentbay.session_params import CreateSessionParams


class TestCreateSessionParams(unittest.TestCase):
    def test_default_initialization(self):
        """Test that CreateSessionParams initializes with default values."""
        params = CreateSessionParams()
        self.assertEqual(params.labels, {})

    def test_custom_labels(self):
        """Test that CreateSessionParams accepts custom labels."""
        labels = {"username": "alice", "project": "my-project"}
        params = CreateSessionParams(labels=labels)
        self.assertEqual(params.labels, labels)

    def test_labels_json_conversion(self):
        """Test that labels can be converted to JSON for the API request."""
        labels = {"username": "alice", "project": "my-project"}
        params = CreateSessionParams(labels=labels)

        # Simulate what happens in AgentBay.create()
        labels_json = json.dumps(params.labels)

        # Verify the JSON string
        parsed_labels = json.loads(labels_json)
        self.assertEqual(parsed_labels, labels)

    def test_mcp_policy_id(self):
        """Test that mcp_policy_id can be carried by CreateSessionParams."""
        params = CreateSessionParams(mcp_policy_id="policy-xyz")
        self.assertEqual(params.mcp_policy_id, "policy-xyz")


if __name__ == "__main__":
    unittest.main()
