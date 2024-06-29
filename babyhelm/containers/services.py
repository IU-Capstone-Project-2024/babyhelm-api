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
from babyhelm.services.auth.service import AuthService
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
    auth: Provider[AuthService] = Factory[AuthService](
        AuthService,
        secret_key=config.auth.secret_key,
        algorithm="HS256",
        access_token_expiration=config.auth.access_token_expire_minutes,
        refresh_token_expiration=config.auth.refresh_token_expire_days,
        user_service=user,
    )
    cluster_manager: Provider[ClusterManagerService] = Factory[ClusterManagerService](
        ClusterManagerService,
        project_repository=repositories.project,
        application_repository=repositories.application,
        manifest_builder=manifest_builder,
        kubeconfig_path=config.kubeconfig.path,
        host_postfix=config.host_postfix,
    )
