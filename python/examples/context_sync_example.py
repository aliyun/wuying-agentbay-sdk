#!/usr/bin/env python3
"""
ContextSync usage example.
Demonstrates how to use the ContextSync API for context synchronization.
"""

from agentbay.context_sync import (
    ContextSync,
    SyncPolicy,
    UploadPolicy,
    UploadStrategy,
    DownloadPolicy,
    DownloadStrategy,
    DeletePolicy,
    BWList,
    WhiteList,
)


def main():
    """Main function demonstrating ContextSync usage."""
    print("=== ContextSync Usage Example ===\n")
    
    # Example 1: Basic ContextSync with default policy
    print("1. Basic ContextSync with default policy:")
    basic_sync = ContextSync.new("my-context-id", "/home/wuying")
    print(f"   ContextID: {basic_sync.context_id}")
    print(f"   Path: {basic_sync.path}")
    print(f"   Upload Auto: {basic_sync.policy.upload_policy.auto_upload}")
    print(f"   Upload Strategy: {basic_sync.policy.upload_policy.upload_strategy}")
    print(f"   Download Auto: {basic_sync.policy.download_policy.auto_download}")
    print(f"   Download Strategy: {basic_sync.policy.download_policy.download_strategy}")
    print()
    
    # Example 2: Advanced ContextSync with custom policies
    print("2. Advanced ContextSync with custom policies:")
    
    # Create custom upload policy
    upload_policy = UploadPolicy(
        auto_upload=True,
        upload_strategy=UploadStrategy.PERIODIC_UPLOAD,
        period=15  # 15 minutes
    )
    
    # Create custom download policy
    download_policy = DownloadPolicy(
        auto_download=True,
        download_strategy=DownloadStrategy.DOWNLOAD_ASYNC
    )
    
    # Create custom delete policy
    delete_policy = DeletePolicy(
        sync_local_file=True
    )
    
    # Create white list for specific paths
    white_list = WhiteList(
        path="/data/important",
        exclude_paths=["/data/important/temp", "/data/important/logs"]
    )
    
    # Create BW list
    bw_list = BWList(
        white_lists=[white_list]
    )
    
    # Create sync policy
    sync_policy = SyncPolicy(
        upload_policy=upload_policy,
        download_policy=download_policy,
        delete_policy=delete_policy,
        bw_list=bw_list
    )
    
    # Create advanced sync
    advanced_sync = ContextSync.new("my-context-id", "/data", sync_policy)
    print(f"   ContextID: {advanced_sync.context_id}")
    print(f"   Path: {advanced_sync.path}")
    print(f"   Upload Auto: {advanced_sync.policy.upload_policy.auto_upload}")
    print(f"   Upload Strategy: {advanced_sync.policy.upload_policy.upload_strategy}")
    print(f"   Upload Period: {advanced_sync.policy.upload_policy.period} minutes")
    print(f"   WhiteList Path: {advanced_sync.policy.bw_list.white_lists[0].path}")
    print(f"   Exclude Paths: {advanced_sync.policy.bw_list.white_lists[0].exclude_paths}")
    print()
    
    # Example 3: Builder pattern usage
    print("3. Builder pattern usage:")
    builder_sync = ContextSync.new("my-context-id", "/workspace").with_policy(
        SyncPolicy(
            upload_policy=UploadPolicy(
                auto_upload=True,
                upload_strategy=UploadStrategy.UPLOAD_BEFORE_RESOURCE_RELEASE
            ),
            download_policy=DownloadPolicy(
                auto_download=True,
                download_strategy=DownloadStrategy.DOWNLOAD_ASYNC
            ),
            bw_list=BWList(
                white_lists=[
                    WhiteList(
                        path="/workspace/src",
                        exclude_paths=["/workspace/src/node_modules", "/workspace/src/.git"]
                    ),
                    WhiteList(
                        path="/workspace/docs",
                        exclude_paths=["/workspace/docs/build"]
                    )
                ]
            )
        )
    )
    print(f"   ContextID: {builder_sync.context_id}")
    print(f"   Path: {builder_sync.path}")
    print(f"   Number of WhiteLists: {len(builder_sync.policy.bw_list.white_lists)}")
    for i, wl in enumerate(builder_sync.policy.bw_list.white_lists):
        print(f"   WhiteList {i+1}: {wl.path} (exclude: {wl.exclude_paths})")
    print()
    
    # Example 4: Multiple white lists with sync paths
    print("4. Multiple white lists with sync paths:")
    
    # Create multiple white lists
    source_white_list = WhiteList(
        path="/workspace/src",
        exclude_paths=["/workspace/src/node_modules", "/workspace/src/.git"]
    )
    
    docs_white_list = WhiteList(
        path="/workspace/docs",
        exclude_paths=["/workspace/docs/build", "/workspace/docs/temp"]
    )
    
    config_white_list = WhiteList(
        path="/workspace/config",
        exclude_paths=["/workspace/config/tmp"]
    )
    
    # Create BW list with multiple white lists
    bw_list = BWList(
        white_lists=[source_white_list, docs_white_list, config_white_list]
    )
    
    # Create sync policy with sync paths
    sync_policy = SyncPolicy(
        upload_policy=UploadPolicy.default(),
        download_policy=DownloadPolicy.default(),
        delete_policy=DeletePolicy.default(),
        bw_list=bw_list,
        sync_paths=["/workspace/src", "/workspace/docs", "/workspace/config"]
    )
    
    # Create context sync
    context_sync = ContextSync.new("my-context-id", "/workspace", sync_policy)
    print(f"   ContextID: {context_sync.context_id}")
    print(f"   Path: {context_sync.path}")
    print(f"   Number of WhiteLists: {len(context_sync.policy.bw_list.white_lists)}")
    print(f"   Sync Paths: {context_sync.policy.sync_paths}")
    print()
    
    # Example 5: Policy modification
    print("5. Policy modification:")
    
    # Create initial context sync
    context_sync = ContextSync.new("my-context-id", "/test", SyncPolicy.default())
    print(f"   Initial Upload Auto: {context_sync.policy.upload_policy.auto_upload}")
    print(f"   Initial Upload Strategy: {context_sync.policy.upload_policy.upload_strategy}")
    
    # Modify upload policy
    new_upload_policy = UploadPolicy(
        auto_upload=False,
        upload_strategy=UploadStrategy.PERIODIC_UPLOAD,
        period=60
    )
    
    # Create new sync policy with modified upload policy
    new_sync_policy = SyncPolicy(
        upload_policy=new_upload_policy,
        download_policy=context_sync.policy.download_policy,
        delete_policy=context_sync.policy.delete_policy,
        bw_list=context_sync.policy.bw_list
    )
    
    # Apply new policy
    context_sync.with_policy(new_sync_policy)
    print(f"   Modified Upload Auto: {context_sync.policy.upload_policy.auto_upload}")
    print(f"   Modified Upload Strategy: {context_sync.policy.upload_policy.upload_strategy}")
    print(f"   Modified Upload Period: {context_sync.policy.upload_policy.period} minutes")
    print()
    
    print("=== Example completed successfully! ===")


if __name__ == "__main__":
    main() 