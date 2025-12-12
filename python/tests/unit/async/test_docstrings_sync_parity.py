from agentbay._async.filesystem import AsyncFileTransfer
from agentbay._async.fingerprint import AsyncBrowserFingerprintGenerator
from agentbay._async.mobile_simulate import AsyncMobileSimulateService


def test_filetransfer_docstring_is_generic():
    doc = AsyncFileTransfer.__doc__ or ""

    assert (
        "Provides pre-signed URL upload/download functionality between local and OSS"
        in doc
    )
    assert "AsyncFileTransfer provides" not in doc


def test_fingerprint_class_docstring_mentions_init_args():
    doc = AsyncBrowserFingerprintGenerator.__doc__ or ""

    assert "headless" in doc
    assert "use_chrome_channel" in doc


def test_mobile_simulate_upload_mobile_info_raises_section():
    doc = AsyncMobileSimulateService.upload_mobile_info.__doc__ or ""

    assert "context_sync is provided but context_sync.context_id is missing" in doc

