from fastapi import APIRouter

user_router = APIRouter()

@user_router.get("/")
async def get_users():
    return {"message": "List of users"}