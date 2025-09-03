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

## Features
- Data persistence ✅
- Cross-session sharing ✅
- Version control ✅
- Real-time sync ✅

## Changelog
- Added real-time sync functionality
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
    """Cross-session data sharing example"""
    print("\n🔗 === Cross-Session Data Sharing Example ===")
    
    # Get project context
    context_result = agent_bay.context.get("demo-project", create=False)
    if not context_result.success:
        print("❌ Project context does not exist")
        return
    
    context = context_result.context
    
    # Create two sessions to demonstrate data sharing
    print("🔄 Creating first session...")
    session1_result = agent_bay.create(CreateSessionParams(
        context_syncs=[ContextSync.new(context.id, "/tmp/shared")]
    ))
    
    if not session1_result.success:
        print(f"❌ First session creation failed: {session1_result.error_message}")
        return
    
    session1 = session1_result.session
    print(f"✅ First session created successfully: {session1.session_id}")
    
    print("🔄 Creating second session...")
    session2_result = agent_bay.create(CreateSessionParams(
        context_syncs=[ContextSync.new(context.id, "/tmp/shared")]
    ))
    
    if not session2_result.success:
        print(f"❌ Second session creation failed: {session2_result.error_message}")
        agent_bay.delete(session1.session_id)
        return
    
    session2 = session2_result.session
    print(f"✅ Second session created successfully: {session2.session_id}")
    
    try:
        # Create shared data in first session
        print("🔄 Creating shared data in session 1...")
        shared_data = {
            "message": "Hello from Session 1!",
            "timestamp": time.time(),
            "data": [1, 2, 3, 4, 5]
        }
        
        session1.file_system.write_file(
            "/tmp/shared/shared_data.json",
            json.dumps(shared_data, indent=2)
        )
        
        # Sync to context
        session1.context.sync()
        print("✅ Data synchronized from session 1 to context")
        
        # Sync and read data in second session
        print("🔄 Syncing and reading data in session 2...")
        session2.context.sync()
        
        result = session2.file_system.read_file("/tmp/shared/shared_data.json")
        if result.success:
            received_data = json.loads(result.data)
            print("✅ Session 2 successfully received shared data:")
            print(f"  Message: {received_data['message']}")
            print(f"  Timestamp: {received_data['timestamp']}")
            print(f"  Data: {received_data['data']}")
        else:
            print(f"❌ Session 2 failed to read data: {result.error_message}")
        
        # Modify data in second session
        print("🔄 Modifying data in session 2...")
        received_data["message"] = "Updated from Session 2!"
        received_data["timestamp"] = time.time()
        received_data["data"].append(6)
        
        session2.file_system.write_file(
            "/tmp/shared/shared_data.json",
            json.dumps(received_data, indent=2)
        )
        
        session2.context.sync()
        print("✅ Modified data synchronized from session 2 to context")
        
        # Sync and verify changes in first session
        print("🔄 Verifying changes in session 1...")
        session1.context.sync()
        
        result = session1.file_system.read_file("/tmp/shared/shared_data.json")
        if result.success:
            updated_data = json.loads(result.data)
            print("✅ Session 1 successfully received updated data:")
            print(f"  Message: {updated_data['message']}")
            print(f"  Data: {updated_data['data']}")
        
    finally:
        # Clean up sessions
        agent_bay.delete(session1)
        agent_bay.delete(session2)
        print("🧹 All sessions cleaned up")

def version_control_example(agent_bay):
    """Version control example"""
    print("\n📚 === Version Control Example ===")
    
    # Get project context
    context_result = agent_bay.context.get("demo-project", create=False)
    if not context_result.success:
        print("❌ Project context does not exist")
        return
    
    context = context_result.context
    
    # Simple version control implementation
    class SimpleVersionControl:
        def __init__(self, agent_bay, context_id):
            self.agent_bay = agent_bay
            self.context_id = context_id
        
        def create_version(self, version_name, description=""):
            """Create version snapshot"""
            print(f"🔄 Creating version: {version_name}")
            
            # Get all files
            files_result = self.agent_bay.context.list_files(self.context_id)
            if not files_result.success:
                print(f"❌ Failed to get file list: {files_result.error_message}")
                return False
            
            # Create version information
            version_info = {
                "version": version_name,
                "description": description,
                "timestamp": time.time(),
                "files": []
            }
            
            # Backup files
            for file in files_result.data:
                if not file.path.startswith("/versions/"):
                    # Read file content
                    content_result = self.agent_bay.context.download_file(
                        self.context_id, file.path
                    )
                    
                    if content_result.success:
                        # Save to version directory
                        version_path = f"/versions/{version_name}{file.path}"
                        self.agent_bay.context.upload_file(
                            self.context_id, version_path, content_result.data
                        )
                        
                        version_info["files"].append({
                            "original_path": file.path,
                            "version_path": version_path,
                            "size": file.size
                        })
            
            # Save version information
            version_info_path = f"/versions/{version_name}/version_info.json"
            self.agent_bay.context.upload_file(
                self.context_id,
                version_info_path,
                json.dumps(version_info, indent=2)
            )
            
            print(f"✅ Version {version_name} created successfully, contains {len(version_info['files'])} files")
            return True
        
        def list_versions(self):
            """List all versions"""
            files_result = self.agent_bay.context.list_files(self.context_id)
            if not files_result.success:
                return []
            
            versions = []
            for file in files_result.data:
                if file.path.endswith("/version_info.json"):
                    # Read version information
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
    
    # Use version control
    vc = SimpleVersionControl(agent_bay, context.id)
    
    # Create initial version
    vc.create_version("v1.0", "Initial version")
    
    # Modify some files
    print("🔄 Modifying project files...")
    updated_config = {
        "name": "Demo Project",
        "version": "1.1.0",
        "description": "AgentBay data persistence demo project - updated",
        "features": ["Data persistence", "Version control", "Cross-session sharing"]
    }
    
    agent_bay.context.upload_file(
        context.id,
        "/project/config.json",
        json.dumps(updated_config, indent=2)
    )
    
    # Create new version
    vc.create_version("v1.1", "Added new features and configuration updates")
    
    # List all versions
    print("🔄 Listing all versions...")
    versions = vc.list_versions()
    
    if versions:
        print("📚 Version history:")
        for version in versions:
            print(f"  - {version['version']}: {version['description']}")
            print(f"    Time: {time.ctime(version['timestamp'])}")
            print(f"    Files: {len(version['files'])}")
            print()
    else:
        print("❌ No version information found")

if __name__ == "__main__":
    main() 