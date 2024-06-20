from datetime import timedelta
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa

from babyhelm.exceptions.http import BadRequestError
from babyhelm.gateways.database import Database

from babyhelm.models import User
from babyhelm.schemas.user import TokenSchema
from babyhelm.services.auth import create_access_token, create_refresh_token, verify_password


class UserRepository:
    """User repository."""

    db: Database

    def __init__(self, db: Database):
        self.db = db

    async def create(self, email: str, hashed_password: str, session: AsyncSession | None = None):
        user = User(email=email, password=hashed_password)
        try:
            async with self.db.session(session) as session_:
                session_.add(user)
                await session_.commit()
        except IntegrityError:
            raise BadRequestError("User already exists.")

    async def get(self, *args, session: AsyncSession | None = None) -> User | None:
        """Get user."""
        async with self.db.session(session) as session_:
            statement = sa.select(User).where(*args)
            execute_result = await session_.execute(statement)
            return execute_result.scalar_one_or_none()
