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

    async def create(self, name: str, session: AsyncSession | None = None):
        project = Project(name=name)
        # TODO add author
        async with self.db.session(session) as session:
            session.add(project)
            await session.commit()


    # TODO add users to project
