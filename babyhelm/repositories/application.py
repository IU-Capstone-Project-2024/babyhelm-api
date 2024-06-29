import logging

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from babyhelm.gateways.database import Database
from babyhelm.models.application import Application


class ApplicationRepository:
    """Application repository."""

    db: Database

    def __init__(self, db: Database):
        self.db = db

    async def create(
        self,
        name: str,
        project_name: str,
        image: str,
        service_name: str,
        deployment_name: str,
        autoscaler_name: str,
        session: AsyncSession | None = None,
    ):
        async with self.db.session(session) as session_:
            application = Application(
                name=name,
                image=image,
                project_name=project_name,
                service_name=service_name,
                deployment_name=deployment_name,
                autoscaler_name=autoscaler_name,
            )

            session_.add(application)
            await session_.commit()

    async def delete(
        self, application: Application, session: AsyncSession | None = None
    ):
        async with self.db.session(session) as session_:
            session_: AsyncSession
            await session_.delete(application)
            await session_.commit()

    async def get(self, project_name: str, application_name: str) -> Application:
        async with self.db.session() as session_:
            session_: AsyncSession
            statement = (
                sa.select(Application)
                .where(Application.name == application_name)
                .where(Application.project_name == project_name)
            )
            return await session_.scalar(statement)

    async def list(self, project_name: str) -> list[Application]:
        async with self.db.session() as session_:
            session_: AsyncSession
            stmt = sa.select(Application).where(
                Application.project_name == project_name
            )
            return (await session_.scalars(stmt)).all()  # noqa
