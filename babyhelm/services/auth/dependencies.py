from typing import Annotated, Optional

import fastapi
from dependency_injector.wiring import Provide, inject
from fastapi import HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from babyhelm.containers.application import ApplicationContainer
from babyhelm.exceptions.auth import NoCredentialsError
from babyhelm.services.auth.service import AuthService
from babyhelm.services.auth.utils import ActionEnum

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
    print("JASHASHAHJS")
    print("Bearer", bearer)
    if not bearer:
        raise NoCredentialsError()
    token = bearer.credentials
    decoded_token = auth_service.decode_jwt(token)
    return decoded_token["sub"]


CURRENT_USER_ID_DEPENDENCY = Annotated[int, Depends(get_current_user_id)]


def check_permissions(
        user_id: int = Depends(get_current_user_id),
        action: str = None,
        project_name: str = None
) -> bool:
    print(f"User ID: {user_id}, Action: {action}, Project Name: {project_name}")
    # Example permission check logic (replace with actual logic)
    if action == "delete" and project_name == "example_project":  # Example check
        return True
    raise HTTPException(status_code=403, detail="Not enough permissions")
