from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import (
    Configuration,
    DependenciesContainer,
    Factory,
    Provider,
)

from babyhelm.containers.gateways import GatewaysContainer
from babyhelm.repositories.application import ApplicationRepository
from babyhelm.repositories.project import ProjectRepository
from babyhelm.repositories.user import UserRepository


class RepositoriesContainer(DeclarativeContainer):
    """Repositories container."""

    config: Configuration = Configuration()
    gateways: GatewaysContainer = DependenciesContainer()

    user: Provider[UserRepository] = Factory[UserRepository](
        UserRepository, db=gateways.db
    )
    project: Provider[ProjectRepository] = Factory[ProjectRepository](
        ProjectRepository, db=gateways.db
    )
    application: Provider[ApplicationRepository] = Factory[ApplicationRepository](
        ApplicationRepository, db=gateways.db
    )
