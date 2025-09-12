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

    def test_network_id(self):
        """Test that network_id can be carried by CreateSessionParams."""
        params = CreateSessionParams(network_id="net-123456")
        self.assertEqual(params.network_id, "net-123456")

    def test_network_id_none(self):
        """Test that network_id defaults to None."""
        params = CreateSessionParams()
        self.assertIsNone(params.network_id)

    def test_all_parameters(self):
        """Test CreateSessionParams with all parameters including network_id."""
        labels = {"env": "test", "project": "demo"}
        params = CreateSessionParams(
            labels=labels,
            image_id="linux_latest",
            is_vpc=True,
            mcp_policy_id="policy-123",
            network_id="net-456789"
        )
        
        self.assertEqual(params.labels, labels)
        self.assertEqual(params.image_id, "linux_latest")
        self.assertTrue(params.is_vpc)
        self.assertEqual(params.mcp_policy_id, "policy-123")
        self.assertEqual(params.network_id, "net-456789")


if __name__ == "__main__":
    unittest.main()
