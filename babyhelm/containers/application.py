"""redirector.containers.application."""
from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Configuration

from babyhelm.containers.gateways import GatewaysContainer
from babyhelm.containers.repositories import RepositoriesContainer
from babyhelm.containers.services import ServicesContainer


class ApplicationContainer(DeclarativeContainer):
    """Application container. Will be used in all dependency injections."""

    wiring_config: WiringConfiguration = WiringConfiguration(
        modules=[

        ],
    )
    config: Configuration = Configuration()

    gateways: GatewaysContainer = None
    repositories: RepositoriesContainer = None
    services: ServicesContainer = None
