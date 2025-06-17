from typing import Dict, Optional


class CreateSessionParams:
    """
    Parameters for creating a new session in the AgentBay cloud environment.

    Attributes:
        labels (Optional[Dict[str, str]]): Custom labels for the Session. These can be used for organizing and filtering sessions.
        context_id (Optional[str]): ID of the context to bind to the session. The context can include various types of persistence like file system (volume) and cookies.
    """

    def __init__(
        self,
        labels: Optional[Dict[str, str]] = None,
        context_id: Optional[str] = None,
        image_id: Optional[str] = None,
    ):
        """
        Initialize CreateSessionParams.

        Args:
            labels (Optional[Dict[str, str]], optional): Custom labels for the Session. Defaults to None.
            context_id (Optional[str], optional): ID of the context to bind to the session. Defaults to None.
            image_id (Optional[str], optional): ID of the image to use for the session. Defaults to None.
        """
        self.labels = labels or {}
        self.context_id = context_id
        self.image_id = image_id
