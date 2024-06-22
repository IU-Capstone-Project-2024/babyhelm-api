import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from babyhelm.gateways.database import Database
from babyhelm.models.application import Application
from babyhelm.models.associations import UserProjectAssociation
from babyhelm.models.project import Project
from babyhelm.models.user import User


class ApplicationRepository:
    """Application repository."""

    db: Database

    def __init__(self, db: Database):
        self.db = db

    async def create(
        self, name: str, namespace: str, image: str, session: AsyncSession | None = None
    ):
        return 1

    async def delete(
        self, name: str, namespace: str, session: AsyncSession | None = None
    ):
        return 1
