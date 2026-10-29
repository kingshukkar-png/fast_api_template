import re
from app.common.list_query_params import SortOrder
from app.modules.todo.schemas import CreateTodoSchema, ListTodoQueryParamsSchema
from app.modules.users.models import User
from app.modules.todo.models import Todo, TodoUser
from beanie import PydanticObjectId
from beanie.operators import Or, RegEx
from datetime import datetime
from typing import List, Any

class TodoRepository:
    async def create_todo(self, todo_data: CreateTodoSchema, user: User) -> Todo:
        todo_user = TodoUser(
            id=PydanticObjectId(user.id),
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email
        )
        new_todo = Todo(
            title=todo_data.title,
            description=todo_data.description,
            completed=todo_data.completed,
            user=todo_user,
            created_at=datetime.now()
        )
        await new_todo.insert()
        return new_todo

    async def list_todos(self, params: ListTodoQueryParamsSchema, user: User)-> tuple[List[Todo], int]:
        filters: List[Any] = [
            Todo.user.id == PydanticObjectId(user.id),
            Todo.deleted_at == None
        ]
        if params.completed is not None:
            filters.append(Todo.completed == params.completed)
        if params.search:
            pattern = re.escape(params.search.strip())
            filters.append(
                Or(
                    RegEx(Todo.title, pattern, options="i"),
                    RegEx(Todo.description, pattern, options="i")
                )
            )
        query = Todo.find(*filters)
        total = await query.count()
        TODO_SORT_FIELDS: dict[str, Any] = {
            "title":      Todo.title,
            "completed":  Todo.completed,
            "created_at": Todo.created_at,
            "updated_at": Todo.updated_at,
        }
        sort_field = TODO_SORT_FIELDS.get(params.sort_by or "created_at", Todo.created_at)
        sort_expr  = sort_field if params.sort_order == SortOrder.ASCENDING else -sort_field
        todos = await query.sort(sort_expr).skip(params.skip()).limit(params.limit()).to_list()
        return todos, total

    async def get_todo_by_id(self, todo_id: str, user: User) -> Todo | None:
        todo = await Todo.find_one(
            Todo.id == PydanticObjectId(todo_id),
            Todo.user.id == PydanticObjectId(user.id),
            Todo.deleted_at == None
        )
        return todo

    async def delete_todo(self, todo: Todo) -> None:
        todo.deleted_at = datetime.now()
        await todo.save()

    async def update_todo(self, todo: Todo, todo_data: CreateTodoSchema) -> Todo:
        todo.title = todo_data.title
        todo.description = todo_data.description
        todo.completed = todo_data.completed
        todo.updated_at = datetime.now()
        await todo.save()
        return todo

    async def update_completed_status(self, todo: Todo, completed: bool) -> Todo:
        todo.completed = completed
        todo.updated_at = datetime.now()
        await todo.save()
        return todo