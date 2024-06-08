from pydantic import BaseModel, EmailStr


class CreateUser(BaseModel):
    email: EmailStr
    raw_password: str
