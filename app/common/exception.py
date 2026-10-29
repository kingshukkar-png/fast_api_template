from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from app.common.response import error_response_handler

def exception_handler(app: FastAPI):

    @app.exception_handler(HTTPException)
    def http_exception_handler(request: Request, execption: HTTPException) -> JSONResponse:
        return error_response_handler(status_code=execption.status_code, error=execption.detail)

    @app.exception_handler(Exception)
    def unhandled_exception_handler(request: Request, exception: Exception) -> JSONResponse:
        return error_response_handler(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error="Internal Server Error")