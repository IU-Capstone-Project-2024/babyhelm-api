from babyhelm.models import User
from babyhelm.repositories.user import UserRepository
from babyhelm.schemas.user import ResponseUserSchema
from babyhelm.services.auth.service import AuthService


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def create(self, email: str, raw_password: str) -> None:
        hashed_password: str = AuthService.hash_password(raw_password)
        await self.user_repository.create(email=email, password=hashed_password)

    async def get(self, *args) -> ResponseUserSchema | None:
        user: User = await self.user_repository.get(*args)
        if user:
            return ResponseUserSchema.model_validate(user)
