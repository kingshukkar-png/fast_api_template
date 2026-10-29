from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from app.config.settings import settings
from app.db.mongo import mongo
from beanie import init_beanie # type: ignore
from app.modules.todo.models import Todo
from app.modules.users.models import User
from app.common.exception import exception_handler

from app.api.v1.router import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Connect to MongoDB
    await mongo.connect()
    await mongo.ping()
    if mongo.db is None:
        raise Exception("MongoDB database is not initialized.")
    await init_beanie(database=mongo.db, document_models=[User,Todo])
    yield
    # Disconnect from MongoDB
    await mongo.disconnect()

app = FastAPI(
    title=settings.TITLE,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    docs_url="/docs" if settings.ENVIRONMENT == "development" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT == "development" else None,
    openapi_url="/openapi.json" if settings.ENVIRONMENT == "development" else None,
    lifespan=lifespan
)

app.include_router(api_router)
exception_handler(app)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=settings.PORT, reload=True)