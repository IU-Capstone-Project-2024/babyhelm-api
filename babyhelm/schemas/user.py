import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class AuthUserSchema(BaseModel):
    email: EmailStr
    raw_password: str


class ResponseUserSchema(BaseModel):
    id: int
    email: EmailStr
    created: datetime.datetime
    modified: datetime.datetime
    hashed_password: str

    model_config = ConfigDict(from_attributes=True)
