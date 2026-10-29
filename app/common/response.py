from fastapi.responses import JSONResponse
from app.common.schemas import ResponseSchema
from typing import Any
from app.common.schemas import ErrorResponseSchema

def success_response_handler(data: Any = None, message:str = "Success", status_code: int = 200) -> JSONResponse:
    content = ResponseSchema(success=True, data=data, message=message)
    return JSONResponse(content=content.model_dump(mode='json'), status_code=status_code)

def error_response_handler(status_code:int, error: str) -> JSONResponse:
    content = ErrorResponseSchema(success=False, error=error)
    return JSONResponse(content=content.model_dump(mode='json'), status_code=status_code)
