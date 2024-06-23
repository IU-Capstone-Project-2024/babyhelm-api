from babyhelm.exceptions.auth import UserNotFoundError
from babyhelm.models import User
from babyhelm.repositories.user import UserRepository
from babyhelm.schemas.user import ViewUserScheme
from babyhelm.services.auth.service import AuthService


class UserService:
    def __init__(self, user_repository: UserRepository, auth_service: AuthService):
        self.user_repository = user_repository
        self.auth_service = auth_service

    async def create(self, email: str, raw_password: str):
        hashed_password = self.auth_service.hash_password(raw_password)
        await self.user_repository.create(email=email, raw_password=hashed_password)

    async def get(self, user_id: int) -> ViewUserScheme:
        return await self.user_repository.get(User.id == user_id)
