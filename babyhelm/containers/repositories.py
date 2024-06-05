"""."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import (
    Configuration,
    DependenciesContainer,
)

from babyhelm.containers.gateways import GatewaysContainer


class RepositoriesContainer(DeclarativeContainer):
    """Repositories container."""

    config: Configuration = Configuration()
    gateways: GatewaysContainer = DependenciesContainer()
