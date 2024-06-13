import fastapi
from dependency_injector.wiring import inject, Provide

from babyhelm.containers.application import ApplicationContainer
from babyhelm.schemas.user import CreateUser, TokenSchema, UserSchema
from babyhelm.services.user import UserService

router = fastapi.APIRouter(prefix="/users", tags=["Users"])


@router.post("/registration", status_code=fastapi.status.HTTP_201_CREATED)
@inject
async def create_user(
        user_data: CreateUser,
        user_service: UserService = fastapi.Depends(
            Provide[ApplicationContainer.services.user],
        ),
):
    await user_service.create(email=user_data.email, raw_password=user_data.raw_password)

@router.post("/login", response_model=TokenSchema)
@inject
async def login(
        user_data: UserSchema,
        user_service: UserService = fastapi.Depends(
            Provide[ApplicationContainer.services.user],
        ),
):
    return await user_service.authenticate(username=user_data.username, password=user_data.row_password)