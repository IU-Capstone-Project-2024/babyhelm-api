import datetime

from pydantic import BaseModel, ConfigDict, EmailStr

USER_EXAMPLE = {
    "id": 1,
    "email": "string@gmail.com",
}


class AuthUserScheme(BaseModel):
    email: EmailStr
    raw_password: str


class ResponseUserScheme(BaseModel):
    id: int
    email: EmailStr
    created: datetime.datetime
    modified: datetime.datetime
    hashed_password: str

    model_config = ConfigDict(from_attributes=True)


class UserSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True, json_schema_extra={"examples": [USER_EXAMPLE]}
    )

    id: int
    email: EmailStr
