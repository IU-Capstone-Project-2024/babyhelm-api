"""."""
import contextlib
import typing

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine, async_sessionmaker


class Database(object):
    """Database."""

    _engine: AsyncEngine
    _factory: async_sessionmaker

    def __init__(
            self,
            url: str,
            echo: bool = False,
            pool_size: int = 5,
            max_overflow: int = 10,
            expire_on_commit: bool = False,
    ):
        """."""
        self._engine = create_async_engine(
            url,
            echo=echo,
            pool_size=pool_size,
            max_overflow=max_overflow,
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
