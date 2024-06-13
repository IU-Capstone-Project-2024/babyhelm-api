from sqlalchemy.ext.asyncio import AsyncSession

from babyhelm.gateways.database import Database
import sqlalchemy as sa

from babyhelm.models.project import Project
from babyhelm.models.user import User
from babyhelm.models.associations import UserProjectAssociation


class ProjectRepository:
    """Project repository."""

    db: Database

    def __init__(self, db: Database):
        self.db = db

    async def create(self, name: str, user_ids: list[int] | None = None, session: AsyncSession | None = None):
        association = UserProjectAssociation()
        association.project = Project(name=name)

        async with self.db.session(session) as session_:
            statement = sa.select(User).where(User.id.in_(user_ids))
            result = await session_.execute(statement)
            for user in result.scalars():
                user.projects.append(association)
            await session_.commit()

    async def get(self, *args, session: AsyncSession | None = None) -> int:
        """Get project."""
        # async with self.db.session(session) as session_:
        #     statement = sa.select(Project).where(*args)
        #     execute_result = await session_.execute(statement)
        #     return execute_result.scalar_one_or_none()
        return 1
