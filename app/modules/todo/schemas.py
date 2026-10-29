from beanie import PydanticObjectId
from pydantic import BaseModel, Field
from datetime import datetime
from app.modules.todo.models import TodoUser
from app.common.list_query_params import ListQueryParamsSchema

class CreateTodoSchema (BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: str | None = Field(None, max_length=1000)
    completed: bool = Field(False)

class UpdateCompletedStatusSchema (BaseModel):
    completed: bool = Field(...)

class CreateTodoResponseSchema (BaseModel):
    id: PydanticObjectId
    title: str
    user: TodoUser
    description: str | None
    completed: bool
    created_at: datetime
    updated_at: datetime | None

class ListsTodoResponseSchema (BaseModel):
    todos: list[CreateTodoResponseSchema]
    total: int
    page: int
    page_size: int

class ListTodoQueryParamsSchema (ListQueryParamsSchema):
    completed: bool | None = Field(None)