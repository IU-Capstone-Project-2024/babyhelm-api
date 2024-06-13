from babyhelm.repositories.user import UserRepository
from babyhelm.schemas.user import TokenSchema


class UserService:
    user_repository: UserRepository

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def create(self, email: str, raw_password: str):
        await self.user_repository.create(email, raw_password)
    
    async def authenticate(self, username: str, password: str) -> TokenSchema:
        return await self.user_repository.authenticate(username=username, password=password)