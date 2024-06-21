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
from babyhelm.services.auth import AuthService


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
    auth: Provider[AuthService] = Factory[AuthService](
        AuthService,
        secret_key=config.auth.secret_key,
        algorithm="HS256"
    )
    user: Provider[UserService] = Factory[UserService](
        UserService,
        user_repository=repositories.user,
        auth_service=auth,
    )
    cluster_manager: Provider[ClusterManagerService] = Factory[ClusterManagerService](
        ClusterManagerService,
        project_repository=repositories.project,
        kubeconfig_path=config.kubeconfig.path,
    )
