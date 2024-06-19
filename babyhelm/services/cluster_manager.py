from kubernetes import client, config
from kubernetes.client.exceptions import ApiException
from sqlalchemy.exc import SQLAlchemyError

from babyhelm.exceptions.cluster_manager import ClusterManagerError
from babyhelm.repositories.project import ProjectRepository
from babyhelm.schemas.namespace import Metadata


class ClusterManagerService:
    def __init__(self, project_repository: ProjectRepository, kubeconfig_path):
        self.project_repository = project_repository

        config.load_kube_config(config_file=kubeconfig_path)

        self.core_v1_api = client.CoreV1Api()
        self.apps_v1_api = client.AppsV1Api()

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
        except SQLAlchemyError:
            raise ClusterManagerError("SQLAlchemy API error, unable to add value to DB")
        else:
            try:
                self.core_v1_api.create_namespace(body=namespace)
            except ApiException:
                await self.project_repository.delete(namespace_data.name)
                raise ClusterManagerError(
                    "Kubernetes API error, unable to add value to cluster"
                )
