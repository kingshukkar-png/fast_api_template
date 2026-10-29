from fastapi import APIRouter, Depends, status
from app.common.schemas import ResponseSchema
from app.modules.auth.schemas import LoginResponseSchema, UserCreateSchema, CreateUserResponseSchema, LoginSchema
from app.modules.auth.service import AuthService
from app.common.response import success_response_handler

auth_router = APIRouter()

@auth_router.post("/login", response_model=ResponseSchema[LoginResponseSchema], status_code=status.HTTP_200_OK)
async def login(credentials: LoginSchema, auth_service: AuthService = Depends(AuthService)):
    token_data = await auth_service.login(credentials)
    return success_response_handler(data=token_data, message="Login successful.")

@auth_router.post("/register", response_model=ResponseSchema[CreateUserResponseSchema], status_code=status.HTTP_201_CREATED)
async def user_registration(user: UserCreateSchema, auth_service: AuthService = Depends(AuthService)):
    user_data = await auth_service.register(user)
    return success_response_handler(data=user_data, message="User registered successfully.")