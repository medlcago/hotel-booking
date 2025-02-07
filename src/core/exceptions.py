from http import HTTPStatus


class APIException(Exception):
    status_code: int = HTTPStatus.INTERNAL_SERVER_ERROR.value
    message: str = HTTPStatus.INTERNAL_SERVER_ERROR.phrase
    description: str = HTTPStatus.INTERNAL_SERVER_ERROR.description

    def __init__(
            self,
            description: str | None = None,
            headers: dict[str, str] | None = None
    ):
        if description is not None:
            self.description = description
        self.headers = headers

    def __str__(self) -> str:
        return f"<{self.status_code} - {self.message}>: {self.description}"

    @property
    def details(self):
        return {
            "status_code": self.status_code,
            "message": self.message,
            "description": self.description,
        }


class TooManyRequestsException(APIException):
    status_code = HTTPStatus.TOO_MANY_REQUESTS.value
    message = HTTPStatus.TOO_MANY_REQUESTS.phrase
    description = HTTPStatus.TOO_MANY_REQUESTS.description


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
    description = "Bad credentials."


class UserNotVerified(UnauthorizedException):
    description = "Your account has not been verified. Please check your email."


class UserNotFound(NotFoundException):
    description = "User not found."


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


class BookingConfirmNotAllowed(ForbiddenException):
    description = "Confirm booking is not allowed."


class HotelNotFound(NotFoundException):
    description = "Hotel not found."


class ReviewAlreadyExists(ConflictException):
    description = "A review has already been submitted."


class ReviewDeleteNotAllowed(ForbiddenException):
    description = "You have not allowed to delete this review."


class TokenExpired(BadRequestException):
    description = "The token has expired."


class InvalidCode(BadRequestException):
    description = "Invalid code."


class CodeAlreadySent(TooManyRequestsException):
    description = "Code has already been sent!"


class PaymentNotFound(NotFoundException):
    description = "Payment not found."
