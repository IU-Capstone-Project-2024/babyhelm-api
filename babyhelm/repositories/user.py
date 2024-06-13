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
    
    async def authenticate(self, username: str, password: str) -> TokenSchema:
        user = await self.get(User.username == username)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

        access_token = create_access_token(data={"sub": user.username}, expires_delta=timedelta(minutes=30))
        refresh_token = create_refresh_token(data={"sub": user.username}, expires_delta=timedelta(days=30))

        return TokenSchema(access_token=access_token, refresh_token=refresh_token, token_type="Bearer")
