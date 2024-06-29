from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Configuration, Container

from babyhelm.containers.gateways import GatewaysContainer
from babyhelm.containers.repositories import RepositoriesContainer
from babyhelm.containers.services import ServicesContainer


class ApplicationContainer(DeclarativeContainer):
    """
    Application container. Will be used in all dependency injections.

    You must register all routes in wiring_config.
    """

    wiring_config: WiringConfiguration = WiringConfiguration(
        modules=[
            "babyhelm.routers.manifest_builder",
            "babyhelm.routers.user",
            "babyhelm.routers.cluster_manager.applications",
            "babyhelm.routers.cluster_manager.projects",
            "babyhelm.services.auth.dependencies",
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
