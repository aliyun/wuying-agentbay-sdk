# NetworkManager API参考

`NetworkManager`类提供了网络管理功能，包括创建网络和查询网络详情。

## 类和方法

### NetworkManager

网络管理器类，提供网络相关操作的高级接口。

#### 方法

##### create_network(image_id: str, network_id: Optional[str] = None) -> CreateNetworkResult

创建一个新的网络环境。

**参数：**
- `image_id` (str): 用于创建网络环境的镜像ID
- `network_id` (Optional[str]): 可选的网络ID，如果不提供则系统自动生成

**返回：**
- `CreateNetworkResult`: 创建结果对象

**示例：**
```python
from agentbay import AgentBay

agent_bay = AgentBay()
session_result = agent_bay.create()
session = session_result.session

# 创建网络（自动生成网络ID）
result = session.network.create_network("linux_latest")
if result.success:
    print(f"网络创建成功: {result.network_info.network_id}")
    print(f"网络令牌: {result.network_info.network_token}")
else:
    print(f"网络创建失败: {result.error_message}")

# 创建网络（指定网络ID）
result = session.network.create_network("linux_latest", "my-custom-network-123")
if result.success:
    print(f"自定义网络创建成功: {result.network_info.network_id}")
    print(f"网络令牌: {result.network_info.network_token}")
else:
    print(f"网络创建失败: {result.error_message}")
```

##### describe_network(network_id: str) -> DescribeNetworkResult

查询指定网络的详细信息。

**参数：**
- `network_id` (str): 要查询的网络ID

**返回：**
- `DescribeNetworkResult`: 查询结果对象

**示例：**
```python
# 查询网络详情
result = session.network.describe_network("net-123456")
if result.success:
    info = result.network_info
    print(f"网络ID: {info.network_id}")
    print(f"在线状态: {'在线' if info.online else '离线'}")
else:
    print(f"查询失败: {result.error_message}")
```


## 数据类

### NetworkInfo

网络信息数据类，包含网络的详细信息。

**属性：**
- `network_id` (str): 网络ID
- `network_token` (str): 网络令牌
- `online` (Optional[bool]): 在线状态

**方法：**
- `from_create_response(data: dict) -> NetworkInfo`: 从CreateNetwork响应创建NetworkInfo对象
- `from_describe_response(network_id: str, data: dict) -> NetworkInfo`: 从DescribeNetwork响应创建NetworkInfo对象
- `to_dict() -> dict`: 转换为字典

### CreateNetworkResult

创建网络操作的结果类。

**属性：**
- `request_id` (str): 请求ID
- `success` (bool): 操作是否成功
- `network_info` (NetworkInfo): 网络信息（成功时）
- `error_message` (str): 错误消息（失败时）

### DescribeNetworkResult

查询网络操作的结果类。

**属性：**
- `request_id` (str): 请求ID
- `success` (bool): 操作是否成功
- `network_info` (NetworkInfo): 网络信息（成功时）
- `error_message` (str): 错误消息（失败时）

## 错误处理

网络操作可能抛出`NetworkError`异常。建议在使用时进行适当的错误处理：

```python
from agentbay import AgentBay, NetworkError

try:
    agent_bay = AgentBay()
    session_result = agent_bay.create()
    session = session_result.session
    
    result = session.network.create_network("linux_latest")
    if not result.success:
        print(f"操作失败: {result.error_message}")
        
except NetworkError as e:
    print(f"网络错误: {e}")
except Exception as e:
    print(f"其他错误: {e}")
```

## 完整示例

```python
#!/usr/bin/env python3
"""
AgentBay SDK - 网络管理示例
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
        
        # 1. 创建网络
        print("\n📡 创建网络...")
        create_result = session.network.create_network("linux_latest")
        
        if create_result.success:
            network_id = create_result.network_info.network_id
            print(f"✅ 网络创建成功: {network_id}")
            print(f"   网络令牌: {create_result.network_info.network_token}")
            
            # 2. 查询网络详情
            print(f"\n🔍 查询网络详情...")
            describe_result = session.network.describe_network(network_id)
            
            if describe_result.success:
                info = describe_result.network_info
                print("✅ 网络详情:")
                print(f"   网络ID: {info.network_id}")
                print(f"   在线状态: {'在线' if info.online else '离线'}")
            else:
                print(f"❌ 查询网络详情失败: {describe_result.error_message}")
            
            # 3. 检查网络状态
            print(f"\n⏱️ 检查网络状态...")
            describe_result2 = session.network.describe_network(network_id)
            if describe_result2.success:
                online_status = describe_result2.network_info.online
                print(f"网络状态: {'在线' if online_status else '离线'}")
                print(f"网络就绪: {'是' if online_status else '否'}")
            else:
                print(f"检查状态失败: {describe_result2.error_message}")
            
        else:
            print(f"❌ 网络创建失败: {create_result.error_message}")
            
    except Exception as e:
        print(f"❌ 示例执行失败: {e}")
    finally:
        # 清理资源
        if 'session' in locals():
            agent_bay.delete(session)
            print("\n🧹 会话已清理")

if __name__ == "__main__":
    main()
```
