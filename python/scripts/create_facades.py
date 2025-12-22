import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AGENTBAY_DIR = os.path.join(ROOT, "agentbay")

FACADES = {
    "agentbay.py": "from ._sync.agentbay import *",
    "session.py": "from ._sync.session import *",
    "context.py": "from ._sync.context import *",
    "context_manager.py": "from ._sync.context_manager import *",
    "context_sync.py": "from ._common.params.context_sync import *",
    "session_params.py": "from ._common.params.session_params import *",
    "filesystem/filesystem.py": "from .._sync.filesystem import *",
    "computer/computer.py": "from .._sync.computer import *",
    "mobile/mobile.py": "from .._sync.mobile import *",
    "oss/oss.py": "from .._sync.oss import *",
    "code/code.py": "from .._sync.code import *",
    "command/command.py": "from .._sync.command import *",
    "agent/agent.py": "from .._sync.agent import *",
    "browser/browser.py": "from .._sync.browser import *",
    "browser/browser_agent.py": "from .._sync.browser_agent import *",
    "browser/fingerprint.py": "from .._sync.fingerprint import *",
}

def create_facades():
    for rel_path, content in FACADES.items():
        file_path = os.path.join(AGENTBAY_DIR, rel_path)
        if os.path.exists(file_path):
            print(f"Creating facade for {rel_path}...")
            with open(file_path, "w") as f:
                f.write(content + "\n")
        else:
            print(f"Warning: {rel_path} does not exist. Skipping.")

if __name__ == "__main__":
    create_facades()

