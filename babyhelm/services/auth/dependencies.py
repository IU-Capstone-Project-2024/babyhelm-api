from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import Depends
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
def get_current_user_id(
    bearer: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    auth_service: AuthService = Depends(
        Provide[ApplicationContainer.services.auth],
    ),
) -> int:
    if not bearer:
        raise NoCredentialsError()
    token = bearer.credentials
    decoded_token = auth_service.decode_jwt(token)
    return decoded_token["sub"]


CURRENT_USER_ID_DEPENDENCY = Annotated[int, Depends(get_current_user_id)]


class CheckUserPermissions:
    def __init__(
        self,
        action: str,
    ):
        self.action = action

    @inject
    async def __call__(
        self,
        user_id: CURRENT_USER_ID_DEPENDENCY,
        project_name: str = None,
        auth_service: AuthService = Depends(
            Provide[ApplicationContainer.services.auth]
        ),
    ):
        await auth_service.validate_permissions(
            project_name=project_name, user_id=user_id, action=self.action
        )
