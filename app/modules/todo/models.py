from datetime import datetime
from beanie import Document, PydanticObjectId
from pymongo import IndexModel, ASCENDING
from pydantic import BaseModel, EmailStr

class TodoUser(BaseModel):
    id: PydanticObjectId
    first_name: str
    last_name: str
    email: EmailStr

class Todo(Document):
    title: str
    user: TodoUser
    description: str | None = None
    completed: bool = False
    created_at: datetime = datetime.now()
    updated_at: datetime | None = None
    deleted_at: datetime | None = None

    class Settings:
        name = "todos"
        indexes = [
            IndexModel([("user.id", ASCENDING)]),
            IndexModel([("title", ASCENDING)]),
        ]