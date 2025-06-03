import os
from agentbay.exceptions import AgentBayError
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_openapi.exceptions._client import ClientException
from threading import Lock

from agentbay.session import Session
from agentbay.api.client import Client as mcp_client
from agentbay.api.models import CreateMcpSessionRequest
from agentbay.config import load_config


class AgentBay:
    """
    AgentBay represents the main client for interacting with the AgentBay cloud runtime environment.
    """

    def __init__(self, api_key: str = ""):
        if not api_key:
            api_key = os.getenv("AGENTBAY_API_KEY")
            if not api_key:
                raise ValueError(
                    "API key is required. Provide it as a parameter or set the AGENTBAY_API_KEY environment variable"
                )

        # Load configuration
        config_data = load_config()

        self.api_key = api_key
        self.region_id = config_data["region_id"]

        config = open_api_models.Config()
        config.endpoint = config_data["endpoint"]
        config.read_timeout = config_data["timeout_ms"]

        self.client = mcp_client(config)
        self._sessions = {}
        self._lock = Lock()

    def create(self) -> Session:
        """Create a new session in the AgentBay cloud environment."""
        try:
            request = CreateMcpSessionRequest(authorization=f"Bearer {self.api_key}")
            response = self.client.create_mcp_session(request)
            print("response =", response)
            session_id = (
                response.to_map().get("body", {}).get("Data", {}).get("SessionId")
            )
            print("session_id =", session_id)
            if not session_id:
                raise RuntimeError(
                    f"Failed to get session_id from response: {response}"
                )
            session = Session(self, session_id)
            with self._lock:
                self._sessions[session_id] = session
            return session
        except ClientException as e:
            print("Aliyun OpenAPI ClientException:", e)
            raise AgentBayError(f"Failed to create session: {e}")
        except Exception as e:
            print("Error calling create_mcp_session:", e)
            raise

    def list(self):
        """List all available sessions."""
        with self._lock:
            return list(self._sessions.values())

    def delete(self, session: Session):
        """Delete a session by session object."""
        try:
            session.delete()
            with self._lock:
                self._sessions.pop(session.session_id, None)
        except Exception as e:
            print("Error deleting session:", e)
            raise AgentBayError(f"Failed to delete session {session.session_id}: {e}")
