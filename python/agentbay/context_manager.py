from typing import Optional
from agentbay.api.models import GetContextInfoRequest, SyncContextRequest
from agentbay.model.response import ApiResponse, extract_request_id
import json

class ContextInfoResult(ApiResponse):
    def __init__(self, request_id: str = "", context_status: str = ""):
        super().__init__(request_id)
        self.context_status = context_status

class ContextSyncResult(ApiResponse):
    def __init__(self, request_id: str = "", success: bool = False):
        super().__init__(request_id)
        self.success = success

class ContextManager:
    def __init__(self, session):
        self.session = session

    def info(self, context_id: Optional[str] = None, path: Optional[str] = None, task_type: Optional[str] = None) -> ContextInfoResult:
        request = GetContextInfoRequest(
            authorization=f"Bearer {self.session.get_api_key()}",
            session_id=self.session.get_session_id(),
        )
        if context_id:
            request.context_id = context_id
        if path:
            request.path = path
        if task_type:
            request.task_type = task_type
        print("API Call: GetContextInfo")
        print(f"Request: SessionId={self.session.get_session_id()}, ContextId={context_id}, Path={path}, TaskType={task_type}")
        response = self.session.get_client().get_context_info(request)
        try:
            print("Response body:")
            print(json.dumps(response.to_map().get("body", {}), ensure_ascii=False, indent=2))
        except Exception:
            print(f"Response: {response}")
        request_id = extract_request_id(response)
        response_map = response.to_map()
        context_status = ""
        if isinstance(response_map, dict):
            body = response_map.get("body", {})
            data = body.get("Data", {})
            context_status = data.get("ContextStatus", "")
        return ContextInfoResult(request_id=request_id, context_status=context_status)

    def sync(self, context_id: Optional[str] = None, path: Optional[str] = None, mode: Optional[str] = None) -> ContextSyncResult:
        request = SyncContextRequest(
            authorization=f"Bearer {self.session.get_api_key()}",
            session_id=self.session.get_session_id(),
        )
        if context_id:
            request.context_id = context_id
        if path:
            request.path = path
        if mode:
            request.mode = mode
        print("API Call: SyncContext")
        print(f"Request: SessionId={self.session.get_session_id()}, ContextId={context_id}, Path={path}, Mode={mode}")
        response = self.session.get_client().sync_context(request)
        try:
            print("Response from SyncContext:")
            print(json.dumps(response.to_map(), ensure_ascii=False, indent=2))
        except Exception:
            print(f"Response from SyncContext: {response}")
        request_id = extract_request_id(response)
        response_map = response.to_map()
        success = False
        if isinstance(response_map, dict):
            body = response_map.get("body", {})
            success = body.get("Success", False)
        return ContextSyncResult(request_id=request_id, success=success) 