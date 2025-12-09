"""
Unit tests for context_sync module exports

These tests ensure that all context_sync classes and enums are properly
exported from the main agentbay package, preventing import issues for users.

Related Issue: Users reported that UploadMode and Lifecycle were not available
for import from the agentbay package, even though they are required by
UploadPolicy and RecyclePolicy respectively.
"""

import pytest


class TestContextSyncExports:
    """Test that all context_sync related classes are properly exported"""

    @pytest.mark.asyncio


    async def test_upload_mode_enum_export(self):
        """Test that UploadMode enum can be imported from agentbay package"""
        # Verify it's an enum
        from enum import Enum

        from agentbay import UploadMode

        assert issubclass(UploadMode, Enum)

        # Verify enum values
        assert hasattr(UploadMode, "FILE")
        assert hasattr(UploadMode, "ARCHIVE")
        assert UploadMode.FILE.value == "File"
        assert UploadMode.ARCHIVE.value == "Archive"

    @pytest.mark.asyncio


    async def test_lifecycle_enum_export(self):
        """Test that Lifecycle enum can be imported from agentbay package"""
        # Verify it's an enum
        from enum import Enum

        from agentbay import Lifecycle

        assert issubclass(Lifecycle, Enum)

        # Verify some key enum values
        assert hasattr(Lifecycle, "LIFECYCLE_1DAY")
        assert hasattr(Lifecycle, "LIFECYCLE_3DAYS")
        assert hasattr(Lifecycle, "LIFECYCLE_FOREVER")
        assert Lifecycle.LIFECYCLE_1DAY.value == "Lifecycle_1Day"
        assert Lifecycle.LIFECYCLE_FOREVER.value == "Lifecycle_Forever"

    @pytest.mark.asyncio


    async def test_upload_policy_with_upload_mode(self):
        """Test that UploadPolicy can be created with UploadMode from main package"""
        from agentbay import UploadMode, UploadPolicy

        # Test FILE mode
        policy = UploadPolicy(upload_mode=UploadMode.FILE)
        assert policy.upload_mode == UploadMode.FILE

        # Test ARCHIVE mode
        policy = UploadPolicy(upload_mode=UploadMode.ARCHIVE)
        assert policy.upload_mode == UploadMode.ARCHIVE

    @pytest.mark.asyncio


    async def test_recycle_policy_with_lifecycle(self):
        """Test that RecyclePolicy can be created with Lifecycle from main package"""
        from agentbay import Lifecycle, RecyclePolicy

        # Test 1 day lifecycle
        policy = RecyclePolicy(lifecycle=Lifecycle.LIFECYCLE_1DAY, paths=[""])
        assert policy.lifecycle == Lifecycle.LIFECYCLE_1DAY

        # Test forever lifecycle
        policy = RecyclePolicy(lifecycle=Lifecycle.LIFECYCLE_FOREVER, paths=[""])
        assert policy.lifecycle == Lifecycle.LIFECYCLE_FOREVER

    @pytest.mark.asyncio


    async def test_all_context_sync_classes_exported(self):
        """Test that all context_sync classes can be imported from main package"""
        from agentbay import (
            BWList,
            ContextSync,
            DeletePolicy,
            DownloadPolicy,
            DownloadStrategy,
            ExtractPolicy,
            Lifecycle,
            RecyclePolicy,
            SyncPolicy,
            UploadMode,
            UploadPolicy,
            UploadStrategy,
            WhiteList,
        )

        # Verify all imports succeed (if we get here, they did)
        assert ContextSync is not None
        assert SyncPolicy is not None
        assert UploadPolicy is not None
        assert UploadStrategy is not None
        assert UploadMode is not None
        assert DownloadPolicy is not None
        assert DownloadStrategy is not None
        assert DeletePolicy is not None
        assert ExtractPolicy is not None
        assert RecyclePolicy is not None
        assert Lifecycle is not None
        assert BWList is not None
        assert WhiteList is not None

    @pytest.mark.asyncio


    async def test_backward_compatibility_context_sync_import(self):
        """Test that importing from context_sync module still works (backward compatibility)"""
        from agentbay import Lifecycle as Lifecycle2
        from agentbay import RecyclePolicy as RecyclePolicy2
        from agentbay import UploadMode as UploadMode2
        from agentbay import (
            Lifecycle,
            RecyclePolicy,
            UploadMode,
        )

        # Verify they are the same classes
        assert UploadMode is UploadMode2
        assert Lifecycle is Lifecycle2
        assert RecyclePolicy is RecyclePolicy2

    @pytest.mark.asyncio


    async def test_all_exports_in_all_list(self):
        """Test that all context_sync exports are in __all__ list"""
        import agentbay

        # Get the __all__ list
        all_exports = agentbay.__all__

        # Check that all context_sync classes are in __all__
        expected_exports = [
            "ContextSync",
            "SyncPolicy",
            "UploadPolicy",
            "UploadStrategy",
            "UploadMode",
            "DownloadPolicy",
            "DownloadStrategy",
            "DeletePolicy",
            "ExtractPolicy",
            "RecyclePolicy",
            "Lifecycle",
            "BWList",
            "WhiteList",
        ]

        for export in expected_exports:
            assert export in all_exports, f"{export} is not in __all__ list"

    @pytest.mark.asyncio


    async def test_complete_sync_policy_with_all_imports(self):
        """Test creating a complete SyncPolicy using imports from main package"""
        from agentbay import (
            BWList,
            DeletePolicy,
            DownloadPolicy,
            ExtractPolicy,
            Lifecycle,
            RecyclePolicy,
            SyncPolicy,
            UploadMode,
            UploadPolicy,
            WhiteList,
        )

        # Create a complete sync policy
        sync_policy = SyncPolicy(
            upload_policy=UploadPolicy(upload_mode=UploadMode.ARCHIVE),
            download_policy=DownloadPolicy(),
            delete_policy=DeletePolicy(),
            extract_policy=ExtractPolicy(),
            recycle_policy=RecyclePolicy(
                lifecycle=Lifecycle.LIFECYCLE_3DAYS, paths=["/tmp/cache"]
            ),
            bw_list=BWList(white_lists=[WhiteList(path="", exclude_paths=[])]),
        )

        # Verify the policy was created correctly
        assert sync_policy.upload_policy.upload_mode == UploadMode.ARCHIVE
        assert sync_policy.recycle_policy.lifecycle == Lifecycle.LIFECYCLE_3DAYS
        assert sync_policy.recycle_policy.paths == ["/tmp/cache"]
