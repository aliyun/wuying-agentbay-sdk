#!/usr/bin/env python3
"""
AgentBay SDK - 数据持久化示例

本示例展示了如何使用AgentBay SDK的数据持久化功能，包括：
- 上下文管理
- 数据同步
- 跨会话数据共享
- 版本控制
"""

import json
import time
from agentbay import AgentBay, ContextSync, SyncPolicy, CreateSessionParams

def main():
    """主函数"""
    print("🗄️ AgentBay 数据持久化示例")
    
    # 初始化AgentBay客户端
    agent_bay = AgentBay()
    
    try:
        # 1. 上下文管理示例
        context_management_example(agent_bay)
        
        # 2. 数据同步示例
        data_sync_example(agent_bay)
        
        # 3. 跨会话数据共享示例
        cross_session_sharing_example(agent_bay)
        
        # 4. 版本控制示例
        version_control_example(agent_bay)
        
    except Exception as e:
        print(f"❌ 示例执行失败: {e}")
    
    print("✅ 数据持久化示例执行完成")

def context_management_example(agent_bay):
    """上下文管理示例"""
    print("\n📦 === 上下文管理示例 ===")
    
    # 创建或获取上下文
    print("🔄 创建项目上下文...")
    context_result = agent_bay.context.get("demo-project", create=True)
    if context_result.is_error:
        print(f"❌ 上下文创建失败: {context_result.error}")
        return None
    
    context = context_result.context
    print(f"✅ 上下文创建成功: {context.id}")
    
    # 上传文件到上下文
    project_files = {
        "/project/config.json": json.dumps({
            "name": "Demo Project",
            "version": "1.0.0",
            "description": "AgentBay数据持久化演示项目"
        }, indent=2),
        "/project/README.md": """# Demo Project

这是一个AgentBay数据持久化的演示项目。

## 功能特性
- 数据持久化
- 跨会话共享
- 版本控制
""",
        "/project/data/sample.txt": "这是一个示例数据文件。"
    }
    
    print("🔄 上传项目文件...")
    for file_path, content in project_files.items():
        result = agent_bay.context.upload_file(context.id, file_path, content)
        if not result.is_error:
            print(f"✅ 文件上传成功: {file_path}")
        else:
            print(f"❌ 文件上传失败: {file_path} - {result.error}")
    
    # 列出上下文中的文件
    print("🔄 列出上下文文件...")
    files_result = agent_bay.context.list_files(context.id)
    if not files_result.is_error:
        print("📁 上下文文件列表:")
        for file in files_result.data:
            print(f"  - {file.path} ({file.size} 字节)")
    
    return context

def data_sync_example(agent_bay):
    """数据同步示例"""
    print("\n🔄 === 数据同步示例 ===")
    
    # 获取项目上下文
    context_result = agent_bay.context.get("demo-project", create=False)
    if context_result.is_error:
        print("❌ 项目上下文不存在，请先运行上下文管理示例")
        return
    
    context = context_result.context
    
    # 创建同步策略
    sync_policy = SyncPolicy(
        sync_on_create=True,
        sync_on_destroy=True,
        auto_sync_interval=0,  # 禁用自动同步，手动控制
        conflict_resolution="latest"
    )
    
    # 创建上下文同步配置
    context_sync = ContextSync.new(
        context_id=context.id,
        mount_path="/mnt/project",
        sync_policy=sync_policy
    )
    
    # 创建带同步的会话
    print("🔄 创建带同步的会话...")
    params = CreateSessionParams(context_syncs=[context_sync])
    session_result = agent_bay.create(params)
    
    if session_result.is_error:
        print(f"❌ 会话创建失败: {session_result.error}")
        return
    
    session = session_result.session
    print(f"✅ 会话创建成功: {session.session_id}")
    
    try:
        # 验证文件已同步
        print("🔄 验证文件同步...")
        files_to_check = [
            "/mnt/project/config.json",
            "/mnt/project/README.md",
            "/mnt/project/data/sample.txt"
        ]
        
        for file_path in files_to_check:
            result = session.file_system.read_file(file_path)
            if not result.is_error:
                print(f"✅ 文件已同步: {file_path}")
            else:
                print(f"❌ 文件同步失败: {file_path}")
        
        # 修改文件并同步回上下文
        print("🔄 修改文件并同步...")
        new_content = """# Demo Project - Updated

这是一个AgentBay数据持久化的演示项目（已更新）。

## 功能特性
- 数据持久化 ✅
- 跨会话共享 ✅
- 版本控制 ✅
- 实时同步 ✅

## 更新日志
- 添加了实时同步功能
"""
        
        session.file_system.write_file("/mnt/project/README.md", new_content)
        
        # 手动同步到上下文
        sync_result = session.context_sync.sync_to_context("/mnt/project")
        if not sync_result.is_error:
            print("✅ 文件更改已同步到上下文")
        else:
            print(f"❌ 同步失败: {sync_result.error}")
    
    finally:
        # 清理会话
        agent_bay.destroy(session.session_id)
        print("🧹 会话已清理")

def cross_session_sharing_example(agent_bay):
    """跨会话数据共享示例"""
    print("\n🔗 === 跨会话数据共享示例 ===")
    
    # 获取项目上下文
    context_result = agent_bay.context.get("demo-project", create=False)
    if context_result.is_error:
        print("❌ 项目上下文不存在")
        return
    
    context = context_result.context
    
    # 创建两个会话来演示数据共享
    print("🔄 创建第一个会话...")
    session1_result = agent_bay.create(CreateSessionParams(
        context_syncs=[ContextSync.new(context.id, "/mnt/shared")]
    ))
    
    if session1_result.is_error:
        print(f"❌ 第一个会话创建失败: {session1_result.error}")
        return
    
    session1 = session1_result.session
    print(f"✅ 第一个会话创建成功: {session1.session_id}")
    
    print("🔄 创建第二个会话...")
    session2_result = agent_bay.create(CreateSessionParams(
        context_syncs=[ContextSync.new(context.id, "/mnt/shared")]
    ))
    
    if session2_result.is_error:
        print(f"❌ 第二个会话创建失败: {session2_result.error}")
        agent_bay.destroy(session1.session_id)
        return
    
    session2 = session2_result.session
    print(f"✅ 第二个会话创建成功: {session2.session_id}")
    
    try:
        # 在第一个会话中创建共享数据
        print("🔄 在会话1中创建共享数据...")
        shared_data = {
            "message": "Hello from Session 1!",
            "timestamp": time.time(),
            "data": [1, 2, 3, 4, 5]
        }
        
        session1.file_system.write_file(
            "/mnt/shared/shared_data.json",
            json.dumps(shared_data, indent=2)
        )
        
        # 同步到上下文
        session1.context_sync.sync_to_context("/mnt/shared")
        print("✅ 数据已从会话1同步到上下文")
        
        # 在第二个会话中同步并读取数据
        print("🔄 在会话2中同步并读取数据...")
        session2.context_sync.sync_from_context("/mnt/shared")
        
        result = session2.file_system.read_file("/mnt/shared/shared_data.json")
        if not result.is_error:
            received_data = json.loads(result.data)
            print("✅ 会话2成功接收到共享数据:")
            print(f"  消息: {received_data['message']}")
            print(f"  时间戳: {received_data['timestamp']}")
            print(f"  数据: {received_data['data']}")
        else:
            print(f"❌ 会话2读取数据失败: {result.error}")
        
        # 在第二个会话中修改数据
        print("🔄 在会话2中修改数据...")
        received_data["message"] = "Updated from Session 2!"
        received_data["timestamp"] = time.time()
        received_data["data"].append(6)
        
        session2.file_system.write_file(
            "/mnt/shared/shared_data.json",
            json.dumps(received_data, indent=2)
        )
        
        session2.context_sync.sync_to_context("/mnt/shared")
        print("✅ 修改后的数据已从会话2同步到上下文")
        
        # 在第一个会话中同步并验证更改
        print("🔄 在会话1中验证更改...")
        session1.context_sync.sync_from_context("/mnt/shared")
        
        result = session1.file_system.read_file("/mnt/shared/shared_data.json")
        if not result.is_error:
            updated_data = json.loads(result.data)
            print("✅ 会话1成功接收到更新的数据:")
            print(f"  消息: {updated_data['message']}")
            print(f"  数据: {updated_data['data']}")
        
    finally:
        # 清理会话
        agent_bay.destroy(session1.session_id)
        agent_bay.destroy(session2.session_id)
        print("🧹 所有会话已清理")

def version_control_example(agent_bay):
    """版本控制示例"""
    print("\n📚 === 版本控制示例 ===")
    
    # 获取项目上下文
    context_result = agent_bay.context.get("demo-project", create=False)
    if context_result.is_error:
        print("❌ 项目上下文不存在")
        return
    
    context = context_result.context
    
    # 简单版本控制实现
    class SimpleVersionControl:
        def __init__(self, agent_bay, context_id):
            self.agent_bay = agent_bay
            self.context_id = context_id
        
        def create_version(self, version_name, description=""):
            """创建版本快照"""
            print(f"🔄 创建版本: {version_name}")
            
            # 获取所有文件
            files_result = self.agent_bay.context.list_files(self.context_id)
            if files_result.is_error:
                print(f"❌ 获取文件列表失败: {files_result.error}")
                return False
            
            # 创建版本信息
            version_info = {
                "version": version_name,
                "description": description,
                "timestamp": time.time(),
                "files": []
            }
            
            # 备份文件
            for file in files_result.data:
                if not file.path.startswith("/versions/"):
                    # 读取文件内容
                    content_result = self.agent_bay.context.download_file(
                        self.context_id, file.path
                    )
                    
                    if not content_result.is_error:
                        # 保存到版本目录
                        version_path = f"/versions/{version_name}{file.path}"
                        self.agent_bay.context.upload_file(
                            self.context_id, version_path, content_result.data
                        )
                        
                        version_info["files"].append({
                            "original_path": file.path,
                            "version_path": version_path,
                            "size": file.size
                        })
            
            # 保存版本信息
            version_info_path = f"/versions/{version_name}/version_info.json"
            self.agent_bay.context.upload_file(
                self.context_id,
                version_info_path,
                json.dumps(version_info, indent=2)
            )
            
            print(f"✅ 版本 {version_name} 创建成功，包含 {len(version_info['files'])} 个文件")
            return True
        
        def list_versions(self):
            """列出所有版本"""
            files_result = self.agent_bay.context.list_files(self.context_id)
            if files_result.is_error:
                return []
            
            versions = []
            for file in files_result.data:
                if file.path.endswith("/version_info.json"):
                    # 读取版本信息
                    info_result = self.agent_bay.context.download_file(
                        self.context_id, file.path
                    )
                    
                    if not info_result.is_error:
                        try:
                            version_info = json.loads(info_result.data)
                            versions.append(version_info)
                        except json.JSONDecodeError:
                            pass
            
            return sorted(versions, key=lambda x: x["timestamp"], reverse=True)
    
    # 使用版本控制
    vc = SimpleVersionControl(agent_bay, context.id)
    
    # 创建初始版本
    vc.create_version("v1.0", "初始版本")
    
    # 修改一些文件
    print("🔄 修改项目文件...")
    updated_config = {
        "name": "Demo Project",
        "version": "1.1.0",
        "description": "AgentBay数据持久化演示项目 - 已更新",
        "features": ["数据持久化", "版本控制", "跨会话共享"]
    }
    
    agent_bay.context.upload_file(
        context.id,
        "/project/config.json",
        json.dumps(updated_config, indent=2)
    )
    
    # 创建新版本
    vc.create_version("v1.1", "添加新功能和配置更新")
    
    # 列出所有版本
    print("🔄 列出所有版本...")
    versions = vc.list_versions()
    
    if versions:
        print("📚 版本历史:")
        for version in versions:
            print(f"  - {version['version']}: {version['description']}")
            print(f"    时间: {time.ctime(version['timestamp'])}")
            print(f"    文件数: {len(version['files'])}")
            print()
    else:
        print("❌ 没有找到版本信息")

if __name__ == "__main__":
    main() 