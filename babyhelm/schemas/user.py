import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class AuthUserScheme(BaseModel):
    email: EmailStr
    raw_password: str


class ResponseUserScheme(BaseModel):
    id: int
    email: EmailStr
    created: datetime.datetime
    modified: datetime.datetime

    model_config = ConfigDict(from_attributes=True)
