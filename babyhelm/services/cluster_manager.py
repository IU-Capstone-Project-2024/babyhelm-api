import datetime

import yaml
from kubernetes import client, config, utils
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import selectinload

from babyhelm.exceptions.auth import UserNotFoundError
from babyhelm.exceptions.cluster_manager import (
    ApplicationNameAlreadyTaken,
    ApplicationNotFound,
    ApplicationsAreNotEmpty,
    ClusterError,
    DatabaseError,
    ForbiddenProjectName,
    ProjectNameAlreadyTaken,
    ProjectNotFound,
)
from babyhelm.models.project import Project as ProjectModel
from babyhelm.models.user import User as UserModel
from babyhelm.repositories.application import ApplicationRepository
from babyhelm.repositories.project import ProjectRepository
from babyhelm.repositories.user import UserRepository
from babyhelm.schemas.cluster_manager import (
    ApplicationSchema,
    ApplicationWithLinkSchema,
    CreateApplicationRequest,
    ProjectSchema,
)
from babyhelm.schemas.manifest_builder import Project
from babyhelm.services.manifest_builder import ManifestBuilderService


class ClusterManagerService:
    FORBIDDEN_NAMES = ["default", "kube-system", "kube-public", "kube-node-lease"]

    def __init__(
        self,
        project_repository: ProjectRepository,
        application_repository: ApplicationRepository,
        user_repository: UserRepository,
        manifest_builder: ManifestBuilderService,
        kubeconfig_path: str,
        host_postfix: str,
    ):
        self.host_postfix = host_postfix
        self.project_repository = project_repository
        self.application_repository = application_repository
        self.manifest_builder = manifest_builder
        self.user_repository = user_repository

        self.k8s_client = config.new_client_from_config_dict(
            yaml.safe_load(open(kubeconfig_path, "r"))
        )

    def _create_app_link(self, project_name: str, app_name: str) -> str:
        return f"{project_name}-{app_name}-{self.host_postfix}"

    async def create_project(self, project: Project, user_id: int) -> ProjectSchema:
        """
        Project - term for user
        Namespace - inner term from k8s
        """
        if project.name in self.FORBIDDEN_NAMES:
            raise ForbiddenProjectName(project.name)
        manifest = self.manifest_builder.render_namespace(project=project)
        user = await self.user_repository.get(UserModel.id == user_id)
        if user is None:
            raise UserNotFoundError
        try:
            try:
                await self.project_repository.create(name=project.name, user=user)
            except IntegrityError:
                raise ProjectNameAlreadyTaken(project.name)
            utils.create_from_dict(self.k8s_client, data=manifest.namespace)
            # TODO add monitoring links provision
            return await self.get_project(project_name=project.name)
        except SQLAlchemyError as e:
            raise DatabaseError(project.name) from e
        except utils.FailToCreateError as e:
            project = await self.project_repository.get(name=project.name)
            await self.project_repository.delete(project)
            raise ClusterError(project.name) from e

    async def create_application(
        self, app: CreateApplicationRequest, project_name: str
    ) -> ApplicationWithLinkSchema:
        application = app.application
        manifests = self.manifest_builder.render_application(application=application)
        try:
            try:
                await self.application_repository.create(
                    name=application.name,
                    project_name=project_name,
                    image=application.image,
                    service_name=manifests.service["metadata"]["name"],
                    deployment_name=manifests.deployment["metadata"]["name"],
                    autoscaler_name=manifests.hpa["metadata"]["name"],
                )
            except IntegrityError:
                raise ApplicationNameAlreadyTaken(application.name)

            utils.create_from_dict(
                self.k8s_client, manifests.deployment, namespace=project_name
            )
            utils.create_from_dict(
                self.k8s_client, manifests.service, namespace=project_name
            )
            utils.create_from_dict(
                self.k8s_client, manifests.hpa, namespace=project_name
            )
            app_link = self._create_app_link(project_name, application.name)
            # TODO add monitoring links provision
            app_schema = await self.get_application(project_name, application.name)
            return ApplicationWithLinkSchema(
                **app_schema.model_dump(), deployment_link=app_link
            )
        except SQLAlchemyError as e:
            raise DatabaseError(application.name) from e
        except utils.FailToCreateError as e:
            app_model = await self.application_repository.get(
                project_name, application.name
            )
            await self.application_repository.delete(application=app_model)
            raise ClusterError(app.application.name) from e

    async def list_projects(self, user_id: int):
        projects = await self.project_repository.list(user_id)
        return [ProjectSchema.from_orm(project) for project in projects]

    async def delete_project(self, project_name: str):
        if project_name in self.FORBIDDEN_NAMES:
            raise ForbiddenProjectName(project_name)
        project = await self.project_repository.get(
            name=project_name, options=(selectinload(ProjectModel.applications),)
        )
        if project is None:
            raise ProjectNotFound
        if project.applications:
            raise ApplicationsAreNotEmpty(project_name)
        v1 = client.CoreV1Api(self.k8s_client)
        v1.delete_namespace(name=project_name)
        await self.project_repository.delete(project)

    async def get_project(self, project_name: str) -> ProjectSchema:
        project_model = await self.project_repository.get(
            name=project_name,
            options=(
                selectinload(ProjectModel.users),
                selectinload(ProjectModel.applications),
            ),
        )
        if project_model is None:
            raise ProjectNotFound
        return ProjectSchema.from_orm(project_model)

    async def delete_application(self, project_name: str, application_name: str):
        application = await self.application_repository.get(
            project_name, application_name
        )
        if application is None:
            raise ApplicationNotFound

        v1 = client.AppsV1Api(self.k8s_client)
        v1_core = client.CoreV1Api(self.k8s_client)
        autoscaling_v1 = client.AutoscalingV1Api(self.k8s_client)

        v1.delete_namespaced_deployment(
            namespace=application.project_name, name=application.deployment_name
        )
        v1_core.delete_namespaced_service(
            namespace=application.project_name, name=application.service_name
        )
        autoscaling_v1.delete_namespaced_horizontal_pod_autoscaler(
            namespace=application.project_name, name=application.autoscaler_name
        )

        await self.application_repository.delete(application=application)

    async def get_application(
        self, project_name: str, application_name: str
    ) -> ApplicationSchema:
        application = await self.application_repository.get(
            project_name, application_name
        )
        if application is None:
            raise ApplicationNotFound
        return ApplicationSchema.from_orm(application)

    async def list_applications(self, project_name: str) -> list[ApplicationSchema]:
        project = await self.project_repository.get(name=project_name)
        if project is None:
            raise ProjectNotFound
        applications = await self.application_repository.list(project_name=project_name)
        return [ApplicationSchema.from_orm(app) for app in applications]

    async def restart_application(self, project_name: str, application_name: str):
        application = await self.application_repository.get(
            project_name, application_name
        )
        if application is None:
            raise ApplicationNotFound
        now = datetime.datetime.utcnow()
        v1 = client.AppsV1Api(self.k8s_client)
        v1.patch_namespaced_deployment(
            namespace=application.project_name,
            name=application.deployment_name,
            body={
                "spec": {
                    "template": {
                        "metadata": {
                            "annotations": {
                                "kubectl.kubernetes.io/restartedAt": str(
                                    now.isoformat("T") + "Z"
                                )
                            }
                        }
                    }
                }
            },
        )
