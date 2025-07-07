import json
import os
from threading import Lock
from typing import Dict, List, Optional

from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_openapi.exceptions._client import ClientException

from agentbay.api.client import Client as mcp_client
from agentbay.api.models import CreateMcpSessionRequest, ListSessionRequest
from agentbay.model import (
    SessionResult,
    SessionListResult,
    DeleteResult,
    extract_request_id
)
from agentbay.config import load_config
from agentbay.context import ContextService
from agentbay.exceptions import AgentBayError
from agentbay.session import Session
from agentbay.session_params import CreateSessionParams
from typing import Optional

class Config:
    def __init__(self, region_id: str, endpoint: str, timeout_ms: str):
        self.region_id = region_id
        self.endpoint = endpoint
        self.timeout_ms = timeout_ms



class AgentBay:
    """
    AgentBay represents the main client for interacting with the AgentBay cloud runtime environment.
    """

    def __init__(self, api_key: str = "", cfg: Optional[Config] = None):
        if not api_key:
            api_key = os.getenv("AGENTBAY_API_KEY")
            if not api_key:
                raise ValueError(
                    "API key is required. Provide it as a parameter or set the AGENTBAY_API_KEY environment variable"
                )

        # Load configuration
        config_data = load_config(cfg)

        self.api_key = api_key
        self.region_id = config_data["region_id"]

        config = open_api_models.Config()
        config.endpoint = config_data["endpoint"]
        config.read_timeout = config_data["timeout_ms"]
        config.connect_timeout = config_data["timeout_ms"]

        self.client = mcp_client(config)
        self._sessions = {}
        self._lock = Lock()

        # Initialize context service
        self.context = ContextService(self)

    def create(self, params: Optional[CreateSessionParams] = None) -> SessionResult:
        """
        Create a new session in the AgentBay cloud environment.

        Args:
            params (Optional[CreateSessionParams], optional): Parameters for creating the session. Defaults to None.

        Returns:
            SessionResult: Result containing the created session and request ID.
        """
        try:
            if params is None:
                params = CreateSessionParams()

            request = CreateMcpSessionRequest(authorization=f"Bearer {self.api_key}")

            # Add context_id if provided
            if params.context_id:
                request.context_id = params.context_id

            # Add labels if provided
            if params.labels:
                # Convert labels to JSON string
                request.labels = json.dumps(params.labels)

            if params.image_id:
                request.image_id = params.image_id
            response = self.client.create_mcp_session(request)
            print("response =", response)

            # Extract request ID
            request_id = extract_request_id(response)

            session_data = response.to_map()

            if not isinstance(session_data, dict):
                return SessionResult(
                    request_id=request_id,
                    success=False,
                    error_message="Invalid response format: expected a dictionary"
                )

            body = session_data.get("body", {})
            if not isinstance(body, dict):
                return SessionResult(
                    request_id=request_id,
                    success=False,
                    error_message="Invalid response format: 'body' field is not a dictionary"
                )

            data = body.get("Data", {})
            if not isinstance(data, dict):
                return SessionResult(
                    request_id=request_id,
                    success=False,
                    error_message="Invalid response format: 'Data' field is not a dictionary"
                )

            session_id = data.get("SessionId")
            if not session_id:
                return SessionResult(
                    request_id=request_id,
                    success=False,
                    error_message="SessionId not found in response"
                )

            # ResourceUrl is optional in CreateMcpSession response
            resource_url = data.get("ResourceUrl")

            print("session_id =", session_id)
            print("resource_url =", resource_url)

            session = Session(self, session_id)
            if resource_url:
                session.resource_url = resource_url

            with self._lock:
                self._sessions[session_id] = session

            # Return SessionResult with request ID
            return SessionResult(request_id=request_id, success=True, session=session)

        except ClientException as e:
            print("Aliyun OpenAPI ClientException:", e)
            return SessionResult(
                request_id="",
                success=False,
                error_message=f"Failed to create session: {e}"
            )
        except Exception as e:
            print("Error calling create_mcp_session:", e)
            return SessionResult(
                request_id="",
                success=False,
                error_message=f"Unexpected error creating session: {e}"
            )

    def list(self) -> List[Session]:
        """
        List all available sessions.

        Returns:
            List[Session]: A list of all available sessions.
        """
        with self._lock:
            return list(self._sessions.values())

    def list_by_labels(self, labels: Dict[str, str]) -> SessionListResult:
        """
        Lists sessions filtered by the provided labels.
        It returns sessions that match all the specified labels.

        Args:
            labels (Dict[str, str]): A map of labels to filter sessions by.

        Returns:
            SessionListResult: Result containing a list of sessions that match the specified labels and request ID.
        """
        try:
            # Convert labels to JSON
            labels_json = json.dumps(labels)

            request = ListSessionRequest(
                authorization=f"Bearer {self.api_key}", labels=labels_json
            )

            response = self.client.list_session(request)

            # Extract request ID
            request_id = extract_request_id(response)

            response_map = response.to_map()
            body = response_map.get("body", {})

            # Check for errors in the response
            if isinstance(body, dict) and isinstance(body.get("Data"), dict) and body.get("Data", {}).get("IsError", False):
                return SessionListResult(
                    request_id=request_id,
                    success=False,
                    sessions=[],
                    error_message="Failed to list sessions by labels"
                )

            sessions = []
            response_data = body.get("Data")

            # Handle both list and dict responses
            if isinstance(response_data, list):
                # Data is a list of session objects
                for session_data in response_data:
                    if isinstance(session_data, dict):
                        session_id = session_data.get("SessionId")
                        if session_id:
                            # Check if we already have this session in our cache
                            with self._lock:
                                if session_id in self._sessions:
                                    session = self._sessions[session_id]
                                else:
                                    # Create a new session object
                                    session = Session(self, session_id)
                                    self._sessions[session_id] = session

                                sessions.append(session)
            elif isinstance(response_data, dict):
                # Data is a dictionary with session info
                session_id = response_data.get("SessionId")
                if session_id:
                    with self._lock:
                        if session_id in self._sessions:
                            session = self._sessions[session_id]
                        else:
                            session = Session(self, session_id)
                            self._sessions[session_id] = session

                        sessions.append(session)

            # Return SessionListResult with request ID
            return SessionListResult(request_id=request_id, success=True, sessions=sessions)

        except Exception as e:
            print("Error calling list_session:", e)
            return SessionListResult(
                request_id="",
                success=False,
                sessions=[],
                error_message=f"Failed to list sessions by labels: {e}"
            )

    def delete(self, session: Session) -> DeleteResult:
        """
        Delete a session by session object.

        Args:
            session (Session): The session to delete.

        Returns:
            DeleteResult: Result indicating success or failure and request ID.
        """
        try:
            # Delete the session and get the result
            delete_result = session.delete()

            with self._lock:
                self._sessions.pop(session.session_id, None)

            # Return the DeleteResult obtained from session.delete()
            return delete_result

        except Exception as e:
            print("Error deleting session:", e)
            return DeleteResult(
                request_id="",
                success=False,
                error_message=f"Failed to delete session {session.session_id}: {e}"
            )
