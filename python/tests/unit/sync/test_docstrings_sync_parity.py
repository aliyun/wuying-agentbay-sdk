from agentbay._sync.filesystem import FileTransfer
from agentbay._sync.fingerprint import BrowserFingerprintGenerator
from agentbay._sync.mobile_simulate import MobileSimulateService


def test_filetransfer_docstring_is_generic():
    doc = FileTransfer.__doc__ or ""

    assert (
        "Provides pre-signed URL upload/download functionality between local and OSS"
        in doc
    )
    assert "SyncFileTransfer provides" not in doc


def test_fingerprint_class_docstring_mentions_init_args():
    doc = BrowserFingerprintGenerator.__doc__ or ""

    assert "headless" in doc
    assert "use_chrome_channel" in doc


def test_mobile_simulate_upload_mobile_info_raises_section():
    doc = MobileSimulateService.upload_mobile_info.__doc__ or ""

    assert "context_sync is provided but context_sync.context_id is missing" in doc

