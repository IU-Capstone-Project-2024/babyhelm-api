from typing import Tuple

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from babyhelm.gateways.database import Database
from babyhelm.models import User
from babyhelm.models.project import Project


class ProjectRepository:
    """Project repository."""

    db: Database

    def __init__(self, db: Database):
        self.db = db

    async def create(self, name: str, user: User, session: AsyncSession | None = None):
        project = Project(name=name)
        project.users.append(user)
        async with self.db.session(session) as session:
            session.add(project)
            await session.commit()

    async def delete(self, project: Project, session: AsyncSession | None = None):
        async with self.db.session(session) as session_:
            session_: AsyncSession
            await session_.delete(project)
            await session_.commit()

    async def list(
        self, user_id: int, session: AsyncSession | None = None
    ) -> list[Project]:
        async with self.db.session(session) as session_:
            session_: AsyncSession
            subquery = (
                sa.select(Project.name)
                .join(Project.users)
                .filter(User.id == user_id)
                .subquery()
            )

            stmt = (
                sa.select(Project)
                .where(Project.name.in_(subquery))
                .options(
                    selectinload(Project.users), selectinload(Project.applications)
                )
            )

            return (await session_.scalars(stmt)).all()  # noqa

    async def get(
        self, name: str, options: Tuple = (), session: AsyncSession | None = None
    ) -> Project:
        async with self.db.session(session) as session_:
            stmt = sa.select(Project).options(*options).where(Project.name == name)
            return await session_.scalar(stmt)
