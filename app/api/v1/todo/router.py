from fastapi import APIRouter, status, Depends
from app.api.deps import get_current_active_user
from app.common.list_query_params import PaginatedResponseSchema
from app.modules.todo.schemas import CreateTodoSchema, CreateTodoResponseSchema, ListTodoQueryParamsSchema, UpdateCompletedStatusSchema
from app.common.schemas import ResponseSchema
from app.modules.users.models import User
from app.modules.todo.service import TodoService
from app.common.response import success_response_handler

todo_router = APIRouter()

@todo_router.post("/", response_model=ResponseSchema[CreateTodoResponseSchema], status_code=status.HTTP_201_CREATED)
async def create_todo(todo_data: CreateTodoSchema, current_user: User = Depends(get_current_active_user), todo_service: TodoService = Depends(TodoService)):
    new_todo = await todo_service.create_todo(todo_data, current_user)
    return success_response_handler(data=new_todo, message="Todo created successfully.", status_code=status.HTTP_201_CREATED)

@todo_router.get("/", response_model=ResponseSchema[PaginatedResponseSchema[CreateTodoResponseSchema]], status_code=status.HTTP_200_OK)
async def list_todos(params: ListTodoQueryParamsSchema = Depends(ListTodoQueryParamsSchema), current_user: User = Depends(get_current_active_user),todo_service: TodoService = Depends(TodoService)):
    todos_response = await todo_service.list_todos(params, current_user)
    return success_response_handler(data=todos_response, message="Todos retrieved successfully.", status_code=status.HTTP_200_OK)

@todo_router.get("/{todo_id}", response_model=ResponseSchema[CreateTodoResponseSchema], status_code=status.HTTP_200_OK)
async def get_todo(todo_id: str, current_user: User = Depends(get_current_active_user), todo_service: TodoService = Depends(TodoService)):
    todos_response = await todo_service.get_todo(todo_id, current_user)
    return success_response_handler(data=todos_response, message="Todo retrieved successfully.", status_code=status.HTTP_200_OK)

@todo_router.delete("/{todo_id}", response_model=ResponseSchema[None], status_code=status.HTTP_200_OK)
async def delete_todo(todo_id: str, current_user: User = Depends(get_current_active_user), todo_service: TodoService = Depends(TodoService)):
    await todo_service.delete_todo(todo_id, current_user)
    return success_response_handler(data=None, message="Todo deleted successfully.", status_code=status.HTTP_200_OK)

@todo_router.put("/{todo_id}", response_model=ResponseSchema[CreateTodoResponseSchema], status_code=status.HTTP_200_OK)
async def update_todo(todo_id: str, todo_data: CreateTodoSchema, current_user: User = Depends(get_current_active_user), todo_service: TodoService = Depends(TodoService)):
    updated_todo = await todo_service.update_todo(todo_id, todo_data, current_user)
    return success_response_handler(data=updated_todo, message="Todo updated successfully.", status_code=status.HTTP_200_OK)


@todo_router.patch("/{todo_id}/completed", response_model=ResponseSchema[CreateTodoResponseSchema], status_code=status.HTTP_200_OK)
async def update_completed_status(todo_id: str, completed_status: UpdateCompletedStatusSchema, current_user: User = Depends(get_current_active_user), todo_service: TodoService = Depends(TodoService)):
    updated_todo = await todo_service.update_completed_status(todo_id, completed_status.completed, current_user)
    return success_response_handler(data=updated_todo, message="Todo completed status updated successfully.", status_code=status.HTTP_200_OK)