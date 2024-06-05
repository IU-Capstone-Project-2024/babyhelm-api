"""."""
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Configuration


class GatewaysContainer(DeclarativeContainer):
    """Gateways container."""

    config: Configuration = Configuration()
