from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import JSONResponse

from babyhelm.containers.application import ApplicationContainer
from babyhelm.schemas.manifest_builder import Application
from babyhelm.services.manifest_builder import ManifestBuilderService

router = APIRouter(prefix="/manifests", tags=["Manifests"])


@router.post("/render", deprecated=True)
@inject
async def render_manifests(
    application: Application,
    manifest_builder_service: ManifestBuilderService = Depends(
        Provide[ApplicationContainer.services.manifest_builder]
    ),
) -> JSONResponse:
    return JSONResponse(
        content=manifest_builder_service.render_application(application).model_dump(),
        status_code=status.HTTP_200_OK,
    )
