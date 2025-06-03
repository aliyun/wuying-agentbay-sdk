from agentbay.exceptions import SessionError
from agentbay.filesystem import FileSystem
from agentbay.command import Command
from agentbay.adb import Adb
from agentbay.api.models import ReleaseMcpSessionRequest


class Session:
    """
    Session represents a session in the AgentBay cloud environment.
    """

    def __init__(self, agent_bay: "AgentBay", session_id: str):
        self.agent_bay = agent_bay
        self.session_id = session_id

        # Initialize file system, command, and adb handlers
        self.file_system = FileSystem(self)
        self.command = Command(self)
        self.adb = Adb(self)

    def get_api_key(self) -> str:
        """Return the API key for this session."""
        return self.agent_bay.api_key

    def get_client(self):
        """Return the HTTP client for this session."""
        return self.agent_bay.client

    def get_session_id(self) -> str:
        """Return the session_id for this session."""
        return self.session_id

    def delete(self):
        """Delete this session."""
        try:
            request = ReleaseMcpSessionRequest(
                authorization=f"Bearer {self.get_api_key()}", session_id=self.session_id
            )
            response = self.get_client().release_mcp_session(request)
            print(response)
        except Exception as e:
            print("Error calling release_mcp_session:", e)
            raise SessionError(f"Failed to delete session {self.session_id}: {e}")
