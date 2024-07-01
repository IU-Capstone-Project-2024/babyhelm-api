from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status

from babyhelm.containers.application import ApplicationContainer
from babyhelm.schemas.cluster_manager import (
    ApplicationSchema,
    ApplicationWithLinkSchema,
    CreateApplicationRequest,
)
from babyhelm.services.auth.dependencies import CURRENT_USER_ID_DEPENDENCY
from babyhelm.services.cluster_manager import ClusterManagerService

router = APIRouter(prefix="/applications", tags=["Applications"])


@router.post("/{project_name}", status_code=status.HTTP_201_CREATED)
@inject
async def create_application(
    project_name: str,
    app: CreateApplicationRequest,
    user_id: CURRENT_USER_ID_DEPENDENCY,
    cluster_manager_service: ClusterManagerService = Depends(
        Provide[ApplicationContainer.services.cluster_manager]
    ),
) -> ApplicationWithLinkSchema:
    # TODO assure that user has permissions (by auth service)
    return await cluster_manager_service.create_application(
        app=app, project_name=project_name
    )


@router.get("/{project_name}/{application_name}")
@inject
async def get_application(
    project_name: str,
    application_name: str,
    user_id: CURRENT_USER_ID_DEPENDENCY,
    cluster_manager_service: ClusterManagerService = Depends(
        Provide[ApplicationContainer.services.cluster_manager]
    ),
) -> ApplicationSchema:
    # TODO assure that user has permissions (by auth service)
    application = await cluster_manager_service.get_application(
        project_name=project_name, application_name=application_name
    )
    return application


@router.get("/{project_name}")
@inject
async def list_application(
    project_name: str,
    user_id: CURRENT_USER_ID_DEPENDENCY,
    cluster_manager_service: ClusterManagerService = Depends(
        Provide[ApplicationContainer.services.cluster_manager]
    ),
) -> list[ApplicationSchema]:
    # TODO assure that user has permissions (by auth service)
    apps = await cluster_manager_service.list_applications(project_name=project_name)
    return apps


@router.delete(
    "/{project_name}/{application_name}", status_code=status.HTTP_204_NO_CONTENT
)
@inject
async def delete_application(
    project_name: str,
    application_name: str,
    user_id: CURRENT_USER_ID_DEPENDENCY,
    cluster_manager_service: ClusterManagerService = Depends(
        Provide[ApplicationContainer.services.cluster_manager]
    ),
):
    # TODO assure that user has permissions (by auth service)
    await cluster_manager_service.delete_application(
        application_name=application_name, project_name=project_name
    )


@router.patch("/{project_name}/{application_name}/restart")
@inject
async def restart_application(
    project_name: str,
    application_name: str,
    user_id: CURRENT_USER_ID_DEPENDENCY,
    cluster_manager_service: ClusterManagerService = Depends(
        Provide[ApplicationContainer.services.cluster_manager]
    ),
):
    # TODO assure that user has permissions (by auth service)
    await cluster_manager_service.restart_application(
        application_name=application_name, project_name=project_name
    )
