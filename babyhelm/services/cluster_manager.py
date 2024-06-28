import logging

import yaml
from kubernetes import config, utils
from sqlalchemy.exc import SQLAlchemyError

from babyhelm.exceptions.cluster_manager import ClusterError, DatabaseError
from babyhelm.repositories.application import ApplicationRepository
from babyhelm.repositories.project import ProjectRepository
from babyhelm.schemas.cluster_manager import CreateApplicationRequest, CreateApplicationResponse, CreateProjectResponse
from babyhelm.schemas.manifest_builder import Project
from babyhelm.services.manifest_builder import ManifestBuilderService


class ClusterManagerService:
    def __init__(
            self,
            project_repository: ProjectRepository,
            application_repository: ApplicationRepository,
            manifest_builder: ManifestBuilderService,
            kubeconfig_path: str,
            host_postfix: str
    ):
        self.host_postfix = host_postfix
        self.project_repository = project_repository
        self.application_repository = application_repository
        self.manifest_builder = manifest_builder

        self.k8s_client = config.new_client_from_config_dict(
            yaml.safe_load(open(kubeconfig_path, "r"))
        )

    def _create_app_link(self, project_name: str, app_name: str) -> str:
        return f"{project_name}-{app_name}-{self.host_postfix}"

    async def create_project(self, project: Project) -> CreateProjectResponse:
        """
        Project - term for user
        Namespace - inner term from k8s
        """
        manifest = self.manifest_builder.render_namespace(project=project)
        try:
            await self.project_repository.create(name=project.name)
            utils.create_from_dict(self.k8s_client, data=manifest.namespace)
            # TODO add monitoring links provision
            return CreateProjectResponse()
        except SQLAlchemyError as e:
            raise DatabaseError(project.name) from e
        except utils.FailToCreateError as e:
            await self.project_repository.delete(name=project.name)
            raise ClusterError(project.name) from e

    async def create_application(self, app: CreateApplicationRequest) -> CreateApplicationResponse:
        application = app.application
        manifests = self.manifest_builder.render_application(application=application)
        project_name = app.project.name
        try:
            await self.application_repository.create(
                name=application.name,
                project_name=project_name,
                image=application.image,
                service_name=manifests.service["metadata"]["name"],
                deployment_name=manifests.deployment["metadata"]["name"],
                autoscaler_name=manifests.hpa["metadata"]["name"],
            )
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
            return CreateApplicationResponse(app_link=app_link)
        except SQLAlchemyError as e:
            logging.error(e)
            raise DatabaseError(application.name) from e
        except utils.FailToCreateError as e:
            logging.error(e)
            await self.application_repository.delete(
                name=application.name, project_name=project_name
            )
            raise ClusterError(app.application.name) from e
