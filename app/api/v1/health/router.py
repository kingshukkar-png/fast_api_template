from fastapi import APIRouter
from app.common.schemas import ResponseSchema
from app.config.settings import settings
from app.db.mongo import mongo

health_router = APIRouter()

@health_router.get("/", response_model=ResponseSchema[dict[str, str]])
async def health_check():
    await mongo.ping()
    return ResponseSchema(
        success=True,
        data={
            "app_status": f"{settings.TITLE} is running.",
            "database_status": "MongoDB is connected."
        },
        message="Health check successful."
    )
