from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status

from babyhelm.containers.application import ApplicationContainer
from babyhelm.schemas.cluster_manager import (
    CreateApplicationRequest,
    CreateApplicationResponse,
    CreateProjectResponse,
)
from babyhelm.schemas.manifest_builder import Project
from babyhelm.services.cluster_manager import ClusterManagerService

router = APIRouter(prefix="/clusters", tags=["Clusters"])


@router.post("/create-project", status_code=status.HTTP_201_CREATED)
@inject
async def create_project(
    project: Project,
    cluster_manager_service: ClusterManagerService = Depends(
        Provide[ApplicationContainer.services.cluster_manager]
    ),
) -> CreateProjectResponse:
    return await cluster_manager_service.create_project(project)


@router.post("/create-application", status_code=status.HTTP_201_CREATED)
@inject
async def create_application(
    app: CreateApplicationRequest,
    cluster_manager_service: ClusterManagerService = Depends(
        Provide[ApplicationContainer.services.cluster_manager]
    ),
) -> CreateApplicationResponse:
    return await cluster_manager_service.create_application(app=app)
