import unittest
from unittest.mock import Mock, patch

from agentbay.network import NetworkManager, NetworkInfo, CreateNetworkResult, DescribeNetworkResult
from agentbay.exceptions import NetworkError


class TestNetworkManager(unittest.TestCase):
    """单元测试：NetworkManager类"""

    def setUp(self):
        """设置测试环境"""
        self.mock_session = Mock()
        self.mock_session.get_api_key.return_value = "test-api-key"
        self.mock_session.get_session_id.return_value = "test-session-id"
        self.mock_session.get_client.return_value = Mock()
        
        self.network_manager = NetworkManager(self.mock_session)

    def test_network_info_creation(self):
        """测试NetworkInfo对象创建"""
        network_info = NetworkInfo(
            network_id="net-123456",
            network_token="token-123456",
            online=True,
        )
        
        self.assertEqual(network_info.network_id, "net-123456")
        self.assertEqual(network_info.network_token, "token-123456")
        self.assertTrue(network_info.online)

    def test_network_info_from_create_response(self):
        """测试从CreateNetwork响应创建NetworkInfo"""
        data = {
            "NetworkId": "net-123456",
            "NetworkToken": "token-123456",
        }
        
        network_info = NetworkInfo.from_create_response(data)
        
        self.assertEqual(network_info.network_id, "net-123456")
        self.assertEqual(network_info.network_token, "token-123456")
        self.assertIsNone(network_info.online)

    def test_network_info_from_describe_response(self):
        """测试从DescribeNetwork响应创建NetworkInfo"""
        data = {
            "Online": True,
        }
        
        network_info = NetworkInfo.from_describe_response("net-123456", data)
        
        self.assertEqual(network_info.network_id, "net-123456")
        self.assertTrue(network_info.online)
        self.assertEqual(network_info.network_token, "")

    def test_network_info_to_dict(self):
        """测试NetworkInfo转换为字典"""
        network_info = NetworkInfo(
            network_id="net-123456",
            network_token="token-123456",
            online=True,
        )
        
        result_dict = network_info.to_dict()
        
        self.assertEqual(result_dict["network_id"], "net-123456")
        self.assertEqual(result_dict["network_token"], "token-123456")
        self.assertTrue(result_dict["online"])

    @patch("agentbay.network.network.extract_request_id")
    def test_create_network_success(self, mock_extract_request_id):
        """测试创建网络成功"""
        # 设置模拟返回值
        mock_extract_request_id.return_value = "test-request-id"
        
        mock_response = Mock()
        mock_response.to_map.return_value = {
            "body": {
                "Success": True,
                "Data": {
                    "NetworkId": "net-123456",
                    "NetworkToken": "token-123456",
                }
            }
        }
        
        self.mock_session.get_client().create_network.return_value = mock_response
        
        # 调用测试方法
        result = self.network_manager.create_network("img-123456")
        
        # 验证结果
        self.assertIsInstance(result, CreateNetworkResult)
        self.assertTrue(result.success)
        self.assertEqual(result.request_id, "test-request-id")
        self.assertIsNotNone(result.network_info)
        self.assertEqual(result.network_info.network_id, "net-123456")
        self.assertEqual(result.network_info.network_token, "token-123456")

    @patch("agentbay.network.network.extract_request_id")
    def test_create_network_with_network_id_success(self, mock_extract_request_id):
        """测试使用指定NetworkId创建网络成功"""
        # 设置模拟返回值
        mock_extract_request_id.return_value = "test-request-id"
        
        mock_response = Mock()
        mock_response.to_map.return_value = {
            "body": {
                "Success": True,
                "Data": {
                    "NetworkId": "net-custom-123456",
                    "NetworkToken": "token-custom-123456",
                }
            }
        }
        
        self.mock_session.get_client().create_network.return_value = mock_response
        
        # 调用测试方法，指定network_id
        result = self.network_manager.create_network("img-123456", "net-custom-123456")
        
        # 验证结果
        self.assertIsInstance(result, CreateNetworkResult)
        self.assertTrue(result.success)
        self.assertEqual(result.request_id, "test-request-id")
        self.assertIsNotNone(result.network_info)
        self.assertEqual(result.network_info.network_id, "net-custom-123456")
        self.assertEqual(result.network_info.network_token, "token-custom-123456")
        
        # 验证调用参数
        call_args = self.mock_session.get_client().create_network.call_args[0][0]
        self.assertEqual(call_args.image_id, "img-123456")
        self.assertEqual(call_args.network_id, "net-custom-123456")

    @patch("agentbay.network.network.extract_request_id")
    def test_create_network_failure(self, mock_extract_request_id):
        """测试创建网络失败"""
        mock_extract_request_id.return_value = "test-request-id"
        
        mock_response = Mock()
        mock_response.to_map.return_value = {
            "body": {
                "Success": False,
                "Message": "Invalid image ID"
            }
        }
        
        self.mock_session.get_client().create_network.return_value = mock_response
        
        result = self.network_manager.create_network("invalid-img-id")
        
        self.assertIsInstance(result, CreateNetworkResult)
        self.assertFalse(result.success)
        self.assertEqual(result.request_id, "test-request-id")
        self.assertEqual(result.error_message, "Invalid image ID")
        self.assertIsNone(result.network_info)

    @patch("agentbay.network.network.extract_request_id")
    def test_describe_network_success(self, mock_extract_request_id):
        """测试查询网络成功"""
        mock_extract_request_id.return_value = "test-request-id"
        
        mock_response = Mock()
        mock_response.to_map.return_value = {
            "body": {
                "Success": True,
                "Data": {
                    "Online": True,
                }
            }
        }
        
        self.mock_session.get_client().describe_network.return_value = mock_response
        
        result = self.network_manager.describe_network("net-123456")
        
        self.assertIsInstance(result, DescribeNetworkResult)
        self.assertTrue(result.success)
        self.assertEqual(result.request_id, "test-request-id")
        self.assertIsNotNone(result.network_info)
        self.assertEqual(result.network_info.network_id, "net-123456")
        self.assertTrue(result.network_info.online)

    @patch("agentbay.network.network.extract_request_id")
    def test_describe_network_failure(self, mock_extract_request_id):
        """测试查询网络失败"""
        mock_extract_request_id.return_value = "test-request-id"
        
        mock_response = Mock()
        mock_response.to_map.return_value = {
            "body": {
                "Success": False,
                "Message": "Network not found"
            }
        }
        
        self.mock_session.get_client().describe_network.return_value = mock_response
        
        result = self.network_manager.describe_network("net-not-exists")
        
        self.assertIsInstance(result, DescribeNetworkResult)
        self.assertFalse(result.success)
        self.assertEqual(result.request_id, "test-request-id")
        self.assertEqual(result.error_message, "Network not found")
        self.assertIsNone(result.network_info)


    def test_create_network_exception(self):
        """测试创建网络时发生异常"""
        self.mock_session.get_client().create_network.side_effect = Exception("Network error")
        
        result = self.network_manager.create_network("img-123456")
        
        self.assertIsInstance(result, CreateNetworkResult)
        self.assertFalse(result.success)
        self.assertIn("创建网络失败", result.error_message)

    def test_describe_network_exception(self):
        """测试查询网络时发生异常"""
        self.mock_session.get_client().describe_network.side_effect = Exception("Network error")
        
        result = self.network_manager.describe_network("net-123456")
        
        self.assertIsInstance(result, DescribeNetworkResult)
        self.assertFalse(result.success)
        self.assertIn("查询网络失败", result.error_message)


if __name__ == '__main__':
    unittest.main()
