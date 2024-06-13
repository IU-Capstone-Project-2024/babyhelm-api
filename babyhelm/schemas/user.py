from pydantic import BaseModel, EmailStr


class CreateUser(BaseModel):
    email: EmailStr
    raw_password: str

class UserSchema(BaseModel):
    username: str
    row_password: str

class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str