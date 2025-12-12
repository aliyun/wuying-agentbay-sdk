import shutil
import subprocess
import sys
from pathlib import Path


def test_generate_python_api_docs():
    project_root = Path(__file__).resolve().parents[3]  # Go up to python directory
    docs_dir = project_root / "docs" / "api"

    if docs_dir.exists():
        shutil.rmtree(docs_dir)

    # Use the current Python executable (should be from virtual environment)
    python_executable = sys.executable

    result = subprocess.run(
        [python_executable, "scripts/generate_api_docs.py"],
        cwd=project_root,
        capture_output=True,
        text=True,
    )

    assert (
        result.returncode == 0
    ), f"Script failed with return code {result.returncode}\nStdout: {result.stdout}\nStderr: {result.stderr}"

    # Check sync API docs
    sync_session_file = docs_dir / "sync" / "session.md"
    assert sync_session_file.exists(), "Sync Session documentation was not generated"
    sync_contents = sync_session_file.read_text(encoding="utf-8")
    assert "# Session API Reference" in sync_contents
    assert "Documentation generated automatically" in sync_contents
    assert "💡 Async Version" in sync_contents

    # Check async API docs
    async_session_file = docs_dir / "async" / "async-session.md"
    assert async_session_file.exists(), "Async Session documentation was not generated"
    async_contents = async_session_file.read_text(encoding="utf-8")
    assert "# AsyncSession API Reference" in async_contents
    assert "Documentation generated automatically" in async_contents
    assert "💡 Sync Version" in async_contents

    # Check common docs
    config_file = docs_dir / "common" / "config.md"
    assert config_file.exists(), "Common Config documentation was not generated"

    # Browser Agent models should include constructor signatures (e.g., ActOptions.__init__)
    browser_agent_models = docs_dir / "common" / "browser-agent-models.md"
    assert browser_agent_models.exists(), "Browser Agent Models documentation was not generated"
    browser_agent_content = browser_agent_models.read_text(encoding="utf-8")
    assert (
        "(self, action: str" in browser_agent_content
        or "def __init__(action: str" in browser_agent_content
    ), "ActOptions constructor not documented"

    # Browser models should include BrowserProxy constructor signature
    browser_models = docs_dir / "common" / "browser-models.md"
    assert browser_models.exists(), "Browser Models documentation was not generated"
    browser_models_content = browser_models.read_text(encoding="utf-8")
    assert "(self, proxy_type: Literal" in browser_models_content, "BrowserProxy constructor not documented"
