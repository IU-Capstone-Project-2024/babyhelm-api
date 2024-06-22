from kubernetes import client, config, utils
from kubernetes.client.exceptions import ApiException
from sqlalchemy.exc import SQLAlchemyError

from babyhelm.exceptions.cluster_manager import ClusterManagerError
from babyhelm.repositories.application import ApplicationRepository
from babyhelm.repositories.project import ProjectRepository
from babyhelm.schemas.manifest_builder import Application
from babyhelm.schemas.namespace import Metadata
from babyhelm.services.manifest_builder import ManifestBuilderService


class ClusterManagerService:
    def __init__(
        self,
        project_repository: ProjectRepository,
        application_repository: ApplicationRepository,
        manifest_builder: ManifestBuilderService,
        kubeconfig_path,
    ):
        self.project_repository = project_repository
        self.manifest_builder = manifest_builder
        self.application_repository = application_repository

        config.load_kube_config(config_file=kubeconfig_path)

        configuration = client.configuration.Configuration()
        self.k8s_client = client.api_client.ApiClient(configuration)

    async def create_namespace(self, namespace_data: Metadata):
        namespace = client.V1Namespace(
            metadata=client.V1ObjectMeta(
                name=namespace_data.name,
                annotations=namespace_data.annotations,
                labels=namespace_data.labels,
            )
        )
        try:
            await self.project_repository.create(namespace_data.name)
            # self.core_v1_api.create_namespace(body=namespace) # TODO make addition via generated manifest
        except SQLAlchemyError:
            raise ClusterManagerError("SQLAlchemy API error, unable to add value to DB")
        except ApiException:
            await self.project_repository.delete(namespace_data.name)
            raise ClusterManagerError(
                "Kubernetes API error, unable to add value to cluster"
            )

    async def create_application(self, app: Application):
        manifests = self.manifest_builder.render_application(application=app)
        namespace = app.namespace
        try:
            await self.application_repository.create(
                name=app.name, namespace=namespace, image=app.image
            )
            utils.create_from_yaml(
                self.k8s_client, yaml_objects=manifests, namespace=namespace
            )
        except SQLAlchemyError:
            raise ClusterManagerError("SQLAlchemy API error, unable to add value to DB")
        except utils.FailToCreateError:
            await self.application_repository.delete(name=app.name, namespace=namespace)
            raise ClusterManagerError(
                "Kubernetes API error, unable to add value to cluster"
            )
