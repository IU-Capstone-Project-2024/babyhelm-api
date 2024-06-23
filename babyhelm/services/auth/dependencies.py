from typing import Annotated

import fastapi
from dependency_injector.wiring import Provide, inject
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from babyhelm.containers.application import ApplicationContainer
from babyhelm.exceptions.auth import NoCredentialsError
from babyhelm.services.auth.service import AuthService

bearer_scheme = HTTPBearer(
    scheme_name="Bearer",
    description="Your JSON Web Token (JWT)",
    bearerFormat="JWT",
    auto_error=False,  # We'll handle error manually
)


@inject
async def get_current_user_id(
        bearer: HTTPAuthorizationCredentials | None = fastapi.Depends(bearer_scheme),
        auth_service: AuthService = fastapi.Depends(
            Provide[ApplicationContainer.services.auth],
        ),
) -> int:
    if not bearer:
        raise NoCredentialsError()
    token = bearer.credentials
    decoded_token = auth_service.decode_jwt(token)
    return decoded_token["sub"]


CURRENT_USER_ID_DEPENDENCY = Annotated[int, fastapi.Depends(get_current_user_id)]
