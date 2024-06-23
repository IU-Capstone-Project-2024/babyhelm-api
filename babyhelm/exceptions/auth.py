import fastapi

from babyhelm.exceptions.base import HttpError


class TokenExpiredError(HttpError):
    """Token expired error."""

    status_code = fastapi.status.HTTP_401_UNAUTHORIZED
    detail = "Token expired"


class InvalidTokenError(HttpError):
    """Invalid token error."""

    status_code = fastapi.status.HTTP_401_UNAUTHORIZED
    detail = "Invalid token"


class InvalidCredentialsError(HttpError):
    """Unauthorized error."""

    status_code = fastapi.status.HTTP_400_BAD_REQUEST
    detail = "Invalid username or password"


class NoCredentialsError(HttpError):
    """No credentials error."""

    status_code = fastapi.status.HTTP_401_UNAUTHORIZED
    detail = "Unauthorized"


class UserNotFoundError(HttpError):
    """User not found error"""

    status_code = fastapi.status.HTTP_400_BAD_REQUEST
    detail = "User not found"
