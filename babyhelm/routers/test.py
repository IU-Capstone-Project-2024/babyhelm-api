import fastapi
from dependency_injector.wiring import inject, Provide
from starlette.responses import JSONResponse

from babyhelm.containers.application import ApplicationContainer
from babyhelm.repositories.user import UserRepository

router = fastapi.APIRouter(prefix="/tg")


@router.post("", status_code=fastapi.status.HTTP_201_CREATED)
@inject
async def save_tg_user(
        user_repository: UserRepository = fastapi.Depends(
            Provide[ApplicationContainer.repositories.user],
        ),
) -> int:
    res = await user_repository.get()
    return res
