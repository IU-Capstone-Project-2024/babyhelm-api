"""."""
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import (
    Configuration,
    DependenciesContainer, Factory, Provider,
)

from babyhelm.containers.gateways import GatewaysContainer
from babyhelm.containers.repositories import RepositoriesContainer
from babyhelm.services.manifest_builder import ManifestBuilderService


class ServicesContainer(DeclarativeContainer):
    """Services container."""

    config: Configuration = Configuration()
    gateways: GatewaysContainer = DependenciesContainer()
    repositories: RepositoriesContainer = DependenciesContainer()
    manifest_builder: Provider[ManifestBuilderService] = Factory[ManifestBuilderService](
            ManifestBuilderService,
            templates_directory="babyhelm/templates", # TODO populate yaml file and take value from it
    )
