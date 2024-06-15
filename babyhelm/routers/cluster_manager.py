from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import JSONResponse
from fastapi.exceptions import HTTPException

from babyhelm.containers.application import ApplicationContainer
from babyhelm.schemas.namespace import Values
from babyhelm.services.cluster_manager import ClusterManagerService
from babyhelm.exceptions.cluster_manager import ClusterManagerError

router = APIRouter(prefix="/clusters", tags=["Clusters"])


@router.post("/create-project")
@inject
async def create_namespace(
        values: Values,
        cluster_manager_service: ClusterManagerService = Depends(
            Provide[ApplicationContainer.services.cluster_manager]
        )
) -> JSONResponse:
    try:
        await cluster_manager_service.create_namespace(values.project)
    except ClusterManagerError as e:
        raise HTTPException(status_code=500, detail=f"Error while creating project '{values.project.name}': " 
                                                    f"{e.message}")
    return JSONResponse(
        content={
            "message": f"Project '{values.project.name}' is created"
        },
        status_code=status.HTTP_200_OK
    )
