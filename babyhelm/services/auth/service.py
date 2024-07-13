from datetime import datetime, timedelta
from typing import TYPE_CHECKING

import bcrypt
import jwt

from babyhelm.exceptions.auth import (
    InvalidCredentialsError,
    InvalidPermissions,
    InvalidTokenError,
    TokenExpiredError,
)
from babyhelm.exceptions.cluster_manager import ProjectNotFound
from babyhelm.models import User
from babyhelm.repositories.project import ProjectRepository
from babyhelm.schemas.auth import TokenEnum, TokenSchema
from babyhelm.schemas.user import ResponseUserSchema
from babyhelm.services.auth.utils import role_permission_dict

if TYPE_CHECKING:
    from babyhelm.services.user import UserService


class AuthService:
    def __init__(
        self,
        secret_key: str,
        access_token_expiration: int,
        refresh_token_expiration: int,
        user_service: "UserService",
        project_repository: ProjectRepository,
        algorithm: str = "HS256",
    ):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expiration = access_token_expiration
        self.refresh_token_expiration = refresh_token_expiration

        self.user_service = user_service
        self.project_repository = project_repository

    @staticmethod
    def hash_password(password: str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode(), salt)
        return hashed.decode()

    @staticmethod
    def _verify_password(password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode(), hashed_password.encode())

    def _create_token(self, data: dict, token_type: TokenEnum) -> str:
        if token_type == TokenEnum.ACCESS:
            expire = datetime.utcnow() + timedelta(minutes=self.access_token_expiration)
        elif token_type == TokenEnum.REFRESH:
            expire = datetime.utcnow() + timedelta(days=self.refresh_token_expiration)
        data.update({"exp": expire})
        encoded_jwt = jwt.encode(data, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def decode_jwt(self, token: str) -> dict:
        try:
            decoded_token: dict = jwt.decode(
                token, self.secret_key, algorithms=[self.algorithm]
            )
            return decoded_token
        except jwt.ExpiredSignatureError:
            raise TokenExpiredError()
        except jwt.InvalidTokenError:
            raise InvalidTokenError()

    async def authenticate_user(self, email: str, password: str) -> TokenSchema:
        user: ResponseUserSchema = await self.user_service.get(User.email == email)
        if not user or not self._verify_password(password, user.hashed_password):
            raise InvalidCredentialsError()

        access_token = self._create_token(
            data={"sub": user.id}, token_type=TokenEnum.ACCESS
        )
        refresh_token = self._create_token(
            data={"sub": user.id}, token_type=TokenEnum.REFRESH
        )

        return TokenSchema(
            access_token=access_token, refresh_token=refresh_token, token_type="Bearer"
        )

    async def refresh_access_token(self, refresh_token: str) -> TokenSchema:
        try:
            decoded_token = self.decode_jwt(refresh_token)
            user_id = decoded_token.get("sub")
            if not user_id:
                raise InvalidTokenError("Invalid token")

            user: ResponseUserSchema = await self.user_service.get(User.id == user_id)
            if not user:
                raise InvalidCredentialsError("User not found")

            access_token = self._create_token(
                data={"sub": user.id}, token_type=TokenEnum.ACCESS
            )
            return TokenSchema(
                access_token=access_token,
                refresh_token=refresh_token,
                token_type="Bearer",
            )
        except (TokenExpiredError, InvalidTokenError):
            raise

    async def validate_permissions(
        self,
        user_id: int,
        action: str,
        project_name: str = None,
        application_name: str = None,
    ):
        role = await self.project_repository.get_user_role(project_name, user_id)
        if role is None:
            raise ProjectNotFound()
        if action not in role_permission_dict[role]:
            raise InvalidPermissions(
                detail="You do not have enough permissions to perform this action."
            )
