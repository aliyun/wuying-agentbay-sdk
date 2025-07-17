import json
import os
from enum import Enum
from threading import Lock
from typing import Dict, List, Optional, Union

from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_openapi.exceptions._client import ClientException

from agentbay.api.client import Client as mcp_client
from agentbay.api.models import CreateMcpSessionRequest, ListSessionRequest
from agentbay.config import load_config
from agentbay.context import ContextService
from agentbay.model import (
    DeleteResult,
    SessionListResult,
    SessionResult,
    extract_request_id,
)
from agentbay.session import Session
from agentbay.session_params import CreateSessionParams, ListSessionParams
from typing import Optional
from agentbay.context_sync import ContextSync


class Config:
    def __init__(self, region_id: str, endpoint: str, timeout_ms: int):
        self.region_id = region_id
        self.endpoint = endpoint
        self.timeout_ms = timeout_ms


class AgentBay:
    """
    AgentBay represents the main client for interacting with the AgentBay cloud runtime
    environment.
    """

    def __init__(self, api_key: str = "", cfg: Optional[Config] = None):
        if not api_key:
            api_key = os.getenv("AGENTBAY_API_KEY")
            if not api_key:
                raise ValueError(
                    "API key is required. Provide it as a parameter or set the "
                    "AGENTBAY_API_KEY environment variable"
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
            params (Optional[CreateSessionParams], optional): Parameters for
              creating the session.Defaults to None.

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
            # Add context_syncs if provided
            if hasattr(params, "context_syncs") and params.context_syncs:
                from agentbay.api.models import (
                    CreateMcpSessionRequestPersistenceDataList,
                )

                persistence_data_list = []
                for cs in params.context_syncs:
                    policy_json = None
                    if cs.policy is not None:
                        # policy 需序列化为 JSON 字符串
                        import json as _json

                        def safe_serialize(obj):
                            try:
                                if isinstance(obj, Enum):
                                    return obj.value
                                elif hasattr(obj, "__dict__") and callable(
                                    obj.__dict__
                                ):
                                    return obj.__dict__()
                                elif hasattr(obj, "__dict__"):
                                    return obj.__dict__
                                elif hasattr(obj, "to_map"):
                                    return obj.to_map()
                                elif hasattr(obj, "to_dict"):
                                    return obj.to_dict()
                                else:
                                    return str(obj)
                            except:
                                return str(obj)

                        policy_json = _json.dumps(
                            cs.policy, default=safe_serialize, ensure_ascii=False
                        )
                    persistence_data_list.append(
                        CreateMcpSessionRequestPersistenceDataList(
                            context_id=cs.context_id, path=cs.path, policy=policy_json
                        )
                    )
                request.persistence_data_list = persistence_data_list

            # Add labels if provided
            if params.labels:
                # Convert labels to JSON string
                request.labels = json.dumps(params.labels)

            if params.image_id:
                request.image_id = params.image_id
            try:
                req_map = request.to_map()
                if "Authorization" in req_map and isinstance(
                    req_map["Authorization"], str
                ):
                    auth = req_map["Authorization"]
                    if len(auth) > 12:
                        req_map["Authorization"] = (
                            auth[:6] + "*" * (len(auth) - 10) + auth[-4:]
                        )
                    else:
                        req_map["Authorization"] = auth[:2] + "****" + auth[-2:]
                print("CreateMcpSessionRequest body:")
                print(json.dumps(req_map, ensure_ascii=False, indent=2))
            except Exception:
                print(f"CreateMcpSessionRequest: {request}")
            response = self.client.create_mcp_session(request)
            try:
                print("Response body:")
                print(
                    json.dumps(
                        response.to_map().get("body", {}), ensure_ascii=False, indent=2
                    )
                )
            except Exception:
                print(f"Response: {response}")

            # Extract request ID
            request_id = extract_request_id(response)

            session_data = response.to_map()

            if not isinstance(session_data, dict):
                return SessionResult(
                    request_id=request_id,
                    success=False,
                    error_message="Invalid response format: expected a dictionary",
                )

            body = session_data.get("body", {})
            if not isinstance(body, dict):
                return SessionResult(
                    request_id=request_id,
                    success=False,
                    error_message="Invalid response format: "
                    "'body' field is not a dictionary",
                )

            data = body.get("Data", {})
            if not isinstance(data, dict):
                return SessionResult(
                    request_id=request_id,
                    success=False,
                    error_message="Invalid response format: "
                    "'Data' field is not a dictionary",
                )

            session_id = data.get("SessionId")
            if not session_id:
                return SessionResult(
                    request_id=request_id,
                    success=False,
                    error_message="SessionId not found in response",
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
                error_message=f"Failed to create session: {e}",
            )
        except Exception as e:
            print("Error calling create_mcp_session:", e)
            return SessionResult(
                request_id="",
                success=False,
                error_message=f"Unexpected error creating session: {e}",
            )

    def list(self) -> List[Session]:
        """
        List all available sessions.

        Returns:
            List[Session]: A list of all available sessions.
        """
        with self._lock:
            return list(self._sessions.values())

    def list_by_labels(
        self, params: Optional[Union[ListSessionParams, Dict[str, str]]] = None
    ) -> SessionListResult:
        """
        Lists sessions filtered by the provided labels with pagination support.
        It returns sessions that match all the specified labels.

        Args:
            params (Optional[Union[ListSessionParams, Dict[str, str]]], optional):
                Parameters for listing sessions or a dictionary of labels.
                Defaults to None.

        Returns:
            SessionListResult: Result containing a list of sessions and pagination
            information.
        """
        try:
            # Use default params if none provided
            if params is None:
                params = ListSessionParams()
            # Convert dict to ListSessionParams if needed
            elif isinstance(params, dict):
                params = ListSessionParams(labels=params)

            # Convert labels to JSON
            labels_json = json.dumps(params.labels)

            # Create request with pagination parameters
            request = ListSessionRequest(
                authorization=f"Bearer {self.api_key}",
                labels=labels_json,
                max_results=str(
                    params.max_results
                ),  # Convert to string as expected by the API
            )

            # Add next_token if provided
            if params.next_token:
                request.next_token = params.next_token

            print("API Call: list_session")
            print(f"Request: Labels={labels_json}, MaxResults={params.max_results}")
            if request.next_token:
                print(f"NextToken={request.next_token}")

            # Make the API call
            response = self.client.list_session(request)

            # Extract request ID
            request_id = extract_request_id(response)

            response_map = response.to_map()
            body = response_map.get("body", {})

            # Check for errors in the response
            if isinstance(body, dict) and body.get("Success") is False:
                # Extract error message from Message field if present, otherwise use Code
                error_message = body.get("Message", body.get("Code", "Unknown error"))
                return SessionListResult(
                    request_id=request_id,
                    success=False,
                    error_message=f"Failed to list sessions by labels: {error_message}",
                    sessions=[],
                    next_token="",
                    max_results=params.max_results,
                    total_count=0,
                )

            sessions = []
            next_token = ""
            max_results = request.max_results
            total_count = 0

            try:
                print("Response body:")
                print(json.dumps(body, ensure_ascii=False, indent=2))
            except Exception:
                print(f"Response: {body}")

            # Extract pagination information
            if isinstance(body, dict):
                next_token = body.get("NextToken", "")
                max_results = int(body.get("MaxResults", 0))
                total_count = int(body.get("TotalCount", 0))

            # Extract session data
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

            # Return SessionListResult with request ID and pagination info
            return SessionListResult(
                request_id=request_id,
                success=True,
                sessions=sessions,
                next_token=next_token,
                max_results=max_results,
                total_count=total_count,
            )

        except Exception as e:
            print("Error calling list_session:", e)
            return SessionListResult(
                request_id="",
                success=False,
                sessions=[],
                error_message=f"Failed to list sessions by labels: {e}",
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
                error_message=f"Failed to delete session {session.session_id}: {e}",
            )
