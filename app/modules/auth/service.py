from fastapi import Depends, HTTPException, status
from app.modules.auth.schemas import CreateUserResponseSchema, LoginResponseSchema, LoginSchema, UserCreateSchema, UserDataForJwt
from app.modules.auth.repository import AuthRepository
from app.utils.security import hash_password, verify_password
from app.utils.security import generate_token
from app.modules.users.models import User

class AuthService:
    def __init__(self, auth_repo: AuthRepository = Depends(AuthRepository)):
        self.auth_repo = auth_repo

    async def generate_token(self, user: User) -> str:
        user_data = UserDataForJwt(
            id=str(user.id),
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            is_active=user.is_active
        )
        return generate_token(user_data)

    async def register(self, user: UserCreateSchema)-> CreateUserResponseSchema:
        existing_user = await self.auth_repo.get_user_by_email(user.email)
        if existing_user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists.")
        user.password = hash_password(user.password)
        new_user = await self.auth_repo.create_user(user)
        if not new_user:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="User creation failed.")
        if not new_user.id:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unable to create user properly.")
        return CreateUserResponseSchema(**new_user.model_dump())

    async def login(self, credentials: LoginSchema)->LoginResponseSchema:
        user = await self.auth_repo.get_user_by_email(credentials.email)
        if not user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email or password.")
        if not verify_password(credentials.password, user.password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email or password.")
        token = await self.generate_token(user)
        return LoginResponseSchema(access_token=token, token_type="bearer")
