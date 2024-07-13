from typing import Tuple

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from babyhelm.gateways.database import Database
from babyhelm.models import User
from babyhelm.models import users_projects as UsersProjects  # noqa N812
from babyhelm.models.project import Project
from babyhelm.services.auth.utils import RoleEnum


class ProjectRepository:
    """Project repository."""

    db: Database

    def __init__(self, db: Database):
        self.db = db

    async def create(
        self, name: str, user: User, session: AsyncSession | None = None
    ) -> None:
        project = Project(name=name)
        async with self.db.session(session) as session:
            stmt = UsersProjects.insert().values(
                project_name=project.name, user_id=user.id, role=RoleEnum.creator
            )
            session.add(project)
            await session.commit()

            await session.execute(stmt)
            await session.commit()

    async def delete(
        self, project: Project, session: AsyncSession | None = None
    ) -> None:
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
        self, *args, options: Tuple = (), session: AsyncSession | None = None
    ) -> Project:
        async with self.db.session(session) as session_:
            stmt = sa.select(Project).options(*options).where(*args)
            return await session_.scalar(stmt)

    async def get_user_role(
        self, project_name: str, user_id: int, session: AsyncSession | None = None
    ) -> str | None:
        async with self.db.session(session) as session_:
            stmt = sa.select(UsersProjects).where(
                (UsersProjects.c.project_name == project_name)
                & (UsersProjects.c.user_id == user_id)
            )
            execute_result = await session_.execute(stmt)
            user_project = execute_result.fetchone()

            if user_project:
                return user_project.role.name

    async def add_new_user(
        self,
        project_name: str,
        user_id: int,
        role: str,
        session: AsyncSession | None = None,
    ) -> None:
        async with self.db.session(session) as session_:
            stmt = insert(UsersProjects).values(
                project_name=project_name, user_id=user_id, role=role
            )
            stmt = stmt.on_conflict_do_update(
                index_elements=[UsersProjects.c.user_id, UsersProjects.c.project_name],
                set_={
                    UsersProjects.c.user_id: stmt.excluded.user_id,
                    UsersProjects.c.project_name: stmt.excluded.project_name,
                    UsersProjects.c.role: stmt.excluded.role,
                },
            )
            await session_.execute(stmt)
            await session_.commit()
