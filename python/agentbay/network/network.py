from typing import Optional
from agentbay.api.base_service import BaseService
from agentbay.exceptions import AgentBayError, NetworkError
from agentbay.model import ApiResponse, extract_request_id
from agentbay.api.models import CreateNetworkRequest, DescribeNetworkRequest


class NetworkInfo:
    """网络信息数据类"""
    
    def __init__(
        self,
        network_id: str = "",
        network_token: str = "",
        online: Optional[bool] = None,
    ):
        self.network_id = network_id
        self.network_token = network_token
        self.online = online

    @classmethod
    def from_create_response(cls, data: dict) -> "NetworkInfo":
        """从CreateNetwork响应创建NetworkInfo对象"""
        return cls(
            network_id=data.get("NetworkId", ""),
            network_token=data.get("NetworkToken", ""),
        )
    
    @classmethod
    def from_describe_response(cls, network_id: str, data: dict) -> "NetworkInfo":
        """从DescribeNetwork响应创建NetworkInfo对象"""
        return cls(
            network_id=network_id,
            online=data.get("Online"),
        )

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "network_id": self.network_id,
            "network_token": self.network_token,
            "online": self.online,
        }

    def __str__(self) -> str:
        online_status = "online" if self.online else "offline" if self.online is False else "unknown"
        return f"NetworkInfo(network_id='{self.network_id}', status='{online_status}')"


class CreateNetworkResult(ApiResponse):
    """创建网络操作的结果"""
    
    def __init__(
        self,
        request_id: str = "",
        success: bool = False,
        network_info: Optional[NetworkInfo] = None,
        error_message: str = "",
    ):
        super().__init__(request_id)
        self.success = success
        self.network_info = network_info
        self.error_message = error_message


class DescribeNetworkResult(ApiResponse):
    """描述网络操作的结果"""
    
    def __init__(
        self,
        request_id: str = "",
        success: bool = False,
        network_info: Optional[NetworkInfo] = None,
        error_message: str = "",
    ):
        super().__init__(request_id)
        self.success = success
        self.network_info = network_info
        self.error_message = error_message


class NetworkManager(BaseService):
    """
    网络管理服务，提供网络创建和查询功能
    """

    def _handle_error(self, e):
        """错误处理转换"""
        if isinstance(e, NetworkError):
            return e
        if isinstance(e, AgentBayError):
            return NetworkError(str(e))
        return e

    def create_network(self, image_id: str, network_id: Optional[str] = None) -> CreateNetworkResult:
        """
        创建网络
        
        Args:
            image_id: 镜像ID
            network_id: 网络ID
            
        Returns:
            CreateNetworkResult: 包含创建结果的对象
        """
        try:
            request = CreateNetworkRequest(
                authorization=f"Bearer {self.session.get_api_key()}",
                image_id=image_id,
                network_id=network_id,
            )
            
            response = self.session.get_client().create_network(request)
            request_id = extract_request_id(response)
            
            response_map = response.to_map()
            body = response_map.get("body", {})
            
            if body.get("Success", False):
                data = body.get("Data", {})
                network_info = NetworkInfo.from_create_response(data)
                
                return CreateNetworkResult(
                    request_id=request_id,
                    success=True,
                    network_info=network_info,
                )
            else:
                return CreateNetworkResult(
                    request_id=request_id,
                    success=False,
                    error_message=body.get("Message", "创建网络失败"),
                )
                
        except NetworkError as e:
            return CreateNetworkResult(request_id="", success=False, error_message=str(e))
        except Exception as e:
            return CreateNetworkResult(
                request_id="",
                success=False,
                error_message=f"创建网络失败: {e}",
            )

    def describe_network(self, network_id: str) -> DescribeNetworkResult:
        """
        查询网络详情
        
        Args:
            network_id: 网络ID
            
        Returns:
            DescribeNetworkResult: 包含网络详情的结果对象
        """
        try:
            request = DescribeNetworkRequest(
                authorization=f"Bearer {self.session.get_api_key()}",
                network_id=network_id,
            )
            
            response = self.session.get_client().describe_network(request)
            request_id = extract_request_id(response)
            
            response_map = response.to_map()
            body = response_map.get("body", {})
            
            if body.get("Success", False):
                data = body.get("Data", {})
                network_info = NetworkInfo.from_describe_response(network_id, data)
                
                return DescribeNetworkResult(
                    request_id=request_id,
                    success=True,
                    network_info=network_info,
                )
            else:
                return DescribeNetworkResult(
                    request_id=request_id,
                    success=False,
                    error_message=body.get("Message", "查询网络失败"),
                )
                
        except NetworkError as e:
            return DescribeNetworkResult(request_id="", success=False, error_message=str(e))
        except Exception as e:
            return DescribeNetworkResult(
                request_id="",
                success=False,
                error_message=f"查询网络失败: {e}",
            )

