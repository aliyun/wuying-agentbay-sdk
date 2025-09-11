from typing import Optional, List, Dict, Any
from agentbay.api.models import GetContextInfoRequest, SyncContextRequest
from agentbay.model.response import ApiResponse, extract_request_id
from .logger import get_logger, log_api_call, log_api_response
import json

# Initialize logger for this module
logger = get_logger("context_manager")


class ContextStatusData:
    def __init__(
        self,
        context_id: str = "",
        path: str = "",
        error_message: str = "",
        status: str = "",
        start_time: int = 0,
        finish_time: int = 0,
        task_type: str = "",
    ):
        self.context_id = context_id
        self.path = path
        self.error_message = error_message
        self.status = status
        self.start_time = start_time
        self.finish_time = finish_time
        self.task_type = task_type

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ContextStatusData":
        return cls(
            context_id=data.get("contextId", ""),
            path=data.get("path", ""),
            error_message=data.get("errorMessage", ""),
            status=data.get("status", ""),
            start_time=data.get("startTime", 0),
            finish_time=data.get("finishTime", 0),
            task_type=data.get("taskType", ""),
        )


class ContextInfoResult(ApiResponse):
    def __init__(
        self, request_id: str = "", context_status_data: List[ContextStatusData] = None
    ):
        super().__init__(request_id)
        self.context_status_data = context_status_data or []


class ContextSyncResult(ApiResponse):
    def __init__(self, request_id: str = "", success: bool = False):
        super().__init__(request_id)
        self.success = success


class ContextManager:
    def __init__(self, session):
        self.session = session

    def info(
        self,
        context_id: Optional[str] = None,
        path: Optional[str] = None,
        task_type: Optional[str] = None,
    ) -> ContextInfoResult:
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
        log_api_call(
            "GetContextInfo",
            f"SessionId={self.session.get_session_id()}, ContextId={context_id}, Path={path}, TaskType={task_type}"
        )
        response = self.session.get_client().get_context_info(request)
        try:
            response_body = json.dumps(
                response.to_map().get("body", {}), ensure_ascii=False, indent=2
            )
            log_api_response(response_body)
        except Exception:
            logger.debug(f"📥 Response: {response}")
        request_id = extract_request_id(response)
        response_map = response.to_map()

        context_status_data = []
        if isinstance(response_map, dict):
            body = response_map.get("body", {})
            data = body.get("Data", {})
            context_status_str = data.get("ContextStatus", "")

            # Parse the context status data
            if context_status_str:
                try:
                    # First, parse the outer array
                    status_items = json.loads(context_status_str)
                    for item in status_items:
                        if item.get("type") == "data":
                            # Parse the inner data string
                            data_items = json.loads(item.get("data", "[]"))
                            for data_item in data_items:
                                context_status_data.append(
                                    ContextStatusData.from_dict(data_item)
                                )
                except json.JSONDecodeError as e:
                    logger.error(f"❌ Error parsing context status: {e}")
                except Exception as e:
                    logger.error(f"❌ Unexpected error parsing context status: {e}")

        return ContextInfoResult(
            request_id=request_id, context_status_data=context_status_data
        )

    def sync(
        self,
        context_id: Optional[str] = None,
        path: Optional[str] = None,
        mode: Optional[str] = None,
    ) -> ContextSyncResult:
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
        log_api_call(
            "SyncContext",
            f"SessionId={self.session.get_session_id()}, ContextId={context_id}, Path={path}, Mode={mode}"
        )
        response = self.session.get_client().sync_context(request)
        try:
            response_body = json.dumps(
                response.to_map().get("body", {}), ensure_ascii=False, indent=2
            )
            log_api_response(response_body)
        except Exception:
            logger.debug(f"📥 Response: {response}")
        request_id = extract_request_id(response)
        response_map = response.to_map()
        success = False
        if isinstance(response_map, dict):
            body = response_map.get("body", {})
            success = body.get("Success", False)
        return ContextSyncResult(request_id=request_id, success=success)
