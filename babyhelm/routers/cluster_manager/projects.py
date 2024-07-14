from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from starlette import status

from babyhelm.containers.application import ApplicationContainer
from babyhelm.schemas.cluster_manager import ProjectSchema
from babyhelm.schemas.manifest_builder import Project
from babyhelm.schemas.user import (
    AddUserToProjectRequestSchema,
    DeleteUserFromProjectRequestSchema,
)
from babyhelm.services.auth.dependencies import (
    CURRENT_USER_ID_DEPENDENCY,
    CheckUserPermissions,
)
from babyhelm.services.auth.utils import ActionEnum
from babyhelm.services.cluster_manager import ClusterManagerService

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("", status_code=status.HTTP_201_CREATED)
@inject
async def create_project(
    user_id: CURRENT_USER_ID_DEPENDENCY,
    project: Project,
    cluster_manager_service: ClusterManagerService = Depends(
        Provide[ApplicationContainer.services.cluster_manager]
    ),
) -> ProjectSchema:
    return await cluster_manager_service.create_project(project, user_id)


@router.delete("/{project_name}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_project(
    project_name: str,
    permitted=Depends(CheckUserPermissions(action=ActionEnum.DELETE.name)),
    cluster_manager_service: ClusterManagerService = Depends(
        Provide[ApplicationContainer.services.cluster_manager]
    ),
):
    await cluster_manager_service.delete_project(project_name)


@router.get("", status_code=status.HTTP_200_OK)
@inject
async def list_projects(
    user_id: CURRENT_USER_ID_DEPENDENCY,
    cluster_manager_service: ClusterManagerService = Depends(
        Provide[ApplicationContainer.services.cluster_manager]
    ),
) -> list[ProjectSchema]:
    return await cluster_manager_service.list_projects(user_id)


@router.get("/{project-name}", status_code=status.HTTP_200_OK)
@inject
async def get_project(
    project_name: str,
    permitted=Depends(CheckUserPermissions(action=ActionEnum.READ.name)),
    cluster_manager_service: ClusterManagerService = Depends(
        Provide[ApplicationContainer.services.cluster_manager]
    ),
) -> ProjectSchema:
    return await cluster_manager_service.get_project(project_name)


@router.post("/{project-name}/add_user", status_code=status.HTTP_200_OK)
@inject
async def add_user_to_the_project(
    project_name: str,
    request: AddUserToProjectRequestSchema,
    permitted=Depends(CheckUserPermissions(action=ActionEnum.ADD_NEW_USER.name)),
    cluster_manager_service: ClusterManagerService = Depends(
        Provide[ApplicationContainer.services.cluster_manager]
    ),
) -> None:
    """Add new registered user to a project or update role of already joined to a project."""
    return await cluster_manager_service.add_new_user_to_the_project(
        user_email=request.email, project_name=project_name, role=request.role.name
    )


@router.delete("/{project-name}/delete_user", status_code=status.HTTP_200_OK)
@inject
async def delete_user(
    project_name: str,
    request: DeleteUserFromProjectRequestSchema,
    permitted=Depends(CheckUserPermissions(action=ActionEnum.DELETE.name)),
    cluster_manager_service: ClusterManagerService = Depends(
        Provide[ApplicationContainer.services.cluster_manager]
    ),
) -> None:
    """Delete user from the project."""
    return await cluster_manager_service.delete_user_from_the_project(
        user_email=request.email, project_name=project_name
    )
