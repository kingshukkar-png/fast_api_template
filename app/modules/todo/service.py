from fastapi import Depends, HTTPException, status
from app.common.list_query_params import PaginatedResponseSchema
from app.modules.todo.repository import TodoRepository
from app.modules.todo.schemas import CreateTodoSchema, CreateTodoResponseSchema, ListTodoQueryParamsSchema
from app.modules.users.models import User

class TodoService: 
    def __init__(self, todo_repo: TodoRepository = Depends(TodoRepository)):
        self.todo_repo = todo_repo

    async def create_todo(self, todo_data: CreateTodoSchema, user: User) -> CreateTodoResponseSchema:
        new_todo = await self.todo_repo.create_todo(todo_data, user)
        return CreateTodoResponseSchema(**new_todo.model_dump())

    async def list_todos(self, params: ListTodoQueryParamsSchema, user: User)->PaginatedResponseSchema[CreateTodoResponseSchema]:
        todos, total = await self.todo_repo.list_todos(params, user)
        todo_response_list = [CreateTodoResponseSchema(**todo.model_dump()) for todo in todos]
        return PaginatedResponseSchema[CreateTodoResponseSchema].build_response(todo_response_list, total, params)

    async def get_todo(self, todo_id: str, user: User) -> CreateTodoResponseSchema:
        todo = await self.todo_repo.get_todo_by_id(todo_id, user)
        if not todo:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found.")
        return CreateTodoResponseSchema(**todo.model_dump())

    async def delete_todo(self, todo_id: str, user: User) -> None:
        todo = await self.todo_repo.get_todo_by_id(todo_id, user)
        if not todo:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found.")
        await self.todo_repo.delete_todo(todo)

    async def update_todo(self, todo_id: str, todo_data: CreateTodoSchema, user: User) -> CreateTodoResponseSchema:
        todo = await self.todo_repo.get_todo_by_id(todo_id, user)
        if not todo:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found.")
        updated_todo = await self.todo_repo.update_todo(todo, todo_data)
        return CreateTodoResponseSchema(**updated_todo.model_dump())

    async def update_completed_status(self, todo_id: str, completed: bool, user: User) -> CreateTodoResponseSchema:
        todo = await self.todo_repo.get_todo_by_id(todo_id, user)
        if not todo:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found.")
        updated_todo = await self.todo_repo.update_completed_status(todo, completed)
        return CreateTodoResponseSchema(**updated_todo.model_dump())