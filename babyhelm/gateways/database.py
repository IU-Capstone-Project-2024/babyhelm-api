"""."""

import contextlib
import typing

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


class Database(object):
    """Database."""

    _engine: AsyncEngine
    _factory: async_sessionmaker

    def __init__(
        self,
        url: str,
        echo: bool = False,
        expire_on_commit: bool = False,
    ):
        """."""
        self._engine = create_async_engine(
            url,
            echo=echo,
        )
        self._factory = async_sessionmaker(
            bind=self._engine,
            expire_on_commit=expire_on_commit,
        )

    @contextlib.asynccontextmanager
    async def session(
        self, session: AsyncSession | None = None
    ) -> typing.AsyncGenerator[AsyncSession, None]:
        """Session factory."""
        if session:
            yield session
        else:
            session: AsyncSession = self._factory()
            try:
                yield session
            finally:
                await session.close()
