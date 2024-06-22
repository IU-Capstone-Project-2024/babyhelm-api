"""."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import (
    Configuration,
    DependenciesContainer,
    Factory,
    Provider,
)

from babyhelm.containers.gateways import GatewaysContainer
from babyhelm.containers.repositories import RepositoriesContainer
from babyhelm.services.cluster_manager import ClusterManagerService
from babyhelm.services.manifest_builder import ManifestBuilderService
from babyhelm.services.user import UserService


class ServicesContainer(DeclarativeContainer):
    """Services container."""

    config: Configuration = Configuration()
    gateways: GatewaysContainer = DependenciesContainer()
    repositories: RepositoriesContainer = DependenciesContainer()
    manifest_builder: Provider[ManifestBuilderService] = Factory[
        ManifestBuilderService
    ](
        ManifestBuilderService,
        templates_directory=config.templates.path,
    )
    user: Provider[UserService] = Factory[UserService](
        UserService,
        user_repository=repositories.user,
    )
    cluster_manager: Provider[ClusterManagerService] = Factory[ClusterManagerService](
        ClusterManagerService,
        project_repository=repositories.project,
        application_repository=repositories.application,
        manifest_builder=manifest_builder,
        kubeconfig_path=config.kubeconfig.path,
    )
