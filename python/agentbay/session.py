import json
from typing import Dict, Optional

from agentbay.adb import Adb
from agentbay.api.models import (GetLabelRequest, ReleaseMcpSessionRequest,
                                 SetLabelRequest)
from agentbay.application import ApplicationManager
from agentbay.command import Command
from agentbay.exceptions import SessionError
from agentbay.filesystem import FileSystem
from agentbay.window import WindowManager


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

        # Initialize application and window managers
        self.application = ApplicationManager(self)
        self.window = WindowManager(self)

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

    def set_labels(self, labels: Dict[str, str]) -> None:
        """
        Sets the labels for this session.

        Args:
            labels (Dict[str, str]): The labels to set for the session.

        Raises:
            SessionError: If the operation fails.
        """
        try:
            # Convert labels to JSON string
            labels_json = json.dumps(labels)

            request = SetLabelRequest(
                authorization=f"Bearer {self.get_api_key()}",
                session_id=self.session_id,
                labels=labels_json,
            )

            response = self.get_client().set_label(request)
            print(response)
        except Exception as e:
            print("Error calling set_label:", e)
            raise SessionError(
                f"Failed to set labels for session {self.session_id}: {e}"
            )

    def get_labels(self) -> Dict[str, str]:
        """
        Gets the labels for this session.

        Returns:
            Dict[str, str]: The labels for the session.

        Raises:
            SessionError: If the operation fails.
        """
        try:
            request = GetLabelRequest(
                authorization=f"Bearer {self.get_api_key()}", session_id=self.session_id
            )

            response = self.get_client().get_label(request)

            # Extract labels from response
            labels_json = (
                response.to_map().get("body", {}).get("Data", {}).get("Labels")
            )

            if labels_json:
                return json.loads(labels_json)

            return {}
        except Exception as e:
            print("Error calling get_label:", e)
            raise SessionError(
                f"Failed to get labels for session {self.session_id}: {e}"
            )
