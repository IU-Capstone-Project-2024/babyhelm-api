import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from babyhelm.exceptions.http import BadRequestError
from babyhelm.gateways.database import Database
from babyhelm.models import User
from babyhelm.services.auth import AuthService

class UserRepository:
    """User repository."""

    def __init__(self, db: Database, config):
        self.db = db
        self.config = config

    async def create(self, email: str, raw_password: str, session: AsyncSession | None = None):
        user = User(email=email, password=raw_password)
        try:
            async with self.db.session(session) as session_:
                session_.add(user)
                await session_.commit()
        except IntegrityError:
            raise BadRequestError("User already exists.")

    async def get(self, *args, session: AsyncSession | None = None) -> User:
        async with self.db.session(session) as session_:
            statement = sa.select(User).where(*args)
            execute_result = await session_.execute(statement)
            return execute_result.scalar_one_or_none()
