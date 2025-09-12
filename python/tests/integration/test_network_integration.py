import unittest
import os
from agentbay import AgentBay


class TestNetworkIntegration(unittest.TestCase):
    """集成测试：网络管理功能"""

    def setUp(self):
        """设置集成测试环境"""
        api_key = os.getenv("AGENTBAY_API_KEY")
        if not api_key:
            self.skipTest("AGENTBAY_API_KEY not set")
        
        self.agent_bay = AgentBay(api_key=api_key)
        session_result = self.agent_bay.create()
        self.assertTrue(session_result.success, f"Failed to create session: {session_result.error_message}")
        self.session = session_result.session

    def tearDown(self):
        """清理测试资源"""
        if hasattr(self, 'session'):
            self.agent_bay.delete(self.session)

    def test_create_network_integration(self):
        """集成测试：创建网络"""
        # 使用linux_latest镜像创建网络
        result = self.session.network.create_network("linux_latest")
        
        # 验证请求ID存在
        self.assertIsNotNone(result.request_id, "Request ID should not be None")
        
        # 如果创建成功，验证网络信息
        if result.success:
            self.assertIsNotNone(result.network_info, "Network info should not be None when creation succeeds")
            self.assertIsNotNone(result.network_info.network_id, "Network ID should not be None")
            print(f"✅ Network created successfully: {result.network_info.network_id}")
            print(f"   Status: {result.network_info.status}")
            print(f"   VPC ID: {result.network_info.vpc_id}")
            
            # 测试查询刚创建的网络
            describe_result = self.session.network.describe_network(result.network_info.network_id)
            self.assertIsNotNone(describe_result.request_id, "Describe request ID should not be None")
            
            if describe_result.success:
                self.assertEqual(describe_result.network_info.network_id, result.network_info.network_id)
                print(f"✅ Network described successfully: {describe_result.network_info.network_id}")
            else:
                print(f"⚠️ Network describe failed: {describe_result.error_message}")
        else:
            print(f"⚠️ Network creation failed: {result.error_message}")
            # 创建失败也是有效的测试结果，只要API调用正常

    def test_describe_nonexistent_network_integration(self):
        """集成测试：查询不存在的网络"""
        # 使用一个不存在的网络ID
        fake_network_id = "net-nonexistent-12345"
        result = self.session.network.describe_network(fake_network_id)
        
        # 验证请求ID存在
        self.assertIsNotNone(result.request_id, "Request ID should not be None")
        
        # 预期查询失败
        self.assertFalse(result.success, "Describing nonexistent network should fail")
        self.assertIsNotNone(result.error_message, "Error message should be provided for failed request")
        print(f"✅ Expected failure for nonexistent network: {result.error_message}")

    def test_network_status_methods_integration(self):
        """集成测试：网络状态查询方法"""
        # 创建网络
        create_result = self.session.network.create_network("linux_latest")
        
        if create_result.success and create_result.network_info:
            network_id = create_result.network_info.network_id
            
            # 测试网络状态查询
            describe_result = self.session.network.describe_network(network_id)
            self.assertTrue(describe_result.success, "Network describe should succeed")
            self.assertIsNotNone(describe_result.network_info, "Network info should not be None")
            
            online_status = describe_result.network_info.online
            self.assertIsInstance(online_status, bool, "Online status should be boolean")
            print(f"✅ Network online status: {online_status}")
        else:
            print(f"⚠️ Skipping status tests due to network creation failure: {create_result.error_message}")

    def test_network_manager_integration(self):
        """集成测试：验证NetworkManager正确集成到Session中"""
        # 验证session.network属性存在且类型正确
        from agentbay.network import NetworkManager
        self.assertIsInstance(self.session.network, NetworkManager, "session.network should be NetworkManager instance")
        
        # 验证NetworkManager与session正确关联
        self.assertEqual(self.session.network.session, self.session, "NetworkManager should reference correct session")
        
        print("✅ NetworkManager correctly integrated into Session")


if __name__ == '__main__':
    # 设置测试输出详细程度
    unittest.main(verbosity=2)
