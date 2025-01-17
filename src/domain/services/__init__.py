from .auth import IAuthService
from .booking import IBookingService
from .email import IEmailService
from .hotel import IHotelService
from .review import IReviewService
from .room import IRoomService
from .user import IUserService

__all__ = (
    "IAuthService",
    "IBookingService",
    "IEmailService",
    "IHotelService",
    "IReviewService",
    "IRoomService",
    "IUserService",
)
