from babyhelm.models.user import User
from babyhelm.repositories.user import UserRepository
from babyhelm.schemas.user import TokenSchema
from babyhelm.schemas.user import CreateUser, UserSchema
from fastapi import HTTPException, status
from dependency_injector.wiring import inject, Provide
from babyhelm.services.auth import AuthService
from babyhelm.exceptions.http import UnauthorizedError

class UserService:
    @inject
    def __init__(self, user_repository: UserRepository, auth_service: AuthService):
        self.user_repository = user_repository
        self.auth_service = auth_service

    async def create(self, email: str, raw_password: str):
        hashed_password = self.auth_service.hash_password(raw_password)
        await self.user_repository.create(email=email, raw_password=hashed_password)

    async def authenticate(self, email: str, password: str) -> TokenSchema:
        user = await self.user_repository.get(User.email == email)
        if not user or not self.auth_service.verify_password(password, user.password):
            raise UnauthorizedError()

        access_token = self.auth_service.create_access_token(data={"sub": user.email})
        refresh_token = self.auth_service.create_refresh_token(data={"sub": user.email})

        return TokenSchema(access_token=access_token, refresh_token=refresh_token, token_type="Bearer")
