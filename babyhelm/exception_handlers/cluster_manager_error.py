from fastapi import Request
from fastapi.responses import JSONResponse
from starlette import status

from babyhelm.exceptions.base import ClusterManagerError


async def handler(request: Request, exc: ClusterManagerError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": exc.message},
    )


handler_info = {"exc_class_or_status_code": ClusterManagerError, "handler": handler}

__all__ = ["handler_info"]
