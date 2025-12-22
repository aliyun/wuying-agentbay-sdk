# -*- coding: utf-8 -*-
"""Version information for the AgentBay SDK."""

from pathlib import Path


def _get_version() -> str:
    """
    Get the version from package metadata.

    This function tries to get the version from installed package metadata first,
    and falls back to reading pyproject.toml if running in development mode.
    """
    try:
        # Try to get version from installed package metadata (works in production)
        from importlib.metadata import PackageNotFoundError, version

        try:
            return version("wuying-agentbay-sdk")
        except PackageNotFoundError:
            pass
    except ImportError:
        # Python < 3.8, try importlib_metadata
        try:
            from importlib_metadata import PackageNotFoundError, version

            try:
                return version("wuying-agentbay-sdk")
            except PackageNotFoundError:
                pass
        except ImportError:
            pass

    # Fallback: Read version from pyproject.toml (works in development)
    try:
        current_dir = Path(__file__).parent
        pyproject_path = current_dir.parent / "pyproject.toml"

        if pyproject_path.exists():
            with open(pyproject_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip().startswith("version = "):
                        # Extract version from: version = "0.13.0"
                        version_str = line.split("=")[1].strip().strip('"')
                        return version_str
    except Exception:
        pass

    # Last resort fallback
    return "0.0.0-dev"


def _is_release_build() -> bool:
    """
    Check if this is a release build.

    This value can be overridden at build time by replacing the line below.
    The CI/CD workflow will replace __AGENTBAY_IS_RELEASE_BUILD__ with True for release builds.
    """
    # This placeholder will be replaced by the build process
    # For release builds: sed -i 's/__AGENTBAY_IS_RELEASE_BUILD__/True/g' agentbay/_common/version.py
    return __AGENTBAY_IS_RELEASE_BUILD__  # Default: False for development builds


__version__ = _get_version()
# For release builds, the CI/CD will replace __AGENTBAY_IS_RELEASE_BUILD__ with True
__AGENTBAY_IS_RELEASE_BUILD__ = False
__is_release__ = _is_release_build()
