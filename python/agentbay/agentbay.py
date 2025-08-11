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
from agentbay.config import BROWSER_DATA_PATH


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

    def _safe_serialize(self, obj):
        """
        Helper function to serialize objects to JSON-compatible format.
        
        Args:
            obj: The object to serialize.
            
        Returns:
            JSON-serializable representation of the object.
        """
        try:
            if isinstance(obj, Enum):
                return obj.value
            elif hasattr(obj, "__dict__") and callable(obj.__dict__):
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

            # Add McpPolicyId if specified
            if hasattr(params, "mcp_policy_id") and params.mcp_policy_id:
                request.mcp_policy_id = params.mcp_policy_id

            # Add VPC resource if specified
            request.vpc_resource = params.is_vpc

            # Flag to indicate if we need to wait for context synchronization
            has_persistence_data = False

            # Add context_syncs if provided
            if hasattr(params, "context_syncs") and params.context_syncs:
                from agentbay.api.models import (
                    CreateMcpSessionRequestPersistenceDataList,
                )

                persistence_data_list = []
                for cs in params.context_syncs:
                    policy_json = None
                    if cs.policy is not None:
                        # Serialize policy to JSON string
                        import json as _json

                        policy_json = _json.dumps(
                            cs.policy, default=self._safe_serialize, ensure_ascii=False
                        )
                    persistence_data_list.append(
                        CreateMcpSessionRequestPersistenceDataList(
                            context_id=cs.context_id, path=cs.path, policy=policy_json
                        )
                    )
                request.persistence_data_list = persistence_data_list
                has_persistence_data = len(persistence_data_list) > 0

            # Add BrowserContext as a ContextSync if provided
            if hasattr(params, "browser_context") and params.browser_context:
                from agentbay.api.models import (
                    CreateMcpSessionRequestPersistenceDataList,
                )
                from agentbay.context_sync import SyncPolicy, UploadPolicy, WhiteList, BWList

                # Create a new SyncPolicy with default values for browser context
                upload_policy = UploadPolicy(auto_upload=params.browser_context.auto_upload)
                
                # Create BWList with white lists for browser data paths
                white_lists = [
                    WhiteList(path="/Local State", exclude_paths=[]),
                    WhiteList(path="/Default/Cookies", exclude_paths=[]),
                    WhiteList(path="/Default/Cookies-journal", exclude_paths=[])
                ]
                bw_list = BWList(white_lists=white_lists)
                
                sync_policy = SyncPolicy(upload_policy=upload_policy, bw_list=bw_list)

                # Serialize policy to JSON string
                import json as _json

                policy_json = _json.dumps(
                    sync_policy, default=self._safe_serialize, ensure_ascii=False
                )

                # Create browser context sync item
                browser_context_sync = CreateMcpSessionRequestPersistenceDataList(
                    context_id=params.browser_context.context_id,
                    path=BROWSER_DATA_PATH,  # Using a constant path for browser data
                    policy=policy_json
                )

                # Add to persistence data list or create new one if not exists
                if not hasattr(request, 'persistence_data_list') or request.persistence_data_list is None:
                    request.persistence_data_list = []
                request.persistence_data_list.append(browser_context_sync)
                has_persistence_data = True

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

            # Check if the session creation was successful
            if data.get("Success") is False:
                error_msg = data.get("ErrMsg", "Session creation failed")
                return SessionResult(
                    request_id=request_id,
                    success=False,
                    error_message=error_msg,
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

            # Create Session object
            from agentbay.session import Session

            session = Session(self, session_id)
            if resource_url is not None:
                session.resource_url = resource_url

            # Set VPC-related information from response
            session.is_vpc = params.is_vpc
            if data.get("NetworkInterfaceIp"):
                session.network_interface_ip = data["NetworkInterfaceIp"]
            if data.get("HttpPort"):
                session.http_port = data["HttpPort"]

            # Store image_id used for this session
            session.image_id = params.image_id

            with self._lock:
                self._sessions[session_id] = session

            # For VPC sessions, automatically fetch MCP tools information
            if params.is_vpc:
                print("VPC session detected, automatically fetching MCP tools...")
                try:
                    tools_result = session.list_mcp_tools()
                    print(f"Successfully fetched {len(tools_result.tools)} MCP tools for VPC session (RequestID: {tools_result.request_id})")
                except Exception as e:
                    print(f"Warning: Failed to fetch MCP tools for VPC session: {e}")
                    # Continue with session creation even if tools fetch fails

            # If we have persistence data, wait for context synchronization
            if has_persistence_data:
                print("Waiting for context synchronization to complete...")
                
                # Wait for context synchronization to complete
                max_retries = 150  # Maximum number of retries
                retry_interval = 2  # Seconds to wait between retries
                
                import time
                for retry in range(max_retries):
                    # Get context status data
                    info_result = session.context.info()
                    
                    # Check if all context items have status "Success" or "Failed"
                    all_completed = True
                    has_failure = False
                    
                    for item in info_result.context_status_data:
                        print(f"Context {item.context_id} status: {item.status}, path: {item.path}")
                        
                        if item.status != "Success" and item.status != "Failed":
                            all_completed = False
                            break
                        
                        if item.status == "Failed":
                            has_failure = True
                            print(f"Context synchronization failed for {item.context_id}: {item.error_message}")
                    
                    if all_completed or not info_result.context_status_data:
                        if has_failure:
                            print("Context synchronization completed with failures")
                        else:
                            print("Context synchronization completed successfully")
                        break
                    
                    print(f"Waiting for context synchronization, attempt {retry+1}/{max_retries}")
                    time.sleep(retry_interval)

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

    def delete(self, session: Session, sync_context: bool = False) -> DeleteResult:
        """
        Delete a session by session object.

        Args:
            session (Session): The session to delete.
            sync_context (bool): Whether to sync context data (trigger file uploads) 
                before deleting the session. Defaults to False.

        Returns:
            DeleteResult: Result indicating success or failure and request ID.
        """
        try:
            # Delete the session and get the result
            delete_result = session.delete(sync_context=sync_context)

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
