import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, ConfigDict, Field

from babyhelm.schemas.namespace import Metadata


class AuthUserScheme(BaseModel):
    email: EmailStr
    raw_password: str


class ViewUserScheme(BaseModel):
    id: int
    email: EmailStr
    created: datetime.datetime
    modified: datetime.datetime

    model_config = ConfigDict(from_attributes=True)
