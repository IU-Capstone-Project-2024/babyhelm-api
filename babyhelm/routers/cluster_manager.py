from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import JSONResponse

from babyhelm.containers.application import ApplicationContainer
from babyhelm.schemas.cluster_manager import ApplicationRequest
from babyhelm.schemas.manifest_builder import Project
from babyhelm.services.cluster_manager import ClusterManagerService

router = APIRouter(prefix="/clusters", tags=["Clusters"])


@router.post(
    "/create-project",
    responses={
        200: {
            "description": "Successful Response",
            "content": {
                "application/json": {
                    "example": {"message": "Project 'MyProject' is created"}
                }
            },
        },
        500: {
            "description": "Server side error",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Error creating 'MyProject'"
                    }
                }
            },
        },
    },
)
@inject
async def create_project(
    project: Project,
    cluster_manager_service: ClusterManagerService = Depends(
        Provide[ApplicationContainer.services.cluster_manager]
    ),
) -> JSONResponse:
    await cluster_manager_service.create_project(project)
    return JSONResponse(
        content={"message": f"Project '{project.name}' is created"},
        status_code=status.HTTP_200_OK,
    )


@router.post(
    "/create-application",
    responses={
        200: {
            "description": "Successful Response",
            "content": {
                "application/json": {
                    "example": {"message": "Application 'MyApplication' is created"}
                }
            },
        },
        500: {
            "description": "Server side error",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Error creating 'MyApplication'"
                    }
                }
            },
        },
    },
)
@inject
async def create_application(
    app: ApplicationRequest,
    cluster_manager_service: ClusterManagerService = Depends(
        Provide[ApplicationContainer.services.cluster_manager]
    ),
) -> JSONResponse:
    await cluster_manager_service.create_application(app=app)
    return JSONResponse(
        content={"message": f"Application '{app.application.name}' is created"},
        status_code=status.HTTP_200_OK,
    )
