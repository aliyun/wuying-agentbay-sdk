#!/usr/bin/env python3
"""
AgentBay SDK - Archive Upload Mode Context Sync Example

This example demonstrates how to use AgentBay SDK archive upload mode for context synchronization:
- Creating context with Archive upload mode
- Session creation with context sync configuration
- Archive upload mode for efficient file compression
- Context info and status monitoring
- File operations with context synchronization
- Proper cleanup and error handling

Based on TypeScript SDK archive-upload-mode-example functionality.
"""

import os
import time
from agentbay import AgentBay
from agentbay.session_params import CreateSessionParams
from agentbay.context_sync import ContextSync, SyncPolicy, UploadPolicy, UploadMode

def get_api_key():
    """Get API key from environment variable with fallback."""
    api_key = os.getenv("AGENTBAY_API_KEY")
    if not api_key:
        print("Warning: AGENTBAY_API_KEY environment variable not set. Using default key.")
        return "your-api-key-here"  # Replace with your actual API key
    return api_key

def generate_unique_id():
    """Generate a unique identifier for this example run."""
    timestamp = int(time.time() * 1000) + (int(time.time() * 1000000) % 1000)
    random_part = int(time.time() * 1000000) % 10000
    return f"{timestamp}-{random_part}"

def main():
    """Main function demonstrating archive upload mode context sync."""
    print("🚀 AgentBay Archive Upload Mode Context Sync Example")
    print("=" * 60)
    
    # Initialize AgentBay client
    agent_bay = AgentBay(api_key=get_api_key())
    unique_id = generate_unique_id()
    
    try:
        # Archive Upload Mode Context Sync Example
        archive_upload_mode_example(agent_bay, unique_id)
        
    except Exception as e:
        print(f"❌ Example execution failed: {e}")
    
    print("✅ Archive upload mode example completed")

def archive_upload_mode_example(agent_bay, unique_id):
    """Archive Upload Mode Context Sync Example"""
    print("\n📦 === Archive Upload Mode Context Sync Example ===")
    
    session = None
    
    try:
        # Step 1: Create context for Archive mode
        print("\n📦 Step 1: Creating context for Archive upload mode...")
        context_name = f"archive-mode-context-{unique_id}"
        context_result = agent_bay.context.get(context_name, create=True)
        
        if not context_result.success:
            raise Exception(f"Context creation failed: {context_result.error_message}")
        
        print(f"✅ Context created successfully!")
        print(f"   Context ID: {context_result.context_id}")
        print(f"   Request ID: {context_result.request_id}")

        # Step 2: Configure sync policy with Archive upload mode
        print("\n⚙️  Step 2: Configuring sync policy with Archive upload mode...")
        upload_policy = UploadPolicy(upload_mode=UploadMode.ARCHIVE)
        sync_policy = SyncPolicy(upload_policy=upload_policy)
        
        print(f"✅ Sync policy configured with uploadMode: {sync_policy.upload_policy.upload_mode.value}")

        # Step 3: Create context sync configuration
        print("\n🔧 Step 3: Creating context sync configuration...")
        context_sync = ContextSync(
            context_id=context_result.context_id,
            path="/tmp/archive-mode-test",
            policy=sync_policy
        )

        print(f"✅ Context sync created:")
        print(f"   Context ID: {context_sync.context_id}")
        print(f"   Path: {context_sync.path}")
        print(f"   Upload Mode: {context_sync.policy.upload_policy.upload_mode.value}")

        # Step 4: Create session with Archive mode context sync
        print("\n🏗️  Step 4: Creating session with Archive mode context sync...")
        session_params = CreateSessionParams(
            labels={
                "example": f"archive-mode-{unique_id}",
                "type": "archive-upload-demo",
                "uploadMode": UploadMode.ARCHIVE.value
            },
            context_syncs=[context_sync]
        )

        session_result = agent_bay.create(session_params)
        if not session_result.success:
            raise Exception(f"Session creation failed: {session_result.error_message}")

        session = session_result.session
        print(f"✅ Session created successfully!")
        print(f"   Session ID: {session.session_id}")
        print(f"   Request ID: {session_result.request_id}")

        # Get session info to verify setup
        session_info = agent_bay.get_session(session.session_id)
        if session_info.success and session_info.data:
            print(f"   App Instance ID: {session_info.data.app_instance_id}")

        # Step 5: Create and write test files
        print("\n📝 Step 5: Creating test files in Archive mode context...")
        
        # Generate 5KB test content
        content_size = 5 * 1024  # 5KB
        base_content = "Archive mode test successful! This is a test file created in the session path. "
        repeated_content = base_content * (content_size // len(base_content) + 1)
        file_content = repeated_content[:content_size]
        
        file_path = "/tmp/archive-mode-test/test-file-5kb.txt"
        
        print(f"📄 Creating file: {file_path}")
        print(f"📊 File content size: {len(file_content)} bytes")

        write_result = session.file_system.write_file(file_path, file_content, mode="overwrite")
        
        if not write_result.success:
            raise Exception(f"File write failed: {write_result.error_message}")

        print(f"✅ File write successful!")
        print(f"   Request ID: {write_result.request_id}")

        # Step 6: Test context sync and info functionality
        print("\n📊 Step 6: Testing context sync and info functionality...")
        
        # Call context sync before getting info
        print("🔄 Calling context sync before getting info...")
        
        # Use asyncio to handle the async sync method
        import asyncio
        
        async def run_sync():
            return await session.context.sync()
        
        sync_result = asyncio.run(run_sync())
        
        if not sync_result.success:
            raise Exception(f"Context sync failed: {sync_result.error_message}")

        print(f"✅ Context sync successful!")
        print(f"   Sync Request ID: {sync_result.request_id}")

        # Now call context info after sync
        print("📋 Calling context info after sync...")
        info_result = session.context.info()
        
        if not info_result.success:
            raise Exception(f"Context info failed: {info_result.error_message}")

        print(f"✅ Context info retrieved successfully!")
        print(f"   Info Request ID: {info_result.request_id}")
        print(f"   Context status data count: {len(info_result.context_status_data)}")
        
        # Display context status details
        if info_result.context_status_data:
            print("\n📋 Context status details:")
            for index, status in enumerate(info_result.context_status_data):
                print(f"   [{index}] Context ID: {status.context_id}")
                print(f"       Path: {status.path}")
                print(f"       Status: {status.status}")
                print(f"       Task Type: {status.task_type}")
                if status.error_message:
                    print(f"       Error: {status.error_message}")

        # Step 7: List files in context sync directory
        print("\n🔍 Step 7: Listing files in context sync directory...")
        
        # Use the sync directory path
        sync_dir_path = "/tmp/archive-mode-test"
        
        list_result = agent_bay.context.list_files(context_result.context_id, sync_dir_path, page_number=1, page_size=10)
        
        if not list_result.success:
            raise Exception(f"List files failed: {list_result.error_message if hasattr(list_result, 'error_message') else 'Unknown error'}")

        print(f"✅ List files successful!")
        print(f"   Request ID: {list_result.request_id}")
        print(f"   Total files found: {len(list_result.entries)}")
        
        if list_result.entries:
            print("\n📋 Files in context sync directory:")
            for index, entry in enumerate(list_result.entries):
                print(f"   [{index}] FilePath: {entry.file_path}")
                print(f"       FileType: {entry.file_type}")
                print(f"       FileName: {entry.file_name}")
                print(f"       Size: {entry.size} bytes")
        else:
            print("   No files found in context sync directory")

        print("\n🎉 Archive upload mode example completed successfully!")
        print("✅ All operations completed without errors.")

    except Exception as error:
        print(f"\n❌ Error occurred during archive upload mode example:")
        print(f"   {error}")
    finally:
        # Step 8: Cleanup
        if session:
            print("\n🧹 Step 8: Cleaning up session...")
            try:
                delete_result = agent_bay.delete(session, sync_context=True)
                print(f"✅ Session deleted successfully!")
                print(f"   Success: {delete_result.success}")
                print(f"   Request ID: {delete_result.request_id}")
            except Exception as delete_error:
                print(f"❌ Failed to delete session: {delete_error}")


if __name__ == "__main__":
    main()