from pydantic import BaseModel, EmailStr


class CreateUser(BaseModel):
    email: EmailStr
    row_password: str
