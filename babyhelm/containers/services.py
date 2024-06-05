"""."""
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import (
    Configuration,
    DependenciesContainer,
)

from babyhelm.containers.gateways import GatewaysContainer
from babyhelm.containers.repositories import RepositoriesContainer


class ServicesContainer(DeclarativeContainer):
    """Services container."""

    config: Configuration = Configuration()
    gateways: GatewaysContainer = DependenciesContainer()
    repositories: RepositoriesContainer = DependenciesContainer()
