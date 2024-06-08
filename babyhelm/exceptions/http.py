import fastapi

from babyhelm.exceptions.base import HttpError


class BadRequestError(HttpError):
    """Bad request error."""

    status_code = fastapi.status.HTTP_400_BAD_REQUEST
    detail = "Bad request"
