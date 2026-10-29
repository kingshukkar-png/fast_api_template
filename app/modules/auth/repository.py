from app.modules.users.models import User
from app.modules.auth.schemas import UserCreateSchema

class AuthRepository:
    async def get_user_by_email(self, email: str) -> User | None:
        return await User.find_one(User.email == email)

    async def create_user(self, user: UserCreateSchema) -> User:
        try:  
            new_user = User(**user.model_dump())
            await new_user.insert()
            return new_user
        except Exception as e:
            raise ValueError(f"Error creating user: {str(e)}")
    