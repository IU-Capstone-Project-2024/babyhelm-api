import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from babyhelm.gateways.database import Database


class UserRepository:
    """User repository."""

    db: Database

    def __init__(self, db: Database):
        """."""
        self.db = db

    async def get(self, *args, session: AsyncSession | None = None) -> int:
        """Get user."""
        # async with self.db.session(session) as session_:
        #     statement = sa.select(User).where(*args)
        #     execute_result = await session_.execute(statement)
        #     return execute_result.scalar_one_or_none()
        return 1
