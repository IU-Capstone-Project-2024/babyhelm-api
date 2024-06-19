import yaml
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import JSONResponse

from babyhelm.containers.application import ApplicationContainer
from babyhelm.schemas.manifest_builder import Values
from babyhelm.services.manifest_builder import ManifestBuilderService

router = APIRouter(prefix="/manifests", tags=["Manifests"])


@router.post("/render")
@inject
async def render_manifests(
    values: Values,
    manifest_builder_service: ManifestBuilderService = Depends(
        Provide[ApplicationContainer.services.manifest_builder]
    ),
) -> JSONResponse:
    deployment_manifest = manifest_builder_service.render_deployment_manifest(values)
    service_manifest = manifest_builder_service.render_service_manifest(values)
    return JSONResponse(
        content={
            "message": "Manifests rendered",
            "deployment": yaml.safe_load(deployment_manifest),
            "service": yaml.safe_load(service_manifest),
        },
        status_code=status.HTTP_200_OK,
    )
