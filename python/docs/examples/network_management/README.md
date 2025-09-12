# 网络管理示例

本示例演示了如何使用AgentBay SDK的网络管理功能。

## 功能特性

- **网络创建**: 基于指定镜像创建网络环境
- **网络查询**: 查询网络的详细信息和状态
- **状态检查**: 便捷的网络状态查询方法
- **就绪检查**: 检查网络是否已就绪可用
- **错误处理**: 完善的错误处理和异常管理

## 运行示例

1. 安装SDK:
```bash
pip install wuying-agentbay-sdk
```

2. 设置API密钥:
```bash
export AGENTBAY_API_KEY=your_api_key_here
```

3. 运行示例:
```bash
python main.py
```

## 代码说明

### 网络创建

```python
# 使用指定镜像创建网络
result = session.network.create_network("linux_latest")
if result.success:
    network_id = result.network_info.network_id
    print(f"网络创建成功: {network_id}")
```

### 网络查询

```python
# 查询网络详细信息
result = session.network.describe_network(network_id)
if result.success:
    info = result.network_info
    print(f"网络ID: {info.network_id}")
    print(f"在线状态: {'在线' if info.online else '离线'}")
```

### 状态检查

```python
# 查询网络状态
describe_result = session.network.describe_network(network_id)
if describe_result.success:
    online_status = describe_result.network_info.online
    print(f"网络状态: {'在线' if online_status else '离线'}")
    print(f"网络就绪: {'是' if online_status else '否'}")
else:
    print(f"查询失败: {describe_result.error_message}")
```

### 错误处理

```python
try:
    result = session.network.create_network("invalid_image")
    if not result.success:
        print(f"创建失败: {result.error_message}")
except NetworkError as e:
    print(f"网络错误: {e}")
```

## API参考

### NetworkManager类

- `create_network(image_id: str, network_id: Optional[str] = None) -> CreateNetworkResult`
- `describe_network(network_id: str) -> DescribeNetworkResult`

### 数据类

- `NetworkInfo`: 网络信息数据类
- `CreateNetworkResult`: 创建网络操作结果
- `DescribeNetworkResult`: 查询网络操作结果

## 使用场景

- **网络环境准备**: 为应用程序创建隔离的网络环境
- **网络状态监控**: 监控网络环境的运行状态
- **自动化部署**: 在自动化脚本中管理网络资源
- **多环境管理**: 为不同的应用场景创建专用网络

## 注意事项

1. **API密钥**: 确保设置了有效的AGENTBAY_API_KEY环境变量
2. **镜像ID**: 使用有效的镜像ID，如"linux_latest"
3. **网络就绪**: 创建网络后可能需要等待一段时间才能就绪
4. **资源清理**: 使用完毕后记得清理会话资源
5. **错误处理**: 建议在生产环境中添加完善的错误处理

## 常见问题

### Q: 支持哪些镜像ID？
A: 常用的镜像ID包括：
- `linux_latest`: 最新Linux环境
- `ubuntu_latest`: 最新Ubuntu环境
- 其他自定义镜像ID

### Q: 网络创建需要多长时间？
A: 通常需要几秒到几分钟不等，具体取决于镜像大小和网络配置复杂度。

### Q: 如何判断网络是否可用？
A: 使用`describe_network()`方法查询网络详情，检查`online`字段是否为True。

### Q: 创建失败的常见原因？
A: 
- 无效的镜像ID
- 配额不足
- 网络权限问题
- 区域不支持
