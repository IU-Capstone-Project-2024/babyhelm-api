from babyhelm.models.user import User
from babyhelm.repositories.user import UserRepository
from babyhelm.schemas.user import TokenSchema
from babyhelm.schemas.user import CreateUser, UserSchema
from datetime import timedelta
from fastapi import HTTPException, status
from dependency_injector.wiring import inject, Provide
from babyhelm.services.auth import AuthService
from babyhelm.containers.application import ApplicationContainer

class UserService:
    @inject
    def __init__(self, user_repository: UserRepository, auth_service: AuthService = Provide[ApplicationContainer.services.auth]):
        self.user_repository = user_repository
        self.auth_service = auth_service

    async def create(self, email: str, username: str, raw_password: str):
        hashed_password = self.auth_service.hash_password(raw_password)
        await self.user_repository.create(email=email, hashed_password=hashed_password, username=username)

    async def authenticate(self, username: str, password: str) -> TokenSchema:
        user = await self.user_repository.get(User.username == username)
        if not user or not self.auth_service.verify_password(password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

        access_token = self.auth_service.create_access_token(data={"sub": user.username})
        refresh_token = self.auth_service.create_refresh_token(data={"sub": user.username})

        return TokenSchema(access_token=access_token, refresh_token=refresh_token, token_type="Bearer")
