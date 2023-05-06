from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr = Field(..., example="example@company.com")
    username: str = Field(..., min_length=4, max_length=50, example="Username")


class User(UserBase):
    id: int = Field(..., example="1")


class UserRegister(UserBase):
    password: str = Field(
        ..., min_length=8, max_length=64, example="strongpass123"
    )
