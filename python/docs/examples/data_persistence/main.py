#!/usr/bin/env python3
"""
AgentBay SDK - Data Persistence Example

This example demonstrates how to use AgentBay SDK's data persistence features, including:
- Context management
- Data synchronization
- Cross-session data sharing
- Version control
"""

import json
import time
from agentbay import AgentBay, ContextSync, SyncPolicy, CreateSessionParams

def main():
    """Main function"""
    print("🗄️ AgentBay Data Persistence Example")
    
    # Initialize AgentBay client
    agent_bay = AgentBay()
    
    try:
        # 1. Context management example
        context_management_example(agent_bay)
        
        # 2. Data synchronization example
        data_sync_example(agent_bay)
        
        # Note: Due to example complexity, temporarily skip the following sections
        print("\n💡 Cross-session data sharing and version control examples are temporarily skipped")
        print("These features require more complex file operations, please refer to other examples")
        
        # # 3. Cross-session data sharing example
        # cross_session_sharing_example(agent_bay)
        
        # # 4. Version control example
        # version_control_example(agent_bay)
        
    except Exception as e:
        print(f"❌ Example execution failed: {e}")
    
    print("✅ Data persistence example execution completed")

def context_management_example(agent_bay):
    """Context management example"""
    print("\n📦 === Context Management Example ===")
    
    # Create or get context
    print("🔄 Creating project context...")
    context_result = agent_bay.context.get("demo-project", create=True)
    if not context_result.success:
        print(f"❌ Context creation failed: {context_result.error_message}")
        return None
    
    context = context_result.context
    print(f"✅ Context created successfully: {context.id}")
    
    # Upload files to context
    project_files = {
        "/project/config.json": json.dumps({
            "name": "Demo Project",
            "version": "1.0.0",
            "description": "AgentBay data persistence demo project"
        }, indent=2),
        "/project/README.md": """# Demo Project

This is an AgentBay data persistence demonstration project.

## Features
- Data persistence
- Cross-session sharing
- Version control
""",
        "/project/data/sample.txt": "This is a sample data file."
    }
    
    # Note: File upload requires session file system operations, then sync to context
    # Here we skip the file upload part and directly demonstrate basic context operations
    print("🔄 Context created successfully, skipping complex file operation demonstration...")
    print("💡 Note: Actual file operations need to be performed through session.file_system, then sync to context")
    
    return context

def data_sync_example(agent_bay):
    """Data synchronization example"""
    print("\n🔄 === Data Synchronization Example ===")
    
    # Get project context
    context_result = agent_bay.context.get("demo-project", create=False)
    if not context_result.success:
        print("❌ Project context does not exist, please run context management example first")
        return
    
    context = context_result.context
    
    # Create sync policy
    sync_policy = SyncPolicy.default()
    
    # Create context sync configuration
    context_sync = ContextSync.new(
        context_id=context.id,
        path="/tmp/project",
        policy=sync_policy
    )
    
    # Create session with sync
    print("🔄 Creating session with sync...")
    params = CreateSessionParams(context_syncs=[context_sync])
    session_result = agent_bay.create(params)
    
    if not session_result.success:
        print(f"❌ Session creation failed: {session_result.error_message}")
        return
    
    session = session_result.session
    print(f"✅ Session created successfully: {session.session_id}")
    
    try:
        # Verify file synchronization
        print("🔄 Verifying file synchronization...")
        files_to_check = [
            "/tmp/project/config.json",
            "/tmp/project/README.md",
            "/tmp/project/data/sample.txt"
        ]
        
        for file_path in files_to_check:
            result = session.file_system.read_file(file_path)
            if result.success:
                print(f"✅ File synchronized: {file_path}")
            else:
                print(f"❌ File synchronization failed: {file_path}")
        
        # Modify file and sync back to context
        print("🔄 Modifying file and syncing...")
        new_content = """# Demo Project - Updated

This is an AgentBay data persistence demonstration project (updated).

## 功能特性
- 数据持久化 ✅
- 跨会话共享 ✅
- 版本控制 ✅
- 实时同步 ✅

## 更新日志
- 添加了实时同步功能
"""
        
        # Create directory first
        session.command.execute_command("mkdir -p /tmp/project")
        
        # Write file
        session.file_system.write_file("/tmp/project/README.md", new_content)
        
        # Manual sync to context
        sync_result = session.context.sync()
        if sync_result.success:
            print("✅ File changes synchronized to context")
        else:
            print(f"❌ Sync failed: {sync_result.error_message}")
    
    finally:
        # Clean up session
        agent_bay.delete(session)
        print("🧹 Session cleaned up")

def cross_session_sharing_example(agent_bay):
    """跨会话数据共享示例"""
    print("\n🔗 === 跨会话数据共享示例 ===")
    
    # 获取项目上下文
    context_result = agent_bay.context.get("demo-project", create=False)
    if not context_result.success:
        print("❌ 项目上下文不存在")
        return
    
    context = context_result.context
    
    # 创建两个会话来演示数据共享
    print("🔄 创建第一个会话...")
    session1_result = agent_bay.create(CreateSessionParams(
        context_syncs=[ContextSync.new(context.id, "/tmp/shared")]
    ))
    
    if not session1_result.success:
        print(f"❌ 第一个会话创建失败: {session1_result.error_message}")
        return
    
    session1 = session1_result.session
    print(f"✅ 第一个会话创建成功: {session1.session_id}")
    
    print("🔄 创建第二个会话...")
    session2_result = agent_bay.create(CreateSessionParams(
        context_syncs=[ContextSync.new(context.id, "/tmp/shared")]
    ))
    
    if not session2_result.success:
        print(f"❌ 第二个会话创建失败: {session2_result.error_message}")
        agent_bay.delete(session1.session_id)
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
            "/tmp/shared/shared_data.json",
            json.dumps(shared_data, indent=2)
        )
        
        # 同步到上下文
        session1.context.sync()
        print("✅ 数据已从会话1同步到上下文")
        
        # 在第二个会话中同步并读取数据
        print("🔄 在会话2中同步并读取数据...")
        session2.context.sync()
        
        result = session2.file_system.read_file("/tmp/shared/shared_data.json")
        if result.success:
            received_data = json.loads(result.data)
            print("✅ 会话2成功接收到共享数据:")
            print(f"  消息: {received_data['message']}")
            print(f"  时间戳: {received_data['timestamp']}")
            print(f"  数据: {received_data['data']}")
        else:
            print(f"❌ 会话2读取数据失败: {result.error_message}")
        
        # 在第二个会话中修改数据
        print("🔄 在会话2中修改数据...")
        received_data["message"] = "Updated from Session 2!"
        received_data["timestamp"] = time.time()
        received_data["data"].append(6)
        
        session2.file_system.write_file(
            "/tmp/shared/shared_data.json",
            json.dumps(received_data, indent=2)
        )
        
        session2.context.sync()
        print("✅ 修改后的数据已从会话2同步到上下文")
        
        # 在第一个会话中同步并验证更改
        print("🔄 在会话1中验证更改...")
        session1.context.sync()
        
        result = session1.file_system.read_file("/tmp/shared/shared_data.json")
        if result.success:
            updated_data = json.loads(result.data)
            print("✅ 会话1成功接收到更新的数据:")
            print(f"  消息: {updated_data['message']}")
            print(f"  数据: {updated_data['data']}")
        
    finally:
        # 清理会话
        agent_bay.delete(session1)
        agent_bay.delete(session2)
        print("🧹 所有会话已清理")

def version_control_example(agent_bay):
    """版本控制示例"""
    print("\n📚 === 版本控制示例 ===")
    
    # 获取项目上下文
    context_result = agent_bay.context.get("demo-project", create=False)
    if not context_result.success:
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
            if not files_result.success:
                print(f"❌ 获取文件列表失败: {files_result.error_message}")
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
                    
                    if content_result.success:
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
            if not files_result.success:
                return []
            
            versions = []
            for file in files_result.data:
                if file.path.endswith("/version_info.json"):
                    # 读取版本信息
                    info_result = self.agent_bay.context.download_file(
                        self.context_id, file.path
                    )
                    
                    if info_result.success:
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