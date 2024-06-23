"""."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Configuration, Singleton

from babyhelm.gateways.database import Database


class GatewaysContainer(DeclarativeContainer):
    """Gateways container."""

    config: Configuration = Configuration()
    db: Singleton[Database] = Singleton[Database](
        Database,
        config.database.url,
        echo=config.database.echo,
        pool_size=5,
        max_overflow=15,
        expire_on_commit=config.database.expire_on_commit,
    )
