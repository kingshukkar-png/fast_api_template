from typing import Any
from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase
from app.config.settings import settings

class MongoManager:
    def __init__(self):
        self.client: AsyncMongoClient[Any] | None = None
        self.db: AsyncDatabase[Any] | None = None

    async def connect(self):
        self.client = AsyncMongoClient(settings.MONGODB_URL)
        self.db = self.client[settings.DB_NAME]
        await self.client.admin.command("ping")

    async def disconnect(self):
        if self.client:
            await self.client.close()
            self.client = None
            self.db = None

    async def ping(self):
        if not self.client:
            raise Exception("MongoDB client is not connected.")
        await self.client.admin.command("ping")

mongo = MongoManager()
mongo_db = mongo.db