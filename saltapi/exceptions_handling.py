# Taken from https://github.com/tiangolo/fastapi/issues/3361#issuecomment-1264208434
import traceback
from typing import Any, Union

from fastapi import FastAPI, Request, status
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse, Response
from jose import JWTError
from loguru import logger
from pydantic.error_wrappers import ValidationError as PydanticValidationError
from starlette.datastructures import URL

from saltapi.exceptions import (
    AuthorizationError,
    NotFoundError,
    ValidationError,
    AuthenticationError,
)


def log_message(method: str, url: Union[str, URL], message: Any) -> None:
    """Log a message together with the HTTP method and URL as an error."""

    logger.error(f"start error \n{method} {url} \n{message} \nend error")


def setup_exception_handler(app: FastAPI) -> None:
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException) -> Response:
        """Catch a FastAPI HTTPException."""

        log_message(request.method, request.url, exc.detail)
        return JSONResponse(
            content={"message": exc.detail},
            status_code=exc.status_code,
            headers=exc.headers,
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> Response:
        """Catch a FastAPI RequestValidationError."""

        exc_str = f"{exc}".replace("\n", " ").replace("   ", " ")
        log_message(request.method, request.url, exc)
        return JSONResponse(
            content={"message": exc_str},
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    @app.exception_handler(Exception)
    async def exception_handle(request: Request, exc: Exception) -> Response:
        """Catch an Exception."""

        log_message(request.method, request.url, traceback.format_exc())
        return JSONResponse(
            content={
                "message": "Sorry, something has gone wrong. Please try again later."
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    @app.exception_handler(NotFoundError)
    async def not_found_error_handler(request: Request, exc: NotFoundError) -> Response:
        """Catch a NotFoundError."""

        log_message(request.method, request.url, exc)
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"message": "Not Found"}
        )

    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError) -> Response:
        """Catch a ValueError."""

        log_message(request.method, request.url, exc)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"message": "Bad Request"}
        )

    @app.exception_handler(PydanticValidationError)
    async def pydantic_validation_error_handler(
        request: Request, exc: PydanticValidationError
    ) -> Response:
        """Catch a ValidationError."""

        log_message(request.method, request.url, exc)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(exc)}
        )

    @app.exception_handler(ValidationError)
    async def validation_error_handler(
        request: Request, exc: ValidationError
    ) -> Response:
        """Catch a ValidationError."""

        log_message(request.method, request.url, exc)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(exc)}
        )

    @app.exception_handler(AuthorizationError)
    async def authorization_error_handler(
        request: Request, exc: AuthorizationError
    ) -> Response:
        """Catch an AuthorizationError."""

        log_message(request.method, request.url, exc)
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN, content={"message": str(exc)}
        )

    @app.exception_handler(AuthenticationError)
    async def authentication_error_handler(
            request: Request, exc: AuthenticationError
    ) -> Response:
        """Catch an AuthenticationError."""

        log_message(request.method, request.url, exc)
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED, content={
                "message": "The authorisation token could not be parsed."
            }
        )


    @app.exception_handler(JWTError)
    async def authentication_error_handler(
            request: Request, exc: JWTError
    ) -> Response:
        """Catch an AuthenticationError."""

        log_message(request.method, request.url, exc)
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED, content={"message": str(exc)}
        )

