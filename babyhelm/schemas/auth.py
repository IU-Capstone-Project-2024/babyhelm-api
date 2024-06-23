from enum import StrEnum

from pydantic import BaseModel


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenEnum(StrEnum):
    ACCESS = "access"
    REFRESH = "refresh"
