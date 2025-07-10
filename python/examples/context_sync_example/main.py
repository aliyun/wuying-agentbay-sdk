#!/usr/bin/env python3
"""
This example demonstrates how to use context synchronization in AgentBay.
"""

from agentbay import (
    SyncPolicy,
    UploadPolicy,
    UploadStrategy,
    DownloadPolicy,
    DownloadStrategy,
    DeletePolicy,
    BWList,
    WhiteList,
    ContextSync,
)

def basic_context_sync():
    """Demonstrate basic context synchronization configuration."""
    # Create a basic context sync configuration with default policy
    context_sync = ContextSync.new(
        "example-context-id",
        "/path/to/mount",
        SyncPolicy.default()
    )
    print("\nBasic Context Sync Configuration:")
    print(f"Context ID: {context_sync.context_id}")
    print(f"Path: {context_sync.path}")
    print(f"Upload Auto: {context_sync.policy.upload_policy.auto_upload}")
    print(f"Upload Strategy: {context_sync.policy.upload_policy.upload_strategy}")
    print(f"Download Auto: {context_sync.policy.download_policy.auto_download}")
    print(f"Download Strategy: {context_sync.policy.download_policy.download_strategy}")
    print(f"Sync Local File Deletions: {context_sync.policy.delete_policy.sync_local_file}")
    return context_sync

def custom_context_sync():
    """Demonstrate custom context synchronization configuration."""
    # Create custom SyncPolicy
    upload_policy = UploadPolicy(
        auto_upload=True,
        upload_strategy=UploadStrategy.PERIODIC_UPLOAD,
        period=15
    )
    download_policy = DownloadPolicy(
        auto_download=True,
        download_strategy=DownloadStrategy.DOWNLOAD_SYNC
    )
    delete_policy = DeletePolicy(sync_local_file=False)
    source_white_list = WhiteList(
        path="/path/to/source",
        exclude_paths=["/path/to/source/node_modules", "/path/to/source/.git"]
    )
    docs_white_list = WhiteList(
        path="/path/to/docs",
        exclude_paths=["/path/to/docs/build"]
    )
    bw_list = BWList(white_lists=[source_white_list, docs_white_list])
    sync_policy = SyncPolicy(
        upload_policy=upload_policy,
        download_policy=download_policy,
        delete_policy=delete_policy,
        bw_list=bw_list,
        sync_paths=["/path/to/source", "/path/to/docs"]
    )
    context_sync = ContextSync.new(
        "example-context-id",
        "/path/to/mount",
        sync_policy
    )
    print("\nCustom Context Sync Configuration:")
    print(f"Context ID: {context_sync.context_id}")
    print(f"Path: {context_sync.path}")
    print(f"Upload Auto: {context_sync.policy.upload_policy.auto_upload}")
    print(f"Upload Strategy: {context_sync.policy.upload_policy.upload_strategy}")
    print(f"Upload Period: {context_sync.policy.upload_policy.period} minutes")
    print(f"Download Auto: {context_sync.policy.download_policy.auto_download}")
    print(f"Download Strategy: {context_sync.policy.download_policy.download_strategy}")
    print(f"Sync Local File Deletions: {context_sync.policy.delete_policy.sync_local_file}")
    print("\nWhite Lists:")
    for i, wl in enumerate(context_sync.policy.bw_list.white_lists):
        print(f"  White List {i+1}:")
        print(f"    Path: {wl.path}")
        print(f"    Exclude Paths: {wl.exclude_paths}")
    print(f"\nSync Paths: {context_sync.policy.sync_paths}")
    return context_sync

def update_existing_policy(context_sync: ContextSync):
    """Demonstrate how to update an existing policy."""
    # Update existing policy
    if context_sync.policy and context_sync.policy.upload_policy:
        context_sync.policy.upload_policy.period = 60
        context_sync.policy.upload_policy.upload_strategy = UploadStrategy.UPLOAD_AFTER_FILE_CLOSE
    # Add a new whitelist
    if context_sync.policy and context_sync.policy.bw_list:
        new_whitelist = WhiteList(
            path="/path/to/config",
            exclude_paths=["/path/to/config/tmp"]
        )
        context_sync.policy.bw_list.white_lists.append(new_whitelist)
    print("\nUpdated Context Sync Configuration:")
    print(f"Upload Strategy: {context_sync.policy.upload_policy.upload_strategy}")
    print(f"Upload Period: {context_sync.policy.upload_policy.period} minutes")
    print("\nWhite Lists:")
    for i, wl in enumerate(context_sync.policy.bw_list.white_lists):
        print(f"  White List {i+1}:")
        print(f"    Path: {wl.path}")
        print(f"    Exclude Paths: {wl.exclude_paths}")

def main():
    print("=== AgentBay Context Sync Example ===")
    basic_config = basic_context_sync()
    custom_config = custom_context_sync()
    update_existing_policy(custom_config)
    print("\nExample completed successfully!")

if __name__ == "__main__":
    main() 