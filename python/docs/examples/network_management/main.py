#!/usr/bin/env python3
"""
AgentBay SDK - 网络管理功能示例

演示如何使用AgentBay SDK进行网络管理，包括：
- 创建网络环境
- 查询网络详情
- 检查网络状态
- 网络就绪状态检查
"""

from agentbay import AgentBay
import time


def main():
    print("🚀 AgentBay 网络管理示例")
    
    agent_bay = AgentBay()
    
    try:
        # 创建会话
        session_result = agent_bay.create()
        if not session_result.success:
            print(f"❌ 创建会话失败: {session_result.error_message}")
            return
            
        session = session_result.session
        print(f"✅ 会话创建成功: {session.session_id}")
        
        # 1. 创建网络（自动生成网络ID）
        print("\n📡 创建网络环境...")
        create_result = session.network.create_network("linux_latest")
        
        if create_result.success:
            network_id = create_result.network_info.network_id
            print(f"✅ 网络创建成功!")
            print(f"   网络ID: {network_id}")
            print(f"   网络令牌: {create_result.network_info.network_token}")
            
            # 1.5. 演示使用自定义网络ID创建网络
            print(f"\n📡 演示使用自定义网络ID创建网络...")
            custom_network_id = "my-custom-network-demo-123"
            custom_create_result = session.network.create_network("linux_latest", custom_network_id)
            
            if custom_create_result.success:
                print(f"✅ 自定义网络创建成功!")
                print(f"   自定义网络ID: {custom_create_result.network_info.network_id}")
                print(f"   网络令牌: {custom_create_result.network_info.network_token}")
            else:
                print(f"❌ 自定义网络创建失败: {custom_create_result.error_message}")
            
            # 2. 查询网络详情
            print(f"\n🔍 查询网络详情...")
            describe_result = session.network.describe_network(network_id)
            
            if describe_result.success:
                info = describe_result.network_info
                print("✅ 网络详细信息:")
                print(f"   网络ID: {info.network_id}")
                print(f"   在线状态: {'在线' if info.online else '离线'}")
            else:
                print(f"❌ 查询网络详情失败: {describe_result.error_message}")
            
            # 3. 再次检查网络状态
            print(f"\n⏱️ 再次检查网络状态...")
            describe_result2 = session.network.describe_network(network_id)
            if describe_result2.success:
                online_status = describe_result2.network_info.online
                print(f"当前网络状态: {'在线' if online_status else '离线'}")
                print(f"网络在线状态: {'✅ 在线' if online_status else '⏳ 离线'}")
                print(f"网络就绪状态: {'✅ 就绪' if online_status else '⏳ 未就绪'}")
                
                # 4. 如果网络未在线，等待一段时间后再次检查
                if not online_status:
                    print("⏳ 网络尚未上线，等待5秒后再次检查...")
                    time.sleep(5)
                    
                    describe_result3 = session.network.describe_network(network_id)
                    if describe_result3.success:
                        new_online_status = describe_result3.network_info.online
                        print(f"更新后的网络状态: {'在线' if new_online_status else '离线'}")
                        print(f"更新后的在线状态: {'✅ 在线' if new_online_status else '⏳ 仍离线'}")
                    else:
                        print(f"❌ 再次查询失败: {describe_result3.error_message}")
            else:
                print(f"❌ 查询网络状态失败: {describe_result2.error_message}")
            
            # 7. 演示错误处理 - 查询不存在的网络
            print(f"\n🔍 演示错误处理 - 查询不存在的网络...")
            fake_network_id = "net-nonexistent-12345"
            error_result = session.network.describe_network(fake_network_id)
            
            if error_result.success:
                print("⚠️ 意外成功 - 这不应该发生")
            else:
                print(f"✅ 预期的错误: {error_result.error_message}")
            
        else:
            print(f"❌ 网络创建失败: {create_result.error_message}")
            
            # 即使创建失败，我们也可以演示其他功能
            print(f"\n🔍 演示查询不存在网络的错误处理...")
            fake_result = session.network.describe_network("net-fake-123456")
            print(f"预期错误: {fake_result.error_message}")
            
    except Exception as e:
        print(f"❌ 示例执行失败: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # 清理资源
        if 'session' in locals():
            try:
                agent_bay.delete(session)
                print("\n🧹 会话已清理")
            except Exception as e:
                print(f"⚠️ 清理会话时出错: {e}")


def demonstrate_network_info_usage():
    """演示NetworkInfo类的使用"""
    print("\n📋 NetworkInfo类使用演示:")
    
    # 从字典创建NetworkInfo
    data = {
        "NetworkId": "net-example-123456",
        "Status": "running",
        "VpcId": "vpc-example-123456",
        "SubnetId": "subnet-example-123456",
        "SecurityGroupId": "sg-example-123456",
        "ImageId": "linux_latest",
        "CreatedTime": "2025-01-01T00:00:00Z",
        "UpdatedTime": "2025-01-01T00:01:00Z",
        "RegionId": "cn-shanghai",
    }
    
    from agentbay.network import NetworkInfo
    
    network_info = NetworkInfo.from_dict(data)
    print(f"从字典创建: {network_info}")
    
    # 转换为字典
    info_dict = network_info.to_dict()
    print("转换为字典:")
    for key, value in info_dict.items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
    demonstrate_network_info_usage()
