import fastapi
from dependency_injector.wiring import Provide, inject
from starlette import status

from babyhelm.containers.application import ApplicationContainer
from babyhelm.schemas.auth import TokenSchema
from babyhelm.schemas.user import AuthUserScheme, ResponseUserScheme
from babyhelm.services.auth.dependencies import CURRENT_USER_ID_DEPENDENCY
from babyhelm.services.auth.service import AuthService
from babyhelm.services.user import UserService

router = fastapi.APIRouter(prefix="/users", tags=["Users"])


@router.post("/registration", status_code=status.HTTP_201_CREATED)
@inject
async def create_user(
    user_data: AuthUserScheme,
    user_service: UserService = fastapi.Depends(
        Provide[ApplicationContainer.services.user],
    ),
):
    await user_service.create(
        email=user_data.email, raw_password=user_data.raw_password
    )


@router.post("/login", response_model=TokenSchema, status_code=status.HTTP_200_OK)
@inject
async def login(
    user_data: AuthUserScheme,
    auth_service: AuthService = fastapi.Depends(
        Provide[ApplicationContainer.services.auth],
    ),
):
    return await auth_service.authenticate_user(
        email=user_data.email, password=user_data.raw_password
    )


@router.get("/me", responses={status.HTTP_200_OK: {"description": "Current user info"}})
@inject
async def get_me(
    user_id: CURRENT_USER_ID_DEPENDENCY,
    user_service: UserService = fastapi.Depends(
        Provide[ApplicationContainer.services.user],
    ),
) -> ResponseUserScheme:
    """
    Get current user info if authenticated.
    """
    user: ResponseUserScheme = await user_service.get(user_id)
    return user


@router.post("/refresh-access-token", response_model=TokenSchema, status_code=status.HTTP_200_OK)
@inject
async def refresh_access_token(
    refresh_token: str,
    auth_service: AuthService = fastapi.Depends(
        Provide[ApplicationContainer.services.auth],
    ),
):
    try:
        new_access_token = await auth_service.refresh_access_token(refresh_token)
        return TokenSchema(access_token=new_access_token, refresh_token=refresh_token, token_type="Bearer")
    except Exception as e:
        raise fastapi.HTTPException(status_code=401, detail=str(e))