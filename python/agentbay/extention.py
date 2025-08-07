import os
import uuid
import requests
from typing import TYPE_CHECKING, List, Optional

from agentbay.exceptions import AgentBayError
from agentbay.model.response import OperationResult

if TYPE_CHECKING:
    from agentbay.agentbay import AgentBay
    from agentbay.context import ContextService

# ==============================================================================
# Constants
# ==============================================================================
EXTENSIONS_BASE_PATH = "/tmp/extensions"

# ==============================================================================
# 1. Data Models (Unchanged)
# ==============================================================================
class Extension:
    """Represents a browser extension as a cloud resource."""
    def __init__(self, id: str, name: str, created_at: Optional[str] = None):
        self.id = id
        self.name = name
        self.created_at = created_at # Retrieved from the cloud

# ==============================================================================
# 2. Core Service Class (Scoped Stateless Model)
# ==============================================================================

class ExtensionsService:
    """
    Provides methods to manage user browser extensions.
    This service integrates with the existing context functionality for file operations.
    
    **Important**: Users must create or obtain a context before initializing this service.
    The context will be used to store all extension files in the cloud.
    
    **User Workflow**:
    1. Create or get a context using `agent_bay.context.get("context_name", create=True)`
    2. Initialize ExtensionsService with the context ID
    3. Use the service methods to manage extensions
    
    Example:
    ```python
    # Step 1: User creates/gets context
    context_result = agent_bay.context.get("browser_extensions", create=True)
    if not context_result.success:
        raise Exception("Failed to create context")
    
    # Step 2: Initialize service with context
    extensions_service = ExtensionsService(agent_bay, context_result.context_id)
    
    # Step 3: Use the service
    extension = extensions_service.create("/path/to/plugin.zip")
    ```
    """

    def __init__(self, agent_bay: "AgentBay", context_id: str):
        """
        Initializes the ExtensionsService with a user-provided context.

        Args:
            agent_bay (AgentBay): The AgentBay client instance.
            context_id (str): The context ID where extensions will be stored.
                             This context must already exist or be created by the user
                             before initializing the service.
                             
        Note:
            Users are responsible for creating the context before using this service.
            Use `agent_bay.context.get(context_name, create=True)` to create a context.
        """
        self.agent_bay = agent_bay
        self.context_id = context_id
        self.context_service: "ContextService" = agent_bay.context

    def _upload_to_cloud(self, local_path: str, remote_path: str):
        """
        An internal helper method that encapsulates the flow of "get upload URL for a specific path and upload".
        Uses the existing context service for file operations.

        Args:
            local_path (str): The path to the local file.
            remote_path (str): The path of the file in context storage.
        
        Raises:
            AgentBayError: If getting the credential or uploading fails.
        """
        # 1. Get upload URL using context service
        try:
            url_result = self.context_service.get_file_upload_url(self.context_id, remote_path);
            if not url_result.success or not url_result.url:
                raise AgentBayError(f"Failed to get upload URL: {url_result.url if url_result.url else 'No URL returned'}")
            
            pre_signed_url = url_result.url
        except Exception as e:
            raise AgentBayError(f"An error occurred while requesting the upload URL: {e}") from e

        # 2. Use the presigned URL to upload the file directly
        try:
            with open(local_path, 'rb') as f:
                response = requests.put(pre_signed_url, data=f)
                response.raise_for_status()  # This will raise an HTTPError if the status is 4xx or 5xx
        except requests.exceptions.RequestException as e:
            raise AgentBayError(f"An error occurred while uploading the file: {e}") from e

    def list(self) -> List[Extension]:
        """
        Lists all available browser extensions within this context from the cloud.
        Uses the context service to list files under the extensions directory.
        """
        try:
            # Use context service to list files in the extensions directory
            file_list_result = self.context_service.list_files(
                context_id=self.context_id,
                parent_folder_path=EXTENSIONS_BASE_PATH,
                page_number=1,
                page_size=100  # Reasonable limit for extensions
            )

            if not file_list_result.success:
                raise AgentBayError("Failed to list extensions: Context file listing failed.")

            extensions = []
            for file_entry in file_list_result.entries:
                # Extract the extension ID from the file name
                extension_id = file_entry.file_name
                extensions.append(Extension(
                    id=extension_id,
                    name=file_entry.file_name,
                    created_at=file_entry.gmt_create
                ))
            return extensions
        except Exception as e:
            raise AgentBayError(f"An error occurred while listing browser extensions: {e}") from e

    def create(self, local_path: str) -> Extension:
        """Uploads a new browser extension from a local path into the current context."""
        if not os.path.exists(local_path):
            raise FileNotFoundError(f"The specified local file was not found: {local_path}")
        
        # Determine the ID and cloud path before uploading
        # Validate file type - only ZIP format is supported
        file_extension = os.path.splitext(local_path)[1].lower()
        if file_extension != '.zip':
            raise ValueError(f"Unsupported plugin format '{file_extension}'. Only ZIP format (.zip) is supported.")
        
        extension_id = f"ext_{uuid.uuid4().hex}{file_extension}"
        extension_name = os.path.basename(local_path)
        remote_path = f"{EXTENSIONS_BASE_PATH}/{extension_id}"

        # Use the helper method to perform the cloud upload
        self._upload_to_cloud(local_path, remote_path)
        
        # Upload implies creation. Return a locally constructed object with basic info.
        return Extension(id=extension_id, name=extension_name)

    def update(self, extension_id: str, new_local_path: str) -> Extension:
        """Updates an existing browser extension in the current context with a new file."""
        if not os.path.exists(new_local_path):
            raise FileNotFoundError(f"The specified new local file was not found: {new_local_path}")

        # Validate that the extension exists by checking the file list
        existing_extensions = {ext.id: ext for ext in self.list()}
        if extension_id not in existing_extensions:
            raise ValueError(f"Browser extension with ID '{extension_id}' not found in the context. Cannot update.")

        remote_path = f"{EXTENSIONS_BASE_PATH}/{extension_id}"
        
        # Use the helper method to perform the cloud upload (overwrite)
        self._upload_to_cloud(new_local_path, remote_path)

        return Extension(id=extension_id, name=os.path.basename(new_local_path))

    def _get_extension_info(self, extension_id: str) -> Optional[Extension]:
        """
        Gets detailed information about a specific browser extension.
        
        Args:
            extension_id (str): The ID of the extension to get info for.
            
        Returns:
            Optional[Extension]: Extension object if found, None otherwise.
        """
        try:
            extensions = self.list()
            for ext in extensions:
                if ext.id == extension_id:
                    return ext
            return None
        except Exception as e:
            print(f"An error occurred while getting extension info for '{extension_id}': {e}")
            return None

    def delete(self, extension_id: str) -> bool:
        """Deletes a browser extension from the current context."""
        remote_path = f"{EXTENSIONS_BASE_PATH}/{extension_id}"
        try:
            # Use context service to delete the file
            delete_result = self.context_service.delete_file(self.context_id, remote_path)
            
            return delete_result.success
        except Exception as e:
            print(f"An error occurred while deleting browser extension '{extension_id}': {e}")
            return False
