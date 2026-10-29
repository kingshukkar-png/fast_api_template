from pydantic import EmailStr
from datetime import datetime
from beanie import Document
from pymongo import IndexModel, ASCENDING

class User(Document):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    is_active: bool = True
    created_at: datetime = datetime.now()
    updated_at: datetime | None = None
    deleted_at: datetime | None = None

    class Settings:
        name = "users"

        indexes = [
            IndexModel([("email", ASCENDING)], unique=True)
        ]


