from typing import Annotated

import fastapi
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from starlette import status

from babyhelm.containers.application import ApplicationContainer
from babyhelm.schemas.cluster_manager import ProjectSchema
from babyhelm.schemas.manifest_builder import Project
from babyhelm.services.auth.dependencies import CURRENT_USER_ID_DEPENDENCY, check_permissions, get_current_user_id
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
        user_id: CURRENT_USER_ID_DEPENDENCY,
        cluster_manager_service: ClusterManagerService = Depends(
            Provide[ApplicationContainer.services.cluster_manager]
        ),
):
    # TODO assure that user has permissions (by auth service)
    await cluster_manager_service.delete_project(project_name)


@router.get("")
@inject
async def list_projects(
        user_id: CURRENT_USER_ID_DEPENDENCY,
        cluster_manager_service: ClusterManagerService = Depends(
            Provide[ApplicationContainer.services.cluster_manager]
        ),
) -> list[ProjectSchema]:
    return await cluster_manager_service.list_projects(user_id)


@router.get("/{project-name}")
@inject
async def get_project(
        project_name: str,
        user_id: CURRENT_USER_ID_DEPENDENCY,
        cluster_manager_service: ClusterManagerService = Depends(
            Provide[ApplicationContainer.services.cluster_manager]
        ),
) -> ProjectSchema:
    # TODO assure that user has permissions (by auth service)
    return await cluster_manager_service.get_project(project_name)


@router.get("/test")
async def some_route(project_name: str, permitted: bool = Depends(
    lambda user_id=Depends(get_current_user_id): check_permissions(user_id=user_id, action="delete",
                                                                   project_name="project_name"))
                     ):
    return {"project_name": project_name, "permitted": permitted}
