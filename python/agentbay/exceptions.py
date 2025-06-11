class AgentBayError(Exception):
    """Base exception for all AgentBay errors."""

    def __init__(self, message=None, *args, **kwargs):
        if message is None:
            message = self.__class__.__name__
        super().__init__(message, *args)
        self.extra = kwargs


class AuthenticationError(AgentBayError):
    """Raised when there is an authentication error."""

    def __init__(self, message="Authentication failed", *args, **kwargs):
        super().__init__(message, *args, **kwargs)


class APIError(AgentBayError):
    """Raised when there is an error with the API."""

    def __init__(self, message="API error", status_code=None, *args, **kwargs):
        super().__init__(message, *args, **kwargs)
        self.status_code = status_code


class FileError(AgentBayError):
    """Raised when there is an error with file operations."""

    def __init__(self, message="File operation error", *args, **kwargs):
        super().__init__(message, *args, **kwargs)


class CommandError(AgentBayError):
    """Raised when there is an error with command execution."""

    def __init__(self, message="Command execution error", *args, **kwargs):
        super().__init__(message, *args, **kwargs)


class SessionError(AgentBayError):
    """Raised when there is an error with the session."""

    def __init__(self, message="Session error", *args, **kwargs):
        super().__init__(message, *args, **kwargs)