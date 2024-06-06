"""redirector.containers.application."""
from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Configuration, Container

from babyhelm.containers.gateways import GatewaysContainer
from babyhelm.containers.repositories import RepositoriesContainer
from babyhelm.containers.services import ServicesContainer


class ApplicationContainer(DeclarativeContainer):
    """Application container. Will be used in all dependency injections."""

    wiring_config: WiringConfiguration = WiringConfiguration(
        modules=[
            "babyhelm.routers.test",
        ],
    )

    config: Configuration = Configuration()

    gateways: GatewaysContainer = Container[GatewaysContainer](
        GatewaysContainer, config=config
    )
    repositories: RepositoriesContainer = Container[RepositoriesContainer](
        RepositoriesContainer,
        config=config,
        gateways=gateways,
    )
    services: ServicesContainer = Container[ServicesContainer](
        ServicesContainer,
        config=config,
        gateways=gateways,
        repositories=repositories,
    )
