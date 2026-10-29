from fastapi import APIRouter

from app.api.v1.health.router import health_router
from app.api.v1.user.router import user_router
from app.api.v1.auth.router import auth_router
from app.api.v1.todo.router import todo_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(health_router, prefix="", tags=["Health"])
api_router.include_router(user_router, prefix="/users", tags=["User"])
api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
api_router.include_router(todo_router, prefix="/todos", tags=["Todo"])