import fastapi

from babyhelm.exceptions.base import HttpError


class BadRequestError(HttpError):
    """Bad request error."""

    status_code = fastapi.status.HTTP_400_BAD_REQUEST
    detail = "Bad request"

class TokenExpiredError(HttpError):
    """Token expired error."""

    status_code = fastapi.status.HTTP_401_UNAUTHORIZED
    detail = "Token expired"

class InvalidTokenError(HttpError):
    """Invalid token error."""

    status_code = fastapi.status.HTTP_401_UNAUTHORIZED
    detail = "Invalid token"

class UnauthorizedError(HttpError):
    """Unauthorized error."""

    status_code = fastapi.status.HTTP_401_UNAUTHORIZED
    detail = "Invalid username or password"
