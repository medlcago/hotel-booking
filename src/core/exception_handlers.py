from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from starlette.responses import JSONResponse
from yookassa.domain.exceptions import ApiError as YookassaApiError

from core.exceptions import APIException
from schemas.response import APIResponse

if TYPE_CHECKING:
    from fastapi import FastAPI, Request


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:  # noqa
    response = APIResponse(
        ok=False,
        error=exc.detail
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=response.model_dump(exclude_none=True),
        headers=exc.headers
    )


async def api_exception_handler(request: Request, exc: APIException) -> JSONResponse:  # noqa
    response = APIResponse(
        ok=False,
        error=exc.description
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=response.model_dump(exclude_none=True),
        headers=exc.headers
    )


async def db_exception_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:  # noqa
    response = APIResponse(
        ok=False,
        error="Oops! Something went wrong!"
    )
    return JSONResponse(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
        content=response.model_dump(exclude_none=True)
    )


async def yookassa_api_exception_handler(request: Request, exc: YookassaApiError) -> JSONResponse:  # noqa
    response = APIResponse(
        ok=False,
        error=exc.content.get("description", "yookassa api error")
    )
    return JSONResponse(
        status_code=exc.HTTP_CODE,
        content=response.model_dump(exclude_none=True)
    )


def init_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(HTTPException, http_exception_handler)  # noqa
    app.add_exception_handler(APIException, api_exception_handler)  # noqa
    app.add_exception_handler(SQLAlchemyError, db_exception_handler)  # noqa
    app.add_exception_handler(YookassaApiError, yookassa_api_exception_handler)  # noqa
