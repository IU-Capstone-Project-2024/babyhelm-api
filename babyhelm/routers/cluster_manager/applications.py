from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status

from babyhelm.containers.application import ApplicationContainer
from babyhelm.schemas.cluster_manager import (
    ApplicationSchema,
    ApplicationWithLinkSchema,
    ApplicationWithPayloadSchema,
    CreateApplicationRequest,
)
from babyhelm.services.auth.dependencies import CheckUserPermissions
from babyhelm.services.auth.utils import ActionEnum
from babyhelm.services.cluster_manager import ClusterManagerService

router = APIRouter(prefix="/applications", tags=["Applications"])


@router.post("/{project_name}", status_code=status.HTTP_201_CREATED)
@inject
async def create_application(
    project_name: str,
    app: CreateApplicationRequest,
    permitted=Depends(CheckUserPermissions(action=ActionEnum.CREATE.name)),
    cluster_manager_service: ClusterManagerService = Depends(
        Provide[ApplicationContainer.services.cluster_manager]
    ),
) -> ApplicationWithLinkSchema:
    return await cluster_manager_service.create_application(
        app=app, project_name=project_name
    )


@router.get("/{project_name}/{application_name}")
@inject
async def get_application(
    project_name: str,
    application_name: str,
    permitted=Depends(CheckUserPermissions(action=ActionEnum.READ.name)),
    cluster_manager_service: ClusterManagerService = Depends(
        Provide[ApplicationContainer.services.cluster_manager]
    ),
) -> ApplicationWithPayloadSchema:
    application = await cluster_manager_service.get_application_with_payload(
        project_name=project_name, application_name=application_name
    )
    return application


@router.get("/{project_name}")
@inject
async def list_application(
    project_name: str,
    permitted=Depends(CheckUserPermissions(action=ActionEnum.READ.name)),
    cluster_manager_service: ClusterManagerService = Depends(
        Provide[ApplicationContainer.services.cluster_manager]
    ),
) -> list[ApplicationSchema]:
    apps = await cluster_manager_service.list_applications(project_name=project_name)
    return apps


@router.delete(
    "/{project_name}/{application_name}", status_code=status.HTTP_204_NO_CONTENT
)
@inject
async def delete_application(
    project_name: str,
    application_name: str,
    permitted=Depends(CheckUserPermissions(action=ActionEnum.DELETE.name)),
    cluster_manager_service: ClusterManagerService = Depends(
        Provide[ApplicationContainer.services.cluster_manager]
    ),
):
    await cluster_manager_service.delete_application(
        application_name=application_name, project_name=project_name
    )


@router.patch("/{project_name}/{application_name}/restart")
@inject
async def restart_application(
    project_name: str,
    application_name: str,
    permitted=Depends(CheckUserPermissions(action=ActionEnum.RESTART.name)),
    cluster_manager_service: ClusterManagerService = Depends(
        Provide[ApplicationContainer.services.cluster_manager]
    ),
):
    await cluster_manager_service.restart_application(
        application_name=application_name, project_name=project_name
    )
