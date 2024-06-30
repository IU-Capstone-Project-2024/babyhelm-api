import fastapi
from dependency_injector.wiring import Provide, inject
from starlette import status

from babyhelm.containers.application import ApplicationContainer
from babyhelm.models import User
from babyhelm.schemas.auth import TokenSchema
from babyhelm.schemas.user import AuthUserSchema, UserSchema
from babyhelm.services.auth.dependencies import CURRENT_USER_ID_DEPENDENCY
from babyhelm.services.auth.service import AuthService
from babyhelm.services.user import UserService

router = fastapi.APIRouter(prefix="/users", tags=["Users"])


@router.post("/registration", status_code=status.HTTP_201_CREATED)
@inject
async def create_user(
    user_data: AuthUserSchema,
    user_service: UserService = fastapi.Depends(
        Provide[ApplicationContainer.services.user],
    ),
) -> None:
    """Register a new user."""
    await user_service.create(
        email=user_data.email, raw_password=user_data.raw_password
    )


@router.post("/login", status_code=status.HTTP_200_OK)
@inject
async def login(
    user_data: AuthUserSchema,
    auth_service: AuthService = fastapi.Depends(
        Provide[ApplicationContainer.services.auth],
    ),
) -> TokenSchema:
    """Login a user."""
    return await auth_service.authenticate_user(
        email=user_data.email, password=user_data.raw_password
    )


@router.get("/me", status_code=status.HTTP_200_OK)
@inject
async def get_me(
    user_id: CURRENT_USER_ID_DEPENDENCY,
    user_service: UserService = fastapi.Depends(
        Provide[ApplicationContainer.services.user],
    ),
) -> UserSchema:
    """Get current user info if authenticated."""
    return UserSchema.model_validate(
        (await user_service.get(User.id == user_id)).model_dump()
    )


@router.post("/refresh_token", status_code=status.HTTP_200_OK)
@inject
async def refresh_access_token(
    refresh_token: str,
    auth_service: AuthService = fastapi.Depends(
        Provide[ApplicationContainer.services.auth],
    ),
) -> TokenSchema:
    """Refresh an access token based on a refresh token."""
    return await auth_service.refresh_access_token(refresh_token)
