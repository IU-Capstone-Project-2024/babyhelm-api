from babyhelm.repositories.user import UserRepository


class UserService:
    user_repository: UserRepository

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def create(self, email: str, raw_password: str):
        await self.user_repository.create(email, raw_password)
