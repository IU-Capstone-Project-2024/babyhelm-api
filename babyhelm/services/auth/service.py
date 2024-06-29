from datetime import datetime, timedelta

import bcrypt
import jwt

from babyhelm.exceptions.auth import (
    InvalidCredentialsError,
    InvalidTokenError,
    TokenExpiredError,
)
from babyhelm.models import User
from babyhelm.repositories.user import UserRepository
from babyhelm.schemas.auth import TokenEnum, TokenSchema
from babyhelm.schemas.user import ResponseUserScheme


class AuthService:
    def __init__(
        self,
        secret_key: str,
        access_token_expiration: int,
        refresh_token_expiration: int,
        user_repository: UserRepository,
        algorithm: str = "HS256",
    ):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expiration = access_token_expiration
        self.refresh_token_expiration = refresh_token_expiration

        self.user_repository = user_repository

    def hash_password(self, password: str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode(), salt)
        return hashed.decode()

    def verify_password(self, password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode(), hashed_password.encode())

    def create_token(self, data: dict, token_type: TokenEnum) -> str:
        if token_type == TokenEnum.ACCESS:
            expire = datetime.utcnow() + timedelta(minutes=self.access_token_expiration)
        elif token_type == TokenEnum.REFRESH:
            expire = datetime.utcnow() + timedelta(days=self.refresh_token_expiration)
        data.update({"exp": expire})
        encoded_jwt = jwt.encode(data, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def decode_jwt(self, token: str) -> dict:
        try:
            decoded_token = jwt.decode(
                token, self.secret_key, algorithms=[self.algorithm]
            )
            return decoded_token
        except jwt.ExpiredSignatureError:
            raise TokenExpiredError()
        except jwt.InvalidTokenError:
            raise InvalidTokenError()

    async def authenticate_user(self, email: str, password: str) -> TokenSchema:
        user: ResponseUserScheme = await self.user_repository.get(User.email == email)
        if not user or not self.verify_password(password, user.hashed_password):
            raise InvalidCredentialsError()

        access_token = self.create_token(
            data={"sub": user.id}, token_type=TokenEnum.ACCESS
        )
        refresh_token = self.create_token(
            data={"sub": user.id}, token_type=TokenEnum.REFRESH
        )

        return TokenSchema(
            access_token=access_token, refresh_token=refresh_token, token_type="Bearer"
        )

    async def refresh_access_token(self, refresh_token: str) -> str:
        try:
            decoded_token = self.decode_jwt(refresh_token)
            user_id = decoded_token.get("sub")
            if not user_id:
                raise InvalidTokenError("Invalid token")

            user = await self.user_repository.get_by_id(user_id)
            if not user:
                raise InvalidCredentialsError("User not found")

            access_token = self.create_token(data={"sub": user.id}, token_type=TokenEnum.ACCESS)
            return access_token
        except (TokenExpiredError, InvalidTokenError):
            raise