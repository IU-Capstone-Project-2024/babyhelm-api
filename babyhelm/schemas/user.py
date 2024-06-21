from pydantic import BaseModel, EmailStr


class CreateUser(BaseModel):
    email: EmailStr
    raw_password: str

class UserSchema(BaseModel):
    email: str
    raw_password: str

class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str