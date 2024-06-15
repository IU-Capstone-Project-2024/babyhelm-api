from kubernetes import client, config

from babyhelm.schemas.namespace import Metadata

from babyhelm.repositories.project import ProjectRepository


class ClusterManagerService:
    def __init__(self, project_repository: ProjectRepository, kubeconfig_path=None):
        self.project_repository = project_repository

        if kubeconfig_path:
            config.load_kube_config(config_file=kubeconfig_path)
        else:
            config.load_kube_config()

        self.core_v1_api = client.CoreV1Api()
        self.apps_v1_api = client.AppsV1Api()

    async def create_namespace(self, namespace_data: Metadata):
        namespace = client.V1Namespace(
            metadata=client.V1ObjectMeta(name=namespace_data.name,
                                         annotations=namespace_data.annotations,
                                         labels=namespace_data.labels)
        )
        try:
            api_response = self.core_v1_api.create_namespace(body=namespace)
            await self.project_repository.create(namespace_data.name)
            return api_response
        except client.exceptions.ApiException as e:
            return None
