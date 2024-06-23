from fastapi import HTTPException


class HttpError(HTTPException):
    """Base http exception."""

    status_code: int = NotImplemented
    detail: str = "Http exception."

    def __init__(self, detail: str = ""):
        """."""
        super().__init__(status_code=self.status_code, detail=detail or self.detail)


class ClusterManagerError(Exception):
    """
    Custom exception class for Cluster Manager Service errors.
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
