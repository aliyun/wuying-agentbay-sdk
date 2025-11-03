# -*- coding: utf-8 -*-
"""Version information for the AgentBay SDK."""

import os
from pathlib import Path


def _get_version_from_pyproject() -> str:
    """Read version from pyproject.toml file."""
    try:
        # Get the path to pyproject.toml (relative to this file)
        current_dir = Path(__file__).parent
        pyproject_path = current_dir.parent / "pyproject.toml"
        
        if pyproject_path.exists():
            with open(pyproject_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip().startswith("version = "):
                        # Extract version from: version = "0.9.3"
                        version = line.split("=")[1].strip().strip('"')
                        return version
    except Exception:
        pass
    
    # Fallback version if pyproject.toml cannot be read
    return "0.9.3"


def _is_release_build() -> bool:
    """
    Check if this is a release build.

    This value can be overridden at build time by replacing the line below.
    The CI/CD workflow will replace __AGENTBAY_IS_RELEASE_BUILD__ with True for release builds.
    """
    # This placeholder will be replaced by the build process
    # For release builds: sed -i 's/__AGENTBAY_IS_RELEASE_BUILD__/True/g' agentbay/version.py
    return __AGENTBAY_IS_RELEASE_BUILD__  # Default: False for development builds


__version__ = _get_version_from_pyproject()
# For release builds, the CI/CD will replace __AGENTBAY_IS_RELEASE_BUILD__ with True
__AGENTBAY_IS_RELEASE_BUILD__ = False
__is_release__ = _is_release_build()

