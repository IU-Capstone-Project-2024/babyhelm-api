from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import JSONResponse

from babyhelm.containers.application import ApplicationContainer
from babyhelm.schemas.namespace import Values
from babyhelm.services.cluster_manager import ClusterManagerService

router = APIRouter(prefix="/clusters", tags=["Clusters"])


@router.post("/create-project")
@inject
async def create_namespace(
        values: Values,
        cluster_manager_service: ClusterManagerService = Depends(
            Provide[ApplicationContainer.services.cluster_manager]
        )
) -> JSONResponse:
    # TODO wrtie logic of creation and adding to db
    await cluster_manager_service.create_namespace(values.project)
    return JSONResponse(
        content={
            "message": f"Project {values.project.name} is created"
        },
        status_code=status.HTTP_200_OK
    )
