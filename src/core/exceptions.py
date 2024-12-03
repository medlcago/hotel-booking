from http import HTTPStatus

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError


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


async def db_exception_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:  # noqa
    return JSONResponse(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
        content={
            "message": "Oops! Something went wrong!",
        }
    )


def init_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(APIException, api_exception_handler)  # noqa
    app.add_exception_handler(SQLAlchemyError, db_exception_handler)  # noqa


class BadRequestException(APIException):
    status_code = HTTPStatus.BAD_REQUEST.value
    message = HTTPStatus.BAD_REQUEST.phrase
    description = HTTPStatus.BAD_REQUEST.description


class UnauthorizedException(APIException):
    status_code = HTTPStatus.UNAUTHORIZED.value
    message = HTTPStatus.UNAUTHORIZED.phrase
    description = HTTPStatus.UNAUTHORIZED.description


class ConflictException(APIException):
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


class BadCredentials(UnauthorizedException):
    description = "Invalid email or password."


class UserNotVerified(UnauthorizedException):
    description = "Your account has not been verified. Please check your email."


class UserAlreadyVerified(BadRequestException):
    description = "Your account has already been verified."


class UserInactive(ForbiddenException):
    description = "Your account has been disabled. Please contact support."


class UserAlreadyExists(ConflictException):
    description = "User already exists."


class RoomNotFound(NotFoundException):
    description = "Room not found."


class RoomAlreadyBooked(BadRequestException):
    description = "Room already booked."


class BookingNotFound(NotFoundException):
    description = "Booking not found."


class BookingCancelNotAllowed(ForbiddenException):
    description = "Cancel booking is not allowed."


class HotelNotFound(NotFoundException):
    description = "Hotel not found."


class ReviewAlreadyExists(ConflictException):
    description = "A review has already been submitted."


class ReviewDeleteNotAllowed(ForbiddenException):
    description = "You have not allowed to delete this review."


class LinkExpired(BadRequestException):
    description = "The link has expired."
