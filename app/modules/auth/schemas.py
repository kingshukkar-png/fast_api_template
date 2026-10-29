from pydantic import BaseModel, EmailStr, Field
from beanie import PydanticObjectId

class UserCreateSchema(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    is_active: bool = True

class CreateUserResponseSchema(BaseModel):
    id: PydanticObjectId
    first_name: str
    last_name: str
    email: EmailStr
    is_active: bool

class LoginSchema(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)

class LoginResponseSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserDataForJwt(BaseModel):
    id: str
    email: EmailStr
    first_name: str
    last_name: str
    is_active: bool