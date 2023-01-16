# Taken from https://github.com/tiangolo/fastapi/issues/3361#issuecomment-1264208434
import traceback
from typing import Any, Union

from fastapi import FastAPI, Request, status
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse, Response
from loguru import logger
from pydantic.error_wrappers import ValidationError
from starlette.datastructures import URL

from saltapi.exceptions import AuthorizationError, NotFoundError


def log_message(method: str, url: Union[str, URL], message: Any):
    """log message when catch exception"""

    logger.error('start error, this is'.center(60, '*'))
    logger.error(f'{method} {url}')
    logger.error(message)
    logger.error('end error'.center(60, '*'))


def setup_exception_handler(app: FastAPI):
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        """catch FastAPI HTTPException"""

        log_message(request.method, request.url, exc.detail)
        return JSONResponse(content={"message": exc.detail}, status_code=exc.status_code, headers=exc.headers)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """catch FastAPI RequestValidationError"""

        exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
        log_message(request.method, request.url, exc)
        return JSONResponse(content={"message": exc_str}, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

    @app.exception_handler(Exception)
    async def exception_handle(request: Request, exc: Exception):
        """catch other exception"""

        log_message(request.method, request.url, traceback.format_exc())
        return JSONResponse(content={"message": str(exc)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @app.exception_handler(NotFoundError)
    async def not_found_error_handler(request: Request, exc: NotFoundError) -> Response:
        log_message(request.method, request.url, exc)
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Not Found"})


    @app.exception_handler(ValidationError)
    async def validation_error_handler(request: Request, exc: ValidationError) -> Response:
        log_message(request.method, request.url, exc)
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": str(exc)})


    @app.exception_handler(AuthorizationError)
    async def authorization_error_handler(
            request: Request, exc: AuthorizationError
    ) -> Response:
        log_message(request.method, request.url, exc)
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"message": "Forbidden"})
