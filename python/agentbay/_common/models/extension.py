from typing import List, Optional

EXTENSIONS_BASE_PATH = "/tmp/extensions"


class Extension:
    """Represents a browser extension as a cloud resource."""

    def __init__(self, id: str, name: str, created_at: Optional[str] = None):
        self.id = id
        self.name = name
        self.created_at = created_at  # Retrieved from the cloud


class ExtensionOption:
    """
    Configuration options for browser extension integration.

    This class encapsulates the necessary parameters for setting up
    browser extension synchronization and context management.

    Attributes:
        context_id (str): ID of the extension context for browser extensions
        extension_ids (List[str]): List of extension IDs to be loaded/synchronized
    """

    def __init__(self, context_id: str, extension_ids: List[str]):
        """
        Initialize ExtensionOption with context and extension configuration.

        Args:
            context_id (str): ID of the extension context for browser extensions.
                             This should match the context where extensions are stored.
            extension_ids (List[str]): List of extension IDs to be loaded in the browser session.
                                      Each ID should correspond to a valid extension in the context.

        Raises:
            ValueError: If context_id is empty or extension_ids is empty.
        """
        if not context_id or not context_id.strip():
            raise ValueError("context_id cannot be empty")

        if not extension_ids or len(extension_ids) == 0:
            raise ValueError("extension_ids cannot be empty")

        self.context_id = context_id
        self.extension_ids = extension_ids

    def __repr__(self) -> str:
        """String representation of ExtensionOption."""
        return (
            f"ExtensionOption(context_id='{self.context_id}', extension_ids={self.extension_ids})"
        )

    def __str__(self) -> str:
        """Human-readable string representation."""
        return f"Extension Config: {len(self.extension_ids)} extension(s) in context '{self.context_id}'"

    def validate(self) -> bool:
        """
        Validate the extension option configuration.

        Returns:
            bool: True if configuration is valid, False otherwise.
        """
        try:
            if not self.context_id or not self.context_id.strip():
                return False

            if not self.extension_ids or len(self.extension_ids) == 0:
                return False

            for ext_id in self.extension_ids:
                if not isinstance(ext_id, str) or not ext_id.strip():
                    return False

            return True
        except Exception:
            return False


