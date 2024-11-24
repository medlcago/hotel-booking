from http import HTTPStatus

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse


class APIException(Exception):
    status_code: int = HTTPStatus.INTERNAL_SERVER_ERROR.value
    message: str = HTTPStatus.INTERNAL_SERVER_ERROR.phrase
    description: str = HTTPStatus.INTERNAL_SERVER_ERROR.description

    def __init__(self, description: str | None = None):
        if description is not None:
            self.description = description

    def __str__(self) -> str:
        return f"<{self.status_code} - {self.message}>: {self.description}"

    @property
    def details(self):
        return {
            "status_code": self.status_code,
            "message": self.message,
            "description": self.description,
        }


async def api_exception_handler(request: Request, exc: APIException) -> JSONResponse:  # noqa
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.details
    )


def init_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(APIException, api_exception_handler)  # noqa


class BadRequestException(APIException):
    status_code = HTTPStatus.BAD_REQUEST.value
    message = HTTPStatus.BAD_REQUEST.phrase
    description = HTTPStatus.BAD_REQUEST.description


class UnauthorizedException(APIException):
    status_code = HTTPStatus.UNAUTHORIZED.value
    message = HTTPStatus.UNAUTHORIZED.phrase
    description = HTTPStatus.UNAUTHORIZED.description


class AlreadyExistsException(APIException):
    status_code = HTTPStatus.CONFLICT.value
    message = HTTPStatus.CONFLICT.phrase
    description = HTTPStatus.CONFLICT.description


class NotFoundException(APIException):
    status_code = HTTPStatus.NOT_FOUND.value
    message = HTTPStatus.NOT_FOUND.phrase
    description = HTTPStatus.NOT_FOUND.description


class ForbiddenException(APIException):
    status_code = HTTPStatus.FORBIDDEN.value
    message = HTTPStatus.FORBIDDEN.phrase
    description = HTTPStatus.FORBIDDEN.description
