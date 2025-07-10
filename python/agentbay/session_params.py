from typing import Dict, Optional, List
from agentbay.context_sync import ContextSync


class CreateSessionParams:
    """
    Parameters for creating a new session in the AgentBay cloud environment.

    Attributes:
        labels (Optional[Dict[str, str]]): Custom labels for the Session. These can be
            used for organizing and filtering sessions.
        context_id (Optional[str]): ID of the context to bind to the session. The
            context can include various types of persistence like file system (volume)
            and cookies.
    """

    def __init__(
        self,
        labels: Optional[Dict[str, str]] = None,
        context_id: Optional[str] = None,
        image_id: Optional[str] = None,
        context_syncs: Optional[List[ContextSync]] = None,
    ):
        """
        Initialize CreateSessionParams.

        Args:
            labels (Optional[Dict[str, str]], optional): Custom labels for the Session.
                Defaults to None.
            context_id (Optional[str], optional): ID of the context to bind to the
                session. Defaults to None.
            image_id (Optional[str], optional): ID of the image to use for the session.
                Defaults to None.
        """
        self.labels = labels or {}
        self.context_id = context_id
        self.image_id = image_id
        self.context_syncs = context_syncs or []


class ListSessionParams:
    """
    Parameters for listing sessions with pagination support.

    Attributes:
        max_results (int): Number of results per page.
        next_token (str): Token for the next page.
        labels (Dict[str, str]): Labels to filter by.
    """

    def __init__(
        self,
        max_results: int = 10,
        next_token: str = "",
        labels: Optional[Dict[str, str]] = None,
    ):
        """
        Initialize ListSessionParams with default values.

        Args:
            max_results (int, optional): Number of results per page. Defaults to 10.
            next_token (str, optional): Token for the next page. Defaults to "".
            labels (Optional[Dict[str, str]], optional): Labels to filter by.
                Defaults to None.
        """
        self.max_results = max_results
        self.next_token = next_token
        self.labels = labels if labels is not None else {}
