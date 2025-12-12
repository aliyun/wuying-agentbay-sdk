import importlib.util
import sys
from pathlib import Path


def _load_generate_api_docs_module():
    module_name = "agentbay_generate_api_docs"
    script_path = Path(__file__).resolve().parents[2] / "scripts" / "generate_api_docs.py"
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def test_common_related_resources_link_to_sync_docs():
    module = _load_generate_api_docs_module()
    metadata = {
        "modules": {
            "browser": {
                "related_resources": [
                    {"name": "Session API Reference", "module": "session"},
                ]
            }
        }
    }

    section = module.get_see_also_section("browser", metadata, doc_group="common")
    assert "../sync/session.md" in section


def test_sync_related_resources_link_to_sync_docs():
    module = _load_generate_api_docs_module()
    metadata = {
        "modules": {
            "browser": {
                "related_resources": [
                    {"name": "Session API Reference", "module": "session"},
                ]
            }
        }
    }

    section = module.get_see_also_section("browser", metadata, doc_group="sync")
    assert "- [Session API Reference](./session.md)" in section


def test_async_related_resources_link_to_async_docs():
    module = _load_generate_api_docs_module()
    metadata = {
        "modules": {
            "browser": {
                "related_resources": [
                    {"name": "Session API Reference", "module": "session"},
                ]
            }
        }
    }

    section = module.get_see_also_section("browser", metadata, doc_group="async")
    assert "./async-session.md" in section

