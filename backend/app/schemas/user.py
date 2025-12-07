from pydantic import BaseModel, EmailStr, Field
from uuid import UUID

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(min_length=8)

class UserResponse(UserBase):
    id: UUID
    is_active: bool

    class Config:
        from_attributes = True

class UserResponseWrapper(BaseModel):
    data: UserResponse
